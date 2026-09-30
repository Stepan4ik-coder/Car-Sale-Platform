from src.schemas.cars import CarCreate


async def test_car_crud(db):
    # Добавление авто
    car_data = CarCreate(
        vin="JA3BB51E9JU024751",
        engine_type="gasoline",
        litres=3,
        horse_power=255,
        year=1986,
        color="white",
        country="Japan",
        price=1000000,
        status="active",
    )

    new_car = await db.cars.add(car_data, owner_id=1)

    assert new_car.car_id is not None
    assert new_car.engine_type == "gasoline"
    assert new_car.status == "active"

    # Получение существующего авто
    existing_car = await db.cars.get_one_or_none(car_id=new_car.car_id)
    assert existing_car is not None
    assert existing_car.car_id == new_car.car_id

    # Обновление
    update_litres = 2
    update_year = 1987
    update_color = "black"
    update_price = 400000
    update_car_data = CarCreate(
        vin="JA3BB51E9JU024751",
        engine_type="gasoline",
        litres=update_litres,
        horse_power=255,
        year=update_year,
        color=update_color,
        country="Japan",
        price=update_price,
        status="active",
    )

    updated_car = await db.cars.put_update(new_car.car_id, update_car_data)
    assert updated_car is not None
    assert updated_car.car_id == new_car.car_id
    assert updated_car.litres == update_litres
    assert updated_car.year == update_year
    assert updated_car.color == update_color
    assert updated_car.price == update_price

    # Удаление
    await db.cars.delete(car_id=existing_car.car_id)
    car = await db.cars.get_one_or_none(car_id=existing_car.car_id)
    assert car is None
