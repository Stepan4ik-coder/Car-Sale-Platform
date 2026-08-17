from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class CarCreate(BaseModel):
    vin: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")
    engine_type: Literal["gasoline", "diesel", "electric", "hybrid"]
    litres: int = Field(ge=1, le=10)  # объём в литрах
    horse_power: int = Field(gt=0, le=2000)
    year: int = Field(ge=1900, le=2026)
    color: str = Field(min_length=1, max_length=50)
    country: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    status: Literal["active", "sold", "reserved"]


# API вернёт черновик характеристик
class CarAutofillResponse(BaseModel):
    vin: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")
    engine_type: Literal["gasoline", "diesel", "electric", "hybrid"]
    litres: int = Field(ge=1, le=10)  # объём в литрах
    horse_power: int = Field(gt=0, le=2000)
    year: int = Field(ge=1900, le=2026)
    color: str = Field(min_length=1, max_length=50)
    country: str = Field(min_length=2, max_length=100)


class CarPatch(BaseModel):
    vin: str | None = Field(
        default=None,
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$"
    )
    engine_type: Literal["gasoline", "diesel", "electric", "hybrid"] | None = None
    litres: int | None = Field(default=None, ge=1, le=10)
    horse_power: int | None = Field(default=None, gt=0, le=2000)
    year: int | None = Field(default=None, ge=1900, le=2026)
    color: str | None = Field(default=None, min_length=1, max_length=50)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    price: int | None = Field(default=None, gt=0)
    status: Literal["active", "sold", "reserved"] | None = None


class CarPut(CarCreate):
    pass


class Car(CarCreate):
    car_id: int
    price: int
    status: str

    model_config = ConfigDict(from_attributes=True)
