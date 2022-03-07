from django.contrib.admin import site
from django.test import Client
from django.test import override_settings
from django.urls import reverse
from model_bakery.baker import make
from parameterized import parameterized
from rest_framework import status

from apps.utils.tests_utils import BaseTestCase


def get_model_name(testcase_func, param_num, param):
    return f"{testcase_func.__name__}_{param[0][0].model._meta.model_name}"


class AdminSmokerCase(BaseTestCase):
    exclude = [
        "home_siteconfiguration_add",
        "home_siteconfiguration_delete",
        "admin_logentry_add",
        "admin_logentry_delete",
    ]

    def setUp(self):
        super().setUp()
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        self.client = Client()
        self.client.login(**self.credentials)

    def test_admin_index(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.request)

    @parameterized.expand([[site._registry[model]] for model in site._registry], name_func=get_model_name)
    def test_admin(self, site_admin):
        obj = make(site_admin.model)
        for url in site_admin.urls:
            args = []
            if not url.name or url.name.endswith("autocomplete") or url.name in self.exclude:
                continue

            if getattr(url.pattern, "_route", "").startswith(("<path:object_id>", "<id>")):
                args = [obj.pk]

            response = self.client.get(reverse(f"admin:{url.name}", args=args))
            self.assertEqual(response.status_code, status.HTTP_200_OK, url.name)


class BuildVersionCase(BaseTestCase):
    @override_settings(BUILD_VERSION=123)
    def test_build_version(self):
        response = self.client.get(reverse("build-version"))
        self.assertEqual(response.json(), 123)
