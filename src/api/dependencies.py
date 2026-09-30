from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import (
    AccessTokenDamagedException,
    AccessTokenDamagedHTTPException,
    AccessTokenExpiredException,
    AccessTokenExpiredHTTPException,
    AccessTokenNotProvidedHTTPException,
)
from src.services.auth.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=24)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise AccessTokenNotProvidedHTTPException()

    return access_token


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
        return data["user_id"]

    except AccessTokenExpiredException:
        raise AccessTokenExpiredHTTPException()

    except AccessTokenDamagedException:
        raise AccessTokenDamagedHTTPException()


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
