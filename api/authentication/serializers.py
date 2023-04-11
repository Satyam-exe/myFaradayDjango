from django.db import transaction
from rest_framework import serializers
from authentication.models import CustomUser, URLCode, MobileAuthToken


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    signup_platform = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password', 'signup_platform')

    @transaction.atomic
    def create(self, validated_data):
        new_user = CustomUser.objects.create_user(
            **validated_data,
        )
        return new_user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    request_platform = serializers.ChoiceField(
        choices=(
            ('flutter', 'Flutter'),
            ('django', 'Django')),
        allow_blank=True,
        allow_null=True,
        required=False
    )
    requested_time_in_days = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        fields = ('email', 'password', 'request_platform', 'requested_time_in_days')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('email',)


class ConfirmPasswordResetSerializer(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('password',)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class EmailVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('code',)


class URLCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLCode
        fields = '__all__'


class MobileAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAuthToken
        fields = '__all__'


class VerifyMobileAuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    uid = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('token', 'uid')


class RevokeMobileAuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('token',)
