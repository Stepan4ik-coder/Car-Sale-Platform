from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    car_id: int


class ChatCreate(BaseModel):
    car_id: int
    buyer_id: int
    created_at: datetime


class ChatResponse(BaseModel):
    chat_id: int
    buyer_id: int
    created_at: datetime
    car_id: int

    model_config = ConfigDict(from_attributes=True)
