from model_bakery.baker import make
import pytest

from apps.locations.models import City, Country


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
