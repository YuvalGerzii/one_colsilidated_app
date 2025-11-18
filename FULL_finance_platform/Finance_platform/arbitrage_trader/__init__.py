"""
Multi-Agent Arbitrage Trading System

A sophisticated arbitrage detection and trading system using multiple specialized agents.
"""

__version__ = "1.0.0"
__author__ = "Finance Platform Team"

from .orchestrator import ArbitrageOrchestrator
from .config.default_config import get_config

# Agent imports
from .agents.cross_exchange_agent import CrossExchangeAgent
from .agents.statistical_agent import StatisticalArbitrageAgent
from .agents.triangular_agent import TriangularArbitrageAgent
from .agents.risk_manager_agent import RiskManagerAgent

# Service imports
from .services.market_data_service import MarketDataService
from .services.execution_service import ExecutionService

# Model imports
from .models.types import (
    ArbitrageType,
    MarketType,
    ArbitrageOpportunity,
    MarketData,
    Trade,
    TradingAction,
    PerformanceMetrics
)

__all__ = [
    # Main components
    "ArbitrageOrchestrator",
    "get_config",

    # Agents
    "CrossExchangeAgent",
    "StatisticalArbitrageAgent",
    "TriangularArbitrageAgent",
    "RiskManagerAgent",

    # Services
    "MarketDataService",
    "ExecutionService",

    # Types
    "ArbitrageType",
    "MarketType",
    "ArbitrageOpportunity",
    "MarketData",
    "Trade",
    "TradingAction",
    "PerformanceMetrics"
]
