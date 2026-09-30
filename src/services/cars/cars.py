from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import CarNotFoundHTTPException, CarPermissionHTTPException


async def getting_existing_car(db: DBDep, car_id: int, owner_id: UserIdDep):
    car = await db.cars.get_one_or_none(car_id=car_id)
    if car is None:
        raise CarNotFoundHTTPException()

    if car.owner_id != owner_id:
        raise CarPermissionHTTPException()

    return car
