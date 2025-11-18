"""
Market research agent for analyzing market conditions and trends.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from collections import deque
import numpy as np

from .base_agent import BaseAgent
from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    MarketType
)
from ..algorithms.market_microstructure import MicrostructureAnalyzer


class MarketResearchAgent(BaseAgent):
    """Agent specialized in market research and analysis."""

    def __init__(self, agent_id: str = "market_research_agent", config: dict = None):
        """
        Initialize market research agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="MarketResearchAgent",
            supported_arbitrage_types=[],  # Doesn't detect arbitrage directly
            supported_market_types=list(MarketType),
            config=config
        )

        # Initialize microstructure analyzer
        self.microstructure_analyzer = MicrostructureAnalyzer(config)

        # Market condition tracking
        self.market_conditions: Dict[str, Dict] = {}
        self.trend_analysis: Dict[str, Dict] = {}

        # Historical data for analysis
        self.price_history: Dict[str, deque] = {}
        self.volume_history: Dict[str, deque] = {}
        self.max_history = config.get("max_history", 100) if config else 100

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(f"{self.agent_type} started - monitoring market conditions")

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data for research purposes.

        Args:
            market_data: List of market data snapshots

        Returns:
            Empty list (research agent doesn't detect opportunities directly)
        """
        # Update historical data
        self._update_history(market_data)

        # Analyze market conditions for each symbol
        for data in market_data:
            key = f"{data.exchange}:{data.symbol}"

            # Perform various analyses
            quality = self.microstructure_analyzer.calculate_market_quality_score(data)
            trend = self._analyze_trend(data)
            volatility = self._analyze_volatility(data)
            liquidity = self._analyze_liquidity(data)

            # Store market conditions
            self.market_conditions[key] = {
                "timestamp": datetime.now(),
                "symbol": data.symbol,
                "exchange": data.exchange,
                "market_type": data.market_type.value,
                "quality": quality,
                "trend": trend,
                "volatility": volatility,
                "liquidity": liquidity,
                "price": float(data.mid_price),
                "spread_pct": float(data.spread_percentage)
            }

        # Detect market regime changes
        await self._detect_regime_changes(market_data)

        return []

    def _update_history(self, market_data: List[MarketData]):
        """Update historical price and volume data."""
        for data in market_data:
            key = f"{data.exchange}:{data.symbol}"

            if key not in self.price_history:
                self.price_history[key] = deque(maxlen=self.max_history)
                self.volume_history[key] = deque(maxlen=self.max_history)

            self.price_history[key].append({
                "timestamp": data.timestamp,
                "price": float(data.mid_price)
            })

            self.volume_history[key].append({
                "timestamp": data.timestamp,
                "volume": float(data.bid_volume + data.ask_volume)
            })

    def _analyze_trend(self, market_data: MarketData) -> Dict:
        """Analyze price trend."""
        key = f"{market_data.exchange}:{market_data.symbol}"

        if key not in self.price_history or len(self.price_history[key]) < 5:
            return {
                "direction": "unknown",
                "strength": 0.0,
                "duration": 0
            }

        prices = [p["price"] for p in self.price_history[key]]

        # Calculate trend using linear regression
        x = np.arange(len(prices))
        slope, intercept = np.polyfit(x, prices, 1)

        # Normalize slope by price level
        avg_price = np.mean(prices)
        normalized_slope = slope / avg_price if avg_price > 0 else 0

        # Determine direction and strength
        if normalized_slope > 0.001:
            direction = "uptrend"
            strength = min(abs(normalized_slope) * 100, 1.0)
        elif normalized_slope < -0.001:
            direction = "downtrend"
            strength = min(abs(normalized_slope) * 100, 1.0)
        else:
            direction = "sideways"
            strength = 0.0

        # Calculate R-squared for trend confidence
        y_pred = slope * x + intercept
        ss_res = np.sum((prices - y_pred) ** 2)
        ss_tot = np.sum((prices - np.mean(prices)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return {
            "direction": direction,
            "strength": float(strength),
            "slope": float(slope),
            "r_squared": float(r_squared),
            "confidence": float(min(strength * r_squared, 1.0))
        }

    def _analyze_volatility(self, market_data: MarketData) -> Dict:
        """Analyze price volatility."""
        key = f"{market_data.exchange}:{market_data.symbol}"

        if key not in self.price_history or len(self.price_history[key]) < 10:
            return {
                "level": "unknown",
                "value": 0.0,
                "percentile": 0.0
            }

        prices = np.array([p["price"] for p in self.price_history[key]])

        # Calculate returns
        returns = np.diff(prices) / prices[:-1]

        # Calculate volatility (standard deviation of returns)
        volatility = np.std(returns)

        # Annualized volatility (assuming minute data)
        # Simplified: vol * sqrt(252 * 24 * 60)
        annual_volatility = volatility * np.sqrt(252 * 24 * 60)

        # Classify volatility level
        if annual_volatility < 0.2:
            level = "low"
        elif annual_volatility < 0.5:
            level = "moderate"
        elif annual_volatility < 1.0:
            level = "high"
        else:
            level = "extreme"

        # Calculate historical percentile
        historical_vols = []
        window = 10
        for i in range(len(prices) - window):
            window_prices = prices[i:i+window]
            window_returns = np.diff(window_prices) / window_prices[:-1]
            historical_vols.append(np.std(window_returns))

        if historical_vols:
            percentile = np.percentile(historical_vols, 50)
        else:
            percentile = 0.0

        return {
            "level": level,
            "value": float(volatility),
            "annual_volatility": float(annual_volatility),
            "percentile": float(percentile)
        }

    def _analyze_liquidity(self, market_data: MarketData) -> Dict:
        """Analyze market liquidity."""
        key = f"{market_data.exchange}:{market_data.symbol}"

        # Current liquidity metrics
        total_volume = market_data.bid_volume + market_data.ask_volume
        volume_imbalance = abs(market_data.bid_volume - market_data.ask_volume)

        # Historical average volume
        if key in self.volume_history and len(self.volume_history[key]) > 5:
            volumes = [v["volume"] for v in self.volume_history[key]]
            avg_volume = np.mean(volumes)
            volume_trend = (volumes[-1] - volumes[0]) / volumes[0] if volumes[0] > 0 else 0
        else:
            avg_volume = float(total_volume)
            volume_trend = 0.0

        # Classify liquidity
        if total_volume > avg_volume * 1.5:
            level = "high"
        elif total_volume > avg_volume * 0.5:
            level = "moderate"
        else:
            level = "low"

        # Calculate liquidity score (0-1)
        spread_score = max(0, 1 - float(market_data.spread_percentage) / 2)
        volume_score = min(float(total_volume) / (avg_volume * 2), 1.0) if avg_volume > 0 else 0
        balance_score = 1 - min(volume_imbalance / total_volume, 1.0) if total_volume > 0 else 0

        liquidity_score = (spread_score + volume_score + balance_score) / 3

        return {
            "level": level,
            "score": liquidity_score,
            "total_volume": float(total_volume),
            "avg_volume": float(avg_volume),
            "volume_trend": float(volume_trend),
            "spread_pct": float(market_data.spread_percentage)
        }

    async def _detect_regime_changes(self, market_data: List[MarketData]):
        """Detect market regime changes."""
        for data in market_data:
            key = f"{data.exchange}:{data.symbol}"

            if key not in self.market_conditions:
                continue

            current_condition = self.market_conditions[key]

            # Check for significant changes
            changes = []

            # Volatility regime change
            if current_condition["volatility"]["level"] in ["high", "extreme"]:
                changes.append("high_volatility_regime")

            # Liquidity regime change
            if current_condition["liquidity"]["level"] == "low":
                changes.append("low_liquidity_regime")

            # Strong trend
            if current_condition["trend"]["strength"] > 0.7:
                changes.append(f"strong_{current_condition['trend']['direction']}")

            if changes:
                self.logger.info(
                    f"Regime change detected for {data.symbol}: {', '.join(changes)}"
                )

    def get_market_report(self, symbol: str = None, exchange: str = None) -> Dict:
        """
        Get market research report.

        Args:
            symbol: Filter by symbol (optional)
            exchange: Filter by exchange (optional)

        Returns:
            Market report
        """
        filtered_conditions = {}

        for key, condition in self.market_conditions.items():
            if symbol and condition["symbol"] != symbol:
                continue
            if exchange and condition["exchange"] != exchange:
                continue

            filtered_conditions[key] = condition

        # Aggregate statistics
        if filtered_conditions:
            avg_quality = np.mean([
                c["quality"]["overall_quality"]
                for c in filtered_conditions.values()
            ])

            volatility_distribution = {}
            for c in filtered_conditions.values():
                level = c["volatility"]["level"]
                volatility_distribution[level] = volatility_distribution.get(level, 0) + 1

            liquidity_distribution = {}
            for c in filtered_conditions.values():
                level = c["liquidity"]["level"]
                liquidity_distribution[level] = liquidity_distribution.get(level, 0) + 1

        else:
            avg_quality = 0
            volatility_distribution = {}
            liquidity_distribution = {}

        return {
            "timestamp": datetime.now().isoformat(),
            "markets_analyzed": len(filtered_conditions),
            "average_market_quality": float(avg_quality),
            "volatility_distribution": volatility_distribution,
            "liquidity_distribution": liquidity_distribution,
            "detailed_conditions": filtered_conditions
        }

    def get_trading_signals(self) -> List[Dict]:
        """
        Get trading signals based on market research.

        Returns:
            List of trading signals
        """
        signals = []

        for key, condition in self.market_conditions.items():
            # Signal: Strong trend with good quality
            if (condition["trend"]["strength"] > 0.6 and
                condition["quality"]["overall_quality"] > 0.7):

                signals.append({
                    "symbol": condition["symbol"],
                    "exchange": condition["exchange"],
                    "signal_type": "trend_following",
                    "direction": condition["trend"]["direction"],
                    "strength": condition["trend"]["strength"],
                    "confidence": condition["trend"]["confidence"],
                    "timestamp": condition["timestamp"].isoformat()
                })

            # Signal: Mean reversion opportunity (high volatility, good liquidity)
            if (condition["volatility"]["level"] in ["moderate", "high"] and
                condition["liquidity"]["score"] > 0.6 and
                condition["quality"]["overall_quality"] > 0.5):

                signals.append({
                    "symbol": condition["symbol"],
                    "exchange": condition["exchange"],
                    "signal_type": "mean_reversion",
                    "volatility": condition["volatility"]["value"],
                    "liquidity_score": condition["liquidity"]["score"],
                    "confidence": 0.6,
                    "timestamp": condition["timestamp"].isoformat()
                })

            # Signal: Liquidity opportunity
            if (condition["liquidity"]["level"] == "high" and
                condition["quality"]["spread_score"] > 0.8):

                signals.append({
                    "symbol": condition["symbol"],
                    "exchange": condition["exchange"],
                    "signal_type": "liquidity_opportunity",
                    "liquidity_score": condition["liquidity"]["score"],
                    "spread_score": condition["quality"]["spread_score"],
                    "confidence": 0.7,
                    "timestamp": condition["timestamp"].isoformat()
                })

        return signals
