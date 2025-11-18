"""
Data models and types for the arbitrage trading system.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from decimal import Decimal


class ArbitrageType(Enum):
    """Types of arbitrage opportunities."""
    CROSS_EXCHANGE = "cross_exchange"  # Spatial arbitrage across exchanges
    STATISTICAL = "statistical"  # Statistical arbitrage (pairs trading, mean reversion)
    TRIANGULAR = "triangular"  # Triangular arbitrage (e.g., currency triangles)
    LATENCY = "latency"  # Latency arbitrage
    INDEX = "index"  # Index arbitrage
    MERGER = "merger"  # Merger arbitrage
    CONVERTIBLE = "convertible"  # Convertible arbitrage
    OPTIONS = "options"  # Options arbitrage


class MarketType(Enum):
    """Types of markets."""
    CRYPTO = "crypto"
    FOREX = "forex"
    STOCKS = "stocks"
    COMMODITIES = "commodities"
    BONDS = "bonds"
    OPTIONS = "options"
    FUTURES = "futures"


class OrderSide(Enum):
    """Order side."""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Order status."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIAL_FILL = "partial_fill"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class MarketData:
    """Market data snapshot."""
    symbol: str
    exchange: str
    market_type: MarketType
    bid_price: Decimal
    ask_price: Decimal
    bid_volume: Decimal
    ask_volume: Decimal
    timestamp: datetime
    last_trade_price: Optional[Decimal] = None
    volume_24h: Optional[Decimal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def mid_price(self) -> Decimal:
        """Calculate mid price."""
        return (self.bid_price + self.ask_price) / Decimal(2)

    @property
    def spread(self) -> Decimal:
        """Calculate spread."""
        return self.ask_price - self.bid_price

    @property
    def spread_percentage(self) -> Decimal:
        """Calculate spread as percentage of mid price."""
        if self.mid_price == 0:
            return Decimal(0)
        return (self.spread / self.mid_price) * Decimal(100)


@dataclass
class ArbitrageOpportunity:
    """Detected arbitrage opportunity."""
    opportunity_id: str
    arbitrage_type: ArbitrageType
    market_type: MarketType
    symbol: str
    timestamp: datetime
    expected_profit: Decimal
    expected_profit_percentage: Decimal
    confidence_score: Decimal  # 0-1
    risk_score: Decimal  # 0-1
    detection_latency_ms: float

    # Market data involved
    market_data: List[MarketData]

    # Execution details
    suggested_actions: List['TradingAction']

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_viable(self, min_profit_threshold: Decimal = Decimal("0.001")) -> bool:
        """Check if opportunity is viable for execution."""
        return (
            self.expected_profit_percentage > min_profit_threshold and
            self.confidence_score > Decimal("0.7") and
            self.risk_score < Decimal("0.5")
        )


@dataclass
class TradingAction:
    """Suggested trading action."""
    action_id: str
    exchange: str
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    order_type: str = "limit"  # limit, market, etc.
    priority: int = 1  # Execution priority
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Trade:
    """Executed trade."""
    trade_id: str
    opportunity_id: str
    action_id: str
    exchange: str
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    status: OrderStatus
    timestamp: datetime
    execution_latency_ms: float
    fees: Decimal = Decimal(0)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentStatus:
    """Agent status information."""
    agent_id: str
    agent_type: str
    is_active: bool
    opportunities_detected: int
    trades_executed: int
    total_profit: Decimal
    total_loss: Decimal
    success_rate: Decimal
    last_activity: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics for the arbitrage system."""
    total_opportunities: int
    viable_opportunities: int
    executed_trades: int
    successful_trades: int
    failed_trades: int
    total_profit: Decimal
    total_loss: Decimal
    net_profit: Decimal
    average_profit_per_trade: Decimal
    average_detection_latency_ms: float
    average_execution_latency_ms: float
    success_rate: Decimal
    sharpe_ratio: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
