from django.urls import path
from .views import user_sign_up_view


urlpatterns = [
    path(
        'signup/',
        user_sign_up_view,
        name="signup"
    ),
]
