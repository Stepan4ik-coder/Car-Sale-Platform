from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    CarNotFoundHTTPException,
    FavoriteAlreadyExistsHTTPException,
    FavoriteNotFoundHTTPException,
)
from src.schemas.favorites import AddFavorite, CreateFavorite

router = APIRouter(
    prefix="/favorites",
    tags=[
        "Действия с избранными автомобилями."
        "\nДоступны только аутентифицированным пользователям"
    ],
)


@router.get("")
async def get_all_fav_cars(db: DBDep, user_id: UserIdDep):
    response = await db.favorites.get_all_favorite_cars(user_id)

    return response


@router.post("")
async def add_new_fav_cars(db: DBDep, user_id: UserIdDep, data: AddFavorite):
    car = await db.cars.get_one_or_none(car_id=data.car_id)
    if not car:
        raise CarNotFoundHTTPException()

    existing_favorite = await db.favorites.get_favorite(
        user_id=user_id, car_id=data.car_id
    )
    if existing_favorite:
        raise FavoriteAlreadyExistsHTTPException()

    add_stmt = CreateFavorite(car_id=data.car_id, user_id=user_id)
    result = await db.favorites.add(add_stmt)
    await db.commit()

    return result


@router.delete("/{car_id}")
async def delete_fav_cars(db: DBDep, user_id: UserIdDep, car_id: int):
    fav_to_del = await db.favorites.get_favorite(car_id=car_id, user_id=user_id)
    if not fav_to_del:
        raise FavoriteNotFoundHTTPException()

    await db.favorites.delete(user_id=user_id, car_id=car_id)
    await db.commit()
