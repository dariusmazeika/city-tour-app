from django.urls import reverse
import pytest
from rest_framework import status

from apps.home.models import SiteConfiguration
from apps.translations.models import Language
from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestAppConfig:

    @pytest.fixture(autouse=True)
    def additional_language(self):
        return Language.objects.get_or_create(code="en", defaults={"name": "English"})[0]

    def test_app_config(self, settings, client):
        site_config = SiteConfiguration.get_solo()
        response = client.get(reverse('app-config'), format='json')
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json()['version'] == site_config.manifest_version
        assert response.json()['default_language'] == settings.DEFAULT_LANGUAGE
        assert response.json()['enabled_languages'] == []
        assert response.json()['translations']['lt'] == {}
        assert response.json()['translations']['en'] == {}

    def test_regenerate_manifest(self, client):
        url = reverse("regenerate-cache")
        response = client.get(url, format="json", HTTP_REFERER="test/url")
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == "test/url"

    def test_regenerate_manifest_redirects(self, settings, client):
        site_config = SiteConfiguration.get_solo()
        url = reverse("regenerate-cache")
        url_final = reverse("app-config")

        response = client.get(url, format="json", HTTP_REFERER=url_final, follow=True)

        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json()["version"] == site_config.manifest_version
        assert response.json()["default_language"] == settings.DEFAULT_LANGUAGE
        assert response.json()["enabled_languages"] == []
        assert response.json()["translations"]["en"] == {}
        assert response.json()["translations"]["lt"] == {}

    def test_regenerate_manifest_creates_site_config_with_authenticated_user(self, settings,
                                                                             client: APIClientWithQueryCounter):
        url = reverse("regenerate-cache")
        url_final = reverse("app-config")

        response = client.get(url, HTTP_REFERER=url_final, follow=True, query_limit=6)
        site_config = SiteConfiguration.get_solo()

        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json()["version"] == site_config.manifest_version
        assert response.json()["default_language"] == settings.DEFAULT_LANGUAGE
        assert response.json()["enabled_languages"] == []
        assert response.json()["translations"]["en"] == {}
        assert response.json()["translations"]["lt"] == {}
