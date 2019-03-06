from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=255, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                'msg_error_bad_credentials', code='authorization')

        if not user.is_active:
            raise serializers.ValidationError(
                'msg_error_account_disabled', code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
