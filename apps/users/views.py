from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.models import ActivationKey, PasswordKey, User
from apps.users.serializers import BasePasswordSerializer, ChangeLanguageSerializer, ChangePasswordSerializer, \
    ForgottenPasswordSerializer, LoginSerializer, UserSerializer, VerificationEmailResendSerializer
from apps.utils.error_codes import Errors


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


class GetUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(instance=request.user).data)


class VerifyUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, activation_key):
        del request
        activation_key = get_object_or_404(ActivationKey, activation_key=str(activation_key))
        activated = activation_key.activate()
        if not activated:
            raise ValidationError(Errors.USER_ALREADY_VERIFIED.value)
        activation_key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeLanguageView(APIView):

    def post(self, request):
        serializer = ChangeLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lang = serializer.validated_data['language']
        request.user.change_language(lang)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer


class ForgottenPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResendVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerificationEmailResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, password_key):
        password_key = get_object_or_404(PasswordKey, password_key=str(password_key))
        if not password_key.validate_expiration():
            password_key.delete()
            return Response({'detail': Errors.RESET_PASSWORD_KEY_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BasePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password_key.user.set_password(serializer.validated_data['password'])
        password_key.user.save()

        # On success - deleting all the remaining password keys and authentication keys
        password_key.user.password_keys.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenRefreshViewWithActiveChecks(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        if access_token:
            self._validate_user_state(access_token)
        return response

    @staticmethod
    def _validate_user_state(access_token: str) -> None:
        token = AccessToken(token=access_token)
        user_id = token.get("user_id")
        user = User.objects.filter(id=user_id).first() if user_id else None
        if not user:
            raise ValidationError(Errors.USER_DOES_NOT_EXIST.value)
        if user.password_last_change and int(user.password_last_change.timestamp()) != token['datetime_claim']:
            raise ValidationError(Errors.USER_DATETIME_CLAIM_CHANGED.value)
        if not user.is_active:
            raise ValidationError(Errors.USER_IS_NOT_ACTIVE.value)