from django.urls import path

from api.request.views import RequestAPIView

urlpatterns = [
    path('', RequestAPIView.as_view(), name='get-create-requests-api')
]