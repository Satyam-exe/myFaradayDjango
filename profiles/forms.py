from django import forms
from .models import CustomUserProfile, CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
            }
        )
    )
    phone_number = forms.CharField(
        disabled=True
    )

    email = forms.EmailField(
        disabled=True if CustomUser.email != (None or '') else False
    )

    class Meta:
        model = CustomUserProfile
        fields = (
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'address',
            'phone_number',
            'secondary_phone_number',
            'email',
            'state',
            'city',
            'pincode',
            )
