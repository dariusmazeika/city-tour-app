from django.conf import settings
from django.urls import reverse
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

    def test_regenerate_manifest(self):
        url = reverse("regenerate-cache")
        response = self.client.get(url, format="json", HTTP_REFERER="test/url")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "test/url")

    def test_regenerate_manifest_redirects(self):
        site_config = SiteConfiguration.get_solo()
        url = reverse("regenerate-cache")
        url_final = reverse("app-config")

        response = self.client.get(url, format="json", HTTP_REFERER=url_final, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["version"], site_config.manifest_version)
        self.assertEqual(response.json()["default_language"], settings.DEFAULT_LANGUAGE)
        self.assertEqual(response.json()["enabled_languages"], [])
        self.assertEqual(response.json()["translations"]["en"], {})
        self.assertEqual(response.json()["translations"]["lt"], {})

    def test_regenerate_manifest_creates_site_config_with_authenticated_user(self):
        url = reverse("regenerate-cache")
        url_final = reverse("app-config")

        self.query_limits["ANY GET REQUEST"] = 10
        response = self.get(url, HTTP_REFERER=url_final, follow=True)
        site_config = SiteConfiguration.get_solo()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["version"], site_config.manifest_version)
        self.assertEqual(response.json()["default_language"], settings.DEFAULT_LANGUAGE)
        self.assertEqual(response.json()["enabled_languages"], [])
        self.assertEqual(response.json()["translations"]["en"], {})
        self.assertEqual(response.json()["translations"]["lt"], {})
