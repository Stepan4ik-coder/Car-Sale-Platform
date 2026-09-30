from http.cookies import SimpleCookie

import socketio
from socketio.exceptions import ConnectionRefusedError

from src.exceptions import AccessTokenDamagedException, AccessTokenExpiredException
from src.services.auth.auth import AuthService

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event()
async def connect(sid, environ, auth):
    cookies = environ.get("HTTP_COOKIE")
    if not cookies:
        raise ConnectionRefusedError()
    object_ = SimpleCookie(cookies)

    access_token = object_.get("access_token")  # Получение чистого JWT
    if not access_token:
        raise ConnectionRefusedError()

    try:
        decoded = AuthService().decode_token(access_token.value)
    except (AccessTokenDamagedException, AccessTokenExpiredException):
        raise ConnectionRefusedError()

    user_id = decoded["user_id"]
    await sio.save_session(sid, {"user_id": user_id})


@sio.event()
async def disconnect(sid):
    session = await sio.get_session(sid)
    room = session.get("room")

    if room is not None:
        await sio.leave_room(sid, room)
