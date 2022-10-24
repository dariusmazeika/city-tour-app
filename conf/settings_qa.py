from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ADMIN_COLOR = "#007704"  # Green
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# AWS access keys
AWS_ACCESS_KEY_ID = os.getenv("AWS_DJANGO_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_DJANGO_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-central-1")

# Email settings
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = "django_amazon_ses.EmailBackend"
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", AWS_DEFAULT_REGION)
AWS_SES_ACCESS_KEY_ID = os.getenv("AWS_SES_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
AWS_SES_SECRET_ACCESS_KEY = os.getenv("AWS_SES_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)

# S3 storage
AWS_STORAGE_BUCKET_NAME = f"media-{os.getenv('CI_PROJECT_NAME')}"
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID", "EDRTXJEZ0X6EMKE1BBWA")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY", "qxhPwheeKulTs/FJikLSH/czIOQnUcLeQyjRcNCi")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", AWS_DEFAULT_REGION)
AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
PRIVATE_FILE_STORAGE = "apps.utils.storage.PrivateMediaStorage"

AWS_S3_ENDPOINT_URL = f"https://minio.{os.getenv('CI_ENVIRONMENT_URL')}"

LOGGING["handlers"] = {
    "applogfile": {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": "/var/log/app.log",
    },
}

LOGGING["loggers"] = {
    "django": {
        "handlers": ["applogfile"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
    },
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.s3boto3_storage",
]
