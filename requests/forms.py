from django import forms
from .models import Request


class RequestForm(forms.ModelForm):
    issue = forms.Textarea()

    class Meta:
        model = Request
        fields = (
            'service_required',
            'issue'
            )
