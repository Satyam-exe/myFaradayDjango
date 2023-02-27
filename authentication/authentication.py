import os
import time
import firebase_admin
from django.contrib.auth import get_user_model
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomFirebaseUser
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)

cred = credentials.Certificate({
  "type": os.environ.get('firebase_type'),
  "project_id": os.environ.get('firebase_project_id'),
  "private_key_id": os.environ.get('firebase_project_key_id'),
  "private_key": os.environ.get('firebase_private_key'),
  "client_email": os.environ.get('firebase_client_email'),
  "client_id": os.environ.get('firebase_client_id'),
  "auth_uri": os.environ.get('firebase_auth_uri'),
  "token_uri": os.environ.get('firebase_token_uri'),
  "auth_provider_x509_cert_url": os.environ.get('firebase_auth_provider_x509_cert_url'),
  "client_x509_cert_url": os.environ.get('firebase_client_x509_cert_url')
})

default_app = firebase_admin.initialize_app(cred)

User = get_user_model()


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise AuthenticationFailed("No auth token provided")

        try:
            _, id_token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid auth header")

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get("uid")
        except auth.InvalidIdTokenError:
            raise AuthenticationFailed("Invalid auth token")

        User = get_user_model()
        try:
            user = CustomFirebaseUser.objects.get(pk=uid)
        except User.DoesNotExist:
            # Create a new user
            user = CustomFirebaseUser(pk=uid)
            user.save()

        # Update the user's last activity
        user.last_activity = time.localtime()
        user.save()

        return (user, None)


