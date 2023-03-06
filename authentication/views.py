import requests
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status

from api import serializers
from . import forms
from . import firebase_auth
from .forms import SignUpForm, LogInForm
from .models import CustomUser


def sign_up_view(request):
    if request.method == 'POST':
        serializer = serializers.SignUpSerializer(data=request.POST)
        if serializer.is_valid():
            data = serializer.validated_data
            url = 'http://localhost:8000/api/signup/'
            response = requests.post(url=url, data=data)
            if response.status_code == 201:
                return redirect('signup-success')
            else:
                return messages.error(request, 'Something went wrong!')
        else:
            return render(request, 'signup.html', {'form': SignUpForm()})
    else:
        return render(request, 'signup.html', {'form': SignUpForm()})


def sign_up_success_view(request):
    return render(request, 'signupsuccess.html')


def log_in_view(request):
    if request.method == 'POST':
        serializer = serializers.LogInSerializer(data=request.POST)
        if serializer.is_valid():
            data = serializer.validated_data
            url = 'http://localhost:8000/api/login/'
            response = requests.post(url=url, data=data)
            if response.status_code == 200:
                login(request, CustomUser.objects.get(pk=response.json().get('user').get('id')))
                return redirect('home')
            elif response.status_code == 400:
                messages.error(request, f'Invalid Credentials. Please Try Again.')
            elif response.status_code == 500:
                messages.error(request, f'Internal Server Error. Please Try Again.')
            elif response.status_code == 409:
                messages.error(request, f'Conflicting Request. Please Try Again.')
            else:
                messages.error(request, f'Something Went Wrong. Please Try Again')
    return render(request, 'login.html', {'form': LogInForm()})


@login_required
def log_out_view(request):
    logout(request)
    return redirect('login')


# def password_reset_view(request):
#     if request.method == 'POST':
#         form = forms.PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             firebase_auth.send_password_reset_email(
#                 request=request,
#                 email=email,
#             )
#         else:
#             messages.error(request,  'Please fill in all the fields appropriately.')
#     else:
#         form = forms.PasswordResetForm()
#     return render(request, 'resetpassword.html', {'form': form})
#
#
# def confirm_password_reset_view(request):
#     oob_code = request.GET.get('oobCode')
#     if request.method == 'POST':
#         form = forms.ConfirmPasswordResetForm(request.POST)
#         if form.is_valid():
#             password = form.clean_new_password2()
#             firebase_auth.confirm_password_reset(
#                 oob_code=oob_code,
#                 new_password=password
#             )
#         else:
#             messages.error(request, 'Please fill in all the fields appropriately.')
#     else:
#         form = forms.ConfirmPasswordResetForm(request)
#     return render(request, 'resetpasswordconfirm.html', {'form': form})
#
#

def verify_email_view(request, code):
    if request.method == "GET":
        print('request method is get')
        if code:
            print('code found')
            serializer = serializers.URLCodeSerializer(data={'code': code})
            if serializer.is_valid():

                print('rserializer is valid')
                data = serializer.validated_data
                url = 'http://localhost:8000/api/auth/verifyemail/'
                response = requests.post(url=url, data=data)
                if response.status_code == 200:
                    messages.success(request, 'Your email has been successfully verified. Please log in.')
                elif response.status_code == 400:
                    messages.error(request, 'The link is either expired or invalid. Please request a new one.')
                elif response.status_code == 500:
                    print('status code is 500')
                    messages.error(request, f'Internal Server Error. Please Try Again.')
                elif response.status_code == 409:
                    print('status code is 409')
                    messages.error(request, f'Conflicting Request. Please Try Again.')
                else:
                    print('status code is else')
                    messages.error(request, f'Something Went Wrong. Please Try Again')
        else:
            print('should redirectt')
            return redirect('home')
    print('rendering')
    return render(request, 'verifyemail.html', {})


# @login_required
# def delete_user_view(request):
#     return firebase_auth.delete_user(request, to_redirect=True)
