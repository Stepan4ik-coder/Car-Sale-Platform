from src.connectors.redis.redis_connector import RedisManager
from src.config import settings


redis_connector = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

