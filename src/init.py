from src.config import settings
from src.connectors.redis.redis_connector import RedisManager

redis_connector = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
