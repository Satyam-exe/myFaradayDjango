import time

import requests.exceptions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from firebase_admin import auth, db
from .forms import LoginForm, SignupForm, ResetPasswordForm, ConfirmResetPasswordForm
from django.contrib import messages
from django.contrib import auth as django_auth
from django.http import HttpResponse
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            try:
                created_user = auth.create_user(
                    email=email,
                    password=password
                )
                firebase_uid = created_user.uid
                # Save user data to the database
                firebase_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone_number,
                    "email": email
                }
                _user = get_user_model()
                _user.objects.create_user(
                    firebase_uid=firebase_uid,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    password=password,
                )
                db.reference('users/' + firebase_uid).set(firebase_data)
                email_verification_link = auth.generate_email_verification_link(email=email)
                subject = 'Email Verification for myFaraday Account'
                body = f'Hello {first_name} {last_name},\nThank you for signing up for a myFaraday account.\nPlease ' \
                       f'click on the link below to verify your email address.\n{email_verification_link}\nRegards,' \
                       f'\nThe myFaraday Team'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [created_user.email, ]
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=email_from,
                    recipient_list=recipient_list,
                )
                messages.success(
                    request,
                    'An email verification link has been sent to you. Please authenticate '
                    'your email.'
                )
                return redirect('home')
            except auth.EmailAlreadyExistsError:
                messages.error(request, 'A myFaraday account with the email already exists.')
            except auth.PhoneNumberAlreadyExistsError:
                messages.error(request, 'A myFaraday account with the phone number already exists')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            try:
                user = django_auth.authenticate(email=email, password=password)
                if user:
                    django_auth.login(request=request, user=user)
                    firebase_uid = user.firebaase_uid
                    db.reference('users/' + firebase_uid).set({'last_login': time.localtime()})
                    return redirect(reverse('home'))
                else:
                    messages.error(request, 'User with the given email does not exist.')
            except:
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please fill in all the fields appropriately.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})



@login_required
def logout_view(request):
    django_auth.logout(request)
    return redirect('home')


def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                User = get_user_model()
                _user = User.objects.get_by_email(email=email)
                password_reset_link = auth.generate_password_reset_link(email)
                subject = 'Password Reset Link for myFaraday Account'
                body = f'Hello, {_user.first_name} {_user.last_name}\n' \
                       f'You can reset your password by following the link below\n' \
                       f'{password_reset_link}\n' \
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
                return HttpResponse('The password reset link has been sent to the email address provided!')
            except:
                return HttpResponse('Failed to send password reset email')
    else:
        form = ResetPasswordForm()
    return render(request, 'resetpassword.html', {'form': form})


def confirm_reset_password_view(request):
    form = ConfirmResetPasswordForm(request.GET)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        try:
            code = request.GET('oobCode')
            auth.verify_password_reset_code(code, password)
            messages.success = 'Password reset successfully. Please log in.'
        except requests.exceptions.HTTPError as e:
            messages.error = e
    return render(request, 'resetpasswordconfirm.html', {'form': form})


def email_verification_view(request):
    # Get the oobCode from the URL
    oob_code = request.GET.get('oobCode', '')

    # Make a request to the Firebase REST API to authentication the email
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:emailVerification?key={settings.FIREBASE_API_KEY}'
    data = {'oobCode': oob_code}
    response = requests.post(url, json=data)

    # Check if the email was verified successfully
    if response.ok:
        messages.success(request, 'Your email has been verified. You can now log in.')
    else:
        messages.error(request, 'Sorry, we could not authentication your email. Please try again later.')

    return redirect(reverse('login'))
