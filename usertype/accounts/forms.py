from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Customer, Staff, Manager


class CustomerSignUpForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ['username', 'email']
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_active = True
        user.is_customer = True
        user.save()
        return user

class StaffSignUpForm(UserCreationForm):
  
    class Meta:
        model = Staff
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.is_staff = True
        if commit:
            user.save()
        return user

class ManagerSignUpForm(UserCreationForm):
   
    class Meta:
        model = Manager
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.is_manager = True
        if commit:
            user.save()
        return user

class AuthenticationFormWithChekUsersStatus(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.status == 'enabled':
            raise forms.ValidationError(
                ("Your account has disabled."),
                code='inactive',
            )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']