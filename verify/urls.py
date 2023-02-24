from django.urls import path
from .views import \
    login_view, \
    signup_view, \
    logout_view, \
    reset_password_view, \
    confirm_reset_password_view, \
    email_verification_view


urlpatterns = [
    path(
        'login/',
        login_view,
        name="login"
    ),
    path(
        'signup/',
        signup_view,
        name="signup"
    ),
    path(
        'logout/',
        logout_view,
        name="logout"
    ),
    path(
        'resetpassword/',
        reset_password_view,
        name="reset-password"
    ),
    path(
        '__/action?mode=verifyEmail&oobCode=<str:oobCode>',
        email_verification_view,
        name="verify-email"
    ),
    path(
        '__/action?mode=resetPassword&oobCode=<str:oobCode>',
        confirm_reset_password_view,
        name="confirm-reset-password"
    ),
    path(
        '__/action?mode=verifyEmail&oobCode=<str:oobCode>',
        confirm_reset_password_view,
        name="confirm-change-email"
    ),
    path(
        '__/action?mode=verifyEmail&oobCode=<str:oobCode>',
        confirm_reset_password_view,
        name="2fa-enrollment"
    ),
]