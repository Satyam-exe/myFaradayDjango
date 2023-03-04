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

COUNTRIES_CHOICES = \
    ast.literal_eval(
        str(
            dict(
                pytz.country_names
            )).replace(',', '), (') \
              .replace(':', ',')    \
              .replace('{', '((')   \
              .replace('}', '))')
    )


class ProfileModel(models.Model):
    firebase_uid = models.OneToOneField(CustomFirebaseUser, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Firebase User ID'), editable=False)
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    gender = models.CharField(max_length=1, verbose_name=_('Gender'), choices=GENDER_CHOICES)
    address1 = models.CharField(max_length=50, verbose_name=_('Address 1'))
    address2 = models.CharField(max_length=50, verbose_name=_('Address 2'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    pincode = models.CharField(verbose_name=_('Postal Code'), max_length=6)
    state = models.CharField(max_length=50, verbose_name=_('State/Territory'))
    country = models.CharField(max_length=2, verbose_name=_('Country'), choices=COUNTRIES_CHOICES)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Longitude'), null=True, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Latitude'), null=True, blank=True)
    profile_picture = models.ImageField(verbose_name=_('Profile Picture'), null=True, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'