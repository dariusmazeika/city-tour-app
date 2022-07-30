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
from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestAuthentication:

    def test_login_valid(self, client: APIClientWithQueryCounter, user_credentials, user):
        response = client.post(reverse("login"), user_credentials, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert response.json()["token"]
        assert response.json()["refresh"]

    def test_login_invalid(self, client):
        credentials = {"email": "test@test.lt", "password": "password"}
        response = client.post(reverse("login"), credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_login_bad_credentials", response.json()

    def test_token_refresh(self, client: APIClientWithQueryCounter, user_credentials, user):
        response = client.post(reverse("login"), user_credentials, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        refresh = response.json()["refresh"]
        response = client.post(reverse("token-refresh"), {"refresh": refresh})
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json()["access"]
        assert response.json()["refresh"]

    def test_token_refresh_after_password_change(self, client: APIClientWithQueryCounter, user_credentials, user):
        response = client.post(reverse("login"), user_credentials, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        refresh = response.json()["refresh"]
        user.password_last_change = timezone.now() + datetime.timedelta(minutes=1)
        user.save()
        response = client.post(reverse("token-refresh"), {"refresh": refresh})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()[0] == "error_user_datetime_claim_changed"

    def test_token_verify(self, client: APIClientWithQueryCounter, user_credentials, user):
        response = client.post(reverse("login"), user_credentials, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        token = response.json()["token"]
        response = client.post(reverse("token-verify"), {"token": token})
        assert response.status_code == status.HTTP_200_OK

    def test_user_delete_with_active_token(self, client: APIClientWithQueryCounter, user_credentials, user):
        response = client.post(reverse("login"), user_credentials, format="json")
        User.objects.all().delete()
        client.credentials(HTTP_AUTHORIZATION=f"Token {response.json()['token']}")
        response = client.post(reverse("token-refresh"), {"refresh": response.json()["refresh"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()[0], "error_user_does_not_exist"

    def test_invalid_password(self, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("login"), {"email": user.email, "password": "invalid"}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"][0] == "error_login_bad_credentials"

    def test_invalid_email(self, client: APIClientWithQueryCounter, user):
        response = client.post(
            reverse("login"), {"email": "invalid@email", "password": user.password}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["email"][0] == "error_invalid_email"

    def test_missing_email(self, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("login"), {"password": user.password}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["email"][0] == "error_field_is_required"

    def test_missing_password(self, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("login"), {"email": user.email}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["password"][0] == "error_field_is_required"

    def test_get_current_user(self, authorized_client: APIClientWithQueryCounter, user):
        response = authorized_client.get(reverse("current-user"))
        assert response.status_code == status.HTTP_200_OK
        for field in ["first_name", "last_name", "email"]:
            assert response.json().get(field) == getattr(user, field)

    def test_get_user_not_authorized(self, client):
        response = client.get(reverse("current-user"))
        assert response.status_code, status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"], "Authentication credentials were not provided."

    @patch.object(PasswordKey, "send_password_key")
    def test_forgot_password(self, mock, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("forgot"), data={"email": user.email})
        assert response.status_code, status.HTTP_204_NO_CONTENT == response.json()
        assert user.password_keys.count() == 1
        assert PasswordKey.objects.count() == 1
        assert mock.called

    @patch.object(PasswordKey, "send_password_key")
    def test_forgot_password_non_existing_email(self, mock, client):
        response = client.post(reverse("forgot"), data={"email": "some@email.com"})
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert PasswordKey.objects.count() == 0
        assert not mock.called

    @patch.object(PasswordKey, "send_password_key")
    def test_reset_password_after_forgot_password(self, _, authorized_client: APIClientWithQueryCounter,
                                                  user_credentials, user):
        user.create_new_password_token()
        previous_psw = user_credentials.get("password")
        uuid = str(uuid4())
        reset_key = user.create_new_password_token()
        response = authorized_client.put(
            reverse("reset-password", args=[reset_key]),
            data={"password": uuid, "confirm_password": uuid}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        user.refresh_from_db()
        assert not user.check_password(previous_psw)
        assert user.check_password(uuid)
        assert not user.password_keys.count()

    @patch.object(PasswordKey, "send_password_key")
    def test_expired_password_key(self, mock, client: APIClientWithQueryCounter, user):
        del mock
        reset_key = user.create_new_password_token()
        user.password_keys.update(
            expires_at=timezone.now() - datetime.timedelta(hours=settings.PASSWORD_TOKEN_EXPIRATION_PERIOD + 1)
        )
        response = client.put(reverse("reset-password", args=[reset_key]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db()
        assert not user.password_keys.count()

    def test_resend_verification_email_required_data(self, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("resend-verification"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["email"][0] == "This field is required."

    @patch.object(ActivationKey, "send_verification")
    def test_resend_verification_email_to_verified_user(self, mock, client: APIClientWithQueryCounter, user):
        response = client.post(reverse("resend-verification"), data={"email": user.email})
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert not mock.called

    @patch.object(ActivationKey, "send_verification")
    def test_resend_verification_email_to_unverified_user(self, mock, client: APIClientWithQueryCounter, user):
        user.is_verified = False
        user.save()
        response = client.post(reverse("resend-verification"), data={"email": user.email})
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert mock.called

    @patch.object(ActivationKey, "send_verification")
    def test_verify_user(self, mock, client: APIClientWithQueryCounter, user):
        del mock
        user.is_verified = False
        user.save()
        verification_key = user.create_activation_key()
        assert not user.is_verified
        response = client.put(reverse("verify", args=[verification_key]))
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        user.refresh_from_db()
        assert user.is_verified
        assert not user.activation_keys.count()

    @patch.object(ActivationKey, "send_verification")
    def test_verify_user_again(self, mock, client: APIClientWithQueryCounter, user):
        del mock
        verification_key = user.create_activation_key()
        user.is_verified = True
        user.save()
        assert user.is_verified
        response = client.put(reverse("verify", args=[verification_key]))
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()[0] == "error_verify_already_verified"

    def test_change_language(self, authorized_client: APIClientWithQueryCounter, user):
        lang = make(Language)
        response = authorized_client.post(reverse("change-language"), data={"language": lang.code})
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        user.refresh_from_db()
        assert user.language == lang

    def test_change_to_invalid_language(self, authorized_client):
        response = authorized_client.post(reverse("change-language"), data={"language": "abc"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["language"][0] == "error_no_such_language"

    def test_change_password(self, authorized_client: APIClientWithQueryCounter, user, user_credentials):
        uuid = str(uuid4())
        previous_psw = user.password
        previous_psw_datetime = user.password_last_change
        response = authorized_client.post(
            reverse("change-password"),
            data={"old_password": user_credentials["password"], "password": uuid, "confirm_password": uuid}
        )
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        user.refresh_from_db()
        assert not previous_psw == user.password
        assert not user.password_keys.all().count()
        assert not user.password_last_change == previous_psw_datetime
        assert response.json()["access"]
        assert response.json()["refresh"]
        response = authorized_client.post(reverse("token-refresh"), {"refresh": response.json()["refresh"]})
        assert response.status_code == status.HTTP_200_OK, response.json()

    def test_change_password_not_equal(self, authorized_client: APIClientWithQueryCounter, user, user_credentials):
        previous_psw = user.password
        response = authorized_client.post(
            reverse("change-password"),
            data={
                "old_password": user_credentials["password"],
                "password": str(uuid4()),
                "confirm_password": str(uuid4())
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db()
        assert previous_psw == user.password
        assert response.json()["non_field_errors"][0] == "error_passwords_not_equal"
