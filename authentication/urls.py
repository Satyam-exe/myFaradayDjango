import os

from django.urls import path
from dotenv import load_dotenv

from . import views

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)


urlpatterns = [
    path(
        'signup/',
        views.sign_up_with_email_and_password_view,
        name="signup"
    ),
    path(
        'signup/success/',
        views.signup_success_view,
        name="signup-success"
    ),
    path(
        'login/',
        views.sign_in_with_email_and_password_view,
        name="login"
    ),
    path(
        'logout/',
        views.logout_view,
        name="logout"
    ),
    path(
        f"verify?mode=verifyEmail&oobCode=<str:oobCode>>",
        views.verify_email_view,
        name="verify-email"
    ),
    path(
        f"verify?mode=resetPassword&oobCode=<str:oobCode>",
        views.confirm_password_reset_view,
        name="reset-password"
    ),
]
