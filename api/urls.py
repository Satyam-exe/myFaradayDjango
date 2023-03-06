from django.urls import path
from .views import SignUpAPIView, LogInAPIView, UserRetrieveView, UserListView, EmailVerificationAPIView


urlpatterns = [
    path('auth/signup/', SignUpAPIView.as_view(), name='signup-api'),
    path('auth/login/', LogInAPIView.as_view(), name='login-api'),
    path('auth/users/', UserListView.as_view()),
    path('auth/users/<int:pk>/', UserRetrieveView.as_view()),
    path('auth/verifyemail/', EmailVerificationAPIView.as_view(), name='email-verification-api')
]
