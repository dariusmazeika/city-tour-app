import datetime
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from model_bakery.baker import make
from rest_framework import status

from apps.translations.models import Language
from apps.users.models import ActivationKey, PasswordKey, User
from apps.utils.tests_utils import BaseTestCase


class AuthenticationTestCase(BaseTestCase):

    def test_login_valid(self):
        response = self.client.post(reverse('login'), self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.assertTrue(response.data['expiry'])
        self.assertTrue(response.data['refresh'])
        self.assertTrue(response.data['refresh_expiry'])

    def test_login_invalid(self):
        credentials = {'email': 'test@test.lt', 'password': "password"}
        response = self.client.post(reverse('login'), credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'error_login_bad_credentials')

    def test_token_refresh(self):
        response = self.client.post(reverse('login'), self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh = response.data["refresh"]
        response = self.post(reverse('token-refresh'), {'refresh': refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['access'])

    def test_token_verify(self):
        response = self.client.post(reverse('login'), self.credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["token"]
        response = self.post(reverse('token-verify'), {"token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_with_active_token(self):
        response = self.client.post(reverse('login'), self.credentials, format='json')
        User.objects.all().delete()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')
        response = self.client.get(reverse('current-user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'user_does_not_exist')

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
            'error_login_bad_credentials' in response.data['non_field_errors'])

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
            'error_login_bad_credentials' in response.data['non_field_errors'])

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

    @patch.object(PasswordKey, 'send_password_key')
    def test_forgot_password(self, mock):
        response = self.client.post(reverse('forgot'), data={'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.password_keys.count(), 1)
        self.assertEqual(PasswordKey.objects.count(), 1)
        self.assertTrue(mock.called)

    @patch.object(PasswordKey, 'send_password_key')
    def test_forgot_password_non_existing_email(self, mock):
        response = self.client.post(reverse('forgot'), data={'email': 'some@email.com'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PasswordKey.objects.count(), 0)
        self.assertFalse(mock.called)

    @patch.object(PasswordKey, 'send_password_key')
    def test_reset_password_after_forgot_password(self, mock):
        del mock
        self.user.create_new_password_token()
        previous_psw = self.user.password
        uuid = str(uuid4())
        reset_key = self.user.create_new_password_token()
        response = self.client.put(
            reverse('reset-password', args=[reset_key]),
            data={'password': uuid, 'confirm_password': uuid}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertNotEqual(previous_psw, self.user.password)
        self.assertFalse(self.user.password_keys.count())

    @patch.object(PasswordKey, 'send_password_key')
    def test_expired_password_key(self, mock):
        del mock
        reset_key = self.user.create_new_password_token()
        self.user.password_keys.update(
            expires_at=timezone.now() - datetime.timedelta(hours=settings.PASSWORD_TOKEN_EXPIRATION_PERIOD + 1)
        )
        response = self.client.put(reverse('reset-password', args=[reset_key]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.password_keys.count())

    def test_resend_verification_email_required_data(self):
        response = self.client.post(reverse('resend-verification'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'][0], 'This field is required.')

    @patch.object(ActivationKey, 'send_verification')
    def test_resend_verification_email_to_verified_user(self, mock):
        response = self.client.post(reverse('resend-verification'), data={'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(mock.called)

    @patch.object(ActivationKey, 'send_verification')
    def test_resend_verification_email_to_unverified_user(self, mock):
        self.user.is_verified = False
        self.user.save()
        response = self.client.post(reverse('resend-verification'), data={'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(mock.called)

    @patch.object(ActivationKey, 'send_verification')
    def test_verify_user(self, mock):
        del mock
        self.user.is_verified = False
        self.user.save()
        verification_key = self.user.create_activation_key()
        self.assertFalse(self.user.is_verified)
        response = self.client.put(reverse('verify', args=[verification_key]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertFalse(self.user.activation_keys.count())

    @patch.object(ActivationKey, 'send_verification')
    def test_verify_user_again(self, mock):
        del mock
        verification_key = self.user.create_activation_key()
        self.user.is_verified = True
        self.user.save()
        self.assertTrue(self.user.is_verified)
        response = self.client.put(reverse('verify', args=[verification_key]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], 'error_verify_already_verified')

    def test_change_language(self):
        lang = make(Language)
        response = self.authorize().post(reverse('change-language'), data={'language': lang.code})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.language, lang)

    def test_change_to_invalid_language(self):
        response = self.authorize().post(reverse('change-language'), data={'language': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['language'][0], 'error_no_such_language')

    def test_change_password(self):
        uuid = str(uuid4())
        previous_psw = self.user.password
        response = self.authorize().post(
            reverse('change-password'),
            data={'old_password': self.credentials['password'], 'password': uuid, 'confirm_password': uuid}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertNotEqual(previous_psw, self.user.password)
        self.assertFalse(self.user.password_keys.all().count())

    def test_change_password_not_equal(self):
        previous_psw = self.user.password
        response = self.authorize().post(
            reverse('change-password'),
            data={
                'old_password': self.credentials['password'],
                'password': str(uuid4()),
                'confirm_password': str(uuid4())
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(previous_psw, self.user.password)
        self.assertEqual(response.json()['non_field_errors'][0], 'error_passwords_not_equal')
