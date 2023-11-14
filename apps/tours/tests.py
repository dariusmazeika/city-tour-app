from django.urls import reverse
from rest_framework import status

from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestGetTours:
    def test_get_tours_returns_tours(self, client: APIClientWithQueryCounter, single_tour, expected_tour_data):
        path = reverse("tours-detail", args=[single_tour.id])
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expected_tour_data == response.json()

    def test_get_not_existing_tour_returns_not_found(self, client: APIClientWithQueryCounter):
        not_existing_tour_id = 100
        path = reverse("tours-detail", args=[not_existing_tour_id])
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()


class TestTourFilterByCity:
    def test_filter_tours_by_city_id(self, client: APIClientWithQueryCounter, get_tours_list, expected_tours):
        path = reverse("city-tours-list", kwargs={"city_id": 5})
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expected_tours == response.json()["results"]

    def test_filter_tours_by_nonexistent_city_id(self, client: APIClientWithQueryCounter, get_tours_list):
        path = reverse("city-tours-list", kwargs={"city_id": 100000})
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
