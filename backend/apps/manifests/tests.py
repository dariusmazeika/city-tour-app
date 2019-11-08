from django.urls import reverse
from django.conf import settings
from rest_framework import status

from apps.home.models import SiteConfiguration
from apps.utils.tests_utils import BaseTestCase


class AppConfigTestCase(BaseTestCase):

    def test_app_config(self):
        site_config = SiteConfiguration.get_solo()
        response = self.client.get(reverse('app-config'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['version'], site_config.manifest_version)
        self.assertEqual(response.json()['default_language'], settings.DEFAULT_LANGUAGE)
        self.assertEqual(response.json()['enabled_languages'], [])
        self.assertEqual(response.json()['translations']['lt'], {})
        self.assertEqual(response.json()['translations']['en'], {})
