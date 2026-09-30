from src.database import async_session_maker
from src.exceptions import ObjectNotFoundException
from src.utils.db_manager import DBManager


async def getting_car_and_chat(chat_id):
    async with DBManager(session_factory=async_session_maker) as db:
        chat = await db.chats.get_chat_by_chat_id(chat_id)
        if chat is None:
            raise ObjectNotFoundException()

        car = await db.cars.get_one_or_none(car_id=chat.car_id)
        if car is None:
            raise ObjectNotFoundException()

    return car, chat
