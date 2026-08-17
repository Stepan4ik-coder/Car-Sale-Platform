from pydantic import BaseModel, Field


# API вернуло VIN после фото СТС
class VrcRecognizeResponse(BaseModel):
    vin: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")


# Клиент прислал VIN для автозаполнения
class CarVinRequest(VrcRecognizeResponse):
    pass
