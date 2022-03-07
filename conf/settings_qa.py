from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ADMIN_COLOR = '#007704'  # Green
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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

# AWS access keys
AWS_S3_ACCESS_KEY_ID = "EDRTXJEZ0X6EMKE1BBWA"
AWS_S3_SECRET_ACCESS_KEY = "qxhPwheeKulTs/FJikLSH/czIOQnUcLeQyjRcNCi"
AWS_S3_REGION_NAME = "eu-central-1"
AWS_DEFAULT_ACL = "public-read"
AWS_STORAGE_BUCKET_NAME = f"media-{os.getenv('CI_PROJECT_NAME')}"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = f"https://minio.{os.getenv('CI_ENVIRONMENT_URL')}"

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'health_check.db',
    'health_check.cache',
    'health_check.contrib.migrations',
    'health_check.contrib.s3boto3_storage',
    'health_check.contrib.redis',
]
