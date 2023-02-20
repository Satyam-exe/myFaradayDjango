from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

CustomUser = get_user_model()


class EmailOrPhoneLoginAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(phone_number=username) | Q(email=username))
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
