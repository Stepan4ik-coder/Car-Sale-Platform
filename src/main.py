import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend


from src.init import redis_connector

sys.path.append(str(Path(__file__).parent.parent))
import src.loggers.logger # noqa: F401
from src.api.cars import router as router_cars
from src.api.auth import router as router_auth
from src.api.favorites import router as router_favorites

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


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_cars)
app.include_router(router_favorites)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
