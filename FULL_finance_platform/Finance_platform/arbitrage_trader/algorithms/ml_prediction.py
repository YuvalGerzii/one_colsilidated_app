"""
Machine Learning-based arbitrage opportunity prediction.
Uses pattern recognition and predictive models.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import numpy as np
from collections import deque
import uuid

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType
)


class MLArbitragePr
edictor:
    """ML-based arbitrage opportunity predictor."""

    def __init__(self, config: dict = None):
        """
        Initialize ML predictor.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}

        # Feature storage
        self.feature_history: Dict[str, deque] = {}
        self.max_history = self.config.get("max_history", 100)

        # Model parameters (simplified - in production use sklearn/tensorflow)
        self.lookback_window = self.config.get("lookback_window", 20)
        self.prediction_threshold = Decimal(self.config.get("prediction_threshold", "0.7"))

    def extract_features(
        self,
        market_data: MarketData,
        historical_data: List[MarketData] = None
    ) -> Dict[str, float]:
        """
        Extract features for ML model.

        Args:
            market_data: Current market data
            historical_data: Historical market data

        Returns:
            Feature dictionary
        """
        features = {}

        # Basic features
        features['spread'] = float(market_data.spread)
        features['spread_pct'] = float(market_data.spread_percentage)
        features['bid_price'] = float(market_data.bid_price)
        features['ask_price'] = float(market_data.ask_price)
        features['mid_price'] = float(market_data.mid_price)
        features['bid_volume'] = float(market_data.bid_volume)
        features['ask_volume'] = float(market_data.ask_volume)

        # Volume imbalance
        total_volume = market_data.bid_volume + market_data.ask_volume
        if total_volume > 0:
            features['volume_imbalance'] = float(
                (market_data.bid_volume - market_data.ask_volume) / total_volume
            )
        else:
            features['volume_imbalance'] = 0.0

        # Volume ratio
        if market_data.ask_volume > 0:
            features['volume_ratio'] = float(market_data.bid_volume / market_data.ask_volume)
        else:
            features['volume_ratio'] = 0.0

        # Historical features
        if historical_data and len(historical_data) >= 2:
            prices = [float(d.mid_price) for d in historical_data]

            # Price momentum
            features['price_momentum'] = (prices[-1] - prices[0]) / prices[0] if prices[0] != 0 else 0

            # Volatility
            features['volatility'] = float(np.std(prices))

            # Price acceleration
            if len(prices) >= 3:
                velocity_1 = prices[-1] - prices[-2]
                velocity_2 = prices[-2] - prices[-3]
                features['price_acceleration'] = velocity_1 - velocity_2
            else:
                features['price_acceleration'] = 0.0

            # Trend strength (using simple linear regression slope)
            if len(prices) >= 5:
                x = np.arange(len(prices))
                slope = np.polyfit(x, prices, 1)[0]
                features['trend_strength'] = float(slope / np.mean(prices)) if np.mean(prices) != 0 else 0
            else:
                features['trend_strength'] = 0.0

            # Mean reversion indicator
            mean_price = np.mean(prices)
            if mean_price > 0:
                features['distance_from_mean'] = (prices[-1] - mean_price) / mean_price
            else:
                features['distance_from_mean'] = 0.0

            # Spread dynamics
            spreads = [float(d.spread_percentage) for d in historical_data]
            features['avg_spread'] = np.mean(spreads)
            features['spread_volatility'] = float(np.std(spreads))
            features['spread_trend'] = (spreads[-1] - spreads[0]) / (spreads[0] if spreads[0] != 0 else 1)

        else:
            # No historical data
            features['price_momentum'] = 0.0
            features['volatility'] = 0.0
            features['price_acceleration'] = 0.0
            features['trend_strength'] = 0.0
            features['distance_from_mean'] = 0.0
            features['avg_spread'] = features['spread_pct']
            features['spread_volatility'] = 0.0
            features['spread_trend'] = 0.0

        # Timestamp features (time of day effects)
        hour = market_data.timestamp.hour
        features['hour_sin'] = np.sin(2 * np.pi * hour / 24)
        features['hour_cos'] = np.cos(2 * np.pi * hour / 24)

        # Day of week
        day = market_data.timestamp.weekday()
        features['day_sin'] = np.sin(2 * np.pi * day / 7)
        features['day_cos'] = np.cos(2 * np.pi * day / 7)

        return features

    def predict_arbitrage_probability(
        self,
        features: Dict[str, float]
    ) -> Tuple[Decimal, Dict]:
        """
        Predict probability of profitable arbitrage.

        In production, this would use a trained model (sklearn, tensorflow, etc.)
        For now, using a simplified rule-based scoring system.

        Args:
            features: Feature dictionary

        Returns:
            Tuple of (probability, explanation)
        """
        score = Decimal(0)
        explanation = {}

        # Spread factor (tighter spreads = higher probability)
        if features['spread_pct'] < 0.1:
            spread_score = Decimal("0.2")
        elif features['spread_pct'] < 0.5:
            spread_score = Decimal("0.1")
        else:
            spread_score = Decimal("0.0")
        score += spread_score
        explanation['spread_contribution'] = float(spread_score)

        # Volume imbalance factor
        imbalance = abs(features['volume_imbalance'])
        if imbalance > 0.3:
            imbalance_score = Decimal(str(min(imbalance, 0.5) * 0.4))
            score += imbalance_score
            explanation['imbalance_contribution'] = float(imbalance_score)
        else:
            explanation['imbalance_contribution'] = 0.0

        # Volatility factor (moderate volatility = opportunities)
        volatility = features['volatility']
        if 0.01 < volatility < 0.05:
            volatility_score = Decimal("0.2")
        elif volatility >= 0.05:
            volatility_score = Decimal("0.1")
        else:
            volatility_score = Decimal("0.0")
        score += volatility_score
        explanation['volatility_contribution'] = float(volatility_score)

        # Mean reversion factor
        distance = abs(features['distance_from_mean'])
        if distance > 0.02:  # More than 2% from mean
            reversion_score = Decimal(str(min(distance, 0.1) * 2))
            score += reversion_score
            explanation['reversion_contribution'] = float(reversion_score)
        else:
            explanation['reversion_contribution'] = 0.0

        # Momentum factor
        momentum = abs(features['price_momentum'])
        if momentum > 0.01:
            momentum_score = Decimal(str(min(momentum, 0.05) * 2))
            score += momentum_score
            explanation['momentum_contribution'] = float(momentum_score)
        else:
            explanation['momentum_contribution'] = 0.0

        # Normalize score to [0, 1]
        probability = min(score, Decimal(1))

        explanation['final_probability'] = float(probability)

        return probability, explanation

    def predict_price_direction(
        self,
        features: Dict[str, float]
    ) -> Tuple[str, Decimal]:
        """
        Predict price direction and confidence.

        Args:
            features: Feature dictionary

        Returns:
            Tuple of (direction, confidence)
        """
        # Aggregate directional signals
        direction_score = Decimal(0)

        # Volume imbalance signal
        if features['volume_imbalance'] > 0.2:
            direction_score += Decimal("0.3")
        elif features['volume_imbalance'] < -0.2:
            direction_score -= Decimal("0.3")

        # Momentum signal
        if features['price_momentum'] > 0.01:
            direction_score += Decimal("0.2")
        elif features['price_momentum'] < -0.01:
            direction_score -= Decimal("0.2")

        # Acceleration signal
        if features['price_acceleration'] > 0:
            direction_score += Decimal("0.15")
        elif features['price_acceleration'] < 0:
            direction_score -= Decimal("0.15")

        # Trend signal
        if features['trend_strength'] > 0.001:
            direction_score += Decimal("0.2")
        elif features['trend_strength'] < -0.001:
            direction_score -= Decimal("0.2")

        # Mean reversion signal (contrarian)
        if features['distance_from_mean'] > 0.02:
            direction_score -= Decimal("0.15")  # Expect reversion down
        elif features['distance_from_mean'] < -0.02:
            direction_score += Decimal("0.15")  # Expect reversion up

        # Determine direction and confidence
        confidence = min(abs(direction_score), Decimal(1))

        if direction_score > Decimal("0.1"):
            direction = "up"
        elif direction_score < Decimal("-0.1"):
            direction = "down"
        else:
            direction = "neutral"
            confidence = Decimal(0)

        return direction, confidence

    def detect_pattern_signals(
        self,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect technical pattern signals.

        Args:
            historical_data: Historical market data

        Returns:
            List of detected patterns
        """
        if len(historical_data) < 10:
            return []

        patterns = []
        prices = [float(d.mid_price) for d in historical_data]

        # Double bottom pattern
        if self._detect_double_bottom(prices):
            patterns.append({
                "pattern": "double_bottom",
                "signal": "bullish",
                "confidence": 0.7
            })

        # Double top pattern
        if self._detect_double_top(prices):
            patterns.append({
                "pattern": "double_top",
                "signal": "bearish",
                "confidence": 0.7
            })

        # Head and shoulders
        if self._detect_head_and_shoulders(prices):
            patterns.append({
                "pattern": "head_and_shoulders",
                "signal": "bearish",
                "confidence": 0.75
            })

        # Inverse head and shoulders
        if self._detect_inverse_head_and_shoulders(prices):
            patterns.append({
                "pattern": "inverse_head_and_shoulders",
                "signal": "bullish",
                "confidence": 0.75
            })

        # Breakout pattern
        breakout = self._detect_breakout(prices)
        if breakout:
            patterns.append({
                "pattern": "breakout",
                "signal": breakout,
                "confidence": 0.65
            })

        return patterns

    def _detect_double_bottom(self, prices: List[float]) -> bool:
        """Detect double bottom pattern (simplified)."""
        if len(prices) < 10:
            return False

        # Find local minima
        minima = []
        for i in range(2, len(prices) - 2):
            if prices[i] < prices[i-1] and prices[i] < prices[i-2] and \
               prices[i] < prices[i+1] and prices[i] < prices[i+2]:
                minima.append((i, prices[i]))

        # Check for two similar lows
        if len(minima) >= 2:
            last_two = minima[-2:]
            if abs(last_two[0][1] - last_two[1][1]) / last_two[0][1] < 0.02:  # Within 2%
                return True

        return False

    def _detect_double_top(self, prices: List[float]) -> bool:
        """Detect double top pattern (simplified)."""
        if len(prices) < 10:
            return False

        # Find local maxima
        maxima = []
        for i in range(2, len(prices) - 2):
            if prices[i] > prices[i-1] and prices[i] > prices[i-2] and \
               prices[i] > prices[i+1] and prices[i] > prices[i+2]:
                maxima.append((i, prices[i]))

        # Check for two similar highs
        if len(maxima) >= 2:
            last_two = maxima[-2:]
            if abs(last_two[0][1] - last_two[1][1]) / last_two[0][1] < 0.02:
                return True

        return False

    def _detect_head_and_shoulders(self, prices: List[float]) -> bool:
        """Detect head and shoulders pattern (simplified)."""
        if len(prices) < 15:
            return False

        # Find three peaks
        maxima = []
        for i in range(2, len(prices) - 2):
            if prices[i] > prices[i-1] and prices[i] > prices[i-2] and \
               prices[i] > prices[i+1] and prices[i] > prices[i+2]:
                maxima.append((i, prices[i]))

        if len(maxima) >= 3:
            last_three = maxima[-3:]
            # Head should be higher than shoulders
            if (last_three[1][1] > last_three[0][1] and
                last_three[1][1] > last_three[2][1] and
                abs(last_three[0][1] - last_three[2][1]) / last_three[0][1] < 0.03):
                return True

        return False

    def _detect_inverse_head_and_shoulders(self, prices: List[float]) -> bool:
        """Detect inverse head and shoulders pattern (simplified)."""
        if len(prices) < 15:
            return False

        # Find three troughs
        minima = []
        for i in range(2, len(prices) - 2):
            if prices[i] < prices[i-1] and prices[i] < prices[i-2] and \
               prices[i] < prices[i+1] and prices[i] < prices[i+2]:
                minima.append((i, prices[i]))

        if len(minima) >= 3:
            last_three = minima[-3:]
            # Head should be lower than shoulders
            if (last_three[1][1] < last_three[0][1] and
                last_three[1][1] < last_three[2][1] and
                abs(last_three[0][1] - last_three[2][1]) / last_three[0][1] < 0.03):
                return True

        return False

    def _detect_breakout(self, prices: List[float]) -> Optional[str]:
        """Detect breakout pattern."""
        if len(prices) < 20:
            return None

        recent_prices = prices[-10:]
        historical_prices = prices[-20:-10]

        recent_high = max(recent_prices)
        recent_low = min(recent_prices)
        historical_high = max(historical_prices)
        historical_low = min(historical_prices)

        # Upward breakout
        if recent_high > historical_high * 1.02:
            return "bullish"

        # Downward breakout
        if recent_low < historical_low * 0.98:
            return "bearish"

        return None

    def generate_ml_based_opportunities(
        self,
        market_data: MarketData,
        historical_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Generate opportunities based on ML predictions.

        Args:
            market_data: Current market data
            historical_data: Historical market data

        Returns:
            List of predicted opportunities
        """
        opportunities = []

        # Extract features
        features = self.extract_features(market_data, historical_data)

        # Predict probability
        probability, explanation = self.predict_arbitrage_probability(features)

        # Only create opportunity if probability is high enough
        if probability < self.prediction_threshold:
            return opportunities

        # Predict direction
        direction, direction_confidence = self.predict_price_direction(features)

        if direction == "neutral":
            return opportunities

        # Detect patterns
        patterns = self.detect_pattern_signals(historical_data)

        # Create opportunity
        side = "buy" if direction == "up" else "sell"
        expected_move = direction_confidence * Decimal("2")  # Expected % move

        confidence = (probability + direction_confidence) / 2
        risk = Decimal(1) - confidence

        # Adjust for pattern signals
        for pattern in patterns:
            if (pattern['signal'] == 'bullish' and direction == 'up') or \
               (pattern['signal'] == 'bearish' and direction == 'down'):
                confidence += Decimal(str(pattern['confidence'])) * Decimal("0.1")
                confidence = min(confidence, Decimal("0.95"))

        opportunity = ArbitrageOpportunity(
            opportunity_id=str(uuid.uuid4()),
            arbitrage_type=ArbitrageType.STATISTICAL,
            market_type=market_data.market_type,
            symbol=market_data.symbol,
            timestamp=datetime.now(),
            expected_profit=expected_move * Decimal(100),
            expected_profit_percentage=expected_move,
            confidence_score=confidence,
            risk_score=risk,
            detection_latency_ms=0,
            market_data=[market_data],
            suggested_actions=[],
            metadata={
                "strategy": "ml_prediction",
                "predicted_direction": direction,
                "direction_confidence": float(direction_confidence),
                "probability": float(probability),
                "patterns": patterns,
                "explanation": explanation,
                "features": features
            }
        )

        opportunities.append(opportunity)

        return opportunities
