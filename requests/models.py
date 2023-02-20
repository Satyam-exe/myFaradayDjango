from django.db import models
from django.contrib.auth import get_user_model


class Request(models.Model):
    MAIN_SERVICES_OFFERED = [
        ('plumber', 'Plumbing'),
        ('electrician', 'Electrical Work'),
    ]

    BOOLEAN_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    service_required = models.CharField(max_length=20, choices=MAIN_SERVICES_OFFERED)
    issue = models.TextField(max_length=500)
    name = models.CharField(max_length=90)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    secondary_phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    pincode = models.CharField(max_length=6)
    is_forwarded = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    forwarded_to = models.CharField(max_length=50, blank=True, null=True)
    is_closed = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)

    def __str__(self):
        return f'Request ID {self.id}({self.service_required}): {self.issue}'

