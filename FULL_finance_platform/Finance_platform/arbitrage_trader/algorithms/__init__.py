"""Algorithm modules for arbitrage detection."""

from .cross_exchange import CrossExchangeDetector
from .statistical import StatisticalArbitrageDetector
from .triangular import TriangularArbitrageDetector
from .order_book_analysis import OrderBookAnalyzer, OrderBook, OrderBookLevel
from .market_microstructure import MicrostructureAnalyzer
from .ml_prediction import MLArbitragePredictor
from .gap_detection import GapDetector
from .opportunity_scoring import OpportunityScorer
from .pattern_recognition import PatternRecognizer
from .execution_algorithms import (
    TWAPExecutor,
    VWAPExecutor,
    ImplementationShortfallExecutor,
    POVExecutor,
    AdaptiveExecutor,
    ExecutionManager
)
from .correlation_analysis import CorrelationAnalyzer
from .risk_models import RiskCalculator

__all__ = [
    # Arbitrage Detection
    "CrossExchangeDetector",
    "StatisticalArbitrageDetector",
    "TriangularArbitrageDetector",

    # Market Analysis
    "OrderBookAnalyzer",
    "OrderBook",
    "OrderBookLevel",
    "MicrostructureAnalyzer",
    "MLArbitragePredictor",
    "GapDetector",
    "OpportunityScorer",
    "PatternRecognizer",

    # Execution
    "TWAPExecutor",
    "VWAPExecutor",
    "ImplementationShortfallExecutor",
    "POVExecutor",
    "AdaptiveExecutor",
    "ExecutionManager",

    # Risk & Correlation
    "CorrelationAnalyzer",
    "RiskCalculator"
]
