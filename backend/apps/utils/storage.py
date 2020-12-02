import os

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("STORAGE_BUCKET_NAME")
    location = "media"
    file_overwrite = True
    custom_domain = f"{bucket_name}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com"  # type: ignore


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("STATIC_BUCKET_NAME")
    location = "static"
    file_overwrite = True
    custom_domain = f"{bucket_name}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com"  # type: ignore
