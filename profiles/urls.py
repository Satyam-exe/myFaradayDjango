from django.urls import path
from .views import profile_form_view

urlpatterns = [
    path('edit/', profile_form_view, name='Edit Profile'),
]