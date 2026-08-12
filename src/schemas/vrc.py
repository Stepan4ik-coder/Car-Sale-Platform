from pydantic import BaseModel


class VrcRecognizeResponse(BaseModel):
    vin: str
