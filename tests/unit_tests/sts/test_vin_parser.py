import pytest

from src.exceptions import IncorrectStsStringException
from src.services.sts.vin_parser import clear_vin, find_vin_candidate


def test_clear_vin():
    old_vin = "—_JHDFSi}ELTO0000000"
    expected_vin = "JHDFS1ELT00000000"

    vin = clear_vin(old_vin)

    assert vin == expected_vin


@pytest.mark.parametrize("vin", ["—_JHDFSi}EO0000000", "JHDFS1ELT0000000Q"])
def test_incorrect_vin(vin):
    with pytest.raises(IncorrectStsStringException) as ex:
        clear_vin(vin)

    assert str(ex.value) == "Невалидные данные СТС"


def test_find_vin_candidate():
    data = ["СВИДЕТЕЛЬСТВО", "—_JHDFSi}ELTO0000000", "Люблю мороженое", "Автомашина"]

    data_dict = {"text": data}

    result = find_vin_candidate(data_dict)

    assert result == "JHDFS1ELT00000000"


def test_lack_of_vin():
    data = ["СВИДЕТЕЛЬСТВО", "123", "Люблю мороженое", "Автомашина"]

    data_dict = {"text": data}
    with pytest.raises(IncorrectStsStringException) as ex:
        find_vin_candidate(data_dict)

    assert str(ex.value) == "Невалидные данные СТС"
