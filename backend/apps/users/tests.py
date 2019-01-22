from apps.utils.tests_utils import BaseTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthentificationTestCase(BaseTestCase):

    def test_login_valid(self):
        response = self.client.post(
            reverse('login'),
            self.credentials,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

    def test_logout(self):
        response = self.authorize().post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user))

    def test_invalid_password(self):
        response = self.client.post(
            reverse('login'),
            {
                'email': self.user.email,
                'password': 'invalid'
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('non_field_errors' in response.data)
        self.assertTrue(
            'msg_error_bad_credentials' in response.data['non_field_errors'])

    def test_invalid_email(self):
        response = self.client.post(
            reverse('login'),
            {
                'email': 'invalid@email.com',
                'password': self.user.password
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('non_field_errors' in response.data)
        self.assertTrue(
            'msg_error_bad_credentials' in response.data['non_field_errors'])

    def test_missing_email(self):
        response = self.client.post(
            reverse('login'),
            {
                'password': self.user.password
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email']
                         [0], 'This field is required.')

    def test_missing_password(self):
        response = self.client.post(
            reverse('login'),
            {
                'email': self.user.email
            },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['password'][0], 'This field is required.')

    def test_get_current_user(self):
        response = self.authorize().get(reverse('current-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ['first_name', 'last_name', 'email']:
            self.assertEqual(response.data.get(field),
                             getattr(self.user, field))

    def test_get_user_not_authorized(self):
        response = self.client.get(reverse('current-user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json()['detail'], 'Authentication credentials were not provided.')
