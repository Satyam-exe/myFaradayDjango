from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LogInAPIView.as_view(), name='login-api'),
    path('users/', UserAPIView.as_view(), name='get-create-users-api'),
    path('users/uid/<int:pk>/', UserRetrieveAPIView.as_view(), name='get-user-by-uid-api'),
    path('users/email/<str:email>/', UserRetrieveWithEmailAPIView.as_view(), name='get-user-by-email-api'),
    path('users/phone/<str:phone_number>/', UserRetrieveWithPhoneNumberAPIView.as_view(), name='get-user-by-phone-api'),
    path('verifyemail/', EmailVerificationAPIView.as_view(), name='email-verification-api'),
    path('passwordreset/', PasswordResetAPIView.as_view(), name="password-reset-api"),
    path('passwordresetconfirm/', ConfirmPasswordResetAPIView.as_view(), name='password-reset-confirm-api'),
    path('sendemailverification/', SendEmailVerificationAPIView.as_view(), name='send-email-verification-api'),
    path('mobiletoken/verify/', VerifyMobileAuthTokenAPIView.as_view(), name='verify-mobile-auth-token-api'),
    path('mobiletoken/', MobileAuthTokenAPIView.as_view(), name='revoke-mobile-auth-token-api'),
]