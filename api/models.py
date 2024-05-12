from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser


class CustomAccountManager(BaseUserManager):
    use_in_migrations=True

    def create_superuser(self, email, username, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

    def create_user(self, email, username,  password, **extra_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)

        user = self.model(email=email, username=username,
                           **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


class NewUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
from django.contrib.auth.models import User

class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields related to properties
    img1 = models.ImageField(upload_to='item_images/')

    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
   
class properties(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    img1 = models.ImageField(upload_to='item_images/')
    img2 = models.ImageField(upload_to='item_images/')
    img3 = models.ImageField(upload_to='item_images/')
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daley_name = models.CharField(max_length=100, null=True, blank=True)
    daley_number = models.CharField(max_length=15, null=True, blank=True)
    daley_image = models.ImageField(upload_to='daley_images/')
    BikeParking = models.CharField(max_length=15, null=True, blank=True)
    CarParking = models.CharField(max_length=15, null=True, blank=True)
    AttachedBathroom = models.CharField(max_length=15, null=True, blank=True)
    Kitchen = models.CharField(max_length=15, null=True, blank=True)
    Bedroom = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    
    

    
    def __str__(self):
        return self.name   