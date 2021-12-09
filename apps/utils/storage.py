from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Class for public uploaded files that will not have a querystring auth, e.g. images that are intended to be
    included in the emails"""
    bucket_name = settings.STORAGE_BUCKET_NAME  # type: ignore
    default_region = settings.AWS_DEFAULT_REGION  # type: ignore
    location = "media"
    file_overwrite = False


class StaticStorage(S3Boto3Storage):
    """Static files storage"""
    bucket_name = settings.STATIC_BUCKET_NAME  # type: ignore
    default_region = settings.AWS_DEFAULT_REGION  # type: ignore
    location = "static"
    file_overwrite = True


class PrivateMediaStorage(MediaStorage):
    """Class for restricted uploaded files that will have a querystring auth"""
    querystring_auth = True
    default_acl = "private"


restricted_file_storage = PrivateMediaStorage() if settings.STORAGE_BUCKET_NAME else FileSystemStorage()  # type: ignore
