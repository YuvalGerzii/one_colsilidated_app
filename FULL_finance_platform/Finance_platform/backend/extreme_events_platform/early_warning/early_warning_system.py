"""
Early Warning System for Financial Crises (V6.0)

Detects crises BEFORE they happen using leading indicators and anomaly detection.

Based on research of 2008 financial crisis warning signs:
- Credit-to-GDP gap (most powerful predictor)
- TED spread (liquidity stress)
- VIX term structure (fear gauge)
- Housing price-to-income ratios
- Bank leverage ratios
- Credit default swap spreads
- Yield curve inversions
- Current account deficits
- Central bank reserves

Key insight: The 2008 crisis HAD warning signs 12-24 months in advance:
- May 2006: JPMorgan warned of housing downturn
- Aug 2006: Yield curve inverted (recession signal)
- Nov 2006: UBS warned of impending housing crisis
- 2007: ABX index (subprime MBS) collapsed
- 2007: TED spread spiked from 0.5% to 2%+

This system tracks 15+ leading indicators with proven track records.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import numpy as np


class CrisisType(Enum):
    """Types of crises that can be predicted"""
    BANKING_CRISIS = "banking_crisis"
    HOUSING_BUBBLE = "housing_bubble"
    CURRENCY_CRISIS = "currency_crisis"
    SOVEREIGN_DEBT = "sovereign_debt"
    MARKET_CRASH = "market_crash"
    RECESSION = "recession"
    INFLATION_SPIRAL = "inflation_spiral"
    LIQUIDITY_CRISIS = "liquidity_crisis"


class AlertLevel(Enum):
    """Alert severity levels"""
    GREEN = "green"  # Normal conditions
    YELLOW = "yellow"  # Watch - some indicators elevated
    ORANGE = "orange"  # Warning - multiple indicators flashing
    RED = "red"  # Critical - crisis imminent (0-6 months)
    BLACK = "black"  # Emergency - crisis occurring now


@dataclass
class Indicator:
    """An early warning indicator"""
    name: str
    current_value: float
    threshold_warning: float  # Yellow alert
    threshold_critical: float  # Red alert
    historical_avg: float
    z_score: float
    trend: str  # 'rising', 'falling', 'stable'
    reliability: float  # 0-1 (how reliable historically)
    lead_time_months: int  # Typical lead time before crisis


@dataclass
class EarlyWarning:
    """Early warning signal"""
    crisis_type: CrisisType
    alert_level: AlertLevel
    probability: float  # 0-1
    estimated_months_until: int  # Months until crisis
    key_indicators: List[Indicator]
    confidence: float  # Overall confidence in prediction
    similar_historical_events: List[str]
    recommended_actions: List[str]


class EarlyWarningSystem:
    """
    Early Warning System for detecting financial crises before they happen.

    Uses 15+ leading indicators with historical validation.
    """

    def __init__(self):
        """Initialize early warning system"""

        # Define indicator thresholds based on historical crises
        self.indicator_thresholds = self._define_thresholds()

        # Indicator weights (based on research - Credit-to-GDP is strongest)
        self.indicator_weights = {
            'credit_to_gdp_gap': 0.30,  # MOST POWERFUL predictor
            'ted_spread': 0.15,
            'vix_term_structure': 0.10,
            'housing_price_to_income': 0.12,
            'bank_leverage': 0.10,
            'cds_spreads': 0.08,
            'yield_curve': 0.08,
            'current_account': 0.04,
            'reserves_to_debt': 0.03,
        }

        # Historical crisis patterns (for pattern matching)
        self.crisis_fingerprints = self._load_crisis_fingerprints()

    def _define_thresholds(self) -> Dict:
        """Define warning thresholds for each indicator"""

        return {
            # Credit-to-GDP gap (BIS threshold)
            'credit_to_gdp_gap': {
                'yellow': 2.0,  # 2pp above trend
                'orange': 6.0,  # 6pp (historical avg before crisis)
                'red': 10.0,  # 10pp+ = crisis very likely
                'historical_avg': 0.0,
                'reliability': 0.85,  # 85% accuracy
                'lead_time': 24  # 2 years average
            },

            # TED spread (LIBOR - T-bill)
            'ted_spread': {
                'yellow': 0.50,  # 50 bps (normal max)
                'orange': 1.00,  # 100 bps (stress)
                'red': 2.00,  # 200 bps+ (crisis - 2008 peak = 4.58%)
                'historical_avg': 0.25,
                'reliability': 0.75,
                'lead_time': 6  # 6 months
            },

            # VIX term structure (contango = calm, backwardation = fear)
            'vix_term_structure': {
                'yellow': -2.0,  # Slight backwardation
                'orange': -5.0,  # Strong backwardation
                'red': -10.0,  # Extreme backwardation
                'historical_avg': 2.0,  # Normal contango
                'reliability': 0.65,
                'lead_time': 3
            },

            # Housing price-to-income ratio
            'housing_price_to_income': {
                'yellow': 5.0,  # Historical avg = 4.0
                'orange': 6.0,  # Bubble territory
                'red': 7.0,  # Severe bubble (2006 = 6.5)
                'historical_avg': 4.0,
                'reliability': 0.80,
                'lead_time': 18  # 18 months before housing crash
            },

            # Bank leverage ratio (assets/equity)
            'bank_leverage': {
                'yellow': 15.0,  # Moderate leverage
                'orange': 25.0,  # High leverage
                'red': 35.0,  # Extreme (2008 = 30-40x)
                'historical_avg': 10.0,
                'reliability': 0.78,
                'lead_time': 12
            },

            # Credit default swap spreads (basis points)
            'cds_spreads': {
                'yellow': 150,  # bps
                'orange': 300,
                'red': 500,  # 2008 peak > 1000 bps
                'historical_avg': 50,
                'reliability': 0.70,
                'lead_time': 9
            },

            # Yield curve (10Y - 2Y)
            'yield_curve': {
                'yellow': 0.0,  # Flat
                'orange': -0.25,  # Inverted
                'red': -0.50,  # Deeply inverted (Aug 2006)
                'historical_avg': 1.0,
                'reliability': 0.82,  # Very reliable for recessions
                'lead_time': 18  # 12-24 months before recession
            },

            # Current account deficit (% of GDP)
            'current_account': {
                'yellow': -3.0,  # -3% deficit
                'orange': -5.0,
                'red': -7.0,
                'historical_avg': -2.0,
                'reliability': 0.60,
                'lead_time': 24
            },

            # Reserves to short-term debt ratio
            'reserves_to_debt': {
                'yellow': 1.0,  # 100% coverage
                'orange': 0.75,
                'red': 0.50,  # Insufficient reserves
                'historical_avg': 1.5,
                'reliability': 0.72,
                'lead_time': 15
            },

            # Household debt to GDP
            'household_debt_to_gdp': {
                'yellow': 75.0,  # % of GDP
                'orange': 90.0,
                'red': 100.0,  # 2008 = 98%
                'historical_avg': 60.0,
                'reliability': 0.75,
                'lead_time': 18
            },

            # Corporate debt to GDP
            'corporate_debt_to_gdp': {
                'yellow': 75.0,
                'orange': 90.0,
                'red': 100.0,
                'historical_avg': 65.0,
                'reliability': 0.68,
                'lead_time': 12
            },

            # Banking sector concentration (Herfindahl index)
            'bank_concentration': {
                'yellow': 0.15,
                'orange': 0.20,
                'red': 0.25,  # Too concentrated = systemic risk
                'historical_avg': 0.10,
                'reliability': 0.55,
                'lead_time': 24
            },

            # Cross-border bank lending growth (% YoY)
            'cross_border_lending': {
                'yellow': 15.0,  # % growth
                'orange': 25.0,
                'red': 35.0,  # Unsustainable growth
                'historical_avg': 5.0,
                'reliability': 0.65,
                'lead_time': 18
            },

            # Real effective exchange rate (% overvaluation)
            'reer_overvaluation': {
                'yellow': 10.0,  # % overvalued
                'orange': 20.0,
                'red': 30.0,
                'historical_avg': 0.0,
                'reliability': 0.70,
                'lead_time': 12
            },

            # Stock market P/E ratio
            'market_pe_ratio': {
                'yellow': 20.0,  # Historical avg = 15-16
                'orange': 25.0,
                'red': 30.0,  # Bubble territory
                'historical_avg': 16.0,
                'reliability': 0.60,  # Less reliable alone
                'lead_time': 12
            },
        }

    def _load_crisis_fingerprints(self) -> Dict:
        """Load historical crisis patterns for matching"""

        return {
            '2008_financial_crisis': {
                'indicators': {
                    'credit_to_gdp_gap': 15.0,  # Massive credit boom
                    'housing_price_to_income': 6.5,
                    'bank_leverage': 35.0,
                    'household_debt_to_gdp': 98.0,
                    'yield_curve': -0.50,  # Inverted Aug 2006
                    'cds_spreads': 1000.0,  # By 2008
                    'ted_spread': 4.58,  # Peak Sept 2008
                },
                'timeline': {
                    '24_months_before': 'Yield curve inverts (Aug 2006)',
                    '18_months_before': 'Housing prices peak, start declining',
                    '12_months_before': 'Subprime lenders start failing',
                    '6_months_before': 'Bear Stearns hedge funds collapse',
                    '3_months_before': 'Northern Rock bank run (UK)',
                    '0_months': 'Lehman Brothers bankruptcy (Sept 2008)'
                },
                'lessons': [
                    'Credit-to-GDP gap was screaming red 2 years before',
                    'Yield curve inversion gave 18-month warning',
                    'Housing bubble obvious to those watching ratios',
                    'TED spread spiked 6 months before crisis peak',
                    'CDS spreads on MBS rose sharply in 2007'
                ]
            },

            '2000_dotcom_bubble': {
                'indicators': {
                    'market_pe_ratio': 45.0,  # NASDAQ P/E absurd
                    'credit_to_gdp_gap': 8.0,
                    'yield_curve': -0.30,  # Inverted 2000
                },
                'timeline': {
                    '12_months_before': 'Fed raises rates to cool economy',
                    '6_months_before': 'NASDAQ hits 5000 (March 2000)',
                    '3_months_before': 'Tech IPOs at absurd valuations',
                    '0_months': 'NASDAQ crashes -78% over 2 years'
                },
                'lessons': [
                    'P/E ratios at historical extremes',
                    'Yield curve inversion preceded crash',
                    'Valuations disconnected from fundamentals'
                ]
            },

            '1997_asian_crisis': {
                'indicators': {
                    'current_account': -8.0,  # Thailand -8% deficit
                    'reer_overvaluation': 25.0,
                    'cross_border_lending': 40.0,
                    'reserves_to_debt': 0.60,
                },
                'timeline': {
                    '18_months_before': 'Current account deficits widen',
                    '12_months_before': 'Real estate bubbles form',
                    '6_months_before': 'Central bank reserves depleting',
                    '0_months': 'Thai baht devaluation triggers contagion'
                },
                'lessons': [
                    'Current account deficits matter',
                    'Currency overvaluation + low reserves = crisis',
                    'Cross-border lending boom preceded bust'
                ]
            },

            '2011_european_debt': {
                'indicators': {
                    'sovereign_debt_to_gdp': 150.0,  # Greece
                    'cds_spreads': 3000.0,  # Greek CDS
                    'bank_concentration': 0.30,
                },
                'timeline': {
                    '24_months_before': 'Greece debt levels rising',
                    '12_months_before': 'CDS spreads widen',
                    '6_months_before': 'Bond yields spike',
                    '0_months': 'Greek debt crisis, contagion to Spain/Italy'
                },
                'lessons': [
                    'Sovereign CDS spreads leading indicator',
                    'Debt-to-GDP >100% unsustainable',
                    'Banking concentration amplifies contagion'
                ]
            },

            '2020_covid_crash': {
                'indicators': {
                    'vix_term_structure': -15.0,  # Extreme backwardation
                    'credit_to_gdp_gap': 12.0,  # Pre-covid credit boom
                    'corporate_debt_to_gdp': 95.0,
                },
                'timeline': {
                    '2_months_before': 'Pandemic spreads in China',
                    '1_month_before': 'Italy lockdowns begin',
                    '2_weeks_before': 'Market volatility spikes',
                    '0_months': 'Circuit breakers triggered, -35% crash'
                },
                'lessons': [
                    'Black swan events can trigger despite low warning',
                    'High corporate debt amplified downturn',
                    'VIX backwardation preceded crash'
                ]
            }
        }

    def analyze_current_conditions(
        self,
        current_data: Dict[str, float],
        region: str = 'US'
    ) -> List[EarlyWarning]:
        """
        Analyze current market conditions for early warning signals

        Args:
            current_data: Dictionary of current indicator values
            region: Geographic region

        Returns:
            List of early warning signals
        """

        warnings = []

        # Calculate indicator status
        indicators_status = []
        for indicator_name, value in current_data.items():
            if indicator_name in self.indicator_thresholds:
                indicator = self._evaluate_indicator(indicator_name, value)
                indicators_status.append(indicator)

        # Detect potential crises
        potential_crises = self._detect_crisis_types(indicators_status)

        # Generate warnings for each potential crisis
        for crisis_type, data in potential_crises.items():
            warning = self._generate_warning(
                crisis_type=crisis_type,
                indicators=data['indicators'],
                overall_score=data['score']
            )
            if warning.alert_level != AlertLevel.GREEN:
                warnings.append(warning)

        # Sort by severity
        severity_order = {
            AlertLevel.BLACK: 5,
            AlertLevel.RED: 4,
            AlertLevel.ORANGE: 3,
            AlertLevel.YELLOW: 2,
            AlertLevel.GREEN: 1
        }
        warnings.sort(key=lambda w: severity_order[w.alert_level], reverse=True)

        return warnings

    def _evaluate_indicator(self, name: str, current_value: float) -> Indicator:
        """Evaluate single indicator"""

        config = self.indicator_thresholds[name]

        # Calculate z-score
        std_dev = abs(config['red'] - config['historical_avg']) / 2
        z_score = (current_value - config['historical_avg']) / max(std_dev, 0.01)

        # Determine trend (simplified - in production would use time series)
        if current_value > config['orange']:
            trend = 'rising'
        elif current_value < config['yellow']:
            trend = 'falling'
        else:
            trend = 'stable'

        return Indicator(
            name=name,
            current_value=current_value,
            threshold_warning=config['yellow'],
            threshold_critical=config['red'],
            historical_avg=config['historical_avg'],
            z_score=z_score,
            trend=trend,
            reliability=config['reliability'],
            lead_time_months=config['lead_time']
        )

    def _detect_crisis_types(self, indicators: List[Indicator]) -> Dict:
        """Detect which crisis types are likely"""

        potential_crises = {}

        # Banking crisis indicators
        banking_indicators = [i for i in indicators if i.name in [
            'credit_to_gdp_gap', 'bank_leverage', 'ted_spread',
            'cds_spreads', 'bank_concentration'
        ]]
        if banking_indicators:
            score = self._calculate_crisis_score(banking_indicators)
            if score > 0.3:
                potential_crises[CrisisType.BANKING_CRISIS] = {
                    'indicators': banking_indicators,
                    'score': score
                }

        # Housing bubble indicators
        housing_indicators = [i for i in indicators if i.name in [
            'housing_price_to_income', 'household_debt_to_gdp',
            'credit_to_gdp_gap'
        ]]
        if housing_indicators:
            score = self._calculate_crisis_score(housing_indicators)
            if score > 0.3:
                potential_crises[CrisisType.HOUSING_BUBBLE] = {
                    'indicators': housing_indicators,
                    'score': score
                }

        # Currency crisis indicators
        currency_indicators = [i for i in indicators if i.name in [
            'current_account', 'reserves_to_debt', 'reer_overvaluation'
        ]]
        if currency_indicators:
            score = self._calculate_crisis_score(currency_indicators)
            if score > 0.3:
                potential_crises[CrisisType.CURRENCY_CRISIS] = {
                    'indicators': currency_indicators,
                    'score': score
                }

        # Recession indicators
        recession_indicators = [i for i in indicators if i.name in [
            'yield_curve', 'credit_to_gdp_gap', 'ted_spread'
        ]]
        if recession_indicators:
            score = self._calculate_crisis_score(recession_indicators)
            if score > 0.3:
                potential_crises[CrisisType.RECESSION] = {
                    'indicators': recession_indicators,
                    'score': score
                }

        # Market crash indicators
        crash_indicators = [i for i in indicators if i.name in [
            'market_pe_ratio', 'vix_term_structure', 'credit_to_gdp_gap'
        ]]
        if crash_indicators:
            score = self._calculate_crisis_score(crash_indicators)
            if score > 0.3:
                potential_crises[CrisisType.MARKET_CRASH] = {
                    'indicators': crash_indicators,
                    'score': score
                }

        return potential_crises

    def _calculate_crisis_score(self, indicators: List[Indicator]) -> float:
        """Calculate overall crisis probability score"""

        if not indicators:
            return 0.0

        weighted_score = 0.0
        total_weight = 0.0

        for indicator in indicators:
            # Get weight
            weight = self.indicator_weights.get(indicator.name, 0.05)

            # Calculate individual score based on thresholds
            if indicator.current_value >= indicator.threshold_critical:
                ind_score = 1.0
            elif indicator.current_value >= indicator.threshold_warning:
                # Linear interpolation between warning and critical
                range_size = indicator.threshold_critical - indicator.threshold_warning
                position = indicator.current_value - indicator.threshold_warning
                ind_score = 0.5 + 0.5 * (position / max(range_size, 0.01))
            else:
                ind_score = 0.0

            # Weight by reliability
            ind_score *= indicator.reliability

            weighted_score += ind_score * weight
            total_weight += weight

        return weighted_score / max(total_weight, 0.01)

    def _generate_warning(
        self,
        crisis_type: CrisisType,
        indicators: List[Indicator],
        overall_score: float
    ) -> EarlyWarning:
        """Generate early warning"""

        # Determine alert level
        if overall_score >= 0.8:
            alert_level = AlertLevel.RED
        elif overall_score >= 0.6:
            alert_level = AlertLevel.ORANGE
        elif overall_score >= 0.4:
            alert_level = AlertLevel.YELLOW
        else:
            alert_level = AlertLevel.GREEN

        # Estimate lead time (use shortest lead time of critical indicators)
        critical_indicators = [i for i in indicators
                             if i.current_value >= i.threshold_critical]
        if critical_indicators:
            lead_time = min([i.lead_time_months for i in critical_indicators])
        else:
            lead_time = max([i.lead_time_months for i in indicators]) if indicators else 12

        # Find similar historical events
        similar_events = self._find_similar_patterns(indicators, crisis_type)

        # Generate recommendations
        recommendations = self._get_recommendations(crisis_type, alert_level)

        return EarlyWarning(
            crisis_type=crisis_type,
            alert_level=alert_level,
            probability=overall_score,
            estimated_months_until=lead_time,
            key_indicators=sorted(indicators, key=lambda x: abs(x.z_score), reverse=True)[:5],
            confidence=np.mean([i.reliability for i in indicators]),
            similar_historical_events=similar_events,
            recommended_actions=recommendations
        )

    def _find_similar_patterns(
        self,
        indicators: List[Indicator],
        crisis_type: CrisisType
    ) -> List[str]:
        """Find similar historical crisis patterns"""

        similar = []

        # Check each historical crisis
        for crisis_name, crisis_data in self.crisis_fingerprints.items():
            # Calculate similarity score
            matches = 0
            total = 0

            for indicator in indicators:
                if indicator.name in crisis_data['indicators']:
                    total += 1
                    historical_value = crisis_data['indicators'][indicator.name]

                    # Check if current value is similar (within 30%)
                    if abs(indicator.current_value - historical_value) / max(historical_value, 0.01) < 0.3:
                        matches += 1

            if total > 0 and matches / total > 0.6:
                similar.append(crisis_name)

        return similar

    def _get_recommendations(self, crisis_type: CrisisType, alert_level: AlertLevel) -> List[str]:
        """Get recommended actions"""

        recommendations = []

        if alert_level == AlertLevel.RED or alert_level == AlertLevel.BLACK:
            recommendations.extend([
                "URGENT: Reduce equity exposure by 40-60%",
                "Raise cash to 30%+ of portfolio",
                "Implement defensive hedges (VIX calls, puts)",
                "Shift to safe havens (treasuries, gold)",
                "Review counterparty risk exposure",
                "Prepare for liquidity squeeze"
            ])

        elif alert_level == AlertLevel.ORANGE:
            recommendations.extend([
                "WARNING: Reduce equity exposure by 20-30%",
                "Increase defensive positioning",
                "Add 15-20% hedges",
                "Monitor daily for deterioration",
                "Reduce leverage"
            ])

        elif alert_level == AlertLevel.YELLOW:
            recommendations.extend([
                "WATCH: Begin defensive positioning",
                "Add 5-10% hedges",
                "Monitor key indicators weekly",
                "Prepare contingency plans"
            ])

        # Crisis-specific recommendations
        if crisis_type == CrisisType.BANKING_CRISIS:
            recommendations.append("Review bank exposure, favor well-capitalized banks")
            recommendations.append("Monitor TED spread and CDS spreads daily")

        elif crisis_type == CrisisType.HOUSING_BUBBLE:
            recommendations.append("Reduce real estate exposure")
            recommendations.append("Short homebuilders and mortgage lenders")

        elif crisis_type == CrisisType.CURRENCY_CRISIS:
            recommendations.append("Hedge currency exposure")
            recommendations.append("Diversify into hard currencies (CHF, JPY)")

        return recommendations

    def backtest_indicator_performance(
        self,
        historical_crises: List[str]
    ) -> Dict:
        """
        Backtest how well indicators predicted historical crises

        Returns accuracy metrics for each indicator
        """

        results = {}

        for crisis_name in historical_crises:
            if crisis_name in self.crisis_fingerprints:
                crisis = self.crisis_fingerprints[crisis_name]

                results[crisis_name] = {
                    'indicators_red': [],
                    'lead_time_actual': crisis.get('timeline', {})
                }

                # Check which indicators were in red zone
                for ind_name, value in crisis['indicators'].items():
                    if ind_name in self.indicator_thresholds:
                        threshold = self.indicator_thresholds[ind_name]['red']
                        if value >= threshold:
                            results[crisis_name]['indicators_red'].append(ind_name)

        return results


def main():
    """Example usage"""

    ews = EarlyWarningSystem()

    # Example 1: Simulate 2007 conditions (1 year before 2008 crisis)
    print("=== Example 1: Pre-2008 Crisis Conditions (2007) ===")
    pre_2008_data = {
        'credit_to_gdp_gap': 12.0,  # Massive credit boom
        'housing_price_to_income': 6.3,  # Bubble
        'bank_leverage': 32.0,  # Very high
        'household_debt_to_gdp': 95.0,
        'yield_curve': -0.45,  # Inverted
        'ted_spread': 0.80,  # Starting to rise
        'cds_spreads': 200.0,  # Rising
    }

    warnings = ews.analyze_current_conditions(pre_2008_data)

    for warning in warnings:
        print(f"\n{warning.crisis_type.value.upper()}")
        print(f"Alert Level: {warning.alert_level.value}")
        print(f"Probability: {warning.probability:.1%}")
        print(f"Estimated time until crisis: {warning.estimated_months_until} months")
        print(f"Confidence: {warning.confidence:.1%}")
        print(f"\nKey indicators:")
        for ind in warning.key_indicators[:3]:
            print(f"  - {ind.name}: {ind.current_value:.2f} (threshold: {ind.threshold_critical:.2f}, z-score: {ind.z_score:.1f})")
        print(f"\nSimilar to: {', '.join(warning.similar_historical_events)}")
        print(f"\nTop recommendations:")
        for rec in warning.recommended_actions[:3]:
            print(f"  → {rec}")

    # Example 2: Current normal conditions
    print("\n\n=== Example 2: Normal Market Conditions ===")
    normal_data = {
        'credit_to_gdp_gap': 1.5,
        'housing_price_to_income': 4.2,
        'bank_leverage': 12.0,
        'yield_curve': 0.8,
        'ted_spread': 0.30,
    }

    warnings = ews.analyze_current_conditions(normal_data)
    if warnings:
        print(f"Warnings detected: {len(warnings)}")
    else:
        print("No warnings - market conditions normal (GREEN)")


if __name__ == "__main__":
    main()
