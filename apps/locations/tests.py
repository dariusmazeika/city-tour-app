from django.urls import reverse
from rest_framework import status

from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestGetCountries:
    def test_get_countries_returns_countries(self, client: APIClientWithQueryCounter, expected_country_data):
        path = reverse("country-list")
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expected_country_data == response.json()["results"]

    def test_get_countries_returns_empty_list(self, client: APIClientWithQueryCounter):
        path = reverse("country-list")
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert response.json()["count"] == 0
        assert response.json()["results"] == []
