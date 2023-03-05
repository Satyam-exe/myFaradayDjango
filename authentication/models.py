from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import CustomFirebaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomFirebaseUser(AbstractBaseUser):
    firebase_uid = models.CharField(max_length=255, unique=True, primary_key=True, verbose_name=_('Firebase User ID'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    signed_up = models.DateTimeField(verbose_name=_('Signed Up'))
    last_login = models.DateTimeField(verbose_name=_('Last Login'), blank=True, null=True)
    last_activity = models.DateTimeField(verbose_name=_('Last Activity'), blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomFirebaseUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['firebase_uid', 'password', 'first_name', 'last_name', 'phone_number']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
