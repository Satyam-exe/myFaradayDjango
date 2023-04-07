from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

SIGNUP_PLATFORM_CHOICES = (
    ('django', 'Django'),
    ('flutter', 'Flutter')
)


class CustomUser(AbstractBaseUser):
    uid = models.BigAutoField(primary_key=True, db_column='uid', verbose_name=_('User ID'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    is_email_verified = models.BooleanField(verbose_name=_('Is Email Verified'), default=False)
    signed_up = models.DateTimeField(verbose_name=_('Signed Up'))
    signup_platform = models.CharField(max_length=10, choices=SIGNUP_PLATFORM_CHOICES,
                                       verbose_name=_('Signup Platform'))
    last_login = models.DateTimeField(verbose_name=_('Last Login'), blank=True, null=True)
    last_activity = models.DateTimeField(verbose_name=_('Last Activity'), blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'phone_number']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class URLCode(models.Model):
    code = models.CharField(max_length=55, verbose_name=_('Code'), editable=False, primary_key=True)
    type_of_link = models.CharField(max_length=100, verbose_name=_('Type of Link'))
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name=_('User'), null=True)
    generated_at = models.DateTimeField(verbose_name=_('Generated At'))
    expires_at = models.DateTimeField(verbose_name=_('Expires At'))
    is_used = models.BooleanField(verbose_name=_('Is Used'), default=False)


class MobileAuthToken(models.Model):
    token = models.CharField(max_length=55, verbose_name=_('Token'), editable=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name=_('User'), null=True)
    generated_at = models.DateTimeField(verbose_name=_('Generated At'))
    expires_at = models.DateTimeField(verbose_name=_('Expires At'))
    is_revoked = models.BooleanField(verbose_name=_('Is Revoked'))
    last_used = models.DateTimeField(verbose_name=_('Last Used'))