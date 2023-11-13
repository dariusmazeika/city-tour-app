from model_bakery.baker import make
import pytest

from apps.locations.models import Country


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
