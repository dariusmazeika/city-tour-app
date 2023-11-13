from model_bakery.baker import make
import pytest

from apps.tours.models import UserTour, Tour
from apps.users.models import User


@pytest.fixture
def expected_user_tour_list_response_results_payload(user: User) -> list:
    user_tour_1 = make(UserTour, tour=make(Tour), user=user)
    user_tour_2 = make(UserTour, tour=make(Tour), user=user)
    expected_response_payload = [
        {
            "id": user_tour_1.id,
            "tour": get_user_tour_data(user_tour_1),
            "created_at": user_tour_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "price": user_tour_1.price,
            "status": user_tour_1.status,
        },
        {
            "id": user_tour_2.id,
            "tour": get_user_tour_data(user_tour_2),
            "created_at": user_tour_2.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "price": user_tour_2.price,
            "status": user_tour_2.status,
        },
    ]
    return expected_response_payload


def get_user_tour_data(user_tour: UserTour) -> dict:
    tour = user_tour.tour
    return {
        "id": tour.id,
        "created_at": tour.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": tour.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "language": tour.language,
        "overview": tour.overview,
        "title": tour.title,
        "price": tour.price,
        "source": tour.source,
        "is_audio": tour.is_audio,
        "is_enabled": tour.is_enabled,
        "is_approved": tour.is_approved,
        "author": tour.author,
    }
