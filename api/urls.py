from django.urls import path
from .views import \
    SignUpAPIView, \
    LogInAPIView, \
    UserRetrieveView, \
    UserListView, \
    EmailVerificationAPIView, \
    ConfirmPasswordResetAPIView, \
    PasswordResetAPIView


urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('auth/login/', LogInAPIView.as_view(), name='login-api'),
    path('auth/users/', UserListView.as_view()),
    path('auth/users/<int:pk>/', UserRetrieveView.as_view()),
    path('auth/verifyemail/', EmailVerificationAPIView.as_view(), name='email-verification-api'),
    path('auth/passwordreset/', PasswordResetAPIView.as_view(), name="password-reset-api"),
    path('auth/passwordresetconfirm/', ConfirmPasswordResetAPIView.as_view(), name='password-reset-confirm-api')
]
