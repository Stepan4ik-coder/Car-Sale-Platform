from src.api import vrc
from src.exceptions import (
    StsImageIsDamagedHTTPException,
    StsImageIsNotRecognizedHTTPException,
)
from src.schemas.vrc import CarVinRequest


async def test_recognize_vrc(ac, monkeypatch):

    def fake_recognize_vin(image_path):
        return "JHDFS1ELT00000000"

    monkeypatch.setattr(vrc, "recognize_vin", fake_recognize_vin)

    vin_file = {"vin_file": ("test.jpg", b"fake image bytes", "image/jpeg")}
    response = await ac.post("/vrc", files=vin_file)

    assert response.status_code == 200
    assert response.json() == {"vin": "JHDFS1ELT00000000"}


async def test_vin_not_found(ac, monkeypatch):
    def fake_recognize_vin(image_path):
        raise StsImageIsNotRecognizedHTTPException()

    monkeypatch.setattr(vrc, "recognize_vin", fake_recognize_vin)

    vin_file = {"vin_file": ("test.jpg", b"fake image bytes", "image/jpeg")}
    response = await ac.post("/vrc", files=vin_file)

    assert response.status_code == 422
    assert response.json() == {"detail": "VIN-номер не распознан"}


async def test_damaged_image(ac, monkeypatch):
    def fake_recognize_vin(image_path):
        raise StsImageIsDamagedHTTPException()

    monkeypatch.setattr(vrc, "recognize_vin", fake_recognize_vin)

    vin_file = {"vin_file": ("test.jpg", b"fake image bytes", "image/jpeg")}
    response = await ac.post("/vrc", files=vin_file)

    assert response.status_code == 415
    assert response.json() == {"detail": "Фото повреждено"}


async def test_autofill(ac):
    data_to_autofill = CarVinRequest(vin="JA3BB51E9JU024751")

    response = await ac.post("/vrc/autofill", json=data_to_autofill.model_dump())

    assert response.status_code == 200
    assert response.json()["vin"] == "JA3BB51E9JU024751"
    assert response.json()["engine_type"] == "diesel"
    assert response.json()["year"] == 1996


async def test_incorrect_autofill(ac):
    data_to_autofill = {"vin": "1"}

    response = await ac.post("/vrc/autofill", json=data_to_autofill)

    assert response.status_code == 422
