"""
Trading Agent Strategies

Collection of research-based algorithmic trading strategies
"""

from .mean_reversion_agent import MeanReversionAgent
from .momentum_agent import MomentumAgent
from .statistical_arbitrage_agent import StatisticalArbitrageAgent
from .lstm_prediction_agent import LSTMPredictionAgent
from .reinforcement_learning_agent import ReinforcementLearningAgent
from .pairs_trading_agent import PairsTradingAgent
from .volatility_adjusted_momentum_agent import VolatilityAdjustedMomentumAgent
from .ensemble_agent import EnsembleAgent, EnsembleMethod

__all__ = [
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
