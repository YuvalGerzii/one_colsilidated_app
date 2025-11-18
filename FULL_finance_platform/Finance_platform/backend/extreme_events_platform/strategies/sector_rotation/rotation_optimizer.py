"""
Advanced Sector Rotation Optimizer (V5.0)

Optimizes sector allocation during extreme events using contagion analysis,
historical patterns, and cross-sector impact modeling.

Key insight: Extreme events create predictable sector rotation patterns.
Winners and losers emerge based on:
1. Direct exposure (energy crisis → energy stocks up)
2. Input cost sensitivity (energy crisis → airlines down)
3. Contagion paths (chip shortage → autos down → steel down)
4. Flight to quality (recession → staples/utilities up, discretionary down)

Real-world examples:
1. COVID crash 2020 → Tech +60%, Energy -40%, Travel -60% → Rotate to tech early = alpha
2. Inflation 2021-2022 → Energy +60%, Tech -30% → Commodities outperformed
3. Banking crisis 2023 → Financials -20%, Defensive +10% → Flight to quality
4. Ukraine invasion 2022 → Defense +30%, Energy +40%, Europe -20%

The opportunity: Use contagion analysis + historical patterns to:
- Overweight beneficiaries BEFORE the crowd
- Underweight/short victims BEFORE stockouts hit
- Rotate back at inflection points
"""

from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np


class EventCategory(Enum):
    """Event categories with different rotation patterns"""
    RECESSION = "recession"
    INFLATION = "inflation"
    ENERGY_CRISIS = "energy_crisis"
    SUPPLY_SHOCK = "supply_shock"
    FINANCIAL_CRISIS = "financial_crisis"
    GEOPOLITICAL = "geopolitical"
    PANDEMIC = "pandemic"
    TECH_DISRUPTION = "tech_disruption"


class RotationPhase(Enum):
    """Phases of sector rotation during event"""
    PANIC = "panic"  # Initial reaction
    CONTAGION = "contagion"  # Secondary effects spread
    ADAPTATION = "adaptation"  # Economy adjusts
    RECOVERY = "recovery"  # Return to normal


@dataclass
class SectorAllocation:
    """Recommended sector allocation"""
    sector: str
    target_weight: float  # % of portfolio
    rationale: str
    conviction: str  # High/Medium/Low
    time_horizon: str
    expected_alpha: float  # % outperformance vs market


@dataclass
class RotationStrategy:
    """Complete rotation strategy"""
    event_type: EventCategory
    phase: RotationPhase
    allocations: List[SectorAllocation]
    overweights: List[str]
    underweights: List[str]
    hedges: List[str]
    expected_sharpe: float


