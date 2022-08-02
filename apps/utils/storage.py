from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    """Class for restricted uploaded files that will have a querystring auth"""
    querystring_auth = True
    default_acl = "private"


# Create storage class in similar manner as in django.core.files.storage.DefaultStorage:
class RestrictedStorage(LazyObject):
    def _setup(self):
        private_file_storage_class_path = getattr(settings, "PRIVATE_FILE_STORAGE", None)
        self._wrapped = get_storage_class(private_file_storage_class_path)()


restricted_file_storage = RestrictedStorage()
