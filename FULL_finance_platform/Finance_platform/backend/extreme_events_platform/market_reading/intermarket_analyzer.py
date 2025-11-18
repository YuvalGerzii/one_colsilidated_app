"""
Intermarket Analysis Module

Analyzes relationships between four major asset classes:
- Stocks
- Bonds (yields)
- Commodities
- Currencies (USD)

Based on John Murphy's intermarket analysis framework.
These relationships help identify business cycle stages and sector rotation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, date
import statistics
import math


class BusinessCycleStage(Enum):
    """Business cycle stages"""
    EARLY_EXPANSION = "early_expansion"  # Bonds up, stocks up, commodities down
    MID_EXPANSION = "mid_expansion"  # Stocks up, commodities up
    LATE_EXPANSION = "late_expansion"  # Commodities up, bonds down
    EARLY_CONTRACTION = "early_contraction"  # Stocks down, commodities down
    MID_CONTRACTION = "mid_contraction"  # Bonds up
    LATE_CONTRACTION = "late_contraction"  # Bonds up, stocks bottoming


class MarketRegime(Enum):
    """Market environment regimes"""
    INFLATIONARY = "inflationary"
    DEFLATIONARY = "deflationary"
    GOLDILOCKS = "goldilocks"  # Low inflation, growth
    STAGFLATION = "stagflation"  # High inflation, low growth
    RISK_ON = "risk_on"
    RISK_OFF = "risk_off"


class CorrelationState(Enum):
    """Correlation states"""
    STRONGLY_POSITIVE = "strongly_positive"  # > 0.7
    POSITIVE = "positive"  # 0.3 to 0.7
    NEUTRAL = "neutral"  # -0.3 to 0.3
    NEGATIVE = "negative"  # -0.7 to -0.3
    STRONGLY_NEGATIVE = "strongly_negative"  # < -0.7


@dataclass
class AssetClassData:
    """Data for an asset class"""
    name: str
    prices: List[float]
    returns: List[float] = field(default_factory=list)
    trend: str = "neutral"  # up, down, neutral


@dataclass
class IntermarketAnalysis:
    """Complete intermarket analysis result"""
    business_cycle_stage: BusinessCycleStage
    market_regime: MarketRegime
    correlations: Dict[str, float]
    correlation_changes: Dict[str, str]  # Breakdown, normal, etc.
    leading_indicators: List[str]
    asset_class_rankings: List[Tuple[str, float]]  # Ranked by expected performance
    sector_recommendations: Dict[str, str]
    risk_level: str
    trading_signals: List[str]
    warnings: List[str]


class IntermarketAnalyzer:
    """
    Analyzes intermarket relationships to understand macro environment.

    Key relationships:
    1. Dollar ↔ Commodities: Inverse (usually)
    2. Bonds ↔ Commodities: Inverse (inflation)
    3. Bonds → Stocks: Bonds often lead stocks
    4. Commodities → Inflation → Interest Rates

    These relationships change in inflationary vs deflationary environments.
    """

    def __init__(self):
        # Normal correlation expectations
        self.normal_correlations = {
            ('stocks', 'bonds'): 0.3,  # Slightly positive in normal times
            ('bonds', 'commodities'): -0.5,  # Inverse
            ('dollar', 'commodities'): -0.6,  # Inverse
            ('stocks', 'commodities'): 0.3,  # Slightly positive
            ('dollar', 'bonds'): 0.2,  # Slightly positive (safe haven)
        }

        # Sector sensitivity to intermarket
        self.sector_sensitivity = {
            'energy': {
                'oil': 0.9,
                'dollar': -0.5,
                'bonds': -0.3
            },
            'materials': {
                'commodities': 0.8,
                'dollar': -0.6
            },
            'financials': {
                'bonds': -0.7,  # Higher rates = steeper curve = good
                'stocks': 0.8
            },
            'technology': {
                'bonds': -0.5,  # Rate sensitive
                'growth': 0.9
            },
            'utilities': {
                'bonds': 0.6,  # Bond proxy
                'rates': -0.7
            },
            'consumer_staples': {
                'bonds': 0.4,  # Defensive
                'dollar': -0.3
            },
            'consumer_discretionary': {
                'stocks': 0.9,
                'consumer': 0.8
            },
            'healthcare': {
                'defensive': 0.7,
                'dollar': 0.3
            },
            'industrials': {
                'commodities': 0.5,
                'growth': 0.7
            },
            'real_estate': {
                'bonds': -0.8,  # Very rate sensitive
                'rates': -0.9
            }
        }

    def analyze_intermarket(self,
                            stocks: AssetClassData,
                            bonds: AssetClassData,
                            commodities: AssetClassData,
                            dollar: AssetClassData) -> IntermarketAnalysis:
        """
        Main intermarket analysis.

        Args:
            stocks: Stock index data (e.g., S&P 500)
            bonds: Bond price data (e.g., 10-year Treasury)
            commodities: Commodity index data (e.g., CRB Index)
            dollar: Dollar index data (e.g., DXY)

        Returns:
            Complete intermarket analysis
        """
        # Calculate returns if not provided
        if not stocks.returns:
            stocks.returns = self._calculate_returns(stocks.prices)
        if not bonds.returns:
            bonds.returns = self._calculate_returns(bonds.prices)
        if not commodities.returns:
            commodities.returns = self._calculate_returns(commodities.prices)
        if not dollar.returns:
            dollar.returns = self._calculate_returns(dollar.prices)

        # Calculate trends
        stocks.trend = self._calculate_trend(stocks.prices)
        bonds.trend = self._calculate_trend(bonds.prices)
        commodities.trend = self._calculate_trend(commodities.prices)
        dollar.trend = self._calculate_trend(dollar.prices)

        # Calculate correlations
        correlations = self._calculate_correlations(
            stocks, bonds, commodities, dollar
        )

        # Check for correlation changes/breakdowns
        correlation_changes = self._check_correlation_changes(correlations)

        # Determine business cycle stage
        cycle_stage = self._determine_cycle_stage(
            stocks.trend, bonds.trend, commodities.trend
        )

        # Determine market regime
        regime = self._determine_market_regime(
            bonds.trend, commodities.trend, correlations
        )

        # Find leading indicators
        leaders = self._identify_leading_indicators(
            stocks, bonds, commodities, dollar
        )

        # Rank asset classes
        rankings = self._rank_asset_classes(
            stocks, bonds, commodities, dollar, cycle_stage, regime
        )

        # Generate sector recommendations
        sector_recs = self._generate_sector_recommendations(
            cycle_stage, regime, correlations
        )

        # Assess risk level
        risk_level = self._assess_risk_level(
            correlation_changes, regime, cycle_stage
        )

        # Generate signals and warnings
        signals = self._generate_signals(
            cycle_stage, regime, correlations, correlation_changes,
            stocks.trend, bonds.trend, commodities.trend, dollar.trend
        )

        warnings = self._generate_warnings(
            correlation_changes, regime, cycle_stage
        )

        return IntermarketAnalysis(
            business_cycle_stage=cycle_stage,
            market_regime=regime,
            correlations=correlations,
            correlation_changes=correlation_changes,
            leading_indicators=leaders,
            asset_class_rankings=rankings,
            sector_recommendations=sector_recs,
            risk_level=risk_level,
            trading_signals=signals,
            warnings=warnings
        )

    def _calculate_returns(self, prices: List[float]) -> List[float]:
        """Calculate period returns from prices"""
        if len(prices) < 2:
            return []

        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(ret)

        return returns

    def _calculate_trend(self, prices: List[float]) -> str:
        """Calculate price trend"""
        if len(prices) < 20:
            return "neutral"

        # Compare recent to older prices
        recent_avg = statistics.mean(prices[-10:])
        older_avg = statistics.mean(prices[-20:-10])

        change = (recent_avg - older_avg) / older_avg

        if change > 0.02:  # >2% higher
            return "up"
        elif change < -0.02:  # >2% lower
            return "down"
        else:
            return "neutral"

    def _calculate_correlations(self,
                                stocks: AssetClassData,
                                bonds: AssetClassData,
                                commodities: AssetClassData,
                                dollar: AssetClassData) -> Dict[str, float]:
        """Calculate correlations between asset classes"""
        correlations = {}

        # Get returns for correlation calculation
        min_len = min(
            len(stocks.returns), len(bonds.returns),
            len(commodities.returns), len(dollar.returns)
        )

        if min_len < 10:
            return {'insufficient_data': True}

        s_ret = stocks.returns[-min_len:]
        b_ret = bonds.returns[-min_len:]
        c_ret = commodities.returns[-min_len:]
        d_ret = dollar.returns[-min_len:]

        # Calculate pairwise correlations
        correlations['stocks_bonds'] = self._correlation(s_ret, b_ret)
        correlations['stocks_commodities'] = self._correlation(s_ret, c_ret)
        correlations['stocks_dollar'] = self._correlation(s_ret, d_ret)
        correlations['bonds_commodities'] = self._correlation(b_ret, c_ret)
        correlations['bonds_dollar'] = self._correlation(b_ret, d_ret)
        correlations['commodities_dollar'] = self._correlation(c_ret, d_ret)

        return correlations

    def _correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0

        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        den_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        den_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

        if den_x == 0 or den_y == 0:
            return 0.0

        return num / (den_x * den_y)

    def _check_correlation_changes(self, correlations: Dict[str, float]) -> Dict[str, str]:
        """
        Check for abnormal correlation changes.

        Correlation breakdowns often precede major market moves.
        """
        changes = {}

        if 'insufficient_data' in correlations:
            return {'status': 'insufficient_data'}

        # Compare to normal correlations
        checks = [
            ('stocks_bonds', ('stocks', 'bonds')),
            ('bonds_commodities', ('bonds', 'commodities')),
            ('commodities_dollar', ('dollar', 'commodities')),
        ]

        for key, normal_key in checks:
            if key in correlations:
                actual = correlations[key]
                expected = self.normal_correlations.get(normal_key, 0)

                # Check for significant deviation
                deviation = abs(actual - expected)

                if deviation > 0.5:
                    changes[key] = 'breakdown'
                elif deviation > 0.3:
                    changes[key] = 'abnormal'
                else:
                    changes[key] = 'normal'

        return changes

    def _determine_cycle_stage(self, stocks_trend: str,
                               bonds_trend: str,
                               commodities_trend: str) -> BusinessCycleStage:
        """
        Determine business cycle stage from asset trends.

        Typical cycle rotation:
        1. Bonds bottom first (early expansion)
        2. Stocks follow (mid expansion)
        3. Commodities follow (late expansion)
        4. Bonds peak (early contraction)
        5. Stocks follow (mid contraction)
        6. Commodities follow (late contraction)
        """
        if bonds_trend == 'up' and stocks_trend == 'up' and commodities_trend == 'down':
            return BusinessCycleStage.EARLY_EXPANSION
        elif stocks_trend == 'up' and commodities_trend == 'up':
            return BusinessCycleStage.MID_EXPANSION
        elif commodities_trend == 'up' and bonds_trend == 'down':
            return BusinessCycleStage.LATE_EXPANSION
        elif stocks_trend == 'down' and commodities_trend == 'down':
            return BusinessCycleStage.EARLY_CONTRACTION
        elif bonds_trend == 'up' and stocks_trend == 'down':
            return BusinessCycleStage.MID_CONTRACTION
        elif bonds_trend == 'up' and stocks_trend == 'neutral':
            return BusinessCycleStage.LATE_CONTRACTION
        else:
            return BusinessCycleStage.MID_EXPANSION  # Default

    def _determine_market_regime(self, bonds_trend: str,
                                  commodities_trend: str,
                                  correlations: Dict[str, float]) -> MarketRegime:
        """
        Determine current market regime.

        Inflationary: Commodities up, bonds down
        Deflationary: Commodities down, bonds up
        Goldilocks: Stocks up, commodities stable, low vol
        Stagflation: Commodities up, stocks down
        """
        if commodities_trend == 'up' and bonds_trend == 'down':
            return MarketRegime.INFLATIONARY
        elif commodities_trend == 'down' and bonds_trend == 'up':
            return MarketRegime.DEFLATIONARY

        # Check for risk on/off
        stocks_bonds_corr = correlations.get('stocks_bonds', 0)

        if stocks_bonds_corr > 0.5:
            return MarketRegime.RISK_OFF  # Flight to quality
        elif stocks_bonds_corr < -0.3:
            return MarketRegime.RISK_ON  # Normal rotation

        return MarketRegime.GOLDILOCKS

    def _identify_leading_indicators(self,
                                     stocks: AssetClassData,
                                     bonds: AssetClassData,
                                     commodities: AssetClassData,
                                     dollar: AssetClassData) -> List[str]:
        """
        Identify which asset classes are leading.

        Typical lead/lag:
        - Bonds lead stocks by 3-6 months
        - Commodities lead inflation
        - Dollar leads commodity prices (inverse)
        """
        leaders = []

        # Check bonds leading stocks
        if bonds.trend == 'up' and stocks.trend != 'up':
            leaders.append("Bonds rising - stocks may follow (bullish)")
        elif bonds.trend == 'down' and stocks.trend != 'down':
            leaders.append("Bonds falling - stocks may follow (bearish)")

        # Check dollar leading commodities
        if dollar.trend == 'up' and commodities.trend != 'down':
            leaders.append("Dollar rising - commodity pressure coming")
        elif dollar.trend == 'down' and commodities.trend != 'up':
            leaders.append("Dollar falling - commodity rally likely")

        # Commodities leading inflation expectations
        if commodities.trend == 'up':
            leaders.append("Rising commodities signal inflation ahead")
        elif commodities.trend == 'down':
            leaders.append("Falling commodities signal disinflation")

        return leaders

    def _rank_asset_classes(self,
                            stocks: AssetClassData,
                            bonds: AssetClassData,
                            commodities: AssetClassData,
                            dollar: AssetClassData,
                            cycle: BusinessCycleStage,
                            regime: MarketRegime) -> List[Tuple[str, float]]:
        """
        Rank asset classes by expected performance.

        Rankings based on cycle stage and regime.
        """
        rankings = {
            'stocks': 0.5,
            'bonds': 0.5,
            'commodities': 0.5,
            'dollar': 0.5
        }

        # Adjust for cycle stage
        cycle_adjustments = {
            BusinessCycleStage.EARLY_EXPANSION: {
                'stocks': 0.3, 'bonds': 0.2, 'commodities': -0.2
            },
            BusinessCycleStage.MID_EXPANSION: {
                'stocks': 0.4, 'commodities': 0.2
            },
            BusinessCycleStage.LATE_EXPANSION: {
                'commodities': 0.3, 'bonds': -0.3
            },
            BusinessCycleStage.EARLY_CONTRACTION: {
                'stocks': -0.3, 'bonds': 0.2, 'commodities': -0.2
            },
            BusinessCycleStage.MID_CONTRACTION: {
                'bonds': 0.4, 'stocks': -0.2
            },
            BusinessCycleStage.LATE_CONTRACTION: {
                'bonds': 0.3, 'stocks': 0.1
            }
        }

        if cycle in cycle_adjustments:
            for asset, adj in cycle_adjustments[cycle].items():
                rankings[asset] += adj

        # Adjust for regime
        regime_adjustments = {
            MarketRegime.INFLATIONARY: {
                'commodities': 0.3, 'bonds': -0.3, 'dollar': -0.2
            },
            MarketRegime.DEFLATIONARY: {
                'bonds': 0.4, 'commodities': -0.3, 'dollar': 0.2
            },
            MarketRegime.RISK_OFF: {
                'bonds': 0.3, 'dollar': 0.2, 'stocks': -0.2
            },
            MarketRegime.RISK_ON: {
                'stocks': 0.3, 'commodities': 0.2, 'bonds': -0.2
            }
        }

        if regime in regime_adjustments:
            for asset, adj in regime_adjustments[regime].items():
                rankings[asset] += adj

        # Sort by ranking
        sorted_rankings = sorted(
            rankings.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_rankings

    def _generate_sector_recommendations(self,
                                          cycle: BusinessCycleStage,
                                          regime: MarketRegime,
                                          correlations: Dict) -> Dict[str, str]:
        """Generate sector recommendations based on intermarket analysis"""
        recommendations = {}

        # Cycle-based recommendations
        if cycle == BusinessCycleStage.EARLY_EXPANSION:
            recommendations['overweight'] = "Financials, Technology, Consumer Discretionary"
            recommendations['underweight'] = "Utilities, Consumer Staples"

        elif cycle == BusinessCycleStage.MID_EXPANSION:
            recommendations['overweight'] = "Technology, Industrials, Materials"
            recommendations['underweight'] = "Utilities, Real Estate"

        elif cycle == BusinessCycleStage.LATE_EXPANSION:
            recommendations['overweight'] = "Energy, Materials, Commodities"
            recommendations['underweight'] = "Financials, Technology"

        elif cycle == BusinessCycleStage.EARLY_CONTRACTION:
            recommendations['overweight'] = "Consumer Staples, Healthcare, Utilities"
            recommendations['underweight'] = "Energy, Materials, Industrials"

        elif cycle == BusinessCycleStage.MID_CONTRACTION:
            recommendations['overweight'] = "Utilities, Consumer Staples, Healthcare"
            recommendations['underweight'] = "Financials, Consumer Discretionary"

        elif cycle == BusinessCycleStage.LATE_CONTRACTION:
            recommendations['overweight'] = "Financials (early), Technology (early)"
            recommendations['underweight'] = "Energy, Materials"

        # Regime adjustments
        if regime == MarketRegime.INFLATIONARY:
            recommendations['inflation_plays'] = "Energy, Materials, TIPS, Gold"
        elif regime == MarketRegime.DEFLATIONARY:
            recommendations['deflation_plays'] = "Treasuries, Quality Growth, USD"
        elif regime == MarketRegime.RISK_OFF:
            recommendations['safety'] = "Treasuries, Gold, JPY, CHF"

        return recommendations

    def _assess_risk_level(self,
                           correlation_changes: Dict[str, str],
                           regime: MarketRegime,
                           cycle: BusinessCycleStage) -> str:
        """Assess overall risk level from intermarket signals"""

        risk_score = 0

        # Correlation breakdowns increase risk
        breakdowns = sum(1 for v in correlation_changes.values() if v == 'breakdown')
        risk_score += breakdowns * 2

        # Certain regimes are higher risk
        if regime in [MarketRegime.DEFLATIONARY, MarketRegime.STAGFLATION]:
            risk_score += 2

        # Late cycle is higher risk
        if cycle in [BusinessCycleStage.LATE_EXPANSION,
                    BusinessCycleStage.EARLY_CONTRACTION]:
            risk_score += 1

        if risk_score >= 4:
            return "HIGH"
        elif risk_score >= 2:
            return "ELEVATED"
        else:
            return "NORMAL"

    def _generate_signals(self, cycle: BusinessCycleStage,
                          regime: MarketRegime,
                          correlations: Dict,
                          correlation_changes: Dict,
                          stocks_trend: str,
                          bonds_trend: str,
                          commodities_trend: str,
                          dollar_trend: str) -> List[str]:
        """Generate trading signals from intermarket analysis"""
        signals = []

        # Cycle signals
        signals.append(f"Business cycle: {cycle.value}")

        if cycle == BusinessCycleStage.EARLY_EXPANSION:
            signals.append("Early expansion - favor risk assets (stocks, credit)")
        elif cycle == BusinessCycleStage.LATE_EXPANSION:
            signals.append("Late expansion - favor commodities, reduce duration")
        elif cycle == BusinessCycleStage.EARLY_CONTRACTION:
            signals.append("Early contraction - reduce risk, favor cash/bonds")

        # Regime signals
        signals.append(f"Market regime: {regime.value}")

        if regime == MarketRegime.INFLATIONARY:
            signals.append("Inflationary environment - favor real assets")
        elif regime == MarketRegime.DEFLATIONARY:
            signals.append("Deflationary pressure - favor quality, duration")

        # Correlation signals
        for key, status in correlation_changes.items():
            if status == 'breakdown':
                signals.append(f"Correlation breakdown: {key} - regime change likely")

        # Trend signals
        if bonds_trend == 'down' and commodities_trend == 'up':
            signals.append("Classic inflation signal: bonds down, commodities up")
        elif bonds_trend == 'up' and stocks_trend == 'down':
            signals.append("Flight to quality: bonds up, stocks down")

        # Dollar signals
        if dollar_trend == 'up':
            signals.append("Strong dollar - headwind for commodities and EM")
        elif dollar_trend == 'down':
            signals.append("Weak dollar - tailwind for commodities and EM")

        return signals

    def _generate_warnings(self, correlation_changes: Dict,
                           regime: MarketRegime,
                           cycle: BusinessCycleStage) -> List[str]:
        """Generate risk warnings from intermarket analysis"""
        warnings = []

        # Correlation breakdown warnings
        breakdowns = [k for k, v in correlation_changes.items() if v == 'breakdown']
        if breakdowns:
            warnings.append(f"Correlation breakdowns detected: {', '.join(breakdowns)}")
            warnings.append("Historical correlations may not hold - adjust strategies")

        # Regime warnings
        if regime == MarketRegime.STAGFLATION:
            warnings.append("Stagflation warning - historically worst for portfolios")
        elif regime == MarketRegime.DEFLATIONARY:
            warnings.append("Deflation risk - avoid commodities, favor quality")

        # Cycle warnings
        if cycle == BusinessCycleStage.LATE_EXPANSION:
            warnings.append("Late cycle - recession risk elevated")
        elif cycle == BusinessCycleStage.EARLY_CONTRACTION:
            warnings.append("Contraction phase - reduce risk exposure")

        return warnings


class CurrencyIntermarket:
    """
    Specialized analysis for currency intermarket relationships.

    Key relationships:
    - USD/JPY: Risk-on/off proxy
    - AUD/JPY: Carry trade, risk sentiment
    - USD/CAD: Oil correlation
    - EUR/USD: Rate differentials
    """

    def __init__(self):
        self.currency_correlations = {
            ('USD', 'oil'): -0.6,
            ('CAD', 'oil'): 0.7,
            ('AUD', 'commodities'): 0.8,
            ('JPY', 'risk'): -0.7,  # Safe haven
            ('CHF', 'risk'): -0.6,  # Safe haven
        }

    def analyze_fx_signals(self,
                           usd_index: List[float],
                           vix: List[float],
                           oil: List[float]) -> Dict:
        """
        Analyze currency signals for intermarket insights.

        Returns signals about risk sentiment and asset class implications.
        """
        if len(usd_index) < 10 or len(vix) < 10:
            return {'status': 'insufficient_data'}

        signals = []

        # USD trend
        usd_trend = self._simple_trend(usd_index)
        if usd_trend == 'up':
            signals.append("Strong USD = headwind for commodities, EM assets")
            signals.append("Expect pressure on: gold, oil, EM equities")
        elif usd_trend == 'down':
            signals.append("Weak USD = tailwind for commodities, EM assets")
            signals.append("Expect strength in: gold, oil, EM equities")

        # VIX signals
        vix_level = vix[-1]
        if vix_level > 30:
            signals.append(f"VIX elevated ({vix_level:.0f}) - risk-off: long JPY, CHF")
        elif vix_level < 15:
            signals.append(f"VIX complacent ({vix_level:.0f}) - risk-on: short JPY, long AUD")

        return {
            'usd_trend': usd_trend,
            'vix_level': vix_level,
            'signals': signals,
            'fx_recommendations': self._get_fx_recommendations(usd_trend, vix_level)
        }

    def _simple_trend(self, prices: List[float]) -> str:
        """Simple trend calculation"""
        if len(prices) < 10:
            return 'neutral'

        recent = statistics.mean(prices[-5:])
        older = statistics.mean(prices[-10:-5])

        if recent > older * 1.01:
            return 'up'
        elif recent < older * 0.99:
            return 'down'
        return 'neutral'

    def _get_fx_recommendations(self, usd_trend: str, vix: float) -> List[str]:
        """Get FX trading recommendations"""
        recs = []

        if vix > 30:
            recs.append("Long JPY/USD or CHF/USD (safe haven)")
            recs.append("Short AUD/JPY (risk-off carry unwind)")
        elif vix < 15:
            recs.append("Long AUD/JPY (carry trade)")
            recs.append("Long EM currencies")

        if usd_trend == 'up':
            recs.append("Short commodity currencies (CAD, AUD, NOK)")
        elif usd_trend == 'down':
            recs.append("Long commodity currencies (CAD, AUD, NOK)")

        return recs
