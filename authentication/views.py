import requests
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status

from api import serializers
from . import forms
from .functions import verify_code
from .models import CustomUser


def sign_up_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form_data = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'email': form.cleaned_data.get('email'),
                'phone_number': form.cleaned_data.get('phone_number'),
                'password': form.cleaned_data.get('password2')
            }
            serializer = serializers.SignUpSerializer(data=form_data)
            if serializer.is_valid():
                serializer_data = serializer.validated_data
                url = 'http://localhost:8000/api/auth/signup/'
                response = requests.post(url=url, data=serializer_data)
                if response.status_code == 201:
                    return redirect('signup-success')
                elif response.status_code == 400:
                    messages.error(request, 'Invalid Credentials. Please Try Again.')
                elif response.status_code == 401:
                    messages.error(request, 'Your email is not verified. Please verify before logging in.')
                elif response.status_code == 500:
                    messages.error(request, 'Internal Server Error. Please Try Again.')
                elif response.status_code == 409:
                    messages.error(request, 'Conflicting Request. Please Try Again.')
                else:
                    messages.error(request, 'Something Went Wrong. Please Try Again')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})


def sign_up_success_view(request):
    return render(request, 'signupsuccess.html')


def log_in_view(request):
    if request.method == 'POST':
        form = forms.LogInForm(request.POST)
        if form.is_valid():
            serializer = serializers.LogInSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                data = serializer.validated_data
                url = 'http://localhost:8000/api/auth/login/'
                response = requests.post(url=url, data=data)
                if response.status_code == 200:
                    login(request, CustomUser.objects.get(pk=response.json().get('user').get('id')))
                    return redirect('home')
                elif response.status_code == 400:
                    messages.error(request, 'Invalid Credentials. Please Try Again.')
                elif response.status_code == 401:
                    messages.error(request, 'Your email is not verified. Please verify before logging in.')
                elif response.status_code == 500:
                    messages.error(request, 'Internal Server Error. Please Try Again.')
                elif response.status_code == 409:
                    messages.error(request, 'Conflicting Request. Please Try Again.')
                else:
                    messages.error(request, 'Something Went Wrong. Please Try Again')
    else:
        form = forms.LogInForm()
    return render(request, 'login.html', {'form': form})


@login_required
def log_out_view(request):
    logout(request)
    return redirect('login')


def password_reset_view(request):
    if request.method == 'POST':
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            serializer = serializers.ResetPasswordSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                data = serializer.validated_data
                url = 'http://localhost:8000/api/auth/passwordreset/'
                response = requests.post(url=url, data=data)
                if response.status_code == 200:
                    messages.success(request, 'A password reset link has been sent to your email successfully.')
                elif response.status_code == 400:
                    messages.error(request, 'User with the provided email does not exist.')
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
                messages.error(request,  'Please fill in all the fields appropriately.')
    else:
        form = forms.PasswordResetForm()
        if request.user.is_authenticated:
            return redirect('home')
    return render(request, 'resetpassword.html', {'form': form})


def confirm_password_reset_view(request, code):
    if request.method == "POST":
        print('code found')
        print(code)
        form = forms.ConfirmPasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('new_password2')
            serializer = serializers.ConfirmPasswordResetSerializer(data={'code': code, 'password': password})
            if serializer.is_valid():
                print('serializer is valid')
                data = serializer.validated_data
                print(data)
                url = 'http://localhost:8000/api/auth/passwordresetconfirm/'
                response = requests.post(url=url, data=data)
                form = None
                print(response.status_code)
                if response.status_code == 200:
                    messages.success(request, 'Your password has been reset successfully. Please log in.')
                elif response.status_code == 400:
                    pass
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
        form = forms.ConfirmPasswordResetForm()
        # if not verify_code(code, 'password_reset_confirm'):
        #     messages.error(request, 'The link is either expired or invalid. Please request a new one.')
        #     form = None
    print('rendering')
    return render(request, 'resetpasswordconfirm.html', {'form': form})


def verify_email_view(request, code):
    if request.method == "GET":
        print('request method is get')
        if code:
            print('code found')
            print(code)
            serializer = serializers.EmailVerificationSerializer(data={"code": code})
            if serializer.is_valid():
                print('rserializer is valid')
                data = serializer.validated_data
                print(serializer.validated_data)
                print('here')
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
            print('should redirect')
            return redirect('home')
    print('rendering')
    return render(request, 'verifyemail.html', {})


