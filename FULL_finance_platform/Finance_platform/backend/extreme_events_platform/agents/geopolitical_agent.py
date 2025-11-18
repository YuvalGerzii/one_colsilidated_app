"""
Geopolitical Agent - Analyzes wars, sanctions, and political instability
Specializes in predicting market impacts from geopolitical events
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class GeopoliticalAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing geopolitical events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('geopolitical', config)
        self.event_type_impacts = {
            'war': 2.5,
            'sanctions': 1.5,
            'political_coup': 1.8,
            'trade_war': 1.6,
            'nuclear_threat': 3.5,
            'regime_change': 1.7,
            'territorial_dispute': 1.4,
            'diplomatic_crisis': 1.2
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a geopolitical event

        Args:
            event_data: {
                'event_subtype': str,  # war, sanctions, etc.
                'countries_involved': List[str],
                'economic_powerhouses_involved': bool,
                'nuclear_powers_involved': bool,
                'escalation_potential': float (0-10),
                'resource_access_impact': str,  # oil, gas, minerals, food
                'trade_route_disruption': bool,
                'duration_estimate_months': int,
                'alliance_implications': List[str],
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis of geopolitical impact
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Geopolitical-specific analysis
        escalation_risk = self._assess_escalation_risk(event_data)
        resource_impact = self._analyze_resource_implications(event_data)
        trade_disruption = self._evaluate_trade_impact(event_data)

        analysis = {
            'severity': severity,
            'escalation_risk_assessment': escalation_risk,
            'resource_market_impact': resource_impact,
            'trade_disruption_analysis': trade_disruption,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['energy', 'defense', 'technology', 'finance', 'consumer'],
                market_predictions['overall_market_impact']
            ),
            'strategic_implications': self._analyze_strategic_implications(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of geopolitical event
        """
        severity = self.assess_severity(event_data)
        event_subtype = event_data.get('event_subtype', 'diplomatic_crisis')
        escalation = event_data.get('escalation_potential', 5.0)
        economic_powers = event_data.get('economic_powerhouses_involved', False)
        nuclear_powers = event_data.get('nuclear_powers_involved', False)

        # Base impact
        base_impact = -10.0 * (severity / 3.0)

        # Event type multiplier
        event_multiplier = self.event_type_impacts.get(event_subtype.lower(), 1.5)

        # Escalation potential
        escalation_factor = 1.0 + (escalation / 10.0)

        # Major economic powers multiply impact
        economic_multiplier = 2.0 if economic_powers else 1.0

        # Nuclear powers create existential fear
        nuclear_multiplier = 1.8 if nuclear_powers else 1.0

        overall_impact = (base_impact * event_multiplier * escalation_factor *
                         economic_multiplier * nuclear_multiplier)

        # Geopolitical events often have prolonged uncertainty
        uncertainty_premium = abs(overall_impact) * 0.2

        return {
            'overall_market_impact': round(overall_impact, 2),
            'immediate_impact_7d': round(overall_impact * 1.2, 2),
            'short_term_impact_30d': round(overall_impact * 0.9, 2),
            'medium_term_impact_90d': round(overall_impact * 0.7, 2),
            'long_term_impact_1y': round(overall_impact * 0.5, 2),
            'uncertainty_premium': round(uncertainty_premium, 2),
            'volatility_increase': round(abs(overall_impact) * 2.5, 2),
            'model_agreement': 0.72
        }

    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess geopolitical event severity on 1-5 scale
        """
        event_subtype = event_data.get('event_subtype', 'diplomatic_crisis')
        escalation = event_data.get('escalation_potential', 5.0)
        num_countries = len(event_data.get('countries_involved', []))
        economic_powers = event_data.get('economic_powerhouses_involved', False)
        nuclear_powers = event_data.get('nuclear_powers_involved', False)

        # Event type severity
        type_severity = min(5, int(self.event_type_impacts.get(event_subtype.lower(), 1.5) * 1.5))

        # Escalation severity
        escalation_severity = min(5, int(escalation / 2))

        # Scale severity
        scale_severity = min(5, int(num_countries / 2))

        # Power involvement adds severity
        power_bonus = 0
        if economic_powers:
            power_bonus += 1
        if nuclear_powers:
            power_bonus += 2

        total_severity = (
            type_severity * 0.35 +
            escalation_severity * 0.30 +
            scale_severity * 0.20 +
            power_bonus * 0.15
        )

        return max(1, min(5, int(round(total_severity))))

    def _assess_escalation_risk(self, event_data: Dict) -> Dict:
        """
        Assess risk of escalation
        """
        escalation_potential = event_data.get('escalation_potential', 5.0)
        nuclear_powers = event_data.get('nuclear_powers_involved', False)
        duration_estimate = event_data.get('duration_estimate_months', 6)

        risk_level = 'low'
        if escalation_potential >= 7:
            risk_level = 'critical'
        elif escalation_potential >= 5:
            risk_level = 'high'
        elif escalation_potential >= 3:
            risk_level = 'moderate'

        # Nuclear involvement raises risk category
        if nuclear_powers and risk_level in ['moderate', 'high']:
            risk_level = 'critical'

        escalation_scenarios = []
        if escalation_potential >= 5:
            escalation_scenarios.append('Direct military confrontation between major powers')
        if nuclear_powers:
            escalation_scenarios.append('Nuclear brinkmanship or escalation')
        if duration_estimate > 12:
            escalation_scenarios.append('Prolonged conflict causing regional destabilization')

        return {
            'escalation_score': escalation_potential,
            'risk_level': risk_level,
            'potential_scenarios': escalation_scenarios,
            'monitoring_priority': 'critical' if escalation_potential >= 7 else 'high'
        }

    def _analyze_resource_implications(self, event_data: Dict) -> Dict:
        """
        Analyze impact on critical resources
        """
        resource_impact = event_data.get('resource_access_impact', '')
        countries = event_data.get('countries_involved', [])

        # Map resources to affected markets
        resource_markets = {
            'oil': {'market': 'Energy', 'impact_multiplier': 2.5, 'sectors': ['Energy', 'Transportation', 'Chemicals']},
            'gas': {'market': 'Energy', 'impact_multiplier': 2.0, 'sectors': ['Energy', 'Utilities', 'Manufacturing']},
            'minerals': {'market': 'Commodities', 'impact_multiplier': 1.5, 'sectors': ['Technology', 'Manufacturing', 'Construction']},
            'food': {'market': 'Agriculture', 'impact_multiplier': 1.8, 'sectors': ['Consumer', 'Agriculture', 'Retail']},
            'semiconductors': {'market': 'Technology', 'impact_multiplier': 2.2, 'sectors': ['Technology', 'Automotive', 'Defense']}
        }

        affected_resources = [
            res for res in resource_markets.keys()
            if res.lower() in resource_impact.lower()
        ]

        impacts = []
        for resource in affected_resources:
            res_data = resource_markets[resource]
            impacts.append({
                'resource': resource.title(),
                'affected_market': res_data['market'],
                'price_impact_estimate_pct': res_data['impact_multiplier'] * 10,
                'affected_sectors': res_data['sectors']
            })

        return {
            'critical_resources_affected': len(impacts),
            'resource_details': impacts,
            'supply_chain_risk': 'high' if len(impacts) >= 2 else 'moderate' if impacts else 'low'
        }

    def _evaluate_trade_impact(self, event_data: Dict) -> Dict:
        """
        Evaluate impact on trade and commerce
        """
        trade_disruption = event_data.get('trade_route_disruption', False)
        event_subtype = event_data.get('event_subtype', 'diplomatic_crisis')
        countries = event_data.get('countries_involved', [])

        # Estimate trade volume affected (in trillions)
        estimated_trade_volume = len(countries) * 0.5  # Rough estimate

        disruption_level = 'none'
        if trade_disruption:
            if event_subtype == 'war':
                disruption_level = 'severe'
            elif event_subtype in ['sanctions', 'trade_war']:
                disruption_level = 'high'
            else:
                disruption_level = 'moderate'

        disruption_effects = {
            'none': [],
            'moderate': ['Increased shipping costs', 'Delays in delivery times'],
            'high': ['Trade route diversions', 'Sanctions compliance costs', 'Lost market access'],
            'severe': ['Complete trade cessation', 'Critical supply shortages', 'Price spikes']
        }

        return {
            'disruption_level': disruption_level,
            'estimated_trade_volume_affected_usd_trillions': round(estimated_trade_volume, 1),
            'primary_effects': disruption_effects.get(disruption_level, []),
            'alternative_routes_needed': disruption_level in ['high', 'severe']
        }

    def _analyze_strategic_implications(self, event_data: Dict) -> Dict:
        """
        Analyze broader strategic implications
        """
        alliances = event_data.get('alliance_implications', [])
        nuclear_powers = event_data.get('nuclear_powers_involved', False)
        event_subtype = event_data.get('event_subtype', 'diplomatic_crisis')

        implications = []

        if nuclear_powers:
            implications.append('Nuclear deterrence dynamics in play')

        if len(alliances) > 0:
            implications.append(f'Alliance structures affected: {", ".join(alliances)}')

        if event_subtype == 'war':
            implications.extend([
                'Potential shift in regional power balance',
                'Defense spending increases likely',
                'Refugee and humanitarian crisis potential'
            ])
        elif event_subtype == 'sanctions':
            implications.extend([
                'Economic decoupling between powers',
                'Alternative financial systems development',
                'Sanctions evasion networks emergence'
            ])

        return {
            'strategic_implications': implications,
            'power_balance_shift': len(implications) >= 3,
            'long_term_structural_changes_expected': event_subtype in ['war', 'sanctions', 'trade_war']
        }

    def __init__(self, config: Dict):
        super().__init__('geopolitical', config)
