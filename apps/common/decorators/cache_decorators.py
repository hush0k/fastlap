"""
Caching decorators for views and methods.
"""

# Python modules
import hashlib
import json
from functools import wraps
from typing import Callable

# Django modules
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.utils.decorators import method_decorator

# Project modules
from apps.common.services.redis_service import RedisService


def cache_response(timeout: int = 300, key_prefix: str = ""):
    """
    Decorator to cache API responses.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            cache_key_parts = [key_prefix]

            if request.user and request.user.is_authenticated:
                cache_key_parts.append(f"user_{request.user.id}")

            query_params = request.GET.dict()
            if query_params:
                params_hash = hashlib.md5(
                    json.dumps(query_params, sort_keys=True).encode()
                ).hexdigest()[:8]
                cache_key_parts.append(params_hash)

            if kwargs:
                kwargs_hash = hashlib.md5(
                    json.dumps(kwargs, sort_keys=True).encode()
                ).hexdigest()[:8]
                cache_key_parts.append(kwargs_hash)

            cache_key = ":".join(cache_key_parts)

            cached_response = async_to_sync(RedisService.get)(cache_key)
            if cached_response:
                return cached_response

            response = func(self, request, *args, **kwargs)

            if response.status_code == 200:
                async_to_sync(RedisService.set)(cache_key, response, timeout=timeout)

            return response
        return wrapper
    return decorator


def invalidate_cache(pattern: str):
    """
    Decorator to invalidate cache after mutation.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)
            if response.status_code in [200, 201, 204]:
                async_to_sync(RedisService.delete_pattern)(pattern)
            return response
        return wrapper
    return decorator
