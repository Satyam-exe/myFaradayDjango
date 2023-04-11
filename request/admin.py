from django.contrib import admin
from myFaraday.commons import linkify
from .models import Request, Feedback


class RequestModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        linkify(field_name='user'),
        linkify(field_name='location'),
        'time_of_request',
        'is_emergency',
        'issue',
        'is_forwarded',
        linkify(field_name='forwarded_to'),
        'is_closed',
    )


class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        linkify(field_name='request'),
        'rating',
        'likely_to_recommend',
        'feedback',
        'time_of_feedback',
    )


admin.site.register(Request, RequestModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)
