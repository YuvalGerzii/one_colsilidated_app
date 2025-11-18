"""
Error recovery and resilience mechanisms.

Implements robustness best practices from 2025 research.
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional, TypeVar
from enum import Enum
from datetime import datetime, timedelta
from loguru import logger

T = TypeVar('T')


class RetryStrategy(Enum):
    """Retry strategies."""
    IMMEDIATE = "immediate"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class ResilientExecutor:
    """
    Resilient task execution with error recovery.

    Features:
    - Automatic retry with backoff
    - Circuit breaker pattern
    - Fallback strategies
    - Timeout handling
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        backoff_factor: float = 2.0,
    ):
        """
        Initialize resilient executor.

        Args:
            max_retries: Maximum retry attempts
            initial_delay: Initial retry delay in seconds
            max_delay: Maximum retry delay
            backoff_factor: Backoff multiplication factor
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

        # Circuit breakers for different operations
        self.circuit_breakers: Dict[str, 'CircuitBreaker'] = {}

        # Fallback handlers
        self.fallback_handlers: Dict[str, Callable] = {}

        logger.info("ResilientExecutor initialized")

    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
        max_retries: Optional[int] = None,
        **kwargs
    ) -> Any:
        """
        Execute function with automatic retry.

        Args:
            func: Function to execute
            *args: Positional arguments
            retry_strategy: Retry strategy to use
            max_retries: Override max retries
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all retries fail
        """
        max_attempts = max_retries or self.max_retries
        last_exception = None

        for attempt in range(max_attempts + 1):
            try:
                # Execute function
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # Success
                if attempt > 0:
                    logger.info(f"Succeeded after {attempt} retries")

                return result

            except Exception as e:
                last_exception = e
                logger.warning(
                    f"Attempt {attempt + 1}/{max_attempts + 1} failed: {e}"
                )

                if attempt < max_attempts:
                    # Calculate delay
                    delay = self._calculate_delay(
                        attempt, retry_strategy
                    )

                    logger.info(f"Retrying in {delay:.2f}s...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"All {max_attempts + 1} attempts failed"
                    )

        # All retries exhausted
        raise last_exception

    def _calculate_delay(
        self, attempt: int, strategy: RetryStrategy
    ) -> float:
        """Calculate retry delay based on strategy."""
        if strategy == RetryStrategy.IMMEDIATE:
            return 0.0

        elif strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.initial_delay * (attempt + 1)

        else:  # EXPONENTIAL_BACKOFF
            delay = self.initial_delay * (self.backoff_factor ** attempt)

        return min(delay, self.max_delay)

    async def execute_with_circuit_breaker(
        self,
        operation_name: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute with circuit breaker pattern.

        Args:
            operation_name: Name of the operation
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If circuit is open or execution fails
        """
        # Get or create circuit breaker
        if operation_name not in self.circuit_breakers:
            self.circuit_breakers[operation_name] = CircuitBreaker(
                operation_name
            )

        breaker = self.circuit_breakers[operation_name]

        # Check circuit state
        if not breaker.can_execute():
            raise Exception(
                f"Circuit breaker OPEN for {operation_name}"
            )

        try:
            # Execute
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Record success
            breaker.record_success()
            return result

        except Exception as e:
            # Record failure
            breaker.record_failure()
            raise

    async def execute_with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Optional[Callable] = None,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute with fallback on failure.

        Args:
            primary_func: Primary function to execute
            fallback_func: Fallback function (optional)
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result from primary or fallback function
        """
        try:
            # Try primary function
            if asyncio.iscoroutinefunction(primary_func):
                return await primary_func(*args, **kwargs)
            else:
                return primary_func(*args, **kwargs)

        except Exception as e:
            logger.warning(f"Primary function failed: {e}")

            if fallback_func:
                logger.info("Executing fallback function")
                try:
                    if asyncio.iscoroutinefunction(fallback_func):
                        return await fallback_func(*args, **kwargs)
                    else:
                        return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    raise

            # No fallback available
            raise

    async def execute_with_timeout(
        self,
        func: Callable,
        timeout_seconds: float,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute with timeout.

        Args:
            func: Function to execute
            timeout_seconds: Timeout in seconds
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            asyncio.TimeoutError: If execution times out
        """
        try:
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout_seconds
                )
            else:
                # Wrap sync function in coroutine with timeout
                result = await asyncio.wait_for(
                    asyncio.to_thread(func, *args, **kwargs),
                    timeout=timeout_seconds
                )

            return result

        except asyncio.TimeoutError:
            logger.error(
                f"Execution timed out after {timeout_seconds}s"
            )
            raise


class CircuitBreaker:
    """
    Circuit breaker for preventing cascading failures.
    """

    def __init__(
        self,
        operation_name: str,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout_seconds: float = 60.0,
    ):
        """
        Initialize circuit breaker.

        Args:
            operation_name: Name of the operation
            failure_threshold: Failures before opening circuit
            success_threshold: Successes needed to close circuit
            timeout_seconds: Timeout before trying half-open
        """
        self.operation_name = operation_name
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout_seconds = timeout_seconds

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None

    def can_execute(self) -> bool:
        """Check if execution is allowed."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout_seconds:
                    logger.info(
                        f"Circuit breaker {self.operation_name}: "
                        f"OPEN -> HALF_OPEN"
                    )
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    return True

            return False

        # HALF_OPEN state
        return True

    def record_success(self) -> None:
        """Record successful execution."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1

            if self.success_count >= self.success_threshold:
                logger.info(
                    f"Circuit breaker {self.operation_name}: "
                    f"HALF_OPEN -> CLOSED"
                )
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0

        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self) -> None:
        """Record failed execution."""
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            logger.info(
                f"Circuit breaker {self.operation_name}: "
                f"HALF_OPEN -> OPEN (failure during recovery)"
            )
            self.state = CircuitState.OPEN
            self.failure_count = 0
            self.success_count = 0

        elif self.state == CircuitState.CLOSED:
            self.failure_count += 1

            if self.failure_count >= self.failure_threshold:
                logger.warning(
                    f"Circuit breaker {self.operation_name}: "
                    f"CLOSED -> OPEN ({self.failure_count} failures)"
                )
                self.state = CircuitState.OPEN

    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "operation": self.operation_name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None,
        }
