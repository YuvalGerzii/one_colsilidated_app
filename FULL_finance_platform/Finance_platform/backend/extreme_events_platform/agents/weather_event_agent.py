"""
Weather Event Agent (V5.0)

Analyzes weather and climate events that impact markets:
- Heatwaves: Energy demand spikes, crop damage, infrastructure stress
- Droughts: Agricultural impact, water scarcity, energy production constraints
- Cold snaps: Natural gas demand, heating costs, crop damage
- Floods: Infrastructure damage, supply chain disruption, insurance claims
- Hurricanes: Regional economic impact, commodity disruptions

Key insight: Weather events create cascading impacts across seemingly unrelated sectors.
Example: Texas freeze 2021 → Natural gas spike → Chemical production halted →
         Semiconductor fab shutdowns → Auto production delays → Tech supply shortage
"""

from typing import Dict, List
from ..agents.base_agent import BaseAgent


class WeatherEventAgent(BaseAgent):
    """
    Analyzes weather and climate events with cross-sector impact analysis.

    Weather events demonstrate perfect example of sector interconnection:
    - Heatwave in Texas → Power grid strain → Bitcoin mining halts → Crypto prices affected
    - Drought in Taiwan → Semiconductor water shortage → Chip production down → Tech stocks fall
    - Hurricane in Gulf → Oil rigs shutdown → Gas prices spike → Airline stocks drop
    """

    def __init__(self, config):
        """Initialize weather event agent"""
        super().__init__(config)

        # Sector vulnerability by weather event type
        self.sector_impacts = {
            'heatwave': {
                'primary_affected': ['utilities', 'energy', 'agriculture'],
                'secondary_affected': ['technology', 'consumer', 'transportation'],
                'tertiary_affected': ['financials', 'industrials', 'healthcare']
            },
            'drought': {
                'primary_affected': ['agriculture', 'utilities', 'beverages'],
                'secondary_affected': ['food_processing', 'chemicals', 'technology'],
                'tertiary_affected': ['transportation', 'consumer', 'materials']
            },
            'cold_snap': {
                'primary_affected': ['energy', 'utilities', 'agriculture'],
                'secondary_affected': ['chemicals', 'materials', 'transportation'],
                'tertiary_affected': ['technology', 'consumer', 'industrials']
            },
            'flood': {
                'primary_affected': ['insurance', 'real_estate', 'transportation'],
                'secondary_affected': ['agriculture', 'utilities', 'materials'],
                'tertiary_affected': ['consumer', 'industrials', 'financials']
            },
            'hurricane': {
                'primary_affected': ['energy', 'insurance', 'real_estate'],
                'secondary_affected': ['transportation', 'utilities', 'materials'],
                'tertiary_affected': ['consumer', 'financials', 'industrials']
            }
        }

        # Cross-sector contagion pathways
        self.contagion_pathways = {
            'heatwave_texas': [
                'Power grid strain → Rolling blackouts',
                'Bitcoin mining halts → Crypto price volatility',
                'Data centers overheat → Cloud service disruptions → Tech stocks',
                'AC demand surge → Utility stocks rally, natural gas prices spike',
                'Crop damage → Food price inflation → Consumer staples affected'
            ],
            'drought_taiwan': [
                'Water restrictions → Semiconductor fabs reduce output',
                'Chip shortage intensifies → Auto production delays',
                'Tech supply chain disrupted → AAPL, NVDA, AMD affected',
                'Agricultural losses → Food export restrictions',
                'Hydropower reduced → Electricity imports increase'
            ],
            'freeze_texas_2021': [
                'Natural gas freeze-offs → Prices spike 100x',
                'Chemical plants shutdown → Plastics shortage',
                'Semiconductor fabs halt → Global chip shortage worsens',
                'Oil refineries offline → Gasoline supply disrupted',
                'Burst pipes → Insurance claims surge → Property casualty stocks'
            ]
        }

    def analyze_event(self, event_data: Dict) -> Dict:
        """
        Analyze weather event with cross-sector impact

        Args:
            event_data: Weather event details
                - weather_type: heatwave, drought, cold_snap, flood, hurricane
                - region: Affected region
                - severity: 1-5 scale
                - duration_days: Event duration
                - temperature_extreme: For heatwaves/cold snaps (deviation from normal)
                - precipitation_pct: For droughts/floods (% of normal)

        Returns:
            Analysis with cross-sector impacts
        """
        weather_type = event_data.get('weather_type', 'heatwave')
        region = event_data.get('region', 'unknown')
        severity = event_data.get('severity', 3)
        duration = event_data.get('duration_days', 7)

        # Analyze immediate impact
        immediate_impact = self._analyze_immediate_impact(weather_type, region, severity)

        # Trace contagion across sectors
        contagion_analysis = self._analyze_cross_sector_contagion(
            weather_type, region, severity, duration
        )

        # Predict market impact
        market_predictions = self._predict_market_impact(
            weather_type, immediate_impact, contagion_analysis, severity
        )

        # Identify investment opportunities
        opportunities = self._identify_opportunities(
            weather_type, contagion_analysis, severity
        )

        return {
            'event_assessment': {
                'weather_type': weather_type,
                'region': region,
                'severity': severity,
                'duration_days': duration,
                'economic_magnitude': self._calculate_economic_magnitude(severity, duration, region)
            },
            'immediate_impact': immediate_impact,
            'cross_sector_contagion': contagion_analysis,
            'predictions': market_predictions,
            'investment_opportunities': opportunities,
            'historical_precedents': self._get_historical_precedents(weather_type, region),
            'risk_assessment': self._assess_systemic_risk(contagion_analysis)
        }

    def _analyze_immediate_impact(self, weather_type: str, region: str, severity: int) -> Dict:
        """Analyze immediate sector impacts"""

        impacts = self.sector_impacts.get(weather_type, {})

        # Regional multipliers (some regions more critical)
        regional_importance = {
            'Texas': 2.0,  # Major energy hub
            'California': 1.8,  # Major agriculture + tech
            'Taiwan': 2.5,  # Critical semiconductor production
            'Gulf_Coast': 2.2,  # Oil and gas production
            'Midwest': 1.5,  # Agriculture heartland
            'Northeast': 1.3   # Population center
        }

        multiplier = regional_importance.get(region, 1.0)

        return {
            'primary_sectors': {
                'affected': impacts.get('primary_affected', []),
                'impact_magnitude': severity * multiplier * 0.3,  # 30% per severity level
                'timeframe': '0-7 days'
            },
            'secondary_sectors': {
                'affected': impacts.get('secondary_affected', []),
                'impact_magnitude': severity * multiplier * 0.15,  # 15% per severity level
                'timeframe': '7-30 days'
            },
            'tertiary_sectors': {
                'affected': impacts.get('tertiary_affected', []),
                'impact_magnitude': severity * multiplier * 0.08,  # 8% per severity level
                'timeframe': '30-90 days'
            }
        }

    def _analyze_cross_sector_contagion(
        self, weather_type: str, region: str, severity: int, duration: int
    ) -> Dict:
        """Trace how impact spreads across seemingly unrelated sectors"""

        # Example: Texas heatwave
        if weather_type == 'heatwave' and 'Texas' in region:
            return {
                'contagion_chain': [
                    {
                        'stage': 1,
                        'timeframe': 'Day 0-3',
                        'trigger': 'Extreme heat (105-115°F)',
                        'primary_effect': 'Power grid strain, ERCOT emergency',
                        'affected_sectors': ['utilities', 'energy'],
                        'magnitude': severity * 0.4
                    },
                    {
                        'stage': 2,
                        'timeframe': 'Day 3-7',
                        'trigger': 'Rolling blackouts implemented',
                        'primary_effect': 'Industrial production halts',
                        'affected_sectors': ['technology', 'chemicals', 'materials'],
                        'magnitude': severity * 0.3,
                        'cascade': 'Bitcoin miners shutdown (Texas = 15% of US Bitcoin mining)'
                    },
                    {
                        'stage': 3,
                        'timeframe': 'Day 7-14',
                        'trigger': 'Extended outages',
                        'primary_effect': 'Supply chain disruptions',
                        'affected_sectors': ['semiconductors', 'autos', 'consumer_electronics'],
                        'magnitude': severity * 0.2,
                        'cascade': 'Samsung/NXP fabs in Austin affected → Global chip shortage'
                    },
                    {
                        'stage': 4,
                        'timeframe': 'Day 14-30',
                        'trigger': 'Crop damage, livestock stress',
                        'primary_effect': 'Agricultural losses',
                        'affected_sectors': ['agriculture', 'food', 'consumer_staples'],
                        'magnitude': severity * 0.25,
                        'cascade': 'Cattle losses → Beef prices spike → Restaurant margins compress'
                    }
                ],
                'unexpected_connections': [
                    'Heatwave → Data centers overheat → Cloud outages → SaaS companies affected',
                    'Heatwave → AC demand → Natural gas spike → Fertilizer production costs rise → Agriculture input costs up',
                    'Heatwave → Tourism decline → Hospitality sector weakness → Regional banks stressed'
                ]
            }

        # Example: Taiwan drought
        elif weather_type == 'drought' and 'Taiwan' in region:
            return {
                'contagion_chain': [
                    {
                        'stage': 1,
                        'timeframe': 'Week 0-2',
                        'trigger': 'Reservoir levels <20%',
                        'primary_effect': 'Water rationing',
                        'affected_sectors': ['utilities', 'agriculture'],
                        'magnitude': severity * 0.3
                    },
                    {
                        'stage': 2,
                        'timeframe': 'Week 2-8',
                        'trigger': 'Industrial water restrictions',
                        'primary_effect': 'TSMC fabs reduce production',
                        'affected_sectors': ['semiconductors'],
                        'magnitude': severity * 0.5,
                        'cascade': 'TSMC = 53% of global foundry market → Massive shortage'
                    },
                    {
                        'stage': 3,
                        'timeframe': 'Week 8-20',
                        'trigger': 'Chip shortage intensifies',
                        'primary_effect': 'Auto/tech production cuts',
                        'affected_sectors': ['autos', 'consumer_electronics', 'technology'],
                        'magnitude': severity * 0.4,
                        'cascade': 'Ford, GM, Toyota cut production → Auto stocks fall 15-20%'
                    },
                    {
                        'stage': 4,
                        'timeframe': 'Week 20+',
                        'trigger': 'Global supply chain restructuring',
                        'primary_effect': 'Geopolitical risk repricing',
                        'affected_sectors': ['all_sectors'],
                        'magnitude': severity * 0.2,
                        'cascade': 'Taiwan risk premium increases → Diversification to US/Europe fabs'
                    }
                ],
                'unexpected_connections': [
                    'Drought → Hydropower down → Coal imports up → Shipping rates rise → Logistics costs affect all sectors',
                    'Drought → Rice crop failure → Food inflation → Consumer spending shifts → Retail affected',
                    'Drought → TSMC water costs up → Chip prices rise → Graphics cards expensive → Nvidia margins expand'
                ]
            }

        # Generic contagion for other weather events
        else:
            return {
                'contagion_chain': [
                    {
                        'stage': 1,
                        'timeframe': 'Immediate (0-7 days)',
                        'trigger': f'{weather_type} event',
                        'primary_effect': 'Direct physical damage and disruption',
                        'affected_sectors': self.sector_impacts.get(weather_type, {}).get('primary_affected', []),
                        'magnitude': severity * 0.3
                    },
                    {
                        'stage': 2,
                        'timeframe': 'Short-term (7-30 days)',
                        'trigger': 'Supply chain disruptions',
                        'primary_effect': 'Production delays and shortages',
                        'affected_sectors': self.sector_impacts.get(weather_type, {}).get('secondary_affected', []),
                        'magnitude': severity * 0.2
                    },
                    {
                        'stage': 3,
                        'timeframe': 'Medium-term (30-90 days)',
                        'trigger': 'Economic ripple effects',
                        'primary_effect': 'Broader market impact',
                        'affected_sectors': self.sector_impacts.get(weather_type, {}).get('tertiary_affected', []),
                        'magnitude': severity * 0.1
                    }
                ],
                'unexpected_connections': [
                    f'{weather_type} creates multi-sector cascades',
                    'Insurance sector heavily impacted',
                    'Regional economic stress affects banks'
                ]
            }

    def _predict_market_impact(
        self, weather_type: str, immediate: Dict, contagion: Dict, severity: int
    ) -> Dict:
        """Predict market-level impacts"""

        # Calculate aggregate impact
        primary_impact = immediate['primary_sectors']['impact_magnitude']
        secondary_impact = immediate['secondary_sectors']['impact_magnitude']

        total_market_impact = -(primary_impact + secondary_impact * 0.5)  # Negative for market

        return {
            'market_predictions': {
                'overall_market_impact': total_market_impact,
                'sector_specific': self._get_sector_predictions(weather_type, severity),
                'timeline': {
                    'immediate_7days': total_market_impact * 0.6,
                    'short_term_30days': total_market_impact * 0.3,
                    'medium_term_90days': total_market_impact * 0.1
                }
            },
            'volatility_forecast': {
                'vix_expected_increase': severity * 3.0,  # +3 VIX points per severity level
                'sector_dispersion_increase': severity * 0.15  # Stock correlations break down
            },
            'recovery_estimate': {
                'market_recovery_days': 30 + (severity * 10),
                'sector_recovery_variance': 'High - some sectors benefit (insurance, reconstruction)'
            }
        }

    def _get_sector_predictions(self, weather_type: str, severity: int) -> Dict:
        """Get detailed sector predictions"""

        predictions = {}

        # Heatwave impacts
        if weather_type == 'heatwave':
            predictions = {
                'utilities': {'direction': 'up', 'magnitude': severity * 8, 'rationale': 'Electricity demand surge'},
                'energy': {'direction': 'up', 'magnitude': severity * 12, 'rationale': 'Natural gas, coal demand for power'},
                'agriculture': {'direction': 'down', 'magnitude': -severity * 15, 'rationale': 'Crop damage, livestock stress'},
                'consumer_staples': {'direction': 'down', 'magnitude': -severity * 5, 'rationale': 'Food inflation'},
                'technology': {'direction': 'down', 'magnitude': -severity * 8, 'rationale': 'Data center disruptions'},
                'insurance': {'direction': 'down', 'magnitude': -severity * 10, 'rationale': 'Claims for crop/property damage'}
            }

        # Drought impacts
        elif weather_type == 'drought':
            predictions = {
                'agriculture': {'direction': 'down', 'magnitude': -severity * 25, 'rationale': 'Crop failures'},
                'beverages': {'direction': 'down', 'magnitude': -severity * 12, 'rationale': 'Water costs, ingredient prices'},
                'utilities': {'direction': 'mixed', 'magnitude': severity * 5, 'rationale': 'Hydropower down, but rates up'},
                'technology': {'direction': 'down', 'magnitude': -severity * 18, 'rationale': 'Fab water shortages (Taiwan)'},
                'chemicals': {'direction': 'down', 'magnitude': -severity * 10, 'rationale': 'Water-intensive production affected'},
                'water_utilities': {'direction': 'up', 'magnitude': severity * 15, 'rationale': 'Scarcity value, rate increases'}
            }

        # Cold snap impacts
        elif weather_type == 'cold_snap':
            predictions = {
                'energy': {'direction': 'up', 'magnitude': severity * 20, 'rationale': 'Heating demand, nat gas spike'},
                'utilities': {'direction': 'up', 'magnitude': severity * 10, 'rationale': 'Electricity usage'},
                'chemicals': {'direction': 'down', 'magnitude': -severity * 15, 'rationale': 'Freeze-offs, shutdowns'},
                'materials': {'direction': 'down', 'magnitude': -severity * 12, 'rationale': 'Production halts'},
                'transportation': {'direction': 'down', 'magnitude': -severity * 8, 'rationale': 'Travel disruptions'},
                'semiconductors': {'direction': 'down', 'magnitude': -severity * 10, 'rationale': 'Fab disruptions (Texas 2021)'}
            }

        return predictions

    def _identify_opportunities(
        self, weather_type: str, contagion: Dict, severity: int
    ) -> Dict:
        """Identify trading opportunities from weather event"""

        opportunities = {
            'immediate_trades': [],
            'pairs_trades': [],
            'derivatives_plays': [],
            'contrarian_bets': []
        }

        # Heatwave opportunities
        if weather_type == 'heatwave':
            opportunities['immediate_trades'] = [
                {'action': 'Long', 'ticker': 'XLU (Utilities ETF)', 'rationale': 'Power demand surge', 'expected_return': '+8-15%'},
                {'action': 'Long', 'ticker': 'UNG (Natural Gas)', 'rationale': 'Cooling demand', 'expected_return': '+15-30%'},
                {'action': 'Short', 'ticker': 'Crop-dependent food stocks', 'rationale': 'Agricultural damage', 'expected_return': '-10-20%'}
            ]
            opportunities['pairs_trades'] = [
                {'long': 'Duke Energy (DUK)', 'short': 'Archer Daniels Midland (ADM)', 'rationale': 'Utilities benefit, agriculture hurt'}
            ]
            opportunities['derivatives_plays'] = [
                {'strategy': 'Buy nat gas call options', 'rationale': 'Asymmetric upside on cooling demand'},
                {'strategy': 'Buy crop price put options', 'rationale': 'Hedge food inflation'}
            ]

        # Drought opportunities
        elif weather_type == 'drought':
            opportunities['immediate_trades'] = [
                {'action': 'Short', 'ticker': 'Taiwan Semiconductor (TSM)', 'rationale': 'Water shortage risk', 'expected_return': '-15-25%'},
                {'action': 'Long', 'ticker': 'Intel (INTC)', 'rationale': 'Benefits from TSMC weakness', 'expected_return': '+5-12%'},
                {'action': 'Long', 'ticker': 'Water ETFs (PHO, FIW)', 'rationale': 'Water scarcity value', 'expected_return': '+10-18%'}
            ]
            opportunities['contrarian_bets'] = [
                {'bet': 'Buy TSM after 20% decline', 'rationale': 'Taiwan will prioritize chip fabs, drought temporary'}
            ]

        return opportunities

    def _calculate_economic_magnitude(self, severity: int, duration: int, region: str) -> float:
        """Calculate economic impact in billions"""

        # Base impact per severity level per day
        base_impact_per_day = {
            1: 0.1,   # $100M/day
            2: 0.5,   # $500M/day
            3: 1.0,   # $1B/day
            4: 2.5,   # $2.5B/day
            5: 5.0    # $5B/day
        }

        daily_impact = base_impact_per_day.get(severity, 1.0)
        total_impact = daily_impact * duration

        # Regional multiplier (larger economies = larger impact)
        regional_gdp_importance = {
            'Texas': 2.0,      # $2T economy
            'California': 3.5,  # $3.5T economy
            'Taiwan': 0.8,     # But critical for global supply chains
            'Midwest': 1.5
        }

        multiplier = regional_gdp_importance.get(region, 1.0)

        return total_impact * multiplier

    def _get_historical_precedents(self, weather_type: str, region: str) -> List[Dict]:
        """Get historical examples"""

        precedents = {
            'heatwave': [
                {
                    'event': 'Europe Heatwave 2003',
                    'impact': '70,000 deaths, $13B economic loss',
                    'market_reaction': 'Utilities +15%, Agriculture -12%',
                    'key_lesson': 'Infrastructure not built for extreme heat'
                },
                {
                    'event': 'Texas Heatwave 2011',
                    'impact': '$7.6B agricultural losses',
                    'market_reaction': 'Cattle futures +40%, Grain -25%',
                    'key_lesson': 'Livestock particularly vulnerable'
                }
            ],
            'drought': [
                {
                    'event': 'California Drought 2012-2016',
                    'impact': '$2.7B/year agricultural loss',
                    'market_reaction': 'Agriculture -15%, Water utilities +25%',
                    'key_lesson': 'Long-duration droughts create structural changes'
                },
                {
                    'event': 'Taiwan Drought 2021',
                    'impact': 'TSMC production at risk, global chip shortage',
                    'market_reaction': 'TSM -8%, chip prices +20%',
                    'key_lesson': 'Single point of failure in global supply chains'
                }
            ],
            'cold_snap': [
                {
                    'event': 'Texas Freeze February 2021',
                    'impact': '$195B total damage, 4.5M without power',
                    'market_reaction': 'Nat gas +100x, Utilities -20%, Chemicals -15%',
                    'key_lesson': 'Infrastructure failure cascades across sectors'
                }
            ]
        }

        return precedents.get(weather_type, [])

    def _assess_systemic_risk(self, contagion: Dict) -> Dict:
        """Assess whether event poses systemic risk"""

        # Count contagion stages and affected sectors
        num_stages = len(contagion.get('contagion_chain', []))

        if num_stages >= 4:
            risk_level = 'HIGH - Multiple contagion stages'
        elif num_stages >= 2:
            risk_level = 'MEDIUM - Limited contagion'
        else:
            risk_level = 'LOW - Localized impact'

        return {
            'systemic_risk_level': risk_level,
            'contagion_stages': num_stages,
            'key_vulnerabilities': [
                'Critical infrastructure (power, water)',
                'Single points of failure (Taiwan chips)',
                'Just-in-time supply chains',
                'Regional concentration of key industries'
            ],
            'mitigation_strategies': [
                'Diversify supply chains geographically',
                'Build redundancy in critical sectors',
                'Hedge with weather derivatives',
                'Monitor leading indicators (reservoir levels, temperature forecasts)'
            ]
        }
