from django.contrib import admin
from .models import CustomUserProfile as Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
         'user_id',
         'first_name',
         'last_name',
         'gender',
         'phone_number',
         'secondary_phone_number',
         'email',
         'address',
         'city',
         'state',
         'pincode',
         'latitude',
         'longitude',
    )


admin.site.register(Profile, ProfileAdmin)
