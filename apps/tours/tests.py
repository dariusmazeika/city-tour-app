from django.urls import reverse
from rest_framework import status

from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestGetTours:
    def test_get_tours_returns_tours(self, client: APIClientWithQueryCounter, single_tour, expexted_tour_data):
        path = reverse("tours-detail", args=[single_tour.id])
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expexted_tour_data == response.json()

    def test_get_not_existing_tour_returns_not_found(self, client: APIClientWithQueryCounter):
        not_existing_tour_id = 100
        path = reverse("tours-detail", args=[not_existing_tour_id])
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
