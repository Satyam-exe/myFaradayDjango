from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
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


admin.site.register(CustomUser, CustomUserAdmin)
