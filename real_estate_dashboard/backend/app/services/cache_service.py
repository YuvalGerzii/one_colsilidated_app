"""
Enhanced Cache Service with Redis and In-Memory Fallback

Provides a robust caching layer with:
- Redis backend for persistent caching (optional)
- In-memory fallback when Redis is unavailable
- Configurable TTL per cache type
- Async support for better performance
- Cache statistics and monitoring
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, Callable
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


class CacheService:
    """
    Enhanced caching service with Redis support and in-memory fallback
    """

    # Cache TTL configurations (in seconds)
    TTL_CONFIG = {
        "market_data": 3600,           # 1 hour for market data
        "integration_status": 300,      # 5 minutes for integration health
        "api_response": 1800,           # 30 minutes for API responses
        "static_data": 86400,           # 24 hours for static data
        "economic_indicators": 3600,    # 1 hour for economic data
        "real_estate_data": 3600,       # 1 hour for real estate market data
        "default": 1800,                # 30 minutes default
    }

    def __init__(self, redis_client: Optional[Any] = None):
        """
        Initialize cache service

        Args:
            redis_client: Optional Redis client (if None, uses in-memory only)
        """
        self.redis = redis_client
        self.use_redis = redis_client is not None

        # In-memory cache as fallback
        self.memory_cache: Dict[str, tuple[Any, datetime]] = {}

        # Cache statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "redis_errors": 0,
            "memory_fallbacks": 0,
        }

        logger.info(f"CacheService initialized (Redis: {self.use_redis})")

    def _get_ttl(self, cache_type: str) -> int:
        """Get TTL for a cache type"""
        return self.TTL_CONFIG.get(cache_type, self.TTL_CONFIG["default"])

    def _make_key(self, namespace: str, key: str) -> str:
        """Create a namespaced cache key"""
        return f"cache:{namespace}:{key}"

    async def get(
        self,
        key: str,
        namespace: str = "default",
        cache_type: str = "default"
    ) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key
            namespace: Cache namespace (e.g., 'market_data', 'integrations')
            cache_type: Type of cache for TTL configuration

        Returns:
            Cached value or None if not found/expired
        """
        full_key = self._make_key(namespace, key)

        # Try Redis first if available
        if self.use_redis:
            try:
                value = await self._get_from_redis(full_key)
                if value is not None:
                    self.stats["hits"] += 1
                    logger.debug(f"Cache HIT (Redis): {full_key}")
                    return value
            except Exception as e:
                logger.warning(f"Redis error, falling back to memory: {e}")
                self.stats["redis_errors"] += 1
                self.stats["memory_fallbacks"] += 1

        # Fallback to in-memory cache
        value = self._get_from_memory(full_key)
        if value is not None:
            self.stats["hits"] += 1
            logger.debug(f"Cache HIT (Memory): {full_key}")
            return value

        self.stats["misses"] += 1
        logger.debug(f"Cache MISS: {full_key}")
        return None

    async def set(
        self,
        key: str,
        value: Any,
        namespace: str = "default",
        cache_type: str = "default",
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            namespace: Cache namespace
            cache_type: Type of cache for TTL configuration
            ttl: Optional custom TTL (overrides cache_type TTL)

        Returns:
            True if successfully cached
        """
        full_key = self._make_key(namespace, key)
        ttl_seconds = ttl if ttl is not None else self._get_ttl(cache_type)

        # Try Redis first
        if self.use_redis:
            try:
                await self._set_in_redis(full_key, value, ttl_seconds)
                logger.debug(f"Cached in Redis: {full_key} (TTL: {ttl_seconds}s)")
            except Exception as e:
                logger.warning(f"Redis error, caching in memory only: {e}")
                self.stats["redis_errors"] += 1

        # Always cache in memory as well (fallback)
        self._set_in_memory(full_key, value, ttl_seconds)
        logger.debug(f"Cached in Memory: {full_key} (TTL: {ttl_seconds}s)")

        return True

    async def delete(self, key: str, namespace: str = "default") -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key
            namespace: Cache namespace

        Returns:
            True if successfully deleted
        """
        full_key = self._make_key(namespace, key)

        # Delete from Redis
        if self.use_redis:
            try:
                await self._delete_from_redis(full_key)
            except Exception as e:
                logger.warning(f"Redis delete error: {e}")
                self.stats["redis_errors"] += 1

        # Delete from memory
        if full_key in self.memory_cache:
            del self.memory_cache[full_key]

        logger.debug(f"Deleted from cache: {full_key}")
        return True

    async def clear_namespace(self, namespace: str) -> int:
        """
        Clear all keys in a namespace

        Args:
            namespace: Cache namespace to clear

        Returns:
            Number of keys deleted
        """
        pattern = f"cache:{namespace}:*"
        deleted_count = 0

        # Clear from Redis
        if self.use_redis:
            try:
                keys = await self._scan_redis_keys(pattern)
                for key in keys:
                    await self._delete_from_redis(key)
                    deleted_count += 1
            except Exception as e:
                logger.warning(f"Redis clear namespace error: {e}")
                self.stats["redis_errors"] += 1

        # Clear from memory
        keys_to_delete = [k for k in self.memory_cache.keys() if k.startswith(f"cache:{namespace}:")]
        for key in keys_to_delete:
            del self.memory_cache[key]
            deleted_count += 1

        logger.info(f"Cleared {deleted_count} keys from namespace: {namespace}")
        return deleted_count

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            **self.stats,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "memory_cache_size": len(self.memory_cache),
            "redis_enabled": self.use_redis,
        }

    def reset_stats(self):
        """Reset cache statistics"""
        self.stats = {
            "hits": 0,
            "misses": 0,
            "redis_errors": 0,
            "memory_fallbacks": 0,
        }

    # Redis operations
    async def _get_from_redis(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if not self.redis:
            return None

        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def _set_in_redis(self, key: str, value: Any, ttl: int):
        """Set value in Redis"""
        if not self.redis:
            return

        serialized = json.dumps(value)
        await self.redis.setex(key, ttl, serialized)

    async def _delete_from_redis(self, key: str):
        """Delete value from Redis"""
        if not self.redis:
            return

        await self.redis.delete(key)

    async def _scan_redis_keys(self, pattern: str) -> list:
        """Scan Redis keys matching pattern"""
        if not self.redis:
            return []

        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = await self.redis.scan(cursor, match=pattern, count=100)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return keys

    # Memory cache operations
    def _get_from_memory(self, key: str) -> Optional[Any]:
        """Get value from memory cache"""
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if datetime.utcnow() < expiry:
                return value
            else:
                # Expired, remove it
                del self.memory_cache[key]
        return None

    def _set_in_memory(self, key: str, value: Any, ttl: int):
        """Set value in memory cache"""
        expiry = datetime.utcnow() + timedelta(seconds=ttl)
        self.memory_cache[key] = (value, expiry)

    def _cleanup_expired_memory(self):
        """Clean up expired entries from memory cache"""
        now = datetime.utcnow()
        expired_keys = [k for k, (_, expiry) in self.memory_cache.items() if now >= expiry]
        for key in expired_keys:
            del self.memory_cache[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired memory cache entries")


def cached(
    namespace: str = "default",
    cache_type: str = "default",
    ttl: Optional[int] = None,
    key_func: Optional[Callable] = None
):
    """
    Decorator for caching function results

    Args:
        namespace: Cache namespace
        cache_type: Type of cache for TTL configuration
        ttl: Optional custom TTL
        key_func: Optional function to generate cache key from function args

    Example:
        @cached(namespace="market_data", cache_type="market_data")
        async def get_market_summary(location: str):
            # Expensive API call
            return data
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache service from first argument if available (for class methods)
            cache_service = None
            if args and hasattr(args[0], 'cache'):
                cache_service = args[0].cache

            if not cache_service:
                # No cache available, execute function
                return await func(*args, **kwargs)

            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                cache_key = f"{func.__name__}:{str(args[1:])}:{str(kwargs)}"

            # Try to get from cache
            cached_value = await cache_service.get(cache_key, namespace, cache_type)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key, result, namespace, cache_type, ttl)

            return result
        return wrapper
    return decorator


# Global cache service instance (initialized on app startup)
cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get the global cache service instance"""
    global cache_service
    if cache_service is None:
        # Initialize with in-memory only (Redis can be added later)
        cache_service = CacheService()
    return cache_service


async def init_cache_service(redis_client: Optional[Any] = None):
    """
    Initialize the global cache service

    Args:
        redis_client: Optional Redis client
    """
    global cache_service
    cache_service = CacheService(redis_client)
    logger.info("Cache service initialized")
