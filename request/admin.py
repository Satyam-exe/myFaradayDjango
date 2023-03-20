from django.contrib import admin
from .models import Request, Feedback


class RequestModelAdmin(admin.ModelAdmin):
    list_display = (
        'request_id',
        'user',
        'location',
        'time_of_request',
        'is_emergency',
        'issue',
        'is_forwarded',
        'forwarded_to',
        'is_closed',
    )


class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = (
        'request',
        'rating',
        'likely_to_recommend',
        'feedback',
        'time_of_feedback',
    )


admin.site.register(Request, RequestModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)
