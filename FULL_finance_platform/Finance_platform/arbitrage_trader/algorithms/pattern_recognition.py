"""
Advanced pattern recognition algorithms for detecting trading patterns.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import numpy as np
from scipy import signal
import uuid

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class PatternRecognizer:
    """Recognizes various trading patterns and chart formations."""

    def __init__(self, config: dict = None):
        """
        Initialize pattern recognizer.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}
        self.min_confidence = Decimal(self.config.get("min_confidence", "0.6"))

    def detect_all_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect all patterns in historical data.

        Args:
            historical_data: Historical market data

        Returns:
            List of detected patterns
        """
        if len(historical_data) < 10:
            return []

        patterns = []

        # Price patterns
        patterns.extend(self.detect_chart_patterns(historical_data))

        # Candlestick patterns (simplified using high/low)
        patterns.extend(self.detect_candlestick_patterns(historical_data))

        # Volume patterns
        patterns.extend(self.detect_volume_patterns(historical_data))

        # Breakout patterns
        patterns.extend(self.detect_breakout_patterns(historical_data))

        # Convergence/Divergence patterns
        patterns.extend(self.detect_convergence_patterns(historical_data))

        return patterns

    def detect_chart_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect chart patterns (head and shoulders, double top/bottom, etc.).

        Args:
            historical_data: Historical market data

        Returns:
            List of detected chart patterns
        """
        if len(historical_data) < 15:
            return []

        patterns = []
        prices = [float(d.mid_price) for d in historical_data]

        # Detect local extrema
        maxima_indices = signal.argrelextrema(np.array(prices), np.greater, order=3)[0]
        minima_indices = signal.argrelextrema(np.array(prices), np.less, order=3)[0]

        # Double Top Pattern
        if len(maxima_indices) >= 2:
            for i in range(len(maxima_indices) - 1):
                idx1 = maxima_indices[i]
                idx2 = maxima_indices[i + 1]

                price1 = prices[idx1]
                price2 = prices[idx2]

                # Check if peaks are similar (within 2%)
                if abs(price1 - price2) / price1 < 0.02:
                    patterns.append({
                        "pattern": "double_top",
                        "type": "reversal",
                        "signal": "bearish",
                        "confidence": 0.75,
                        "peak1_price": price1,
                        "peak2_price": price2,
                        "peak1_index": idx1,
                        "peak2_index": idx2,
                        "description": "Two similar peaks suggesting resistance and potential downtrend"
                    })

        # Double Bottom Pattern
        if len(minima_indices) >= 2:
            for i in range(len(minima_indices) - 1):
                idx1 = minima_indices[i]
                idx2 = minima_indices[i + 1]

                price1 = prices[idx1]
                price2 = prices[idx2]

                if abs(price1 - price2) / price1 < 0.02:
                    patterns.append({
                        "pattern": "double_bottom",
                        "type": "reversal",
                        "signal": "bullish",
                        "confidence": 0.75,
                        "trough1_price": price1,
                        "trough2_price": price2,
                        "trough1_index": idx1,
                        "trough2_index": idx2,
                        "description": "Two similar troughs suggesting support and potential uptrend"
                    })

        # Head and Shoulders
        if len(maxima_indices) >= 3:
            for i in range(len(maxima_indices) - 2):
                idx1 = maxima_indices[i]
                idx2 = maxima_indices[i + 1]
                idx3 = maxima_indices[i + 2]

                price1 = prices[idx1]
                price2 = prices[idx2]
                price3 = prices[idx3]

                # Head should be higher than shoulders
                if (price2 > price1 * 1.02 and price2 > price3 * 1.02 and
                    abs(price1 - price3) / price1 < 0.03):

                    patterns.append({
                        "pattern": "head_and_shoulders",
                        "type": "reversal",
                        "signal": "bearish",
                        "confidence": 0.80,
                        "left_shoulder": price1,
                        "head": price2,
                        "right_shoulder": price3,
                        "description": "Classic reversal pattern indicating potential downtrend"
                    })

        # Inverse Head and Shoulders
        if len(minima_indices) >= 3:
            for i in range(len(minima_indices) - 2):
                idx1 = minima_indices[i]
                idx2 = minima_indices[i + 1]
                idx3 = minima_indices[i + 2]

                price1 = prices[idx1]
                price2 = prices[idx2]
                price3 = prices[idx3]

                # Head should be lower than shoulders
                if (price2 < price1 * 0.98 and price2 < price3 * 0.98 and
                    abs(price1 - price3) / price1 < 0.03):

                    patterns.append({
                        "pattern": "inverse_head_and_shoulders",
                        "type": "reversal",
                        "signal": "bullish",
                        "confidence": 0.80,
                        "left_shoulder": price1,
                        "head": price2,
                        "right_shoulder": price3,
                        "description": "Classic reversal pattern indicating potential uptrend"
                    })

        # Triangle patterns
        triangle = self._detect_triangle(prices)
        if triangle:
            patterns.append(triangle)

        return patterns

    def _detect_triangle(self, prices: List[float]) -> Optional[Dict]:
        """Detect triangle consolidation patterns."""
        if len(prices) < 20:
            return None

        # Calculate highs and lows over time
        window = 5
        highs = [max(prices[i:i+window]) for i in range(len(prices) - window)]
        lows = [min(prices[i:i+window]) for i in range(len(prices) - window)]

        # Fit trend lines
        x = np.arange(len(highs))
        high_slope = np.polyfit(x, highs, 1)[0]
        low_slope = np.polyfit(x, lows, 1)[0]

        # Ascending triangle: flat top, rising bottom
        if abs(high_slope) < 0.001 and low_slope > 0.001:
            return {
                "pattern": "ascending_triangle",
                "type": "continuation",
                "signal": "bullish",
                "confidence": 0.70,
                "description": "Consolidation pattern with rising support, typically breaks upward"
            }

        # Descending triangle: falling top, flat bottom
        elif high_slope < -0.001 and abs(low_slope) < 0.001:
            return {
                "pattern": "descending_triangle",
                "type": "continuation",
                "signal": "bearish",
                "confidence": 0.70,
                "description": "Consolidation pattern with falling resistance, typically breaks downward"
            }

        # Symmetrical triangle: converging lines
        elif high_slope < -0.001 and low_slope > 0.001:
            return {
                "pattern": "symmetrical_triangle",
                "type": "continuation",
                "signal": "neutral",
                "confidence": 0.65,
                "description": "Consolidation pattern, breakout direction uncertain"
            }

        return None

    def detect_candlestick_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect candlestick patterns.

        Simplified version using bid/ask as proxies for open/close.

        Args:
            historical_data: Historical market data

        Returns:
            List of detected candlestick patterns
        """
        patterns = []

        if len(historical_data) < 3:
            return patterns

        # Get last few candles
        recent = historical_data[-3:]

        # Bullish Engulfing
        if len(recent) >= 2:
            prev = recent[-2]
            curr = recent[-1]

            prev_body = abs(prev.ask_price - prev.bid_price)
            curr_body = abs(curr.ask_price - curr.bid_price)

            # Current candle engulfs previous
            if (curr.bid_price < prev.bid_price and
                curr.ask_price > prev.ask_price and
                curr_body > prev_body * 1.5):

                patterns.append({
                    "pattern": "bullish_engulfing",
                    "type": "reversal",
                    "signal": "bullish",
                    "confidence": 0.70,
                    "description": "Strong bullish reversal signal"
                })

        # Morning Star (simplified)
        if len(recent) >= 3:
            first = recent[-3]
            middle = recent[-2]
            last = recent[-1]

            first_mid = first.mid_price
            middle_mid = middle.mid_price
            last_mid = last.mid_price

            # Down, small body, up
            if (first_mid > middle_mid and
                last_mid > middle_mid and
                last_mid > first_mid * 0.99):

                patterns.append({
                    "pattern": "morning_star",
                    "type": "reversal",
                    "signal": "bullish",
                    "confidence": 0.75,
                    "description": "Three-candle bullish reversal pattern"
                })

        return patterns

    def detect_volume_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect volume-based patterns.

        Args:
            historical_data: Historical market data

        Returns:
            List of detected volume patterns
        """
        patterns = []

        if len(historical_data) < 10:
            return patterns

        volumes = [float(d.bid_volume + d.ask_volume) for d in historical_data]
        prices = [float(d.mid_price) for d in historical_data]

        avg_volume = np.mean(volumes)

        # Volume Spike
        if volumes[-1] > avg_volume * 2:
            price_change = (prices[-1] - prices[-2]) / prices[-2] if prices[-2] > 0 else 0

            patterns.append({
                "pattern": "volume_spike",
                "type": "confirmation",
                "signal": "bullish" if price_change > 0 else "bearish",
                "confidence": 0.65,
                "volume_ratio": volumes[-1] / avg_volume,
                "price_change_pct": price_change * 100,
                "description": f"Volume spike with {'upward' if price_change > 0 else 'downward'} price movement"
            })

        # Volume Divergence (price up, volume down = bearish)
        if len(prices) >= 5:
            price_trend = prices[-1] - prices[-5]
            volume_trend = volumes[-1] - np.mean(volumes[-5:-1])

            if price_trend > 0 and volume_trend < 0:
                patterns.append({
                    "pattern": "bearish_divergence",
                    "type": "warning",
                    "signal": "bearish",
                    "confidence": 0.60,
                    "description": "Price rising but volume declining, potential reversal"
                })

            elif price_trend < 0 and volume_trend > 0:
                patterns.append({
                    "pattern": "bullish_divergence",
                    "type": "warning",
                    "signal": "bullish",
                    "confidence": 0.60,
                    "description": "Price falling but volume increasing, potential reversal"
                })

        return patterns

    def detect_breakout_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect breakout patterns.

        Args:
            historical_data: Historical market data

        Returns:
            List of detected breakout patterns
        """
        patterns = []

        if len(historical_data) < 20:
            return patterns

        prices = [float(d.mid_price) for d in historical_data]

        # Recent vs historical
        recent_prices = prices[-5:]
        historical_prices = prices[-20:-5]

        recent_high = max(recent_prices)
        recent_low = min(recent_prices)
        historical_high = max(historical_prices)
        historical_low = min(historical_prices)

        # Upward Breakout
        if recent_high > historical_high * 1.02:
            patterns.append({
                "pattern": "upward_breakout",
                "type": "continuation",
                "signal": "bullish",
                "confidence": 0.75,
                "breakout_price": recent_high,
                "resistance_level": historical_high,
                "breakout_percentage": (recent_high - historical_high) / historical_high * 100,
                "description": "Price broke above resistance, bullish continuation expected"
            })

        # Downward Breakout
        if recent_low < historical_low * 0.98:
            patterns.append({
                "pattern": "downward_breakout",
                "type": "continuation",
                "signal": "bearish",
                "confidence": 0.75,
                "breakout_price": recent_low,
                "support_level": historical_low,
                "breakout_percentage": (historical_low - recent_low) / historical_low * 100,
                "description": "Price broke below support, bearish continuation expected"
            })

        # Range Consolidation
        price_range = max(prices[-10:]) - min(prices[-10:])
        avg_price = np.mean(prices[-10:])
        range_pct = (price_range / avg_price) * 100

        if range_pct < 2:  # Less than 2% range
            patterns.append({
                "pattern": "consolidation",
                "type": "pre_breakout",
                "signal": "neutral",
                "confidence": 0.60,
                "range_percentage": range_pct,
                "description": "Tight consolidation, breakout imminent"
            })

        return patterns

    def detect_convergence_patterns(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect convergence and divergence patterns (MACD-like).

        Args:
            historical_data: Historical market data

        Returns:
            List of detected convergence patterns
        """
        patterns = []

        if len(historical_data) < 26:
            return patterns

        prices = np.array([float(d.mid_price) for d in historical_data])

        # Calculate EMAs (simplified)
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)

        # MACD line
        macd_line = ema_12 - ema_26

        # Signal line (9-period EMA of MACD)
        signal_line = self._calculate_ema(macd_line, 9)

        # Detect crossovers
        if len(macd_line) >= 2 and len(signal_line) >= 2:
            # Bullish crossover
            if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
                patterns.append({
                    "pattern": "macd_bullish_crossover",
                    "type": "momentum",
                    "signal": "bullish",
                    "confidence": 0.70,
                    "macd_value": float(macd_line[-1]),
                    "signal_value": float(signal_line[-1]),
                    "description": "MACD crossed above signal line, bullish momentum"
                })

            # Bearish crossover
            elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
                patterns.append({
                    "pattern": "macd_bearish_crossover",
                    "type": "momentum",
                    "signal": "bearish",
                    "confidence": 0.70,
                    "macd_value": float(macd_line[-1]),
                    "signal_value": float(signal_line[-1]),
                    "description": "MACD crossed below signal line, bearish momentum"
                })

        return patterns

    def _calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average."""
        if len(data) < period:
            return data

        ema = np.zeros_like(data)
        ema[0] = data[0]

        multiplier = 2 / (period + 1)

        for i in range(1, len(data)):
            ema[i] = (data[i] * multiplier) + (ema[i-1] * (1 - multiplier))

        return ema

    def generate_pattern_based_opportunities(
        self,
        historical_data: List[MarketData],
        detected_patterns: List[Dict]
    ) -> List[ArbitrageOpportunity]:
        """
        Generate trading opportunities based on detected patterns.

        Args:
            historical_data: Historical market data
            detected_patterns: Detected patterns

        Returns:
            List of opportunities
        """
        opportunities = []

        if not historical_data or not detected_patterns:
            return opportunities

        current_data = historical_data[-1]

        for pattern in detected_patterns:
            # Only create opportunities for high-confidence patterns
            if pattern.get("confidence", 0) < float(self.min_confidence):
                continue

            # Map signal to order side
            if pattern["signal"] == "bullish":
                side = OrderSide.BUY
                expected_profit_pct = Decimal("1.5")
            elif pattern["signal"] == "bearish":
                side = OrderSide.SELL
                expected_profit_pct = Decimal("1.5")
            else:
                continue  # Skip neutral signals

            # Create opportunity
            opportunity = ArbitrageOpportunity(
                opportunity_id=str(uuid.uuid4()),
                arbitrage_type=ArbitrageType.STATISTICAL,
                market_type=current_data.market_type,
                symbol=current_data.symbol,
                timestamp=datetime.now(),
                expected_profit=expected_profit_pct * Decimal(100),
                expected_profit_percentage=expected_profit_pct,
                confidence_score=Decimal(str(pattern["confidence"])),
                risk_score=Decimal(1) - Decimal(str(pattern["confidence"])),
                detection_latency_ms=0,
                market_data=[current_data],
                suggested_actions=[
                    TradingAction(
                        action_id=str(uuid.uuid4()),
                        exchange=current_data.exchange,
                        symbol=current_data.symbol,
                        side=side,
                        quantity=Decimal(100),
                        price=current_data.ask_price if side == OrderSide.BUY else current_data.bid_price,
                        order_type="limit",
                        priority=1
                    )
                ],
                metadata={
                    "strategy": "pattern_recognition",
                    "pattern": pattern["pattern"],
                    "pattern_type": pattern["type"],
                    "pattern_confidence": pattern["confidence"],
                    "pattern_description": pattern.get("description", "")
                }
            )

            opportunities.append(opportunity)

        return opportunities
