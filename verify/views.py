import json
import requests.exceptions
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from .config import auth, database
from .forms import LoginForm, SignupForm, ResetPasswordForm, ConfirmResetPasswordForm
from django.contrib import messages
from django.contrib import auth as django_auth
from django.http import HttpResponse
from .models import FirebaseUser
from django.db import transaction


@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email           = form.cleaned_data.get('email')
            password        = form.cleaned_data.get('password')
            first_name      = form.cleaned_data.get('first_name')
            last_name       = form.cleaned_data.get('last_name')
            mobile_number   = form.cleaned_data.get('mobile_number')
            try:
                auth_user = auth.create_user_with_email_and_password(email, password)
                user_id = auth_user['localId']
                # Save user data to the database
                data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "mobile_number": mobile_number,
                    "email": email
                }
                database.child("users").child(user_id).set(data)
                FirebaseUser.objects.create_user(
                    firebase_uid    = user_id,
                    first_name      = first_name,
                    last_name       = last_name,
                    email           = email,
                    mobile_number   = mobile_number,
                    password        = password
                )
                auth.send_email_verification(auth_user['idToken'])

                messages.success(request, 'An email verification link has been sent to you. Please verify your email.')
                return redirect('home')
            except requests.exceptions.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                if error == "EMAIL_EXISTS":
                    messages.error(request, 'Email already exists')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                # Authenticate user with Firebase
                auth.sign_in_with_email_and_password(email, password)
                # Authenticate user with Django
                django_user = django_auth.authenticate(request, email=email, password=password)
                if django_user is not None:
                    django_auth.login(request, django_user, backend='verify.backends.FirebaseAuthenticationBackend')
                    messages.success(request, 'You have successfully logged in!')
                    return redirect(reverse('home'))
            except:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    django_auth.logout(request)  # logout the user from Django session
    auth.current_user = None  # logout the user from Firebase session
    return redirect('home')  # redirect to home page or any other page you want


def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if auth.send_password_reset_email(email):
                return HttpResponse('Password reset email sent!')
            else:
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

    # Make a request to the Firebase REST API to verify the email
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:emailVerification?key={settings.FIREBASE_API_KEY}'
    data = {'oobCode': oob_code}
    response = requests.post(url, json=data)

    # Check if the email was verified successfully
    if response.ok:
        messages.success(request, 'Your email has been verified. You can now log in.')
    else:
        messages.error(request, 'Sorry, we could not verify your email. Please try again later.')

    return redirect(reverse('login'))
