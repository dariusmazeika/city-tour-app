"""
urls.py
API level urls
"""
from django.conf.urls import include
from django.urls import path, re_path
from django.views.defaults import page_not_found
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

from apps.api.views import PingView
from apps.manifests.views import AppConfigView
from apps.users.views import ChangeLanguageView, ChangePasswordView, ForgottenPasswordView, GetUserView, LoginView, \
    ResendVerificationView, ResetPasswordView, VerifyUserView

router = DefaultRouter()

urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
    path('app-config/', AppConfigView.as_view(), name='app-config'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('current-user/', GetUserView.as_view(), name='current-user'),
    path('verify/<uuid:activation_key>/', VerifyUserView.as_view(), name='verify'),
    path('change-language/', ChangeLanguageView.as_view(), name='change-language'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot/', ForgottenPasswordView.as_view(), name='forgot'),
    path('reset-password/<uuid:password_key>/', ResetPasswordView.as_view(), name='reset-password'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('', include(router.urls)),
    # In case nothing matches in /api/ urls - return 404 error
    re_path('^.*?', page_not_found, {'exception': Exception('error_api_page_not_found')})
]
