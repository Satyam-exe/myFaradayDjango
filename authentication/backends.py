from firebase_admin import auth
from django.contrib.auth import get_user_model

User = get_user_model()


class FirebaseAuthenticationBackend(object):
    def authenticate(self, request, token):
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = User.objects.get(username=uid)
        except (ValueError, KeyError, User.DoesNotExist):
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None