"""
Supply Chain Disruption Strategy Analyzer (V5.0)

Identifies supply chain vulnerabilities and bottlenecks, then generates
trading strategies to profit from just-in-time inventory failures.

Key insight: Modern supply chains are optimized for efficiency (just-in-time),
not resilience. Single points of failure can cause cascading stockouts.

Real-world examples:
1. Suez Canal blockage (2021) → $10B/day in trade disrupted → Shipping stocks +30%
2. Taiwan chip shortage (2021-2023) → Auto production -20% → Auto stocks -15%, TSMC +50%
3. Red Sea shipping crisis (2024) → Container rates +200% → ZIM, MATX rally
4. Baby formula shortage (2022) → Abbott plant closure → Stockouts nationwide

The opportunity: Identify bottlenecks BEFORE disruptions, then trade the cascade:
- Short sectors dependent on bottleneck
- Long alternative suppliers
- Long logistics/shipping during rerouting
- Long substitutes/competitors
"""

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class BottleneckType(Enum):
    """Types of supply chain bottlenecks"""
    SINGLE_SUPPLIER = "single_supplier"  # One dominant supplier
    CHOKEPOINT = "chokepoint"  # Geographic bottleneck
    JUST_IN_TIME = "just_in_time"  # No inventory buffer
    CRITICAL_INPUT = "critical_input"  # Essential component
    LONG_LEAD_TIME = "long_lead_time"  # Takes months to ramp


class DisruptionSeverity(Enum):
    """Severity levels"""
    MINOR = "minor"  # 1-2 week impact
    MODERATE = "moderate"  # 2-8 week impact
    SEVERE = "severe"  # 2-6 month impact
    CATASTROPHIC = "catastrophic"  # 6+ months


@dataclass
class SupplyChainBottleneck:
    """A vulnerable point in supply chain"""
    name: str
    type: BottleneckType
    sectors_affected: List[str]
    concentration_ratio: float  # % from top supplier
    buffer_days: int  # Days of inventory
    lead_time_days: int  # Days to restore
    alternatives_available: bool
    real_world_example: str


@dataclass
class DisruptionScenario:
    """Disruption scenario and impacts"""
    bottleneck: str
    trigger: str
    probability: float
    severity: DisruptionSeverity
    affected_sectors: List[str]
    timeline: Dict[str, List[str]]
    trading_strategy: Dict


