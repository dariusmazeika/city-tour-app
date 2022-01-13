from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from apps.users.views import ChangeLanguageView, ChangePasswordView, ForgottenPasswordView, GetUserView, LoginView, \
    ResendVerificationView, ResetPasswordView, TokenRefreshViewWithActiveChecks, VerifyUserView

router = DefaultRouter()

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshViewWithActiveChecks.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('current-user/', GetUserView.as_view(), name='current-user'),
    path('verify/<uuid:activation_key>/', VerifyUserView.as_view(), name='verify'),
    path('change-language/', ChangeLanguageView.as_view(), name='change-language'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot/', ForgottenPasswordView.as_view(), name='forgot'),
    path('reset-password/<uuid:password_key>/', ResetPasswordView.as_view(), name='reset-password'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
]