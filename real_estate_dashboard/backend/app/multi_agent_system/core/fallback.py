"""
Advanced fallback system with multi-level chains and automatic selection.

Implements enterprise-grade fallback strategies for resilient operation.
"""

from typing import Any, Callable, Dict, List, Optional, TypeVar
from enum import Enum
from dataclasses import dataclass
from loguru import logger
import asyncio

T = TypeVar('T')


class FallbackStrategy(Enum):
    """Fallback execution strategies."""
    SEQUENTIAL = "sequential"  # Try fallbacks in order
    PARALLEL = "parallel"  # Try all fallbacks simultaneously
    WEIGHTED = "weighted"  # Use weights to select fallback
    ADAPTIVE = "adaptive"  # Learn which fallback works best


@dataclass
class FallbackOption:
    """A single fallback option."""
    name: str
    handler: Callable
    priority: int = 1  # Higher priority tried first
    weight: float = 1.0  # For weighted selection
    success_count: int = 0
    failure_count: int = 0
    avg_execution_time: float = 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5  # Unknown, assume neutral
        return self.success_count / total

    @property
    def score(self) -> float:
        """Calculate overall score for adaptive selection."""
        # Combine success rate and execution time
        success_score = self.success_rate
        time_score = 1.0 / (1.0 + self.avg_execution_time)  # Faster is better
        return 0.7 * success_score + 0.3 * time_score


