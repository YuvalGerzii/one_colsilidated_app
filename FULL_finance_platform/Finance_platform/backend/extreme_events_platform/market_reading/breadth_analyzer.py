"""
Market Breadth Analyzer

Analyzes market-wide breadth indicators to assess market health:
- Advance/Decline Line
- McClellan Oscillator and Summation Index
- TRIN (Arms Index)
- New Highs/Lows
- Percent Above Moving Averages

These indicators reveal the internal health of the market.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, date
import statistics
import math


class BreadthSignal(Enum):
    """Market breadth signals"""
    STRONG_BULLISH = "strong_bullish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    STRONG_BEARISH = "strong_bearish"
    BREADTH_THRUST = "breadth_thrust"  # Powerful bullish signal
    HINDENBURG_OMEN = "hindenburg_omen"  # Potential crash warning


@dataclass
class DailyBreadthData:
    """Daily market breadth data"""
    date: date
    advances: int
    declines: int
    unchanged: int
    advancing_volume: int
    declining_volume: int
    new_highs: int
    new_lows: int
    total_issues: int


@dataclass
class BreadthAnalysis:
    """Complete market breadth analysis result"""
    ad_line: float
    ad_line_trend: str  # 'up', 'down', 'flat'
    ad_divergence: bool  # Price vs A/D divergence
    mcclellan_oscillator: float
    mcclellan_summation: float
    trin: float
    trin_signal: str
    new_highs_lows_ratio: float
    percent_above_50ma: float
    percent_above_200ma: float
    overall_signal: BreadthSignal
    confidence: float
    breadth_thrust_detected: bool
    hindenburg_omen_detected: bool
    trading_signals: List[str]
    recommendations: List[str]


class BreadthAnalyzer:
    """
    Analyzes market breadth to assess internal market health.

    Breadth indicators measure participation across all stocks,
    not just index components. Healthy rallies have broad participation;
    unhealthy ones are narrow (few stocks doing the heavy lifting).
    """

    def __init__(self):
        # McClellan parameters (standard values)
        self.mcclellan_short_ema = 19  # ~10% smoothing
        self.mcclellan_long_ema = 39   # ~5% smoothing

        # Signal thresholds
        self.thresholds = {
            'mcclellan': {
                'overbought': 100,
                'oversold': -100,
                'extreme_overbought': 150,
                'extreme_oversold': -150,
                'breadth_thrust': 100  # +100 point move
            },
            'trin': {
                'extreme_selling': 2.0,  # Capitulation
                'heavy_selling': 1.5,
                'balanced': 1.0,
                'heavy_buying': 0.7,
                'extreme_buying': 0.5
            },
            'percent_above_ma': {
                'very_overbought': 80,
                'overbought': 70,
                'neutral': 50,
                'oversold': 30,
                'very_oversold': 20
            }
        }

        # Historical data storage
        self.ad_history = []
        self.mcclellan_history = []
        self.summation_history = []

    def analyze_breadth(self, breadth_data: List[DailyBreadthData],
                        index_prices: List[float] = None) -> BreadthAnalysis:
        """
        Main breadth analysis function.

        Args:
            breadth_data: Daily breadth data (most recent last)
            index_prices: Corresponding index prices for divergence analysis

        Returns:
            Complete breadth analysis
        """
        if not breadth_data:
            return self._empty_analysis()

        # Calculate A/D Line
        ad_line = self._calculate_ad_line(breadth_data)
        ad_trend = self._determine_ad_trend(ad_line)

        # Check for A/D divergence with price
        ad_divergence = self._check_ad_divergence(ad_line, index_prices)

        # Calculate McClellan Oscillator
        mcclellan = self._calculate_mcclellan_oscillator(breadth_data)

        # Calculate McClellan Summation Index
        summation = self._calculate_summation_index(mcclellan)

        # Calculate TRIN (Arms Index)
        trin = self._calculate_trin(breadth_data[-1])
        trin_signal = self._interpret_trin(trin)

        # New Highs/Lows ratio
        nh_nl_ratio = self._calculate_new_highs_lows_ratio(breadth_data[-1])

        # Percent above moving averages (need more data typically)
        pct_above_50ma = self._estimate_percent_above_ma(breadth_data, 50)
        pct_above_200ma = self._estimate_percent_above_ma(breadth_data, 200)

        # Detect special patterns
        breadth_thrust = self._detect_breadth_thrust(mcclellan)
        hindenburg = self._detect_hindenburg_omen(breadth_data)

        # Determine overall signal
        overall_signal = self._determine_overall_signal(
            mcclellan[-1] if mcclellan else 0,
            trin,
            ad_divergence,
            breadth_thrust,
            hindenburg,
            nh_nl_ratio
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            breadth_data, mcclellan, ad_divergence, breadth_thrust
        )

        # Generate signals and recommendations
        signals = self._generate_signals(
            mcclellan[-1] if mcclellan else 0,
            summation,
            trin,
            ad_divergence,
            breadth_thrust,
            hindenburg,
            pct_above_50ma
        )

        recommendations = self._generate_recommendations(
            overall_signal, mcclellan[-1] if mcclellan else 0,
            trin, ad_divergence, confidence
        )

        return BreadthAnalysis(
            ad_line=ad_line[-1] if ad_line else 0,
            ad_line_trend=ad_trend,
            ad_divergence=ad_divergence,
            mcclellan_oscillator=mcclellan[-1] if mcclellan else 0,
            mcclellan_summation=summation,
            trin=trin,
            trin_signal=trin_signal,
            new_highs_lows_ratio=nh_nl_ratio,
            percent_above_50ma=pct_above_50ma,
            percent_above_200ma=pct_above_200ma,
            overall_signal=overall_signal,
            confidence=confidence,
            breadth_thrust_detected=breadth_thrust,
            hindenburg_omen_detected=hindenburg,
            trading_signals=signals,
            recommendations=recommendations
        )

    def _calculate_ad_line(self, data: List[DailyBreadthData]) -> List[float]:
        """
        Calculate cumulative Advance/Decline Line.

        A/D Line = Previous A/D + (Advances - Declines)

        Rising A/D Line = healthy market breadth
        Falling A/D Line = deteriorating breadth
        """
        ad_line = []
        cumulative = 0

        for day in data:
            net_advances = day.advances - day.declines
            cumulative += net_advances
            ad_line.append(cumulative)

        return ad_line

    def _determine_ad_trend(self, ad_line: List[float]) -> str:
        """Determine A/D Line trend"""
        if len(ad_line) < 10:
            return 'insufficient_data'

        recent = ad_line[-10:]

        # Simple trend determination
        if recent[-1] > recent[0] * 1.02:
            return 'up'
        elif recent[-1] < recent[0] * 0.98:
            return 'down'
        else:
            return 'flat'

    def _check_ad_divergence(self, ad_line: List[float],
                             prices: List[float] = None) -> bool:
        """
        Check for divergence between A/D Line and price.

        Bearish divergence: Price makes new high, A/D doesn't = weakness
        Bullish divergence: Price makes new low, A/D doesn't = strength
        """
        if not prices or len(ad_line) < 20 or len(prices) < 20:
            return False

        # Compare last 20 days
        recent_ad = ad_line[-20:]
        recent_prices = prices[-20:]

        # Check if price made new high but A/D didn't
        price_high = max(recent_prices)
        price_high_idx = recent_prices.index(price_high)

        ad_high = max(recent_ad)
        ad_high_idx = recent_ad.index(ad_high)

        # If price high is recent but A/D high is not = bearish divergence
        if price_high_idx > 15 and ad_high_idx < 10:
            return True

        # Check for bullish divergence
        price_low = min(recent_prices)
        price_low_idx = recent_prices.index(price_low)

        ad_low = min(recent_ad)
        ad_low_idx = recent_ad.index(ad_low)

        if price_low_idx > 15 and ad_low_idx < 10:
            return True

        return False

    def _calculate_mcclellan_oscillator(self,
                                        data: List[DailyBreadthData]) -> List[float]:
        """
        Calculate McClellan Oscillator.

        McClellan = 19-day EMA of Net Advances - 39-day EMA of Net Advances

        Positive = bullish breadth momentum
        Negative = bearish breadth momentum
        """
        if not data:
            return []

        # Calculate daily net advances
        net_advances = [d.advances - d.declines for d in data]

        # Calculate EMAs
        short_ema = self._calculate_ema(net_advances, self.mcclellan_short_ema)
        long_ema = self._calculate_ema(net_advances, self.mcclellan_long_ema)

        # McClellan = short EMA - long EMA
        if len(short_ema) == len(long_ema):
            mcclellan = [s - l for s, l in zip(short_ema, long_ema)]
        else:
            min_len = min(len(short_ema), len(long_ema))
            mcclellan = [short_ema[i] - long_ema[i] for i in range(min_len)]

        return mcclellan

    def _calculate_ema(self, values: List[float], period: int) -> List[float]:
        """Calculate Exponential Moving Average"""
        if not values or period <= 0:
            return []

        multiplier = 2 / (period + 1)
        ema = [values[0]]  # Start with first value

        for i in range(1, len(values)):
            ema_value = (values[i] * multiplier) + (ema[-1] * (1 - multiplier))
            ema.append(ema_value)

        return ema

    def _calculate_summation_index(self, mcclellan: List[float]) -> float:
        """
        Calculate McClellan Summation Index.

        Summation Index = cumulative sum of McClellan Oscillator

        Used to identify major market tops and bottoms.
        """
        if not mcclellan:
            return 0

        return sum(mcclellan)

    def _calculate_trin(self, day: DailyBreadthData) -> float:
        """
        Calculate TRIN (Arms Index).

        TRIN = (Advances/Declines) / (Advancing Volume/Declining Volume)

        TRIN < 1.0 = buying pressure (more volume in advancing stocks)
        TRIN > 1.0 = selling pressure (more volume in declining stocks)
        TRIN > 2.0 = extreme selling (potential capitulation/bottom)
        """
        if day.declines == 0 or day.declining_volume == 0:
            return 1.0

        ad_ratio = day.advances / day.declines if day.declines > 0 else 1
        vol_ratio = day.advancing_volume / day.declining_volume if day.declining_volume > 0 else 1

        trin = ad_ratio / vol_ratio if vol_ratio > 0 else 1.0

        return trin

    def _interpret_trin(self, trin: float) -> str:
        """Interpret TRIN reading"""
        thresholds = self.thresholds['trin']

        if trin >= thresholds['extreme_selling']:
            return "Extreme selling (capitulation likely)"
        elif trin >= thresholds['heavy_selling']:
            return "Heavy selling pressure"
        elif trin <= thresholds['extreme_buying']:
            return "Extreme buying (potential top)"
        elif trin <= thresholds['heavy_buying']:
            return "Heavy buying pressure"
        else:
            return "Balanced flow"

    def _calculate_new_highs_lows_ratio(self, day: DailyBreadthData) -> float:
        """
        Calculate New Highs / New Lows ratio.

        > 1.0 = more new highs (bullish)
        < 1.0 = more new lows (bearish)
        """
        if day.new_lows == 0:
            return float('inf') if day.new_highs > 0 else 1.0

        return day.new_highs / day.new_lows

    def _estimate_percent_above_ma(self, data: List[DailyBreadthData],
                                   ma_period: int) -> float:
        """
        Estimate percent of stocks above moving average.

        This is a simplified estimation based on breadth data.
        In practice, you'd scan all stocks.
        """
        if not data:
            return 50.0

        # Use recent breadth data as proxy
        recent = data[-min(ma_period, len(data)):]

        total_advances = sum(d.advances for d in recent)
        total_declines = sum(d.declines for d in recent)
        total = total_advances + total_declines

        if total == 0:
            return 50.0

        # Rough estimate: sustained advances = more above MA
        advance_pct = total_advances / total

        # Scale to typical range (20-80%)
        pct_above = 20 + (advance_pct * 60)

        return pct_above

    def _detect_breadth_thrust(self, mcclellan: List[float]) -> bool:
        """
        Detect Breadth Thrust - powerful bullish signal.

        Breadth Thrust occurs when McClellan surges from below -50
        to above +50 (a +100 point move).

        This is one of the most reliable bullish signals,
        often occurring at the start of major bull markets.
        """
        if len(mcclellan) < 10:
            return False

        recent = mcclellan[-10:]

        # Find if we went from <-50 to >+50
        min_val = min(recent)
        min_idx = recent.index(min_val)

        max_val = max(recent)
        max_idx = recent.index(max_val)

        # Thrust = min below -50, max above +50, max after min
        if min_val < -50 and max_val > 50 and max_idx > min_idx:
            return True

        return False

    def _detect_hindenburg_omen(self, data: List[DailyBreadthData]) -> bool:
        """
        Detect Hindenburg Omen - potential crash warning.

        Conditions (all must be true):
        1. NYSE 52-week highs and lows both > 2.2% of issues
        2. 10-week MA of NYSE is rising
        3. McClellan Oscillator is negative

        The Hindenburg Omen has predicted several major crashes,
        but also has many false positives.
        """
        if not data:
            return False

        day = data[-1]

        # Condition 1: Both highs and lows > 2.2% of total issues
        high_pct = day.new_highs / day.total_issues if day.total_issues > 0 else 0
        low_pct = day.new_lows / day.total_issues if day.total_issues > 0 else 0

        condition1 = high_pct > 0.022 and low_pct > 0.022

        # Condition 2: Rising 10-week MA (use A/D line as proxy)
        if len(data) >= 50:
            recent_ad = sum(d.advances - d.declines for d in data[-10:])
            prior_ad = sum(d.advances - d.declines for d in data[-20:-10])
            condition2 = recent_ad > prior_ad
        else:
            condition2 = False

        # Condition 3: Would need McClellan data
        # For now, use net advances as proxy
        net_advances = day.advances - day.declines
        condition3 = net_advances < 0

        return condition1 and condition2 and condition3

    def _determine_overall_signal(self, mcclellan: float,
                                   trin: float,
                                   divergence: bool,
                                   breadth_thrust: bool,
                                   hindenburg: bool,
                                   nh_nl_ratio: float) -> BreadthSignal:
        """Determine overall breadth signal"""

        # Special signals take precedence
        if breadth_thrust:
            return BreadthSignal.BREADTH_THRUST

        if hindenburg:
            return BreadthSignal.HINDENBURG_OMEN

        # Score-based determination
        score = 0

        # McClellan contribution
        if mcclellan > 100:
            score += 2
        elif mcclellan > 50:
            score += 1
        elif mcclellan < -100:
            score -= 2
        elif mcclellan < -50:
            score -= 1

        # TRIN contribution (inverted - low TRIN is bullish)
        if trin < 0.7:
            score += 1
        elif trin > 1.5:
            score -= 1

        # NH/NL ratio
        if nh_nl_ratio > 3:
            score += 1
        elif nh_nl_ratio < 0.33:
            score -= 1

        # Divergence is bearish
        if divergence:
            score -= 1

        # Determine signal
        if score >= 3:
            return BreadthSignal.STRONG_BULLISH
        elif score >= 1:
            return BreadthSignal.BULLISH
        elif score <= -3:
            return BreadthSignal.STRONG_BEARISH
        elif score <= -1:
            return BreadthSignal.BEARISH
        else:
            return BreadthSignal.NEUTRAL

    def _calculate_confidence(self, data: List[DailyBreadthData],
                              mcclellan: List[float],
                              divergence: bool,
                              breadth_thrust: bool) -> float:
        """Calculate confidence in the signal"""
        confidence = 0.5

        # More data = more confidence
        if len(data) >= 50:
            confidence += 0.1

        # Breadth thrust is very reliable
        if breadth_thrust:
            confidence += 0.2

        # Strong McClellan readings
        if mcclellan and abs(mcclellan[-1]) > 100:
            confidence += 0.1

        # Divergence confirmation
        if divergence:
            confidence += 0.1

        return min(confidence, 0.95)

    def _generate_signals(self, mcclellan: float,
                          summation: float,
                          trin: float,
                          divergence: bool,
                          breadth_thrust: bool,
                          hindenburg: bool,
                          pct_above_50ma: float) -> List[str]:
        """Generate trading signals from breadth analysis"""
        signals = []

        # McClellan signals
        if mcclellan > self.thresholds['mcclellan']['extreme_overbought']:
            signals.append(f"McClellan extremely overbought ({mcclellan:.0f}) - potential pullback")
        elif mcclellan > self.thresholds['mcclellan']['overbought']:
            signals.append(f"McClellan overbought ({mcclellan:.0f}) - caution on new longs")
        elif mcclellan < self.thresholds['mcclellan']['extreme_oversold']:
            signals.append(f"McClellan extremely oversold ({mcclellan:.0f}) - potential bounce")
        elif mcclellan < self.thresholds['mcclellan']['oversold']:
            signals.append(f"McClellan oversold ({mcclellan:.0f}) - watch for reversal")

        # Summation Index signals
        if summation > 1000:
            signals.append(f"Summation Index bullish ({summation:.0f}) - bull market intact")
        elif summation < -1000:
            signals.append(f"Summation Index bearish ({summation:.0f}) - bear market")

        # TRIN signals
        if trin > 2.0:
            signals.append(f"TRIN at capitulation level ({trin:.2f}) - contrarian BUY signal")
        elif trin < 0.5:
            signals.append(f"TRIN at euphoria level ({trin:.2f}) - contrarian SELL signal")

        # Special patterns
        if breadth_thrust:
            signals.append("BREADTH THRUST detected - highly bullish (rare signal)")
            signals.append("Historically precedes extended rallies")

        if hindenburg:
            signals.append("HINDENBURG OMEN detected - elevated crash risk")
            signals.append("Consider protective hedges")

        if divergence:
            signals.append("A/D Line divergence detected - potential reversal")

        # Percent above MA
        if pct_above_50ma < 20:
            signals.append(f"Only {pct_above_50ma:.0f}% above 50-day MA - oversold market")
        elif pct_above_50ma > 80:
            signals.append(f"{pct_above_50ma:.0f}% above 50-day MA - overbought market")

        return signals

    def _generate_recommendations(self, signal: BreadthSignal,
                                   mcclellan: float,
                                   trin: float,
                                   divergence: bool,
                                   confidence: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if signal == BreadthSignal.BREADTH_THRUST:
            recommendations.append("Aggressively add long exposure - breadth thrust is rare and reliable")
            recommendations.append("Reduce/eliminate shorts")
            recommendations.append("Expected: 10-20% rally over 3-6 months")

        elif signal == BreadthSignal.HINDENBURG_OMEN:
            recommendations.append("Increase cash allocation")
            recommendations.append("Consider protective puts or VIX calls")
            recommendations.append("Reduce speculative positions")

        elif signal == BreadthSignal.STRONG_BULLISH:
            recommendations.append("Add to long positions on pullbacks")
            recommendations.append("Raise stops on existing positions")

        elif signal == BreadthSignal.BULLISH:
            recommendations.append("Maintain long bias")
            recommendations.append("Wait for pullbacks to add")

        elif signal == BreadthSignal.STRONG_BEARISH:
            recommendations.append("Reduce long exposure")
            recommendations.append("Consider short positions")
            recommendations.append("Raise cash levels")

        elif signal == BreadthSignal.BEARISH:
            recommendations.append("Be cautious with new longs")
            recommendations.append("Tighten stops")

        # TRIN-based recommendations
        if trin > 2.0:
            recommendations.append("TRIN suggests capitulation - look for reversal entry")
        elif trin < 0.5:
            recommendations.append("TRIN suggests euphoria - take profits on longs")

        # Divergence recommendations
        if divergence:
            recommendations.append("A/D divergence warns of potential reversal - reduce position size")

        return recommendations

    def _empty_analysis(self) -> BreadthAnalysis:
        """Return empty analysis when no data"""
        return BreadthAnalysis(
            ad_line=0,
            ad_line_trend='insufficient_data',
            ad_divergence=False,
            mcclellan_oscillator=0,
            mcclellan_summation=0,
            trin=1.0,
            trin_signal='no_data',
            new_highs_lows_ratio=1.0,
            percent_above_50ma=50,
            percent_above_200ma=50,
            overall_signal=BreadthSignal.NEUTRAL,
            confidence=0,
            breadth_thrust_detected=False,
            hindenburg_omen_detected=False,
            trading_signals=["Insufficient data for analysis"],
            recommendations=[]
        )


class BreadthThrust:
    """
    Specialized analyzer for Breadth Thrust signals.

    The Zweig Breadth Thrust is one of the most reliable bullish signals.
    It occurs when the market goes from extreme weakness to extreme strength
    in a short period.

    Historical performance:
    - Preceded every major bull market since 1945
    - False positive rate: ~15%
    - Average 6-month return after signal: +15%
    """

    def __init__(self):
        self.thrust_period = 10  # trading days
        self.threshold = 0.615  # 61.5% of stocks advancing

    def check_for_thrust(self, daily_data: List[DailyBreadthData]) -> Dict:
        """
        Check for Zweig Breadth Thrust.

        Conditions:
        1. In last 10 days, thrust ratio went from below 0.40 to above 0.615
        2. Thrust ratio = advances / (advances + declines)
        """
        if len(daily_data) < self.thrust_period:
            return {'detected': False, 'reason': 'insufficient_data'}

        recent = daily_data[-self.thrust_period:]

        # Calculate thrust ratios
        ratios = []
        for day in recent:
            total = day.advances + day.declines
            if total > 0:
                ratio = day.advances / total
                ratios.append(ratio)

        if not ratios:
            return {'detected': False, 'reason': 'no_valid_data'}

        min_ratio = min(ratios)
        max_ratio = max(ratios)
        min_idx = ratios.index(min_ratio)
        max_idx = ratios.index(max_ratio)

        # Check conditions
        if min_ratio < 0.40 and max_ratio > self.threshold and max_idx > min_idx:
            return {
                'detected': True,
                'min_ratio': min_ratio,
                'max_ratio': max_ratio,
                'days_to_thrust': max_idx - min_idx,
                'historical_performance': {
                    '3_month_avg': '+8%',
                    '6_month_avg': '+15%',
                    '12_month_avg': '+24%'
                },
                'recommendation': 'Strong BUY signal - add long exposure aggressively'
            }

        return {
            'detected': False,
            'current_ratio': ratios[-1] if ratios else 0,
            'max_ratio': max_ratio,
            'threshold': self.threshold
        }
