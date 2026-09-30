import pytest
from PIL import Image

from src.exceptions import (
    StsFormatIsNotCorrectHTTPException,
    StsImageIsDamagedHTTPException,
)
from src.services.sts.image_preprocessor import (
    apply_autocontrast,
    check_image,
    convert_to_grayscale,
    crop_vin_label,
    crop_vin_line,
    preprocess_image,
    preprocess_vin_image,
    resize_image_to_big,
    resize_image_to_small,
)


@pytest.mark.parametrize(
    ("image_format", "extension"), [("JPEG", "jpg"), ("PNG", "png")]
)
def test_jpeg_and_png_format(tmp_path, image_format, extension):
    image_path = tmp_path / f"test.{extension}"
    Image.new("RGB", (100, 100), "white").save(image_path, format=image_format)
    width, height, current_format = check_image(image_path)

    assert width == 100
    assert height == 100
    assert current_format == image_format


def test_gif_format(tmp_path):
    image_path = tmp_path / "test.gif"
    Image.new("RGB", (100, 100), "white").save(image_path, format="GIF")

    with pytest.raises(StsFormatIsNotCorrectHTTPException) as ex:
        preprocess_image(image_path)

    assert ex.value.status_code == 415


def test_damaged_image(tmp_path):
    image_path = tmp_path / "test.jpg"
    image_path.write_bytes(b"This is not an image")

    with pytest.raises(StsImageIsDamagedHTTPException) as ex:
        preprocess_image(image_path)

    assert ex.value.status_code == 415


@pytest.mark.parametrize(
    ("image_format", "extension"), [("JPEG", "jpg"), ("PNG", "png")]
)
def test_grayscale(tmp_path, image_format, extension):
    image_path = tmp_path / f"test.{extension}"
    (Image.new("RGB", (100, 100), "white").save(image_path, format=image_format))

    width, height, grayscale_image = convert_to_grayscale(image_path)

    assert width == 100
    assert height == 100
    assert grayscale_image.mode == "L"
    assert grayscale_image.size == (100, 100)


def test_exif_transpose(tmp_path):
    image_path = tmp_path / "test.jpg"

    image = Image.new("RGB", (120, 80), "white")

    image_exif = image.getexif()
    image_exif[274] = 6
    image.save(image_path, format="JPEG", exif=image_exif)

    width, height, grayscale_image = convert_to_grayscale(image_path)

    assert width == 80
    assert height == 120
    assert grayscale_image.mode == "L"
    assert grayscale_image.size == (80, 120)


def test_apply_autocontrast():
    image = Image.new("L", (120, 140), 120)

    image.putpixel((119, 139), 140)
    new_image = apply_autocontrast(image)
    new_image_contrast = new_image.getextrema()

    assert new_image_contrast == (0, 255)


def test_resize_image_to_small():
    image = Image.new("L", (4000, 3000), 120)
    small_image = Image.new("L", (1000, 800), 120)

    resized_image = resize_image_to_small(image)
    resized_small_image = resize_image_to_small(
        small_image
    )  # проверяется, нужно ли уменьшать маленькое изображение

    assert image.size == (4000, 3000)
    assert resized_image.size == (2500, 1875)
    assert resized_small_image.size == (1000, 800)


def test_resize_image_to_big():
    image = Image.new("L", (282, 34), 120)
    big_image = Image.new("L", (1600, 193))

    resized_image = resize_image_to_big(image)
    resized_big_image = resize_image_to_big(
        big_image
    )  # проверяется, нужно ли увеличивать больше изображение

    assert image.size == (282, 34)
    assert resized_image.size == (1600, 193)
    assert resized_big_image.size == (1600, 193)


def test_preprocess_vin_image():
    new_img = Image.new("RGB", (282, 34), "white")
    result = preprocess_vin_image(new_img)

    assert new_img.size == (282, 34)
    assert new_img.mode == "RGB"
    assert result.size == (1600, 193)
    assert result.mode == "L"


def test_preprocess_image(tmp_path):
    path = tmp_path / "test.png"
    image = Image.new("L", (4000, 3000), 120)
    image.putpixel((0, 0), 140)

    image.save(path, format="PNG")

    result = preprocess_image(path)

    assert result.mode == "L"
    assert result.size == (2500, 1875)
    assert result.getextrema() == (0, 255)


def test_crop_vin_label():
    new_img = Image.new("RGB", (200, 300), "white")
    new_img.putpixel((100, 200), (0, 0, 0))

    left, top, width, height = 100, 200, 60, 25
    result = crop_vin_label(new_img, (left, top, width, height))

    assert result.size == (60, 25)
    assert result.getpixel((0, 0)) == (0, 0, 0)


def test_crop_vin_line():
    new_img = Image.new("RGB", (200, 300), "white")
    left, top, width, height = 100, 200, 60, 25

    result = crop_vin_line(
        new_img,
        (left, top, width, height),
        left_padding=320,
        right_padding=0,
        top_offset=10,
        bottom_padding=50,
    )

    assert result.size == (160, 40)