class SupplyChainDisruptionAnalyzer:
    """
    Analyzes supply chain vulnerabilities and generates trading strategies.

    Focus: Just-in-time inventory failures, single points of failure,
    geographic chokepoints, critical input shortages.
    """

    def __init__(self):
        """Initialize supply chain analyzer"""

        # Map critical bottlenecks
        self.bottlenecks = self._map_bottlenecks()

        # Inventory buffer by sector (days)
        self.inventory_buffers = {
            'autos': 30,  # Very lean after Toyota pioneered JIT
            'semiconductors': 90,  # Long lead times
            'retail': 45,  # Seasonal variations
            'aerospace': 180,  # Long-cycle products
            'pharmaceuticals': 90,  # FDA requirements
            'consumer_electronics': 60,  # Fast product cycles
            'industrial': 75,  # Moderate buffers
            'food': 14,  # Perishable = very short
        }

        # Lead times to restore (days)
        self.restoration_times = {
            'semiconductor_fab': 180,  # Takes 6 months to ramp a fab
            'shipping_route': 60,  # Reroute takes 2 months
            'chemical_plant': 90,  # Restart complex
            'mine': 120,  # Mining ramp-up slow
            'port': 30,  # Port congestion clears in 1 month
            'factory': 45,  # Factory restart 1.5 months
        }

    def _map_bottlenecks(self) -> Dict[str, SupplyChainBottleneck]:
        """Map all critical supply chain bottlenecks"""

        return {
            'taiwan_semiconductors': SupplyChainBottleneck(
                name='Taiwan Semiconductor Concentration',
                type=BottleneckType.SINGLE_SUPPLIER,
                sectors_affected=['autos', 'consumer_electronics', 'technology', 'industrials'],
                concentration_ratio=0.92,  # TSMC = 92% of advanced chips
                buffer_days=60,
                lead_time_days=180,  # 6 months to shift production
                alternatives_available=False,  # No alternatives for <5nm
                real_world_example='Taiwan drought 2021 → Global chip shortage → Auto production -20%'
            ),

            'suez_canal': SupplyChainBottleneck(
                name='Suez Canal Chokepoint',
                type=BottleneckType.CHOKEPOINT,
                sectors_affected=['retail', 'manufacturing', 'energy', 'all_trade'],
                concentration_ratio=0.12,  # 12% of global trade
                buffer_days=45,
                lead_time_days=60,  # 2 months to reroute via Cape
                alternatives_available=True,  # Cape of Good Hope (but +2 weeks)
                real_world_example='Ever Given 2021 → $10B/day disrupted → ZIM +30%'
            ),

            'panama_canal': SupplyChainBottleneck(
                name='Panama Canal Chokepoint',
                type=BottleneckType.CHOKEPOINT,
                sectors_affected=['retail', 'manufacturing', 'agriculture', 'lng'],
                concentration_ratio=0.06,  # 6% of global trade
                buffer_days=30,
                lead_time_days=45,
                alternatives_available=True,  # Cape Horn or land routes
                real_world_example='Panama drought 2023 → Ship delays → LNG disruption'
            ),

            'strait_hormuz': SupplyChainBottleneck(
                name='Strait of Hormuz (Oil Chokepoint)',
                type=BottleneckType.CHOKEPOINT,
                sectors_affected=['energy', 'transportation', 'all_sectors'],
                concentration_ratio=0.21,  # 21% of global oil
                buffer_days=90,  # Strategic reserves
                lead_time_days=180,  # Long to reroute Middle East oil
                alternatives_available=True,  # Pipelines, other routes
                real_world_example='Iran tensions 2019 → Oil spike → Energy stocks rally'
            ),

            'rare_earth_china': SupplyChainBottleneck(
                name='China Rare Earth Monopoly',
                type=BottleneckType.SINGLE_SUPPLIER,
                sectors_affected=['technology', 'defense', 'automotive', 'renewables'],
                concentration_ratio=0.70,  # China = 70% of rare earths
                buffer_days=120,
                lead_time_days=365,  # Years to develop alternative mines
                alternatives_available=False,  # No quick alternatives
                real_world_example='China export restrictions 2010 → Rare earth prices +10x'
            ),

            'tsmc_advanced_chips': SupplyChainBottleneck(
                name='TSMC Advanced Process Monopoly',
                type=BottleneckType.SINGLE_SUPPLIER,
                sectors_affected=['smartphones', 'ai', 'datacenter', 'automotive'],
                concentration_ratio=0.92,  # 92% of <7nm chips
                buffer_days=45,
                lead_time_days=730,  # 2 years to build competing fab
                alternatives_available=False,  # Samsung far behind
                real_world_example='Apple, NVIDIA, AMD all depend on TSMC'
            ),

            'asml_euv': SupplyChainBottleneck(
                name='ASML EUV Lithography Monopoly',
                type=BottleneckType.SINGLE_SUPPLIER,
                sectors_affected=['semiconductors'],
                concentration_ratio=1.0,  # 100% monopoly
                buffer_days=180,
                lead_time_days=1095,  # 3+ years to build alternative
                alternatives_available=False,  # No one else can make EUV
                real_world_example='All advanced chip production requires ASML machines'
            ),

            'auto_chips': SupplyChainBottleneck(
                name='Automotive Semiconductor Shortage',
                type=BottleneckType.JUST_IN_TIME,
                sectors_affected=['autos'],
                concentration_ratio=0.60,
                buffer_days=7,  # Autos run VERY lean
                lead_time_days=180,
                alternatives_available=False,  # Custom chips
                real_world_example='2021-2022 chip shortage → Auto production -20% → Used car prices +40%'
            ),

            'container_ships': SupplyChainBottleneck(
                name='Container Shipping Capacity',
                type=BottleneckType.CHOKEPOINT,
                sectors_affected=['retail', 'manufacturing', 'consumer'],
                concentration_ratio=0.30,  # Top 3 alliances = 30%
                buffer_days=60,
                lead_time_days=730,  # 2 years to build ships
                alternatives_available=False,  # Air freight not viable for bulk
                real_world_example='COVID congestion → Container rates +500% → ZIM, MATX +200%'
            ),

            'lithium_batteries': SupplyChainBottleneck(
                name='Lithium Supply Concentration',
                type=BottleneckType.CRITICAL_INPUT,
                sectors_affected=['ev', 'consumer_electronics', 'renewables'],
                concentration_ratio=0.80,  # Top 3 countries = 80%
                buffer_days=90,
                lead_time_days=365,  # New mines take years
                alternatives_available=False,  # No substitute for lithium in batteries
                real_world_example='EV boom → Lithium prices +500% 2021-2022'
            ),
        }

    def analyze_disruption(
        self,
        bottleneck_name: str,
        trigger_event: str,
        estimated_duration_days: int
    ) -> DisruptionScenario:
        """
        Analyze impact of supply chain disruption

        Args:
            bottleneck_name: Which bottleneck is disrupted
            trigger_event: What caused disruption
            estimated_duration_days: Expected duration

        Returns:
            Detailed disruption scenario with trading strategies
        """

        bottleneck = self.bottlenecks.get(bottleneck_name)
        if not bottleneck:
            raise ValueError(f"Unknown bottleneck: {bottleneck_name}")

        # Determine severity
        severity = self._assess_severity(
            bottleneck,
            estimated_duration_days
        )

        # Calculate affected sectors and timing
        impact_timeline = self._create_impact_timeline(
            bottleneck,
            estimated_duration_days
        )

        # Generate trading strategies
        strategies = self._generate_disruption_strategies(
            bottleneck,
            severity,
            estimated_duration_days
        )

        # Estimate probability of severe impact
        probability = self._estimate_probability(bottleneck, severity)

        return DisruptionScenario(
            bottleneck=bottleneck_name,
            trigger=trigger_event,
            probability=probability,
            severity=severity,
            affected_sectors=bottleneck.sectors_affected,
            timeline=impact_timeline,
            trading_strategy=strategies
        )

    def _assess_severity(
        self,
        bottleneck: SupplyChainBottleneck,
        duration: int
    ) -> DisruptionSeverity:
        """Assess disruption severity"""

        # Compare disruption duration to buffer
        buffer_ratio = duration / max(bottleneck.buffer_days, 1)

        # Also consider concentration and alternatives
        severity_score = (
            buffer_ratio * 40 +  # How long vs buffer
            bottleneck.concentration_ratio * 30 +  # Concentration
            (0 if bottleneck.alternatives_available else 30)  # No alternatives
        )

        if severity_score > 80:
            return DisruptionSeverity.CATASTROPHIC
        elif severity_score > 60:
            return DisruptionSeverity.SEVERE
        elif severity_score > 40:
            return DisruptionSeverity.MODERATE
        else:
            return DisruptionSeverity.MINOR

    def _create_impact_timeline(
        self,
        bottleneck: SupplyChainBottleneck,
        duration: int
    ) -> Dict[str, List[str]]:
        """Create timeline of impacts"""

        timeline = {
            'immediate': [],  # 0-2 weeks
            'short_term': [],  # 2-8 weeks
            'medium_term': [],  # 2-6 months
            'long_term': []  # 6+ months
        }

        # Immediate impacts
        timeline['immediate'].extend([
            f"{bottleneck.name} disrupted",
            "Prices spike for alternatives",
            "Panic buying begins",
            "Futures/spot spreads widen"
        ])

        # Short-term (buffer exhaustion)
        if duration > bottleneck.buffer_days:
            timeline['short_term'].extend([
                "Inventory buffers exhausted",
                "Production slowdowns begin",
                "Earnings warnings issued",
                "Stock prices adjust"
            ])

        # Medium-term (secondary effects)
        if duration > bottleneck.buffer_days * 2:
            timeline['medium_term'].extend([
                "Widespread stockouts",
                "Consumer price inflation",
                "Market share shifts",
                "Substitution accelerates"
            ])

        # Long-term (structural changes)
        if duration > bottleneck.lead_time_days:
            timeline['long_term'].extend([
                "Supply chain restructuring",
                "Permanent market share changes",
                "Policy interventions",
                "New suppliers emerge"
            ])

        return timeline

    def _generate_disruption_strategies(
        self,
        bottleneck: SupplyChainBottleneck,
        severity: DisruptionSeverity,
        duration: int
    ) -> Dict:
        """Generate trading strategies for disruption"""

        strategies = {
            'immediate_trades': [],
            'short_trades': [],
            'long_trades': [],
            'pairs_trades': [],
            'commodities': [],
            'options': []
        }

        # Immediate: Long alternatives, short dependents
        strategies['immediate_trades'].extend([
            {
                'action': 'BUY IMMEDIATELY',
                'target': 'Alternative suppliers',
                'rationale': f"{bottleneck.name} disruption → Demand shifts to alternatives",
                'expected_return': '+20-50% if disruption severe',
                'time_horizon': '1-3 months'
            },
            {
                'action': 'BUY IMMEDIATELY',
                'target': 'Logistics/shipping stocks',
                'rationale': 'Rerouting → Higher freight rates → Shipping profits',
                'expected_return': '+30-100% (see ZIM 2021)',
                'time_horizon': '2-6 months'
            }
        ])

        # Short dependent sectors
        for sector in bottleneck.sectors_affected[:3]:
            if duration > self.inventory_buffers.get(sector, 60):
                strategies['short_trades'].append({
                    'action': 'SHORT',
                    'sector': sector,
                    'rationale': f"Buffer exhausted → Production cuts → Earnings miss",
                    'entry_timing': f"When {sector} buffer expires (~{self.inventory_buffers.get(sector, 60)} days)",
                    'expected_return': '-10-30%'
                })

        # Long beneficiaries
        if bottleneck.type == BottleneckType.CHOKEPOINT:
            strategies['long_trades'].append({
                'action': 'LONG',
                'target': 'Shipping/logistics companies',
                'tickers_examples': 'ZIM, MATX, DAC (containers), STNG, FRO (tankers)',
                'rationale': 'Rerouting → Longer distances → Higher rates → Pricing power',
                'expected_return': '+50-200% (historical: ZIM +200% in 2021)',
                'time_horizon': 'Duration of disruption'
            })

        if bottleneck.type == BottleneckType.SINGLE_SUPPLIER:
            strategies['long_trades'].append({
                'action': 'LONG',
                'target': 'The monopoly supplier itself',
                'rationale': 'Shortage → Pricing power → Margin expansion',
                'expected_return': '+20-50%',
                'risk': 'Geopolitical risk if supplier is the problem'
            })

        # Pairs trades (relative value)
        if len(bottleneck.sectors_affected) >= 2:
            strategies['pairs_trades'].append({
                'long': 'Alternative suppliers',
                'short': 'Dependent manufacturers',
                'rationale': 'Shortage benefits suppliers, hurts customers',
                'spread_expected': '30-60%'
            })

        # Commodity plays
        if 'energy' in bottleneck.name.lower() or 'oil' in bottleneck.name.lower():
            strategies['commodities'].append({
                'action': 'LONG',
                'commodity': 'Oil/Natural Gas futures',
                'rationale': 'Supply disruption → Price spike',
                'expected_move': '+30-100% (see Hormuz tensions)',
                'instruments': 'CL futures, USO, XLE'
            })

        if 'chip' in bottleneck.name.lower() or 'semiconductor' in bottleneck.name.lower():
            strategies['long_trades'].append({
                'action': 'LONG',
                'tickers': 'TSM (TSMC), ASML, NVDA, AMD',
                'rationale': 'Chip shortage → Pricing power for chip makers',
                'expected_return': '+30-50%',
                'time_horizon': 'Until new capacity comes online (18-24 months)'
            })

            strategies['short_trades'].append({
                'action': 'SHORT',
                'tickers': 'GM, F, STLA (auto OEMs)',
                'rationale': 'Chip shortage → Production cuts → Revenue miss',
                'expected_return': '-15-30%',
                'timing': 'After inventory buffers exhausted'
            })

        # Options strategies
        if severity in [DisruptionSeverity.SEVERE, DisruptionSeverity.CATASTROPHIC]:
            strategies['options'].extend([
                {
                    'strategy': 'Call spreads on logistics',
                    'rationale': 'Capped upside but high probability',
                    'example': 'ZIM $30/$40 call spread (if disruption confirmed)'
                },
                {
                    'strategy': 'Protective puts on dependents',
                    'rationale': 'Hedge against stockouts',
                    'example': 'SPY puts, XLY puts if consumer affected'
                },
                {
                    'strategy': 'Straddles on commodities',
                    'rationale': 'Uncertainty → Volatility spike',
                    'example': 'USO straddles, /CL straddles'
                }
            ])

        return strategies

    def _estimate_probability(
        self,
        bottleneck: SupplyChainBottleneck,
        severity: DisruptionSeverity
    ) -> float:
        """Estimate probability of severe impact"""

        # Base probability on concentration and alternatives
        base_prob = bottleneck.concentration_ratio

        # Adjust for alternatives
        if not bottleneck.alternatives_available:
            base_prob *= 1.5

        # Adjust for severity
        severity_multipliers = {
            DisruptionSeverity.CATASTROPHIC: 0.9,
            DisruptionSeverity.SEVERE: 0.8,
            DisruptionSeverity.MODERATE: 0.6,
            DisruptionSeverity.MINOR: 0.3
        }

        probability = min(0.95, base_prob * severity_multipliers[severity])
        return probability

    def identify_vulnerabilities(self) -> List[Dict]:
        """
        Identify most vulnerable supply chain points

        Returns ranked list of vulnerabilities
        """

        vulnerabilities = []

        for name, bottleneck in self.bottlenecks.items():
            # Vulnerability score
            score = (
                bottleneck.concentration_ratio * 40 +
                (1 if not bottleneck.alternatives_available else 0) * 30 +
                (100 / max(bottleneck.buffer_days, 1)) * 20 +
                (bottleneck.lead_time_days / 10) * 10
            )

            vulnerabilities.append({
                'name': name,
                'vulnerability_score': score,
                'concentration': f"{bottleneck.concentration_ratio:.0%}",
                'buffer_days': bottleneck.buffer_days,
                'alternatives': 'Yes' if bottleneck.alternatives_available else 'No',
                'sectors_at_risk': bottleneck.sectors_affected,
                'example': bottleneck.real_world_example,
                'recommendation': self._get_vulnerability_recommendation(bottleneck, score)
            })

        # Sort by score
        vulnerabilities.sort(key=lambda x: x['vulnerability_score'], reverse=True)

        return vulnerabilities

    def _get_vulnerability_recommendation(
        self,
        bottleneck: SupplyChainBottleneck,
        score: float
    ) -> str:
        """Get recommendation for vulnerability"""

        if score > 80:
            return f"CRITICAL RISK: Monitor {bottleneck.name} closely. Disruption would be catastrophic. Consider hedges."
        elif score > 60:
            return f"HIGH RISK: {bottleneck.name} failure would cascade. Have playbook ready."
        elif score > 40:
            return f"MODERATE RISK: {bottleneck.name} disruption manageable but watch closely."
        else:
            return f"LOW RISK: {bottleneck.name} has alternatives and buffers."

    def get_historical_disruptions(self) -> List[Dict]:
        """Return historical disruption case studies"""

        return [
            {
                'event': 'Ever Given Suez Canal Blockage',
                'date': 'March 2021',
                'duration': '6 days',
                'impact': '$10B/day in trade blocked',
                'bottleneck': 'suez_canal',
                'outcome': 'ZIM +30%, container rates spiked, but resolved quickly',
                'lesson': 'Even short disruptions to chokepoints have massive impact'
            },
            {
                'event': 'Global Chip Shortage',
                'date': '2021-2023',
                'duration': '2 years',
                'impact': 'Auto production -20%, electronics delayed',
                'bottleneck': 'taiwan_semiconductors',
                'outcome': 'TSMC +50%, auto stocks -15%, used car prices +40%',
                'lesson': 'Just-in-time + single supplier = catastrophic when broken'
            },
            {
                'event': 'COVID Container Shortage',
                'date': '2020-2022',
                'duration': '2 years',
                'impact': 'Container rates +500%',
                'bottleneck': 'container_ships',
                'outcome': 'ZIM +500%, MATX +300%, retail stockouts',
                'lesson': 'Capacity constraints + demand surge = explosive rates'
            },
            {
                'event': 'Texas Freeze Fertilizer Shortage',
                'date': 'February 2021',
                'duration': '3 months',
                'impact': 'Fertilizer production -50%',
                'bottleneck': 'Natural gas → Fertilizer plants',
                'outcome': 'Agriculture input costs +40%, food inflation',
                'lesson': 'Energy shocks cascade through chemicals to agriculture'
            },
            {
                'event': 'Red Sea Shipping Crisis',
                'date': '2024',
                'duration': 'Ongoing',
                'impact': 'Container rates +200%, rerouting via Cape',
                'bottleneck': 'suez_canal (alternative to Red Sea)',
                'outcome': 'ZIM, MATX rally, retail inventory delays',
                'lesson': 'Geopolitical risk to chokepoints is persistent'
            }
        ]


