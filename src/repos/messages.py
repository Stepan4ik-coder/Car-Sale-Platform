from sqlalchemy import select

from src.models import MessageOrm
from src.repos.base import BaseRepository


class MessagesRepository(BaseRepository):
    model = MessageOrm

    async def sorted_by_created_at(self, chat_id):
        query = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .order_by(self.model.created_at.asc())
        )

        result = await self.session.execute(query)

        return result.scalars().all()
