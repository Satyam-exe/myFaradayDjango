from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.authentication.urls')),
    path('profile/', include('api.profile.urls')),
    path('request/', include('api.request.urls'))
]
