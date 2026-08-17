from src.schemas.cars import CarCreate


async def test_get_cars(ac):
    response = await ac.get("/cars")

    assert response.status_code == 200


async def test_add_cars_correctly(ac):
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

    response = await ac.post("/cars", json=car_data.model_dump())

    assert response.status_code == 200
    assert response.json()["vin"] == "JA3BB51E9JU024751"


async def test_add_cars_incorrectly(ac):
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