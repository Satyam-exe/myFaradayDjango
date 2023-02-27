from django.contrib import admin
from .models import CustomFirebaseUser


class CustomFirebaseUserAdmin(admin.ModelAdmin):
    list_display = (
        'firebase_uid',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    )


admin.site.register(CustomFirebaseUser, CustomFirebaseUserAdmin)
