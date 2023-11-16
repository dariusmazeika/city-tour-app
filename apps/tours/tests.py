from django.urls import reverse
from model_bakery.baker import make
import pytest
from rest_framework import status

from apps.locations.models import City
from apps.sites.models import Site, BaseSite, SiteAudio
from apps.tours.models import UserTour, Tour, TourSite
from apps.users.models import User
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

    @pytest.mark.parametrize("is_approved,is_enabled", [(True, False), (False, True), (False, False)])
    def test_retrieve_tours_returns_only_approved_and_enabled_tours(
        self, client: APIClientWithQueryCounter, single_tour: Tour, is_approved, is_enabled
    ):
        tour = make(Tour, is_approved=is_approved, is_enabled=is_enabled)
        response = client.get(reverse("tours-detail", args=[tour.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()


class TestBuyTour:
    def test_unauthenticated_client_cannot_buy_tour(self, client: APIClientWithQueryCounter, single_tour: Tour):
        response = client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    def test_non_existing_tour_returns_not_found(self, authorized_client: APIClientWithQueryCounter):
        response = authorized_client.post(reverse("tours-buy", args=[100]))
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()

    def test_cannot_buy_already_owned_tour(
        self,
        authorized_client: APIClientWithQueryCounter,
        single_tour: Tour,
        user: User,
    ):
        UserTour.objects.create(tour=single_tour, user=user, price=single_tour.price)
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_tour_already_owned"

    @pytest.mark.parametrize("balance_difference", [(0, None), (1, None)])
    def test_tour_bought_successfully(
        self,
        authorized_client: APIClientWithQueryCounter,
        single_tour: Tour,
        user: User,
        expected_tour_data: dict,
        balance_difference: tuple,
    ):
        user.balance = single_tour.price + balance_difference[0]
        user.save(update_fields=["balance"])
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))
        assert response.status_code == status.HTTP_201_CREATED, response.json()

        # Check UserTour created in db
        user_tour_from_db = UserTour.objects.filter(tour__id=single_tour.id).first()
        assert user_tour_from_db is not None
        assert user_tour_from_db.tour == single_tour
        assert user_tour_from_db.user == user
        assert user_tour_from_db.price == single_tour.price
        assert user_tour_from_db.status == "New"

        # Check if user balance was updated
        user.refresh_from_db()
        assert user.balance == balance_difference[0]

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
        self,
        authorized_client: APIClientWithQueryCounter,
        single_tour: Tour,
        user: User,
    ):
        user.balance = 1
        user.save(update_fields=["balance"])
        single_tour.price = 10
        single_tour.save(update_fields=["price"])
        response = authorized_client.post(reverse("tours-buy", args=[single_tour.id]))

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_wallet_balance_less_than_tour_price"


class TestTourFilterByCity:
    def test_filter_tours_by_city_id(self, client: APIClientWithQueryCounter, get_tours_list, expected_tours):
        path = reverse("city-tours", args=[5])
        response = client.get(path)

        assert response.status_code == status.HTTP_200_OK, response.json()

        assert expected_tours == response.json()["results"]

    def test_filter_tours_by_nonexistent_city_id(self, client: APIClientWithQueryCounter, get_tours_list):
        path = reverse("city-tours", args=[100000])
        response = client.get(path)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()


class TestCreateTourEndpoint:
    def test_unauthenticated_user_cannot_create_tour(
        self, client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        response = client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    def test_cannot_create_tour_with_unapproved_site(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        unapproved_site = Site.objects.get(id=create_tour_request_data["sites_ids_ordered"][0])
        unapproved_site.is_approved = False
        unapproved_site.save(update_fields=["is_approved"])

        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_not_all_sites_are_approved"

    def test_cannot_create_tour_with_non_unique_site_ids(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        create_tour_request_data["sites_ids_ordered"][0] = create_tour_request_data["sites_ids_ordered"][1]

        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_site_ids_non_unique"

    def test_cannot_create_tour_with_different_site_city(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        site_with_changed_city = BaseSite.objects.get(site__id=create_tour_request_data["sites_ids_ordered"][0])
        site_with_changed_city.city = make(City)
        site_with_changed_city.save(update_fields=["city"])

        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_all_sites_not_in_same_city"

    def test_cannot_create_tour_with_different_site_languages(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        site_with_changed_language = Site.objects.get(id=create_tour_request_data["sites_ids_ordered"][0])
        site_with_changed_language.language = "LT"
        site_with_changed_language.save(update_fields=["language"])

        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert response.json()["non_field_errors"][0] == "error_sites_languages_not_same"

    def test_tour_created(self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict):
        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert Tour.objects.count() == 1

        created_tour_from_db = Tour.objects.first()
        created_tour_sites_ids = list(created_tour_from_db.sites.values_list("id", flat=True))

        expected_response_payload = {
            "id": created_tour_from_db.id,
            "language": create_tour_request_data["language"],
            "overview": create_tour_request_data["overview"],
            "title": create_tour_request_data["title"],
            "price": create_tour_request_data["price"],
            "source": create_tour_request_data["source"],
            "sites": list(
                Site.objects.filter(id__in=create_tour_request_data["sites_ids_ordered"]).values_list("id", flat=True)
            ),
            "is_audio": False,
        }

        assert response.json() == expected_response_payload
        assert created_tour_sites_ids == expected_response_payload["sites"]
        assert created_tour_from_db.language == expected_response_payload["language"]
        assert created_tour_from_db.overview == expected_response_payload["overview"]
        assert created_tour_from_db.title == expected_response_payload["title"]
        assert created_tour_from_db.price == expected_response_payload["price"]
        assert created_tour_from_db.source == expected_response_payload["source"]
        assert created_tour_from_db.is_audio == expected_response_payload["is_audio"]

        # check if site order was assigned correctly
        tour_site_0 = TourSite.objects.get(site_id=create_tour_request_data["sites_ids_ordered"][0])
        tour_site_1 = TourSite.objects.get(site_id=create_tour_request_data["sites_ids_ordered"][1])
        tour_site_2 = TourSite.objects.get(site_id=create_tour_request_data["sites_ids_ordered"][2])
        assert tour_site_0.order == 0
        assert tour_site_1.order == 1
        assert tour_site_2.order == 2

    def test_audio_tour_flag_set_correct(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        make(SiteAudio, site_id=create_tour_request_data["sites_ids_ordered"][0])
        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_201_CREATED, response.json()

        created_tour_from_db = Tour.objects.filter(id=response.json()["id"]).first()

        assert created_tour_from_db.is_audio is True
        assert response.json()["is_audio"] is True

    def test_non_existing_site_id_response(
        self, authorized_client: APIClientWithQueryCounter, create_tour_request_data: dict
    ):
        create_tour_request_data["sites_ids_ordered"][0] = 100000
        response = authorized_client.post(reverse("tours-list"), data=create_tour_request_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
        assert response.json()["detail"] == "error_one_or_more_sites_do_not_exist"
