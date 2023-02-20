from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    username     = None

    class Meta:
        model    = CustomUser
        fields   = [
            'phone_number',
            'email',
            'password1',
            'password2',
        ]


class UserLoginForm(forms.Form):
    email_or_phone_number = forms.CharField(
        label='Email or Phone Number',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput
    )

    def clean(self):
        email_or_phone_number = self.cleaned_data.get('email_or_phone_number')
        password = self.cleaned_data.get('password')

        # Check if the email_or_phone_number is a valid email address
        if '@' in email_or_phone_number:
            user = authenticate(email=email_or_phone_number, password=password)
        else:
            user = authenticate(phone_number=email_or_phone_number, password=password)

        if not user:
            raise forms.ValidationError(
                'Invalid login credentials. Please try again.'
            )

        return self.cleaned_data
