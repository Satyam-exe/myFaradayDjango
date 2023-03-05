from django.contrib import admin
from .models import CustomFirebaseUser


class CustomFirebaseUserAdmin(admin.ModelAdmin):
    list_display = (
        'firebase_uid',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'signed_up',
        'last_login',
        'last_activity',
        'is_active',
        'is_staff',
        'is_superuser'
    )


admin.site.register(CustomFirebaseUser, CustomFirebaseUserAdmin)
