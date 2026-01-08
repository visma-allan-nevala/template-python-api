"""
Redis Client for Caching.

Provides async Redis connection and common cache operations.

Usage
-----
In route handlers with dependency injection::

    from src.storage.redis_client import get_redis

    @router.get("/cached-data")
    async def get_cached(redis: Redis = Depends(get_redis)):
        cached = await redis.get("my-key")
        if cached:
            return json.loads(cached)
        # ... fetch data, then cache it
        await redis.set("my-key", json.dumps(data), ex=300)
        return data

In services or background tasks::

    from src.storage.redis_client import get_redis_client

    async def some_function():
        redis = await get_redis_client()
        await redis.set("key", "value", ex=60)

Configuration
-------------
Redis settings are loaded from environment variables:
- REDIS_HOST
- REDIS_PORT
- REDIS_DB
- REDIS_PASSWORD (optional)

Common Operations
-----------------
- get/set: Simple key-value storage
- hget/hset: Hash maps
- lpush/rpush/lrange: Lists
- sadd/smembers: Sets
- setex: Set with expiration
- incr/decr: Atomic counters
- expire: Set TTL on existing key
"""

from collections.abc import AsyncGenerator
from typing import Any

# Note: redis package is an optional dependency
# Install with: uv sync --extra redis
try:
    from redis.asyncio import Redis, from_url
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = Any  # type: ignore[assignment,misc]

from src.core.config import settings

# Global Redis client
_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    """
    Get or create the Redis client.

    Returns
    -------
    Redis
        Async Redis client instance

    Raises
    ------
    ImportError
        If redis package is not installed
    RuntimeError
        If Redis connection fails
    """
    global _redis_client

    if not REDIS_AVAILABLE:
        raise ImportError(
            "Redis package not installed. Install with: uv sync --extra redis"
        )

    if _redis_client is None:
        _redis_client = await from_url(
            settings.redis.url,
            encoding="utf-8",
            decode_responses=True,
        )

    return _redis_client


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Dependency for getting Redis client in route handlers.

    Yields
    ------
    Redis
        Redis client instance

    Example
    -------
    ::

        @router.get("/cached")
        async def get_cached(redis: Redis = Depends(get_redis)):
            return await redis.get("key")
    """
    client = await get_redis_client()
    yield client


async def init_redis() -> None:
    """
    Initialize Redis connection.

    Call this during application startup to verify connectivity.
    """
    if not REDIS_AVAILABLE:
        return

    client = await get_redis_client()
    await client.ping()


async def close_redis() -> None:
    """
    Close Redis connection.

    Call this during application shutdown to cleanly close connection.
    """
    global _redis_client

    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None


# =============================================================================
# Cache Helpers
# =============================================================================


async def cache_get(key: str) -> str | None:
    """
    Get value from cache.

    Parameters
    ----------
    key : str
        Cache key

    Returns
    -------
    str | None
        Cached value or None if not found
    """
    client = await get_redis_client()
    return await client.get(key)


async def cache_set(
    key: str,
    value: str,
    ttl_seconds: int = 300,
) -> None:
    """
    Set value in cache with TTL.

    Parameters
    ----------
    key : str
        Cache key
    value : str
        Value to cache (use json.dumps for complex objects)
    ttl_seconds : int
        Time-to-live in seconds (default: 5 minutes)
    """
    client = await get_redis_client()
    await client.set(key, value, ex=ttl_seconds)


async def cache_delete(key: str) -> None:
    """
    Delete value from cache.

    Parameters
    ----------
    key : str
        Cache key to delete
    """
    client = await get_redis_client()
    await client.delete(key)


async def cache_get_or_set(
    key: str,
    factory: Any,
    ttl_seconds: int = 300,
) -> str:
    """
    Get from cache or compute and cache.

    Parameters
    ----------
    key : str
        Cache key
    factory : Callable
        Async function to compute value if not cached
    ttl_seconds : int
        Time-to-live in seconds

    Returns
    -------
    str
        Cached or computed value

    Example
    -------
    ::

        async def fetch_expensive_data():
            # ... expensive computation
            return json.dumps(data)

        result = await cache_get_or_set("my-key", fetch_expensive_data, ttl_seconds=600)
    """
    client = await get_redis_client()

    # Try cache first
    cached = await client.get(key)
    if cached is not None:
        return cached

    # Compute value
    value = await factory()

    # Cache and return
    await client.set(key, value, ex=ttl_seconds)
    return value
