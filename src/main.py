import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend

from src.init import redis_connector

sys.path.append(str(Path(__file__).parent.parent))
import src.loggers.logger  # noqa: F401
import src.sockets.chat_handlers  # noqa: F401
from src.api.auth import router as router_auth
from src.api.cars import router as router_cars
from src.api.chat import router as router_chat
from src.api.favorites import router as router_favorites
from src.api.vrc import router as router_vrc
from src.sockets.socket_conn import sio

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        await redis_connector.connect()
        FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
        logger.info("Cache initialized with Redis backend")
    except Exception as exc:
        logger.warning("Redis unavailable, using in-memory cache: %s", exc)
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield
    await redis_connector.close()


fastapi_app = FastAPI(lifespan=lifespan)

fastapi_app.include_router(router_auth)
fastapi_app.include_router(router_cars)
fastapi_app.include_router(router_favorites)
fastapi_app.include_router(router_vrc)
fastapi_app.include_router(router_chat)


@fastapi_app.get("/demo/chat.html")
async def chat_demo_page():
    return FileResponse(
        Path(__file__).parent / "static" / "chat.html",
        headers={"Cache-Control": "no-store"},
    )


@fastapi_app.get("/demo/chat-reel.html")
async def chat_reel_page():
    return FileResponse(
        Path(__file__).parent / "static" / "chat-reel.html",
        headers={"Cache-Control": "no-store"},
    )


fastapi_app.mount("/demo", StaticFiles(directory="src/static"), name="demo")

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
