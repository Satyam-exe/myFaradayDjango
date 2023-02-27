from django.conf import settings
from firebase_admin import db, auth
from django.core.mail import send_mail
from django.contrib import messages


def create_firebase_user(email=None, password=None, display_name=None, firebase_uid=None, phone_number=None):
    _user = auth.create_user(
        email=email or None,
        password=password or None,
        display_name=display_name or None,
        uid=firebase_uid or None,
        phone_number=phone_number or None
    )
    return _user


def get_firebase_user(firebase_uid=None, email=None, phone_number=None):
    if firebase_uid:
        _user = auth.get_user(uid=firebase_uid)
    elif email:
        _user = auth.get_user_by_email(email=email)
    elif phone_number:
        _user = auth.get_user_by_phone_number(phone_number=phone_number)
    else:
        _user = None
    return _user


def send_email_verification_link(request, email):
    _user = get_firebase_user(email=email)
    link = auth.generate_email_verification_link(email=email)
    subject = 'Email Verification - myFaraday'
    body = f"Hello {_user.display_name},\nThank you for signing up for a myFaraday account.\nPlease " \
           f"click on the link below to verify your email address.\n{link}\nRegards," \
           f"\nThe myFaraday Team"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(
        subject=subject,
        message=body,
        from_email=email_from,
        recipient_list=recipient_list,
    )
    messages.success(
        request,
        'An email verification link has been sent to you. Please authenticate your email.'
    )


def send_password_reset_email(request, email):
    link = auth.generate_password_reset_link(email=email)
    _user = get_firebase_user(email=email)
    subject = 'Password Reset Email - myFaraday'
    body = f"Hello {_user.display_name}, \n " \
           f"We have recieved a request for a password reset link. You can reset your password by clicking on the " \
           f"link below: \n" \
           f"{link} \n" \
           f"If not requested by you, kindly ignore this email \n" \
           f"Regards,\nThe myFaraday Team"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(
        subject=subject,
        message=body,
        from_email=email_from,
        recipient_list=recipient_list
    )
    messages.success(
        request,
        'A password reset link has been sent to your email address.'
    )

