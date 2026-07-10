import redis.asyncio as redis
import logging

class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        try:
            logging.info(f'Начало подключения к Redis. Host: {self.host}. Port: {self.port}.')
            self.redis = await redis.Redis(host=self.host)
            logging.info(f'Успешно подключены к Redis. Host: {self.host}. Port: {self.port}.')
        except ConnectionError:
            raise TimeoutError("Время ожидания подключения истекло.")


    async def set(self, key: str, value: str, expire: int):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)


    async def get(self, key: str):
        return await self.redis.get(key)


    async def delete(self, key: str):
        return await self.redis.delete(key)


    async def close(self):
        return await self.redis.close()
