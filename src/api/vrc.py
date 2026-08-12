from fastapi import APIRouter, UploadFile
import os
import tempfile

from src.services.sts.ocr import recognize_vin
from src.exceptions import IncorrectStsStringException, StsImageIsNotRecognizedHTTPException
from src.schemas.vrc import VrcRecognizeResponse

router = APIRouter(prefix="/vrc", tags=["Действия со свидетельством о регистрации ТС (СТС)"])


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


