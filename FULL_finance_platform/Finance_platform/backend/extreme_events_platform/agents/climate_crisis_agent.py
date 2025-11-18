"""
Climate Crisis Agent - Analyzes climate change events and environmental crises
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class ClimateCrisisAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing climate crisis events
    """

    def __init__(self, config: Dict):
        super().__init__('climate_crisis', config)

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a climate crisis event

        Args:
            event_data: {
                'crisis_type': str,  # heat wave, drought, sea level, etc.
                'temperature_anomaly': float,
                'duration_months': int,
                'affected_regions': List[str],
                'agricultural_impact': str,
                'infrastructure_risk': str,
                'migration_pressure': bool,
                'tipping_point_risk': bool,
                'geographic_scope': str
            }
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        analysis = {
            'severity': severity,
            'long_term_risk': self._assess_long_term_risk(event_data),
            'transition_opportunities': self._identify_transition_opportunities(event_data),
            'stranded_assets_risk': self._assess_stranded_assets(event_data),
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['energy', 'agriculture', 'real_estate', 'insurance', 'renewable_energy'],
                market_predictions['overall_market_impact']
            ),
            'policy_catalyst_potential': self._assess_policy_catalyst(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict market impact"""
        severity = self.assess_severity(event_data)

        # Climate events have asymmetric impact (winners and losers)
        base_impact = -6.0 * (severity / 3.0)

        # Long-term vs short-term split
        return {
            'overall_market_impact': round(base_impact, 2),
            'immediate_impact': round(base_impact * 0.5, 2),  # Markets slow to react
            'long_term_impact_5y': round(base_impact * 2.0, 2),  # Compounds over time
            'fossil_fuel_impact': round(base_impact * 3.0, 2),
            'renewable_energy_gain': round(abs(base_impact) * 1.5, 2),
            'model_agreement': 0.75
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess severity"""
        temp_anomaly = abs(event_data.get('temperature_anomaly', 0))
        duration = event_data.get('duration_months', 1)
        tipping_point = event_data.get('tipping_point_risk', False)

        severity = 2  # Base

        if temp_anomaly > 2.0:
            severity += 2
        elif temp_anomaly > 1.0:
            severity += 1

        if duration > 12:
            severity += 1

        if tipping_point:
            severity += 2

        return max(1, min(5, severity))

    def _assess_long_term_risk(self, event_data: Dict) -> Dict:
        """Assess long-term climate risk"""
        return {
            'tipping_point_proximity': 0.6 if event_data.get('tipping_point_risk') else 0.2,
            'irreversibility_risk': 0.7 if event_data.get('duration_months', 0) > 24 else 0.3,
            'compounding_effects': 'high' if event_data.get('temperature_anomaly', 0) > 1.5 else 'medium'
        }

    def _identify_transition_opportunities(self, event_data: Dict) -> List[Dict]:
        """Identify green transition opportunities"""
        return [
            {'sector': 'Renewable Energy', 'opportunity': 'Accelerated adoption', 'gain_potential': 40},
            {'sector': 'Electric Vehicles', 'opportunity': 'Policy support surge', 'gain_potential': 35},
            {'sector': 'Energy Efficiency', 'opportunity': 'Demand spike', 'gain_potential': 25},
            {'sector': 'Climate Tech', 'opportunity': 'Investment flood', 'gain_potential': 50}
        ]

    def _assess_stranded_assets(self, event_data: Dict) -> Dict:
        """Assess stranded asset risk"""
        severity = self.assess_severity(event_data)

        return {
            'fossil_fuel_reserves': 'high_risk' if severity >= 4 else 'medium_risk',
            'coastal_real_estate': 'high_risk',
            'carbon_intensive_industries': 'high_risk',
            'estimated_value_at_risk_trillions': severity * 2.0
        }

    def _assess_policy_catalyst(self, event_data: Dict) -> Dict:
        """Assess potential for policy action"""
        severity = self.assess_severity(event_data)

        return {
            'catalyst_probability': severity * 0.2,
            'expected_policies': ['Carbon pricing', 'Renewable mandates', 'Fossil fuel phase-out'],
            'investment_redirection': 'Major' if severity >= 4 else 'Moderate'
        }
