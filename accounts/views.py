from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def user_registration_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_or_phone_number = form.cleaned_data.get('email_or_phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=email_or_phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profiles/edit/')
            else:
                raise forms.ValidationError(
                    'Invalid login credentials. Please try again.'
                )
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout_view(request):
    logout(request)
