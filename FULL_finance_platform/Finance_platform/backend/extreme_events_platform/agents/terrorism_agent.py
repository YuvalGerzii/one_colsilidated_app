"""
Terrorism Agent - Analyzes terror attacks and security events
Specializes in predicting market impacts from terrorism and security threats
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class TerrorismAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing terrorism events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('terrorism', config)
        self.attack_type_impacts = {
            'bombing': 1.5,
            'shooting': 1.2,
            'hijacking': 2.0,
            'cyber_attack': 1.8,
            'chemical': 2.5,
            'biological': 3.0,
            'nuclear': 5.0
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a terrorism event

        Args:
            event_data: {
                'attack_type': str,
                'casualties': int,
                'target_type': str,  # civilian, military, infrastructure, financial
                'location': str,
                'economic_center': bool,  # Is it a major economic center?
                'symbolic_value': int (1-5),
                'claimed_by': str,
                'follow_up_threat': bool,
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis of terrorism impact
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Terrorism-specific analysis
        psychological_impact = self._assess_psychological_impact(event_data)
        confidence_effect = self._calculate_confidence_effect(event_data)
        security_cost = self._estimate_security_costs(event_data)

        analysis = {
            'severity': severity,
            'psychological_impact_score': psychological_impact,
            'consumer_confidence_effect': confidence_effect,
            'estimated_security_costs': security_cost,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['travel', 'finance', 'real_estate', 'technology', 'consumer'],
                market_predictions['overall_market_impact']
            ),
            'target_analysis': self._analyze_target(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of terrorism event
        """
        severity = self.assess_severity(event_data)
        attack_type = event_data.get('attack_type', 'bombing')
        is_economic_center = event_data.get('economic_center', False)
        follow_up_threat = event_data.get('follow_up_threat', False)

        # Base impact (terrorism typically has sharp but shorter-lived impact)
        base_impact = -7.5 * (severity / 3.0)

        # Attack type multiplier
        attack_multiplier = self.attack_type_impacts.get(attack_type.lower(), 1.0)

        # Economic center multiplier
        location_multiplier = 1.5 if is_economic_center else 1.0

        # Ongoing threat extends impact
        threat_multiplier = 1.3 if follow_up_threat else 1.0

        overall_impact = base_impact * attack_multiplier * location_multiplier * threat_multiplier

        # Market immunity (markets recover faster from subsequent attacks)
        immunity = self.calculate_market_immunity(
            len(event_data.get('similar_recent_events', []))
        )
        adjusted_impact = overall_impact * (1 - immunity * 0.4)

        return {
            'overall_market_impact': round(adjusted_impact, 2),
            'immediate_impact_24h': round(adjusted_impact * 1.5, 2),
            'short_term_impact_7d': round(adjusted_impact * 1.0, 2),
            'medium_term_impact_30d': round(adjusted_impact * 0.4, 2),
            'long_term_impact_90d': round(adjusted_impact * 0.15, 2),
            'volatility_spike': round(abs(adjusted_impact) * 3.0, 2),
            'model_agreement': 0.82
        }

    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess terrorism event severity on 1-5 scale
        """
        casualties = event_data.get('casualties', 0)
        symbolic_value = event_data.get('symbolic_value', 1)
        attack_type = event_data.get('attack_type', 'bombing')
        is_economic_center = event_data.get('economic_center', False)

        # Casualty-based severity
        casualty_severity = min(5, 1 + int(np.log1p(casualties) / 2))

        # Symbolic value adds to severity
        symbolic_severity = symbolic_value

        # Attack type severity
        attack_type_severity = min(5, int(self.attack_type_impacts.get(attack_type.lower(), 1.0)))

        # Economic center adds severity
        location_severity = 1 if is_economic_center else 0

        # Weighted average
        total_severity = (
            casualty_severity * 0.35 +
            symbolic_severity * 0.25 +
            attack_type_severity * 0.25 +
            location_severity * 0.15
        )

        return max(1, min(5, int(round(total_severity))))

    def _assess_psychological_impact(self, event_data: Dict) -> float:
        """
        Assess psychological impact on society (0-10 scale)
        """
        casualties = event_data.get('casualties', 0)
        symbolic_value = event_data.get('symbolic_value', 1)
        target_type = event_data.get('target_type', 'civilian')

        # Base psychological score from casualties
        base_score = min(10, np.log1p(casualties))

        # Symbolic targets have higher psychological impact
        symbolic_multiplier = 1.0 + (symbolic_value * 0.2)

        # Civilian targets create more fear than military
        target_multipliers = {
            'civilian': 1.5,
            'infrastructure': 1.3,
            'financial': 1.4,
            'military': 0.8,
            'government': 1.2
        }
        target_multiplier = target_multipliers.get(target_type.lower(), 1.0)

        return min(10, base_score * symbolic_multiplier * target_multiplier)

    def _calculate_confidence_effect(self, event_data: Dict) -> Dict:
        """
        Calculate effect on consumer and business confidence
        """
        psychological_impact = self._assess_psychological_impact(event_data)
        is_economic_center = event_data.get('economic_center', False)
        follow_up_threat = event_data.get('follow_up_threat', False)

        # Base confidence drop
        consumer_confidence_drop = psychological_impact * 2
        business_confidence_drop = psychological_impact * 1.5

        # Economic centers see larger business confidence drops
        if is_economic_center:
            business_confidence_drop *= 1.3

        # Ongoing threats compound the effect
        if follow_up_threat:
            consumer_confidence_drop *= 1.4
            business_confidence_drop *= 1.3

        return {
            'consumer_confidence_drop': round(-consumer_confidence_drop, 2),
            'business_confidence_drop': round(-business_confidence_drop, 2),
            'recovery_time_days': int(30 * (psychological_impact / 5.0))
        }

    def _estimate_security_costs(self, event_data: Dict) -> Dict:
        """
        Estimate increased security costs following attack
        """
        severity = self.assess_severity(event_data)
        is_economic_center = event_data.get('economic_center', False)

        # Base security cost increase (millions USD)
        base_cost = severity * 100

        # Economic centers require more security
        if is_economic_center:
            base_cost *= 2.5

        return {
            'immediate_security_costs_usd_millions': base_cost,
            'annual_ongoing_costs_usd_millions': base_cost * 0.3,
            'duration_years': 2 + severity
        }

    def _analyze_target(self, event_data: Dict) -> Dict:
        """
        Analyze the target and implications
        """
        target_type = event_data.get('target_type', 'civilian')
        location = event_data.get('location', 'unknown')

        implications = {
            'civilian': 'High public fear, pressure for enhanced security measures',
            'military': 'Potential for military response, geopolitical escalation',
            'infrastructure': 'Economic disruption, supply chain impacts',
            'financial': 'Direct market impact, systemic risk concerns',
            'government': 'Political instability, potential policy changes'
        }

        return {
            'target_type': target_type,
            'location': location,
            'strategic_implication': implications.get(target_type.lower(), 'Uncertain'),
            'requires_immediate_response': target_type.lower() in ['financial', 'infrastructure']
        }
