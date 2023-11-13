from django.urls import reverse
from rest_framework import status

from apps.tours.models import UserTour, Tour
from apps.users.models import User
from apps.utils.tests_query_counter import APIClientWithQueryCounter


class TestGetTours:
    def test_get_tours_returns_tours(self, client: APIClientWithQueryCounter, single_tour, expected_tour_data):
        path = reverse("tours-detail", args=[single_tour.id])
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expected_tour_data == response.json()

    def test_get_not_existing_tour_returns_not_found(self, client: APIClientWithQueryCounter, not_existing_tour_id):
        path = reverse("tours-detail", args=[not_existing_tour_id])
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()


class TestBuyTour:
    def test_unauthenticated_client_cannot_buy_tour(self, client: APIClientWithQueryCounter, single_tour: Tour):
        response = client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    def test_non_existing_tour_returns_not_found(
        self, authorized_client: APIClientWithQueryCounter, not_existing_tour_id
    ):
        response = authorized_client.post(reverse("tours-buy", args=[not_existing_tour_id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()

    def test_cannot_buy_already_owned_tour(
        self, authorized_client: APIClientWithQueryCounter, single_tour: Tour, user: User
    ):
        UserTour.objects.create(tour=single_tour, user=user, price=single_tour.price)
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_tour_already_owned"

    def test_tour_bought_successfully(
        self, authorized_client: APIClientWithQueryCounter, single_tour: Tour, user: User, expected_tour_data: dict
    ):
        user.balance = single_tour.price + 1
        user.save(update_fields=["balance"])
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))
        assert response.status_code == status.HTTP_201_CREATED, response.json()

        # Check UserTour created in db
        user_tour_from_db = UserTour.objects.filter(tour__id=single_tour.id).first()
        assert user_tour_from_db is not None

        # Check if user balance was updated
        user.refresh_from_db()
        assert user.balance == 1

        expected_tour_data.pop("sites", None)  # Tour will be serialized without sites
        expected_response_payload = {
            "id": user_tour_from_db.id,
            "created_at": user_tour_from_db.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "price": single_tour.price,
            "status": "New",
            "tour": expected_tour_data,
        }
        assert response.json() == expected_response_payload

    def test_tour_price_greater_than_user_balance_response(
        self, authorized_client: APIClientWithQueryCounter, single_tour: Tour, user: User
    ):
        user.balance = 1
        user.save(update_fields=["balance"])
        single_tour.price = 10
        single_tour.save(update_fields=["price"])
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_wallet_balance_less_than_tour_price"
