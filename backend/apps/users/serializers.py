from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.translations.models import Language
from apps.users.models import User, PasswordKey


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=255, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('msg_error_bad_credentials', code='authorization')

        if not user.is_active:
            raise serializers.ValidationError('msg_error_account_disabled', code='authorization')

        if not user.is_verified:
            raise serializers.ValidationError('msg_error_user_email_not_verified', code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangeLanguageSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10, required=True)

    class Meta:
        fields = ('language', )

    @staticmethod
    def validate_language(attrs):
        if not Language.objects.filter(code=attrs).exists():
            raise serializers.ValidationError('msg_error_no_such_language')
        return attrs


class BasePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('msg_error_passwords_not_equal')
        return attrs


class ChangePasswordSerializer(BasePasswordSerializer):
    old_password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        fields = ('old_password', 'password', 'confirm_password')

    def validate_old_password(self, attr):
        if not authenticate(email=self._context.get('email'), password=attr):
            raise serializers.ValidationError('msg_error_password_is_incorrect')
        return attr


class ForgottenPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def create(self, validated_data):
        user = User.objects.filter(email__iexact=validated_data['email']).first()

        if not user:
            # To prevent registered email checking we just do nothing here
            return {}

        PasswordKey.objects.filter(user=user).delete()
        user.create_new_password_token()
        return {}


class VerificationEmailResendSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def create(self, validated_data):
        user = User.objects.filter(email__iexact=validated_data['email'], is_verified=False).first()

        if not user:
            # To prevent registered email checking we just do nothing here
            return {}

        user.create_activation_key()
        return {}
