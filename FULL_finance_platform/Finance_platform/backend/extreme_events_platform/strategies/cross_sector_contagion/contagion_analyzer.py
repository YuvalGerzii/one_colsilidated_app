"""
Cross-Sector Contagion Analyzer (V5.0)

Analyzes how events in one sector cascade to seemingly unrelated sectors.
Maps hidden connections and identifies non-obvious trading opportunities.

Examples of non-obvious contagion:
1. Taiwan drought → TSMC water shortage → Global chip shortage → Auto production halt → Used car prices spike → Consumer spending affected
2. Texas freeze → Natural gas spike → Fertilizer production halt → Agriculture input costs rise → Food inflation → Restaurant margins compress
3. Red Sea shipping disruption → Container rates spike → Retail inventory delays → Earnings warnings → Consumer discretionary stocks fall

The key insight: Modern economy is highly interconnected. Events propagate through:
- Supply chains (physical dependencies)
- Input costs (economic transmission)
- Financial linkages (credit, funding)
- Sentiment (risk-off cascades)
"""

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import networkx as nx  # For dependency graph analysis


class ContagionMechanism(Enum):
    """How contagion spreads"""
    SUPPLY_CHAIN = "supply_chain"
    INPUT_COST = "input_cost"
    DEMAND_SHOCK = "demand_shock"
    CREDIT_LINKAGE = "credit_linkage"
    SENTIMENT = "sentiment"
    REGULATORY = "regulatory"
    TECHNOLOGY = "technology"


@dataclass
class SectorConnection:
    """Connection between two sectors"""
    from_sector: str
    to_sector: str
    mechanism: ContagionMechanism
    strength: float  # 0-1 (how strong the linkage)
    lag_days: int  # How long for contagion to propagate
    amplification: float  # Impact multiplier (can be >1 if amplified)
    example: str


@dataclass
class ContagionPath:
    """Multi-hop contagion path"""
    path: List[str]  # Sequence of sectors
    total_impact: float
    timeframe: str
    probability: float
    trading_opportunity: str


