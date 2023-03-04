import os
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from authentication.models import CustomFirebaseUser
from firebase_admin import auth
from rest_framework import serializers
import requests

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=50, style={'placeholder': 'First Name'})
    last_name = serializers.CharField(required=True, max_length=50, style={'placeholder': 'Last Name'})
    phone_number = serializers.CharField(required=True, max_length=10, style={'placeholder': 'Phone Number'})
    email = serializers.EmailField(required=True, max_length=255, style={'placeholder': 'Email', 'autofocus': True})
    password = serializers.CharField(write_only=True, style={'placeholder': 'Password', 'input_type': 'password'})

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone_number = validated_data['phone_number']

        user_data = {
            'email': email,
            'password': password,
            'returnSecureToken': True,
        }

        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={os.environ.get('FIREBASE_API_KEY')}",
            json=user_data
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Error creating user")

        user_data = response.json()
        id_token = user_data['idToken']
        refresh_token = user_data['refreshToken']
        local_id = user_data['localId']

        # Save user data to the database
        CustomFirebaseUser.objects.create_user(
            firebase_uid=local_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password
        )

        custom_claims = {
            'last_log_in': None,
            'last_activity': None,
            'is_active': True
        }
        auth.set_custom_user_claims(local_id, custom_claims)
        auth.update_user(local_id)

        return {
            'id_token': id_token,
            'email': email,
            'refresh_token': refresh_token,
            'local_id': local_id,
        }


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
