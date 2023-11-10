from model_bakery.baker import make
import pytest

from apps.sites.models import BaseSite, Site
from apps.tours.models import Tour, TourSite


@pytest.fixture
def expected_tour_data(single_tour: Tour):
    site = single_tour.sites.first()
    base_site = site.base_site
    expected_tour_data = {
        "id": single_tour.id,
        "sites": [
            {
                "id": site.id,
                "created_at": site.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": site.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
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
                    "city": base_site.city.id,
                },
            }
        ],
        "created_at": single_tour.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": single_tour.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "language": single_tour.language,
        "overview": single_tour.overview,
        "title": single_tour.title,
        "price": single_tour.price,
        "source": single_tour.source,
        "is_audio": single_tour.is_audio,
        "is_enabled": single_tour.is_enabled,
        "is_approved": single_tour.is_approved,
        "author": None,
    }
    return expected_tour_data


@pytest.fixture
def single_tour():
    base_site = make(BaseSite)
    site = make(Site, base_site=base_site)
    tour = make(Tour)
    make(TourSite, site=site, tour=tour, order=1)

    return tour