def main():
    """Example usage"""

    analyzer = SupplyChainDisruptionAnalyzer()

    # Example 1: Analyze Taiwan chip disruption
    print("=== Example 1: Taiwan Chip Disruption ===")
    scenario = analyzer.analyze_disruption(
        bottleneck_name='taiwan_semiconductors',
        trigger_event='Taiwan drought reduces TSMC output by 30%',
        estimated_duration_days=180
    )

    print(f"Bottleneck: {scenario.bottleneck}")
    print(f"Severity: {scenario.severity.value}")
    print(f"Probability: {scenario.probability:.0%}")
    print(f"\nAffected sectors: {', '.join(scenario.affected_sectors)}")
    print(f"\nTrading strategies:")
    for strategy in scenario.trading_strategy.get('long_trades', []):
        print(f"  - {strategy['action']}: {strategy.get('tickers', strategy.get('target'))}")
        print(f"    {strategy['rationale']}")

    # Example 2: Identify vulnerabilities
    print("\n\n=== Top 5 Supply Chain Vulnerabilities ===")
    vulnerabilities = analyzer.identify_vulnerabilities()
    for vuln in vulnerabilities[:5]:
        print(f"\n{vuln['name']}:")
        print(f"  Vulnerability Score: {vuln['vulnerability_score']:.1f}")
        print(f"  Concentration: {vuln['concentration']}")
        print(f"  Buffer: {vuln['buffer_days']} days")
        print(f"  Alternatives: {vuln['alternatives']}")
        print(f"  Recommendation: {vuln['recommendation']}")


if __name__ == "__main__":
    main()
