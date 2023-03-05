from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import forms
from . import firebase_auth


def sign_up_with_email_and_password_view(request):
    if request.method == 'POST':
        form = forms.SignUpWithEmailAndPasswordForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            firebase_auth.sign_up_with_email_and_password(
                request=request,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
                to_redirect=True
            )
        else:
            messages.error(request,  'Please fill in all the fields appropriately.')
    else:
        form = forms.SignUpWithEmailAndPasswordForm()
    return render(request, 'signup.html', {'form': form})


def signup_success_view(request):
    return render(request, 'signupsuccess.html')


def sign_in_with_email_and_password_view(request):
    if request.method == 'POST':
        form = forms.SignInWithEmailAndPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            firebase_auth.sign_in_with_email_and_password(
                request=request,
                email=email,
                password=password,
                to_redirect=True
            )
        else:
            messages.error(request,  'Please fill in all the fields appropriately.')
    else:
        form = forms.SignInWithEmailAndPasswordForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def password_reset_view(request):
    if request.method == 'POST':
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            firebase_auth.send_password_reset_email(
                request=request,
                email=email,
            )
        else:
            messages.error(request,  'Please fill in all the fields appropriately.')
    else:
        form = forms.PasswordResetForm()
    return render(request, 'resetpassword.html', {'form': form})


def confirm_password_reset_view(request):
    oob_code = request.GET.get('oobCode')
    if request.method == 'POST':
        form = forms.ConfirmPasswordResetForm(request.POST)
        if form.is_valid():
            password = form.clean_new_password2()
            firebase_auth.confirm_password_reset(
                oob_code=oob_code,
                new_password=password
            )
        else:
            messages.error(request, 'Please fill in all the fields appropriately.')
    else:
        form = forms.ConfirmPasswordResetForm(request)
    return render(request, 'resetpasswordconfirm.html', {'form': form})


def verify_email_view(request):
    oob_code = request.GET.get('oobCode')
    firebase_auth.confirm_email_verification(request, oob_code)
    return render(request, 'verifyemail.html')


@login_required
def delete_user_view(request):
    return firebase_auth.delete_user(request, to_redirect=True)
