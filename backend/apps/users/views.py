from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import ActivationKey, PasswordKey
from apps.users.serializers import BasePasswordSerializer, ChangeLanguageSerializer, ChangePasswordSerializer, \
    ForgottenPasswordSerializer, LoginSerializer, UserSerializer, VerificationEmailResendSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_logged_in.send(sender=self.__class__, request=request, user=user)
        return Response(serializer.validated_data["token"])


class GetUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(instance=request.user).data)


class VerifyUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def put(request, activation_key):
        del request
        activation_key_model = get_object_or_404(
            ActivationKey, activation_key=str(activation_key))
        activated = activation_key_model.activate()
        if not activated:
            raise ValidationError('error_verify_already_verified')
        activation_key_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeLanguageView(APIView):

    def post(self, request):
        serializer = ChangeLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lang = serializer.validated_data['language']
        request.user.change_language(lang)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):

    @staticmethod
    def post(request):
        serializer = ChangePasswordSerializer(data=request.data, context={
                                              'email': request.user.email})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        password_key = get_object_or_404(
            PasswordKey, password_key=str(password_key))
        if not password_key.validate_expiration():
            password_key.delete()
            return Response({'detail': 'error_reset_password_key_expired'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BasePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password_key.user.set_password(serializer.validated_data['password'])
        password_key.user.save()

        # On success - deleting all the remaining password keys and authentication keys
        password_key.user.password_keys.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
