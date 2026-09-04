from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import Base


class CarsOrm(Base):
    __tablename__ = "cars"

    vin: Mapped[str] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    car_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    engine_type: Mapped[str] = mapped_column(String(100))
    litres: Mapped[int] = mapped_column()
    horse_power: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    color: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(30))
