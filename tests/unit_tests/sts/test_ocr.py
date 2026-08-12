from src.services.sts import ocr


def test_recognize_vin(monkeypatch):
    data = [
        "СВИДЕТЕЛЬСТВО",
        "—_JHDFSi}ELTO0000000",
        "Люблю мороженое",
        "Автомашина"
    ]

    data_dict = {"text": data}


    def fake_preprocess_image(image_path):
        return "fake_image"


    def fake_recognize_data(image):
        return data_dict

    monkeypatch.setattr(ocr, "preprocess_image", fake_preprocess_image)
    monkeypatch.setattr(ocr, "recognize_data", fake_recognize_data)

    result = ocr.recognize_vin("test.jpeg")

    assert result == "JHDFS1ELT00000000"