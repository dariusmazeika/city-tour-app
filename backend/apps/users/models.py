import datetime
import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone

from apps.translations.models import Language
from apps.utils.email import VERIFICATION_EMAIL_TEMPLATE, VERIFICATION_EMAIL_CATEGORY, PASSWORD_RESET_EMAIL_CATEGORY, \
    PASSWORD_RESET_EMAIL_TEMPLATE
from apps.utils.models import BaseModel
from apps.utils.tasks import send_email_task

LOGGER = logging.getLogger('app')


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = CIEmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    language = models.ForeignKey(
        Language,
        default=settings.DEFAULT_LANGUAGE,
        on_delete=models.CASCADE,
    )

    password_last_change = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.password_last_change = timezone.now()

    def verify(self):
        self.is_verified = True
        self.save()

    def create_activation_key(self) -> str:
        activation = ActivationKey.objects.create(user=self)
        activation.send_verification()
        return str(activation.activation_key)

    def create_new_password_token(self):
        psw_key = PasswordKey.objects.create(user=self)
        psw_key.send_password_key()
        return str(psw_key.password_key)

    def change_language(self, language_code: str):
        lang = Language.objects.filter(code=language_code).first()
        if lang:
            self.language = lang
            self.save()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Here we need to ignore mypy error https://github.com/typeddjango/django-stubs/issues/174#issuecomment-534210437
    # but setting explicit type will help to avoid multiple ignores in the usages (User.objects...)
    objects: 'models.QuerySet[User]' = UserManager()  # type: ignore


class ActivationKey(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_keys')
    activation_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def send_verification(self):
        LOGGER.info('Sending verification email to %s', self.user.email)
        context = {
            'activationUrl': settings.VERIFICATION_BASE_URL.format(settings.APP_HOST, self.activation_key)
        }

        send_email_task.delay(
            self.user.email,
            VERIFICATION_EMAIL_TEMPLATE,
            VERIFICATION_EMAIL_CATEGORY,
            context,
            self.user.language.code,
        )

    def activate(self) -> bool:
        if self.user.is_verified:
            return False
        self.user.verify()
        return True


class PasswordKey(BaseModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='password_keys')
    password_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField(blank=False, null=False)

    @staticmethod
    def _default_expiration_period():
        return timezone.now() + datetime.timedelta(hours=settings.PASSWORD_TOKEN_EXPIRATION_PERIOD)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = self._default_expiration_period()
        super().save(*args, **kwargs)

    def validate_expiration(self) -> bool:
        return self.expires_at >= timezone.now()

    def send_password_key(self):
        LOGGER.info('Sending password renewal email to %s', self.user.email)
        context = {
            'passwordUrl': settings.RESET_PASSWORD_BASE_URL.format(settings.APP_HOST, self.password_key)
        }

        send_email_task.delay(
            self.user.email,
            PASSWORD_RESET_EMAIL_TEMPLATE,
            PASSWORD_RESET_EMAIL_CATEGORY,
            context,
            self.user.language.code,
        )
