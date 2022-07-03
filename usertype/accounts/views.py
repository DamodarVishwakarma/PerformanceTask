from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomerSignUpForm, LoginForm, StaffSignUpForm, ManagerSignUpForm
from accounts.models import Staff, User,Pet,Manager, Customer
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,  TemplateView
from accounts.decorators import customer_required, staff_required, manager_required
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class CustomerSignUpView(CreateView):
    model = Customer
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.CUSTOMER)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)
        


class StaffSignUpView(CreateView):
    model = Staff
    form_class = StaffSignUpForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('login')
   

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.STAFF)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)
        


class ManagerSignUpView(CreateView):
    model = Manager
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.SELLER)
        user.save()
        form.instance.user = self.request.MANAGER
        return super().form_valid(form)
        

def home(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            return render('pets/pet_list')
        if request.user.is_staff:
            return render('pets/staff_pet_list')
        else:
            return render('pets/manager_pet_list')
    else:
        return render(request, 'home.html')

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")

@method_decorator([login_required], name='dispatch')
class PetListView(ListView):
    model = Pet
    ordering = ('name', )
    context_object_name = 'pets'
    template_name = 'pets/pet_list.html'

    def get_context_data(self, **kwargs):
        context_data= super().get_context_data(**kwargs)
        context_data['pets'] = Pet.objects.all()
        return context_data


@method_decorator([login_required, customer_required], name='dispatch')
class PetCreateView(CreateView, PermissionRequiredMixin):
    model = Pet
    fields = ('owner', 'name', 'room_number' )
    template_name = 'pets/pet_add_form.html'
    permission_required = ('accounts.add_pet', 'accounts.change_pet', 'accounts.delete_pet')

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.owner = self.request.user
        pet.save()
        return redirect('pet_list')

@method_decorator([login_required, customer_required], name='dispatch')
class PetCustomerUpdateView(UpdateView):
    model = Pet
    fields = ('owner', 'name', 'room_number')
    context_object_name = 'pets'
    template_name = 'pets/pet_change_form.html'
  

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.pets.all()

    def get_success_url(self):
        return reverse('pet_list', kwargs={'pk': self.object.pk})

@method_decorator([login_required, staff_required], name='dispatch')
class PetStaffUpdateView(UpdateView, PermissionRequiredMixin):
    model = Pet
    fields = ('owner', 'name', 'room_number')
    context_object_name = 'pets'
    template_name = 'pets/pet_change_form.html'
    permission_required = ('accounts.add_pet', 'accounts.change_pet', 'accounts.view_pet')

    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.pets.all()

    def get_success_url(self):
        return reverse('pet_list', kwargs={'pk': self.object.pk})

    # search pet
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        
        keyword = self.request.GET.get('keyword')
        if keyword:
            return queryset.filter(name__icontains = keyword)
        return queryset


@method_decorator([login_required, manager_required], name='dispatch')
class PetManagerUpdateView(UpdateView, PermissionRequiredMixin):
    model = Pet
    fields = ('owner', 'name', 'room_number')
    context_object_name = 'pets'
    template_name = 'pets/pet_change_form.html'
    permission_required = ('accounts.add_pet', 'accounts.change_pet', 'accounts.view_pet')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.pets.all()

    def get_success_url(self):
        return reverse('pet_list', kwargs={'pk': self.object.pk})

    # search pet
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        
        keyword = self.request.GET.get('keyword')
        if keyword:
            return queryset.filter(name__icontains = keyword)
        return queryset


@method_decorator([login_required, customer_required], name='dispatch')
class PetCustomerDeleteView(DeleteView):
    model = Pet
    context_object_name = 'pets'
    template_name = 'pets/pet_delete_confirm.html'
    success_url = reverse_lazy('pet_list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.pets.all()


@method_decorator([login_required, manager_required], name='dispatch')
class PetManagerDeleteView(DeleteView, PermissionRequiredMixin):
    model = Pet
    context_object_name = 'pets'
    template_name = 'pets/pet_delete_confirm.html'
    success_url = reverse_lazy('pet_list')
    permission_required = ('accounts.add_pet', 'accounts.change_pet', 'accounts.view_pet', 'accounts.delete_pet')


    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.pets.all()

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            unauthenticated_user = None
            user = None
            
            try:
                unauthenticated_user = Customer.objects.get(username=form.cleaned_data["username"].lower())
                user = authenticate(request, username=unauthenticated_user.username, password=form.cleaned_date["password"])
            except User.DoesNotExist:

                pass

        if not user:
            form.add_error(field="username", error="Wrong password or unknown username. Please try again.")
           
            if unauthenticated_user:
                unauthenticated_user.logins_failed += 1
                unauthenticated_user.save()

        elif user.logins_failed >= 3:
            form.add_error(field=None, error="You're blocked due to too many attempts. Contact your admin.")

        else:
            login(request, user)
            user.logins_failed = 0
            user.save()

            return redirect(reverse("home"))

    else:
        form = LoginForm()
    
    return render(request, "userlogin.html", {"form": form})


class SendEmailView(View):
    model = User
    template_name = 'registration/send_email.html'
    success_url = reverse_lazy('home')

class SendEmailConfirmView(View):
    model = User
    template_name = 'registration/send_email_confirm.html'
    success_url = reverse_lazy('home')

