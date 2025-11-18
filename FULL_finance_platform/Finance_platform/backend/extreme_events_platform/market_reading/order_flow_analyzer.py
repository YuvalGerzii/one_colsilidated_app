"""
Order Flow and Tape Reading Analyzer

Analyzes real-time market order flow to understand:
- Aggressive buyers vs sellers (delta)
- Volume footprint analysis
- Absorption patterns
- Exhaustion signals
- Institutional vs retail flow patterns

Based on professional tape reading and order flow analysis techniques.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import statistics


class OrderFlowSignal(Enum):
    """Order flow signals"""
    STRONG_BUYING = "strong_buying"
    MODERATE_BUYING = "moderate_buying"
    NEUTRAL = "neutral"
    MODERATE_SELLING = "moderate_selling"
    STRONG_SELLING = "strong_selling"
    ABSORPTION = "absorption"
    EXHAUSTION = "exhaustion"
    BREAKOUT_IMMINENT = "breakout_imminent"


class TradeAggressor(Enum):
    """Who initiated the trade"""
    BUYER = "buyer"  # Market buy hitting ask
    SELLER = "seller"  # Market sell hitting bid


@dataclass
class Trade:
    """Single trade from time & sales"""
    timestamp: datetime
    price: float
    size: int
    aggressor: TradeAggressor
    is_block: bool = False  # Large block trade
    is_odd_lot: bool = False  # Odd lot (potential algo)


@dataclass
class VolumeFootprint:
    """Volume at price level showing buy/sell breakdown"""
    price: float
    buy_volume: int
    sell_volume: int
    delta: int  # buy - sell
    total_volume: int
    imbalance_ratio: float  # abs(delta) / total


@dataclass
class OrderFlowAnalysis:
    """Complete order flow analysis result"""
    cumulative_delta: int
    delta_divergence: bool  # Price up but delta down = bearish
    absorption_detected: bool
    exhaustion_detected: bool
    signal: OrderFlowSignal
    confidence: float
    key_levels: List[float]
    institutional_activity: float  # 0-1 score
    trading_recommendation: str
    details: Dict


class OrderFlowAnalyzer:
    """
    Analyzes order flow and tape to read market intent.

    Key concepts:
    - Delta: Difference between buy and sell volume
    - Absorption: Large volume with no price movement = strong hands absorbing
    - Exhaustion: Climactic volume with reversal = buyers/sellers exhausted
    - Footprint: Volume breakdown at each price level
    """

    def __init__(self):
        # Thresholds for analysis
        self.block_trade_threshold = 10000  # shares
        self.significant_delta_threshold = 0.6  # 60% imbalance
        self.absorption_volume_multiple = 3.0  # 3x normal volume
        self.exhaustion_volume_multiple = 5.0  # 5x normal volume

        # Institutional detection patterns
        self.institutional_patterns = {
            'iceberg': {
                'consistent_size': True,
                'regular_interval': True,
                'odd_lot': True  # e.g., 137, 244 shares
            },
            'twap': {
                'even_distribution': True,
                'time_weighted': True
            },
            'vwap': {
                'volume_weighted': True,
                'follows_market_volume': True
            }
        }

    def analyze_tape(self, trades: List[Trade],
                     price_history: List[float] = None) -> OrderFlowAnalysis:
        """
        Main analysis of time & sales tape.

        Args:
            trades: List of trades from time & sales
            price_history: Recent price history for context

        Returns:
            Complete order flow analysis
        """
        if not trades:
            return self._empty_analysis()

        # Calculate basic metrics
        buy_volume = sum(t.size for t in trades if t.aggressor == TradeAggressor.BUYER)
        sell_volume = sum(t.size for t in trades if t.aggressor == TradeAggressor.SELLER)
        total_volume = buy_volume + sell_volume
        cumulative_delta = buy_volume - sell_volume

        # Calculate delta percentage
        delta_pct = cumulative_delta / total_volume if total_volume > 0 else 0

        # Build volume footprint
        footprint = self._build_footprint(trades)

        # Detect patterns
        absorption = self._detect_absorption(trades, footprint, price_history)
        exhaustion = self._detect_exhaustion(trades, price_history)

        # Check for delta divergence
        divergence = self._check_delta_divergence(
            cumulative_delta, price_history
        ) if price_history else False

        # Detect institutional activity
        institutional_score = self._detect_institutional_activity(trades)

        # Find key levels from footprint
        key_levels = self._find_key_levels(footprint)

        # Determine signal
        signal = self._determine_signal(
            delta_pct, absorption, exhaustion, divergence
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            trades, delta_pct, absorption, exhaustion
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(
            signal, key_levels, institutional_score, divergence
        )

        return OrderFlowAnalysis(
            cumulative_delta=cumulative_delta,
            delta_divergence=divergence,
            absorption_detected=absorption,
            exhaustion_detected=exhaustion,
            signal=signal,
            confidence=confidence,
            key_levels=key_levels,
            institutional_activity=institutional_score,
            trading_recommendation=recommendation,
            details={
                'buy_volume': buy_volume,
                'sell_volume': sell_volume,
                'total_volume': total_volume,
                'delta_pct': delta_pct,
                'footprint': footprint,
                'block_trades': sum(1 for t in trades if t.is_block),
                'avg_trade_size': total_volume / len(trades) if trades else 0
            }
        )

    def _build_footprint(self, trades: List[Trade]) -> List[VolumeFootprint]:
        """Build volume footprint showing buy/sell at each price"""
        price_levels = {}

        for trade in trades:
            price = round(trade.price, 2)
            if price not in price_levels:
                price_levels[price] = {'buy': 0, 'sell': 0}

            if trade.aggressor == TradeAggressor.BUYER:
                price_levels[price]['buy'] += trade.size
            else:
                price_levels[price]['sell'] += trade.size

        footprint = []
        for price, volumes in sorted(price_levels.items()):
            buy_vol = volumes['buy']
            sell_vol = volumes['sell']
            total = buy_vol + sell_vol
            delta = buy_vol - sell_vol
            imbalance = abs(delta) / total if total > 0 else 0

            footprint.append(VolumeFootprint(
                price=price,
                buy_volume=buy_vol,
                sell_volume=sell_vol,
                delta=delta,
                total_volume=total,
                imbalance_ratio=imbalance
            ))

        return footprint

    def _detect_absorption(self, trades: List[Trade],
                          footprint: List[VolumeFootprint],
                          price_history: List[float] = None) -> bool:
        """
        Detect absorption - large volume with minimal price movement.

        Absorption indicates strong hands (institutions) absorbing
        aggressive selling/buying without letting price move.
        This often precedes reversals.
        """
        if not footprint or not price_history or len(price_history) < 2:
            return False

        total_volume = sum(fp.total_volume for fp in footprint)
        avg_volume = total_volume / len(footprint) if footprint else 0

        # Price range during period
        price_range = max(price_history) - min(price_history)
        avg_price = sum(price_history) / len(price_history)
        price_range_pct = price_range / avg_price if avg_price > 0 else 0

        # Absorption: high volume, tight range
        # Normal: 1% range with 1x volume
        # Absorption: <0.3% range with 3x+ volume

        # Check for high volume at specific levels
        max_volume_level = max(footprint, key=lambda x: x.total_volume)

        is_absorption = (
            price_range_pct < 0.003 and  # <0.3% price movement
            max_volume_level.total_volume > avg_volume * self.absorption_volume_multiple
        )

        return is_absorption

    def _detect_exhaustion(self, trades: List[Trade],
                          price_history: List[float] = None) -> bool:
        """
        Detect exhaustion - climactic volume with reversal.

        Exhaustion occurs when aggressive buyers/sellers have
        used up their firepower, often at tops/bottoms.
        """
        if not trades or not price_history or len(price_history) < 5:
            return False

        # Need climactic volume
        total_volume = sum(t.size for t in trades)

        # Split trades into first half and second half
        mid = len(trades) // 2
        first_half = trades[:mid]
        second_half = trades[mid:]

        # Calculate delta for each half
        first_delta = sum(
            t.size if t.aggressor == TradeAggressor.BUYER else -t.size
            for t in first_half
        )
        second_delta = sum(
            t.size if t.aggressor == TradeAggressor.BUYER else -t.size
            for t in second_half
        )

        # Exhaustion: strong delta reversal within period
        # First half strongly buying, second half selling (or vice versa)
        delta_reversal = (first_delta > 0 and second_delta < 0) or \
                        (first_delta < 0 and second_delta > 0)

        # Price should have made a high/low then reversed
        prices = price_history[-10:] if len(price_history) >= 10 else price_history
        high_idx = prices.index(max(prices))
        low_idx = prices.index(min(prices))

        # High or low should be in middle, not at end
        reversal_pattern = (
            (high_idx > 2 and high_idx < len(prices) - 2) or
            (low_idx > 2 and low_idx < len(prices) - 2)
        )

        return delta_reversal and reversal_pattern

    def _check_delta_divergence(self, cumulative_delta: int,
                                price_history: List[float]) -> bool:
        """
        Check for delta divergence - powerful reversal signal.

        Bullish divergence: Price making lower lows, delta making higher lows
        Bearish divergence: Price making higher highs, delta making lower highs
        """
        if not price_history or len(price_history) < 2:
            return False

        price_direction = price_history[-1] - price_history[0]

        # Simple check: price and delta moving opposite directions
        if price_direction > 0 and cumulative_delta < 0:
            return True  # Bearish divergence
        elif price_direction < 0 and cumulative_delta > 0:
            return True  # Bullish divergence

        return False

    def _detect_institutional_activity(self, trades: List[Trade]) -> float:
        """
        Detect institutional trading patterns.

        Institutional signatures:
        - Regular intervals (TWAP)
        - Consistent odd-lot sizes (e.g., 137, 244)
        - Large blocks broken into smaller pieces (iceberg)
        - Slower reaction to price but defend levels with size

        Returns score 0-1 indicating likelihood of institutional activity.
        """
        if not trades:
            return 0.0

        score = 0.0
        weights = {'block': 0.3, 'odd_lot': 0.2, 'consistent': 0.2, 'timing': 0.3}

        # Block trades
        block_trades = [t for t in trades if t.is_block]
        if block_trades:
            block_ratio = len(block_trades) / len(trades)
            score += weights['block'] * min(block_ratio * 10, 1.0)

        # Odd lot patterns (algorithmic)
        odd_lots = [t for t in trades if t.is_odd_lot]
        if odd_lots:
            odd_lot_ratio = len(odd_lots) / len(trades)
            # High odd lot ratio suggests algo trading
            if odd_lot_ratio > 0.3:
                score += weights['odd_lot']

        # Consistent trade sizes (TWAP/VWAP)
        sizes = [t.size for t in trades]
        if len(sizes) > 5:
            size_std = statistics.stdev(sizes)
            size_mean = statistics.mean(sizes)
            cv = size_std / size_mean if size_mean > 0 else 1
            # Low coefficient of variation = consistent sizes
            if cv < 0.3:
                score += weights['consistent']

        # Regular timing intervals
        if len(trades) > 5:
            intervals = []
            for i in range(1, len(trades)):
                interval = (trades[i].timestamp - trades[i-1].timestamp).total_seconds()
                intervals.append(interval)

            if intervals:
                interval_std = statistics.stdev(intervals) if len(intervals) > 1 else 0
                interval_mean = statistics.mean(intervals)
                interval_cv = interval_std / interval_mean if interval_mean > 0 else 1
                # Regular intervals suggest algorithmic execution
                if interval_cv < 0.5:
                    score += weights['timing']

        return min(score, 1.0)

    def _find_key_levels(self, footprint: List[VolumeFootprint]) -> List[float]:
        """Find key support/resistance levels from volume profile"""
        if not footprint:
            return []

        # Sort by volume to find high volume nodes (HVN)
        sorted_by_volume = sorted(footprint, key=lambda x: x.total_volume, reverse=True)

        # Top 3 volume levels are key levels
        key_levels = [fp.price for fp in sorted_by_volume[:3]]

        # Also look for levels with high imbalance
        high_imbalance = [
            fp.price for fp in footprint
            if fp.imbalance_ratio > self.significant_delta_threshold
        ]

        # Combine and deduplicate
        all_levels = list(set(key_levels + high_imbalance[:2]))
        return sorted(all_levels)

    def _determine_signal(self, delta_pct: float,
                         absorption: bool,
                         exhaustion: bool,
                         divergence: bool) -> OrderFlowSignal:
        """Determine overall order flow signal"""

        if exhaustion:
            return OrderFlowSignal.EXHAUSTION

        if absorption:
            return OrderFlowSignal.ABSORPTION

        if divergence:
            # Divergence suggests imminent reversal
            return OrderFlowSignal.BREAKOUT_IMMINENT

        if delta_pct > 0.4:
            return OrderFlowSignal.STRONG_BUYING
        elif delta_pct > 0.15:
            return OrderFlowSignal.MODERATE_BUYING
        elif delta_pct < -0.4:
            return OrderFlowSignal.STRONG_SELLING
        elif delta_pct < -0.15:
            return OrderFlowSignal.MODERATE_SELLING
        else:
            return OrderFlowSignal.NEUTRAL

    def _calculate_confidence(self, trades: List[Trade],
                             delta_pct: float,
                             absorption: bool,
                             exhaustion: bool) -> float:
        """Calculate confidence in the signal"""
        confidence = 0.5  # Base confidence

        # More trades = more confidence
        if len(trades) > 100:
            confidence += 0.1
        if len(trades) > 500:
            confidence += 0.1

        # Stronger delta = more confidence
        confidence += abs(delta_pct) * 0.2

        # Pattern detection adds confidence
        if absorption or exhaustion:
            confidence += 0.15

        return min(confidence, 0.95)

    def _generate_recommendation(self, signal: OrderFlowSignal,
                                 key_levels: List[float],
                                 institutional_score: float,
                                 divergence: bool) -> str:
        """Generate actionable trading recommendation"""

        recommendations = []

        # Signal-based recommendations
        if signal == OrderFlowSignal.STRONG_BUYING:
            recommendations.append("Strong buying pressure - consider long entries on pullbacks")
            recommendations.append("Set stops below nearest key level")

        elif signal == OrderFlowSignal.STRONG_SELLING:
            recommendations.append("Strong selling pressure - consider short entries on bounces")
            recommendations.append("Set stops above nearest key level")

        elif signal == OrderFlowSignal.ABSORPTION:
            recommendations.append("Absorption detected - potential reversal forming")
            recommendations.append("Wait for confirmation before entering against trend")
            recommendations.append("High probability setup if price breaks away from absorption zone")

        elif signal == OrderFlowSignal.EXHAUSTION:
            recommendations.append("Exhaustion signal - climactic move may be ending")
            recommendations.append("Consider counter-trend positions with tight stops")
            recommendations.append("Scale in on confirmation, not anticipation")

        elif signal == OrderFlowSignal.BREAKOUT_IMMINENT:
            recommendations.append("Delta divergence detected - breakout likely imminent")
            if divergence:
                recommendations.append("Prepare for reversal in price direction")

        else:  # Neutral or moderate
            recommendations.append("Mixed signals - wait for clearer setup")
            recommendations.append("Focus on key levels for entries")

        # Institutional activity warning
        if institutional_score > 0.7:
            recommendations.append(f"High institutional activity ({institutional_score:.0%}) - follow the smart money")
        elif institutional_score > 0.4:
            recommendations.append(f"Moderate institutional activity ({institutional_score:.0%}) - be aware of hidden orders")

        # Key levels
        if key_levels:
            levels_str = ", ".join(f"${level:.2f}" for level in key_levels)
            recommendations.append(f"Key levels to watch: {levels_str}")

        return " | ".join(recommendations)

    def _empty_analysis(self) -> OrderFlowAnalysis:
        """Return empty analysis when no data"""
        return OrderFlowAnalysis(
            cumulative_delta=0,
            delta_divergence=False,
            absorption_detected=False,
            exhaustion_detected=False,
            signal=OrderFlowSignal.NEUTRAL,
            confidence=0.0,
            key_levels=[],
            institutional_activity=0.0,
            trading_recommendation="Insufficient data for analysis",
            details={}
        )

    def analyze_volume_imbalance(self, footprint: List[VolumeFootprint]) -> Dict:
        """
        Analyze volume imbalances at price levels.

        Stacked imbalances (3+ consecutive levels with same direction)
        indicate strong conviction and often predict breakouts.
        """
        if not footprint:
            return {'stacked_imbalances': [], 'bias': 'neutral'}

        # Find stacked imbalances
        stacked = []
        current_stack = []
        current_direction = None

        for fp in footprint:
            if fp.imbalance_ratio > 0.3:  # Significant imbalance
                direction = 'buy' if fp.delta > 0 else 'sell'

                if direction == current_direction:
                    current_stack.append(fp)
                else:
                    if len(current_stack) >= 3:
                        stacked.append({
                            'direction': current_direction,
                            'levels': [f.price for f in current_stack],
                            'total_imbalance': sum(f.delta for f in current_stack)
                        })
                    current_stack = [fp]
                    current_direction = direction

        # Don't forget last stack
        if len(current_stack) >= 3:
            stacked.append({
                'direction': current_direction,
                'levels': [f.price for f in current_stack],
                'total_imbalance': sum(f.delta for f in current_stack)
            })

        # Determine overall bias
        total_delta = sum(fp.delta for fp in footprint)
        if total_delta > 0:
            bias = 'bullish'
        elif total_delta < 0:
            bias = 'bearish'
        else:
            bias = 'neutral'

        return {
            'stacked_imbalances': stacked,
            'bias': bias,
            'total_delta': total_delta
        }

    def detect_iceberg_orders(self, trades: List[Trade]) -> List[Dict]:
        """
        Detect potential iceberg orders.

        Iceberg characteristics:
        - Repeated fills at same price
        - Consistent small sizes that add up to large total
        - Price doesn't move despite large cumulative volume
        """
        if not trades:
            return []

        icebergs = []
        price_fills = {}

        for trade in trades:
            price = round(trade.price, 2)
            if price not in price_fills:
                price_fills[price] = {'sizes': [], 'total': 0, 'direction': None}

            price_fills[price]['sizes'].append(trade.size)
            price_fills[price]['total'] += trade.size
            price_fills[price]['direction'] = trade.aggressor

        for price, data in price_fills.items():
            sizes = data['sizes']
            if len(sizes) >= 5:  # Multiple fills
                # Check for consistent sizes
                if len(sizes) > 1:
                    cv = statistics.stdev(sizes) / statistics.mean(sizes)
                    if cv < 0.3 and data['total'] > self.block_trade_threshold:
                        icebergs.append({
                            'price': price,
                            'total_volume': data['total'],
                            'num_fills': len(sizes),
                            'avg_fill_size': data['total'] / len(sizes),
                            'direction': data['direction'].value if data['direction'] else 'unknown',
                            'confidence': 0.8 if cv < 0.2 else 0.6
                        })

        return icebergs


class DeltaAccumulator:
    """
    Tracks cumulative delta over time for trend analysis.

    Rising cumulative delta with rising price = healthy trend
    Rising price with falling delta = weak trend, reversal likely
    """

    def __init__(self):
        self.history = []  # List of (timestamp, delta, price)

    def add_period(self, timestamp: datetime, delta: int, price: float):
        """Add a period's delta to history"""
        cumulative = self.history[-1][1] + delta if self.history else delta
        self.history.append((timestamp, cumulative, price))

        # Keep last 1000 periods
        if len(self.history) > 1000:
            self.history = self.history[-1000:]

    def get_divergence_signal(self) -> Optional[str]:
        """Check for divergence between delta and price"""
        if len(self.history) < 20:
            return None

        recent = self.history[-20:]

        # Compare first half to second half
        first_half = recent[:10]
        second_half = recent[10:]

        first_delta_avg = sum(d[1] for d in first_half) / 10
        second_delta_avg = sum(d[1] for d in second_half) / 10

        first_price_avg = sum(d[2] for d in first_half) / 10
        second_price_avg = sum(d[2] for d in second_half) / 10

        price_rising = second_price_avg > first_price_avg
        delta_rising = second_delta_avg > first_delta_avg

        if price_rising and not delta_rising:
            return "BEARISH_DIVERGENCE"
        elif not price_rising and delta_rising:
            return "BULLISH_DIVERGENCE"

        return None

    def get_trend_strength(self) -> float:
        """Calculate trend strength based on delta momentum"""
        if len(self.history) < 10:
            return 0.0

        recent_deltas = [d[1] for d in self.history[-10:]]

        # Trend strength = consistency of delta direction
        positive = sum(1 for d in recent_deltas if d > 0)

        if positive >= 8:
            return 0.8  # Strong bullish
        elif positive >= 6:
            return 0.4  # Moderate bullish
        elif positive <= 2:
            return -0.8  # Strong bearish
        elif positive <= 4:
            return -0.4  # Moderate bearish
        else:
            return 0.0  # Neutral
