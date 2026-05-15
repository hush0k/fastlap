"""
Cache utilities for models and queries.
"""

# Python modules
from typing import Any, Optional

# Django modules
from django.core.cache import cache


class ModelCache:
  """
  Cache manager for model instances.
  """
  
  @staticmethod
  def get_model_key(model_name: str, instance_id: int) -> str:
    """Generate cache key for model instance."""
    return f'model:{model_name}:{instance_id}'
  
  @staticmethod
  def get_list_key(model_name: str, filters: dict = None) -> str:
    """Generate cache key for model list."""
    import json
    filter_str = json.dumps(filters, sort_keys=True) if filters else ''
    return f'model_list:{model_name}:{filter_str}'
  
  @staticmethod
  def get_or_set(key: str, callback: callable, timeout: int = 300) -> Any:
    """
    Get from cache or execute callback and cache result.
    """
    result = cache.get(key)
    if result is None:
      result = callback()
      cache.set(key, result, timeout)
    return result
  
  @staticmethod
  def invalidate_model(model_name: str, instance_id: Optional[int] = None):
    """
    Invalidate cache for a model.
    """
    if instance_id:
      cache.delete(ModelCache.get_model_key(model_name, instance_id))
    cache.delete_pattern(f'model_list:{model_name}:*')
    cache.delete_pattern(f'model:{model_name}:*')