from django.contrib.auth.models import BaseUserManager


class CustomFirebaseUserManager(BaseUserManager):

    def create_user(self, firebase_uid, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        email = self.normalize_email(email)
        _user = self.model(
            email=email,
            firebase_uid=firebase_uid,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        _user.set_password(password)
        _user.save()
        return _user

    def create_superuser(self, firebase_uid, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(firebase_uid, email, password, first_name, last_name, **extra_fields)
