from django.db import models
from profiles.models import Profile
from django.utils.translation import gettext_lazy as _


class RequestModel(models.Model):
    request_id = models.IntegerField(verbose_name=_('Request ID'), primary_key=True, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT,
                             verbose_name=_('User ID'))
    time_of_request = models.DateTimeField(verbose_name=_('Time of Request'))
    name = models.CharField(verbose_name=_('Full Name'), max_length=100)
    address = models.CharField(max_length=100, verbose_name=_('Address'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    state = models.CharField(max_length=50, verbose_name=_('State/Territory'))
    country = models.CharField(max_length=2, verbose_name=_('Country'))
    pincode = models.CharField(verbose_name=_('Postal Code'), max_length=6)
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_('Phone Number'))
    longitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Longitude'), null=True,
                                    blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name=_('Latitude'), null=True, blank=True)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
