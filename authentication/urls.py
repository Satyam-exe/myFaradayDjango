import os

from django.urls import path
from dotenv import load_dotenv

from . import views

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'myFaraday', '.env')
load_dotenv(dotenv_path)


urlpatterns = [
    path(
        'signup/',
        views.sign_up_view,
        name="signup"
    ),
    path(
        'signup/success/',
        views.sign_up_success_view,
        name="signup-success"
    ),
    path(
        'login/',
        views.log_in_view,
        name="login"
    ),
    path(
        'logout/',
        views.log_out_view,
        name="logout"
    ),
     path(
         f"verifyemail/<str:code>/",
         views.verify_email_view,
         name="verify-email"
     ),
    # path(
    #     f"verify?mode=resetPassword&oobCode=<str:oobCode>",
    #     name="reset-password"
    # ),
]
