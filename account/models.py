import uuid

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class CustomAccountManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def create_user(self, email, user_name, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('You must provide an email address'))

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, user_name, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_name, password, **extra_fields)
   

class Customer(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # User information
    about = models.TextField(_('about'), max_length=500, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    # postCode = models.CharField(max_length=12, blank=True)
    # address_line_1 = models.CharField(max_length=150, blank=True)
    # landMark = models.CharField(max_length=150, blank=True)
    # town_city = models.CharField(max_length=150, blank=True)
    # state = models.CharField(max_length=50, blank=True)
    # district = models.CharField(max_length=50, blank=True)

    # User Status
    is_active =  models.BooleanField(default=False)
    is_staff  =  models.BooleanField(default=False)
    created   =  models.BooleanField(default=False)
    updated   =  models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Acccounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user_name

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'admin@palavPoshak.com',
            [self.email],
            fail_silently=False,
        )



# Address
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), on_delete=models.CASCADE)
    full_name = models.CharField(_('Full Name'), max_length=150)
    mobile_number = models.CharField(_('Mobile Number'), max_length=20)
    postcode = models.CharField(_('Postcode'), max_length=10)
    address = models.CharField(_('Address'), max_length=255)
    LandMark = models.CharField(_('Land Mark'), max_length=255)
    town = models.CharField(_('Town/City'), max_length=150)
    district = models.CharField(_('District'), max_length=70)
    state = models.CharField(_('State'), max_length=70, default="")
    delivery_Instructions = models.CharField(_('Delivery Instructions'), max_length=300)
    default = models.BooleanField(_('Default'), default=False)

    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name="Address"
        verbose_name_plural="Addresses"

    def __str__(self):
        return "Address"
        


 