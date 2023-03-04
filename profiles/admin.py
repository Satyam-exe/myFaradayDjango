from django.contrib import admin
from .models import ProfileModel


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        'firebase_uid',
        'first_name',
        'last_name',
        'date_of_birth',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'pincode',
        'email',
        'phone_number',
        'latitude',
        'longitude',
        'profile_picture',
    )


admin.site.register(ProfileModel, ProfileModelAdmin)
