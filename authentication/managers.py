import pytz
from django.contrib.auth.models import BaseUserManager
from pytz import timezone
from datetime import datetime


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone_number, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        email = self.normalize_email(email)
        _user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            signed_up=datetime.now(timezone('Asia/Kolkata')),
            **extra_fields
        )
        _user.set_password(password)
        _user.save()
        from profiles.models import Profile
        profile = Profile(
            user=_user,
            first_name=_user.first_name,
            last_name=_user.last_name,
            email=_user.email,
            phone_number=_user.phone_number,
        )
        from profiles.functions import generate_default_profile_picture_content_file
        profile.profile_picture.save(f'{_user.pk}/{datetime.now(pytz.timezone("Asia/Kolkata"))}.png',
                                     content=generate_default_profile_picture_content_file(_user)
                                     )
        profile.save()
        from authentication.functions import send_email_verification_link
        send_email_verification_link(_user.pk)
        return _user

    def create_superuser(self, email, phone_number, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, phone_number, password, first_name, last_name, **extra_fields)