from .firebase_auth import send_email_verification_link
from .firebase_auth import send_password_reset_email
from .firebase_auth import get_firebase_user
from .firebase_auth import create_firebase_user
from .forms import SignupForm

from .models import CustomFirebaseUser

from django.shortcuts import redirect, reverse, render
from django.db import transaction
from django.contrib import messages

from firebase_admin import auth

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

