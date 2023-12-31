from django.contrib.auth import authenticate, user_logged_in
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

from apps.translations.models import Language
from apps.users.models import PasswordKey, User
from apps.utils.error_codes import ApiErrors
from apps.utils.token import get_token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return get_token(user)


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    password = PasswordField(required=True)
    password_validation = PasswordField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "password_validation")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["email"] = validated_data["email"].lower()
        validate_password(validated_data["password"])

        if validated_data["password"] != validated_data["password_validation"]:
            raise ValidationError("error_passwords_do_not_match")
        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError("error_user_with_this_email_already_exists")
        return validated_data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            is_verified=True,
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user


class LoginSerializer(CustomTokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": ApiErrors.BAD_CREDENTIALS,
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
            error_messages={"invalid": ApiErrors.INVALID_EMAIL, "required": ApiErrors.FIELD_IS_REQUIRED},
        )
        self.fields["password"] = PasswordField(error_messages={"required": ApiErrors.FIELD_IS_REQUIRED})

    def validate(self, attrs):
        try:
            validated_data = super(LoginSerializer, self).validate(attrs)
        except exceptions.AuthenticationFailed:
            raise serializers.ValidationError(ApiErrors.BAD_CREDENTIALS, code="authorization")

        if not self.user.is_verified:
            raise serializers.ValidationError(ApiErrors.USER_EMAIL_NOT_VERIFIED, code="authorization")

        validated_data["token"] = validated_data.pop("access")
        return validated_data

    def create(self, validated_data):
        user_logged_in.send(sender=self.__class__, request=self.context["request"], user=self.user)
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "balance")


class ChangeLanguageSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10, required=True)

    class Meta:
        fields = ("language",)

    @staticmethod
    def validate_language(attrs):
        if not Language.objects.filter(code=attrs).exists():
            raise serializers.ValidationError(ApiErrors.NO_SUCH_LANGUAGE)
        return attrs


class BasePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        fields = ("password", "confirm_password")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(ApiErrors.PASSWORDS_NOT_EQUAL)
        return attrs


class ChangePasswordSerializer(BasePasswordSerializer):
    old_password = PasswordField(required=True, write_only=True)

    class Meta:
        fields = ("old_password", "password", "confirm_password")

    def validate_old_password(self, attr):
        if not authenticate(email=self.context["request"].user.email, password=attr):
            raise serializers.ValidationError(ApiErrors.PASSWORD_IS_INCORRECT)
        return attr

    def to_representation(self, instance):
        refresh = get_token(self.context["request"].user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def create(self, validated_data):
        self.context["request"].user.set_password(validated_data["password"])
        self.context["request"].user.save()
        return {}


class ForgottenPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def create(self, validated_data):
        user = User.objects.filter(email__iexact=validated_data["email"]).first()

        if not user:
            # To prevent registered email checking we just do nothing here
            return {}

        PasswordKey.objects.filter(user=user).delete()
        user.create_new_password_token()
        return {}


class VerificationEmailResendSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    def create(self, validated_data):
        user = User.objects.filter(email__iexact=validated_data["email"], is_verified=False).first()

        if not user:
            # To prevent registered email checking we just do nothing here
            return {}

        user.create_activation_key()
        return {}
