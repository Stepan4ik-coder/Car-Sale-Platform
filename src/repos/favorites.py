from sqlalchemy import select

from src.models.cars import CarsOrm
from src.models.favorites import FavoritesOrm
from src.models.user import UsersOrm
from src.repos.base import BaseRepository


class FavoritesRepository(BaseRepository):
    model = FavoritesOrm

    async def get_all_favorite_cars(self, user_id: int):
        fav_strings = select(self.model).where(
            self.model.user_id == user_id
        )  # строки из favorites
        result = await self.session.execute(fav_strings)

        fav_rows = result.scalars().all()
        cars_ids = [row.car_id for row in fav_rows]

        cars = select(CarsOrm).where(CarsOrm.car_id.in_(cars_ids))
        total_result = await self.session.execute(cars)

        return total_result.scalars().all()

    async def get_favorite(self, user_id: int, car_id: int):
        query = select(self.model).where(
            self.model.user_id == user_id,
            self.model.car_id == car_id,
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def get_users_by_car_id(self, car_id: int):
        fav_strings = select(self.model).where(
            self.model.car_id == car_id
        )  # строки из favorites
        result = await self.session.execute(fav_strings)

        fav_rows = result.scalars().all()
        users_ids = [row.user_id for row in fav_rows]
        if not users_ids:
            return []

        users = select(UsersOrm).where(UsersOrm.id.in_(users_ids))
        total_result = await self.session.execute(users)

        return total_result.scalars().all()
