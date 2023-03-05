import ast

import pytz
from authentication.models import CustomFirebaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models

GENDER_CHOICES = [
    ('M', _('Male')),
    ('F', _('Female')),
    ('O', _('Others')),
]

COUNTRIES_CHOICES = ast.literal_eval(
    str(
        dict(
            pytz.country_names
        ))
    .replace(',', '), (') \
    .replace(':', ',') \
    .replace('{', '((') \
    .replace('}', '))')
)


class Profile(models.Model):
    user = models.OneToOneField(CustomFirebaseUser, on_delete=models.CASCADE, primary_key=True,
                                verbose_name=_('Firebase User ID'), db_column='firebase_uid')
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name=_('Gender'), choices=GENDER_CHOICES, null=True, blank=True)
    address1 = models.CharField(max_length=50, verbose_name=_('Address 1'), null=True, blank=True)
    address2 = models.CharField(max_length=50, verbose_name=_('Address 2'), null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name=_('City'), null=True, blank=True)
    pincode = models.CharField(verbose_name=_('Postal Code'), max_length=6, null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name=_('State/Territory'), null=True, blank=True)
    country = models.CharField(max_length=2, verbose_name=_('Country'), choices=COUNTRIES_CHOICES, null=True,
                               blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Longitude'), null=True,
                                    blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Latitude'), null=True, blank=True)
    profile_picture = models.ImageField(verbose_name=_('Profile Picture'), null=True, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
