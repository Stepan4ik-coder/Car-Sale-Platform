import pytest
from pydantic import ValidationError

from src.schemas.cars import CarCreate


def test_correct_vin():
    new_car = CarCreate(
        vin="JA3BB51E9JU024751",
        engine_type="gasoline",
        litres=3,
        horse_power=255,
        year=1986,
        color="white",
        country="Japan",
        price=1000000,
        status="active"
    )

    assert new_car.vin == "JA3BB51E9JU024751"


def test_incorrect_vin():
    with pytest.raises(ValidationError) as ex:
        CarCreate(
            vin="1",
            engine_type="gasoline",
            litres=3,
            horse_power=255,
            year=1986,
            color="white",
            country="Japan",
            price=1000000,
            status="active"
        )

    assert ex.value.errors()[0]["loc"] == ("vin",)


def test_incorrect_symbols_in_vin():
    with pytest.raises(ValidationError) as ex:
        CarCreate(
            vin="JQ3BB51E9JU024751",
            engine_type="gasoline",
            litres=3,
            horse_power=255,
            year=1986,
            color="white",
            country="Japan",
            price=1000000,
            status="active"
        )

    assert ex.value.errors()[0]["loc"] == ("vin",)
    assert ex.value.errors()[0]["type"] == "string_pattern_mismatch"