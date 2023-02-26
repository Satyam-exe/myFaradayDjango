from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import CustomFirebaseUserManager


class CustomFirebaseUser(AbstractBaseUser):
    firebase_uid = models.CharField(max_length=255, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomFirebaseUserManager()

    USERNAME_FIELD = 'firebase_uid'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name', 'phone_number']
