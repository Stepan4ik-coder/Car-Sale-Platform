from sqlalchemy import select

from src.models import ChatOrm
from src.repos.base import BaseRepository


class ChatsRepository(BaseRepository):
    model = ChatOrm

    async def get_chat_by_chat_id(self, chat_id):
        chat_string = select(self.model).where(self.model.chat_id == chat_id)

        result = await self.session.execute(chat_string)

        return result.scalars().one_or_none()

    async def get_chat_by_car_id_and_buyer_id(self, car_id, buyer_id):
        chat_by_ids = select(self.model).where(
            self.model.car_id == car_id, self.model.buyer_id == buyer_id
        )

        result = await self.session.execute(chat_by_ids)

        return result.scalars().one_or_none()
