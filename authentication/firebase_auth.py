# import os
#
# import firebase_admin.exceptions
# import pytz
#
# import requests
#
# from datetime import datetime
#
# from django.shortcuts import redirect
# from dotenv import load_dotenv
#
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.db import transaction
# from django.core.mail import send_mail
#
# from firebase_admin import auth
#
# from profiles.models import Profile
# from .models import CustomFirebaseUser
#
# from profiles.firebase_profile import users_ref, update_profile, get_profile
#
# dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
# load_dotenv(dotenv_path)
#
#
# def get_id_token(request, firebase_uid=None):
#     if not request.session.get('id_token'):
#         print('session doesnt have id token')
#         custom_id_token = create_custom_id_token(firebase_uid=firebase_uid)
#         id_token = custom_id_token
#     else:
#         id_token = request.session.get('id_token')
#     return id_token
#
#
# def get_refresh_token(request):
#     return request.session.get('refresh_token')
#
#
# def create_custom_id_token(firebase_uid, developer_claims=None, app=None):
#     return auth.create_custom_token(firebase_uid, developer_claims, app)
#
#
# def exchange_refresh_token_for_id_token(request):
#     refresh_token = get_refresh_token(request)
#     url = f"https://securetoken.googleapis.com/v1/token?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'refresh_token': bytes(refresh_token).decode('utf-8'),
#         'grant_type': 'refresh_token'
#     }
#     response = requests.post(url=url, json=payload)
#     id_token = response.json().get('id_token') or None
#     project_id = response.json().get('project_id') or None
#     error_message = response.json().get('error').get('message') or None
#     if response.status_code != 200 \
#             or error_message \
#             or not id_token \
#             or project_id != os.environ.get('firebase_project_id'):
#         return messages.error(request, 'An error occurred. Please try again.')
#     request.session['id_token'] = id_token
#     request.session['refresh_token'] = response.json().get('refresh_token')
#     request.session['id_token_expires_in'] = response.json().get('expires_in')
#
#
# def sign_up_with_email_and_password(request, email, password, first_name, last_name, phone_number, to_redirect=False):
#     try:
#         firebase_user = auth.create_user(
#             email=email,
#             password=password,
#             display_name=f'{first_name} {last_name}',
#             phone_number=f'+91{phone_number}',
#             email_verified=False
#         )
#         print('created firebase user')
#         firebase_uid = firebase_user.uid
#         django_user = CustomFirebaseUser(
#             firebase_uid=firebase_uid,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             phone_number=phone_number,
#             signed_up=datetime.fromtimestamp(firebase_user.user_metadata.creation_timestamp / 1000),
#             last_activity=(datetime.fromtimestamp(
#                 firebase_user.user_metadata.last_refresh_timestamp / 1000)) if firebase_user.user_metadata.last_refresh_timestamp else None,
#             is_active=True,
#             is_staff=False,
#             is_superuser=False
#         )
#         django_user.set_password(raw_password=password)
#         django_user.save()
#         print('created django user')
#         users_ref.set({
#             firebase_uid: {
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'email': email,
#                 'phone_number': phone_number,
#                 'date_of_birth': None,
#                 'gender': None,
#                 'address1': None,
#                 'address2': None,
#                 'city': None,
#                 'pincode': None,
#                 'state': None,
#                 'country': None,
#                 'latitude': None,
#                 'longitude': None,
#                 'profile_picture': firebase_user.photo_url or None,
#                 'requests_made': None
#             }
#         })
#         print('created firebase profile')
#         new_user_profile = Profile(
#             user=django_user,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone_number=phone_number,
#             date_of_birth=None,
#             gender=None,
#             address1=None,
#             address2=None,
#             city=None,
#             pincode=None,
#             state=None,
#             country=None,
#             latitude=None,
#             longitude=None,
#             profile_picture=firebase_user.photo_url or None
#         )
#         new_user_profile.save()
#         print('created django profile')
#         send_email_verification(request, firebase_uid=firebase_uid)
#         print('email probably sent')
#         if to_redirect:
#             print('should have redirected')
#             return redirect('signup-success')
#     except auth.EmailAlreadyExistsError:
#         print('The user with the provided email already exists.')
#         return messages.error(request, 'The user with the provided email already exists.')
#     except auth.PhoneNumberAlreadyExistsError:
#         print('The user with the provided phone number already exists.')
#         return messages.error(request, 'The user with the provided phone number already exists.')
#     except auth.UidAlreadyExistsError:
#         print('The user with this UID already exists.')
#         return messages.error(request, 'The user with this UID already exists.')
#
#
# def sign_in_with_email_and_password(request, email, password, to_redirect=False):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'email': email,
#         'password': password,
#         'returnSecureToken': True
#     }
#     response = requests.post(url=url, json=payload)
#     email = response.json().get('email') or None
#     id_token = response.json().get('idToken')
#     refresh_token = response.json().get('refreshToken')
#     id_token_expires_in = response.json().get('expiresIn')
#     firebase_uid = response.json().get('localId')
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == ('INVALID_PASSWORD' or 'EMAIL_NOT_FOUND'):
#             return messages.error(request, 'Invalid credentials. Please try again.')
#         elif error_message == 'USER_DISABLED':
#             return messages.error(request, 'Your account has been disabled. Please contact myFaraday for support.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     if not (email and id_token):
#         return messages.error(request, 'Could not log in. Please try again.')
#     firebase_user = get_firebase_user(email=email)
#     if not firebase_user.email_verified:
#         return messages.error(request, 'Please verify your email before logging in.')
#     django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_uid) or None
#     if not django_user:
#         display_name_list = firebase_user.display_name.rsplit(" ", 1)
#         django_user = CustomFirebaseUser(
#             firebase_uid=firebase_uid,
#             email=email,
#             phone_number=firebase_user.phone_number,
#             first_name=display_name_list[1],
#             last_name=display_name_list[0],
#             signed_up=datetime.fromtimestamp(firebase_user.user_metadata.creation_timestamp / 1000),
#             last_login=datetime.fromtimestamp(firebase_user.user_metadata.last_sign_in_timestamp / 1000),
#             last_activity=datetime.fromtimestamp(firebase_user.user_metadata.last_refresh_timestamp / 1000),
#             is_active=True,
#             is_staff=False,
#             is_superuser=False
#         )
#         django_user.set_password(password)
#         django_user.save()
#         firebase_user_profile = get_profile(firebase_uid)
#         django_user_profile = Profile(
#             user=django_user,
#             first_name=firebase_user_profile.get('first_name'),
#             last_name=firebase_user_profile.get('last_name'),
#             email=firebase_user_profile.get('email'),
#             phone_number=firebase_user_profile.get('phone_number'),
#             date_of_birth=firebase_user_profile.get('date_of_birth') or None,
#             gender=firebase_user_profile.get('gender') or None,
#             address1=firebase_user_profile.get('address1') or None,
#             address2=firebase_user_profile.get('address2') or None,
#             city=firebase_user_profile.get('city') or None,
#             pincode=firebase_user_profile.get('pincode') or None,
#             state=firebase_user_profile.get('state') or None,
#             country=firebase_user_profile.get('country') or None,
#             latitude=firebase_user_profile.get('latitude') or None,
#             longitude=firebase_user_profile.get('longitude') or None,
#             profile_picture=firebase_user_profile.get('profile_picture') or None
#         )
#         django_user_profile.save()
#     temp_django_user = authenticate(request=request, email=email, password=password) or None
#     if not temp_django_user:
#         return messages.error(request, 'Could not log in, please try again.')
#     login(request=request, user=temp_django_user)
#     request.session['id_token'] = id_token
#     request.session['refresh_token'] = refresh_token
#     request.session['firebase_uid'] = firebase_uid
#     request.session['id_token_expires_in'] = id_token_expires_in
#     if to_redirect:
#         return redirect('home')
#
#
# def get_firebase_user(firebase_uid=None, email=None, phone_number=None, id_token=None):
#     if firebase_uid:
#         _user = auth.get_user(uid=firebase_uid)
#     elif email:
#         _user = auth.get_user_by_email(email=email)
#     elif phone_number:
#         _user = auth.get_user_by_phone_number(phone_number=phone_number)
#     elif id_token:
#         decoded_token = auth.verify_id_token(id_token)
#         firebase_uid = decoded_token['uid']
#         _user = get_firebase_user(firebase_uid=firebase_uid)
#     else:
#         _user = None
#     return _user
#
#
# def send_email_verification(request, firebase_uid=None):
#     print('inside send email verification now.')
#     id_token = get_id_token(request, firebase_uid)
#     print('We have id token' + id_token) if len(id_token) > 20 else print('We do not have id token')
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'requestType': 'VERIFY_EMAIL',
#         'idToken': bytes(id_token).decode(encoding='utf-8')
#     }
#     print('payload ready')
#     response = requests.post(url=url, json=payload)
#     email = response.json().get('email') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         print(str(error_message))
#         if error_message == 'INVALID_ID_TOKEN':
#             return messages.error(request, 'The ID Token is invalid. Please try to log in to solve this issue.')
#         elif error_message == 'USER_NOT_FOUND':
#             return messages.error(request, 'Cannot find the user. Please try to log in to solve this issue.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         print('code != 200')
#         print(response.status_code)
#         print(response.json())
#         return messages.error(request, 'An error occurred. Please request an email verification again.')
#     if not email:
#         print('email isnt in the response payload')
#         return messages.error(request, 'An error occurred. Please try again later.')
#     print('Second last line of send email verification.')
#     return messages.success(request, 'We have sent an email verification link to your email. Please verify your email.')
#
#
# def confirm_email_verification(request, oob_code):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'oobCode': oob_code
#     }
#     response = requests.post(url=url, json=payload)
#     is_email_verified_after_try = response.json().get('emailVerified') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EXPIRED_OOB_CODE':
#             return messages.error(request, 'This link is expired. Please generate a new one.')
#         elif error_message == 'INVALID_OOB_CODE':
#             return messages.error(request, 'Invalid link.')
#         elif error_message == 'USER_DISABLED':
#             return messages.error(request, 'Your account has been disabled. Kindly contact myFaraday for support.')
#         elif error_message == 'EMAIL_NOT_FOUND':
#             return messages.error(request, 'Could not verify your email.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     if not is_email_verified_after_try:
#         return messages.error(request, 'Could not verify your email. Please try again.')
#     return messages.success(request, 'Your email has been verified.')
#
#
# def send_password_reset_email(request, email):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'requestType': 'PASSWORD_RESET',
#         'email': email
#     }
#     response = requests.post(url=url, json=payload)
#     email = response.json().get('email') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EMAIL_NOT_FOUND':
#             return messages.error(request, 'No user associated with the email found.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     if not email:
#         return messages.error(request, 'An error occurred. Please try again later.')
#     return messages.success(request, 'We have sent a password reset link to your email.')
#
#
# def verify_password_reset_code(request, oob_code):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'oobCode': oob_code
#     }
#     response = requests.post(url=url, json=payload)
#     request_type = response.json().get('requestType') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EXPIRED_OOB_CODE':
#             return messages.error(request, 'This link is expired. Please generate a new one.')
#         elif error_message == 'INVALID_OOB_CODE':
#             return messages.error(request, 'Invalid link.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     if not (request_type and request_type == 'PASSWORD_RESET'):
#         return messages.error(request, 'An error occurred. Please try generating a new link.')
#     return True
#
#
# def confirm_password_reset(request, oob_code, new_password):
#     if not verify_password_reset_code(request, oob_code):
#         return False
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:resetPassword?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'oobCode': oob_code,
#         'newPassword': new_password
#     }
#     response = requests.post(url=url, json=payload)
#     request_type = response.json().get('requestType') or None
#     email = response.json().get('email') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EXPIRED_OOB_CODE':
#             return messages.error(request, 'This link is expired. Please generate a new one.')
#         elif error_message == 'INVALID_OOB_CODE':
#             return messages.error(request, 'Invalid link.')
#         elif error_message == 'USER_DISABLED':
#             return messages.error(request, 'Your account has been disabled. Kindly contact myFaraday support.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     if not (request_type and request_type == 'PASSWORD_RESET'):
#         return messages.error(request, 'An error occurred. Please try generating a new link.')
#     firebase_user = get_firebase_user(email=email)
#     django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_user.uid)
#     django_user.set_password(new_password)
#     django_user.save()
#     password_change_timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
#     subject = 'Password Reset Recently - myFaraday'
#     body = f'Dear {firebase_user.display_name}\n' \
#            f'You have recently reset your password on {password_change_timestamp.strftime("%A, %d %B %Y")} at ' \
#            f'{password_change_timestamp.strftime("%l:%M:%S %p")} IST (UTC+5:30)\n' \
#            f'If this was not you, please contact myFaraday immediately.\n' \
#            f'Thanks,\n' \
#            f'The myFaraday Team'
#     to_email = email
#     from_email = os.environ.get('EMAIL_HOST_USER')
#     send_mail(
#         subject=subject,
#         message=body,
#         from_email=from_email,
#         recipient_list=[to_email, ]
#     )
#     return messages.success(request, 'You have successfully reset your password.')
#
#
# @transaction.atomic
# def change_password(request, new_password):
#     id_token = get_id_token(request)
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'idToken': bytes(id_token).decode('utf-8'),
#         'password': new_password,
#         'returnSecureToken': True
#     }
#     response = requests.post(url=url, json=payload)
#     email = response.json().get('email') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EXPIRED_OOB_CODE':
#             return messages.error(request, 'This link is expired. Please generate a new one.')
#         elif error_message == 'INVALID_OOB_CODE':
#             return messages.error(request, 'Invalid link.')
#         elif error_message == 'USER_DISABLED':
#             return messages.error(request, 'Your account has been disabled. Kindly contact myFaraday support.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     firebase_user = get_firebase_user(email=email)
#     django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_user.uid)
#     django_user.set_password(new_password)
#     django_user.save()
#     request.session['id_token'] = response.json().get('idToken')
#     request.session['refresh_token'] = response.json().get('refreshToken')
#     request.session['id_token_expires_in'] = response.json().get('expiresIn')
#     password_change_timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
#     subject = 'Password Reset Recently - myFaraday'
#     body = f'Dear {firebase_user.display_name}\n' \
#            f'You have recently changed your password on {password_change_timestamp.strftime("%A, %d %B %Y")} at ' \
#            f'{password_change_timestamp.strftime("%l:%M:%S %p")} IST (UTC+5:30)\n' \
#            f'If this was not you, please contact myFaraday immediately.\n' \
#            f'Thanks,\n' \
#            f'The myFaraday Team'
#     to_email = email
#     from_email = os.environ.get('EMAIL_HOST_USER')
#     send_mail(
#         subject=subject,
#         message=body,
#         from_email=from_email,
#         recipient_list=[to_email, ]
#     )
#     return messages.success(request, 'You have successfully changed your password.')
#
#
# def change_email(request, new_email):
#     id_token: str = str(get_id_token(request))
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'idToken': str(id_token).encode('UTF8'),
#         'email': new_email,
#         'returnSecureToken': True
#     }
#     response = requests.post(url=url, json=payload)
#     email = response.json().get('email') or None
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'EMAIL_EXISTS':
#             return messages.error(request, 'An account with this email already exists.')
#         elif error_message == 'INVALID_ID_TOKEN':
#             return messages.error(request, 'Invalid ID Token. Please log out and log in again.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     firebase_user = get_firebase_user(email=email)
#     django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_user.uid)
#     django_user.update(email=new_email)
#     django_user.save()
#     update_profile(request, email=email)
#     request.session['id_token'] = str(response.json().get('idToken'))
#     request.session['refresh_token'] = str(response.json().get('refreshToken'))
#     request.session['id_token_expires_in'] = response.json().get('expiresIn')
#     return messages.success(request, 'You have successfully changed your password.')
#
#
# def change_phone_number(request, new_phone_number):
#     try:
#         firebase_uid = request.session.get('firebase_uid')
#         firebase_user = get_firebase_user(firebase_uid=firebase_uid)
#         old_phone_number = firebase_user.phone_number
#         auth.update_user(
#             uid=request.session.get('firebase_uid'),
#             phone_number=new_phone_number
#         )
#         django_user = CustomFirebaseUser.objects.get(firebase_uid=firebase_uid)
#         django_user.update(phone_number=new_phone_number)
#         django_user.save()
#         update_profile(request, phone_number=new_phone_number)
#         phone_number_change_timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
#         subject = 'Phone Number Changed Recently - myFaraday'
#         body = f'Dear {firebase_user.display_name}\n' \
#                f'You have recently changed your phone number from {old_phone_number} to {new_phone_number} on ' \
#                f'{phone_number_change_timestamp.strftime("%A, %d %B %Y")} at ' \
#                f'{phone_number_change_timestamp.strftime("%l:%M:%S %p")} IST (UTC+5:30). If this was not you, please ' \
#                f'contact myFaraday immediately.\n' \
#                f'Thanks,\n' \
#                f'The myFaraday Team'
#         from_email = os.environ.get('EMAIL_HOST_USER')
#         send_mail(
#             subject=subject,
#             message=body,
#             from_email=from_email,
#             recipient_list=[firebase_user.email, ]
#         )
#         return messages.success(request, 'You have successfully changed your password.')
#     except firebase_admin.exceptions.FirebaseError:
#         return messages.error(request, 'An error occurred while updating your account. Please try again')
#     except Exception as e:
#         messages.error(request, str(e))
#
#
# def delete_user(request, to_redirect=False):
#     id_token: str = str(get_id_token(request))
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:delete?key={os.environ.get('FIREBASE_API_KEY')}"
#     payload = {
#         'idToken': str(id_token).encode('UTF8'),
#     }
#     response = requests.post(url=url, json=payload)
#     error_message = response.json().get('error').get('message') or None
#     if error_message:
#         if error_message == 'INVALID_ID__TOKEN':
#             return messages.error(request, 'The ID Token is invalid. Please log out and log in again to fix this.')
#         elif error_message == 'USER_NOT_FOUND':
#             return messages.error(request, 'User not found.')
#         else:
#             return messages.error(request, str(error_message))
#     if response.status_code != 200:
#         return messages.error(request, 'An error occurred. Please try again.')
#     firebase_uid = request.session.get('firebase_uid')
#     firebase_user = get_firebase_user(firebase_uid=firebase_uid)
#     CustomFirebaseUser.objects.get(firebase_uid=firebase_uid).delete()
#     account_deletion_timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
#     subject = 'Password Reset Recently - myFaraday'
#     body = f'Dear {firebase_user.display_name}\n' \
#            f'We have successfully deleted your myFaraday account as of ' \
#            f'{account_deletion_timestamp.strftime("%A, %d %B %Y")} at {account_deletion_timestamp.strftime("%l:%M:%S %p")} ' \
#            f'IST (UTC+5:30). If this was not you, please contact myFaraday immediately.\n' \
#            f'Thanks,\n' \
#            f'The myFaraday Team'
#     from_email = os.environ.get('EMAIL_HOST_USER')
#     send_mail(
#         subject=subject,
#         message=body,
#         from_email=from_email,
#         recipient_list=[firebase_user.email, ]
#     )
#     messages.success(request, 'Successfully deleted your account')
#     if to_redirect:
#         return redirect('home')
