import pytz
import requests
import rest_framework.authentication

from .firebase_auth import send_email_verification_link
from .firebase_auth import send_password_reset_email
from .firebase_auth import get_firebase_user
from .firebase_auth import create_firebase_user
from .firebase_auth import update_last_login
from .firebase_auth import update_last_activity

from .forms import SignupForm
from .forms import LoginForm

from .models import CustomFirebaseUser

from django.shortcuts import redirect, reverse, render
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from firebase_admin import auth, db

from datetime import datetime

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


@transaction.atomic
def user_sign_up_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = str(f"{'+91'}{form.cleaned_data.get('phone_number')}")
            try:
                _user = create_firebase_user(
                    email=email,
                    password=password,
                    display_name=f'{first_name} {last_name}',
                    phone_number=phone_number
                )
                CustomFirebaseUser.objects.create_user(
                    firebase_uid=_user.uid,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    password=password
                )
                custom_claims = {
                    'last_log_in': None,
                    'last_activity': None,
                    'is_active': True
                }
                auth.set_custom_user_claims(_user.uid, custom_claims)
                auth.update_user(_user.uid)
                # Save user data to the database
                send_email_verification_link(request, email)
                return redirect(reverse('home'))
            except auth.EmailAlreadyExistsError:
                messages.error(request, 'Error: The email already exists')
            except auth.PhoneNumberAlreadyExistsError:
                messages.error(request, 'Error: The phone number already exists')
            except auth.UidAlreadyExistsError:
                messages.error(request, 'Error: The User ID already exists')
        else:
            messages.error(request, 'Please fill up all the fields appropriately')
    else:
        form = SignupForm()
    return render(request=request, template_name='signup.html', context={'form': form})


def user_login_view(request):
    if request.method == 'POST':
        print('Method is post')
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print('form is valid')
            try:
                firebase_user = get_firebase_user(email=email)
                if firebase_user:
                    print('firebase user exists')
                    if firebase_user.email_verified:
                        print('firebase user\'s email is verified')
                        django_user = authenticate(email=email, password=password)
                        if django_user:
                            print('django user exists')
                            login(request, django_user)
                            update_last_login(firebase_user.uid)
                            update_last_activity(firebase_user.uid)
                            return redirect('home')
                        elif firebase_user and not django_user:
                            print('Django user doesnt exist')
                            CustomFirebaseUser.objects.create_user(
                                firebase_uid=firebase_user.uid,
                                first_name=firebase_user.first_name,
                                last_name=firebase_user.last_name,
                                email=firebase_user.email,
                                phone_number=firebase_user.phone_number,
                                password=password
                            )
                            created_and_authenticated_user = authenticate(email=email, password=password)
                            login(request, created_and_authenticated_user)
                            update_last_login(firebase_user.uid)
                            update_last_activity(firebase_user.uid)
                            return redirect('home')
                        else:
                            print('Does not exist')
                            messages.error(request, 'Invalid credentials')
                    else:
                        print('Email Not Verified')
                        messages.error(
                            request,
                            'Your email is not verified. Please verify your email before logging in.'
                        )
                else:
                    print('No firebase user found')
                    messages.error(request, 'Invalid credentials')
            except Exception as e:
                print(e)
                pass
        else:
            print('Form is not valid')
            messages.error(request, 'Please fill in all the required fields appropriately.')
    else:
        print('Method is not post')
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout_view(request):
    logout(request)
    return redirect('home')