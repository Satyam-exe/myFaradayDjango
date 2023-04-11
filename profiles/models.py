from django.core.validators import RegexValidator

from authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.db import models

GENDER_CHOICES = [
    ('M', _('Male')),
    ('F', _('Female')),
    ('O', _('Others')),
]


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,
                                verbose_name=_('User ID'))
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name=_('Gender'), choices=GENDER_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(verbose_name=_('Profile Picture'), upload_to=f'profile-pictures/')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


STATE_CHOICES = (
    ("AN", "Andaman and Nicobar Islands"),
    ("AP", "Andhra Pradesh"),
    ("AR", "Arunachal Pradesh"),
    ("AS", "Assam"),
    ("BR", "Bihar"),
    ("CG", "Chhattisgarh"),
    ("CH", "Chandigarh"),
    ("DN", "Dadra and Nagar Haveli"),
    ("DD", "Daman and Diu"),
    ("DL", "Delhi"),
    ("GA", "Goa"),
    ("GJ", "Gujarat"),
    ("HR", "Haryana"),
    ("HP", "Himachal Pradesh"),
    ("JK", "Jammu and Kashmir"),
    ("JH", "Jharkhand"),
    ("KA", "Karnataka"),
    ("KL", "Kerala"),
    ("LA", "Ladakh"),
    ("LD", "Lakshadweep"),
    ("MP", "Madhya Pradesh"),
    ("MH", "Maharashtra"),
    ("MN", "Manipur"),
    ("ML", "Meghalaya"),
    ("MZ", "Mizoram"),
    ("NL", "Nagaland"),
    ("OD", "Odisha"),
    ("PB", "Punjab"),
    ("PY", "Pondicherry"),
    ("RJ", "Rajasthan"),
    ("SK", "Sikkim"),
    ("TN", "Tamil Nadu"),
    ("TS", "Telangana"),
    ("TR", "Tripura"),
    ("UP", "Uttar Pradesh"),
    ("UK", "Uttarakhand"),
    ("WB", "West Bengal")
)


class Location(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('User'))
    created_at = models.DateTimeField(verbose_name=_('Created At'))
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    pincode = models.IntegerField(validators=[RegexValidator('^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$')],
                                  verbose_name=_('Postal Code'))
    state = models.CharField(max_length=2, verbose_name=_('State'), choices=STATE_CHOICES)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Longitude'), null=True,
                                    blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Latitude'), null=True, blank=True)


UPDATE_CHOICES = (
    ('first_name', 'first_name'),
    ('last_name', 'last_name'),
    ('email', 'email'),
    ('phone_number', 'phone_number'),
    ('date_of_birth', 'date_of_birth'),
    ('gender', 'gender'),
    ('address1', 'address1'),
    ('address2', 'address2'),
    ('city', 'city'),
    ('pincode', 'pincode'),
    ('state', 'state'),
    ('latitude', 'latitude'),
    ('longitude', 'longitude'),
    ('profile_picture', 'profile_picture')
)


class ProfileUpdates(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name=_('User'), null=True)
    update_type = models.CharField(max_length=50, choices=UPDATE_CHOICES, verbose_name=_('Update Type'))
    updated_from = models.CharField(max_length=100, verbose_name=_('Updated From'))
    updated_to = models.CharField(max_length=100, verbose_name=_('Updated To'))
    updated_at = models.DateTimeField(verbose_name=_('Updated At'))

    class Meta:
        verbose_name = 'Profile Update'
        verbose_name_plural = 'Profile Updates'
