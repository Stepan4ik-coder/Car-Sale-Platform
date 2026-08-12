import re

from src.exceptions import IncorrectStsStringException


def clear_vin(text: str) -> str:
    vin_str = text.upper()

    vin_str = re.sub(r"[^A-Z0-9]", "", vin_str)
    vin_str = re.sub(r"I", "1", vin_str)
    vin_str = re.sub(r"O", "0", vin_str)

    if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin_str):
        raise IncorrectStsStringException()

    return vin_str


def find_vin_candidate(ocr_data: dict) -> str:
    data_list = ocr_data["text"]
    for element in data_list:
        try:
            result = clear_vin(element)
            return result

        except IncorrectStsStringException:
            continue
    raise IncorrectStsStringException()