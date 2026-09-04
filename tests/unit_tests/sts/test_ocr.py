from PIL import Image


from src.services.sts import ocr
from src.services.sts.ocr import find_vin_label
from src.services.sts.paddle_engine import lazy_rus_reader


def test_recognize_vin(monkeypatch):
    data = [
        "СВИДЕТЕЛЬСТВО",
        "—_JHDFSi}ELTO0000000",
        "Люблю мороженое",
        "Автомашина"
    ]

    data_dict = {"text": data}


    def fake_preprocess_image(path):
        return "fake_image"


    def fake_recognize_paddle_data(image, config=""):
        return data_dict


    def fake_find_vin_label(ocr_data):
        vin_coordinates = (100, 200, 60, 25)
        return vin_coordinates


    def fake_crop_vin_line(image, vin_coordinates):
        return "fake_crop"

    def fake_preprocess_vin_image(image):
        return "fake_prepared_crop"


    monkeypatch.setattr(ocr, "preprocess_image", fake_preprocess_image)
    monkeypatch.setattr(ocr, "recognize_paddle_data", fake_recognize_paddle_data)
    monkeypatch.setattr(ocr, "find_vin_label", fake_find_vin_label)
    monkeypatch.setattr(ocr, "crop_vin_line", fake_crop_vin_line)
    monkeypatch.setattr(ocr, "preprocess_vin_image", fake_preprocess_vin_image)


    result = ocr.recognize_vin("test.jpeg")

    assert result == "JHDFS1ELT00000000"


def test_recognize_vin_line(monkeypatch):
    called_with = {}

    def fake_image_to_string(image, lang, config):
        called_with["lang"] = lang
        called_with["config"] = config

        return "JHDFS1ELT00000000\n"

    monkeypatch.setattr(ocr.pytesseract, "image_to_string", fake_image_to_string)

    ocr.recognize_vin_line("fake")



    assert called_with["lang"] == "eng"
    assert "--psm 7" in called_with["config"]
    assert "tessedit_char_whitelist" in called_with["config"]


def test_find_vin_label():
    ocr_data = {
        "text": ["СВИДЕТЕЛЬСТВО", "(VIN)", "МАРКА"],
        "left": [10, 100, 20],
        "top": [20, 200, 30],
        "width": [50, 60, 70],
        "height": [15, 25, 35]
    }

    result = find_vin_label(ocr_data)

    assert result == (100, 200, 60, 25)


def test_recognize_paddle_data(monkeypatch):
    captured = dict()
    image = Image.new("L", (100, 100), "white")

    def fake_predict(image_array):
        captured["shape"] = image_array.shape

        return [
            {
                "rec_texts": ["Регистрационный знак", "VIN"],
                "rec_scores": [0.90, 0.85],
                "rec_boxes": [
                    [10, 20, 60, 70],
                    [20, 45, 65, 89]
                ]
            }
        ]

    monkeypatch.setattr(ocr.lazy_rus_reader, "predict", fake_predict)
    result = ocr.recognize_paddle_data(image, reader=lazy_rus_reader)

    assert image.mode == "L"
    assert captured["shape"] == (100, 100, 3)

    assert result["text"] == ["Регистрационный знак", "VIN"]
    assert result["left"] == [10, 20]
    assert result["top"] == [20, 45]
    assert result["width"] == [50, 45]
    assert result["height"] == [50 , 44]

