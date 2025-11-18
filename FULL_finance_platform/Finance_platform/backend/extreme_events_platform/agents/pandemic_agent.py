"""
Pandemic Agent - Analyzes disease outbreaks and health crises
Specializes in predicting market impacts from pandemics and epidemics
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class PandemicAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing pandemic events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('pandemic', config)
        self.transmission_models = []
        self.healthcare_capacity_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.9
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a pandemic event

        Args:
            event_data: {
                'disease_name': str,
                'r0': float,  # Basic reproduction number
                'mortality_rate': float,
                'affected_countries': List[str],
                'containment_measures': List[str],
                'healthcare_capacity': str,
                'vaccine_availability': bool,
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis of pandemic impact
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Pandemic-specific analysis
        transmission_score = self._analyze_transmission(event_data)
        healthcare_stress = self._assess_healthcare_stress(event_data)
        economic_disruption = self._calculate_economic_disruption(event_data)

        analysis = {
            'severity': severity,
            'transmission_potential': transmission_score,
            'healthcare_system_stress': healthcare_stress,
            'economic_disruption_score': economic_disruption,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['healthcare', 'travel', 'consumer', 'technology', 'finance'],
                market_predictions['overall_market_impact']
            ),
            'policy_recommendations': self._generate_policy_recommendations(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of pandemic

        Returns:
            Market impact predictions including timelines
        """
        severity = self.assess_severity(event_data)
        r0 = event_data.get('r0', 2.5)
        mortality_rate = event_data.get('mortality_rate', 0.01)
        has_vaccine = event_data.get('vaccine_availability', False)

        # Base impact calculation
        base_impact = -10.0 * (severity / 3.0)  # -10% for avg severity

        # Adjust for transmission rate (higher R0 = worse impact)
        transmission_factor = min(r0 / 2.0, 3.0)

        # Adjust for mortality (psychological impact on markets)
        mortality_factor = 1.0 + (mortality_rate * 100)

        # Vaccine reduces impact significantly
        vaccine_factor = 0.6 if has_vaccine else 1.0

        # Calculate overall impact
        overall_impact = base_impact * transmission_factor * mortality_factor * vaccine_factor

        # Market immunity from previous pandemics
        immunity = self.calculate_market_immunity(
            len(event_data.get('similar_recent_events', []))
        )
        adjusted_impact = overall_impact * (1 - immunity * 0.3)

        return {
            'overall_market_impact': round(adjusted_impact, 2),
            'short_term_impact_30d': round(adjusted_impact * 1.2, 2),
            'medium_term_impact_90d': round(adjusted_impact * 0.8, 2),
            'long_term_impact_1y': round(adjusted_impact * 0.4, 2),
            'volatility_increase': round(abs(adjusted_impact) * 2.5, 2),
            'model_agreement': 0.78
        }

    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess pandemic severity on 1-5 scale
        """
        r0 = event_data.get('r0', 2.5)
        mortality_rate = event_data.get('mortality_rate', 0.01)
        num_countries = len(event_data.get('affected_countries', []))
        has_vaccine = event_data.get('vaccine_availability', False)

        # Calculate severity components
        transmission_severity = min(int(r0), 5)
        mortality_severity = min(int(mortality_rate * 200), 5)
        geographic_severity = min(int(num_countries / 30), 5)

        # Average the components
        base_severity = (transmission_severity + mortality_severity + geographic_severity) / 3

        # Vaccine reduces severity
        if has_vaccine:
            base_severity *= 0.7

        return max(1, min(5, int(round(base_severity))))

    def _analyze_transmission(self, event_data: Dict) -> float:
        """
        Analyze transmission potential (0-10 scale)
        """
        r0 = event_data.get('r0', 2.5)
        containment = len(event_data.get('containment_measures', []))

        # Higher R0 = higher transmission
        base_score = min(r0 * 2, 10)

        # Containment measures reduce transmission
        containment_reduction = min(containment * 0.5, 4)

        return max(0, base_score - containment_reduction)

    def _assess_healthcare_stress(self, event_data: Dict) -> str:
        """
        Assess stress on healthcare system
        """
        capacity = event_data.get('healthcare_capacity', 'medium')
        severity = self.assess_severity(event_data)

        if capacity == 'low' or severity >= 4:
            return 'critical'
        elif capacity == 'medium' and severity >= 3:
            return 'high'
        elif severity >= 2:
            return 'moderate'
        else:
            return 'manageable'

    def _calculate_economic_disruption(self, event_data: Dict) -> float:
        """
        Calculate economic disruption score (0-100)
        """
        containment = event_data.get('containment_measures', [])
        geographic_scope = event_data.get('geographic_scope', 'regional')

        # Different containment measures have different economic impacts
        disruption_weights = {
            'lockdown': 30,
            'travel_ban': 20,
            'business_closure': 25,
            'quarantine': 15,
            'social_distancing': 10,
            'mask_mandate': 5
        }

        disruption_score = sum(
            disruption_weights.get(measure.lower(), 5)
            for measure in containment
        )

        # Multiply by regional scope
        regional_multiplier = self.calculate_regional_multiplier(geographic_scope)

        return min(100, disruption_score * (regional_multiplier / 5.0))

    def _generate_policy_recommendations(self, event_data: Dict) -> List[str]:
        """
        Generate policy recommendations for stakeholders
        """
        recommendations = []
        severity = self.assess_severity(event_data)

        if severity >= 4:
            recommendations.extend([
                "Implement emergency liquidity measures",
                "Consider market circuit breakers for extreme volatility",
                "Increase healthcare sector investments"
            ])

        if not event_data.get('vaccine_availability', False):
            recommendations.append("Accelerate vaccine development funding")

        if event_data.get('healthcare_capacity', 'medium') == 'low':
            recommendations.append("Emergency healthcare capacity expansion required")

        recommendations.extend([
            "Diversify supply chains to reduce concentration risk",
            "Increase strategic reserves for essential goods",
            "Implement remote work infrastructure investments"
        ])

        return recommendations
