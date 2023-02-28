from django import forms
from .models import CustomFirebaseUser


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomFirebaseUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']
