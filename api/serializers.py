from rest_framework import serializers
from authentication.functions import send_email_verification_link
from authentication.models import CustomUser, URLCode, MobileAuthToken
from profiles.models import Profile


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

    def create(self, validated_data):
        new_user = CustomUser.objects.create_user(
            **validated_data,
        )
        profile = Profile(
            user=new_user,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            phone_number=new_user.phone_number
        )
        profile.save()
        send_email_verification_link(new_user.pk)
        return new_user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    request_platform = serializers.ChoiceField(
        choices=(
            ('flutter', 'Flutter'),
            ('django', 'Django')),
        allow_blank=True,
        allow_null=True
    )
    requested_time_in_days = serializers.CharField(
        allow_blank=True,
        allow_null=True
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

