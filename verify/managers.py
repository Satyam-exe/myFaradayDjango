from django.contrib.auth.models import BaseUserManager


class FirebaseUserManager(BaseUserManager):
    def create_user(self, email, firebase_uid, password=None, **kwargs):
        if not firebase_uid:
            raise ValueError('Users must have a firebase_uid')
        if not email:
            raise ValueError('Users must have an email address')

        # create user
        user = self.model(email=self.normalize_email(email), firebase_uid=firebase_uid, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        firebase_uid = ''
        return self.create_user(email, password, firebase_uid, **kwargs)
