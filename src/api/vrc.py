import os
import tempfile

from fastapi import APIRouter, UploadFile

from src.exceptions import (
    IncorrectStsStringException,
    StsImageIsNotRecognizedHTTPException,
)
from src.schemas.cars import CarAutofillResponse
from src.schemas.vrc import CarVinRequest, VrcRecognizeResponse
from src.services.autofill_example.vehicle_lookup import autofill_example
from src.services.sts.ocr import recognize_vin

router = APIRouter(
    prefix="/vrc", tags=["Действия со свидетельством о регистрации ТС (СТС)"]
)


@router.post("", response_model=VrcRecognizeResponse)
async def recognize_vrc(
    vin_file: UploadFile,
):
    vin_file_bytes = await vin_file.read()
    temp_file = tempfile.NamedTemporaryFile(prefix="vrc_", suffix=".jpg", delete=False)
    cur_path = temp_file.name
    temp_file.close()
    try:
        with open(cur_path, "wb") as new_file:
            new_file.write(vin_file_bytes)
        result = recognize_vin(cur_path)
        return {"vin": result}
    except IncorrectStsStringException:
        raise StsImageIsNotRecognizedHTTPException()

    finally:
        if os.path.exists(cur_path):
            os.remove(cur_path)


@router.post("/autofill", response_model=CarAutofillResponse)
def example_to_autofill(data: CarVinRequest):
    data_to_autofill = autofill_example(data.vin)

    return data_to_autofill
