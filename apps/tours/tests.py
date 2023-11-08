from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.tours.models import Tour


class GetToursTestCase(TestCase):
    def setUp(self) -> None:
        self.tour = baker.make(Tour, make_m2m=True)

    def test_get_tours_returns_tours(self):
        tour_id = 1
        path = reverse("tours-detail", args=[tour_id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        retrieved_tour_id = response.data["id"]
        self.assertEqual(retrieved_tour_id, tour_id)

        created_tour = Tour.objects.all().first()
        self.assertEqual(created_tour, self.tour)

    def test_get_not_existing_tour_returns_not_found(self):
        tour_id = 100
        path = reverse("tours-detail", args=[tour_id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
