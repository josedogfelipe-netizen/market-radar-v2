import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisClient:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

    async def ping(self):
        try:
            return await self.redis.ping()
        except Exception:
            return False

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value, ex=None):
        return await self.redis.set(key, value, ex=ex)
    
    async def publish(self, channel, message):
        return await self.redis.publish(channel, message)

redis_client = RedisClient()
