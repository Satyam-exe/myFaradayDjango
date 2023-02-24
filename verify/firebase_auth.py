from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .config import auth
from .config import database as db


class FirebaseAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user = None
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except:
            pass

        if user:
            try:
                user_model = get_user_model()
                user_data = db.child("users").child(user['localId']).get().val()
                first_name = user_data.get("first_name")
                last_name = user_data.get("last_name")
                mobile_number = user_data.get("mobile_number")
                user, created = user_model.objects.get_or_create(
                    username=user['localId'],
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    mobile_number=mobile_number
                )
                return user
            except IntegrityError:
                pass

        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

