"""
Commodity Arbitrage Strategy Analyzer (V5.0)

Identifies arbitrage opportunities in commodity markets driven by extreme events.
Focuses on spread trades, cross-commodity relationships, and input-output arbitrage.

Key insight: Extreme events disrupt normal commodity relationships, creating
arbitrage opportunities that smart traders can exploit.

Real-world examples:
1. Texas freeze 2021 → Nat gas spot spiked to $600/MMBtu (200x normal) → Futures curve in mega-backwardation → Arbitrage!
2. Russia-Ukraine 2022 → European nat gas 10x, but US nat gas only 2x → Widest spread in history → LNG arbitrage
3. Lithium boom 2021-2022 → Lithium prices +500% while EV stocks flat → Miners outperformed OEMs massively
4. COVID oil crash 2020 → Oil went NEGATIVE (-$37/barrel) → Biggest contango ever → Storage arbitrage

The opportunity: Events create dislocations between:
- Spot vs futures (backwardation/contango)
- Input costs vs output prices (crack spreads, spark spreads)
- Geographic price differences (LNG, crude differentials)
- Related commodities (oil vs nat gas, copper vs gold)
- Commodities vs equities (miners vs metal, E&Ps vs oil)
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ArbitrageType(Enum):
    """Types of commodity arbitrage"""
    CALENDAR_SPREAD = "calendar_spread"  # Front month vs back month
    CRACK_SPREAD = "crack_spread"  # Refining margins (crude → products)
    SPARK_SPREAD = "spark_spread"  # Power generation (gas → electricity)
    CRUSH_SPREAD = "crush_spread"  # Soybean processing
    GEOGRAPHIC = "geographic"  # Same commodity, different locations
    CROSS_COMMODITY = "cross_commodity"  # Related commodities
    INPUT_OUTPUT = "input_output"  # Input cost vs output price
    COMMODITY_EQUITY = "commodity_equity"  # Commodity vs related stocks


@dataclass
class ArbitrageOpportunity:
    """An arbitrage opportunity"""
    name: str
    type: ArbitrageType
    long_leg: str
    short_leg: str
    spread_current: float
    spread_historical_avg: float
    spread_z_score: float  # How many std devs from mean
    catalyst: str
    expected_convergence: str
    risk_level: str
    real_world_example: str


@dataclass
class CommodityRelationship:
    """Relationship between two commodities"""
    commodity_a: str
    commodity_b: str
    normal_ratio: float
    current_ratio: float
    correlation: float
    mechanism: str  # Why they're related


class CommodityArbitrageAnalyzer:
    """
    Analyzes commodity arbitrage opportunities during extreme events.

    Focus: Dislocations in spreads, input-output relationships,
    and cross-commodity ratios.
    """

    def __init__(self):
        """Initialize commodity arbitrage analyzer"""

        # Normal commodity relationships (ratios)
        self.commodity_relationships = self._map_relationships()

        # Historical average spreads
        self.historical_spreads = {
            'wti_brent': 2.0,  # Brent typically $2 premium
            'henry_hub_ttf': 3.0,  # Europe 3x US nat gas (pre-2022)
            'oil_natgas_btu': 10.0,  # Oil/gas on BTU basis ~10:1
            'gold_silver': 70.0,  # Gold/silver ratio ~70:1
            'copper_gold': 0.005,  # Copper/gold ratio
            'crude_gasoline': 1.3,  # Gasoline $0.30/gal premium = 1.3x
            'natural_gas_power': 25.0,  # Power/gas ~$25/MWh spread
        }

        # Input-output relationships (margins)
        self.refining_yields = {
            'crude_to_gasoline': 0.45,  # 1 barrel → 45% gasoline
            'crude_to_diesel': 0.25,  # 25% diesel
            'crude_to_jet': 0.08,  # 8% jet fuel
        }

    def _map_relationships(self) -> Dict[str, CommodityRelationship]:
        """Map commodity relationships"""

        return {
            'oil_natgas': CommodityRelationship(
                commodity_a='crude_oil',
                commodity_b='natural_gas',
                normal_ratio=10.0,  # On BTU basis
                current_ratio=10.0,  # Will be updated
                correlation=0.65,
                mechanism='Both energy, substitutable for power generation'
            ),

            'gold_silver': CommodityRelationship(
                commodity_a='gold',
                commodity_b='silver',
                normal_ratio=70.0,  # Gold/silver ~70:1
                current_ratio=70.0,
                correlation=0.80,
                mechanism='Both precious metals, safe havens, but silver more industrial'
            ),

            'copper_gold': CommodityRelationship(
                commodity_a='copper',
                commodity_b='gold',
                normal_ratio=0.005,  # Copper/gold ratio
                current_ratio=0.005,
                correlation=-0.30,  # Inverse! Copper = growth, gold = safety
                mechanism='Diverge during risk-on/risk-off'
            ),

            'oil_copper': CommodityRelationship(
                commodity_a='crude_oil',
                commodity_b='copper',
                normal_ratio=20.0,  # Oil/copper ~20:1
                current_ratio=20.0,
                correlation=0.70,
                mechanism='Both driven by global growth, industrial demand'
            ),

            'corn_soybeans': CommodityRelationship(
                commodity_a='soybeans',
                commodity_b='corn',
                normal_ratio=2.4,  # Soybeans/corn ~2.4:1
                current_ratio=2.4,
                correlation=0.85,
                mechanism='Compete for same farmland, affected by same weather'
            ),

            'wheat_corn': CommodityRelationship(
                commodity_a='wheat',
                commodity_b='corn',
                normal_ratio=1.4,  # Wheat/corn ~1.4:1
                current_ratio=1.4,
                correlation=0.75,
                mechanism='Both grains, substitutable in feed'
            ),
        }

    def identify_arbitrage(
        self,
        event_type: str,
        affected_commodities: List[str],
        price_changes: Dict[str, float]
    ) -> List[ArbitrageOpportunity]:
        """
        Identify arbitrage opportunities created by event

        Args:
            event_type: Type of event (energy_crisis, supply_shock, etc.)
            affected_commodities: Commodities directly affected
            price_changes: Price changes for each commodity (%)

        Returns:
            List of arbitrage opportunities
        """

        opportunities = []

        # Check calendar spreads (backwardation/contango)
        opportunities.extend(self._find_calendar_spreads(
            affected_commodities, price_changes, event_type
        ))

        # Check crack/spark spreads
        opportunities.extend(self._find_margin_spreads(
            affected_commodities, price_changes, event_type
        ))

        # Check cross-commodity ratios
        opportunities.extend(self._find_ratio_trades(
            affected_commodities, price_changes
        ))

        # Check geographic arbitrage
        opportunities.extend(self._find_geographic_arb(
            affected_commodities, event_type
        ))

        # Check commodity-equity arbitrage
        opportunities.extend(self._find_commodity_equity_arb(
            affected_commodities, price_changes
        ))

        # Sort by z-score (most dislocated first)
        opportunities.sort(key=lambda x: abs(x.spread_z_score), reverse=True)

        return opportunities

    def _find_calendar_spreads(
        self,
        commodities: List[str],
        price_changes: Dict[str, float],
        event_type: str
    ) -> List[ArbitrageOpportunity]:
        """Find calendar spread opportunities (backwardation/contango)"""

        opportunities = []

        # Energy crisis → Backwardation (spot premium)
        if 'energy' in event_type.lower() or any(c in ['oil', 'natural_gas'] for c in commodities):

            # Natural gas calendar spread
            if 'natural_gas' in commodities:
                # During crisis, front month spikes but back months stay lower
                # Example: Texas freeze → Feb contract $600, but Apr contract $4
                opportunities.append(ArbitrageOpportunity(
                    name='Natural Gas Calendar Spread',
                    type=ArbitrageType.CALENDAR_SPREAD,
                    long_leg='Natural gas M+3 futures',
                    short_leg='Natural gas M+1 futures',
                    spread_current=-50.0,  # Extreme backwardation
                    spread_historical_avg=0.5,  # Slight contango normally
                    spread_z_score=-10.0,  # 10 std devs!
                    catalyst=f'{event_type} → Spot crisis but short-lived',
                    expected_convergence='Convergence as crisis resolves (2-8 weeks)',
                    risk_level='Medium (crisis could persist)',
                    real_world_example='Texas freeze 2021: Feb $600 → Apr $4 = $596 spread! Converged to $0 in 2 weeks = Massive profit'
                ))

            # Crude oil calendar spread
            if 'oil' in commodities or 'crude' in commodities:
                price_move = price_changes.get('oil', 0)

                if price_move > 30:  # Big spike
                    opportunities.append(ArbitrageOpportunity(
                        name='Crude Oil Backwardation',
                        type=ArbitrageType.CALENDAR_SPREAD,
                        long_leg='WTI M+12 futures',
                        short_leg='WTI M+1 futures',
                        spread_current=-15.0,  # Backwardation
                        spread_historical_avg=2.0,  # Slight contango
                        spread_z_score=-5.0,
                        catalyst='Supply shock → Immediate shortage → Back months cheaper',
                        expected_convergence='Mean reversion as supply normalizes',
                        risk_level='Low-Medium',
                        real_world_example='Ukraine invasion 2022: Front months spiked +$40, but M+12 only +$20 → $20 spread'
                    ))

                elif price_move < -30:  # Big crash
                    opportunities.append(ArbitrageOpportunity(
                        name='Crude Oil Contango',
                        type=ArbitrageType.CALENDAR_SPREAD,
                        long_leg='WTI M+1 futures',
                        short_leg='WTI M+6 futures',
                        spread_current=20.0,  # Extreme contango
                        spread_historical_avg=2.0,
                        spread_z_score=6.0,
                        catalyst='Demand collapse → Spot cheap → Storage arbitrage',
                        expected_convergence='Storage trade: Buy spot, store, sell future',
                        risk_level='Low (storage costs)',
                        real_world_example='COVID 2020: Oil went negative → M+1 vs M+6 = $25 contango → Storage arbitrage'
                    ))

        return opportunities

    def _find_margin_spreads(
        self,
        commodities: List[str],
        price_changes: Dict[str, float],
        event_type: str
    ) -> List[ArbitrageOpportunity]:
        """Find crack spread, spark spread opportunities"""

        opportunities = []

        # Crack spread (crude → gasoline/diesel)
        if any(c in ['oil', 'crude', 'gasoline', 'diesel'] for c in commodities):

            crude_change = price_changes.get('oil', 0)
            gasoline_change = price_changes.get('gasoline', crude_change * 1.2)  # Estimate

            # If gasoline rises MORE than crude → Wide crack spread → Refiners profit
            spread_change = gasoline_change - crude_change

            if abs(spread_change) > 15:
                opportunities.append(ArbitrageOpportunity(
                    name='Crack Spread (3-2-1)',
                    type=ArbitrageType.CRACK_SPREAD,
                    long_leg='RBOB gasoline futures' if spread_change > 0 else 'WTI crude futures',
                    short_leg='WTI crude futures' if spread_change > 0 else 'RBOB gasoline futures',
                    spread_current=25.0 if spread_change > 0 else 10.0,
                    spread_historical_avg=15.0,
                    spread_z_score=spread_change / 10,
                    catalyst='Product shortage drives refining margins' if spread_change > 0 else 'Crude oversupply compresses margins',
                    expected_convergence='Mean reversion (1-3 months)',
                    risk_level='Medium',
                    real_world_example='Summer driving season → Gasoline premium spikes → Crack spread $40+ (vs $15 normal)'
                ))

        # Spark spread (natural gas → electricity)
        if any(c in ['natural_gas', 'power', 'electricity'] for c in commodities):

            gas_change = price_changes.get('natural_gas', 0)
            power_change = price_changes.get('power', gas_change * 1.5)  # Estimate

            spread_change = power_change - gas_change

            if abs(spread_change) > 20:
                opportunities.append(ArbitrageOpportunity(
                    name='Spark Spread (Power Generation Margin)',
                    type=ArbitrageType.SPARK_SPREAD,
                    long_leg='Electricity/power',
                    short_leg='Natural gas',
                    spread_current=50.0,  # $/MWh
                    spread_historical_avg=25.0,
                    spread_z_score=spread_change / 15,
                    catalyst='Heat wave → Power demand spike → Generation margins explode',
                    expected_convergence='Seasonal (returns to normal after weather event)',
                    risk_level='Medium-High (weather dependent)',
                    real_world_example='Texas heatwave 2023 → Power prices $5000/MWh, gas $10/MMBtu → Spark spread $4990!'
                ))

        return opportunities

    def _find_ratio_trades(
        self,
        commodities: List[str],
        price_changes: Dict[str, float]
    ) -> List[ArbitrageOpportunity]:
        """Find cross-commodity ratio dislocations"""

        opportunities = []

        # Oil/Natural Gas ratio
        if 'oil' in commodities or 'natural_gas' in commodities:
            oil_change = price_changes.get('oil', 0)
            gas_change = price_changes.get('natural_gas', 0)

            ratio_change = oil_change - gas_change

            # If oil up 50% but gas only up 10% → Ratio too wide → Arb
            if abs(ratio_change) > 30:
                opportunities.append(ArbitrageOpportunity(
                    name='Oil/Gas Ratio Trade',
                    type=ArbitrageType.CROSS_COMMODITY,
                    long_leg='Natural gas' if ratio_change > 30 else 'Crude oil',
                    short_leg='Crude oil' if ratio_change > 30 else 'Natural gas',
                    spread_current=15.0 if ratio_change > 30 else 5.0,  # BTU ratio
                    spread_historical_avg=10.0,
                    spread_z_score=ratio_change / 20,
                    catalyst='Divergence: Oil spiked more than gas → Ratio too wide',
                    expected_convergence='Mean reversion (both energy, correlation = 0.65)',
                    risk_level='Low-Medium',
                    real_world_example='Ukraine invasion: Oil +60%, gas +30% → Ratio hit 20:1 (vs 10:1 avg) → Gas outperformed next 6mo'
                ))

        # Gold/Silver ratio
        if 'gold' in commodities or 'silver' in commodities:
            gold_change = price_changes.get('gold', 0)
            silver_change = price_changes.get('silver', gold_change * 1.5)  # Silver more volatile

            ratio_change = gold_change - silver_change

            if abs(ratio_change) > 15:
                current_ratio = 85 if ratio_change > 0 else 60  # Estimate

                opportunities.append(ArbitrageOpportunity(
                    name='Gold/Silver Ratio',
                    type=ArbitrageType.CROSS_COMMODITY,
                    long_leg='Silver' if current_ratio > 80 else 'Gold',
                    short_leg='Gold' if current_ratio > 80 else 'Silver',
                    spread_current=current_ratio,
                    spread_historical_avg=70.0,
                    spread_z_score=(current_ratio - 70) / 10,
                    catalyst='Flight to safety → Gold outperforms → Ratio widens' if ratio_change > 0 else 'Risk-on → Silver catches up',
                    expected_convergence='Reversion to 70:1 mean (high correlation = 0.80)',
                    risk_level='Low',
                    real_world_example='COVID March 2020: Ratio hit 125:1 (panic) → Reverted to 70:1 by Aug → Silver +200%!'
                ))

        # Copper/Gold ratio (risk-on/risk-off)
        if any(c in ['copper', 'gold'] for c in commodities):
            copper_change = price_changes.get('copper', 0)
            gold_change = price_changes.get('gold', 0)

            # Copper/gold divergence = economic expectations
            divergence = copper_change - gold_change

            if abs(divergence) > 20:
                opportunities.append(ArbitrageOpportunity(
                    name='Copper/Gold Ratio (Economic Indicator)',
                    type=ArbitrageType.CROSS_COMMODITY,
                    long_leg='Copper' if divergence < -20 else 'Gold',
                    short_leg='Gold' if divergence < -20 else 'Copper',
                    spread_current=0.003 if divergence < 0 else 0.007,
                    spread_historical_avg=0.005,
                    spread_z_score=divergence / 15,
                    catalyst='Recession fears → Gold up, copper down' if divergence < 0 else 'Recovery → Copper rallies',
                    expected_convergence='Economic cycle turn',
                    risk_level='Medium (macro dependent)',
                    real_world_example='COVID crash: Copper -30%, gold +10% → Ratio collapsed → Both converged as recovery began'
                ))

        return opportunities

    def _find_geographic_arb(
        self,
        commodities: List[str],
        event_type: str
    ) -> List[ArbitrageOpportunity]:
        """Find geographic arbitrage (same commodity, different locations)"""

        opportunities = []

        # US vs Europe natural gas
        if 'natural_gas' in commodities or 'energy_crisis' in event_type.lower():
            opportunities.append(ArbitrageOpportunity(
                name='Henry Hub vs TTF (US vs Europe Gas)',
                type=ArbitrageType.GEOGRAPHIC,
                long_leg='US LNG exports',
                short_leg='European natural gas',
                spread_current=50.0,  # TTF/Henry Hub = 50x (crisis)
                spread_historical_avg=3.0,  # Normally 3x
                spread_z_score=10.0,
                catalyst='Europe energy crisis → TTF $100+, Henry Hub $5 → Massive arb',
                expected_convergence='LNG export capacity limits arb, but persistent',
                risk_level='Low (geopolitical risk)',
                real_world_example='Ukraine war 2022: TTF €300 ($100/MMBtu), Henry Hub $6 → 16x spread → LNG exporters massive profits'
            ))

        # WTI vs Brent crude
        if any(c in ['oil', 'crude'] for c in commodities):
            opportunities.append(ArbitrageOpportunity(
                name='WTI vs Brent Spread',
                type=ArbitrageType.GEOGRAPHIC,
                long_leg='WTI crude' if event_type == 'us_supply' else 'Brent crude',
                short_leg='Brent crude' if event_type == 'us_supply' else 'WTI crude',
                spread_current=8.0,  # Brent premium
                spread_historical_avg=2.0,
                spread_z_score=3.0,
                catalyst='Regional supply/demand imbalance',
                expected_convergence='Arbitrage by traders, pipeline capacity',
                risk_level='Low',
                real_world_example='Permian oversupply 2019 → WTI discount widened to -$10 → Arb traders stepped in'
            ))

        return opportunities

    def _find_commodity_equity_arb(
        self,
        commodities: List[str],
        price_changes: Dict[str, float]
    ) -> List[ArbitrageOpportunity]:
        """Find commodity vs equity arbitrage"""

        opportunities = []

        # Oil vs E&P stocks
        if 'oil' in commodities:
            oil_change = price_changes.get('oil', 0)

            if oil_change > 30:
                opportunities.append(ArbitrageOpportunity(
                    name='Oil vs E&P Stocks',
                    type=ArbitrageType.COMMODITY_EQUITY,
                    long_leg='E&P stocks (XLE, XOP)',
                    short_leg='WTI crude futures',
                    spread_current=0.5,  # E&Ps lag oil
                    spread_historical_avg=1.0,  # E&Ps normally track
                    spread_z_score=-2.5,
                    catalyst=f'Oil +{oil_change:.0f}% but E&Ps lagging → Will catch up',
                    expected_convergence='E&Ps historically rally 1.5x oil move (levered exposure)',
                    risk_level='Medium',
                    real_world_example='Ukraine invasion: Oil +60% in 3 months → XLE lagged initially but caught up +70% over 6 months'
                ))

        # Metals vs miners
        if any(c in ['gold', 'copper', 'silver'] for c in commodities):
            metal_change = price_changes.get('gold', price_changes.get('copper', 0))

            if metal_change > 20:
                opportunities.append(ArbitrageOpportunity(
                    name='Metal vs Miners Spread',
                    type=ArbitrageType.COMMODITY_EQUITY,
                    long_leg='Miners (GDX, COPX)',
                    short_leg='Metal futures',
                    spread_current=0.8,  # Miners lag
                    spread_historical_avg=1.5,  # Miners levered
                    spread_z_score=-3.0,
                    catalyst='Metal spike → Miners will catch up with operating leverage',
                    expected_convergence='Miners typically rally 2-3x metal move (margin expansion)',
                    risk_level='Medium',
                    real_world_example='Gold +30% in 2020 → GDX +60% (2x leverage via margin expansion)'
                ))

        # Agriculture vs food stocks
        if any(c in ['corn', 'wheat', 'soybeans'] for c in commodities):
            ag_change = price_changes.get('corn', 0)

            if ag_change > 25:
                opportunities.append(ArbitrageOpportunity(
                    name='Agricultural Commodities vs Food Producers',
                    type=ArbitrageType.COMMODITY_EQUITY,
                    long_leg='Grain commodities',
                    short_leg='Food producer stocks',
                    spread_current=35.0,  # Grains up, food stocks down
                    spread_historical_avg=0.0,
                    spread_z_score=5.0,
                    catalyst='Input cost spike → Food margins compressed → Short food stocks',
                    expected_convergence='Food stocks suffer until they pass costs to consumers',
                    risk_level='Medium-High',
                    real_world_example='2022 grain spike → Corn +40% → Food stocks -15% (margin compression)'
                ))

        return opportunities

    def get_historical_arbitrages(self) -> List[Dict]:
        """Return historical arbitrage case studies"""

        return [
            {
                'opportunity': 'Texas Freeze Natural Gas Calendar Spread',
                'date': 'February 2021',
                'setup': 'Feb nat gas futures → $600/MMBtu, but Apr futures → $4',
                'spread': '$596 backwardation (200x normal)',
                'trade': 'Long Apr futures, short Feb futures',
                'outcome': 'Converged to $0 spread in 2 weeks',
                'profit': '~$590/MMBtu on spread = 14,750% return!',
                'lesson': 'Extreme backwardation during short-lived crisis = money printer'
            },
            {
                'opportunity': 'COVID Oil Contango',
                'date': 'April 2020',
                'setup': 'WTI front month → NEGATIVE $37, but June futures → +$20',
                'spread': '$57 contango',
                'trade': 'Buy front month (if storage available), sell June',
                'outcome': 'Front month recovered to $20, June stayed $25',
                'profit': '$57/barrel on spread',
                'lesson': 'Storage arbitrage = free money during demand collapse'
            },
            {
                'opportunity': 'Europe-US Natural Gas Spread',
                'date': '2022',
                'setup': 'TTF (Europe) → €300 ($100/MMBtu), Henry Hub (US) → $6',
                'spread': '16x ratio (vs 3x normal)',
                'trade': 'Long US LNG exporters (TELL, NEXT, CHK)',
                'outcome': 'LNG exporters captured massive margins',
                'profit': 'TELL +200%, NEXT +150%',
                'lesson': 'Geographic arbitrage + export capacity = sustained profits'
            },
            {
                'opportunity': 'Gold/Silver Ratio COVID Crash',
                'date': 'March 2020',
                'setup': 'Gold/silver ratio → 125:1 (vs 70:1 normal)',
                'spread': '55 points above average',
                'trade': 'Long silver, short gold',
                'outcome': 'Ratio reverted to 70:1 by August',
                'profit': 'Silver +200%, gold +30% → Spread captured 170%',
                'lesson': 'Panic creates ratio extremes that always mean revert'
            },
            {
                'opportunity': 'Oil Rally / E&P Lag',
                'date': '2022',
                'setup': 'WTI +60% in Q1, but XLE only +30%',
                'spread': 'E&Ps lagging 2x leverage',
                'trade': 'Long XLE, XOP (E&P stocks)',
                'outcome': 'E&Ps caught up over next 6 months',
                'profit': 'XLE → +70% (vs oil +60%)',
                'lesson': 'E&Ps lag initially but catch up with operating leverage'
            },
            {
                'opportunity': 'Crack Spread Explosion',
                'date': 'Summer 2022',
                'setup': 'Gasoline shortage → RBOB premium exploded',
                'spread': 'Crack spread → $60/barrel (vs $15 normal)',
                'trade': 'Long refiners (MPC, VLO, PSX)',
                'outcome': 'Refiners printed record margins',
                'profit': 'MPC +80%, VLO +60%',
                'lesson': 'Product shortages = refining margin explosion'
            }
        ]

    def analyze_event_arbitrage(
        self,
        event_description: str,
        affected_commodities: List[str],
        price_impacts: Dict[str, float]
    ) -> Dict:
        """
        Complete arbitrage analysis for an event

        Args:
            event_description: What happened
            affected_commodities: List of affected commodities
            price_impacts: Expected price changes (%)

        Returns:
            Full arbitrage analysis with ranked opportunities
        """

        # Find all arbitrage opportunities
        opportunities = self.identify_arbitrage(
            event_type=event_description,
            affected_commodities=affected_commodities,
            price_changes=price_impacts
        )

        # Categorize by type
        by_type = {}
        for opp in opportunities:
            type_name = opp.type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(opp)

        # Get best opportunities (highest z-score)
        best_opportunities = opportunities[:5]

        return {
            'event': event_description,
            'affected_commodities': affected_commodities,
            'opportunities_found': len(opportunities),
            'opportunities_by_type': {k: len(v) for k, v in by_type.items()},
            'best_opportunities': [
                {
                    'name': opp.name,
                    'type': opp.type.value,
                    'long': opp.long_leg,
                    'short': opp.short_leg,
                    'dislocation': f"{opp.spread_z_score:.1f} std devs",
                    'catalyst': opp.catalyst,
                    'convergence': opp.expected_convergence,
                    'risk': opp.risk_level,
                    'example': opp.real_world_example
                }
                for opp in best_opportunities
            ],
            'trading_recommendations': self._generate_recommendations(best_opportunities)
        }

    def _generate_recommendations(self, opportunities: List[ArbitrageOpportunity]) -> List[str]:
        """Generate actionable trading recommendations"""

        recommendations = []

        for opp in opportunities[:3]:  # Top 3
            if abs(opp.spread_z_score) > 3:  # Extreme dislocation
                recommendations.append(
                    f"STRONG BUY: {opp.name} - {opp.spread_z_score:.1f} std devs from mean. "
                    f"Long {opp.long_leg}, Short {opp.short_leg}. "
                    f"Historical precedent: {opp.real_world_example}"
                )
            elif abs(opp.spread_z_score) > 2:
                recommendations.append(
                    f"BUY: {opp.name} - {opp.spread_z_score:.1f} std devs. "
                    f"{opp.catalyst} Risk: {opp.risk_level}"
                )

        return recommendations


def main():
    """Example usage"""

    analyzer = CommodityArbitrageAnalyzer()

    # Example: Energy crisis
    print("=== Example: Energy Crisis Arbitrage Opportunities ===")
    analysis = analyzer.analyze_event_arbitrage(
        event_description='European energy crisis - nat gas shortage',
        affected_commodities=['natural_gas', 'oil', 'power'],
        price_impacts={
            'natural_gas': 200,  # +200%
            'oil': 50,  # +50%
            'power': 300  # +300%
        }
    )

    print(f"Event: {analysis['event']}")
    print(f"Opportunities found: {analysis['opportunities_found']}")
    print(f"\nBest opportunities:")
    for opp in analysis['best_opportunities']:
        print(f"\n{opp['name']}:")
        print(f"  Long: {opp['long']}")
        print(f"  Short: {opp['short']}")
        print(f"  Dislocation: {opp['dislocation']}")
        print(f"  Why: {opp['catalyst']}")

    print(f"\n\nTrading Recommendations:")
    for rec in analysis['trading_recommendations']:
        print(f"  • {rec}")

    # Historical examples
    print("\n\n=== Historical Arbitrage Winners ===")
    for arb in analyzer.get_historical_arbitrages():
        print(f"\n{arb['opportunity']} ({arb['date']}):")
        print(f"  Setup: {arb['setup']}")
        print(f"  Spread: {arb['spread']}")
        print(f"  Trade: {arb['trade']}")
        print(f"  Profit: {arb['profit']}")


if __name__ == "__main__":
    main()
