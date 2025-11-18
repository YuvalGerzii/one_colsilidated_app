"""
Inflation Agent - Analyzes inflation surges and monetary policy responses
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseExtremeEventAgent


class InflationAgent(BaseExtremeEventAgent):
    """Specialized agent for analyzing inflation events"""

    def __init__(self, config: Dict):
        super().__init__('inflation', config)
        self.fed_target = 2.0  # Fed's 2% inflation target

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze inflation event

        Args:
            event_data: {
                'current_cpi': float,
                'current_pce': float,  # Fed's preferred measure
                'core_pce': float,
                'inflation_trend_6m': str,  # 'accelerating', 'stable', 'decelerating'
                'fed_response': str,  # 'dovish', 'neutral', 'hawkish'
                'rate_hikes_expected': int,
                'wage_growth': float,
                'supply_factors': List[str],
                'demand_factors': List[str],
                'geographic_scope': str
            }
        """
        severity = self.assess_severity(event_data)
        market_predictions = self.predict_market_impact(event_data)

        analysis = {
            'severity': severity,
            'inflation_breakdown': self._analyze_inflation_components(event_data),
            'fed_response_analysis': self._analyze_fed_response(event_data),
            'rate_path_projection': self._project_rate_path(event_data),
            'market_predictions': market_predictions,
            'sectoral_impact': self._analyze_inflation_winners_losers(event_data),
            'investment_implications': self._generate_investment_strategy(event_data),
            'historical_comparisons': self.get_historical_comparisons(event_data)
        }

        return self.compile_analysis_report(event_data, analysis)

    def predict_market_impact(self, event_data: Dict) -> Dict:
        """Predict market impact"""
        current_pce = event_data.get('current_pce', 2.5)
        rate_hikes_expected = event_data.get('rate_hikes_expected', 0)

        # Higher inflation = tighter policy = negative for risk assets
        inflation_gap = current_pce - self.fed_target
        base_impact = -inflation_gap * 5  # -5% per 1% above target

        # Rate hikes amplify impact
        rate_impact = rate_hikes_expected * -3  # -3% per 25bps hike

        total_impact = base_impact + rate_impact

        return {
            'overall_market_impact': round(total_impact, 2),
            'bonds_impact': round(total_impact * 1.5, 2),  # Bonds hit harder
            'equities_impact': round(total_impact * 1.0, 2),
            'real_assets_benefit': round(abs(total_impact) * 0.3, 2),
            'model_agreement': 0.75
        }

    def assess_severity(self, event_data: Dict) -> int:
        """Assess inflation severity"""
        current_pce = event_data.get('current_pce', 2.5)

        if current_pce > 6.0:
            return 5
        elif current_pce > 4.5:
            return 4
        elif current_pce > 3.5:
            return 3
        elif current_pce > 2.5:
            return 2
        else:
            return 1

    def _analyze_inflation_components(self, event_data: Dict) -> Dict:
        """Break down inflation sources"""
        return {
            'headline_cpi': event_data.get('current_cpi', 3.0),
            'core_pce': event_data.get('core_pce', 2.7),
            'supply_driven': len(event_data.get('supply_factors', [])) > len(event_data.get('demand_factors', [])),
            'wage_pressure': event_data.get('wage_growth', 3.0) > 3.5,
            'trend': event_data.get('inflation_trend_6m', 'stable')
        }

    def _analyze_fed_response(self, event_data: Dict) -> Dict:
        """Analyze Federal Reserve response"""
        response = event_data.get('fed_response', 'neutral')
        rate_hikes = event_data.get('rate_hikes_expected', 0)

        return {
            'stance': response,
            'rate_hikes_expected': rate_hikes,
            'adequacy': 'sufficient' if rate_hikes * 0.25 >= (event_data.get('current_pce', 2.5) - 2.0) else 'insufficient',
            'timeline': f"{rate_hikes * 2} months" if rate_hikes > 0 else 'N/A'
        }

    def _project_rate_path(self, event_data: Dict) -> List[Dict]:
        """Project Fed rate path"""
        current_pce = event_data.get('current_pce', 2.5)
        hikes_needed = max(0, int((current_pce - 2.0) / 0.25))

        path = []
        for i in range(min(hikes_needed, 8)):
            path.append({
                'meeting': i + 1,
                'hike_bps': 25,
                'cumulative_bps': (i + 1) * 25
            })

        return path

    def _analyze_inflation_winners_losers(self, event_data: Dict) -> Dict:
        """Identify winners and losers from inflation"""
        return {
            'winners': ['commodities', 'real_estate', 'tips', 'energy', 'materials'],
            'losers': ['long_bonds', 'growth_stocks', 'cash', 'fixed_income']
        }

    def _generate_investment_strategy(self, event_data: Dict) -> Dict:
        """Investment strategy for inflationary environment"""
        severity = self.assess_severity(event_data)

        if severity >= 4:
            return {
                'asset_allocation': {
                    'equities': '40%',
                    'real_assets': '30%',
                    'tips': '20%',
                    'cash': '10%'
                },
                'recommendations': [
                    'Shift to real assets (commodities, real estate)',
                    'TIPS over nominal bonds',
                    'Value over growth stocks',
                    'International diversification'
                ]
            }
        else:
            return {
                'asset_allocation': 'balanced with inflation protection',
                'recommendations': [
                    'Add TIPS for inflation protection',
                    'Maintain some commodity exposure',
                    'Shorten bond duration'
                ]
            }
