from rest_framework import serializers

from request.models import RequestModel, FeedbackModel


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
