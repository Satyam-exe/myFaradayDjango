from django.urls import path
from .views import user_registration_view, user_login_view

urlpatterns = [
    path('signup/', user_registration_view, name='Sign Up'),
    path('login/', user_login_view, name='Log In'),
]