import pytest

from src.schemas.cars import CarCreate
from src.utils.db_manager import DBManager


@pytest.fixture
async def auth_client(ac):
    await ac.post("/auth/login", json={
        "email": "lays@pring.com",
        "password": "123456789",
    })
    return ac  # cookie уже в клиенте


async def test_get_all_fav_cars(auth_client):
    response = await auth_client.get("/favorites")

    assert response.status_code == 200


async def test_add_new_fav_cars(db: DBManager, auth_client):
    car = await db.cars.add(CarCreate(
        vin="1FA6P8CF0H5194382",
        engine_type="gasoline",
        litres=3,
        horse_power=255,
        year=1986,
        color="white",
        country="Japan",
        price=1000000,
        status="active",
    ))
    await db.commit()

    response = await auth_client.post("/favorites", json={"car_id": car.car_id})

    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
