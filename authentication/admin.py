from django.contrib import admin
from .models import CustomUser, Worker


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'uid',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'signed_up',
        'last_login',
        'last_activity',
        'is_email_verified',
        'is_active',
        'is_staff',
        'is_superuser'
    )


class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'wid',
        'user',
        'aadhar_number',
        'pan',
        'requests_completed',
        'rating',
        'worker_type',
        'is_available',
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Worker, WorkerAdmin)
