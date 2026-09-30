from fastapi import APIRouter, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    ObjectNotFoundException,
    UserAlreadyExistsHTTPException,
    UserNotFoundHTTPException,
)
from src.schemas.user import User, UserCreate, UserLogin, UserRequestCreate
from src.services.auth.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register(db: DBDep, data: UserRequestCreate):
    try:
        new_user_info = UserCreate(
            email=data.email,
            password=AuthService().hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
        )

        await db.users.add(new_user_info)
        await db.commit()

    except IntegrityError:
        await db.session.rollback()
        raise UserAlreadyExistsHTTPException()
    return {"status": "OK"}


@router.post("/login")
async def login(db: DBDep, data: UserLogin, response: Response):
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException()

    if not AuthService().verify_password(data.password, user.password):
        raise UserNotFoundHTTPException()

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.get("/get_me", response_model=User)
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        user = await db.users.get_by_id(user_id)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException()

    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")

    return {"status": "OK"}
