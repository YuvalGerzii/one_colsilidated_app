"""
Retry utilities for integrations

Provides retry logic with exponential backoff for API calls
"""

import asyncio
import logging
from typing import Callable, Any, Optional, TypeVar, Union
from functools import wraps
import httpx

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryConfig:
    """Configuration for retry behavior"""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        """
        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff (delay = initial_delay * base^attempt)
            jitter: Add random jitter to delay to prevent thundering herd
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        import random

        # Exponential backoff: delay = initial_delay * (base ^ attempt)
        delay = min(
            self.initial_delay * (self.exponential_base ** attempt),
            self.max_delay
        )

        # Add jitter (random factor between 0.5 and 1.5)
        if self.jitter:
            delay = delay * (0.5 + random.random())

        return delay


# Exceptions that are retryable
RETRYABLE_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.NetworkError,
    ConnectionError,
    TimeoutError,
)


def is_retryable_exception(exc: Exception) -> bool:
    """Check if exception is retryable"""
    if isinstance(exc, RETRYABLE_EXCEPTIONS):
        return True

    # Check for HTTP status codes that are retryable
    if isinstance(exc, httpx.HTTPStatusError):
        # Retry on 429 (Too Many Requests), 500, 502, 503, 504
        status_code = exc.response.status_code
        return status_code in [429, 500, 502, 503, 504]

    return False


async def retry_async(
    func: Callable[..., Any],
    config: Optional[RetryConfig] = None,
    operation_name: str = "operation"
) -> Any:
    """
    Retry an async function with exponential backoff

    Args:
        func: Async function to retry
        config: Retry configuration (uses default if None)
        operation_name: Name of operation for logging

    Returns:
        Result of function call

    Raises:
        Last exception if all retries fail
    """
    if config is None:
        config = RetryConfig()

    last_exception = None

    for attempt in range(config.max_retries + 1):
        try:
            result = await func()

            # Log success after retry
            if attempt > 0:
                logger.info(
                    f"{operation_name} succeeded on attempt {attempt + 1}/{config.max_retries + 1}"
                )

            return result

        except Exception as e:
            last_exception = e

            # Check if exception is retryable
            if not is_retryable_exception(e):
                logger.warning(
                    f"{operation_name} failed with non-retryable error: {type(e).__name__}: {str(e)}"
                )
                raise

            # Check if we have retries left
            if attempt >= config.max_retries:
                logger.error(
                    f"{operation_name} failed after {config.max_retries + 1} attempts: {type(e).__name__}: {str(e)}"
                )
                raise

            # Calculate delay and wait
            delay = config.calculate_delay(attempt)
            logger.warning(
                f"{operation_name} failed (attempt {attempt + 1}/{config.max_retries + 1}): "
                f"{type(e).__name__}: {str(e)}. Retrying in {delay:.2f}s..."
            )

            await asyncio.sleep(delay)

    # Should never reach here, but just in case
    if last_exception:
        raise last_exception


def retry_with_config(config: Optional[RetryConfig] = None, operation_name: Optional[str] = None):
    """
    Decorator for async functions to add retry logic

    Args:
        config: Retry configuration
        operation_name: Name of operation for logging (uses function name if None)

    Example:
        @retry_with_config(RetryConfig(max_retries=5), "fetch_data")
        async def fetch_data():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__

            async def call_func():
                return await func(*args, **kwargs)

            return await retry_async(call_func, config, op_name)

        return wrapper
    return decorator


# Predefined retry configurations for common scenarios

# Fast retry for quick operations (max 3 attempts, 1-4s delays)
FAST_RETRY = RetryConfig(
    max_retries=3,
    initial_delay=1.0,
    max_delay=4.0,
    exponential_base=2.0,
    jitter=True
)

# Standard retry for normal operations (max 3 attempts, 2-16s delays)
STANDARD_RETRY = RetryConfig(
    max_retries=3,
    initial_delay=2.0,
    max_delay=16.0,
    exponential_base=2.0,
    jitter=True
)

# Aggressive retry for critical operations (max 5 attempts, 2-60s delays)
AGGRESSIVE_RETRY = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True
)

# Conservative retry for rate-limited APIs (max 3 attempts, 5-30s delays)
CONSERVATIVE_RETRY = RetryConfig(
    max_retries=3,
    initial_delay=5.0,
    max_delay=30.0,
    exponential_base=1.5,
    jitter=True
)
