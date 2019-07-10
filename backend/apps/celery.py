# pylint: disable=invalid-name
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger('app')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
app = Celery('apps')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'UTC'
