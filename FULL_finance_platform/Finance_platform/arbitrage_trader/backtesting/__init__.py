"""Backtesting module for arbitrage trading strategies."""

from .engine import (
    BacktestEngine,
    BacktestConfig,
    BacktestMode,
    BacktestTrade,
    BacktestResult,
    simple_momentum_strategy,
    mean_reversion_strategy,
    cross_exchange_arbitrage_strategy
)
from .data_storage import (
    DataStorage,
    FileStorage,
    SQLiteStorage,
    CachedDataProvider
)

__all__ = [
    # Engine
    "BacktestEngine",
    "BacktestConfig",
    "BacktestMode",
    "BacktestTrade",
    "BacktestResult",

    # Example Strategies
    "simple_momentum_strategy",
    "mean_reversion_strategy",
    "cross_exchange_arbitrage_strategy",

    # Storage
    "DataStorage",
    "FileStorage",
    "SQLiteStorage",
    "CachedDataProvider"
]
