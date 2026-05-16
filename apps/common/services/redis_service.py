"""
Redis service for caching and rate limiting.
"""

# Python modules
import asyncio
import json
import logging
from typing import Any, Optional

# Django modules
from django.core.cache import cache

logger = logging.getLogger(__name__)


class RedisService:
    """
    Service for interacting with Redis cache.
    """

    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """
        Get value from cache by key.
        """
        try:
            return await cache.aget(key)
        except Exception as e:
            logger.error("Redis get error for key %s: %s", key, e)
            return None

    @staticmethod
    async def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """
        Set value in cache with optional timeout (seconds).
        """
        try:
            await cache.aset(key, value, timeout=timeout)
            return True
        except Exception as e:
            logger.error("Redis set error for key %s: %s", key, e)
            return False

    @staticmethod
    async def delete(key: str) -> bool:
        """
        Delete key from cache.
        """
        try:
            await cache.adelete(key)
            return True
        except Exception as e:
            logger.error("Redis delete error for key %s: %s", key, e)
            return False

    @staticmethod
    async def delete_pattern(pattern: str) -> int:
        """
        Delete all keys matching pattern.
        """
        try:
            from django.core.cache import caches
            redis_client = caches["default"].client.get_client()
            keys = await asyncio.to_thread(redis_client.keys, f"fastlap:{pattern}")
            if keys:
                return await asyncio.to_thread(redis_client.delete, *keys)
            return 0
        except Exception as e:
            logger.error("Redis delete_pattern error for pattern %s: %s", pattern, e)
            return 0

    @staticmethod
    async def increment(key: str, delta: int = 1) -> Optional[int]:
        """
        Increment counter by delta.
        """
        try:
            return await cache.aincr(key, delta)
        except Exception:
            await cache.aset(key, delta, timeout=60)
            return delta

    @staticmethod
    async def set_json(key: str, data: dict, timeout: Optional[int] = None) -> bool:
        """
        Set JSON data in cache.
        """
        try:
            await cache.aset(key, json.dumps(data), timeout=timeout)
            return True
        except Exception as e:
            logger.error("Redis set_json error for key %s: %s", key, e)
            return False

    @staticmethod
    async def get_json(key: str) -> Optional[dict]:
        """
        Get JSON data from cache.
        """
        try:
            data = await cache.aget(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error("Redis get_json error for key %s: %s", key, e)
            return None
