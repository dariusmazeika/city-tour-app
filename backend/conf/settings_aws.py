import json

from .settings import *

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# AWS access keys
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-central-1")

# Email settings
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = "django_amazon_ses.EmailBackend"

# S3 storage
STORAGE_BUCKET_NAME = os.environ.get("STORAGE_BUCKET_NAME")
STATIC_BUCKET_NAME = os.environ.get("STATIC_BUCKET_NAME")

DEFAULT_FILE_STORAGE = "apps.utils.storage.MediaStorage"
STATICFILES_STORAGE = "apps.utils.storage.StaticStorage"

# Below is set to False so that the default MediaStorage files would not have
# querystring auth unless explicitly set
AWS_QUERYSTRING_AUTH = False

# Unset MEDIA_ROOT, so health checks wont try to write in local file system
del MEDIA_ROOT

# RDS config
DB_CONF = json.loads(os.getenv("DB_SECRET"))
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", **DB_CONF}}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ADMIN_COLOR = '#6f4300'  # Brown
