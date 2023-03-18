from django import forms
from django.contrib.auth import password_validation
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
        }
    ))
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'}),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        password_validation.validate_password(password2)
        return password2

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']


class LogInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ['email']


class ConfirmPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match")
        password_validation.validate_password(new_password2)
        return new_password2
