from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.sites.models import Site
from apps.sites.serializers import SiteSerializer
from apps.tours.models import Tour, UserTour
from apps.tours.serializers import UserTourSerializer, UserTourUpdateStatusSerializer, TourWithoutSitesSerializer
from apps.users.models import ActivationKey, PasswordKey, User
from apps.users.serializers import (
    BasePasswordSerializer,
    ChangeLanguageSerializer,
    ChangePasswordSerializer,
    ForgottenPasswordSerializer,
    LoginSerializer,
    UserSerializer,
    VerificationEmailResendSerializer,
    RegisterSerializer,
)
from apps.utils.error_codes import ApiErrors


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


class GetUserView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        return Response(UserSerializer(instance=request.user).data)


@extend_schema_view(put=extend_schema(responses={status.HTTP_204_NO_CONTENT: None}))
class VerifyUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = None

    @staticmethod
    def put(request, activation_key):
        del request
        activation_key = get_object_or_404(ActivationKey, activation_key=str(activation_key))
        activated = activation_key.activate()
        if not activated:
            raise ValidationError(ApiErrors.USER_ALREADY_VERIFIED)
        activation_key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeLanguageView(APIView):
    serializer_class = ChangeLanguageSerializer

    def post(self, request):
        serializer = ChangeLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lang = serializer.validated_data["language"]
        request.user.change_language(lang)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer


class ForgottenPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ForgottenPasswordSerializer

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = ForgottenPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResendVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerificationEmailResendSerializer

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = VerificationEmailResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(put=extend_schema(responses={status.HTTP_204_NO_CONTENT: None}))
class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BasePasswordSerializer

    @staticmethod
    def put(request, password_key):
        password_key = get_object_or_404(PasswordKey, password_key=str(password_key))
        if not password_key.validate_expiration():
            password_key.delete()
            return Response({"detail": ApiErrors.RESET_PASSWORD_KEY_EXPIRED}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BasePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password_key.user.set_password(serializer.validated_data["password"])
        password_key.user.save()

        # On success - deleting all the remaining password keys and authentication keys
        password_key.user.password_keys.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenRefreshViewWithActiveChecks(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        if access_token:
            self._validate_user_state(access_token)
        return response

    @staticmethod
    def _validate_user_state(access_token: str) -> None:
        token = AccessToken(token=access_token)
        user_id = token.get("user_id")
        user = User.objects.filter(id=user_id).first() if user_id else None
        if not user:
            raise ValidationError(ApiErrors.USER_DOES_NOT_EXIST)
        if user.password_last_change and int(user.password_last_change.timestamp()) != token["datetime_claim"]:
            raise ValidationError(ApiErrors.USER_DATETIME_CLAIM_CHANGED)
        if not user.is_active:
            raise ValidationError(ApiErrors.USER_IS_NOT_ACTIVE)


class GetUserToursViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
):
    serializer_class = UserTourSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        return UserTour.objects.filter(user=current_user)

    @action(detail=True, methods=["put"], url_path="update-status", serializer_class=UserTourUpdateStatusSerializer)
    def update_status(self, request, pk=None):
        user = self.request.user
        user_tour = get_object_or_404(UserTour, user=user, pk=pk)

        request.data["status"] = request.data.get("status", "").capitalize()
        serializer = self.get_serializer(user_tour, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="shared", serializer_class=TourWithoutSitesSerializer)
    def shared(self, request, pk=None):
        current_user = self.request.user
        queryset = Tour.objects.filter(
            usertour__user=current_user, usertour__shared_private_tour__isnull=False, is_enabled=True
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetUserSitesViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = SiteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        return Site.objects.filter(author=current_user)
