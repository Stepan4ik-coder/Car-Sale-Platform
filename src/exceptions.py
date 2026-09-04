from fastapi import HTTPException


class CarSalesPlatformException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self):
        super().__init__(self.detail)


class ObjectNotFoundException(CarSalesPlatformException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(CarSalesPlatformException):
    detail = "Объект уже существует"


class IncorrectValuesException(CarSalesPlatformException):
    detail = "Неверные данные"


class IncorrectCreationException(CarSalesPlatformException):
    detail = "Ошибка при создании объекта"


class IncorrectStsStringException(CarSalesPlatformException):
    detail = "Невалидные данные СТС"


# HTTPException
class CarSalesPlatformHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundHTTPException(CarSalesPlatformHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class UserAlreadyExistsHTTPException(CarSalesPlatformHTTPException):
    status_code = 409
    detail = "Пользователь уже существует"


class CarAlreadyExistsHTTPException(CarSalesPlatformHTTPException):
    status_code = 409
    detail = "Автомобиль уже существует"


class CarNotFoundHTTPException(CarSalesPlatformHTTPException):
    status_code = 404
    detail = "Автомобиль не найден"


class FavoriteAlreadyExistsHTTPException(CarSalesPlatformHTTPException):
    status_code = 409
    detail = "Автомобиль уже в избранном"


class FavoriteNotFoundHTTPException(CarSalesPlatformHTTPException):
    status_code = 404
    detail = "Автомобиль в избранном не найден"


class StsFormatIsNotCorrectHTTPException(CarSalesPlatformHTTPException):
    status_code = 415
    detail = "Неподдерживаемый формат изображения"


class StsImageIsDamagedHTTPException(CarSalesPlatformHTTPException):
    status_code = 415
    detail = "Фото повреждено"


class StsImageIsNotRecognizedHTTPException(CarSalesPlatformHTTPException):
    status_code = 422
    detail = "VIN-номер не распознан"


class CarPermissionHTTPException(CarSalesPlatformHTTPException):
    status_code = 403
    detail = "Недостаточно прав доступа для управления автомобилем"