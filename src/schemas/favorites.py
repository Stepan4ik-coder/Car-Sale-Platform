from pydantic import BaseModel


class AddFavorite(BaseModel):
    car_id: int


class CreateFavorite(BaseModel):
    car_id: int
    user_id: int
