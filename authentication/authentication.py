import time
import firebase_admin
from django.contrib.auth import get_user_model
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from firebase_admin import auth
from rest_framework.exceptions import AuthenticationFailed

cred = credentials.Certificate('/secret/myfaraday-firebase-adminsdk-fw8b2-b6c4a55d41.json')

default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise AuthenticationFailed("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise AuthenticationFailed("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise AuthenticationFailed("Invalid user")

        User = get_user_model()

        user = User.objects.get_or_create_firebase_user()

        # Update the user's last activity
        user.last_activity = time.localtime()
        user.save()

        return (user, None)