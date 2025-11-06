"""
Redis client for token blacklist and caching.

Manages Redis connections for the auth service.
"""

from gravity_common.redis_client import RedisClient
from app.config import settings


# Initialize Redis client
redis_client = RedisClient(
    redis_url=settings.REDIS_URL,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    decode_responses=True,
)
