# noinspection PyUnresolvedReferences
from .settings import *


# Do not use Redis in tests
REDIS_URL = ""
CELERY_BROKER_URL = REDIS_URL
