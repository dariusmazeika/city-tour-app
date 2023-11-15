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


class TestCityTourFilterByTag:
    @staticmethod
    def expected_tours(tours_list_with_specific_tags):
        expected_tour_list_data = [
            {
                "id": tours_list_with_specific_tags[0].id,
                "created_at": tours_list_with_specific_tags[0].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": tours_list_with_specific_tags[0].updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "language": tours_list_with_specific_tags[0].language,
                "overview": tours_list_with_specific_tags[0].overview,
                "title": tours_list_with_specific_tags[0].title,
                "price": tours_list_with_specific_tags[0].price,
                "source": tours_list_with_specific_tags[0].source,
                "is_audio": tours_list_with_specific_tags[0].is_audio,
                "is_enabled": tours_list_with_specific_tags[0].is_enabled,
                "is_approved": tours_list_with_specific_tags[0].is_approved,
                "author": None,
            },
            {
                "id": tours_list_with_specific_tags[1].id,
                "created_at": tours_list_with_specific_tags[1].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": tours_list_with_specific_tags[1].updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "language": tours_list_with_specific_tags[1].language,
                "overview": tours_list_with_specific_tags[1].overview,
                "title": tours_list_with_specific_tags[1].title,
                "price": tours_list_with_specific_tags[1].price,
                "source": tours_list_with_specific_tags[1].source,
                "is_audio": tours_list_with_specific_tags[1].is_audio,
                "is_enabled": tours_list_with_specific_tags[1].is_enabled,
                "is_approved": tours_list_with_specific_tags[1].is_approved,
                "author": None,
            },
        ]

        return expected_tour_list_data

    def test_get_tours_by_one_tag(self, client: APIClientWithQueryCounter, tours_list_with_specific_tags):
        expected_tours_list = self.expected_tours(tours_list_with_specific_tags)
        tags = "?tag_id=4"
        path = reverse("city-tours-list", kwargs={"city_id": 5}) + tags
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()
        assert len(response.data["results"]) == 2
        assert expected_tours_list == response.json()["results"]

    def test_filter_tours_by_multiple_tags(self, client: APIClientWithQueryCounter, tours_list_with_specific_tags):
        expected_tours_list = self.expected_tours(tours_list_with_specific_tags)
        tags = "?tag_id=4&tag_id=5"
        path = reverse("city-tours-list", kwargs={"city_id": 5}) + tags
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()
        assert len(response.data["results"]) == 2
        assert expected_tours_list == response.json()["results"]
