import pytesseract

from src.services.sts.image_preprocessor import preprocess_image
from src.services.sts.vin_parser import find_vin_candidate


def recognize_sts(image_path) -> str:
    # Подготавливаем фотографию СТС и передаём её в Tesseract.
    processed_image = preprocess_image(image_path)
    text = recognize_text(processed_image)

    return text


def recognize_text(processed_image) -> str:
    text = pytesseract.image_to_string(
        processed_image,
        lang="rus+eng"
    )

    return text.strip()


def recognize_data(image):
    # Получаем не только текст, но и confidence и координаты каждого фрагмента.
    # Output.DICT возвращает эти данные в виде удобного Python-словаря.
    data = pytesseract.image_to_data(
        image,
        lang="rus+eng",
        output_type=pytesseract.Output.DICT
    )

    return data


def recognize_vin(image_path) -> str:
    image = preprocess_image(image_path)
    ocr_dict = recognize_data(image)
    vin = find_vin_candidate(ocr_dict)

    return vin