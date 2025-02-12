from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.utils import timezone
from uuid import uuid4
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

"""
After overriding the default user model, we implement the UserManager for this new 
model. It provides the methods for creating both the users and the super users.
"""

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError('The Password field must be set')
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    email = models.EmailField(verbose_name='email address',max_length=150,unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    """
    the users are managed on a basis of groups. i.e, the customers and the 
    admins as well as the product managers
    """
    group = models.ForeignKey(Group, related_name='users', blank=True, on_delete=models.SET_NULL, null=True)

    objects = UserManager()

    # the primary credential that uniquely identifies all users is the email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    # the following property methods are used to check for the user's group

    @property
    def is_admin(self):
        return self.group.name == "Admin"
    
    @property
    def is_customer(self):
        return self.group.name == "Customer"


class Customer(User):
    phone = PhoneNumberField(region='KE', unique=True)
    address = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    wallet = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.00)], default=0.00)
    image = models.ImageField(upload_to="accounts/profile", default="accounts/profile/default.png")

    
class Admin(User):
    employee_id = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
