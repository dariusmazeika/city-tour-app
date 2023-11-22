from django.urls import reverse
from model_bakery.baker import make
from rest_framework import status

from apps.reviews.models import Review
from apps.tours.models import UserTour


class TestCreateReview:
    def test_create_review(self, user, create_tour, authorized_client, review_data):
        make(UserTour, user=user, tour=create_tour, status=UserTour.FINISHED)

        response = authorized_client.post(reverse("review-list"), review_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()

        created_review = Review.objects.filter(tour=review_data["tour"]).first()
        review_count = Review.objects.filter(tour=review_data["tour"]).count()

        assert review_count == 1
        assert created_review.text == review_data["text"]
        assert created_review.rating == review_data["rating"]
        assert created_review.reviewer_id == user.id
        assert created_review.is_approved is False

    def test_create_review_no_text(self, user, create_tour, authorized_client, review_data_no_text):
        make(UserTour, user=user, tour=create_tour, status=UserTour.FINISHED)

        response = authorized_client.post(reverse("review-list"), review_data_no_text, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()

        created_review = Review.objects.filter(tour=create_tour).first()

        review_text = created_review.text or None

        assert review_text is None
        assert created_review.rating == review_data_no_text["rating"]
        assert created_review.reviewer.id == review_data_no_text["reviewer"]
        assert created_review.is_approved is True

    def test_create_review_already_reviewed(self, user, create_tour, authorized_client, review_data):
        make(UserTour, user=user, tour=create_tour, status=UserTour.FINISHED)

        response = authorized_client.post(reverse("review-list"), review_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.json()

        response = authorized_client.post(reverse("review-list"), review_data, format="json")

        review_count = Review.objects.filter(tour=create_tour).count()
        assert review_count == 1

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"][0] == "error_tour_already_reviewed", response.json()

    def test_create_review_tour_not_purchased(self, authorized_client, review_data):
        response = authorized_client.post(reverse("review-list"), review_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"][0] == "error_tour_not_purchased", response.json()

    def test_create_review_tour_not_finished(self, user, create_tour, authorized_client, review_data):
        make(UserTour, user=user, tour=create_tour, status=UserTour.NEW)
        response = authorized_client.post(reverse("review-list"), review_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"][0] == "error_tour_not_finished", response.json()