class FallbackChain:
    """
    Multi-level fallback chain with automatic selection.

    Supports multiple fallback strategies and learns from execution history.
    """

    def __init__(
        self,
        name: str,
        strategy: FallbackStrategy = FallbackStrategy.SEQUENTIAL,
    ):
        """
        Initialize fallback chain.

        Args:
            name: Name of the fallback chain
            strategy: Fallback execution strategy
        """
        self.name = name
        self.strategy = strategy
        self.fallbacks: List[FallbackOption] = []
        self.execution_count = 0

        logger.info(f"FallbackChain '{name}' initialized with {strategy.value} strategy")

    def add_fallback(
        self,
        name: str,
        handler: Callable,
        priority: int = 1,
        weight: float = 1.0,
    ) -> None:
        """
        Add a fallback option.

        Args:
            name: Fallback name
            handler: Fallback handler function
            priority: Priority (higher = tried first)
            weight: Weight for weighted selection
        """
        fallback = FallbackOption(
            name=name,
            handler=handler,
            priority=priority,
            weight=weight,
        )
        self.fallbacks.append(fallback)

        # Sort by priority
        self.fallbacks.sort(key=lambda f: f.priority, reverse=True)

        logger.debug(f"Added fallback '{name}' to chain '{self.name}'")

    async def execute(
        self,
        primary_handler: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute with fallback chain.

        Args:
            primary_handler: Primary function to try
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result from primary or fallback

        Raises:
            Exception: If all options fail
        """
        self.execution_count += 1

        # Try primary first
        try:
            logger.debug(f"Executing primary handler for '{self.name}'")
            result = await self._execute_handler(primary_handler, *args, **kwargs)
            logger.info(f"Primary handler succeeded for '{self.name}'")
            return result
        except Exception as primary_error:
            logger.warning(
                f"Primary handler failed for '{self.name}': {primary_error}"
            )

            # Execute fallback strategy
            if self.strategy == FallbackStrategy.SEQUENTIAL:
                return await self._execute_sequential(*args, **kwargs)
            elif self.strategy == FallbackStrategy.PARALLEL:
                return await self._execute_parallel(*args, **kwargs)
            elif self.strategy == FallbackStrategy.WEIGHTED:
                return await self._execute_weighted(*args, **kwargs)
            elif self.strategy == FallbackStrategy.ADAPTIVE:
                return await self._execute_adaptive(*args, **kwargs)

    async def _execute_sequential(self, *args, **kwargs) -> Any:
        """Execute fallbacks sequentially in priority order."""
        last_error = None

        for fallback in self.fallbacks:
            try:
                logger.info(f"Trying fallback '{fallback.name}'")
                import time
                start = time.time()

                result = await self._execute_handler(fallback.handler, *args, **kwargs)

                # Update statistics
                execution_time = time.time() - start
                fallback.success_count += 1
                fallback.avg_execution_time = (
                    fallback.avg_execution_time * (fallback.success_count - 1)
                    + execution_time
                ) / fallback.success_count

                logger.info(
                    f"Fallback '{fallback.name}' succeeded "
                    f"(time={execution_time:.2f}s)"
                )
                return result

            except Exception as e:
                fallback.failure_count += 1
                last_error = e
                logger.warning(f"Fallback '{fallback.name}' failed: {e}")
                continue

        # All fallbacks failed
        logger.error(f"All fallbacks exhausted for '{self.name}'")
        raise Exception(
            f"Primary and all {len(self.fallbacks)} fallbacks failed. "
            f"Last error: {last_error}"
        )

    async def _execute_parallel(self, *args, **kwargs) -> Any:
        """Execute all fallbacks in parallel, return first success."""
        if not self.fallbacks:
            raise Exception("No fallbacks available")

        # Create tasks for all fallbacks
        tasks = []
        for fallback in self.fallbacks:
            task = asyncio.create_task(
                self._execute_handler(fallback.handler, *args, **kwargs)
            )
            tasks.append((fallback, task))

        # Wait for first success
        done = []
        pending = [task for _, task in tasks]

        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                # Find which fallback completed
                for fallback, fb_task in tasks:
                    if fb_task == task:
                        try:
                            result = task.result()
                            fallback.success_count += 1

                            # Cancel remaining tasks
                            for p in pending:
                                p.cancel()

                            logger.info(f"Parallel fallback '{fallback.name}' succeeded")
                            return result

                        except Exception as e:
                            fallback.failure_count += 1
                            logger.debug(f"Fallback '{fallback.name}' failed: {e}")
                            break

        # All failed
        raise Exception(f"All parallel fallbacks failed for '{self.name}'")

    async def _execute_weighted(self, *args, **kwargs) -> Any:
        """Execute fallback selected by weight."""
        if not self.fallbacks:
            raise Exception("No fallbacks available")

        # Select based on weights
        import random
        weights = [f.weight for f in self.fallbacks]
        selected = random.choices(self.fallbacks, weights=weights, k=1)[0]

        logger.info(f"Selected weighted fallback '{selected.name}'")

        try:
            result = await self._execute_handler(selected.handler, *args, **kwargs)
            selected.success_count += 1
            return result
        except Exception as e:
            selected.failure_count += 1
            logger.warning(f"Weighted fallback '{selected.name}' failed: {e}")

            # Try sequential as backup
            remaining = [f for f in self.fallbacks if f != selected]
            for fallback in remaining:
                try:
                    result = await self._execute_handler(fallback.handler, *args, **kwargs)
                    fallback.success_count += 1
                    return result
                except Exception as e2:
                    fallback.failure_count += 1
                    continue

            raise Exception(f"All weighted fallbacks failed")

    async def _execute_adaptive(self, *args, **kwargs) -> Any:
        """Execute fallback using adaptive selection based on history."""
        if not self.fallbacks:
            raise Exception("No fallbacks available")

        # Sort by score (best performing first)
        sorted_fallbacks = sorted(
            self.fallbacks,
            key=lambda f: f.score,
            reverse=True
        )

        logger.debug(
            f"Adaptive selection scores: "
            f"{[(f.name, f.score) for f in sorted_fallbacks[:3]]}"
        )

        # Try in order of best score
        for fallback in sorted_fallbacks:
            try:
                import time
                start = time.time()

                result = await self._execute_handler(fallback.handler, *args, **kwargs)

                execution_time = time.time() - start
                fallback.success_count += 1
                fallback.avg_execution_time = (
                    fallback.avg_execution_time * (fallback.success_count - 1)
                    + execution_time
                ) / fallback.success_count

                logger.info(
                    f"Adaptive fallback '{fallback.name}' succeeded "
                    f"(score={fallback.score:.3f})"
                )
                return result

            except Exception as e:
                fallback.failure_count += 1
                logger.debug(f"Adaptive fallback '{fallback.name}' failed: {e}")
                continue

        raise Exception("All adaptive fallbacks failed")

    async def _execute_handler(self, handler: Callable, *args, **kwargs) -> Any:
        """Execute a handler (async or sync)."""
        if asyncio.iscoroutinefunction(handler):
            return await handler(*args, **kwargs)
        else:
            return handler(*args, **kwargs)

    def get_statistics(self) -> Dict[str, Any]:
        """Get fallback chain statistics."""
        return {
            "name": self.name,
            "strategy": self.strategy.value,
            "execution_count": self.execution_count,
            "fallback_count": len(self.fallbacks),
            "fallbacks": [
                {
                    "name": f.name,
                    "priority": f.priority,
                    "success_rate": f.success_rate,
                    "avg_time": f.avg_execution_time,
                    "score": f.score,
                }
                for f in self.fallbacks
            ],
        }


class FallbackRegistry:
    """
    Global registry for managing fallback chains.
    """

    def __init__(self):
        """Initialize fallback registry."""
        self.chains: Dict[str, FallbackChain] = {}
        logger.info("FallbackRegistry initialized")

    def register_chain(
        self,
        name: str,
        strategy: FallbackStrategy = FallbackStrategy.ADAPTIVE,
    ) -> FallbackChain:
        """
        Register a new fallback chain.

        Args:
            name: Chain name
            strategy: Fallback strategy

        Returns:
            FallbackChain instance
        """
        if name in self.chains:
            logger.warning(f"Fallback chain '{name}' already exists")
            return self.chains[name]

        chain = FallbackChain(name, strategy)
        self.chains[name] = chain

        logger.info(f"Registered fallback chain '{name}'")
        return chain

    def get_chain(self, name: str) -> Optional[FallbackChain]:
        """Get a fallback chain by name."""
        return self.chains.get(name)

    def get_all_statistics(self) -> Dict[str, Any]:
        """Get statistics for all chains."""
        return {
            name: chain.get_statistics()
            for name, chain in self.chains.items()
        }


# Global registry instance
_global_registry = FallbackRegistry()


def get_fallback_registry() -> FallbackRegistry:
    """Get the global fallback registry."""
    return _global_registry
