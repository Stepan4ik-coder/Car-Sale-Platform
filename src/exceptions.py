from fastapi import HTTPException


class CarSalesPlatformException(Exception):
    def __init__(self, *args, **kwargs):
        detail = "Неожиданная ошибка"

        super().__init__(*args, detail, **kwargs)


class ObjectNotFoundException(CarSalesPlatformException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(CarSalesPlatformException):
    detail = "Объект уже существует"


class IncorrectValuesException(CarSalesPlatformException):
    detail = "Неверные данные"



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