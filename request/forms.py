from django import forms
from django.utils.translation import gettext_lazy as _

from request.models import SERVICE_CHOICES, Request, Feedback, RATING_CHOICES


class RequestForm(forms.ModelForm):
    service_needed = forms.ChoiceField(choices=SERVICE_CHOICES, label=_('Type of Service Required'))
    appliance = forms.CharField(max_length=100)
    issue = forms.CharField(max_length=200, widget=forms.Textarea())
    is_emergency = forms.BooleanField(label=_('Do you require an emergency service?'))

    class Meta:
        model = Request


class FeedbackForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    likely_to_recommend = forms.ChoiceField(choices=RATING_CHOICES)
    feedback = forms.CharField(max_length=100, empty_value=True, widget=forms.Textarea())

    class Meta:
        model = Feedback
