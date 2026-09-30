from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models.cars import CarsOrm
from src.repos.base import BaseRepository


class CarsRepository(BaseRepository):
    model = CarsOrm

    async def get_filtered(
        self,
        engine_type=None,
        litres=None,
        horse_power=None,
        year=None,
        color=None,
        country=None,
    ):

        query = select(self.model)
        if engine_type is not None:
            query = query.where(self.model.engine_type == engine_type)

        if litres is not None:
            query = query.where(self.model.litres == litres)

        if horse_power is not None:
            query = query.where(self.model.horse_power == horse_power)

        if year is not None:
            query = query.where(self.model.year == year)

        if color is not None:
            query = query.where(self.model.color == color)

        if country is not None:
            query = query.where(self.model.country == country)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def add(self, data: BaseModel, owner_id: int | None = None):
        new_car_data = data.model_dump()
        new_car_data["owner_id"] = owner_id

        add_stmt = insert(self.model).values(new_car_data).returning(self.model)
        result = await self.session.execute(add_stmt)

        return result.scalars().one()
