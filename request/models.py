from django.db import models
from authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _

from profiles.models import Location
from worker.models import Worker


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

SERVICE_CHOICES = (
    ('Installation', 'Installation'),
    ('Maintenance', 'Maintenance'),
    ('Repair', 'Repair'),
    ('Consultation', 'Consultation')
)

REPAIR_OPTIONS = (
    ('Lighting', 'Lighting'),
    ('Outlets/Switches', 'Outlets/Switches'),
    ('Ceiling Fans', 'Ceiling Fans'),
    ('Circuit Breakers', 'Circuit Breakers (MCB)'),
    ('Electrical Panels', 'Electrical Panels'),
    ('Wiring', 'Wiring'),
    ('Air Conditioning', 'Air Conditioning'),
    ('Refrigerator', 'Refrigerator'),
    ('Other', 'Other')
)

MAINTENANCE_OPTIONS = (
    ('Lighting', 'Lighting'),
    ('Outlets/Switches', 'Outlets/Switches'),
    ('Ceiling Fans', 'Ceiling Fans'),
    ('Circuit Breakers', 'Circuit Breakers (MCB)'),
    ('Electrical Panels', 'Electrical Panels'),
    ('Wiring', 'Wiring'),
    ('Air Conditioning', 'Air Conditioning'),
    ('Refrigerator', 'Refrigerator'),
    ('Other', 'Other')
)

INSTALLATION_OPTIONS = (
    ('Lighting', 'Lighting'),
    ('Ceiling Fans', 'Ceiling Fans'),
    ('Electrical Panels', 'Electrical Panels'),
    ('Air Conditioning', 'Air Conditioning'),
    ('Refrigerator', 'Refrigerator'),
    ('Other', 'Other')
)

CONSULTATION_OPTIONS = (
    ('General Inquiry', 'General Inquiry')
)


class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name=_('User ID'), null=True)
    service_needed = models.CharField(max_length=50, verbose_name=_('Service Needed'), choices=SERVICE_CHOICES)
    appliance = models.CharField(max_length=100, verbose_name=_('Appliance'))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name=_('Location ID'))
    time_of_request = models.DateTimeField(verbose_name=_('Time of Request'))
    is_emergency = models.BooleanField(verbose_name=_('Is Emergency'), default=False)
    issue = models.TextField(verbose_name=_('Issue'))
    is_forwarded = models.BooleanField(verbose_name=_('Is Forwarded'), default=False)
    forwarded_to = models.ForeignKey(Worker, on_delete=models.SET_NULL, verbose_name=_('Worker ID'), null=True)
    is_closed = models.BooleanField(verbose_name=_('Is Closed'), default=False)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'


class Feedback(models.Model):
    request = models.OneToOneField(Request, verbose_name=_('Request ID'), on_delete=models.CASCADE,
                                   primary_key=True)
    rating = models.IntegerField(verbose_name=_('Rating'), choices=RATING_CHOICES)
    likely_to_recommend = models.IntegerField(verbose_name=_('Likely to Recommend'), choices=RATING_CHOICES)
    feedback = models.TextField(verbose_name=_('Feedback'), blank=True, null=True)
    time_of_feedback = models.DateTimeField(verbose_name=_('Time of Feedback'))

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
