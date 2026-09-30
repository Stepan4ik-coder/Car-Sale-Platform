from datetime import datetime

from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    CarNotFoundHTTPException,
    ChatNotFoundHTTPException,
    ChatPermissionHTTPException,
    DontMessageWithYourselfHTTPException,
)
from src.schemas.chats import ChatCreate, ChatRequest, ChatResponse
from src.schemas.messages import MessageResponse

router = APIRouter(prefix="/chat", tags=["Чат"])


@router.post("", response_model=ChatResponse)
async def add_new_chat(data: ChatRequest, buyer_id: UserIdDep, db: DBDep):

    existing_car = await db.cars.get_one_or_none(car_id=data.car_id)
    if not existing_car:
        raise CarNotFoundHTTPException()

    if buyer_id == existing_car.owner_id:
        raise DontMessageWithYourselfHTTPException()

    existing_chat = await db.chats.get_chat_by_car_id_and_buyer_id(
        data.car_id, buyer_id
    )

    if not existing_chat:
        new_chat = ChatCreate(
            car_id=data.car_id, buyer_id=buyer_id, created_at=datetime.now()
        )
        saved_chat = await db.chats.add(new_chat)
        await db.commit()
        return saved_chat

    return existing_chat


@router.get("/{chat_id}/history", response_model=list[MessageResponse])
async def get_history(chat_id: int, user_id: UserIdDep, db: DBDep):
    existing_chat = await db.chats.get_chat_by_chat_id(chat_id)
    if not existing_chat:
        raise ChatNotFoundHTTPException()

    existing_car = await db.cars.get_one_or_none(car_id=existing_chat.car_id)
    if not existing_car:
        raise CarNotFoundHTTPException()

    if user_id != existing_car.owner_id and user_id != existing_chat.buyer_id:
        raise ChatPermissionHTTPException()

    messages = await db.messages.sorted_by_created_at(chat_id=chat_id)

    return messages
