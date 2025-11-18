"""
Sentiment analysis agent for analyzing market sentiment.
Uses various indicators to gauge market mood and sentiment.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
from collections import deque
import numpy as np

from .base_agent import BaseAgent
from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    MarketType
)


class SentimentAnalysisAgent(BaseAgent):
    """Agent specialized in market sentiment analysis."""

    def __init__(self, agent_id: str = "sentiment_analysis_agent", config: dict = None):
        """
        Initialize sentiment analysis agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="SentimentAnalysisAgent",
            supported_arbitrage_types=[],  # Research agent
            supported_market_types=list(MarketType),
            config=config
        )

        # Sentiment tracking
        self.sentiment_scores: Dict[str, Dict] = {}
        self.sentiment_history: Dict[str, deque] = {}
        self.max_history = config.get("max_history", 50) if config else 50

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(f"{self.agent_type} started - analyzing market sentiment")

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data for sentiment signals.

        Args:
            market_data: List of market data snapshots

        Returns:
            Empty list (sentiment agent provides context, not opportunities)
        """
        for data in market_data:
            sentiment = self._calculate_sentiment(data)

            key = f"{data.exchange}:{data.symbol}"

            # Store current sentiment
            self.sentiment_scores[key] = sentiment

            # Update history
            if key not in self.sentiment_history:
                self.sentiment_history[key] = deque(maxlen=self.max_history)

            self.sentiment_history[key].append({
                "timestamp": datetime.now(),
                "sentiment_score": sentiment["score"],
                "sentiment_class": sentiment["classification"]
            })

        return []

    def _calculate_sentiment(self, market_data: MarketData) -> Dict:
        """
        Calculate market sentiment from market data.

        Uses multiple indicators:
        - Volume imbalance (bid vs ask)
        - Spread dynamics
        - Price momentum
        - Liquidity

        Args:
            market_data: Market data

        Returns:
            Sentiment analysis
        """
        sentiment_signals = []

        # 1. Volume Imbalance Signal
        total_volume = market_data.bid_volume + market_data.ask_volume
        if total_volume > 0:
            imbalance = (market_data.bid_volume - market_data.ask_volume) / total_volume
            volume_sentiment = float(imbalance) * 0.5  # Scale to contribution

            sentiment_signals.append({
                "indicator": "volume_imbalance",
                "value": float(imbalance),
                "sentiment": volume_sentiment,
                "weight": 0.3
            })
        else:
            sentiment_signals.append({
                "indicator": "volume_imbalance",
                "value": 0,
                "sentiment": 0,
                "weight": 0.3
            })

        # 2. Spread Signal (widening spread = fear, tightening = confidence)
        key = f"{market_data.exchange}:{market_data.symbol}"
        if key in self.sentiment_history and len(self.sentiment_history[key]) > 1:
            # Compare current spread to recent average
            # Note: We're storing sentiment history, not spread history
            # In production, maintain separate spread history
            spread_sentiment = 0  # Placeholder
        else:
            spread_sentiment = 0

        sentiment_signals.append({
            "indicator": "spread_dynamics",
            "value": float(market_data.spread_percentage),
            "sentiment": spread_sentiment,
            "weight": 0.2
        })

        # 3. Liquidity Signal (high liquidity = confidence)
        if total_volume > Decimal(100):
            liquidity_sentiment = 0.5
        elif total_volume > Decimal(50):
            liquidity_sentiment = 0.2
        elif total_volume > Decimal(10):
            liquidity_sentiment = 0
        else:
            liquidity_sentiment = -0.3

        sentiment_signals.append({
            "indicator": "liquidity",
            "value": float(total_volume),
            "sentiment": liquidity_sentiment,
            "weight": 0.2
        })

        # 4. Price Position Signal (near high/low)
        # Simplified - would need historical high/low
        price_position_sentiment = 0

        sentiment_signals.append({
            "indicator": "price_position",
            "value": float(market_data.mid_price),
            "sentiment": price_position_sentiment,
            "weight": 0.15
        })

        # 5. Momentum Signal
        if key in self.sentiment_history and len(self.sentiment_history[key]) > 2:
            # Calculate if sentiment is improving or deteriorating
            recent_sentiments = [h["sentiment_score"] for h in list(self.sentiment_history[key])[-3:]]
            if len(recent_sentiments) == 3:
                momentum = recent_sentiments[-1] - recent_sentiments[0]
                momentum_sentiment = float(np.clip(momentum, -0.5, 0.5))
            else:
                momentum_sentiment = 0
        else:
            momentum_sentiment = 0

        sentiment_signals.append({
            "indicator": "sentiment_momentum",
            "value": momentum_sentiment,
            "sentiment": momentum_sentiment,
            "weight": 0.15
        })

        # Calculate weighted sentiment score
        total_sentiment = sum(
            signal["sentiment"] * signal["weight"]
            for signal in sentiment_signals
        )

        # Normalize to [-1, 1]
        sentiment_score = float(np.clip(total_sentiment, -1.0, 1.0))

        # Classify sentiment
        if sentiment_score > 0.3:
            classification = "bullish"
            confidence = min(sentiment_score, 1.0)
        elif sentiment_score < -0.3:
            classification = "bearish"
            confidence = min(abs(sentiment_score), 1.0)
        else:
            classification = "neutral"
            confidence = 1.0 - abs(sentiment_score)

        return {
            "score": sentiment_score,
            "classification": classification,
            "confidence": confidence,
            "signals": sentiment_signals,
            "timestamp": datetime.now()
        }

    def get_sentiment(
        self,
        symbol: str = None,
        exchange: str = None
    ) -> Dict:
        """
        Get current sentiment analysis.

        Args:
            symbol: Filter by symbol (optional)
            exchange: Filter by exchange (optional)

        Returns:
            Sentiment analysis
        """
        if symbol and exchange:
            key = f"{exchange}:{symbol}"
            if key in self.sentiment_scores:
                return self.sentiment_scores[key]
            else:
                return {"error": "No sentiment data available"}

        # Return all sentiment data
        filtered_sentiments = {}
        for key, sentiment in self.sentiment_scores.items():
            exch, sym = key.split(":")
            if symbol and sym != symbol:
                continue
            if exchange and exch != exchange:
                continue
            filtered_sentiments[key] = sentiment

        return filtered_sentiments

    def get_sentiment_trend(
        self,
        symbol: str,
        exchange: str,
        periods: int = 10
    ) -> Dict:
        """
        Get sentiment trend over time.

        Args:
            symbol: Symbol
            exchange: Exchange
            periods: Number of periods to analyze

        Returns:
            Sentiment trend analysis
        """
        key = f"{exchange}:{symbol}"

        if key not in self.sentiment_history or len(self.sentiment_history[key]) < 2:
            return {
                "error": "Insufficient data for trend analysis",
                "available_periods": 0
            }

        history = list(self.sentiment_history[key])[-periods:]
        scores = [h["sentiment_score"] for h in history]

        # Calculate trend
        x = np.arange(len(scores))
        slope = np.polyfit(x, scores, 1)[0]

        # Determine trend direction
        if slope > 0.01:
            trend = "improving"
        elif slope < -0.01:
            trend = "deteriorating"
        else:
            trend = "stable"

        # Calculate volatility
        volatility = np.std(scores)

        return {
            "symbol": symbol,
            "exchange": exchange,
            "periods_analyzed": len(history),
            "current_score": scores[-1],
            "average_score": float(np.mean(scores)),
            "trend": trend,
            "trend_slope": float(slope),
            "volatility": float(volatility),
            "min_score": float(np.min(scores)),
            "max_score": float(np.max(scores)),
            "history": [
                {
                    "timestamp": h["timestamp"].isoformat(),
                    "score": h["sentiment_score"],
                    "class": h["sentiment_class"]
                }
                for h in history
            ]
        }

    def get_market_mood(self) -> Dict:
        """
        Get overall market mood across all tracked symbols.

        Returns:
            Market mood analysis
        """
        if not self.sentiment_scores:
            return {
                "overall_mood": "unknown",
                "confidence": 0,
                "statistics": {}
            }

        # Aggregate all sentiment scores
        all_scores = [s["score"] for s in self.sentiment_scores.values()]
        all_classifications = [s["classification"] for s in self.sentiment_scores.values()]

        avg_score = np.mean(all_scores)
        median_score = np.median(all_scores)

        # Count classifications
        classification_counts = {
            "bullish": all_classifications.count("bullish"),
            "bearish": all_classifications.count("bearish"),
            "neutral": all_classifications.count("neutral")
        }

        # Determine overall mood
        if avg_score > 0.2:
            overall_mood = "bullish"
            confidence = min(avg_score, 1.0)
        elif avg_score < -0.2:
            overall_mood = "bearish"
            confidence = min(abs(avg_score), 1.0)
        else:
            overall_mood = "neutral"
            confidence = 0.5

        # Calculate consensus strength
        max_count = max(classification_counts.values())
        total_count = len(all_classifications)
        consensus_strength = max_count / total_count if total_count > 0 else 0

        return {
            "overall_mood": overall_mood,
            "average_score": float(avg_score),
            "median_score": float(median_score),
            "confidence": float(confidence),
            "consensus_strength": float(consensus_strength),
            "statistics": {
                "total_symbols": len(self.sentiment_scores),
                "bullish_count": classification_counts["bullish"],
                "bearish_count": classification_counts["bearish"],
                "neutral_count": classification_counts["neutral"],
                "bullish_pct": float(classification_counts["bullish"] / total_count * 100) if total_count > 0 else 0,
                "bearish_pct": float(classification_counts["bearish"] / total_count * 100) if total_count > 0 else 0,
                "neutral_pct": float(classification_counts["neutral"] / total_count * 100) if total_count > 0 else 0
            },
            "timestamp": datetime.now().isoformat()
        }

    def detect_sentiment_extremes(self) -> List[Dict]:
        """
        Detect symbols with extreme sentiment (potential reversals).

        Returns:
            List of extreme sentiment events
        """
        extremes = []

        for key, sentiment in self.sentiment_scores.items():
            exchange, symbol = key.split(":")

            # Extreme bullish (potential top)
            if sentiment["score"] > 0.7:
                extremes.append({
                    "symbol": symbol,
                    "exchange": exchange,
                    "type": "extreme_bullish",
                    "score": sentiment["score"],
                    "warning": "Potential overbought condition",
                    "suggested_action": "Consider taking profits or contrarian short",
                    "timestamp": datetime.now().isoformat()
                })

            # Extreme bearish (potential bottom)
            elif sentiment["score"] < -0.7:
                extremes.append({
                    "symbol": symbol,
                    "exchange": exchange,
                    "type": "extreme_bearish",
                    "score": sentiment["score"],
                    "warning": "Potential oversold condition",
                    "suggested_action": "Consider contrarian long position",
                    "timestamp": datetime.now().isoformat()
                })

        return extremes
