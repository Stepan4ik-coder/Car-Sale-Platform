from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class FavoritesOrm(Base):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.car_id"), primary_key=True)
