from django import forms
from .firebase_auth import create_firebase_user
from .models import CustomFirebaseUser


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomFirebaseUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']