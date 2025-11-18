"""
Cyber Attack Agent - Analyzes cyber attacks and digital infrastructure failures
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class CyberAttackAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing cyber attack events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('cyber_attack', config)
        self.attack_type_impacts = {
            'ransomware': 1.5,
            'data_breach': 1.3,
            'infrastructure_hack': 2.0,
            'ddos': 1.1,
            'supply_chain_attack': 2.5,
            'financial_system_hack': 3.0,
            'critical_infrastructure': 2.8
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a cyber attack event

        Args:
            event_data: {
                'attack_type': str,
                'target_sector': str,
                'affected_companies': List[str],
                'data_compromised': bool,
                'systems_down': bool,
                'ransom_amount_usd': float,
                'recovery_time_estimate_hours': int,
                'attribution': str,  # nation-state, criminal, hacktivist
                'cascading_effects': bool,
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Cyber-specific analysis
        cyber_risk = self._assess_cyber_risk(event_data)
        cascading = self._analyze_cascading_effects(event_data)
        recovery = self._estimate_recovery(event_data)

        analysis = {
            'severity': severity,
            'cyber_risk_score': cyber_risk,
            'cascading_analysis': cascading,
            'recovery_analysis': recovery,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['technology', 'finance', 'cybersecurity', 'insurance', 'cloud_computing'],
                market_predictions['overall_market_impact']
            ),
            'attribution_impact': self._analyze_attribution(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict market impact of cyber attack"""
        severity = self.assess_severity(event_data)
        attack_type = event_data.get('attack_type', 'ddos')
        target_sector = event_data.get('target_sector', 'technology')
        systems_down = event_data.get('systems_down', False)

        # Base impact
        base_impact = -8.0 * (severity / 3.0)

        # Attack type multiplier
        attack_multiplier = self.attack_type_impacts.get(attack_type.lower(), 1.0)

        # Critical sector multiplier
        critical_sectors = {'finance': 2.0, 'energy': 1.8, 'healthcare': 1.6}
        sector_multiplier = critical_sectors.get(target_sector.lower(), 1.0)

        # Systems down significantly worsens impact
        downtime_multiplier = 1.5 if systems_down else 1.0

        overall_impact = base_impact * attack_multiplier * sector_multiplier * downtime_multiplier

        return {
            'overall_market_impact': round(overall_impact, 2),
            'immediate_impact_24h': round(overall_impact * 1.3, 2),
            'sector_specific_impact': round(overall_impact * sector_multiplier * 2, 2),
            'short_term_7d': round(overall_impact * 0.8, 2),
            'medium_term_30d': round(overall_impact * 0.3, 2),
            'cybersecurity_sector_boost': round(abs(overall_impact) * 0.8, 2),
            'model_agreement': 0.80
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess cyber attack severity"""
        attack_type = event_data.get('attack_type', 'ddos')
        num_affected = len(event_data.get('affected_companies', []))
        systems_down = event_data.get('systems_down', False)
        data_compromised = event_data.get('data_compromised', False)

        # Base severity from attack type
        type_severity = min(5, int(self.attack_type_impacts.get(attack_type.lower(), 1.0) * 2))

        # Scale from number of affected organizations
        scale_severity = min(3, num_affected // 5)

        # Impact severity
        impact_severity = 0
        if systems_down:
            impact_severity += 2
        if data_compromised:
            impact_severity += 1

        total = (type_severity + scale_severity + impact_severity) // 2

        return max(1, min(5, int(round(total))))

    def _assess_cyber_risk(self, event_data: Dict) -> float:
        """Assess ongoing cyber risk (0-10 scale)"""
        risk = 5.0  # Base

        # Attribution increases risk if nation-state
        if event_data.get('attribution', '').lower() == 'nation-state':
            risk += 2.0

        # Cascading effects
        if event_data.get('cascading_effects', False):
            risk += 2.0

        # Critical sector
        if event_data.get('target_sector', '').lower() in ['finance', 'energy', 'healthcare']:
            risk += 1.5

        return min(10.0, risk)

    def _analyze_cascading_effects(self, event_data: Dict) -> Dict:
        """Analyze potential cascading effects"""
        will_cascade = event_data.get('cascading_effects', False)
        attack_type = event_data.get('attack_type', '')

        cascading_sectors = []
        if 'supply_chain' in attack_type.lower():
            cascading_sectors = ['All dependent companies', 'Downstream manufacturers', 'Retailers']
        elif event_data.get('target_sector') == 'finance':
            cascading_sectors = ['Banking system', 'Payments', 'Trading']

        return {
            'will_cascade': will_cascade,
            'probability': 0.7 if will_cascade else 0.2,
            'affected_sectors': cascading_sectors,
            'estimated_total_impact': len(cascading_sectors) * 10  # Rough estimate
        }

    def _estimate_recovery(self, event_data: Dict) -> Dict:
        """Estimate recovery timeline"""
        recovery_hours = event_data.get('recovery_time_estimate_hours', 48)

        return {
            'estimated_hours': recovery_hours,
            'estimated_days': recovery_hours / 24,
            'full_operations_days': recovery_hours / 24 * 1.5,
            'reputation_recovery_months': 3 if event_data.get('data_compromised') else 1
        }

    def _analyze_attribution(self, event_data: Dict) -> Dict:
        """Analyze attribution and geopolitical implications"""
        attribution = event_data.get('attribution', 'unknown')

        implications = {
            'nation-state': 'Potential for retaliation, escalation risk high',
            'criminal': 'Law enforcement response, insurance claims',
            'hacktivist': 'Ideological motivation, possible continued attacks',
            'unknown': 'High uncertainty, defensive posture required'
        }

        return {
            'attribution': attribution,
            'implication': implications.get(attribution.lower(), 'Unknown'),
            'geopolitical_risk': attribution.lower() == 'nation-state'
        }
