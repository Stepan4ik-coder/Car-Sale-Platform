import cv2
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from src.exceptions import (
    StsFormatIsNotCorrectHTTPException,
    StsImageIsDamagedHTTPException,
)
from src.services.sts.config import NEEDED_FORMATS


def check_format_in_needed_formats(image_format):
    if image_format not in NEEDED_FORMATS:
        raise StsFormatIsNotCorrectHTTPException()


def _open_and_validate(image_path):
    try:
        with Image.open(image_path) as image:
            image.load()
            image_format = image.format
            image = ImageOps.exif_transpose(image)
            img_copy = image.copy()

            check_format_in_needed_formats(image_format)

            return img_copy, image_format

    except (UnidentifiedImageError, OSError) as error:
        raise StsImageIsDamagedHTTPException() from error


def check_image(image_path):
    image, image_format = _open_and_validate(image_path)
    width, height = image.size

    return width, height, image_format


def convert_to_grayscale(image_path):
    image, _ = _open_and_validate(image_path)
    width, height = image.size
    grayscale_image = image.convert("L")

    return width, height, grayscale_image


def apply_autocontrast(image):
    new_image = ImageOps.autocontrast(image)

    return new_image


def process_of_binarization(crop_vin):
    final_image = preprocess_vin_image(crop_vin)

    from_img_to_numpy = np.array(final_image)
    # Порог (0) игнорируется, алгоритм сам вычислит нужный
    _, binary_array = cv2.threshold(
        from_img_to_numpy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    from_numpy_to_img = Image.fromarray(binary_array)

    return from_numpy_to_img


def resize_image_to_small(image):
    resized_image = image.copy()
    resized_image.thumbnail((2500, 2500), Image.Resampling.LANCZOS)

    return resized_image


def resize_image_to_big(image):
    resized_image = image.copy()
    if resized_image.width < 1600:
        coefficient = 1600 / resized_image.width
        new_height = round(resized_image.height * coefficient)
        new_resized_image = resized_image.resize(
            (1600, new_height), Image.Resampling.LANCZOS
        )
        return new_resized_image
    else:
        return resized_image


def preprocess_vin_image(image):
    resized_vin_image = image.convert("L")
    bigger_resized_vin_image = resize_image_to_big(resized_vin_image)
    final_img = apply_autocontrast(bigger_resized_vin_image)

    return final_img


def preprocess_image(path):
    # Исправляем EXIF-ориентацию и переводим фото в оттенки серого.
    # Ширина и высота здесь не нужны, поэтому пропускаем их через _.
    _, _, grayscale_img = convert_to_grayscale(path)

    # Уменьшаем слишком большое фото, сохраняя его пропорции.
    resized_img = resize_image_to_small(grayscale_img)

    # Усиливаем разницу между текстом и фоном для последующего OCR.
    final_img = apply_autocontrast(resized_img)

    return final_img


# Вырезаем подпись VIN по координатам
def crop_vin_label(image, vin_coordinates):
    left, top, width, height = vin_coordinates

    crop_left = left
    crop_top = top
    crop_right = left + width
    crop_bottom = top + height

    vin_region = image.crop((crop_left, crop_top, crop_right, crop_bottom))

    return vin_region


def crop_vin_line(
    image,
    vin_coordinates,
    left_padding=380,
    right_padding=0,
    top_offset=10,
    bottom_padding=40,
):

    left, top, width, height = vin_coordinates

    image_width, image_height = image.size
    crop_left = left - left_padding
    crop_top = top + height + top_offset
    crop_right = left + width + right_padding
    crop_bottom = top + height + bottom_padding

    new_coordinates = [
        max(0, crop_left),
        max(0, crop_top),
        min(image_width, crop_right),
        min(image_height, crop_bottom),
    ]

    cropped_image = image.crop(new_coordinates)

    return cropped_image
