from django.contrib import admin
from .models import Profile, HomeAddress, ProfileUpdates


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'first_name',
        'last_name',
        'date_of_birth',
        'email',
        'phone_number',
        'profile_picture',
    )


class HomeAddressModelAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'address1',
        'address2',
        'city',
        'state',
        'pincode',
        'latitude',
        'longitude',
    )


class ProfileUpdateModelAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'update_type',
        'updated_at',
        'updated_from',
        'updated_to'
    )


admin.site.register(Profile, ProfileModelAdmin)
admin.site.register(ProfileUpdates, ProfileUpdateModelAdmin)
admin.site.register(HomeAddress, HomeAddressModelAdmin)
