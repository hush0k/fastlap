"""
Redis service for caching and rate limiting.
"""

# Python modules
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
    def get(key: str) -> Optional[Any]:
        """
        Get value from cache by key.
        """
        try:
            return cache.get(key)
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None

    @staticmethod
    def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """
        Set value in cache with optional timeout (seconds).
        """
        try:
            cache.set(key, value, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False

    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete key from cache.
        """
        try:
            cache.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False

    @staticmethod
    def delete_pattern(pattern: str) -> int:
        """
        Delete all keys matching pattern.
        """
        try:
            from django.core.cache import caches

            redis_client = caches["default"].client.get_client()
            keys = redis_client.keys(f"fastlap:{pattern}")
            if keys:
                return redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Redis delete_pattern error for pattern {pattern}: {e}")
            return 0

    @staticmethod
    def increment(key: str, delta: int = 1) -> Optional[int]:
        """
        Increment counter by delta.
        """
        try:
            return cache.incr(key, delta)
        except Exception:
            cache.set(key, delta, timeout=60)
            return delta

    @staticmethod
    def set_json(key: str, data: dict, timeout: Optional[int] = None) -> bool:
        """
        Set JSON data in cache.
        """
        try:
            cache.set(key, json.dumps(data), timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Redis set_json error for key {key}: {e}")
            return False

    @staticmethod
    def get_json(key: str) -> Optional[dict]:
        """
        Get JSON data from cache.
        """
        try:
            data = cache.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get_json error for key {key}: {e}")
            return None
