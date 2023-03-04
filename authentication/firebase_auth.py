import os
import pytz
import requests
import calendar
from django.conf import settings
from django.db import transaction
from dotenv import load_dotenv
from firebase_admin import db, auth
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from .models import CustomFirebaseUser

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)


@transaction.atomic
def signup_with_email_and_password(request, email, password, first_name, last_name, phone_number):
    firebase_user = auth.create_user(
        email=email,
        password=password,
        display_name=f'{first_name} {last_name}',
        phone_number=phone_number,
        email_verified=False
    )
    firebase_uid = firebase_user.uid
    django_user = CustomFirebaseUser.objects.create_user(
        firebase_uid=firebase_uid,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        signed_up=firebase_user.user_metadata.creation_timestamp,
        last_activity=firebase_user.user_metadata.last_refresh_timestamp or None,
        is_active=True,
        is_staff=False,
        is_superuser=False
    )
    send_email_verification(request, firebase_uid)
    to_return = {
        'firebase_user': firebase_user,
        'django_user': django_user
    }
    return to_return


def get_firebase_user(firebase_uid=None, email=None, phone_number=None, id_token=None):
    if firebase_uid:
        _user = auth.get_user(uid=firebase_uid)
    elif email:
        _user = auth.get_user_by_email(email=email)
    elif phone_number:
        _user = auth.get_user_by_phone_number(phone_number=phone_number)
    elif id_token:
        decoded_token = auth.verify_id_token(id_token)
        firebase_uid = decoded_token['uid']
        _user = get_firebase_user(firebase_uid=firebase_uid)
    else:
        _user = None
    return _user


def send_email_verification(request, firebase_uid):
    id_token = auth.create_custom_token(firebase_uid)
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.environ.get('FIREBASE_API_KEY')}"
    payload = {
        'requestType': 'VERIFY_EMAIL',
        'idToken': str(id_token)
    }
    response = requests.post(url=url, json=payload)
    email = response.json().get('email') or None
    error_message = response.json().get('error').get('message') or None
    if response.status_code != 200:
        messages.error(request, 'An error occurred. Please request an email verification again.')
        return False
    if error_message:
        if error_message == 'INVALID_ID_TOKEN':
            messages.error(request, 'The ID Token is invalid. Please try to log in to solve this issue.')
        elif error_message == 'USER_NOT_FOUND':
            messages.error(request, 'Cannot find the user. Please try to log in to solve this issue.')
        else:
            messages.error(request, str(error_message))
        return False
    if not email:
        messages.error(request, 'An error occurred. Please try again later.')
        return False
    messages.success(request, 'We have sent an email verification link to your email. Please verify your email.')
    return True


def confirm_email_verification(request, oob_code):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={os.environ.get('FIREBASE_API_KEY')}"
    payload = {
        'oobCode': str(oob_code)
    }
    response = requests.post(url=url, json=payload)
    is_email_verified_after_try = response.json().get('emailVerified') or None
    error_message = response.json().get('error').get('message') or None
    if response.status_code != 200:
        messages.error(request, 'An error occurred. Please request an email verification again.')
        return False
    if error_message:
        if error_message == 'EXPIRED_OOB_CODE':
            messages.error(request, 'This link is expired. Please generate a new one.')
        elif error_message == 'INVALID_OOB_CODE':
            messages.error(request, 'Invalid link.')
        elif error_message == 'USER_DISABLED':
            messages.error(request, 'Your account has been disabled. Kindly contact myFaraday for support.')
        elif error_message == 'EMAIL_NOT_FOUND':
            messages.error(request, 'Could not verify your email.')
        else:
            messages.error(request, str(error_message))
        return False
    if not is_email_verified_after_try:
        messages.error(request, 'Could not verify your email. Please try again.')
        return False
    messages.success(request, 'Your email has been verified.')
    return True


def send_password_reset_email(request, email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.environ.get('FIREBASE_API_KEY')}"
    payload = {
        'requestType': 'PASSWORD_RESET',
        'email': email
    }
    response = requests.post(url=url, json=payload)
    email = response.json().get('email') or None
    error_message = response.json().get('error').get('message') or None
    if response.status_code != 200:
        messages.error(request, 'An error occurred. Please request an email verification again.')
        return False
    if error_message:
        if error_message == 'EMAIL_NOT_FOUND':
            messages.error(request, 'No user associated with the email found.')
        else:
            messages.error(request, str(error_message))
        return False
    if not email:
        messages.error(request, 'An error occurred. Please try again later.')
        return False
    messages.success(request, 'We have sent a password reset link to your email.')
    return True


def verify_password_reset_code(request, oob_code):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={os.environ.get('FIREBASE_API_KEY')}"
    payload = {
        'oobCode': str(oob_code)
    }
    response = requests.post(url=url, json=payload)
    request_type = response.json().get('requestType') or None
    error_message = response.json().get('error').get('message') or None
    if response.status_code != 200:
        messages.error(request, 'An error occurred. Please request an email verification again.')
        return False
    if error_message:
        if error_message == 'EXPIRED_OOB_CODE':
            messages.error(request, 'This link is expired. Please generate a new one.')
        elif error_message == 'INVALID_OOB_CODE':
            messages.error(request, 'Invalid link.')
        else:
            messages.error(request, str(error_message))
        return False
    if not (request_type and request_type == 'PASSWORD_RESET'):
        messages.error(request, 'An error occurred. Please try generating a new link.')
        return False
    return True


@transaction.atomic
def confirm_password_reset(request, oob_code, new_password):
    if verify_password_reset_code(request, oob_code):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={os.environ.get('FIREBASE_API_KEY')}"
        payload = {
            'oobCode': str(oob_code),
            'newPassword': new_password
        }
        response = requests.post(url=url, json=payload)
        request_type = response.json().get('requestType') or None
        email = response.json().get('email') or None
        error_message = response.json().get('error').get('message') or None
        if response.status_code != 200:
            messages.error(request, 'An error occurred. Please request an email verification again.')
            return False
        if error_message:
            if error_message == 'EXPIRED_OOB_CODE':
                messages.error(request, 'This link is expired. Please generate a new one.')
            elif error_message == 'INVALID_OOB_CODE':
                messages.error(request, 'Invalid link.')
            elif error_message == 'USER_DISABLED':
                messages.error(request, 'Your account has been disabled. Kindly contact myFaraday support.')
            else:
                messages.error(request, str(error_message))
            return False
        if not (request_type and request_type == 'PASSWORD_RESET'):
            messages.error(request, 'An error occurred. Please try generating a new link.')
            return False
        firebase_user = get_firebase_user(email=email)
        django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_user.uid)
        django_user.set_password(new_password)
        django_user.save()
        password_change_timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        subject = 'Password Reset Recently - myFaraday'
        body = f'Dear {firebase_user.display_name}\n' \
               f'You have recently changed your password on {password_change_timestamp.strftime("%A, %d %B %Y")} at ' \
               f'{password_change_timestamp.strftime("%l:%M:%S %p")} IST (UTC+5:30)\n' \
               f'If this was not you, please contact myFaraday immediately.\n' \
               f'Thanks,\n' \
               f'The myFaraday Team'
        to_email = email
        from_email = os.environ.get('EMAIL_HOST_USER')
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email, ]
        )
        messages.success(request, 'You have successfully changed your password.')
        return True
    else:
        return messages
