"""
Energy Event Agent (V5.0)

Analyzes energy-related events and their cross-sector impacts:
- Oil shocks: Supply disruptions, price spikes, geopolitical events
- Natural gas disruptions: Pipeline issues, LNG shortages, pricing volatility
- Power grid failures: Blackouts, capacity constraints, grid instability
- Renewable energy transitions: Policy shifts, technology breakthroughs
- Nuclear events: Plant shutdowns, new capacity, regulatory changes

Cross-sector cascades example:
Oil spike → Transportation costs rise → Logistics inflation → All consumer goods affected →
Retail margins compress → Consumer spending falls → Recession risk increases
"""

from typing import Dict, List
from ..agents.base_agent import BaseAgent


class EnergyEventAgent(BaseAgent):
    """
    Analyzes energy events with comprehensive cross-sector impact modeling.

    Energy is the most interconnected sector - affects literally everything.
    """

    def __init__(self, config):
        """Initialize energy event agent"""
        super().__init__(config)

        # Energy price elasticity by sector (how much a 10% energy price change affects sector)
        self.energy_elasticity = {
            'airlines': -0.35,      # Fuel = 20-30% of costs
            'transportation': -0.25,  # Logistics, trucking
            'chemicals': -0.20,     # Energy-intensive production
            'materials': -0.18,     # Steel, aluminum = high energy use
            'utilities': +0.30,     # Higher energy prices = higher rates
            'energy': +0.80,        # Direct beneficiary
            'consumer': -0.12,      # Indirect through transportation
            'agriculture': -0.15,   # Fertilizer costs, fuel for equipment
            'industrials': -0.14,   # Manufacturing energy costs
            'technology': -0.05,    # Data centers, but less sensitive
            'financials': -0.08,    # Indirect through economic impact
            'healthcare': -0.03,    # Relatively insulated
            'real_estate': -0.10    # Heating/cooling costs
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze energy event

        Args:
            event_data:
                - energy_type: oil, natural_gas, electricity, renewable, nuclear
                - event_subtype: shock, disruption, transition, crisis
                - price_change_pct: % change in energy price
                - supply_disruption_pct: % of supply affected
                - duration_estimate_days: Expected duration
                - affected_region: Geographic scope

        Returns:
            Comprehensive energy impact analysis
        """
        energy_type = event_data.get('energy_type', 'oil')
        event_subtype = event_data.get('event_subtype', 'shock')
        price_change = event_data.get('price_change_pct', 0)
        supply_disruption = event_data.get('supply_disruption_pct', 0)
        duration = event_data.get('duration_estimate_days', 30)
        region = event_data.get('affected_region', 'global')

        # Analyze immediate impact
        immediate = self._analyze_immediate_impact(
            energy_type, price_change, supply_disruption
        )

        # Cross-sector cascade
        cascade = self._analyze_energy_cascade(
            energy_type, price_change, duration
        )

        # Market predictions
        predictions = self._predict_market_reactions(
            energy_type, price_change, supply_disruption, cascade
        )

        # Investment strategies
        strategies = self._generate_energy_strategies(
            energy_type, event_subtype, price_change, duration
        )

        return {
            'event_assessment': {
                'energy_type': energy_type,
                'event_subtype': event_subtype,
                'price_impact': price_change,
                'supply_impact': supply_disruption,
                'duration': duration,
                'severity_score': self._calculate_severity(price_change, supply_disruption)
            },
            'immediate_impact': immediate,
            'cross_sector_cascade': cascade,
            'predictions': predictions,
            'investment_strategies': strategies,
            'inflation_impact': self._calculate_inflation_impact(energy_type, price_change),
            'recession_risk': self._assess_recession_risk(energy_type, price_change, duration),
            'historical_analogs': self._get_historical_analogs(energy_type, price_change)
        }

    def _analyze_immediate_impact(
        self, energy_type: str, price_change: float, supply_disruption: float
    ) -> Dict:
        """Analyze immediate sector impacts"""

        impacts = {}

        if energy_type == 'oil':
            impacts = {
                'airlines': {
                    'impact_pct': price_change * self.energy_elasticity['airlines'],
                    'rationale': 'Jet fuel = 25% of costs. Each $10/barrel = -$1B annual cost for major airline',
                    'timeframe': 'Immediate'
                },
                'transportation': {
                    'impact_pct': price_change * self.energy_elasticity['transportation'],
                    'rationale': 'Diesel costs directly affect trucking, shipping, logistics',
                    'timeframe': 'Immediate'
                },
                'consumer': {
                    'impact_pct': price_change * self.energy_elasticity['consumer'],
                    'rationale': 'Gasoline costs reduce discretionary spending',
                    'timeframe': '1-2 weeks'
                },
                'energy_sector': {
                    'impact_pct': price_change * self.energy_elasticity['energy'],
                    'rationale': 'Oil producers benefit from higher prices',
                    'timeframe': 'Immediate'
                }
            }

        elif energy_type == 'natural_gas':
            impacts = {
                'utilities': {
                    'impact_pct': price_change * 0.35,
                    'rationale': 'Nat gas = primary fuel for power generation',
                    'timeframe': 'Immediate'
                },
                'chemicals': {
                    'impact_pct': price_change * -0.25,
                    'rationale': 'Nat gas = feedstock for fertilizers, plastics',
                    'timeframe': '1-2 weeks'
                },
                'agriculture': {
                    'impact_pct': price_change * -0.18,
                    'rationale': 'Fertilizer costs rise, farm input costs up',
                    'timeframe': '2-4 weeks'
                },
                'consumer': {
                    'impact_pct': price_change * -0.10,
                    'rationale': 'Heating costs for households',
                    'timeframe': 'Seasonal (winter)'
                }
            }

        return impacts

    def _analyze_energy_cascade(
        self, energy_type: str, price_change: float, duration: int
    ) -> Dict:
        """Analyze how energy shock cascades through economy"""

        if energy_type == 'oil' and price_change > 30:  # Oil shock >30%
            return {
                'cascade_stages': [
                    {
                        'stage': 1,
                        'timeframe': 'Week 0-2',
                        'event': f'Oil prices spike {price_change:.0f}%',
                        'sectors': ['energy', 'airlines', 'transportation'],
                        'impact': 'Immediate cost increases, stock price reactions'
                    },
                    {
                        'stage': 2,
                        'timeframe': 'Week 2-6',
                        'event': 'Transportation costs rise across all logistics',
                        'sectors': ['logistics', 'retail', 'consumer', 'manufacturing'],
                        'impact': 'Supply chain inflation, companies announce price increases',
                        'magnitude': price_change * 0.4
                    },
                    {
                        'stage': 3,
                        'timeframe': 'Week 6-12',
                        'event': 'Consumer prices rise (CPI impact)',
                        'sectors': ['consumer_staples', 'consumer_discretionary', 'restaurants'],
                        'impact': 'Demand destruction begins, consumer spending weakens',
                        'magnitude': price_change * 0.25
                    },
                    {
                        'stage': 4,
                        'timeframe': 'Week 12-26',
                        'event': 'Economic growth slows',
                        'sectors': ['all_sectors'],
                        'impact': 'GDP growth reduced, recession risk increases',
                        'magnitude': price_change * 0.15,
                        'historical_note': '10 of last 11 US recessions preceded by oil shock'
                    },
                    {
                        'stage': 5,
                        'timeframe': 'Week 26+',
                        'event': 'Policy response (Fed, government)',
                        'sectors': ['financials', 'real_estate'],
                        'impact': 'Interest rate policy, potential strategic petroleum reserve release',
                        'magnitude': 'Variable based on policy effectiveness'
                    }
                ],
                'feedback_loops': [
                    'Higher oil → Weaker economy → Lower oil demand → Prices stabilize',
                    'Higher oil → Inflation → Fed hikes → Recession → Demand destruction',
                    'Higher oil → Consumer spending down → Earnings warnings → Market sells off → Wealth effect negative'
                ]
            }

        elif energy_type == 'natural_gas' and price_change > 50:
            return {
                'cascade_stages': [
                    {
                        'stage': 1,
                        'timeframe': 'Week 0-1',
                        'event': f'Natural gas prices spike {price_change:.0f}%',
                        'sectors': ['utilities', 'energy'],
                        'impact': 'Power generation costs surge'
                    },
                    {
                        'stage': 2,
                        'timeframe': 'Week 1-4',
                        'event': 'Electricity prices rise',
                        'sectors': ['industrials', 'materials', 'chemicals'],
                        'impact': 'Energy-intensive industries face margin compression',
                        'example': 'Aluminum smelters shut down (happened in Europe 2022)'
                    },
                    {
                        'stage': 3,
                        'timeframe': 'Week 4-12',
                        'event': 'Fertilizer production cuts',
                        'sectors': ['chemicals', 'agriculture'],
                        'impact': 'Ammonia/urea production becomes unprofitable',
                        'magnitude': price_change * 0.3
                    },
                    {
                        'stage': 4,
                        'timeframe': 'Month 3-9',
                        'event': 'Global food inflation',
                        'sectors': ['agriculture', 'food', 'emerging_markets'],
                        'impact': 'Fertilizer shortage → Crop yields down → Food prices spike',
                        'magnitude': 'Can cause social unrest in emerging markets'
                    }
                ],
                'regional_differences': {
                    'Europe': 'Highly vulnerable - Russia gas dependence (pre-2022)',
                    'US': 'Natural gas producer - domestic prices more stable',
                    'Asia': 'LNG import dependent - vulnerable to global prices'
                }
            }

        return {
            'cascade_stages': [{'stage': 1, 'event': 'Standard energy price movement', 'impact': 'Moderate'}],
            'feedback_loops': []
        }

    def _predict_market_reactions(
        self, energy_type: str, price_change: float, supply_disruption: float, cascade: Dict
    ) -> Dict:
        """Predict market-level reactions"""

        # Calculate sector-by-sector predictions
        sector_predictions = {}
        for sector, elasticity in self.energy_elasticity.items():
            impact_pct = price_change * elasticity
            sector_predictions[sector] = {
                'expected_move': impact_pct,
                'direction': 'up' if impact_pct > 0 else 'down',
                'confidence': 0.75  # Energy impacts are fairly predictable
            }

        # Overall market impact
        # Oil shocks generally negative for market (unless you're energy sector)
        market_impact = -abs(price_change) * 0.20  # -20% of oil move translates to market

        return {
            'market_predictions': {
                'overall_market': market_impact,
                'sector_specific': sector_predictions,
                'timeline': self._predict_price_movement_timeline(price_change)
            },
            'volatility_impact': {
                'vix_increase_expected': abs(price_change) * 0.15,
                'energy_sector_vol_increase': abs(price_change) * 0.25
            },
            'correlation_changes': {
                'note': 'Energy shocks break normal correlations',
                'energy_vs_market': 'Negative correlation increases',
                'defensives_vs_cyclicals': 'Defensives outperform'
            }
        }

    def _predict_price_movement_timeline(self, price_change: float) -> Dict:
        """Predict how stock prices move over time"""

        if abs(price_change) > 30:  # Major shock
            return {
                'day_1': 'Energy stocks +10-20%, airlines -8-15%, market -2-4%',
                'week_1': 'Continued volatility, macro concerns emerge',
                'month_1': 'Earnings warnings from affected sectors, market digests',
                'month_3': 'Economic data weakens, recession fears if sustained',
                'month_6': 'Demand destruction kicks in, prices stabilize',
                'note': 'Historical pattern from 1973, 1979, 1990, 2008 oil shocks'
            }
        else:
            return {
                'day_1': 'Moderate sector rotation',
                'week_1': 'Market absorbs change',
                'month_1': 'Returns to normal',
                'note': 'Minor price fluctuations don't materially impact economy'
            }

    def _generate_energy_strategies(
        self, energy_type: str, event_subtype: str, price_change: float, duration: int
    ) -> Dict:
        """Generate investment strategies for energy events"""

        strategies = {
            'immediate_trades': [],
            'pairs_trades': [],
            'options_strategies': [],
            'long_term_themes': []
        }

        # Oil shock strategies
        if energy_type == 'oil' and price_change > 20:
            strategies['immediate_trades'] = [
                {'action': 'Long', 'ticker': 'XLE (Energy ETF)', 'rationale': 'Oil producers benefit', 'return': f'+{price_change * 0.8:.0f}%'},
                {'action': 'Short', 'ticker': 'JETS (Airline ETF)', 'rationale': 'Fuel costs spike', 'return': f'{price_change * 0.35:.0f}%'},
                {'action': 'Long', 'ticker': 'XLU (Utilities)', 'rationale': 'Defensive play', 'return': '+5-10%'}
            ]
            strategies['pairs_trades'] = [
                {'long': 'Exxon (XOM)', 'short': 'Delta (DAL)', 'rationale': 'Classic energy shock play'},
                {'long': 'ConocoPhillips (COP)', 'short': 'Uber (UBER)', 'rationale': 'Producer vs high fuel cost business'}
            ]
            strategies['options_strategies'] = [
                {'strategy': 'Buy XLE calls', 'strike': 'ATM', 'expiration': '60 DTE', 'expected_return': '+50-150%'},
                {'strategy': 'Buy JETS puts', 'strike': '5% OTM', 'expiration': '45 DTE', 'expected_return': '+30-80%'}
            ]

        # Natural gas spike strategies
        elif energy_type == 'natural_gas' and price_change > 30:
            strategies['immediate_trades'] = [
                {'action': 'Long', 'ticker': 'UNG (Nat Gas ETF)', 'rationale': 'Direct exposure', 'return': f'+{price_change * 0.6:.0f}%'},
                {'action': 'Short', 'ticker': 'CF Industries (CF)', 'rationale': 'Fertilizer margins compressed', 'return': '-15-25%'},
                {'action': 'Long', 'ticker': 'EQT (Nat Gas Producer)', 'rationale': 'Largest US producer benefits', 'return': '+30-50%'}
            ]

        # Renewable energy transition
        elif energy_type == 'renewable' and event_subtype == 'transition':
            strategies['long_term_themes'] = [
                {'theme': 'Solar/Wind build-out', 'tickers': 'ICLN, TAN, FAN', 'horizon': '3-5 years', 'return': '+100-200%'},
                {'theme': 'Battery storage', 'tickers': 'ALB, LAC, SQM (lithium)', 'horizon': '3-5 years', 'return': '+80-150%'},
                {'theme': 'Electric vehicles', 'tickers': 'TSLA, RIVN, charging infrastructure', 'horizon': '3-5 years', 'return': '+50-120%'},
                {'theme': 'Short legacy energy', 'tickers': 'Coal utilities, old pipelines', 'horizon': '5-10 years', 'return': 'Structural decline'}
            ]

        return strategies

    def _calculate_inflation_impact(self, energy_type: str, price_change: float) -> Dict:
        """Calculate impact on inflation"""

        # Energy weight in CPI: ~7-8%
        # But indirect effects (transportation) add another 5-7%
        # Total energy influence on CPI: ~12-15%

        direct_cpi_impact = (price_change / 100) * 0.08  # 8% weight
        indirect_cpi_impact = (price_change / 100) * 0.06  # 6% indirect
        total_cpi_impact = direct_cpi_impact + indirect_cpi_impact

        return {
            'cpi_impact_pct': total_cpi_impact * 100,
            'direct_component': direct_cpi_impact * 100,
            'indirect_component': indirect_cpi_impact * 100,
            'timeline': {
                'month_1': 'Direct impact shows up in CPI',
                'month_2_3': 'Indirect impacts through transportation, food',
                'month_4_plus': 'Second-round effects as wages adjust'
            },
            'fed_response_likely': total_cpi_impact > 0.005,  # >0.5pp CPI move triggers Fed concern
            'historical_note': '1970s oil shocks caused stagflation - growth down, inflation up'
        }

    def _assess_recession_risk(self, energy_type: str, price_change: float, duration: int) -> Dict:
        """Assess recession risk from energy shock"""

        # Historical: 10 of 11 US recessions preceded by oil shock
        # Rule of thumb: Oil spike >50% that lasts >6 months = recession risk

        recession_probability = 0.0

        if energy_type == 'oil':
            if price_change > 50 and duration > 180:
                recession_probability = 0.75  # 75% chance
            elif price_change > 30 and duration > 90:
                recession_probability = 0.50  # 50% chance
            elif price_change > 20:
                recession_probability = 0.25  # 25% chance

        return {
            'recession_probability': recession_probability,
            'rationale': f'{price_change:.0f}% price change over {duration} days',
            'mechanism': [
                'Higher energy costs → Consumer spending falls',
                'Transportation/logistics more expensive → Business margins compress',
                'Inflation rises → Fed tightens → Demand destruction',
                'Uncertainty rises → Investment delayed → Growth slows'
            ],
            'historical_precedents': [
                '1973-74 Oil Embargo: Oil 4x → Recession',
                '1979-80 Iranian Revolution: Oil +150% → Recession',
                '1990 Gulf War: Oil +100% → Recession',
                '2008 Oil spike to $147 → Great Recession (contributed)',
                '2022 Russia-Ukraine: Gas spike in Europe → Recession risk'
            ],
            'mitigating_factors': [
                'SPR releases can dampen spikes',
                'Renewable energy reduces oil dependence over time',
                'US shale production can ramp quickly',
                'Demand destruction self-corrects at high enough prices'
            ]
        }

    def _calculate_severity(self, price_change: float, supply_disruption: float) -> int:
        """Calculate severity score 1-5"""

        # Price change severity
        if abs(price_change) > 100:
            price_severity = 5
        elif abs(price_change) > 50:
            price_severity = 4
        elif abs(price_change) > 30:
            price_severity = 3
        elif abs(price_change) > 15:
            price_severity = 2
        else:
            price_severity = 1

        # Supply disruption severity
        if supply_disruption > 20:
            supply_severity = 5
        elif supply_disruption > 10:
            supply_severity = 4
        elif supply_disruption > 5:
            supply_severity = 3
        elif supply_disruption > 2:
            supply_severity = 2
        else:
            supply_severity = 1

        # Take max of both
        return max(price_severity, supply_severity)

    def _get_historical_analogs(self, energy_type: str, price_change: float) -> List[Dict]:
        """Get historical energy events"""

        if energy_type == 'oil':
            return [
                {
                    'event': '1973 Oil Embargo',
                    'price_change': '+400%',
                    'impact': 'Severe recession, stagflation era begins',
                    'market': 'S&P 500 -48% peak to trough',
                    'duration': '1973-1975',
                    'lessons': 'Energy shocks can cause both recession AND inflation'
                },
                {
                    'event': '2008 Oil Spike',
                    'price_change': '+140% to $147/barrel',
                    'impact': 'Contributed to Great Recession',
                    'market': 'S&P 500 -57%',
                    'duration': '2007-2009',
                    'lessons': 'High oil prices broke consumer spending just before financial crisis'
                },
                {
                    'event': '2014 Oil Crash',
                    'price_change': '-70% ($100→$30)',
                    'impact': 'Energy sector bloodbath, but broader market benefited',
                    'market': 'XLE -50%, but SPY +3%',
                    'duration': '2014-2016',
                    'lessons': 'Oil crash = transfer of wealth from producers to consumers'
                },
                {
                    'event': '2020 COVID Oil Crash',
                    'price_change': '-100% (went NEGATIVE!)',
                    'impact': 'Unprecedented - storage full, no demand',
                    'market': 'XLE -60%, SPY recovered quickly',
                    'duration': 'April 2020',
                    'lessons': 'Demand shock more severe than supply shock'
                }
            ]

        return []
