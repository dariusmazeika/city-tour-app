# noinspection PyUnresolvedReferences
from .settings import *

CELERY_TASK_ALWAYS_EAGER = True


# Do not use Redis in tests
REDIS_URL = ""
CELERY_BROKER_URL = REDIS_URL

INSTALLED_APPS = list(INSTALLED_APPS) + ['django_extensions']
