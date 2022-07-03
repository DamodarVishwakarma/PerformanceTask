from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Q

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)                
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class LowercaseEmailField(models.EmailField):

    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

class User(AbstractUser):

    email =LowercaseEmailField(max_length=50, unique=True)
    username = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Types(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        STAFF = "STAFF", "Staff"
        MANAGER = "MANAGER", "Manager"

    base_type = Types.CUSTOMER

    type = models.CharField(max_length=100,choices=Types.choices, default=base_type)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)


class CustomerAdditional(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class StaffAdditional(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class ManagerAdditional(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = User.Types.CUSTOMER))

class StaffManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = User.Types.STAFF))

class ManagerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = User.Types.MANAGER))

class Customer(User):
    default_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True 

    @property
    def showAdditional(self):
        return self.customeradditional

    @property
    def is_customer(self):
        return str(self.user_type) == self.default_type

class Staff(User):
    default_type = User.Types.STAFF
    objects = StaffManager()
    
    class Meta:
        proxy = True 

    @property
    def showAdditional(self):
        return self.staffadditional

    @property
    def is_staff(self):
        return str(self.user_type) == self.default_type


class Manager(User):
    default_type = User.Types.MANAGER
    objects = ManagerManager()
    
    class Meta:
        proxy = True 

    @property
    def showAdditional(self):
        return self.manageradditional

    @property
    def is_manager(self):
        return str(self.user_type) == self.default_type



class Pet(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    room_number = models.IntegerField()

    def __str__(self):
        return self.name
