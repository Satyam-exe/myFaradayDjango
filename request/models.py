from django.db import models
from authentication.models import CustomUser
from django.utils.translation import gettext_lazy as _

from profiles.models import Location
from worker.models import Worker


class Request(models.Model):
    request_id = models.IntegerField(verbose_name=_('Request ID'), primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name=_('User ID'), null=True)
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
    rating = models.IntegerField(verbose_name=_('Rating'), choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    likely_to_recommend = models.IntegerField(verbose_name=_('Likely to Recommend'), choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    feedback = models.TextField(verbose_name=_('Feedback'), blank=True, null=True)
    time_of_feedback = models.DateTimeField(verbose_name=_('Time of Feedback'))

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