class SectorRotationOptimizer:
    """
    Optimizes sector allocation during extreme events.

    Uses historical patterns + contagion analysis to generate
    optimal sector weights.
    """

    def __init__(self):
        """Initialize sector rotation optimizer"""

        # Historical sector performance by event type (%)
        self.event_performance_patterns = self._load_historical_patterns()

        # Sector characteristics
        self.sector_characteristics = self._define_sector_characteristics()

        # Rotation timing (how long each phase lasts)
        self.phase_duration = {
            RotationPhase.PANIC: 14,  # 2 weeks
            RotationPhase.CONTAGION: 60,  # 2 months
            RotationPhase.ADAPTATION: 120,  # 4 months
            RotationPhase.RECOVERY: 180,  # 6 months
        }

    def _load_historical_patterns(self) -> Dict[EventCategory, Dict[str, float]]:
        """Load historical sector performance patterns"""

        return {
            EventCategory.RECESSION: {
                # Defensive outperform
                'consumer_staples': +5,  # Relative to market
                'utilities': +8,
                'healthcare': +6,
                'telecom': +4,
                # Cyclicals underperform
                'consumer_discretionary': -15,
                'industrials': -12,
                'materials': -10,
                'financials': -18,
                'energy': -8,
                # Tech depends on type
                'technology': -5,
                'real_estate': -12,
            },

            EventCategory.INFLATION: {
                # Real assets outperform
                'energy': +25,
                'materials': +15,
                'real_estate': +10,
                'industrials': +8,
                # Long duration underperform
                'technology': -12,
                'consumer_discretionary': -10,
                'utilities': -8,
                'financials': +5,  # If rates rising
                # Staples mixed
                'consumer_staples': 0,
                'healthcare': -3,
                'telecom': -5,
            },

            EventCategory.ENERGY_CRISIS: {
                # Energy obvious winner
                'energy': +40,
                # High energy cost = losers
                'airlines': -25,
                'transportation': -15,
                'chemicals': -10,
                'consumer_discretionary': -12,
                # Utilities benefit from higher power prices
                'utilities': +15,
                # Others relatively neutral
                'technology': -5,
                'healthcare': 0,
                'financials': -3,
                'consumer_staples': -5,
                'materials': +5,
            },

            EventCategory.SUPPLY_SHOCK: {
                # Depends on what's in shortage
                # Semiconductors example
                'semiconductors': +30,  # Pricing power
                'software': +10,  # Less affected
                'autos': -20,  # Production cuts
                'consumer_electronics': -15,
                'industrials': -10,
                # Beneficiaries
                'alternatives': +20,  # Alternative suppliers
                'logistics': +25,  # Rerouting demand
            },

            EventCategory.FINANCIAL_CRISIS: {
                # Flight to quality
                'consumer_staples': +12,
                'healthcare': +10,
                'utilities': +15,
                'technology': 0,  # Depends on fundamentals
                # Hardest hit
                'financials': -30,
                'real_estate': -25,
                'consumer_discretionary': -20,
                'industrials': -15,
                'materials': -12,
                'energy': -10,
            },

            EventCategory.GEOPOLITICAL: {
                # Defense and commodities
                'defense': +30,
                'energy': +25,
                'materials': +10,
                'gold': +15,
                # Cyclicals suffer
                'consumer_discretionary': -10,
                'technology': -8,
                'industrials': -5,
                # Defensive hold up
                'consumer_staples': +5,
                'utilities': +3,
                'healthcare': +5,
            },

            EventCategory.PANDEMIC: {
                # COVID example
                'technology': +40,  # WFH beneficiaries
                'healthcare': +20,  # Vaccines, treatments
                'consumer_staples': +8,  # Essential
                'ecommerce': +50,
                # Devastated
                'travel': -60,
                'hospitality': -50,
                'energy': -40,
                'financials': -20,
                'real_estate': -15,
                'consumer_discretionary': -25,
            },

            EventCategory.TECH_DISRUPTION: {
                # AI boom example
                'ai_chips': +60,  # NVDA
                'cloud': +30,
                'software': +20,
                # Disrupted
                'legacy_tech': -15,
                'traditional_media': -20,
                # Indirect beneficiaries
                'utilities': +10,  # Power for datacenters
                'real_estate': +5,  # Datacenter REITs
            }
        }

    def _define_sector_characteristics(self) -> Dict[str, Dict]:
        """Define sector characteristics for analysis"""

        return {
            'energy': {
                'beta': 1.2,
                'cyclicality': 'high',
                'defensive': False,
                'input_sensitivity': {'oil': 0.9, 'natural_gas': 0.8},
                'typical_pe': 12,
                'dividend_yield': 0.04
            },
            'technology': {
                'beta': 1.3,
                'cyclicality': 'medium',
                'defensive': False,
                'input_sensitivity': {'semiconductors': 0.7},
                'typical_pe': 25,
                'dividend_yield': 0.01
            },
            'consumer_staples': {
                'beta': 0.7,
                'cyclicality': 'low',
                'defensive': True,
                'input_sensitivity': {'commodities': 0.4},
                'typical_pe': 20,
                'dividend_yield': 0.03
            },
            'consumer_discretionary': {
                'beta': 1.4,
                'cyclicality': 'high',
                'defensive': False,
                'input_sensitivity': {'consumer_confidence': 0.8},
                'typical_pe': 22,
                'dividend_yield': 0.015
            },
            'financials': {
                'beta': 1.15,
                'cyclicality': 'high',
                'defensive': False,
                'input_sensitivity': {'interest_rates': 0.7, 'credit': 0.9},
                'typical_pe': 12,
                'dividend_yield': 0.03
            },
            'healthcare': {
                'beta': 0.85,
                'cyclicality': 'low',
                'defensive': True,
                'input_sensitivity': {},
                'typical_pe': 18,
                'dividend_yield': 0.02
            },
            'utilities': {
                'beta': 0.6,
                'cyclicality': 'low',
                'defensive': True,
                'input_sensitivity': {'interest_rates': -0.5},  # Inverse
                'typical_pe': 16,
                'dividend_yield': 0.04
            },
            'industrials': {
                'beta': 1.1,
                'cyclicality': 'high',
                'defensive': False,
                'input_sensitivity': {'gdp': 0.8},
                'typical_pe': 18,
                'dividend_yield': 0.02
            },
            'materials': {
                'beta': 1.15,
                'cyclicality': 'high',
                'defensive': False,
                'input_sensitivity': {'commodities': 0.9},
                'typical_pe': 14,
                'dividend_yield': 0.025
            },
            'real_estate': {
                'beta': 0.9,
                'cyclicality': 'medium',
                'defensive': False,
                'input_sensitivity': {'interest_rates': -0.7},  # Inverse
                'typical_pe': 40,  # FFO multiple
                'dividend_yield': 0.04
            }
        }

    def optimize_allocation(
        self,
        event_type: EventCategory,
        phase: RotationPhase,
        conviction: float = 1.0,  # 0-1 confidence in event
        contagion_data: Dict = None  # From contagion analyzer
    ) -> RotationStrategy:
        """
        Optimize sector allocation for event

        Args:
            event_type: Type of event
            phase: Current phase of event
            conviction: Confidence in event thesis (0-1)
            contagion_data: Optional contagion analysis data

        Returns:
            Optimal rotation strategy
        """

        # Get base performance pattern
        base_pattern = self.event_performance_patterns.get(event_type, {})

        # Adjust for phase (panic = more extreme, recovery = reversion)
        phase_multiplier = self._get_phase_multiplier(phase)

        # Calculate sector scores
        sector_scores = {}
        for sector, base_alpha in base_pattern.items():
            # Apply phase adjustment
            adjusted_alpha = base_alpha * phase_multiplier * conviction

            # Apply contagion adjustments if available
            if contagion_data:
                contagion_adjustment = self._get_contagion_adjustment(
                    sector, contagion_data
                )
                adjusted_alpha += contagion_adjustment

            sector_scores[sector] = adjusted_alpha

        # Generate allocations
        allocations = self._generate_allocations(sector_scores, phase)

        # Identify overweights/underweights
        overweights = [s for s, score in sector_scores.items() if score > 10]
        underweights = [s for s, score in sector_scores.items() if score < -10]

        # Recommend hedges
        hedges = self._recommend_hedges(event_type, phase, sector_scores)

        # Estimate Sharpe ratio
        expected_sharpe = self._estimate_sharpe(sector_scores, phase)

        return RotationStrategy(
            event_type=event_type,
            phase=phase,
            allocations=allocations,
            overweights=overweights,
            underweights=underweights,
            hedges=hedges,
            expected_sharpe=expected_sharpe
        )

    def _get_phase_multiplier(self, phase: RotationPhase) -> float:
        """Get multiplier for rotation based on phase"""

        multipliers = {
            RotationPhase.PANIC: 1.5,  # Exaggerated moves
            RotationPhase.CONTAGION: 1.2,  # Still strong
            RotationPhase.ADAPTATION: 0.8,  # Mean reversion begins
            RotationPhase.RECOVERY: 0.3,  # Mostly reversed
        }

        return multipliers[phase]

    def _get_contagion_adjustment(
        self,
        sector: str,
        contagion_data: Dict
    ) -> float:
        """Adjust sector score based on contagion analysis"""

        # Look for sector in contagion paths
        affected = contagion_data.get('affected_sectors', [])

        if sector in affected:
            # Find impact magnitude
            for path in contagion_data.get('contagion_paths', []):
                if path.path[-1] == sector:
                    # Negative impact → Underweight more
                    # Positive impact → Overweight more
                    return path.total_impact

        return 0.0

    def _generate_allocations(
        self,
        sector_scores: Dict[str, float],
        phase: RotationPhase
    ) -> List[SectorAllocation]:
        """Generate target allocations from scores"""

        allocations = []

        # Normalize scores to weights (start with equal weight = 10%)
        base_weight = 10.0
        total_sectors = len(sector_scores)

        for sector, score in sorted(sector_scores.items(), key=lambda x: x[1], reverse=True):
            # Adjust weight based on score
            # Score of +20 → 2x weight = 20%
            # Score of -20 → 0.5x weight = 5%
            weight_multiplier = 1.0 + (score / 100)
            target_weight = base_weight * weight_multiplier

            # Ensure weights are reasonable (0-30%)
            target_weight = max(0, min(30, target_weight))

            # Determine conviction
            if abs(score) > 20:
                conviction = 'High'
            elif abs(score) > 10:
                conviction = 'Medium'
            else:
                conviction = 'Low'

            allocations.append(SectorAllocation(
                sector=sector,
                target_weight=target_weight,
                rationale=self._get_allocation_rationale(sector, score, phase),
                conviction=conviction,
                time_horizon=f"{self.phase_duration[phase]} days",
                expected_alpha=score
            ))

        # Normalize to 100%
        total_weight = sum(a.target_weight for a in allocations)
        if total_weight > 0:
            for allocation in allocations:
                allocation.target_weight = (allocation.target_weight / total_weight) * 100

        return allocations

    def _get_allocation_rationale(
        self,
        sector: str,
        score: float,
        phase: RotationPhase
    ) -> str:
        """Generate rationale for allocation"""

        if score > 20:
            return f"{sector.title()} major beneficiary - historical +{score:.0f}% alpha"
        elif score > 10:
            return f"{sector.title()} outperforms - defensive characteristics"
        elif score > -10:
            return f"{sector.title()} neutral - market weight appropriate"
        elif score > -20:
            return f"{sector.title()} underperforms - reduce exposure"
        else:
            return f"{sector.title()} major victim - consider shorting"

    def _recommend_hedges(
        self,
        event_type: EventCategory,
        phase: RotationPhase,
        sector_scores: Dict[str, float]
    ) -> List[str]:
        """Recommend hedging strategies"""

        hedges = []

        # Always hedge in panic phase
        if phase == RotationPhase.PANIC:
            hedges.append('VIX calls (volatility spike protection)')
            hedges.append('SPY puts 5-10% OTM (tail risk hedge)')

        # Event-specific hedges
        if event_type == EventCategory.ENERGY_CRISIS:
            hedges.append('Long USO calls (oil spike hedge)')
            hedges.append('Short XLE (if overextended)')

        elif event_type == EventCategory.FINANCIAL_CRISIS:
            hedges.append('Long TLT (flight to treasuries)')
            hedges.append('Short XLF (financials pressure)')
            hedges.append('Long GLD (safe haven)')

        elif event_type == EventCategory.INFLATION:
            hedges.append('Long TIP (inflation-protected bonds)')
            hedges.append('Long GLD/SLV (inflation hedge)')
            hedges.append('Long DBA (agriculture commodities)')

        elif event_type == EventCategory.RECESSION:
            hedges.append('Long XLP (consumer staples defense)')
            hedges.append('Long XLU (utilities defense)')
            hedges.append('Short XLY (discretionary weakness)')

        # Sector-specific hedges
        worst_sectors = [s for s, score in sector_scores.items() if score < -15]
        if worst_sectors:
            hedges.append(f"Short {', '.join(worst_sectors[:3])} (most exposed)")

        return hedges

    def _estimate_sharpe(
        self,
        sector_scores: Dict[str, float],
        phase: RotationPhase
    ) -> float:
        """Estimate expected Sharpe ratio of strategy"""

        # Calculate expected return
        expected_return = np.mean(list(sector_scores.values()))

        # Estimate volatility (higher in panic, lower in recovery)
        phase_vol = {
            RotationPhase.PANIC: 30,  # High vol
            RotationPhase.CONTAGION: 25,
            RotationPhase.ADAPTATION: 20,
            RotationPhase.RECOVERY: 18,
        }

        volatility = phase_vol[phase]

        # Sharpe = (Return - RiskFree) / Vol
        # Assume risk-free = 4%
        sharpe = (expected_return - 4) / volatility

        return max(0, sharpe)  # Can't be negative

    def get_rotation_playbook(self, event_type: EventCategory) -> Dict:
        """
        Get complete rotation playbook for event type

        Returns playbook with all phases
        """

        playbook = {
            'event': event_type.value,
            'phases': {}
        }

        for phase in RotationPhase:
            strategy = self.optimize_allocation(event_type, phase, conviction=1.0)

            playbook['phases'][phase.value] = {
                'duration': f"{self.phase_duration[phase]} days",
                'top_sectors': strategy.overweights[:3],
                'worst_sectors': strategy.underweights[:3],
                'hedges': strategy.hedges,
                'expected_sharpe': strategy.expected_sharpe,
                'key_trades': [
                    f"Overweight {sector}" for sector in strategy.overweights[:3]
                ] + [
                    f"Underweight {sector}" for sector in strategy.underweights[:3]
                ]
            }

        return playbook

    def compare_strategies(
        self,
        events: List[EventCategory]
    ) -> Dict[str, List[str]]:
        """
        Compare sector winners across different event types

        Useful for identifying diversification and common themes
        """

        comparison = {
            'always_winners': [],  # Win in all scenarios
            'always_losers': [],  # Lose in all scenarios
            'recession_plays': [],
            'inflation_plays': [],
            'crisis_plays': []
        }

        # Collect sector performance across events
        sector_performance = {}

        for event in events:
            pattern = self.event_performance_patterns.get(event, {})
            for sector, alpha in pattern.items():
                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append((event, alpha))

        # Analyze
        for sector, performances in sector_performance.items():
            alphas = [p[1] for p in performances]

            if all(a > 10 for a in alphas):
                comparison['always_winners'].append(sector)
            elif all(a < -10 for a in alphas):
                comparison['always_losers'].append(sector)

        # Event-specific plays
        recession_pattern = self.event_performance_patterns.get(EventCategory.RECESSION, {})
        comparison['recession_plays'] = [s for s, a in recession_pattern.items() if a > 10]

        inflation_pattern = self.event_performance_patterns.get(EventCategory.INFLATION, {})
        comparison['inflation_plays'] = [s for s, a in inflation_pattern.items() if a > 10]

        return comparison

    def backtest_rotation(
        self,
        event_type: EventCategory,
        actual_returns: Dict[str, float],
        phase: RotationPhase
    ) -> Dict:
        """
        Backtest rotation strategy against actual returns

        Args:
            event_type: Event that occurred
            actual_returns: Actual sector returns (%)
            phase: Phase during backtest period

        Returns:
            Backtest results
        """

        # Get recommended strategy
        strategy = self.optimize_allocation(event_type, phase, conviction=1.0)

        # Calculate portfolio return
        portfolio_return = 0.0
        for allocation in strategy.allocations:
            sector = allocation.sector
            weight = allocation.target_weight / 100
            actual_return = actual_returns.get(sector, 0)
            portfolio_return += weight * actual_return

        # Calculate benchmark return (equal weight)
        benchmark_return = np.mean(list(actual_returns.values()))

        # Calculate alpha
        alpha = portfolio_return - benchmark_return

        # Identify best and worst calls
        best_calls = []
        worst_calls = []

        for allocation in strategy.allocations:
            sector = allocation.sector
            expected = allocation.expected_alpha
            actual = actual_returns.get(sector, 0)
            error = actual - expected

            if error > 10:
                best_calls.append(f"{sector}: Expected {expected:.0f}%, got {actual:.0f}%")
            elif error < -10:
                worst_calls.append(f"{sector}: Expected {expected:.0f}%, got {actual:.0f}%")

        return {
            'portfolio_return': portfolio_return,
            'benchmark_return': benchmark_return,
            'alpha': alpha,
            'best_calls': best_calls[:3],
            'worst_calls': worst_calls[:3],
            'hit_rate': len(best_calls) / max(len(strategy.allocations), 1)
        }


