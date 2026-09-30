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


class AccessTokenExpiredException(CarSalesPlatformException):
    detail = "Токен доступа просрочен"


class AccessTokenDamagedException(CarSalesPlatformException):
    detail = "Токен доступа повреждён"


class PermissionException(CarSalesPlatformException):
    detail = "Недостаточно прав доступа"


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


class DontMessageWithYourselfHTTPException(CarSalesPlatformHTTPException):
    status_code = 409
    detail = "Нельзя писать самому себе"


class CarAlreadyExistsHTTPException(CarSalesPlatformHTTPException):
    status_code = 409
    detail = "Автомобиль уже существует"


class CarNotFoundHTTPException(CarSalesPlatformHTTPException):
    status_code = 404
    detail = "Автомобиль не найден"


class ChatNotFoundHTTPException(CarSalesPlatformHTTPException):
    status_code = 404
    detail = "Чат не найден"


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


class ChatPermissionHTTPException(CarSalesPlatformHTTPException):
    status_code = 403
    detail = "Недостаточно прав доступа для вхождения в чат"


class AccessTokenExpiredHTTPException(CarSalesPlatformHTTPException):
    detail = "Токен доступа просрочен"
    status_code = 401


class AccessTokenDamagedHTTPException(CarSalesPlatformHTTPException):
    detail = "Токен доступа повреждён"
    status_code = 401


class AccessTokenNotProvidedHTTPException(CarSalesPlatformHTTPException):
    detail = "Токен доступа не предоставлен"
    status_code = 401
