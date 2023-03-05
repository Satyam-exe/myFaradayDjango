from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomFirebaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class SignUpWithEmailAndPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomFirebaseUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


class SignInWithEmailAndPasswordForm(AuthenticationForm):
    class Meta:
        fields = ['email', 'passwor1d']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ['email']


class ConfirmPasswordResetForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2