class CrossSectorContagionAnalyzer:
    """
    Analyzes cross-sector contagion and finds hidden connections.

    Uses dependency graph to trace impact propagation.
    """

    def __init__(self):
        """Initialize contagion analyzer"""

        # Build sector dependency graph
        self.dependency_graph = self._build_dependency_graph()

        # Contagion amplifiers (certain connections amplify vs dampen)
        self.amplifiers = {
            ('energy', 'airlines'): 1.4,  # Airlines very sensitive to fuel
            ('semiconductors', 'autos'): 2.0,  # Chip shortage halts production entirely
            ('semiconductors', 'consumer_electronics'): 1.8,
            ('fertilizer', 'agriculture'): 1.6,  # No fertilizer = major yield loss
            ('agriculture', 'food'): 1.3,
            ('shipping', 'retail'): 1.5,  # Just-in-time inventory amplifies
            ('credit', 'real_estate'): 2.5,  # Leverage amplifies credit shocks
        }

    def _build_dependency_graph(self) -> nx.DiGraph:
        """Build directed graph of sector dependencies"""

        G = nx.DiGraph()

        # Add all sector nodes
        sectors = [
            'energy', 'semiconductors', 'autos', 'airlines', 'transportation',
            'retail', 'consumer', 'agriculture', 'food', 'chemicals', 'fertilizer',
            'utilities', 'technology', 'financials', 'real_estate', 'materials',
            'industrials', 'healthcare', 'shipping', 'logistics'
        ]

        G.add_nodes_from(sectors)

        # Add directed edges with attributes (dependency relationships)
        dependencies = [
            # Energy dependencies
            ('energy', 'airlines', {'mechanism': 'input_cost', 'strength': 0.9, 'lag': 0}),
            ('energy', 'transportation', {'mechanism': 'input_cost', 'strength': 0.8, 'lag': 0}),
            ('energy', 'chemicals', {'mechanism': 'input_cost', 'strength': 0.7, 'lag': 3}),
            ('energy', 'utilities', {'mechanism': 'input_cost', 'strength': 0.8, 'lag': 0}),
            ('energy', 'agriculture', {'mechanism': 'input_cost', 'strength': 0.5, 'lag': 7}),

            # Semiconductor dependencies (critical!)
            ('semiconductors', 'autos', {'mechanism': 'supply_chain', 'strength': 0.95, 'lag': 30}),
            ('semiconductors', 'consumer_electronics', {'mechanism': 'supply_chain', 'strength': 0.90, 'lag': 14}),
            ('semiconductors', 'technology', {'mechanism': 'supply_chain', 'strength': 0.75, 'lag': 21}),
            ('semiconductors', 'industrials', {'mechanism': 'supply_chain', 'strength': 0.60, 'lag': 45}),

            # Transportation/Logistics dependencies
            ('transportation', 'retail', {'mechanism': 'supply_chain', 'strength': 0.85, 'lag': 14}),
            ('transportation', 'consumer', {'mechanism': 'input_cost', 'strength': 0.60, 'lag': 30}),
            ('shipping', 'retail', {'mechanism': 'supply_chain', 'strength': 0.80, 'lag': 60}),
            ('shipping', 'manufacturing', {'mechanism': 'supply_chain', 'strength': 0.70, 'lag': 45}),

            # Agriculture/Food dependencies
            ('fertilizer', 'agriculture', {'mechanism': 'input_cost', 'strength': 0.85, 'lag': 60}),
            ('agriculture', 'food', {'mechanism': 'supply_chain', 'strength': 0.90, 'lag': 30}),
            ('food', 'consumer', {'mechanism': 'input_cost', 'strength': 0.70, 'lag': 14}),
            ('food', 'restaurants', {'mechanism': 'input_cost', 'strength': 0.80, 'lag': 7}),

            # Chemical dependencies
            ('chemicals', 'agriculture', {'mechanism': 'supply_chain', 'strength': 0.75, 'lag': 30}),
            ('chemicals', 'manufacturing', {'mechanism': 'supply_chain', 'strength': 0.65, 'lag': 21}),

            # Financial linkages
            ('financials', 'real_estate', {'mechanism': 'credit_linkage', 'strength': 0.90, 'lag': 30}),
            ('financials', 'consumer', {'mechanism': 'credit_linkage', 'strength': 0.70, 'lag': 14}),
            ('financials', 'all_sectors', {'mechanism': 'credit_linkage', 'strength': 0.50, 'lag': 60}),

            # Second-order effects
            ('airlines', 'tourism', {'mechanism': 'demand_shock', 'strength': 0.85, 'lag': 7}),
            ('autos', 'steel', {'mechanism': 'demand_shock', 'strength': 0.70, 'lag': 30}),
            ('real_estate', 'construction', {'mechanism': 'demand_shock', 'strength': 0.80, 'lag': 60}),
        ]

        for from_sec, to_sec, attrs in dependencies:
            G.add_edge(from_sec, to_sec, **attrs)

        return G

    def analyze_contagion(
        self,
        source_sector: str,
        shock_magnitude: float,  # % impact on source sector
        event_description: str
    ) -> Dict:
        """
        Analyze how shock to source sector propagates

        Args:
            source_sector: Where the shock originates
            shock_magnitude: Size of initial shock (%)
            event_description: What happened

        Returns:
            Contagion analysis with multi-hop paths
        """

        # Find all reachable sectors
        reachable = nx.descendants(self.dependency_graph, source_sector)

        # Find contagion paths (up to 4 hops)
        paths = self._find_contagion_paths(source_sector, shock_magnitude, max_hops=4)

        # Identify critical nodes (most connected)
        critical_sectors = self._identify_critical_sectors()

        # Generate trading strategies
        strategies = self._generate_contagion_strategies(paths, shock_magnitude)

        # Calculate timeline
        timeline = self._create_contagion_timeline(paths)

        return {
            'source': {
                'sector': source_sector,
                'shock_magnitude': shock_magnitude,
                'event': event_description
            },
            'affected_sectors': list(reachable),
            'contagion_paths': paths,
            'critical_vulnerabilities': critical_sectors,
            'trading_strategies': strategies,
            'timeline': timeline,
            'hidden_connections': self._find_hidden_connections(paths),
            'systemic_risk_score': self._calculate_systemic_risk(paths, shock_magnitude)
        }

    def _find_contagion_paths(
        self, source: str, magnitude: float, max_hops: int = 4
    ) -> List[ContagionPath]:
        """Find all significant contagion paths"""

        paths = []

        # Use BFS to find paths up to max_hops
        for target in self.dependency_graph.nodes():
            if target == source:
                continue

            try:
                # Find all simple paths (no cycles)
                all_paths = list(nx.all_simple_paths(
                    self.dependency_graph, source, target, cutoff=max_hops
                ))

                for path in all_paths:
                    if len(path) <= max_hops + 1:  # Include source
                        # Calculate impact propagation along path
                        path_impact = self._calculate_path_impact(path, magnitude)

                        if path_impact['total_impact'] > magnitude * 0.05:  # >5% of original
                            paths.append(ContagionPath(
                                path=path,
                                total_impact=path_impact['total_impact'],
                                timeframe=path_impact['timeframe'],
                                probability=path_impact['probability'],
                                trading_opportunity=path_impact['trade']
                            ))
            except nx.NetworkXNoPath:
                continue

        # Sort by impact
        paths.sort(key=lambda x: abs(x.total_impact), reverse=True)

        return paths[:20]  # Top 20 most significant

    def _calculate_path_impact(self, path: List[str], initial_magnitude: float) -> Dict:
        """Calculate impact propagation along a path"""

        current_impact = initial_magnitude
        total_lag = 0
        probability = 1.0

        # Propagate impact along each edge
        for i in range(len(path) - 1):
            from_sec = path[i]
            to_sec = path[i + 1]

            edge_data = self.dependency_graph[from_sec][to_sec]
            strength = edge_data['strength']
            lag = edge_data['lag']

            # Apply amplification if exists
            amplifier = self.amplifiers.get((from_sec, to_sec), 1.0)

            # Impact decays by (1 - strength) but can be amplified
            current_impact = current_impact * strength * amplifier
            total_lag += lag
            probability *= strength  # Probability decreases with each hop

        # Determine timeframe
        if total_lag < 14:
            timeframe = 'Immediate (0-2 weeks)'
        elif total_lag < 60:
            timeframe = f'Short-term ({total_lag//7} weeks)'
        else:
            timeframe = f'Medium-term ({total_lag//30} months)'

        # Generate trade idea
        if current_impact < 0:
            trade = f"Short {path[-1]} sector (expected impact: {current_impact:.1f}%)"
        else:
            trade = f"Long {path[-1]} sector (expected impact: {current_impact:.1f}%)"

        return {
            'total_impact': current_impact,
            'timeframe': timeframe,
            'probability': probability,
            'trade': trade
        }

    def _identify_critical_sectors(self) -> List[Dict]:
        """Identify sectors that are critical nodes in dependency graph"""

        # Calculate centrality measures
        in_degree = dict(self.dependency_graph.in_degree())
        out_degree = dict(self.dependency_graph.out_degree())
        betweenness = nx.betweenness_centrality(self.dependency_graph)

        critical = []
        for sector in self.dependency_graph.nodes():
            score = (
                in_degree.get(sector, 0) * 2 +  # Being depended upon is 2x important
                out_degree.get(sector, 0) +
                betweenness.get(sector, 0) * 10  # Betweenness = bottleneck
            )

            if score > 5:  # Threshold for "critical"
                critical.append({
                    'sector': sector,
                    'criticality_score': score,
                    'dependencies_out': out_degree.get(sector, 0),
                    'dependencies_in': in_degree.get(sector, 0),
                    'rationale': self._explain_criticality(sector, in_degree[sector], out_degree[sector])
                })

        critical.sort(key=lambda x: x['criticality_score'], reverse=True)
        return critical

    def _explain_criticality(self, sector: str, in_deg: int, out_deg: int) -> str:
        """Explain why sector is critical"""

        if sector == 'semiconductors':
            return 'Chips required for all modern electronics. Taiwan concentration = single point of failure.'
        elif sector == 'energy':
            return 'Energy inputs required across all sectors. Oil shocks cause recessions.'
        elif sector == 'shipping':
            return 'Global trade depends on shipping. Disruptions cascade to all imports.'
        elif sector == 'financials':
            return 'Credit system = lifeblood of economy. Bank failures → systemic crisis.'
        else:
            return f'{in_deg} sectors depend on this, affects {out_deg} downstream sectors'

    def _generate_contagion_strategies(self, paths: List[ContagionPath], magnitude: float) -> Dict:
        """Generate trading strategies based on contagion paths"""

        strategies = {
            'immediate_trades': [],
            'anticipatory_trades': [],
            'pairs_trades': [],
            'supply_chain_arbitrage': []
        }

        # Group paths by timeframe
        immediate_paths = [p for p in paths if 'Immediate' in p.timeframe]
        delayed_paths = [p for p in paths if 'Short-term' in p.timeframe or 'Medium-term' in p.timeframe]

        # Immediate trades (already happening)
        for path in immediate_paths[:5]:
            target_sector = path.path[-1]
            strategies['immediate_trades'].append({
                'action': 'Short' if path.total_impact < 0 else 'Long',
                'sector': target_sector,
                'rationale': f"Contagion from {path.path[0]} via {' → '.join(path.path[1:-1])}",
                'expected_impact': f"{path.total_impact:.1f}%",
                'probability': f"{path.probability:.0%}",
                'timeframe': path.timeframe
            })

        # Anticipatory trades (will happen later)
        for path in delayed_paths[:5]:
            target_sector = path.path[-1]
            strategies['anticipatory_trades'].append({
                'action': 'Short' if path.total_impact < 0 else 'Long',
                'sector': target_sector,
                'rationale': f"Future contagion from {path.path[0]}",
                'path_length': f"{len(path.path) - 1} hops",
                'expected_impact': f"{path.total_impact:.1f}%",
                'entry_timing': path.timeframe,
                'edge': 'Most investors won\'t see this connection'
            })

        # Pairs trades (relative value)
        if len(paths) >= 2:
            # Find paths with opposite impacts
            negative_paths = [p for p in paths if p.total_impact < 0]
            positive_paths = [p for p in paths if p.total_impact > 0]

            for neg_path in negative_paths[:3]:
                for pos_path in positive_paths[:3]:
                    strategies['pairs_trades'].append({
                        'long': pos_path.path[-1],
                        'short': neg_path.path[-1],
                        'rationale': f"Contagion creates divergence",
                        'spread_expected': f"{abs(pos_path.total_impact - neg_path.total_impact):.1f}%"
                    })

        return strategies

    def _create_contagion_timeline(self, paths: List[ContagionPath]) -> Dict:
        """Create timeline of when each sector gets affected"""

        timeline = {
            'week_1': [],
            'week_2_4': [],
            'month_2_3': [],
            'month_3_plus': []
        }

        for path in paths:
            target = path.path[-1]

            if 'Immediate' in path.timeframe:
                timeline['week_1'].append({
                    'sector': target,
                    'impact': path.total_impact,
                    'via': ' → '.join(path.path[:-1])
                })
            elif 'week' in path.timeframe.lower():
                timeline['week_2_4'].append({
                    'sector': target,
                    'impact': path.total_impact,
                    'via': ' → '.join(path.path[:-1])
                })
            elif 'month' in path.timeframe.lower():
                if '2' in path.timeframe or '3' in path.timeframe:
                    timeline['month_2_3'].append({
                        'sector': target,
                        'impact': path.total_impact,
                        'via': ' → '.join(path.path[:-1])
                    })
                else:
                    timeline['month_3_plus'].append({
                        'sector': target,
                        'impact': path.total_impact,
                        'via': ' → '.join(path.path[:-1])
                    })

        return timeline

    def _find_hidden_connections(self, paths: List[ContagionPath]) -> List[Dict]:
        """Find non-obvious sector connections"""

        hidden = []

        for path in paths:
            # Hidden = path length >= 3 (at least 2 intermediaries)
            if len(path.path) >= 4:
                hidden.append({
                    'from': path.path[0],
                    'to': path.path[-1],
                    'via': ' → '.join(path.path[1:-1]),
                    'why_hidden': f"{len(path.path) - 2} degrees of separation",
                    'impact': path.total_impact,
                    'timeframe': path.timeframe,
                    'example': self._get_example(path.path)
                })

        return hidden[:10]  # Top 10 most hidden

    def _get_example(self, path: List[str]) -> str:
        """Get real-world example of this contagion path"""

        path_str = ' → '.join(path)

        examples = {
            'energy → fertilizer → agriculture → food → consumer':
                'Europe nat gas spike 2022 → Fertilizer plants shut → Global food crisis → Consumer inflation',

            'semiconductors → autos → steel → materials':
                'Taiwan drought 2021 → TSMC water shortage → Auto production halt → Steel demand collapse',

            'shipping → retail → consumer':
                'Red Sea crisis 2024 → Container delays → Retail stockouts → Consumer spending shift',

            'energy → chemicals → agriculture':
                'Texas freeze 2021 → Nat gas spike → Chemical plants shut → Fertilizer shortage',
        }

        # Try to match path
        for known_path, example in examples.items():
            if all(sector in known_path for sector in path[:3]):
                return example

        return f"Generic {path[0]} disruption cascades through supply chain"

    def _calculate_systemic_risk(self, paths: List[ContagionPath], magnitude: float) -> Dict:
        """Calculate systemic risk score"""

        # Count sectors affected
        affected = set()
        for path in paths:
            affected.update(path.path)

        num_affected = len(affected)
        max_impact = max([abs(p.total_impact) for p in paths]) if paths else 0

        # Systemic risk score (0-100)
        risk_score = min(100, (
            num_affected * 3 +  # More sectors = higher risk
            max_impact * 2 +  # Larger impacts = higher risk
            len(paths) * 0.5  # More paths = more interconnection = higher risk
        ))

        if risk_score > 70:
            level = 'CRITICAL - Widespread contagion'
        elif risk_score > 50:
            level = 'HIGH - Multi-sector impact'
        elif risk_score > 30:
            level = 'MEDIUM - Limited contagion'
        else:
            level = 'LOW - Localized impact'

        return {
            'risk_score': risk_score,
            'risk_level': level,
            'sectors_affected': num_affected,
            'max_secondary_impact': max_impact,
            'contagion_paths': len(paths),
            'recommendation': self._get_risk_recommendation(risk_score)
        }

    def _get_risk_recommendation(self, score: float) -> str:
        """Get recommendation based on risk score"""

        if score > 70:
            return 'HEDGE AGGRESSIVELY: Buy VIX calls, protective puts, raise cash to 25%+'
        elif score > 50:
            return 'INCREASE HEDGES: Add 10-15% hedges, reduce leverage, defensive positioning'
        elif score > 30:
            return 'MONITOR: Watch for cascade, moderate hedging, maintain flexibility'
        else:
            return 'BUSINESS AS USUAL: Localized impact, selective opportunities'
