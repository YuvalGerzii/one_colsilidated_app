"""
Interest Rate Change Agent - Analyzes Fed rate decisions and impacts
"""

from typing import Dict, List
from .base_agent import BaseExtremeEventAgent


class InterestRateAgent(BaseExtremeEventAgent):
    """Specialized agent for analyzing interest rate changes"""

    def __init__(self, config: Dict):
        super().__init__('interest_rate_change', config)

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze interest rate change event

        Args:
            event_data: {
                'rate_change_bps': int,  # basis points
                'new_rate': float,
                'direction': str,  # 'hike' or 'cut'
                'surprise_factor': float,  # 0-1, 1 = complete surprise
                'forward_guidance': str,
                'economic_justification': str,
                'market_priced_in': float,  # 0-1, how much was priced in
                'geographic_scope': str
            }
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        analysis = {
            'severity': severity,
            'surprise_analysis': self._analyze_surprise(event_data),
            'market_predictions': market_predictions,
            'sectoral_impact': self._analyze_sector_sensitivity(event_data),
            'forward_guidance_implications': self._analyze_forward_guidance(event_data),
            'investment_strategy': self._generate_strategy(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict market impact of rate change"""
        rate_change_bps = event_data.get('rate_change_bps', 25)
        surprise_factor = event_data.get('surprise_factor', 0.0)
        direction = event_data.get('direction', 'hike')

        # Base impact
        base_impact = (rate_change_bps / 25) * (-2 if direction == 'hike' else 3)

        # Surprise amplifies impact
        total_impact = base_impact * (1 + surprise_factor)

        return {
            'overall_market_impact': round(total_impact, 2),
            'immediate_24h': round(total_impact * 1.5, 2),
            'bond_impact': round(total_impact * 2.0, 2),
            'model_agreement': 0.85
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess severity"""
        rate_change_bps = abs(event_data.get('rate_change_bps', 25))
        surprise = event_data.get('surprise_factor', 0.0)

        if rate_change_bps >= 75 or surprise > 0.8:
            return 5
        elif rate_change_bps >= 50 or surprise > 0.5:
            return 4
        elif rate_change_bps >= 25:
            return 3
        else:
            return 2

    def _analyze_surprise(self, event_data: Dict) -> Dict:
        """Analyze surprise factor"""
        surprise = event_data.get('surprise_factor', 0.0)
        return {
            'surprise_level': 'high' if surprise > 0.7 else 'moderate' if surprise > 0.3 else 'low',
            'market_prepared': event_data.get('market_priced_in', 0.5) > 0.7,
            'volatility_expected': surprise > 0.5
        }

    def _analyze_sector_sensitivity(self, event_data: Dict) -> Dict:
        """Analyze sector sensitivity to rates"""
        direction = event_data.get('direction', 'hike')

        if direction == 'hike':
            return {
                'most_negative': ['real_estate', 'utilities', 'growth_tech'],
                'most_positive': ['financials', 'value_stocks']
            }
        else:
            return {
                'most_positive': ['real_estate', 'growth_tech', 'small_caps'],
                'most_negative': ['financials']
            }

    def _analyze_forward_guidance(self, event_data: Dict) -> Dict:
        """Analyze forward guidance implications"""
        guidance = event_data.get('forward_guidance', 'data_dependent')
        return {
            'guidance_type': guidance,
            'market_interpretation': 'More hikes coming' if 'hawkish' in guidance else 'Pause likely'
        }

    def _generate_strategy(self, event_data: Dict) -> Dict:
        """Generate investment strategy"""
        direction = event_data.get('direction', 'hike')

        if direction == 'hike':
            return {
                'bonds': 'Shorten duration',
                'equities': 'Favor value over growth',
                'sectors': 'Overweight financials',
                'alternatives': 'Consider floating rate securities'
            }
        else:
            return {
                'bonds': 'Extend duration',
                'equities': 'Favor growth',
                'sectors': 'Overweight REITs, tech',
                'alternatives': 'Reduce cash holdings'
            }
