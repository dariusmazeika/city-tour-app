from model_bakery.baker import make
import pytest

from apps.reviews.models import Review
from apps.sites.models import Site, BaseSite
from apps.tours.models import Tour


@pytest.fixture
def create_tour(user):
    base_site = make(BaseSite)
    site = make(Site, base_site=base_site)
    tour = make(Tour, sites=[site])

    return tour


@pytest.fixture
def review_data(user, create_tour):
    return {"text": "some text with over 20 symbols", "rating": 5, "reviewer": user.id, "tour": create_tour.id}


@pytest.fixture
def review_data_no_text(user, create_tour):
    return {"rating": 5, "reviewer": user.id, "tour": create_tour.id}


@pytest.fixture
def review(user, create_tour):
    return Review.objects.create(tour=create_tour, reviewer=user, text="some text with over 20 symbols", rating=5)
