from django.urls import path

from .views import *

urlpatterns = [
    path('', ProfileListAPIView.as_view(), name='get-all-profiles-api'),
    path('uid/<int:pk>/', ProfileRetrieveAPIView.as_view(), name='get-profile-api'),
]