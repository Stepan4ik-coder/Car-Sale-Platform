import pytest
from unittest.mock import MagicMock

from src.tasks.tasks_for_celery import send_notifications

from src.schemas.cars import CarCreate


@pytest.fixture
async def auth_client(ac):
    await ac.post("/auth/login", json={
        "email": "lays@pring.com",
        "password": "123456789",
    })
    return ac  # cookie уже в клиенте


@pytest.fixture
def test_for_fake_celery_task(monkeypatch):
    mock_delay = MagicMock()

    monkeypatch.setattr(
        send_notifications,
        "delay",
        mock_delay
    )


async def test_get_cars(auth_client):
    response = await auth_client.get("/cars")

    assert response.status_code == 200


async def test_correctly_add_cars(auth_client):
    car_data = CarCreate(
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

    response = await auth_client.post("/cars", json=car_data.model_dump())

    assert response.status_code == 200
    assert response.json()["vin"] == "JA3BB51E9JU024751"


async def test_incorrect_add_cars(ac):
    car_data = {
        "vin": "QI1",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await ac.post("/cars", json=car_data)

    assert response.status_code == 422


async def test_put_cars(auth_client):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]

    put_car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 4,
        "horse_power": 280,
        "year": 1986,
        "color": "red",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.put(f"/cars/{car_id}", json=put_car_data)

    assert response.status_code == 200
    assert response.json()["litres"] == 4
    assert response.json()["horse_power"] == 280
    assert response.json()["color"] == "red"


async def test_patch_cars(auth_client):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]

    patch_car_data = {
        "vin": "JA4BB51E9JU024751",
        "engine_type": "diesel",
        "litres": 2,
        "horse_power": 80,
        "year": 1996,
        "color": "blue",
        "country": "Korea",
        "price": 500000,
        "status": "active"
    }

    response = await auth_client.patch(f"/cars/{car_id}", json=patch_car_data)

    assert response.status_code == 200
    assert response.json()["vin"] == "JA4BB51E9JU024751"
    assert response.json()["engine_type"] == "diesel"
    assert response.json()["litres"] == 2
    assert response.json()["horse_power"] == 80
    assert response.json()["year"] == 1996
    assert response.json()["color"] == "blue"
    assert response.json()["country"] ==  "Korea"
    assert response.json()["price"] == 500000


async def test_delete_cars(auth_client, test_for_fake_celery_task):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]
    response = await auth_client.delete(f"/cars/{car_id}")

    assert response.status_code == 200



async def test_delete_without_access(auth_client):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]

    # Регистрируем 2-го юзера
    register_second_user = await auth_client.post(
        "/auth/register",
        json={
            "email": "second@example.com",
            "password": "123456789",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone_number": "89000000000",
        },
    )

    assert register_second_user.status_code == 200

    # Логинимся под 2-м юзером
    login_second_user = await auth_client.post(
        "/auth/login",
        json={
            "email": "second@example.com",
            "password": "123456789",
        },
    )

    assert login_second_user.status_code == 200


    car_to_del_by_second = await auth_client.delete(f"/cars/{car_id}")
    assert car_to_del_by_second.status_code == 403

    find_that_car = await auth_client.get(f"/cars/{car_id}")
    assert find_that_car.status_code == 200



async def test_put_without_access(auth_client):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]

    # Регистрируем 3-го юзера
    register_third_user = await auth_client.post(
        "/auth/register",
        json={
            "email": "third@example.com",
            "password": "123456789",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone_number": "89000000000",
        },
    )

    assert register_third_user.status_code == 200

    # Логинимся под 3-м юзером
    login_third_user = await auth_client.post(
        "/auth/login",
        json={
            "email": "third@example.com",
            "password": "123456789",
        },
    )

    assert login_third_user.status_code == 200


    put_car_data = {
        "vin": "JA3BB51E8JU024751",
        "engine_type": "diesel",
        "litres": 4,
        "horse_power": 280,
        "year": 1996,
        "color": "red",
        "country": "USA",
        "price": 2000000,
        "status": "active"
    }

    response = await auth_client.put(f"/cars/{car_id}", json=put_car_data)
    assert response.status_code == 403

    find_car = await auth_client.get(f"/cars/{car_id}")
    assert find_car.status_code == 200
    assert find_car.json()["engine_type"] == "gasoline"
    assert find_car.json()["litres"] == 3
    assert find_car.json()["price"] == 1000000


async def test_patch_without_access(auth_client):
    car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 3,
        "horse_power": 255,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.post("/cars", json=car_data)
    assert response.status_code == 200

    car_id = response.json()["car_id"]


    # Регистрируем 4-го юзера
    register_second_user = await auth_client.post(
        "/auth/register",
        json={
            "email": "fourth@example.com",
            "password": "123456789",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "phone_number": "89000000000",
        },
    )

    assert register_second_user.status_code == 200

    # Логинимся под 4-м юзером
    login_fourth_user = await auth_client.post(
        "/auth/login",
        json={
            "email": "fourth@example.com",
            "password": "123456789",
        },
    )

    assert login_fourth_user.status_code == 200


    patch_car_data = {
        "vin": "JA3BB51E9JU024751",
        "engine_type": "gasoline",
        "litres": 4,
        "horse_power": 280,
        "year": 1986,
        "color": "white",
        "country": "Japan",
        "price": 1000000,
        "status": "active"
    }

    response = await auth_client.patch(f"/cars/{car_id}", json=patch_car_data)
    assert response.status_code == 403

    find_car = await auth_client.get(f"/cars/{car_id}")
    assert find_car.status_code == 200
    assert find_car.json()["engine_type"] == "gasoline"
    assert find_car.json()["litres"] == 3
    assert find_car.json()["price"] == 1000000

