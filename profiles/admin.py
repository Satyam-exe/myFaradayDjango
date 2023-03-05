from django.contrib import admin
from .models import Profile


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        'user',
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


admin.site.register(Profile, ProfileModelAdmin)
