from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import CarNotFoundHTTPException
from src.schemas.cars import CarCreate, CarPut, CarPatch
from src.services.send_notifications import check_car_price, check_car_status
from src.tasks.tasks_for_celery import send_notifications


router = APIRouter(prefix="/cars", tags=["Действия с автомобилями на платформе"])


@router.get("")
@cache(expire=30)
async def get_cars(
    db: DBDep,
    engine_type=None,
    litres=None,
    horse_power=None,
    year=None,
    color=None,
    country=None,
):

    return await db.cars.get_filtered(
        engine_type, litres, horse_power, year, color, country
    )


@router.get("/{car_id}")
async def get_one_car(db: DBDep, car_id: int):
    car = await db.cars.get_one_or_none(car_id)
    if car is None:
        raise CarNotFoundHTTPException()
    return car



@router.post("")
async def add(db: DBDep, data: CarCreate):
    car = await db.cars.add(data)
    await db.commit()

    return car


@router.put("/{car_id}")
async def put_update(db: DBDep, data: CarPut, car_id: int):
    car = await db.cars.get_one_or_none(car_id)
    if car is None:
        raise CarNotFoundHTTPException()

    car = await db.cars.put_update(car_id, data)
    await db.commit()

    return car


@router.patch("/{car_id}")
async def patch_update(db: DBDep, data: CarPatch, car_id: int):
    old_car = await db.cars.get_one_or_none(car_id)
    if old_car is None:
        raise CarNotFoundHTTPException()

    car = await db.cars.patch_update(car_id, data)

    await db.commit()
    check_car_price(old_car, car, car_id)
    check_car_status(old_car, car, car_id)

    return car


@router.delete("/{car_id}")
async def delete(db: DBDep, car_id: int):

    car_to_delete = await db.cars.get_one_or_none(car_id)
    if car_to_delete is None:
        raise CarNotFoundHTTPException()

    await db.cars.delete(car_id=car_id)
    await db.commit()

    send_notifications.delay(
        car_id=car_id, status=car_to_delete.status, price=car_to_delete.price
    )

    return {"status": "OK"}
