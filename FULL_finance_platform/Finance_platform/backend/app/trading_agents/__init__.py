"""
Trading Agents Module

Research-based algorithmic trading agents for the Finance Platform

Includes:
- Mean Reversion Agent (Statistical Arbitrage)
- Momentum Trading Agent
- Statistical Arbitrage Agent (Combined Strategy)
- LSTM Price Prediction Agent (Deep Learning)
- Reinforcement Learning Agent (DRL)
- Pairs Trading Agent
- Volatility-Adjusted Momentum Agent
- Ensemble Agent (Multi-Agent Orchestrator)
"""

from .base_agent import (
    BaseTradingAgent,
    AgentType,
    SignalType,
    TradingSignal,
    MarketData,
    AgentPerformance,
    AgentRegistry,
    agent_registry
)

from .strategies import (
    MeanReversionAgent,
    MomentumAgent,
    StatisticalArbitrageAgent,
    LSTMPredictionAgent,
    ReinforcementLearningAgent,
    PairsTradingAgent,
    VolatilityAdjustedMomentumAgent,
    EnsembleAgent,
    EnsembleMethod
)

__all__ = [
    # Base classes
    "BaseTradingAgent",
    "AgentType",
    "SignalType",
    "TradingSignal",
    "MarketData",
    "AgentPerformance",
    "AgentRegistry",
    "agent_registry",

    # Strategy agents
    "MeanReversionAgent",
    "MomentumAgent",
    "StatisticalArbitrageAgent",
    "LSTMPredictionAgent",
    "ReinforcementLearningAgent",
    "PairsTradingAgent",
    "VolatilityAdjustedMomentumAgent",
    "EnsembleAgent",
    "EnsembleMethod"
]
