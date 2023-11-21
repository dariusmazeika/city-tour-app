from django.contrib.gis.geos import Point
from model_bakery.baker import make
import pytest

from apps.locations.models import City, Country
from apps.sites.models import BaseSite, Site, SiteTag
from apps.tours.models import Tour, TourSite


@pytest.fixture
def expected_country_data():
    country = make(Country)
    expected_country_data = [
        {
            "id": country.id,
            "name": country.name,
            "code": country.code,
        }
    ]
    return expected_country_data


@pytest.fixture
def expected_city_data(single_city: City):
    return get_city_data(single_city)


@pytest.fixture
def expected_two_cities_data():
    country = make(Country)
    first_city = make(City, country=country, image=None)
    second_city = make(City, country=country, image=None)
    expected_data = [
        get_city_data(first_city),
        get_city_data(second_city),
    ]
    return expected_data


@pytest.fixture
def single_city():
    country = make(Country)
    city = make(City, country=country, image=None)
    return city


def get_city_data(city: City) -> dict:
    country = city.country
    city_data = {
        "id": city.id,
        "name": city.name,
        "country": {
            "id": country.id,
            "name": country.name,
            "code": country.code,
        },
        "image": city.image,
    }
    return city_data


@pytest.fixture
def tours_list_with_specific_tags():
    city = make(City, id=5)
    base_site = make(BaseSite, city=city, location=Point(10, 10))
    site1 = make(Site, base_site=base_site)
    site2 = make(Site, base_site=base_site)
    site3 = make(Site, base_site=base_site)

    tag3 = make(SiteTag, id=3)
    tag4 = make(SiteTag, id=4)
    tag5 = make(SiteTag, id=5)
    tag6 = make(SiteTag, id=6)

    tour1 = make(Tour, is_enabled=True, is_approved=True)
    tour2 = make(Tour, is_enabled=True, is_approved=True)
    tour3 = make(Tour, is_enabled=True, is_approved=True)
    tour4 = make(Tour, is_enabled=True, is_approved=True)

    site1.tags.set([tag3, tag4])
    site2.tags.set([tag4, tag5])
    site3.tags.set([tag6])

    make(TourSite, site=site1, tour=tour1)
    make(TourSite, site=site2, tour=tour1)
    make(TourSite, site=site2, tour=tour2)
    make(TourSite, site=site3, tour=tour3)
    make(TourSite, site=site3, tour=tour4)

    return [tour1, tour2, tour3, tour4]
