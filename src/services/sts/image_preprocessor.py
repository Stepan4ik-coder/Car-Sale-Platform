from PIL import Image, UnidentifiedImageError, ImageOps

from src.services.sts.config import NEEDED_FORMATS
from src.exceptions import StsFormatIsNotCorrectHTTPException, StsImageIsDamagedHTTPException


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


def resize_image(image):
    resized_image = image.copy()
    resized_image.thumbnail((2500, 2500), Image.Resampling.LANCZOS)


    return resized_image


def preprocess_image(path):
    # Исправляем EXIF-ориентацию и переводим фото в оттенки серого.
    # Ширина и высота здесь не нужны, поэтому пропускаем их через _.
    _, _, grayscale_img = convert_to_grayscale(path)

    # Уменьшаем слишком большое фото, сохраняя его пропорции.
    resized_img = resize_image(grayscale_img)

    # Усиливаем разницу между текстом и фоном для последующего OCR.
    final_img = apply_autocontrast(resized_img)

    return final_img