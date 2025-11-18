"""
Recession Agent - Analyzes recession risk and economic contractions
Based on 2025 research and predictive indicators
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class RecessionAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing recession events
    Uses yield curve, labor market, GDP, and sentiment indicators
    """

    def __init__(self, config: Dict):
        super().__init__('recession', config)
        self.indicator_weights = {
            'yield_curve': 0.30,  # Best predictor
            'unemployment': 0.25,
            'gdp_growth': 0.20,
            'consumer_confidence': 0.15,
            'manufacturing_pmi': 0.10
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze recession risk and impact

        Args:
            event_data: {
                'yield_curve_spread': float,  # 10yr - 3mo spread
                'unemployment_rate': float,
                'unemployment_change_6m': float,
                'gdp_growth_q1': float,
                'gdp_growth_q2': float,
                'consumer_confidence_index': float,
                'manufacturing_pmi': float,
                'probability_estimate': float,  # Optional
                'expected_depth': str,  # 'mild', 'moderate', 'severe'
                'geographic_scope': str
            }

        Returns:
            Comprehensive recession analysis
        """
        # Calculate recession probability
        recession_prob = self._calculate_recession_probability(event_data)

        # Assess severity if recession occurs
        severity = self.assess_severity(event_data)

        # Predict market impact
        market_predictions = self.predict_market_impact(event_data)

        # Analyze leading indicators
        indicators_analysis = self._analyze_leading_indicators(event_data)

        # Determine recession phase
        phase = self._determine_recession_phase(event_data, recession_prob)

        # Sector impact analysis
        sector_impact = self._analyze_sector_resilience(event_data)

        analysis = {
            'severity': severity,
            'recession_probability': recession_prob,
            'leading_indicators': indicators_analysis,
            'recession_phase': phase,
            'market_predictions': market_predictions,
            'sectoral_impact': sector_impact,
            'policy_recommendations': self._generate_policy_recommendations(event_data, recession_prob),
            'investment_strategy': self._generate_investment_strategy(event_data, recession_prob),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def _calculate_recession_probability(self, event_data: Dict) -> float:
        """
        Calculate recession probability from multiple indicators
        Based on 2025 Fed and economic research
        """
        probability = 0.0

        # 1. Yield Curve (most reliable predictor)
        yield_spread = event_data.get('yield_curve_spread', 0)
        if yield_spread < 0:  # Inverted
            months_inverted = abs(event_data.get('months_inverted', 6))
            # Probability increases with duration of inversion
            yield_prob = min(0.7, 0.3 + (months_inverted / 24) * 0.4)
        else:
            yield_prob = 0.1

        # 2. Unemployment (Sahm Rule)
        unemployment = event_data.get('unemployment_rate', 4.0)
        unemployment_change = event_data.get('unemployment_change_6m', 0)
        # Sahm Rule: 0.5pp increase in U3 from recent low indicates recession
        if unemployment_change >= 0.5:
            unemployment_prob = min(0.8, 0.5 + unemployment_change * 0.3)
        else:
            unemployment_prob = 0.1

        # 3. GDP Growth
        gdp_q1 = event_data.get('gdp_growth_q1', 2.0)
        gdp_q2 = event_data.get('gdp_growth_q2', 2.0)
        # Technical recession: 2 consecutive quarters of negative growth
        if gdp_q1 < 0 and gdp_q2 < 0:
            gdp_prob = 0.9  # Already in technical recession
        elif gdp_q1 < 0 or gdp_q2 < 0:
            gdp_prob = 0.5
        elif gdp_q1 < 1.0 or gdp_q2 < 1.0:
            gdp_prob = 0.3
        else:
            gdp_prob = 0.1

        # 4. Consumer Confidence
        confidence = event_data.get('consumer_confidence_index', 100)
        if confidence < 80:
            confidence_prob = 0.5
        elif confidence < 90:
            confidence_prob = 0.3
        else:
            confidence_prob = 0.1

        # 5. Manufacturing PMI
        pmi = event_data.get('manufacturing_pmi', 50)
        if pmi < 45:
            pmi_prob = 0.6
        elif pmi < 50:
            pmi_prob = 0.4
        else:
            pmi_prob = 0.1

        # Weighted combination
        probability = (
            yield_prob * self.indicator_weights['yield_curve'] +
            unemployment_prob * self.indicator_weights['unemployment'] +
            gdp_prob * self.indicator_weights['gdp_growth'] +
            confidence_prob * self.indicator_weights['consumer_confidence'] +
            pmi_prob * self.indicator_weights['manufacturing_pmi']
        )

        # Use provided estimate if available
        if 'probability_estimate' in event_data:
            # Blend with our calculation
            probability = (probability + event_data['probability_estimate']) / 2

        return min(0.95, probability)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict market impact of recession"""
        severity = self.assess_severity(event_data)
        recession_prob = self._calculate_recession_probability(event_data)
        depth = event_data.get('expected_depth', 'moderate')

        # Base impact adjusted by probability
        depth_impacts = {'mild': -15, 'moderate': -25, 'severe': -40}
        base_impact = depth_impacts.get(depth, -25) * recession_prob

        # Yield curve inversion adds market concern
        if event_data.get('yield_curve_spread', 0) < 0:
            base_impact *= 1.2

        return {
            'overall_market_impact': round(base_impact, 2),
            'pre_recession_decline': round(base_impact * 0.6, 2),  # Markets lead by 6-12mo
            'recession_bottom': round(base_impact * 1.0, 2),
            'recovery_phase': round(base_impact * 0.4, 2),
            'expected_duration_months': self._estimate_duration(event_data),
            'bottom_timing_months': 6 + severity * 2,
            'volatility_increase': round(abs(base_impact) * 1.5, 2),
            'model_agreement': 0.80
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess recession severity"""
        depth = event_data.get('expected_depth', 'moderate')
        gdp_contraction = abs(min(event_data.get('gdp_growth_q1', 0), event_data.get('gdp_growth_q2', 0)))
        unemployment_change = event_data.get('unemployment_change_6m', 0)

        severity_map = {'mild': 2, 'moderate': 3, 'severe': 5}
        base_severity = severity_map.get(depth, 3)

        # Adjust for GDP contraction
        if gdp_contraction > 5:
            base_severity = min(5, base_severity + 1)

        # Adjust for unemployment
        if unemployment_change > 2:
            base_severity = min(5, base_severity + 1)

        return base_severity

    def _analyze_leading_indicators(self, event_data: Dict) -> Dict:
        """Analyze status of leading indicators"""
        indicators = {}

        # Yield Curve
        yield_spread = event_data.get('yield_curve_spread', 0)
        indicators['yield_curve'] = {
            'value': yield_spread,
            'status': 'INVERTED' if yield_spread < 0 else 'NORMAL',
            'signal': 'STRONG WARNING' if yield_spread < -0.5 else 'WARNING' if yield_spread < 0 else 'POSITIVE'
        }

        # Unemployment
        unemployment = event_data.get('unemployment_rate', 4.0)
        unemployment_change = event_data.get('unemployment_change_6m', 0)
        indicators['unemployment'] = {
            'current_rate': unemployment,
            '6m_change': unemployment_change,
            'sahm_rule_triggered': unemployment_change >= 0.5,
            'signal': 'STRONG WARNING' if unemployment_change >= 0.5 else 'WARNING' if unemployment_change > 0.2 else 'STABLE'
        }

        # GDP
        gdp_q1 = event_data.get('gdp_growth_q1', 2.0)
        gdp_q2 = event_data.get('gdp_growth_q2', 2.0)
        indicators['gdp'] = {
            'q1_growth': gdp_q1,
            'q2_growth': gdp_q2,
            'technical_recession': gdp_q1 < 0 and gdp_q2 < 0,
            'signal': 'RECESSION' if (gdp_q1 < 0 and gdp_q2 < 0) else 'WARNING' if (gdp_q1 < 1 or gdp_q2 < 1) else 'POSITIVE'
        }

        # Consumer Confidence
        confidence = event_data.get('consumer_confidence_index', 100)
        indicators['consumer_confidence'] = {
            'index': confidence,
            'signal': 'WARNING' if confidence < 80 else 'CAUTION' if confidence < 90 else 'POSITIVE'
        }

        # Manufacturing PMI
        pmi = event_data.get('manufacturing_pmi', 50)
        indicators['manufacturing'] = {
            'pmi': pmi,
            'status': 'CONTRACTION' if pmi < 50 else 'EXPANSION',
            'signal': 'STRONG WARNING' if pmi < 45 else 'WARNING' if pmi < 50 else 'POSITIVE'
        }

        return indicators

    def _determine_recession_phase(self, event_data: Dict, probability: float) -> str:
        """Determine which phase of recession cycle we're in"""
        gdp_q1 = event_data.get('gdp_growth_q1', 2.0)
        gdp_q2 = event_data.get('gdp_growth_q2', 2.0)
        yield_spread = event_data.get('yield_curve_spread', 0)

        if gdp_q1 < 0 and gdp_q2 < 0:
            return 'IN_RECESSION'
        elif probability > 0.6 and yield_spread < 0:
            return 'IMMINENT'
        elif probability > 0.4:
            return 'ELEVATED_RISK'
        elif yield_spread < 0:
            return 'EARLY_WARNING'
        else:
            return 'LOW_RISK'

    def _analyze_sector_resilience(self, event_data: Dict) -> Dict:
        """Analyze which sectors are resilient vs vulnerable"""
        return {
            'defensive_sectors': {
                'utilities': {'expected_impact': -5, 'rationale': 'Essential services, stable demand'},
                'consumer_staples': {'expected_impact': -8, 'rationale': 'Non-discretionary goods'},
                'healthcare': {'expected_impact': -10, 'rationale': 'Essential services'}
            },
            'vulnerable_sectors': {
                'consumer_discretionary': {'expected_impact': -30, 'rationale': 'First to be cut in downturn'},
                'financials': {'expected_impact': -35, 'rationale': 'Loan defaults, credit losses'},
                'real_estate': {'expected_impact': -28, 'rationale': 'Vacancy increases, values fall'},
                'industrials': {'expected_impact': -32, 'rationale': 'Capital spending falls'}
            },
            'counter_cyclical': {
                'discount_retail': {'expected_impact': +5, 'rationale': 'Trade-down consumer behavior'},
                'debt_collection': {'expected_impact': +15, 'rationale': 'Default surge'}
            }
        }

    def _estimate_duration(self, event_data: Dict) -> int:
        """Estimate recession duration in months"""
        depth = event_data.get('expected_depth', 'moderate')
        durations = {'mild': 8, 'moderate': 14, 'severe': 20}
        return durations.get(depth, 14)

    def _generate_policy_recommendations(self, event_data: Dict, probability: float) -> List[str]:
        """Generate policy recommendations"""
        recommendations = []

        if probability > 0.6:
            recommendations.extend([
                'Federal Reserve should consider preemptive rate cuts',
                'Prepare fiscal stimulus packages',
                'Enhance unemployment insurance systems',
                'Coordinate with other central banks'
            ])

        if event_data.get('unemployment_change_6m', 0) > 0.5:
            recommendations.append('Immediate job market support programs needed')

        if event_data.get('consumer_confidence_index', 100) < 80:
            recommendations.append('Consumer confidence restoration measures critical')

        return recommendations

    def _generate_investment_strategy(self, event_data: Dict, probability: float) -> Dict:
        """Generate investment strategy for recession"""
        if probability > 0.6:
            return {
                'equity_allocation': '30-40%',  # Reduced
                'fixed_income': '40-50%',      # Increased
                'cash': '10-20%',               # Increased
                'alternatives': '10%',
                'sector_tilts': {
                    'overweight': ['utilities', 'consumer_staples', 'healthcare'],
                    'underweight': ['consumer_discretionary', 'financials', 'real_estate']
                },
                'key_moves': [
                    'Shift to defensive sectors',
                    'Increase bond duration',
                    'Raise cash reserves',
                    'Consider gold as hedge'
                ]
            }
        elif probability > 0.4:
            return {
                'equity_allocation': '50-60%',
                'fixed_income': '30-40%',
                'cash': '5-10%',
                'alternatives': '5-10%',
                'sector_tilts': {
                    'overweight': ['healthcare', 'utilities'],
                    'neutral': ['consumer_staples'],
                    'underweight': ['consumer_discretionary']
                },
                'key_moves': [
                    'Begin defensive rotation',
                    'Monitor indicators closely',
                    'Prepare hedging strategies'
                ]
            }
        else:
            return {
                'equity_allocation': '60-70%',
                'fixed_income': '20-30%',
                'cash': '5%',
                'alternatives': '5-10%',
                'sector_tilts': 'balanced',
                'key_moves': ['Maintain diversification', 'Monitor early warnings']
            }
