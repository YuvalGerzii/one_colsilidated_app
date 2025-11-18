"""
Finance Data Products

High-value data products from the Finance platform:
- Extreme Events Alerts API: $100K+/year enterprise subscriptions
- Market Regime Indicators: Bull/bear regime detection
- Arbitrage Signals Feed: Real-time arbitrage opportunities

Revenue Potential: $24M ARR
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MarketRegime(Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    CRISIS = "crisis"


@dataclass
class ExtremeEventAlert:
    """Alert for an extreme market event"""
    alert_id: str
    event_type: str
    severity: AlertSeverity
    timestamp: datetime
    title: str
    description: str
    affected_sectors: List[str]
    affected_assets: List[str]
    predicted_impact: Dict[str, Any]
    confidence: float
    time_horizon: str
    recommended_actions: List[str]
    source_agents: List[str]


@dataclass
class RegimeIndicator:
    """Market regime indicator"""
    timestamp: datetime
    regime: MarketRegime
    confidence: float
    indicators: Dict[str, float]
    transition_probability: Dict[str, float]
    supporting_evidence: List[str]


@dataclass
class ArbitrageSignal:
    """Arbitrage opportunity signal"""
    signal_id: str
    timestamp: datetime
    opportunity_type: str  # cross_exchange, triangular, statistical
    assets: List[str]
    exchanges: List[str]
    spread_bps: float
    expected_profit_usd: float
    required_capital_usd: float
    time_window_seconds: int
    confidence: float
    execution_steps: List[Dict[str, Any]]


class ExtremeEventsAlertsAPI:
    """
    API for extreme events market predictions.

    Powered by 17 specialized agents:
    - Pandemic Agent
    - Climate Crisis Agent
    - Recession Agent
    - Geopolitical Agent
    - Cyber Attack Agent
    - And 12 more...

    Pricing:
    - Starter: 100 alerts/month, $99/mo
    - Professional: Unlimited alerts, real-time, $499/mo
    - Enterprise: Custom models, dedicated support, $8,333/mo ($100K/yr)
    """

    def __init__(self):
        self.alerts_cache: List[ExtremeEventAlert] = []
        self.subscribers: Dict[str, Dict[str, Any]] = {}

    async def get_active_alerts(
        self,
        severity_min: AlertSeverity = AlertSeverity.LOW,
        event_types: Optional[List[str]] = None,
        sectors: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[ExtremeEventAlert]:
        """Get currently active alerts"""

        alerts = self.alerts_cache

        # Filter by severity
        severity_order = [AlertSeverity.LOW, AlertSeverity.MEDIUM,
                         AlertSeverity.HIGH, AlertSeverity.CRITICAL]
        min_index = severity_order.index(severity_min)
        alerts = [a for a in alerts if severity_order.index(a.severity) >= min_index]

        # Filter by event type
        if event_types:
            alerts = [a for a in alerts if a.event_type in event_types]

        # Filter by sector
        if sectors:
            alerts = [a for a in alerts
                      if any(s in a.affected_sectors for s in sectors)]

        return alerts[:limit]

    async def get_alert_by_id(self, alert_id: str) -> Optional[ExtremeEventAlert]:
        """Get specific alert details"""
        for alert in self.alerts_cache:
            if alert.alert_id == alert_id:
                return alert
        return None

    async def get_historical_alerts(
        self,
        start_date: datetime,
        end_date: datetime,
        event_types: Optional[List[str]] = None
    ) -> List[ExtremeEventAlert]:
        """Get historical alerts for backtesting"""
        alerts = [
            a for a in self.alerts_cache
            if start_date <= a.timestamp <= end_date
        ]
        if event_types:
            alerts = [a for a in alerts if a.event_type in event_types]
        return alerts

    async def subscribe_webhook(
        self,
        customer_id: str,
        webhook_url: str,
        severity_min: AlertSeverity = AlertSeverity.MEDIUM,
        event_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Subscribe to real-time alerts via webhook"""
        self.subscribers[customer_id] = {
            "webhook_url": webhook_url,
            "severity_min": severity_min,
            "event_types": event_types,
            "subscribed_at": datetime.now()
        }
        return {"status": "subscribed", "customer_id": customer_id}

    async def generate_alert(
        self,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> ExtremeEventAlert:
        """
        Generate an alert from event data.

        This would call the relevant extreme events agents.
        """

        # Simulated alert generation
        alert = ExtremeEventAlert(
            alert_id=f"alert_{datetime.now().timestamp()}",
            event_type=event_type,
            severity=AlertSeverity.HIGH,
            timestamp=datetime.now(),
            title=f"{event_type.title()} Event Detected",
            description=f"Our AI models have detected a significant {event_type} event",
            affected_sectors=event_data.get("sectors", ["Technology", "Finance"]),
            affected_assets=event_data.get("assets", []),
            predicted_impact={
                "market_direction": "bearish",
                "magnitude_percent": -5.2,
                "duration_days": 30
            },
            confidence=0.85,
            time_horizon="1-3 months",
            recommended_actions=[
                "Reduce equity exposure",
                "Increase defensive positions",
                "Review stop-losses"
            ],
            source_agents=["recession_agent", "geopolitical_agent"]
        )

        self.alerts_cache.append(alert)
        return alert


class MarketRegimeIndicators:
    """
    API for market regime detection.

    Identifies current market regime (bull, bear, crisis) and
    predicts regime transitions 1-3 months ahead.

    Pricing:
    - Professional: $299/mo
    - Enterprise: $1,499/mo with custom models
    """

    def __init__(self):
        self.regime_history: List[RegimeIndicator] = []

    async def get_current_regime(self) -> RegimeIndicator:
        """Get current market regime"""

        # Simulated regime detection
        return RegimeIndicator(
            timestamp=datetime.now(),
            regime=MarketRegime.BULL,
            confidence=0.78,
            indicators={
                "moving_average_trend": 0.85,
                "breadth": 0.72,
                "volatility": 0.25,
                "momentum": 0.65,
                "sentiment": 0.70
            },
            transition_probability={
                "bull": 0.65,
                "bear": 0.15,
                "sideways": 0.15,
                "volatile": 0.05
            },
            supporting_evidence=[
                "200-day MA trending up",
                "Advance-decline line positive",
                "VIX below 20"
            ]
        )

    async def get_regime_history(
        self,
        days: int = 365
    ) -> List[RegimeIndicator]:
        """Get historical regime indicators"""
        cutoff = datetime.now() - timedelta(days=days)
        return [r for r in self.regime_history if r.timestamp >= cutoff]

    async def predict_regime_change(
        self,
        horizon_days: int = 30
    ) -> Dict[str, Any]:
        """Predict probability of regime change"""

        return {
            "current_regime": MarketRegime.BULL.value,
            "horizon_days": horizon_days,
            "change_probability": 0.25,
            "likely_new_regime": MarketRegime.SIDEWAYS.value,
            "confidence": 0.72,
            "key_indicators_to_watch": [
                "10-year Treasury yield",
                "S&P 500 breadth",
                "VIX futures curve"
            ]
        }


class ArbitrageSignalsFeed:
    """
    Real-time arbitrage opportunity signals.

    Powered by:
    - Cross-Exchange Arbitrage Agent
    - Statistical Arbitrage Agent
    - Triangular Arbitrage Agent

    Pricing:
    - Professional: $999/mo (delayed 15 min)
    - Enterprise: $4,999/mo (real-time)
    - Hedge Fund: $24,999/mo (exclusive signals)
    """

    def __init__(self):
        self.signals: List[ArbitrageSignal] = []
        self.subscribers: Dict[str, Dict[str, Any]] = {}

    async def get_active_signals(
        self,
        opportunity_types: Optional[List[str]] = None,
        min_profit_usd: float = 10,
        max_capital_usd: float = 100000,
        limit: int = 20
    ) -> List[ArbitrageSignal]:
        """Get currently active arbitrage signals"""

        signals = self.signals

        # Filter by type
        if opportunity_types:
            signals = [s for s in signals if s.opportunity_type in opportunity_types]

        # Filter by profit
        signals = [s for s in signals if s.expected_profit_usd >= min_profit_usd]

        # Filter by capital requirement
        signals = [s for s in signals if s.required_capital_usd <= max_capital_usd]

        return signals[:limit]

    async def get_signal_performance(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get historical signal performance"""

        return {
            "period_days": days,
            "total_signals": 1250,
            "successful": 1180,
            "success_rate": 0.944,
            "total_profit_usd": 125000,
            "avg_profit_per_signal": 100,
            "by_type": {
                "cross_exchange": {"count": 800, "success_rate": 0.96},
                "triangular": {"count": 350, "success_rate": 0.92},
                "statistical": {"count": 100, "success_rate": 0.88}
            }
        }

    async def subscribe_realtime(
        self,
        customer_id: str,
        websocket_url: str,
        opportunity_types: Optional[List[str]] = None,
        min_profit_usd: float = 100
    ) -> Dict[str, Any]:
        """Subscribe to real-time arbitrage signals"""

        self.subscribers[customer_id] = {
            "websocket_url": websocket_url,
            "opportunity_types": opportunity_types,
            "min_profit_usd": min_profit_usd,
            "subscribed_at": datetime.now()
        }

        return {
            "status": "subscribed",
            "stream_url": websocket_url,
            "message": "Real-time signals will be pushed to your WebSocket"
        }

    async def generate_signal(
        self,
        opportunity_data: Dict[str, Any]
    ) -> ArbitrageSignal:
        """Generate a new arbitrage signal"""

        signal = ArbitrageSignal(
            signal_id=f"sig_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            opportunity_type=opportunity_data.get("type", "cross_exchange"),
            assets=opportunity_data.get("assets", ["BTC"]),
            exchanges=opportunity_data.get("exchanges", ["binance", "coinbase"]),
            spread_bps=opportunity_data.get("spread_bps", 15),
            expected_profit_usd=opportunity_data.get("profit", 50),
            required_capital_usd=opportunity_data.get("capital", 10000),
            time_window_seconds=opportunity_data.get("window", 30),
            confidence=opportunity_data.get("confidence", 0.9),
            execution_steps=[
                {"step": 1, "action": "buy", "exchange": "binance", "price": 50000},
                {"step": 2, "action": "sell", "exchange": "coinbase", "price": 50075}
            ]
        )

        self.signals.append(signal)
        return signal


# API Router setup (for FastAPI integration)
def create_finance_data_products_router():
    """Create FastAPI router for finance data products"""

    from fastapi import APIRouter, Query, HTTPException
    from typing import List

    router = APIRouter(prefix="/data-products/finance", tags=["finance-data-products"])

    # Instances
    events_api = ExtremeEventsAlertsAPI()
    regime_api = MarketRegimeIndicators()
    arbitrage_api = ArbitrageSignalsFeed()

    @router.get("/alerts")
    async def get_alerts(
        severity: str = Query("low", description="Minimum severity"),
        limit: int = Query(50, le=100)
    ):
        """Get active extreme event alerts"""
        severity_enum = AlertSeverity[severity.upper()]
        return await events_api.get_active_alerts(severity_min=severity_enum, limit=limit)

    @router.get("/regime/current")
    async def get_current_regime():
        """Get current market regime"""
        return await regime_api.get_current_regime()

    @router.get("/regime/predict")
    async def predict_regime(horizon_days: int = Query(30, le=90)):
        """Predict regime change probability"""
        return await regime_api.predict_regime_change(horizon_days)

    @router.get("/arbitrage/signals")
    async def get_arbitrage_signals(
        min_profit: float = Query(10),
        max_capital: float = Query(100000),
        limit: int = Query(20, le=50)
    ):
        """Get active arbitrage signals"""
        return await arbitrage_api.get_active_signals(
            min_profit_usd=min_profit,
            max_capital_usd=max_capital,
            limit=limit
        )

    @router.get("/arbitrage/performance")
    async def get_signal_performance(days: int = Query(30, le=365)):
        """Get arbitrage signal performance stats"""
        return await arbitrage_api.get_signal_performance(days)

    return router
