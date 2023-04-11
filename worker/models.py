from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomUser


# Create your models here.
class Worker(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )
    aadhar_number = models.PositiveBigIntegerField(
        verbose_name=_('Aadhar Number'),
        validators=[
            RegexValidator('^[0-9]{12}$')
        ],
        unique=True
    )
    pan = models.CharField(
        verbose_name=_('Permanent Account Number'),
        max_length=10,
        validators=[RegexValidator(r'^[a-zA-z]{5}[0-9]{4}[a-zA-Z]{1}$')],
        unique=True
    )
    requests_completed = models.IntegerField(
        verbose_name=_('Requests Completed'),
        default=0
    )
    rating = models.DecimalField(
        verbose_name=_('Rating'),
        max_digits=3,
        decimal_places=2,
        default=0,
    )
    worker_type = models.CharField(
        max_length=15,
        choices=(
            ('electrician', 'electrician'),
            ('plumber', 'plumber')
        )
    )
    is_available = models.BooleanField(
        verbose_name=_('Is Available'),
        default=False
    )

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'
