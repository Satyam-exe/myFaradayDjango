from django.urls import path
from .views import request_form_view

urlpatterns = [
    path('create/', request_form_view, name='Create Request'),
]