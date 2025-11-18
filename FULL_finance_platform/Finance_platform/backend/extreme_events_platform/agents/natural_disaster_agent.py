"""
Natural Disaster Agent - Analyzes storms, earthquakes, floods, wildfires
Specializes in predicting market impacts from natural disasters
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class NaturalDisasterAgent(BaseExtremeEventAgent):
    """
    Specialized agent for analyzing natural disaster events and their market impact
    """

    def __init__(self, config: Dict):
        super().__init__('natural_disaster', config)
        self.disaster_type_impacts = {
            'hurricane': 1.5,
            'earthquake': 2.0,
            'tsunami': 2.5,
            'flood': 1.3,
            'wildfire': 1.2,
            'tornado': 1.1,
            'drought': 1.4,
            'volcanic_eruption': 1.8
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze a natural disaster event

        Args:
            event_data: {
                'disaster_type': str,
                'magnitude': float,  # Richter scale, wind speed, etc.
                'affected_area_sq_km': float,
                'population_affected': int,
                'infrastructure_damage': str,  # minimal, moderate, severe, catastrophic
                'economic_losses_usd': float,
                'insurance_coverage': float (0-1),
                'location': str,
                'industrial_facilities_affected': List[str],
                'geographic_scope': str
            }

        Returns:
            Comprehensive analysis of natural disaster impact
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        # Disaster-specific analysis
        infrastructure_impact = self._assess_infrastructure_damage(event_data)
        supply_chain_disruption = self._analyze_supply_chain_impact(event_data)
        insurance_burden = self._calculate_insurance_burden(event_data)

        analysis = {
            'severity': severity,
            'infrastructure_damage_score': infrastructure_impact,
            'supply_chain_disruption': supply_chain_disruption,
            'insurance_sector_burden': insurance_burden,
            'market_predictions': market_predictions,
            'sectoral_impact': self.assess_sector_impact(
                ['utilities', 'real_estate', 'consumer', 'energy', 'finance'],
                market_predictions['overall_market_impact']
            ),
            'reconstruction_opportunities': self._identify_reconstruction_sectors(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """
        Predict market impact of natural disaster
        """
        severity = self.assess_severity(event_data)
        disaster_type = event_data.get('disaster_type', 'storm')
        economic_losses = event_data.get('economic_losses_usd', 0)
        population_affected = event_data.get('population_affected', 0)

        # Base impact calculation
        base_impact = -5.0 * (severity / 3.0)

        # Disaster type multiplier
        disaster_multiplier = self.disaster_type_impacts.get(disaster_type.lower(), 1.0)

        # Economic loss adjustment (in billions)
        loss_factor = 1.0 + min(economic_losses / 1e10, 5.0) * 0.1

        # Population affected adds to impact
        population_factor = 1.0 + min(population_affected / 1e7, 3.0) * 0.05

        overall_impact = base_impact * disaster_multiplier * loss_factor * population_factor

        # Natural disasters often have localized impact unless massive
        if severity < 4:
            overall_impact *= 0.7

        return {
            'overall_market_impact': round(overall_impact, 2),
            'immediate_impact_7d': round(overall_impact * 1.1, 2),
            'short_term_impact_30d': round(overall_impact * 0.8, 2),
            'medium_term_impact_90d': round(overall_impact * 0.4, 2),
            'reconstruction_benefit_6m': round(abs(overall_impact) * 0.3, 2),
            'volatility_increase': round(abs(overall_impact) * 1.5, 2),
            'model_agreement': 0.85
        }

    def assess_severity(self, event_data: Dict) -> int:
        """
        Assess natural disaster severity on 1-5 scale
        """
        economic_losses = event_data.get('economic_losses_usd', 0)
        population_affected = event_data.get('population_affected', 0)
        infrastructure_damage = event_data.get('infrastructure_damage', 'moderate')
        disaster_type = event_data.get('disaster_type', 'storm')

        # Economic loss severity (in billions)
        loss_severity = min(5, int(np.log10(max(economic_losses, 1e6)) - 8))

        # Population severity
        pop_severity = min(5, int(np.log10(max(population_affected, 1)) - 3))

        # Infrastructure damage severity
        damage_map = {'minimal': 1, 'moderate': 2, 'severe': 4, 'catastrophic': 5}
        infra_severity = damage_map.get(infrastructure_damage.lower(), 2)

        # Disaster type baseline
        type_severity = min(5, int(self.disaster_type_impacts.get(disaster_type.lower(), 1.0) * 2))

        # Weighted average
        total_severity = (
            loss_severity * 0.3 +
            pop_severity * 0.25 +
            infra_severity * 0.3 +
            type_severity * 0.15
        )

        return max(1, min(5, int(round(total_severity))))

    def _assess_infrastructure_damage(self, event_data: Dict) -> Dict:
        """
        Assess infrastructure damage in detail
        """
        damage_level = event_data.get('infrastructure_damage', 'moderate')
        economic_losses = event_data.get('economic_losses_usd', 0)
        facilities = event_data.get('industrial_facilities_affected', [])

        damage_scores = {
            'minimal': 2,
            'moderate': 5,
            'severe': 7,
            'catastrophic': 10
        }

        return {
            'overall_damage_score': damage_scores.get(damage_level.lower(), 5),
            'estimated_rebuild_time_months': damage_scores.get(damage_level.lower(), 5) * 2,
            'critical_facilities_affected': len(facilities),
            'estimated_rebuild_cost_usd': economic_losses * 1.2  # Includes indirect costs
        }

    def _analyze_supply_chain_impact(self, event_data: Dict) -> Dict:
        """
        Analyze supply chain disruptions
        """
        facilities = event_data.get('industrial_facilities_affected', [])
        disaster_type = event_data.get('disaster_type', 'storm')
        severity = self.assess_severity(event_data)

        # Identify critical facility types
        critical_facilities = {
            'port': 'Maritime shipping disruption',
            'airport': 'Air freight disruption',
            'factory': 'Manufacturing disruption',
            'power_plant': 'Energy supply disruption',
            'refinery': 'Fuel supply disruption',
            'warehouse': 'Distribution disruption'
        }

        affected_critical = [
            {'facility': f, 'impact': critical_facilities.get(f.lower(), 'Supply disruption')}
            for f in facilities
            if any(key in f.lower() for key in critical_facilities.keys())
        ]

        # Estimate disruption duration
        disruption_days = severity * 15

        return {
            'disruption_severity': 'high' if len(affected_critical) > 2 else 'moderate' if affected_critical else 'low',
            'critical_facilities_affected': affected_critical,
            'estimated_disruption_days': disruption_days,
            'alternative_routes_needed': len(affected_critical) > 0
        }

    def _calculate_insurance_burden(self, event_data: Dict) -> Dict:
        """
        Calculate burden on insurance sector
        """
        economic_losses = event_data.get('economic_losses_usd', 0)
        insurance_coverage = event_data.get('insurance_coverage', 0.5)

        # Insured losses
        insured_losses = economic_losses * insurance_coverage

        # Estimate impact on insurance sector
        insurance_impact_pct = min(10, (insured_losses / 1e9) * 0.5)

        return {
            'total_insured_losses_usd': insured_losses,
            'estimated_insurance_sector_impact_pct': round(-insurance_impact_pct, 2),
            'reinsurance_needed': insured_losses > 1e10,
            'premium_increases_expected': insured_losses > 5e9
        }

    def _identify_reconstruction_sectors(self, event_data: Dict) -> List[Dict]:
        """
        Identify sectors that benefit from reconstruction
        """
        infrastructure_damage = event_data.get('infrastructure_damage', 'moderate')
        economic_losses = event_data.get('economic_losses_usd', 0)

        if economic_losses < 1e9:
            return []

        opportunity_sectors = [
            {
                'sector': 'Construction',
                'opportunity_level': 'high',
                'timeline_months': 6,
                'estimated_benefit_pct': 15
            },
            {
                'sector': 'Building Materials',
                'opportunity_level': 'high',
                'timeline_months': 3,
                'estimated_benefit_pct': 20
            },
            {
                'sector': 'Engineering Services',
                'opportunity_level': 'medium',
                'timeline_months': 6,
                'estimated_benefit_pct': 10
            },
            {
                'sector': 'Heavy Equipment',
                'opportunity_level': 'medium',
                'timeline_months': 4,
                'estimated_benefit_pct': 12
            }
        ]

        if infrastructure_damage in ['severe', 'catastrophic']:
            opportunity_sectors.append({
                'sector': 'Infrastructure Development',
                'opportunity_level': 'high',
                'timeline_months': 12,
                'estimated_benefit_pct': 25
            })

        return opportunity_sectors
