import datetime
import secrets
import string
import pytz
from django.conf import settings
from django.core.mail import send_mail
from authentication.models import CustomUser, URLCode, MobileAuthToken


def generate_url(uid, type_of_link):
    code = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(55))
    i = 1
    try:
        while i > 0:
            if URLCode.objects.get(pk=code):
                code = generate_url(uid, type_of_link)
            else:
                i = 0
    except URLCode.DoesNotExist:
        pass
    finally:
        if type_of_link == 'email_verification':
            url = f'{settings.SITE_URL}auth/verifyemail/{code}'
            expires_at = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) + datetime.timedelta(days=10)
        elif type_of_link == 'password_reset_confirm':
            url = f'{settings.SITE_URL}auth/passwordreset/confirm/{code}'
            expires_at = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) + datetime.timedelta(days=2)
        else:
            return None
        new_code_object = URLCode(
            code=code,
            type_of_link=type_of_link,
            user=CustomUser.objects.get(pk=uid),
            generated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata')),
            expires_at=expires_at
        )
        new_code_object.save()
        return url


def send_email_verification_link(uid):
    user = CustomUser.objects.get(pk=uid)
    link = generate_url(uid, 'email_verification')
    subject = 'Email Verification for myFaraday Account'
    body = f'Hello {user.first_name} {user.last_name},\n' \
           f'Thank you for signing up for a myFaraday account.' \
           f'\nPlease click on the link below to verify your email address. It is valid for the next 10 days.\n' \
           f'{link}\n' \
           f'Regards,\n' \
           f'The myFaraday Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(
        subject=subject,
        message=body,
        from_email=email_from,
        recipient_list=recipient_list,
    )


def send_confirm_password_reset_link(email):
    try:
        user = CustomUser.objects.get(email=email)
        link = generate_url(user.pk, 'password_reset_confirm')
        subject = 'Password Reset Link for myFaraday Account'
        body = f'Hello, {user.first_name} {user.last_name}\n' \
               f'You can reset your password by following the link below. The link is valid for 2 days.\n' \
               f'{link}\n' \
               f'If you did not request for a password reset link, You can ignore this email.\n' \
               f'Regards,\n' \
               f'The myFaraday team'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(
            subject=subject,
            message=body,
            from_email=email_from,
            recipient_list=recipient_list,
        )
        return True
    except CustomUser.DoesNotExist:
        return False


def verify_code(code, type_of_link):
    try:
        code_object = URLCode.objects.get(pk=code) or None
        if not code_object:
            return None
        user = CustomUser.objects.get(pk=code_object.user.pk) or None
        if not user:
            return None
        if code_object.type_of_link != type_of_link:
            return None
        if code_object.expires_at < datetime.datetime.now(pytz.timezone('Asia/Kolkata')):
            return None
        if code_object.is_used:
            return None
        return [user, code_object]
    except URLCode.DoesNotExist:
        return None
    except CustomUser.DoesNotExist:
        return None


def generate_mobile_auth_token(uid, requested_time_in_days):
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(55))
    i = 1
    try:
        while i > 0:
            if MobileAuthToken.objects.get(pk=token):
                token = generate_url(uid, requested_time_in_days)
            else:
                i = 0
    except MobileAuthToken.DoesNotExist:
        pass
    finally:
        new_token_object = MobileAuthToken(
            token=token,
            user=CustomUser.objects.get(pk=uid),
            generated_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata')),
            expires_at=datetime.datetime.now(pytz.timezone('Asia/Kolkata')) + datetime.timedelta(days=float(requested_time_in_days)),
            is_revoked=False,
            last_used=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        )
        new_token_object.save()
        return token


def verify_mobile_auth_token(token, uid):
    try:
        token_object = MobileAuthToken.objects.get(pk=token)
        user = CustomUser.objects.get(pk=uid)
        if not token_object.user == user:
            return None
        if token_object.expires_at < datetime.datetime.now(pytz.timezone('Asia/Kolkata')):
            return None
        if token_object.is_revoked:
            return None
        return [user, token_object]
    except MobileAuthToken.DoesNotExist:
        return None
    except CustomUser.DoesNotExist:
        return None

