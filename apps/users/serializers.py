from django.contrib.auth import authenticate, user_logged_in
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

from apps.translations.models import Language
from apps.users.models import PasswordKey, User
from apps.utils.error_codes import Errors
from apps.utils.token import get_token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return get_token(user)


class LoginSerializer(CustomTokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": Errors.BAD_CREDENTIALS.value,
    }

    token = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Not defined as class variables since DRF ignores class variables if its already defined in self.fields
        # And simple-JWT defines username_field via self.fields
        self.fields[self.username_field] = serializers.EmailField(
            write_only=True,
            required=True,
            error_messages={"invalid": Errors.INVALID_EMAIL.value, "required": Errors.FIELD_IS_REQUIRED.value},
        )
        self.fields["password"] = PasswordField(error_messages={"required": Errors.FIELD_IS_REQUIRED.value})

    def validate(self, attrs):
        try:
            validated_data = super(LoginSerializer, self).validate(attrs)
        except exceptions.AuthenticationFailed:
            raise serializers.ValidationError(Errors.BAD_CREDENTIALS.value, code="authorization")

        if not self.user.is_verified:
            raise serializers.ValidationError(Errors.USER_EMAIL_NOT_VERIFIED.value, code="authorization")

        validated_data["token"] = validated_data.pop("access")
        return validated_data

    def create(self, validated_data):
        user_logged_in.send(sender=self.__class__, request=self.context["request"], user=self.user)
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangeLanguageSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10, required=True)

    class Meta:
        fields = ('language',)

    @staticmethod
    def validate_language(attrs):
        if not Language.objects.filter(code=attrs).exists():
            raise serializers.ValidationError(Errors.NO_SUCH_LANGUAGE.value)
        return attrs


class BasePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(Errors.PASSWORDS_NOT_EQUAL.value)
        return attrs


class ChangePasswordSerializer(BasePasswordSerializer):
    old_password = PasswordField(required=True, write_only=True)

    class Meta:
        fields = ("old_password", "password", "confirm_password")

    def validate_old_password(self, attr):
        if not authenticate(email=self.context["request"].user.email, password=attr):
            raise serializers.ValidationError(Errors.PASSWORD_IS_INCORRECT.value)
        return attr

    def to_representation(self, instance):
        refresh = get_token(self.context["request"].user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def create(self, validated_data):
        self.context["request"].user.set_password(validated_data["password"])
        self.context["request"].user.save()
        return {}


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
