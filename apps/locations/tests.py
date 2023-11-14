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


class TestGetCities:
    def test_get_city_returns_expected_city(self, client: APIClientWithQueryCounter, single_city, expected_city_data):
        path = reverse("city-detail", args=[single_city.id])
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert response.json() == expected_city_data

    def test_get_not_existing_city_returns_not_found(self, client: APIClientWithQueryCounter):
        not_existing_city_id = 100
        path = reverse("city-detail", args=[not_existing_city_id])
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()

    def test_get_cities_returns_expected_cities(self, client: APIClientWithQueryCounter, expected_two_cities_data):
        path = reverse("city-list")
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert response.json()["count"] == 2
        assert response.json()["results"] == expected_two_cities_data

    def test_get_cities_returns_empty_list(self, client: APIClientWithQueryCounter):
        path = reverse("city-list")
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert response.json()["count"] == 0
        assert response.json()["results"] == []
