from django.contrib import admin
from .models import Request
# Register your models here.


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'name',
        'service_required',
        'issue',
        'address',
        'phone_number',
        'secondary_phone_number',
        'email',
        'is_forwarded',
        'forwarded_to',
        'is_closed',
    )


admin.site.register(Request, RequestAdmin)
