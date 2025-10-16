from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('guest', 'Guest'),
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='user'
    )
    is_details_saved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['name', 'role']
    objects = CustomUserManager() 
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return self.email