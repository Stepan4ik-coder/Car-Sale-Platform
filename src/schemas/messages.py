from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    chat_id: int
    text: str
    author_id: int
    created_at: datetime


class MessageRequest(BaseModel):
    chat_id: int
    text: str


class MessageResponse(BaseModel):
    chat_id: int
    message_id: int
    text: str
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
