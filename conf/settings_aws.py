from .settings import *

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False
TEMPLATE_DEBUG = False
ADMIN_COLOR = "#417690"  # Blue (default admin color)
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
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID)
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", AWS_DEFAULT_REGION)
AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
PRIVATE_FILE_STORAGE = "apps.utils.storage.PrivateMediaStorage"

# Below is set to False so that the default MediaStorage files would not have
# querystring auth unless explicitly set
AWS_QUERYSTRING_AUTH = False

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'health_check.db',
    'health_check.cache',
    'health_check.contrib.migrations',
    'health_check.contrib.s3boto3_storage',
    'health_check.contrib.redis',
]
