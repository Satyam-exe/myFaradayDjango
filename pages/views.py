from django.contrib import messages
from django.shortcuts import render
from django.utils.html import format_html


# Create your views here.
def home_view(request):
    messages.error(request, format_html(
        'Your email is not verified. Please verify before logging in. <a href="#" role="button">Click here</a> to resend verification email.'))
    return render(request, 'home.html', {})
