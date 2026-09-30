from datetime import datetime

from pydantic import ValidationError

from src.database import async_session_maker
from src.exceptions import IncorrectCreationException, PermissionException
from src.schemas.messages import MessageCreate, MessageRequest
from src.sockets.chat_service import getting_car_and_chat
from src.sockets.socket_conn import sio
from src.utils.db_manager import DBManager


@sio.on("join_room")
async def handle_join_room(sid, data):
    session = await sio.get_session(sid)
    user_id = session["user_id"]
    chat_id = data["chat_id"]

    car, chat = await getting_car_and_chat(chat_id)

    buyer_id = chat.buyer_id
    owner_id = car.owner_id

    if user_id == buyer_id or user_id == owner_id:
        await sio.enter_room(sid, f"chat:{chat_id}")
        await sio.save_session(sid, {"user_id": user_id, "room": f"chat:{chat_id}"})
    else:
        raise PermissionException()


@sio.on("send_message")
async def handle_message(sid, data: dict):
    session = await sio.get_session(sid)
    user_id = session["user_id"]

    try:
        validated_message = MessageRequest.model_validate(data)
        chat_id = validated_message.chat_id
        text = validated_message.text

    except ValidationError:
        raise IncorrectCreationException()

    car, chat = await getting_car_and_chat(chat_id)

    buyer_id = chat.buyer_id
    owner_id = car.owner_id

    if user_id != buyer_id and user_id != owner_id:
        raise PermissionException()

    new_message = MessageCreate(
        author_id=user_id, created_at=datetime.now(), text=text, chat_id=chat_id
    )

    async with DBManager(session_factory=async_session_maker) as db:
        saved_message = await db.messages.add(new_message)
        await db.commit()

    await sio.emit(
        "new_message",
        {
            "message_id": saved_message.message_id,
            "text": saved_message.text,
            "author_id": saved_message.author_id,
            "created_at": saved_message.created_at.isoformat(),
        },
        to=f"chat:{chat_id}",
    )
