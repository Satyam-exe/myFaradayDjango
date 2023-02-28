from django.urls import path
from .views import user_sign_up_view, user_login_view, user_logout_view

urlpatterns = [
    path(
        'signup/',
        user_sign_up_view,
        name="signup"
    ),
    path(
        'login/',
        user_login_view,
        name="login"
    ),
    path(
        'logout/',
        user_logout_view,
        name='logout'
    )
]
