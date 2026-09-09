import redis.asyncio as redis

from app.config import settings


# Redis server URL
REDIS_URL = settings.redis_url or f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"


# Create a connection pool
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)