from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomFirebaseUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, firebase_uid, email, password, **extra_fields):
        if not firebase_uid:
            raise ValueError('The given firebase_uid must be set')
        email = self.normalize_email(email)
        user = self.model(firebase_uid=firebase_uid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, firebase_uid, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(firebase_uid, email, password, **extra_fields)

    def create_superuser(self, firebase_uid, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(firebase_uid, email, password, **extra_fields)

    def get_or_create_firebase_user(self, firebase_uid, email, password=None, **extra_fields):
        try:
            user = self.get(firebase_uid=firebase_uid)
        except self.model.DoesNotExist:
            user = self.create_user(firebase_uid, email, password, **extra_fields)
        return user

    def get_by_firebase_uid(self, firebase_uid):
        return self.get(firebase_uid=firebase_uid)

    def get_by_email(self, email):
        return self.get(email=email)