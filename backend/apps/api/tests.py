from django.urls import reverse
from rest_framework import status

from apps.utils.tests_utils import BaseTestCase


class PingTestCase(BaseTestCase):

    def test_ping_pong(self):
        response = self.client.get(reverse('ping'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'pong')
