"""
Economic Crisis Agent - Analyzes financial system stress and economic collapses
Specializes in predicting market impacts from economic and financial crises
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class EconomicCrisisAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing economic crisis events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('economic_crisis', config)
        self.crisis_type_impacts = {
            'banking_crisis': 2.5,
            'sovereign_debt': 2.0,
            'currency_crisis': 1.8,
            'stock_market_crash': 3.0,
            'housing_bubble': 2.2,
            'commodity_shock': 1.5,
            'systemic_failure': 4.0
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze an economic crisis event

        Args:
            event_data: {
                'crisis_type': str,
                'affected_institutions': List[str],
                'systemic_risk_score': float (0-10),
                'credit_market_stress': str,  # low, medium, high, severe
                'contagion_risk': float (0-1),
                'central_bank_response': str,  # none, moderate, aggressive
                'fiscal_stimulus': float,  # USD amount
                'unemployment_increase': float,  # percentage points
                'gdp_contraction': float,  # percentage
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis of economic crisis impact
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Crisis-specific analysis
        systemic_risk = self._assess_systemic_risk(event_data)
        contagion_analysis = self._analyze_contagion_potential(event_data)
        policy_effectiveness = self._evaluate_policy_response(event_data)

        analysis = {
            'severity': severity,
            'systemic_risk_assessment': systemic_risk,
            'contagion_analysis': contagion_analysis,
            'policy_response_effectiveness': policy_effectiveness,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['finance', 'real_estate', 'consumer', 'technology', 'energy'],
                market_predictions['overall_market_impact']
            ),
            'recovery_scenarios': self._generate_recovery_scenarios(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of economic crisis
        """
        severity = self.assess_severity(event_data)
        crisis_type = event_data.get('crisis_type', 'banking_crisis')
        systemic_risk = event_data.get('systemic_risk_score', 5.0)
        contagion_risk = event_data.get('contagion_risk', 0.5)
        central_bank_response = event_data.get('central_bank_response', 'moderate')

        # Base impact (economic crises have the most severe impact)
        base_impact = -30.0 * (severity / 3.0)

        # Crisis type multiplier
        crisis_multiplier = self.crisis_type_impacts.get(crisis_type.lower(), 2.0)

        # Systemic risk amplifies impact
        systemic_multiplier = 1.0 + (systemic_risk / 10.0)

        # Contagion risk adds uncertainty
        contagion_multiplier = 1.0 + contagion_risk

        # Central bank response mitigates impact
        response_mitigation = {
            'none': 1.0,
            'moderate': 0.8,
            'aggressive': 0.6
        }
        response_factor = response_mitigation.get(central_bank_response.lower(), 0.8)

        overall_impact = (base_impact * crisis_multiplier * systemic_multiplier *
                         contagion_multiplier * response_factor)

        return {
            'overall_market_impact': round(overall_impact, 2),
            'immediate_crash_risk': round(overall_impact * 1.3, 2),
            'short_term_impact_90d': round(overall_impact * 1.0, 2),
            'medium_term_impact_6m': round(overall_impact * 0.7, 2),
            'long_term_impact_2y': round(overall_impact * 0.4, 2),
            'credit_spread_widening_bps': round(abs(overall_impact) * 50, 0),
            'volatility_explosion': round(abs(overall_impact) * 4.0, 2),
            'model_agreement': 0.75
        }

    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess economic crisis severity on 1-5 scale
        """
        systemic_risk = event_data.get('systemic_risk_score', 5.0)
        gdp_contraction = abs(event_data.get('gdp_contraction', 0))
        unemployment_increase = event_data.get('unemployment_increase', 0)
        num_institutions = len(event_data.get('affected_institutions', []))

        # Systemic risk severity
        systemic_severity = min(5, int(systemic_risk / 2))

        # Economic impact severity
        gdp_severity = min(5, int(gdp_contraction / 2))

        # Unemployment severity
        unemployment_severity = min(5, int(unemployment_increase / 2))

        # Institutional severity
        institution_severity = min(5, int(num_institutions / 3))

        # Weighted average
        total_severity = (
            systemic_severity * 0.35 +
            gdp_severity * 0.30 +
            unemployment_severity * 0.20 +
            institution_severity * 0.15
        )

        return max(1, min(5, int(round(total_severity))))

    def _assess_systemic_risk(self, event_data: Dict) -> Dict:
        """
        Assess systemic risk to financial system
        """
        systemic_score = event_data.get('systemic_risk_score', 5.0)
        institutions = event_data.get('affected_institutions', [])
        credit_stress = event_data.get('credit_market_stress', 'medium')

        # Identify systemically important institutions
        systemically_important = [
            inst for inst in institutions
            if any(key in inst.lower() for key in ['bank', 'fed', 'reserve', 'insurance', 'fund'])
        ]

        risk_levels = {
            'contained': (0, 3),
            'elevated': (3, 5),
            'high': (5, 7),
            'critical': (7, 10)
        }

        risk_level = 'contained'
        for level, (low, high) in risk_levels.items():
            if low <= systemic_score < high:
                risk_level = level
                break
        if systemic_score >= 10:
            risk_level = 'critical'

        return {
            'systemic_risk_score': systemic_score,
            'risk_level': risk_level,
            'systemically_important_institutions': len(systemically_important),
            'credit_market_stress': credit_stress,
            'requires_emergency_intervention': systemic_score >= 7
        }

    def _analyze_contagion_potential(self, event_data: Dict) -> Dict:
        """
        Analyze potential for crisis contagion
        """
        contagion_risk = event_data.get('contagion_risk', 0.5)
        geographic_scope = event_data.get('geographic_scope', 'national')

        # Geographic contagion potential
        scope_multipliers = {
            'local': 0.2,
            'regional': 0.5,
            'national': 0.7,
            'continental': 0.9,
            'global': 1.0
        }

        geographic_factor = scope_multipliers.get(geographic_scope.lower(), 0.7)

        # Calculate total contagion probability
        total_contagion_prob = contagion_risk * geographic_factor

        # Identify at-risk regions
        at_risk = []
        if total_contagion_prob > 0.3:
            at_risk.append('Interconnected financial markets')
        if total_contagion_prob > 0.5:
            at_risk.append('Trading partner economies')
        if total_contagion_prob > 0.7:
            at_risk.append('Emerging markets with currency exposure')

        return {
            'contagion_probability': round(total_contagion_prob, 2),
            'contagion_level': 'high' if total_contagion_prob > 0.7 else 'medium' if total_contagion_prob > 0.4 else 'low',
            'at_risk_regions': at_risk,
            'transmission_channels': ['Banking system', 'Trade linkages', 'Currency markets', 'Confidence effects']
        }

    def _evaluate_policy_response(self, event_data: Dict) -> Dict:
        """
        Evaluate effectiveness of policy response
        """
        central_bank = event_data.get('central_bank_response', 'moderate')
        fiscal_stimulus = event_data.get('fiscal_stimulus', 0)
        severity = self.assess_severity(event_data)

        # Assess adequacy of response
        response_scores = {
            'none': 0,
            'moderate': 5,
            'aggressive': 9
        }

        central_bank_score = response_scores.get(central_bank.lower(), 5)

        # Fiscal stimulus score (in billions, as % of typical GDP)
        fiscal_score = min(10, (fiscal_stimulus / 1e11) * 2)

        # Total policy score
        total_policy_score = (central_bank_score + fiscal_score) / 2

        # Is response adequate for severity?
        required_score = severity * 1.5
        is_adequate = total_policy_score >= required_score

        return {
            'central_bank_score': central_bank_score,
            'fiscal_stimulus_score': round(fiscal_score, 1),
            'total_policy_score': round(total_policy_score, 1),
            'is_adequate': is_adequate,
            'recommended_actions': self._generate_policy_recommendations(event_data, is_adequate)
        }

    def _generate_policy_recommendations(self, event_data: Dict, current_adequate: bool) -> List[str]:
        """
        Generate policy recommendations
        """
        recommendations = []
        severity = self.assess_severity(event_data)
        central_bank = event_data.get('central_bank_response', 'moderate')

        if not current_adequate or severity >= 4:
            recommendations.extend([
                "Implement emergency liquidity facilities",
                "Consider quantitative easing programs",
                "Deploy targeted fiscal stimulus"
            ])

        if central_bank == 'none':
            recommendations.extend([
                "Immediate rate cuts required",
                "Activate emergency lending programs"
            ])

        if event_data.get('credit_market_stress', 'medium') in ['high', 'severe']:
            recommendations.append("Establish credit guarantee programs")

        if event_data.get('systemic_risk_score', 5.0) >= 7:
            recommendations.extend([
                "Coordinate international central bank response",
                "Consider temporary market stabilization measures"
            ])

        return recommendations

    def _generate_recovery_scenarios(self, event_data: Dict) -> List[Dict]:
        """
        Generate potential recovery scenarios
        """
        severity = self.assess_severity(event_data)
        policy_response = event_data.get('central_bank_response', 'moderate')

        scenarios = [
            {
                'name': 'V-Shaped Recovery',
                'probability': 0.20 if severity <= 2 else 0.10,
                'timeline_months': 6,
                'description': 'Rapid recovery with aggressive policy response'
            },
            {
                'name': 'U-Shaped Recovery',
                'probability': 0.40 if severity <= 3 else 0.30,
                'timeline_months': 12,
                'description': 'Moderate recovery period with sustained policy support'
            },
            {
                'name': 'L-Shaped Recovery',
                'probability': 0.30 if severity >= 4 else 0.15,
                'timeline_months': 24,
                'description': 'Extended stagnation before gradual recovery'
            },
            {
                'name': 'W-Shaped Recovery',
                'probability': 0.25 if policy_response == 'none' else 0.10,
                'timeline_months': 18,
                'description': 'Initial recovery followed by relapse, then recovery'
            }
        ]

        # Normalize probabilities
        total_prob = sum(s['probability'] for s in scenarios)
        for scenario in scenarios:
            scenario['probability'] = round(scenario['probability'] / total_prob, 2)

        return sorted(scenarios, key=lambda x: x['probability'], reverse=True)
