import numpy as np
import pytesseract

from src.exceptions import IncorrectStsStringException
from src.services.sts.image_preprocessor import preprocess_image, crop_vin_line, preprocess_vin_image
from src.services.sts.vin_parser import clear_vin
from src.services.sts.paddle_engine import lazy_rus_reader, lazy_eng_reader




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


def recognize_data(image, config=""):
    # Получаем не только текст, но и confidence и координаты каждого фрагмента.
    # Output.DICT возвращает эти данные в виде удобного Python-словаря.
    data = pytesseract.image_to_data(
        image,
        lang="rus+eng",
        config=config,
        output_type=pytesseract.Output.DICT
    )

    return data


def recognize_paddle_data(image, reader):
    results = reader.predict(np.array(image.convert("RGB")))

    texts = []
    lefts = []
    tops = []
    widths = []
    heights = []

    for result in results:
        rec_texts = result["rec_texts"]
        rec_scores = result["rec_scores"]
        rec_boxes = result["rec_boxes"]

        for index, text in enumerate(rec_texts):
            score = rec_scores[index]
            box = rec_boxes[index]
            left, top, right, bottom = box

            width = right - left
            height = bottom - top

            texts.append(text)
            lefts.append(left)
            tops.append(top)
            widths.append(width)
            heights.append(height)


    return {
        "text": texts,
        "left": lefts,
        "top": tops,
        "width": widths,
        "height": heights
    }


def recognize_vin(image_path) -> str:
    image = preprocess_image(image_path)
    ocr_dict = recognize_paddle_data(image, lazy_rus_reader)
    vin_coordinates = find_vin_label(ocr_dict)

    try:
        vin_crop = crop_vin_line(image, vin_coordinates)
    except TypeError:
        raise IncorrectStsStringException()

    prepared_vin_crop = preprocess_vin_image(vin_crop)
    vin = read_vin_crop(prepared_vin_crop)

    return vin


def recognize_vin_line(image):
    vin_text = pytesseract.image_to_string(
        image,
        lang="eng",
        config=(
            "--psm 7 "
            "-c tessedit_char_whitelist=ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    ))

    return vin_text.strip()


def read_vin_crop(vin_crop):
    vin_crop_to_rgb = vin_crop.convert("RGB")
    rgb_vin_crop_to_array = np.array(vin_crop_to_rgb)
    english_model = lazy_eng_reader.predict(rgb_vin_crop_to_array)
    first_result = english_model[0]
    vin_string = first_result["rec_text"]

    result = clear_vin(vin_string)

    return result


def find_vin_label(ocr_data: dict):
    text_value = ocr_data["text"]

    for index, text in enumerate(text_value):
        if "VIN" in text.upper():
            left = ocr_data["left"][index]
            top = ocr_data["top"][index]
            width = ocr_data["width"][index]
            height = ocr_data["height"][index]

            return left, top, width, height