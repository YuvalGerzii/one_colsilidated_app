"""
Caching utility for performance optimization

Provides in-memory caching with TTL support.
Can be easily upgraded to Redis for distributed caching.
"""

from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
import threading


class CacheStore:
    """Thread-safe in-memory cache with TTL support"""

    def __init__(self):
        self._cache = {}
        self._lock = threading.RLock()
        self._ttl_defaults = {
            "profile": 300,  # 5 minutes
            "jobs": 60,      # 1 minute
            "analytics": 300,  # 5 minutes
            "marketplace": 180,  # 3 minutes
            "default": 120   # 2 minutes
        }

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if datetime.utcnow() > entry["expires_at"]:
                del self._cache[key]
                return None

            entry["hits"] += 1
            entry["last_accessed"] = datetime.utcnow()
            return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None, category: str = "default"):
        """Set value in cache with TTL"""
        if ttl_seconds is None:
            ttl_seconds = self._ttl_defaults.get(category, self._ttl_defaults["default"])

        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": datetime.utcnow() + timedelta(seconds=ttl_seconds),
                "created_at": datetime.utcnow(),
                "last_accessed": datetime.utcnow(),
                "hits": 0,
                "category": category
            }

    def delete(self, key: str):
        """Delete a key from cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def delete_pattern(self, pattern: str):
        """Delete all keys matching a pattern (simple prefix matching)"""
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(pattern)]
            for key in keys_to_delete:
                del self._cache[key]

    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self):
        """Remove all expired entries"""
        with self._lock:
            now = datetime.utcnow()
            expired_keys = [
                k for k, v in self._cache.items()
                if now > v["expires_at"]
            ]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)

    def get_stats(self) -> dict:
        """Get cache statistics"""
        with self._lock:
            total_entries = len(self._cache)
            total_hits = sum(v["hits"] for v in self._cache.values())
            categories = {}

            for entry in self._cache.values():
                cat = entry["category"]
                if cat not in categories:
                    categories[cat] = {"count": 0, "hits": 0}
                categories[cat]["count"] += 1
                categories[cat]["hits"] += entry["hits"]

            return {
                "total_entries": total_entries,
                "total_hits": total_hits,
                "categories": categories,
                "memory_estimate_kb": total_entries * 2  # Rough estimate
            }


# Global cache instance
_cache = CacheStore()


def get_cache() -> CacheStore:
    """Get the global cache instance"""
    return _cache


def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments"""
    # Create a deterministic string from args and kwargs
    key_data = {
        "args": args,
        "kwargs": sorted(kwargs.items())
    }
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl_seconds: Optional[int] = None, category: str = "default", key_prefix: str = ""):
    """
    Decorator to cache function results

    Usage:
        @cached(ttl_seconds=300, category="profile")
        def get_profile(user_id):
            return expensive_operation()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}{func.__name__}:{cache_key(*args, **kwargs)}"

            # Try to get from cache
            cached_value = _cache.get(key)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            result = func(*args, **kwargs)
            _cache.set(key, result, ttl_seconds=ttl_seconds, category=category)

            return result

        # Add cache management methods to the wrapper
        wrapper.cache_clear = lambda: _cache.delete_pattern(f"{key_prefix}{func.__name__}:")
        wrapper.cache_info = lambda: _cache.get_stats()

        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str):
    """Invalidate all cache entries matching a pattern"""
    _cache.delete_pattern(pattern)


def clear_all_cache():
    """Clear all cache entries"""
    _cache.clear()
