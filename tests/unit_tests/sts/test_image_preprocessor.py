import pytest
from PIL import Image

from src.exceptions import StsFormatIsNotCorrectHTTPException, StsImageIsDamagedHTTPException
from src.services.sts.image_preprocessor import check_image, convert_to_grayscale, apply_autocontrast, resize_image, preprocess_image


@pytest.mark.parametrize(
    ("image_format", "extension"),
    [("JPEG", "jpg"), ("PNG", "png")]
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
    ("image_format", "extension"),
    [("JPEG", "jpg"), ("PNG", "png")]
)
def test_grayscale(tmp_path, image_format, extension):
    image_path = tmp_path / f"test.{extension}"
    (Image.new("RGB", (100, 100), "white")
     .save(
        image_path,
        format=image_format
    ))

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


def test_resize_image():
    image = Image.new("L", (4000, 3000), 120)
    small_image = Image.new("L", (1000, 800), 120)

    resized_image = resize_image(image)
    resized_small_image = resize_image(small_image)

    assert image.size == (4000, 3000)
    assert resized_image.size == (2500, 1875)
    assert resized_small_image.size == (1000, 800)


def test_preprocess_image(tmp_path):
    path = tmp_path / "test.png"
    image = Image.new("L", (4000, 3000), 120)
    image.putpixel((0, 0), 140)

    image.save(path, format="PNG")

    result = preprocess_image(path)

    assert result.mode == "L"
    assert result.size == (2500, 1875)
    assert result.getextrema() == (0, 255)