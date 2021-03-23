from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.STORAGE_BUCKET_NAME  # type: ignore
    location = "media"
    file_overwrite = True
    custom_domain = f"{bucket_name}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com"  # type: ignore


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.STATIC_BUCKET_NAME  # type: ignore
    location = "static"
    file_overwrite = True
    custom_domain = f"{bucket_name}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com"  # type: ignore
