from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestCreate(BaseModel):  # идет в API
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)  # Сырой пароль
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    phone_number: str = Field(pattern=r"^\+?\d{10,15}$")


class UserCreate(BaseModel):  # идет в БД
    email: EmailStr
    password: str  # Хэш - пароль
    first_name: str
    last_name: str
    phone_number: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str  # Сырой пароль
