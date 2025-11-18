"""
Rate Limiting Utility for API Protection

Implements token bucket algorithm for rate limiting.
Can be easily upgraded to use Redis for distributed rate limiting.
"""

from typing import Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
from fastapi import HTTPException, Request
import threading
from collections import defaultdict
import time


class TokenBucket:
    """Token bucket for rate limiting"""

    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens
        Returns True if tokens were available, False otherwise
        """
        with self.lock:
            now = time.time()
            # Refill tokens based on time passed
            time_passed = now - self.last_refill
            self.tokens = min(
                self.capacity,
                self.tokens + time_passed * self.refill_rate
            )
            self.last_refill = now

            # Try to consume
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def get_tokens(self) -> float:
        """Get current token count"""
        with self.lock:
            now = time.time()
            time_passed = now - self.last_refill
            return min(
                self.capacity,
                self.tokens + time_passed * self.refill_rate
            )


class RateLimiter:
    """Rate limiter using token bucket algorithm"""

    def __init__(self):
        self.buckets = defaultdict(lambda: {})
        self.lock = threading.RLock()
        self.cleanup_interval = 300  # 5 minutes

    def check_rate_limit(
        self,
        key: str,
        capacity: int,
        refill_rate: float,
        tokens: int = 1
    ) -> tuple[bool, dict]:
        """
        Check if request is allowed under rate limit

        Args:
            key: Unique identifier (e.g., IP address, user ID)
            capacity: Maximum requests
            refill_rate: Requests per second refill rate
            tokens: Tokens to consume (default 1)

        Returns:
            (allowed: bool, info: dict)
        """
        with self.lock:
            bucket_key = f"{capacity}:{refill_rate}"

            # Get or create bucket for this key
            if bucket_key not in self.buckets[key]:
                self.buckets[key][bucket_key] = TokenBucket(capacity, refill_rate)

            bucket = self.buckets[key][bucket_key]
            allowed = bucket.consume(tokens)

            info = {
                "allowed": allowed,
                "remaining": int(bucket.get_tokens()),
                "capacity": capacity,
                "refill_rate": refill_rate
            }

            return allowed, info

    def reset(self, key: str):
        """Reset rate limit for a key"""
        with self.lock:
            if key in self.buckets:
                del self.buckets[key]

    def cleanup_old_buckets(self):
        """Remove inactive buckets"""
        with self.lock:
            # In production, implement proper cleanup based on last access time
            pass


# Global rate limiter instance
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance"""
    return _rate_limiter


def get_client_identifier(request: Request) -> str:
    """
    Get client identifier for rate limiting

    In production, consider:
    - User ID (if authenticated)
    - API key
    - IP address (as fallback)
    """
    # Try to get user ID from request state (if auth is implemented)
    if hasattr(request.state, "user_id"):
        return f"user:{request.state.user_id}"

    # Fallback to IP address
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"

    client_host = request.client.host if request.client else "unknown"
    return f"ip:{client_host}"


def rate_limit(
    capacity: int = 60,
    window_seconds: int = 60,
    key_func: Optional[Callable] = None
):
    """
    Rate limiting decorator for FastAPI endpoints

    Args:
        capacity: Maximum requests allowed in the time window
        window_seconds: Time window in seconds
        key_func: Optional function to get rate limit key from request

    Usage:
        @router.get("/endpoint")
        @rate_limit(capacity=10, window_seconds=60)  # 10 requests per minute
        async def endpoint(request: Request):
            return {"data": "..."}
    """
    refill_rate = capacity / window_seconds

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(request: Request, *args, **kwargs):
            # Get client identifier
            if key_func:
                key = key_func(request)
            else:
                key = get_client_identifier(request)

            # Check rate limit
            limiter = get_rate_limiter()
            allowed, info = limiter.check_rate_limit(key, capacity, refill_rate)

            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Limit: {capacity} requests per {window_seconds} seconds",
                        "retry_after": int(1 / refill_rate) if refill_rate > 0 else 60,
                        "remaining": info["remaining"],
                        "capacity": capacity
                    }
                )

            # Add rate limit info to response headers
            # Note: In FastAPI, you'd need to use a Response object to set headers
            # This is a simplified version

            # Call the original function
            return await func(request, *args, **kwargs)

        @wraps(func)
        def sync_wrapper(request: Request, *args, **kwargs):
            # Get client identifier
            if key_func:
                key = key_func(request)
            else:
                key = get_client_identifier(request)

            # Check rate limit
            limiter = get_rate_limiter()
            allowed, info = limiter.check_rate_limit(key, capacity, refill_rate)

            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Limit: {capacity} requests per {window_seconds} seconds",
                        "retry_after": int(1 / refill_rate) if refill_rate > 0 else 60,
                        "remaining": info["remaining"],
                        "capacity": capacity
                    }
                )

            # Call the original function
            return func(request, *args, **kwargs)

        # Check if function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Predefined rate limit configurations
class RateLimitConfig:
    """Common rate limit configurations"""

    # Very strict - for expensive operations
    STRICT = {"capacity": 5, "window_seconds": 60}  # 5 per minute

    # Standard - for normal API calls
    STANDARD = {"capacity": 60, "window_seconds": 60}  # 60 per minute

    # Lenient - for lightweight operations
    LENIENT = {"capacity": 300, "window_seconds": 60}  # 300 per minute

    # For authentication attempts
    AUTH = {"capacity": 5, "window_seconds": 300}  # 5 per 5 minutes

    # For search operations
    SEARCH = {"capacity": 30, "window_seconds": 60}  # 30 per minute

    # For data exports
    EXPORT = {"capacity": 2, "window_seconds": 300}  # 2 per 5 minutes
