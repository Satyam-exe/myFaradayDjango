import datetime
import os
import base64
import firebase_admin
import pytz
from django.contrib.auth import get_user_model
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth, db
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomFirebaseUser
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)

private_key = os.environ.get('firebase_private_key').replace('\\n', '\n')
private_key_bytes = private_key.encode('utf-8')
private_key_b64 = base64.b64encode(private_key_bytes)
private_key_pkcs8 = base64.b64decode(private_key_b64)

cred = credentials.Certificate({
  "type": os.environ.get('firebase_type'),
  "project_id": os.environ.get('firebase_project_id'),
  "private_key_id": os.environ.get('firebase_private_key_id'),
  "private_key": private_key_pkcs8,
  "client_email": os.environ.get('firebase_client_email'),
  "client_id": os.environ.get('firebase_client_id'),
  "auth_uri": os.environ.get('firebase_auth_uri'),
  "token_uri": os.environ.get('firebase_token_uri'),
  "auth_provider_x509_cert_url": os.environ.get('firebase_auth_provider_x509_cert_url'),
  "client_x509_cert_url": os.environ.get('firebase_client_x509_cert_url')
})

default_app = firebase_admin.initialize_app(cred, {'database_url': os.environ.get('FIREBASE_DATABASE_URL')})

ref = db.reference('/')

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
            user = CustomFirebaseUser.objects.get(firebase_uid=uid)
        except User.DoesNotExist:
            # Create a new user
            user = CustomFirebaseUser(firebase_uid=uid)
            user.save()

        # Update the user's last activity
        user.last_login = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")
        user.last_activity = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%Y %H:%M:%S")
        user.save()

        return (user, None)

