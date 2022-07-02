from django.urls import path
from .views import*


urlpatterns = [
    path('', home , name = 'home'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('signup/customer/',CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/staff/',StaffSignUpView.as_view(), name='staff_signup'),
    path('signup/manager/',ManagerSignUpView.as_view(), name='manager_signup'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('send_email/',SendEmailView.as_view(),name='send_email'),
    path('send_email/<uidb64>/<token>/',SendEmailConfirmView.as_view(),name='send_email_confirm'),
   
   # related to pet urls
   
    path('', PetListView.as_view(), name='pet_list'),
    path('pet/add/', PetCreateView.as_view(), name='pet_add'),
    path('pet/change/<int:pk>/', PetCustomerUpdateView.as_view(), name='pet_change'),
    path('pet/change/<int:pk>/staff/', PetStaffUpdateView.as_view(), name='pet_change_staff'),
    path('pet/change/<int:pk>/manager/', PetManagerUpdateView.as_view(), name='pet_change_manager'),
    path('pet/delete/<int:pk>/', PetCustomerDeleteView.as_view(), name='pet_delete'),
    path('pet/delete/staff/<int:pk>/', PetStaffDeleteView.as_view(), name='pet_delete_staff'),
    path('pet/delete/manager/<int:pk>/', PetManagerDeleteView.as_view(), name='pet_delete_manager'),
]
