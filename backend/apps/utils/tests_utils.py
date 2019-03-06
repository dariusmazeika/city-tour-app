import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.translations.models import Language
from apps.users.models import User


class BaseTestCase(TestCase):
    email = 'test@test.lt'
    password = 'testtest'
    credentials = {'email': email, 'password': password}
    user_data = {'email': email, 'password': password, 'first_name': 'First', 'last_name': 'Last'}
    auth_url = reverse('login')

    def setUp(self):
        logging.disable(logging.INFO)
        self.language = Language.objects.create(
            name='test',
            code='en'
        )
        self.user = User.objects.create_user(**self.user_data)
        self.client = APIClient()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        super(BaseTestCase, self).tearDown()

    def authorize(self):
        token = self.client.post(self.auth_url, self.credentials).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client
