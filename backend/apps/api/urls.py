# pylint: disable=invalid-name
"""
urls.py
API level urls
"""
from django.conf.urls import include
from django.urls import path, re_path
from django.views.defaults import page_not_found
from rest_framework.routers import DefaultRouter

from apps.api.views import PingView
from apps.manifests.views import AppConfigView
from apps.users.views import LoginView, LogoutView, GetUserView, VerifyUserView, ChangePasswordView, \
    ForgottenPasswordView, ResetPasswordView, ResendVerificationView, ChangeLanguageView

router = DefaultRouter()

urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
    path('app-config/', AppConfigView.as_view(), name='app-config'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current-user/', GetUserView.as_view(), name='current-user'),
    path('verify/<uuid:activation_key>/', VerifyUserView.as_view(), name='verify'),
    path('change-language/', ChangeLanguageView.as_view(), name='change-language'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot/', ForgottenPasswordView.as_view(), name='forgot'),
    path('reset-password/<uuid:password_key>/', ResetPasswordView.as_view(), name='reset-password'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('', include(router.urls)),
    # In case nothing matches in /api/ urls - return 404 error
    re_path('^.*?', page_not_found, {'exception': Exception('msg_error_page_not_found')})
]
