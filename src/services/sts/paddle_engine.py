from paddleocr import PaddleOCR, TextRecognition


class LazyRusPaddleOCR:
    def __init__(self, **kwargs):
        self._kwargs = kwargs # Запоминает настройки модели, переданные при создании LazyPaddleOCR
        self._ocr = None # Пока настоящей PaddleOCR-модели нет в памяти.

    @property
    def ocr(self):
        # Объект создается только при первом обращении
        if self._ocr is None:
            print("Инициализация RusPaddleOCR (загрузка моделей)...")
            self._ocr = PaddleOCR(**self._kwargs)
        return self._ocr

    def predict(self, img):
        # Вызываем через property, запуская ленивую загрузку при необходимости
        return self.ocr.predict(img)


class LazyEngPaddleOCR:
    def __init__(self, **kwargs):
        self._kwargs = kwargs # Запоминает настройки модели, переданные при создании LazyPaddleOCR
        self._ocr = None # Пока настоящей PaddleOCR-модели нет в памяти.

    @property
    def ocr(self):
        # Объект создается только при первом обращении
        if self._ocr is None:
            print("Инициализация EngPaddleOCR (загрузка моделей)...")
            self._ocr = TextRecognition(**self._kwargs)
        return self._ocr

    def predict(self, img):
        # Вызываем через property, запуская ленивую загрузку при необходимости
        return self.ocr.predict(img)


# Использование:
# При создании объекта класса модели НЕ загружаются в память
lazy_rus_reader = LazyRusPaddleOCR(
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="cyrillic_PP-OCRv5_mobile_rec"
)

lazy_eng_reader = LazyEngPaddleOCR(
    model_name="en_PP-OCRv5_mobile_rec"
)


