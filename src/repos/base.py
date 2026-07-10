from sqlalchemy import select, delete, insert, update
from pydantic import BaseModel



class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()


    async def get_one_or_none(self, car_id, **filter_by):
        query = select(self.model).filter_by(**filter_by, car_id=car_id)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()


    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)

        return result.scalars().one()


    async def put_update(self, car_id, data: BaseModel):
        full_update_stmt = (
            update(self.model)
            .filter_by(car_id=car_id)
            .values(data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(full_update_stmt)

        return result.scalars().one()


    async def patch_update(self, car_id, data: BaseModel):
        partially_update_stmt = (
            update(self.model)
            .filter_by(car_id=car_id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(partially_update_stmt)

        return result.scalars().one()


    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

        return {"status": "OK"}
