from django.contrib.admin import site
from django.db.models import Model
from django.urls import reverse
from model_bakery.baker import make
import pytest
from rest_framework import status

from apps.utils.tests_query_counter import APIClientWithQueryCounter


def get_model_name(value):
    admin = value  # because [site._registry[model]] is a model name inside a list
    return f"{admin.model._meta.model_name}"


class TestAdminSmokerCase:
    exclude = [
        "home_siteconfiguration_add",
        "home_siteconfiguration_delete",
        "admin_logentry_add",
        "admin_logentry_delete",
        "admin_logentry_list",
    ]

    @pytest.fixture
    def authorized_admin_client(self, client: APIClientWithQueryCounter, superuser, user_credentials):
        client.login(**user_credentials)
        return client

    def test_admin_index(self, authorized_admin_client):
        response = authorized_admin_client.get(reverse("admin:index"))
        assert response.status_code == status.HTTP_200_OK, response.request

    @pytest.mark.parametrize("site_admin", [site._registry[model] for model in site._registry], ids=get_model_name)
    def test_admin(self, site_admin, authorized_admin_client: APIClientWithQueryCounter):
        obj: Model = make(site_admin.model)
        for url in site_admin.urls:
            args = []
            if not url.name or url.name.endswith("autocomplete") or url.name in self.exclude:
                continue

            if getattr(url.pattern, "_route", "").startswith(("<path:object_id>", "<id>")):
                args = [obj.pk]

            response = authorized_admin_client.get(reverse(f"admin:{url.name}", args=args), query_limit=9)
            assert response.status_code == status.HTTP_200_OK, url.name


class TestBuildVersionCase:
    def test_build_version(self, settings, client):
        settings.BUILD_VERSION = 123
        response = client.get(reverse("build-version"))
        assert response.json() == 123, response.json()
