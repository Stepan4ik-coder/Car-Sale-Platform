from sqlalchemy import select

from src.exceptions import ObjectNotFoundException
from src.models.user import UsersOrm
from src.repos.base import BaseRepository
from src.schemas.user import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_by_user_email(self, email: str):
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if not user:
            raise ObjectNotFoundException()

        return user

    async def get_by_id(self, user_id: int):
        query = select(self.model).where(self.model.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if not user:
            raise ObjectNotFoundException()
        return user

    async def get_user_with_hashed_password(self, email: str):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            raise ObjectNotFoundException()

        return UserWithHashedPassword.model_validate(model)
