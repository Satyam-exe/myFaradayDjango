from django.contrib import admin
from .models import RequestModel


class RequestModelAdmin(admin.ModelAdmin):
    list_display = (
        'request_id',
        'firebase_uid',
        'name',
        'time_of_request',
        'address',
        'city',
        'state',
        'country',
        'pincode',
        'email',
        'phone_number',
        'latitude',
        'longitude',
    )


admin.site.register(RequestModel, RequestModelAdmin)