def main():
    """Example usage"""

    optimizer = SectorRotationOptimizer()

    # Example 1: Energy crisis rotation
    print("=== Example 1: Energy Crisis Rotation ===")
    strategy = optimizer.optimize_allocation(
        event_type=EventCategory.ENERGY_CRISIS,
        phase=RotationPhase.CONTAGION,
        conviction=0.9
    )

    print(f"Event: {strategy.event_type.value}")
    print(f"Phase: {strategy.phase.value}")
    print(f"Expected Sharpe: {strategy.expected_sharpe:.2f}")
    print(f"\nOverweight: {', '.join(strategy.overweights)}")
    print(f"Underweight: {', '.join(strategy.underweights)}")
    print(f"\nTop allocations:")
    for alloc in strategy.allocations[:5]:
        print(f"  {alloc.sector}: {alloc.target_weight:.1f}% ({alloc.conviction} conviction)")
        print(f"    {alloc.rationale}")

    print(f"\nHedges:")
    for hedge in strategy.hedges:
        print(f"  - {hedge}")

    # Example 2: Get full playbook for recession
    print("\n\n=== Example 2: Recession Playbook ===")
    playbook = optimizer.get_rotation_playbook(EventCategory.RECESSION)

    print(f"Event: {playbook['event']}")
    for phase_name, phase_data in playbook['phases'].items():
        print(f"\n{phase_name.upper()} ({phase_data['duration']}):")
        print(f"  Top sectors: {', '.join(phase_data['top_sectors'])}")
        print(f"  Worst sectors: {', '.join(phase_data['worst_sectors'])}")
        print(f"  Expected Sharpe: {phase_data['expected_sharpe']:.2f}")

    # Example 3: Compare strategies
    print("\n\n=== Example 3: Strategy Comparison ===")
    comparison = optimizer.compare_strategies([
        EventCategory.RECESSION,
        EventCategory.INFLATION,
        EventCategory.FINANCIAL_CRISIS
    ])

    print(f"Recession plays: {', '.join(comparison['recession_plays'])}")
    print(f"Inflation plays: {', '.join(comparison['inflation_plays'])}")


if __name__ == "__main__":
    main()
