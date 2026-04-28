"""Redis client for caching and real-time operations."""
import json
import redis.asyncio as redis
from typing import Optional, Any
from app.config import get_settings

settings = get_settings()

_redis_pool: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get or create Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_pool


async def set_json(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """Store JSON-serializable value in Redis."""
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=ttl or settings.redis_ttl_seconds)


async def get_json(key: str) -> Optional[Any]:
    """Retrieve and deserialize JSON value from Redis."""
    r = await get_redis()
    data = await r.get(key)
    return json.loads(data) if data else None


async def delete_key(key: str) -> None:
    """Delete a key from Redis."""
    r = await get_redis()
    await r.delete(key)


async def push_to_list(key: str, value: Any, max_length: int = 100, ttl: Optional[int] = None) -> None:
    """Push JSON-serializable value to a Redis list (left push), trim to max_length."""
    r = await get_redis()
    pipe = r.pipeline()
    pipe.lpush(key, json.dumps(value))
    pipe.ltrim(key, 0, max_length - 1)
    pipe.expire(key, ttl or settings.redis_ttl_seconds)
    await pipe.execute()


async def get_list_range(key: str, start: int = 0, end: int = -1) -> list:
    """Retrieve and deserialize a range of values from a Redis list."""
    r = await get_redis()
    data = await r.lrange(key, start, end)
    return [json.loads(item) for item in data if item]


async def add_to_sorted_set(key: str, score: float, member: str) -> None:
    """Add member to sorted set with score."""
    r = await get_redis()
    await r.zadd(key, {member: score})


async def get_sorted_set_range(key: str, start: int = 0, end: int = -1) -> list:
    """Get range from sorted set."""
    r = await get_redis()
    return await r.zrange(key, start, end, withscores=True)
