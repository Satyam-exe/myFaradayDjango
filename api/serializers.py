from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from authentication.models import CustomFirebaseUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ConfirmResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text=_('Enter your new password')
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text=_('Re-enter your new password')
    )
