from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from apps.utils.tests_utils import BaseTestCase


class WatchmanCase(BaseTestCase):
    def test_watchman_state(self):
        response = self.client.get(reverse("watchman"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BuildVersionCase(BaseTestCase):
    @override_settings(BUILD_VERSION=123)
    def test_build_version(self):
        response = self.client.get(reverse("build-version"))
        self.assertEqual(response.json(), 123)
