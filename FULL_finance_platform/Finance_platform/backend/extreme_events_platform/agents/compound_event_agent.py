"""
Compound Event Agent - Analyzes simultaneous multiple crises (polycrisis)
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class CompoundEventAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing compound/multiple simultaneous extreme events
    """

    def __init__(self, config: Dict):
        super().__init__('compound_event', config)

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze compound event

        Args:
            event_data: {
                'primary_events': List[str],
                'event_details': List[Dict],
                'interaction_type': str,  # cascading, simultaneous, reinforcing
                'total_severity': int,
                'systemic_stress': float,
                'geographic_scope': str
            }
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Compound-specific analysis
        interaction_analysis = self._analyze_interactions(event_data)
        systemic_risk = self._assess_systemic_stress(event_data)
        complexity = self._assess_complexity(event_data)

        analysis = {
            'severity': severity,
            'interaction_analysis': interaction_analysis,
            'systemic_risk': systemic_risk,
            'complexity_score': complexity,
            'market_predictions': market_predictions,
            'sectoral_impact': self._analyze_compound_sector_impact(event_data),
            'policy_overload_risk': self._assess_policy_capacity(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict impact of compound event"""
        num_events = len(event_data.get('primary_events', []))
        interaction_type = event_data.get('interaction_type', 'simultaneous')

        # Base impact from multiple events
        base_impact = -15.0 * (num_events / 2.0)

        # Interaction multiplier
        interaction_multipliers = {
            'cascading': 1.5,  # One causes another
            'simultaneous': 1.8,  # Multiple at once (hardest to handle)
            'reinforcing': 2.0  # Events amplify each other
        }

        interaction_mult = interaction_multipliers.get(interaction_type, 1.5)

        overall_impact = base_impact * interaction_mult

        return {
            'overall_market_impact': round(overall_impact, 2),
            'non_linear_amplification': round((interaction_mult - 1.0) * 100, 0),
            'immediate_impact': round(overall_impact * 1.4, 2),
            'medium_term': round(overall_impact * 0.8, 2),
            'systemic_breakdown_risk': min(100, abs(overall_impact) * 3),
            'model_agreement': 0.65  # Lower confidence for complex scenarios
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess compound event severity"""
        num_events = len(event_data.get('primary_events', []))
        systemic_stress = event_data.get('systemic_stress', 0.5)

        # More events = higher severity
        severity = min(5, 2 + num_events)

        # Systemic stress adds to severity
        if systemic_stress > 0.8:
            severity = 5
        elif systemic_stress > 0.6:
            severity = min(5, severity + 1)

        return severity

    def _analyze_interactions(self, event_data: Dict) -> Dict:
        """Analyze how events interact"""
        events = event_data.get('primary_events', [])
        interaction_type = event_data.get('interaction_type', 'simultaneous')

        return {
            'number_of_events': len(events),
            'interaction_type': interaction_type,
            'amplification_factor': 2.0 if interaction_type == 'reinforcing' else 1.5,
            'complexity_level': 'extreme' if len(events) >= 3 else 'high'
        }

    def _assess_systemic_stress(self, event_data: Dict) -> Dict:
        """Assess stress on systems"""
        systemic_stress = event_data.get('systemic_stress', 0.5)

        return {
            'overall_stress': systemic_stress,
            'breaking_point_proximity': systemic_stress,
            'resilience_exhaustion': systemic_stress > 0.7,
            'cascade_probability': min(1.0, systemic_stress * 1.5)
        }

    def _assess_complexity(self, event_data: Dict) -> float:
        """Assess complexity score (0-10)"""
        num_events = len(event_data.get('primary_events', []))
        interaction_complexity = {
            'simultaneous': 2,
            'cascading': 1.5,
            'reinforcing': 2.5
        }

        base_complexity = num_events * 2
        interaction_add = interaction_complexity.get(event_data.get('interaction_type', 'simultaneous'), 1.5)

        return min(10.0, base_complexity + interaction_add)

    def _analyze_compound_sector_impact(self, event_data: Dict) -> Dict:
        """Analyze sector impacts from compound event"""
        # All sectors affected in compound events
        return {
            'all_sectors': 'negative',
            'magnitude': 'severe',
            'differentiation': 'minimal',  # Hard to find shelter
            'correlation': 'very_high'  # All assets move together
        }

    def _assess_policy_capacity(self, event_data: Dict) -> Dict:
        """Assess if policymakers can handle multiple crises"""
        num_events = len(event_data.get('primary_events', []))

        overloaded = num_events >= 3

        return {
            'policy_overload': overloaded,
            'effectiveness_reduction': f"{num_events * 20}%",
            'coordination_challenge': 'extreme' if num_events >= 3 else 'high',
            'response_delay_likely': overloaded
        }
