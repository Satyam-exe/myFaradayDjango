from django.urls import path
from .views import \
    SignUpAPIView, \
    LogInAPIView, \
    UserRetrieveAPIView, \
    UserListAPIView, \
    EmailVerificationAPIView, \
    ConfirmPasswordResetAPIView, \
    PasswordResetAPIView, \
    SendEmailVerificationAPIView, \
    UserRetrieveWithEmailAPIView, \
    UserRetrieveWithPhoneNumberAPIView


urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('auth/login/', LogInAPIView.as_view(), name='login-api'),
    path('auth/users/', UserListAPIView.as_view()),
    path('auth/users/uid/<int:pk>/', UserRetrieveAPIView.as_view()),
    path('auth/users/email/<str:email>/', UserRetrieveWithEmailAPIView.as_view()),
    path('auth/users/phone/<str:phone_number>/', UserRetrieveWithPhoneNumberAPIView.as_view()),
    path('auth/verifyemail/', EmailVerificationAPIView.as_view(), name='email-verification-api'),
    path('auth/passwordreset/', PasswordResetAPIView.as_view(), name="password-reset-api"),
    path('auth/passwordresetconfirm/', ConfirmPasswordResetAPIView.as_view(), name='password-reset-confirm-api'),
    path('auth/sendemailverification/', SendEmailVerificationAPIView.as_view(), name='send-email-verification-api')
]
