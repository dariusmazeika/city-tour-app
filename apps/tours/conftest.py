from model_bakery.baker import make
import pytest

from apps.locations.models import City
from apps.sites.models import BaseSite, Site
from apps.tours.models import Tour, TourSite


@pytest.fixture
def expected_tour_data(single_tour: Tour) -> dict:
    site = single_tour.sites.first()
    base_site = site.base_site
    expected_tour_data = {
        "id": single_tour.id,
        "sites": [
            {
                "id": site.id,
                "created_at": site.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": site.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "title": site.title,
                "overview": site.overview,
                "language": site.language,
                "source": site.source,
                "is_approved": site.is_approved,
                "author": None,
                "base_site": {
                    "id": base_site.id,
                    "created_at": base_site.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "updated_at": base_site.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "longitude": base_site.longitude,
                    "latitude": base_site.latitude,
                    "title": base_site.title,
                    "city": base_site.city_id,
                },
            }
        ],
        "image": None,
        "reviews": [],
        "created_at": single_tour.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": single_tour.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "language": single_tour.language,
        "overview": single_tour.overview,
        "title": single_tour.title,
        "source": single_tour.source,
        "is_audio": single_tour.is_audio,
        "is_enabled": single_tour.is_enabled,
        "is_approved": single_tour.is_approved,
        "author": single_tour.author_id,
        "rating": None,
        "finished_count": single_tour.finished_count,
    }
    return expected_tour_data


@pytest.fixture
def expected_tour_data_with_1_review(single_tour: Tour) -> dict:
    site = single_tour.sites.first()
    base_site = site.base_site
    expected_tour_data = {
        "id": single_tour.id,
        "sites": [
            {
                "id": site.id,
                "created_at": site.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": site.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "title": site.title,
                "overview": site.overview,
                "language": site.language,
                "source": site.source,
                "is_approved": site.is_approved,
                "author": None,
                "base_site": {
                    "id": base_site.id,
                    "created_at": base_site.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "updated_at": base_site.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "longitude": base_site.longitude,
                    "latitude": base_site.latitude,
                    "title": base_site.title,
                    "city": base_site.city_id,
                },
            }
        ],
        "reviews": [
            {
                "id": 1,
                "text": "some text with over 20 symbols",
                "rating": 5,
                "reviewer": 1,
                "tour": single_tour.id,
            }
        ],
        "image": None,
        "created_at": single_tour.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": single_tour.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "language": single_tour.language,
        "overview": single_tour.overview,
        "title": single_tour.title,
        "source": single_tour.source,
        "is_audio": single_tour.is_audio,
        "is_enabled": single_tour.is_enabled,
        "is_approved": single_tour.is_approved,
        "finished_count": single_tour.finished_count,
        "author": single_tour.author_id,
    }
    return expected_tour_data


@pytest.fixture
def single_tour(user) -> Tour:
    base_site = make(BaseSite)
    site = make(Site, base_site=base_site)
    tour = make(Tour, is_approved=True, is_enabled=True, author=user)
    make(TourSite, site=site, tour=tour, order=1)

    return tour


@pytest.fixture
def expected_tours(tours_list):
    expected_tour_list_data = [
        {
            "id": tours_list[0].id,
            "image": None,
            "created_at": tours_list[0].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": tours_list[0].updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "language": tours_list[0].language,
            "overview": tours_list[0].overview,
            "title": tours_list[0].title,
            "rating": None,
            "source": tours_list[0].source,
            "is_audio": tours_list[0].is_audio,
            "is_enabled": tours_list[0].is_enabled,
            "is_approved": tours_list[0].is_approved,
            "finished_count": tours_list[0].finished_count,
            "author": tours_list[0].author_id,
        },
        {
            "id": tours_list[2].id,
            "image": None,
            "created_at": tours_list[2].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": tours_list[2].updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "language": tours_list[2].language,
            "overview": tours_list[2].overview,
            "title": tours_list[2].title,
            "rating": None,
            "source": tours_list[2].source,
            "is_audio": tours_list[2].is_audio,
            "is_enabled": tours_list[2].is_enabled,
            "is_approved": tours_list[2].is_approved,
            "finished_count": tours_list[2].finished_count,
            "author": tours_list[0].author_id,
        },
    ]

    return expected_tour_list_data


@pytest.fixture
def tours_list(user):
    city = make(City, id=5)
    base_site = make(BaseSite, city=city)
    site = make(Site, base_site=base_site)

    tour1, tour3 = make(Tour, is_enabled=True, is_approved=True, author=user, _quantity=2)
    tour2 = make(Tour, is_enabled=True, is_approved=True)
    not_enabled_tour = make(Tour, is_enabled=False, is_approved=True)
    not_approved_tour = make(Tour, is_enabled=False, is_approved=True)

    make(TourSite, site=site, tour=tour1)
    make(TourSite, site=site, tour=tour3)
    make(TourSite, site=site, tour=not_enabled_tour)
    make(TourSite, site=site, tour=not_approved_tour)

    return [tour1, tour2, tour3, not_enabled_tour, not_approved_tour]


@pytest.fixture
def create_tour_request_data():
    city = make(City)
    sites = make(Site, _quantity=3, language="EN", base_site__city=city, is_approved=True)
    request_data = {
        "sites_ids_ordered": [sites[2].id, sites[1].id, sites[0].id],
        "language": "EN",
        "overview": "string",
        "title": "string",
        "source": "string",
    }
    return request_data
