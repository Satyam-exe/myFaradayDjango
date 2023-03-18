from django.urls import path
from .authentication import views as auth_views
from .profile import views as profile_views


urlpatterns = [
    path('auth/login/', auth_views.LogInAPIView.as_view(), name='login-api'),
    path('auth/users/', auth_views.UserAPIView.as_view(), name='get-create-users-api'),
    path('auth/users/uid/<int:pk>/', auth_views.UserRetrieveAPIView.as_view(), name='get-user-by-uid-api'),
    path('auth/users/email/<str:email>/', auth_views.UserRetrieveWithEmailAPIView.as_view(), name='get-user-by-email-api'),
    path('auth/users/phone/<str:phone_number>/', auth_views.UserRetrieveWithPhoneNumberAPIView.as_view(), name='get-user-by-phone-api'),
    path('auth/verifyemail/', auth_views.EmailVerificationAPIView.as_view(), name='email-verification-api'),
    path('auth/passwordreset/', auth_views.PasswordResetAPIView.as_view(), name="password-reset-api"),
    path('auth/passwordresetconfirm/', auth_views.ConfirmPasswordResetAPIView.as_view(), name='password-reset-confirm-api'),
    path('auth/sendemailverification/', auth_views.SendEmailVerificationAPIView.as_view(), name='send-email-verification-api'),
    path('auth/mobiletoken/verify/', auth_views.VerifyMobileAuthTokenAPIView.as_view(), name='verify-mobile-auth-token-api'),
    path('auth/mobiletoken/', auth_views.MobileAuthTokenAPIView.as_view(), name='revoke-mobile-auth-token-api'),

    path('profile/', profile_views.ProfileListAPIView.as_view(), name='get-all-profiles-api'),
    path('profile/uid/<int:pk>/', profile_views.ProfileRetrieveAPIView.as_view(), name='get-profile-api'),
]