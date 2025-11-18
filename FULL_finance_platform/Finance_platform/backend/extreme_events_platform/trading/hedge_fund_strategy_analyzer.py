"""
Hedge Fund Strategy Analyzer (V4.0)

Analyzes which hedge fund strategies perform best during extreme events.
Based on 2025 market intelligence:
- Macro funds: +11.2% YTD during volatility
- Event-driven: +8.7% during deal activity
- Convertible arbitrage: +4.0% from volatility capture
- Statistical arbitrage and quant strategies
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class HedgeFundStrategy(Enum):
    """Hedge fund strategy types"""
    GLOBAL_MACRO = "global_macro"
    EVENT_DRIVEN = "event_driven"
    CONVERTIBLE_ARBITRAGE = "convertible_arbitrage"
    LONG_SHORT_EQUITY = "long_short_equity"
    STATISTICAL_ARBITRAGE = "statistical_arbitrage"
    MERGER_ARBITRAGE = "merger_arbitrage"
    VOLATILITY_ARBITRAGE = "volatility_arbitrage"
    DISTRESSED_DEBT = "distressed_debt"
    MULTI_STRATEGY = "multi_strategy"
    CTA_TREND_FOLLOWING = "cta_trend_following"
    MARKET_NEUTRAL = "market_neutral"
    FIXED_INCOME_ARBITRAGE = "fixed_income_arbitrage"


@dataclass
class StrategyRecommendation:
    """Recommendation for a specific hedge fund strategy"""
    strategy: HedgeFundStrategy
    suitability_score: float  # 0-100
    expected_alpha: float  # Expected outperformance vs market
    risk_level: str  # low, medium, high
    time_horizon: str  # short (days), medium (weeks), long (months)
    rationale: str
    key_positions: List[str]
    risk_factors: List[str]
    historical_performance: str  # How this strategy performed in similar events


@dataclass
class StrategyAllocation:
    """Portfolio allocation across strategies"""
    strategy: HedgeFundStrategy
    allocation_pct: float
    position_sizing: str
    entry_timing: str
    exit_criteria: List[str]


class HedgeFundStrategyAnalyzer:
    """
    Analyzes which hedge fund strategies work best for each extreme event type.
    Based on 2025 market data and hedge fund performance patterns.
    """

    def __init__(self):
        """Initialize strategy analyzer with 2025 performance data"""

        # Strategy performance by event type (based on historical data)
        self.strategy_performance_matrix = {
            'recession': {
                HedgeFundStrategy.GLOBAL_MACRO: 85,  # High score = good fit
                HedgeFundStrategy.DISTRESSED_DEBT: 90,
                HedgeFundStrategy.MARKET_NEUTRAL: 75,
                HedgeFundStrategy.CTA_TREND_FOLLOWING: 80,
                HedgeFundStrategy.LONG_SHORT_EQUITY: 60,
                HedgeFundStrategy.EVENT_DRIVEN: 40,
            },
            'inflation': {
                HedgeFundStrategy.GLOBAL_MACRO: 90,
                HedgeFundStrategy.CTA_TREND_FOLLOWING: 85,
                HedgeFundStrategy.VOLATILITY_ARBITRAGE: 70,
                HedgeFundStrategy.LONG_SHORT_EQUITY: 65,
                HedgeFundStrategy.CONVERTIBLE_ARBITRAGE: 55,
            },
            'interest_rate_change': {
                HedgeFundStrategy.FIXED_INCOME_ARBITRAGE: 85,
                HedgeFundStrategy.GLOBAL_MACRO: 80,
                HedgeFundStrategy.CONVERTIBLE_ARBITRAGE: 75,
                HedgeFundStrategy.VOLATILITY_ARBITRAGE: 70,
            },
            'market_crash': {
                HedgeFundStrategy.VOLATILITY_ARBITRAGE: 95,
                HedgeFundStrategy.MARKET_NEUTRAL: 85,
                HedgeFundStrategy.GLOBAL_MACRO: 80,
                HedgeFundStrategy.CTA_TREND_FOLLOWING: 75,
                HedgeFundStrategy.DISTRESSED_DEBT: 70,
            },
            'geopolitical': {
                HedgeFundStrategy.GLOBAL_MACRO: 90,
                HedgeFundStrategy.CTA_TREND_FOLLOWING: 85,
                HedgeFundStrategy.EVENT_DRIVEN: 75,
                HedgeFundStrategy.LONG_SHORT_EQUITY: 70,
            },
            'pandemic': {
                HedgeFundStrategy.LONG_SHORT_EQUITY: 80,
                HedgeFundStrategy.EVENT_DRIVEN: 75,
                HedgeFundStrategy.GLOBAL_MACRO: 70,
                HedgeFundStrategy.DISTRESSED_DEBT: 65,
            },
            'cyber_attack': {
                HedgeFundStrategy.EVENT_DRIVEN: 85,
                HedgeFundStrategy.LONG_SHORT_EQUITY: 80,
                HedgeFundStrategy.MULTI_STRATEGY: 75,
            },
            'economic_crisis': {
                HedgeFundStrategy.DISTRESSED_DEBT: 95,
                HedgeFundStrategy.GLOBAL_MACRO: 85,
                HedgeFundStrategy.EVENT_DRIVEN: 80,
                HedgeFundStrategy.MARKET_NEUTRAL: 75,
            }
        }

        # 2025 baseline performance data
        self.baseline_alpha = {
            HedgeFundStrategy.GLOBAL_MACRO: 11.2,  # 2025 YTD
            HedgeFundStrategy.EVENT_DRIVEN: 8.7,
            HedgeFundStrategy.CONVERTIBLE_ARBITRAGE: 4.0,
            HedgeFundStrategy.STATISTICAL_ARBITRAGE: 7.5,
            HedgeFundStrategy.LONG_SHORT_EQUITY: 6.5,
            HedgeFundStrategy.VOLATILITY_ARBITRAGE: 9.0,
            HedgeFundStrategy.DISTRESSED_DEBT: 8.0,
            HedgeFundStrategy.MULTI_STRATEGY: 6.8,
            HedgeFundStrategy.CTA_TREND_FOLLOWING: 7.2,
            HedgeFundStrategy.MARKET_NEUTRAL: 5.5,
            HedgeFundStrategy.MERGER_ARBITRAGE: 6.0,
            HedgeFundStrategy.FIXED_INCOME_ARBITRAGE: 5.0,
        }

    def analyze_strategies(
        self,
        event_type: str,
        event_data: Dict,
        market_conditions: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze which hedge fund strategies are best for this event

        Args:
            event_type: Type of extreme event
            event_data: Event details
            market_conditions: Current market state (VIX, rates, etc.)

        Returns:
            Strategy recommendations and portfolio allocation
        """

        # Get base strategy scores
        if event_type not in self.strategy_performance_matrix:
            event_type = 'economic_crisis'  # Default fallback

        strategy_scores = self.strategy_performance_matrix[event_type]

        # Adjust scores based on market conditions
        if market_conditions:
            strategy_scores = self._adjust_for_market_conditions(
                strategy_scores,
                market_conditions
            )

        # Adjust based on event severity
        severity = event_data.get('severity', 3)
        if severity >= 4:
            # High severity favors defensive/arbitrage strategies
            strategy_scores = self._boost_defensive_strategies(strategy_scores)

        # Generate recommendations
        recommendations = []
        for strategy, score in sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True):
            if score >= 60:  # Only recommend strategies with score >= 60
                rec = self._create_recommendation(strategy, score, event_type, event_data)
                recommendations.append(rec)

        # Generate portfolio allocation
        allocation = self._generate_allocation(recommendations, severity)

        # Identify opportunistic plays
        opportunistic_plays = self._identify_opportunistic_plays(
            event_type,
            event_data,
            recommendations
        )

        return {
            'top_strategies': recommendations[:5],
            'all_recommendations': recommendations,
            'portfolio_allocation': allocation,
            'opportunistic_plays': opportunistic_plays,
            'execution_priority': self._determine_execution_priority(recommendations),
            'risk_management': self._generate_risk_management_plan(event_type, severity)
        }

    def _create_recommendation(
        self,
        strategy: HedgeFundStrategy,
        score: float,
        event_type: str,
        event_data: Dict
    ) -> StrategyRecommendation:
        """Create detailed strategy recommendation"""

        # Get baseline alpha and adjust for event
        base_alpha = self.baseline_alpha.get(strategy, 5.0)
        event_multiplier = score / 70.0  # 70 is average score
        expected_alpha = base_alpha * event_multiplier

        # Determine risk level
        risk_level = 'high' if score < 70 else ('medium' if score < 85 else 'low')

        # Get strategy-specific details
        details = self._get_strategy_details(strategy, event_type, event_data)

        return StrategyRecommendation(
            strategy=strategy,
            suitability_score=score,
            expected_alpha=expected_alpha,
            risk_level=risk_level,
            time_horizon=details['time_horizon'],
            rationale=details['rationale'],
            key_positions=details['key_positions'],
            risk_factors=details['risk_factors'],
            historical_performance=details['historical_performance']
        )

    def _get_strategy_details(self, strategy: HedgeFundStrategy, event_type: str, event_data: Dict) -> Dict:
        """Get detailed information for each strategy"""

        details_map = {
            HedgeFundStrategy.GLOBAL_MACRO: {
                'time_horizon': 'medium',
                'rationale': f"Macro funds excel during {event_type} by capitalizing on central bank divergence, currency moves, and commodity spreads. 2025 YTD: +11.2%.",
                'key_positions': [
                    'Long USD vs emerging market currencies',
                    'Short government bonds (rising rates)',
                    'Long commodities (inflation hedge)',
                    'FX carry trades on rate differentials'
                ],
                'risk_factors': [
                    'Central bank policy surprises',
                    'Geopolitical escalation',
                    'Liquidity dry-ups'
                ],
                'historical_performance': 'Macro funds averaged +15% during major crises (2008, 2020, 2022)'
            },
            HedgeFundStrategy.EVENT_DRIVEN: {
                'time_horizon': 'short',
                'rationale': f"Event-driven strategies capitalize on deal activity, restructurings, and special situations during {event_type}. 2025 YTD: +8.7%.",
                'key_positions': [
                    'Merger arbitrage spreads',
                    'Distressed company bonds',
                    'Activist positions',
                    'Special situations (spin-offs, splits)'
                ],
                'risk_factors': [
                    'Deal breaks',
                    'Regulatory intervention',
                    'Financing issues'
                ],
                'historical_performance': 'Event-driven +12% during 2020 crisis with M&A surge'
            },
            HedgeFundStrategy.CONVERTIBLE_ARBITRAGE: {
                'time_horizon': 'short',
                'rationale': f"Convertible arb captures volatility in underlying equities while maintaining hedged positions. 2025 YTD: +4.0% with tech volatility.",
                'key_positions': [
                    'Long convertible bonds, short underlying stock',
                    'Volatility capture on tech sector',
                    'Credit spread arbitrage',
                    'Gamma trading'
                ],
                'risk_factors': [
                    'Correlation breakdowns',
                    'Credit deterioration',
                    'Liquidity shocks'
                ],
                'historical_performance': 'Convertible arb +8% in 2025 H1 with robust issuance'
            },
            HedgeFundStrategy.VOLATILITY_ARBITRAGE: {
                'time_horizon': 'short',
                'rationale': f"Vol arb exploits mispricings in options and volatility derivatives during extreme events.",
                'key_positions': [
                    'Long VIX calls (crash protection)',
                    'Short volatility in overpriced sectors',
                    'Dispersion trades (index vol vs single stock)',
                    'Vol curve arbitrage'
                ],
                'risk_factors': [
                    'Gamma squeezes',
                    'Tail events',
                    'Model risk'
                ],
                'historical_performance': 'Vol strategies +25% during March 2020 VIX spike'
            },
            HedgeFundStrategy.DISTRESSED_DEBT: {
                'time_horizon': 'long',
                'rationale': f"Distressed debt captures deep value in stressed companies during {event_type}.",
                'key_positions': [
                    'Senior secured debt of distressed companies',
                    'DIP (debtor-in-possession) financing',
                    'Bankruptcy claims',
                    'Loan-to-own strategies'
                ],
                'risk_factors': [
                    'Recovery rate uncertainty',
                    'Extended bankruptcy timelines',
                    'Priority disputes'
                ],
                'historical_performance': 'Distressed averaged +20% in 2009-2010 recovery'
            },
            HedgeFundStrategy.LONG_SHORT_EQUITY: {
                'time_horizon': 'medium',
                'rationale': f"Long/short equity benefits from dispersion and volatility during {event_type}.",
                'key_positions': [
                    'Long quality/defensive stocks',
                    'Short cyclicals/high-beta',
                    'Sector pair trades',
                    'Factor-based long/short'
                ],
                'risk_factors': [
                    'Correlation spikes',
                    'Short squeezes',
                    'Factor reversals'
                ],
                'historical_performance': 'L/S equity +12% in 2022 bear market with high dispersion'
            },
            HedgeFundStrategy.STATISTICAL_ARBITRAGE: {
                'time_horizon': 'short',
                'rationale': f"Stat arb exploits mean reversion and pricing inefficiencies during {event_type} volatility.",
                'key_positions': [
                    'Pairs trading (relative value)',
                    'Index arbitrage',
                    'ETF/basket arbitrage',
                    'High-frequency mean reversion'
                ],
                'risk_factors': [
                    'Regime changes',
                    'Correlation breakdowns',
                    'Execution slippage'
                ],
                'historical_performance': 'Stat arb +10% during 2020 with elevated volatility'
            },
            HedgeFundStrategy.CTA_TREND_FOLLOWING: {
                'time_horizon': 'medium',
                'rationale': f"CTAs capture sustained trends in commodities, FX, and rates during {event_type}.",
                'key_positions': [
                    'Long commodities trends',
                    'Short equity indices',
                    'FX momentum',
                    'Interest rate trends'
                ],
                'risk_factors': [
                    'Trend reversals',
                    'Whipsaw losses',
                    'Crowded trades'
                ],
                'historical_performance': 'CTAs +15% in 2022 with sustained inflation trend'
            },
            HedgeFundStrategy.MARKET_NEUTRAL: {
                'time_horizon': 'medium',
                'rationale': f"Market neutral strategies provide uncorrelated returns during {event_type} with beta near zero.",
                'key_positions': [
                    'Equal dollar long/short',
                    'Factor-neutral portfolios',
                    'Statistical arbitrage',
                    'Cash rebate on short positions (4-5% in 2025)'
                ],
                'risk_factors': [
                    'Factor tilts',
                    'Unintended beta exposure',
                    'Correlation shocks'
                ],
                'historical_performance': 'Market neutral +6% steady returns regardless of market direction'
            }
        }

        return details_map.get(strategy, {
            'time_horizon': 'medium',
            'rationale': f"Multi-strategy approach suitable for {event_type}",
            'key_positions': ['Diversified across strategies'],
            'risk_factors': ['General market risk'],
            'historical_performance': 'Varies by sub-strategy'
        })

    def _adjust_for_market_conditions(self, scores: Dict, conditions: Dict) -> Dict:
        """Adjust strategy scores based on current market conditions"""
        adjusted = scores.copy()

        # VIX level adjustments
        vix = conditions.get('vix', 20)
        if vix > 30:  # High volatility
            # Boost volatility strategies
            for strategy in [HedgeFundStrategy.VOLATILITY_ARBITRAGE,
                           HedgeFundStrategy.CONVERTIBLE_ARBITRAGE]:
                if strategy in adjusted:
                    adjusted[strategy] *= 1.2

        # Rate environment
        rates = conditions.get('interest_rate', 4.0)
        if rates > 4.5:  # High rates
            # Boost market neutral (cash rebate benefit)
            if HedgeFundStrategy.MARKET_NEUTRAL in adjusted:
                adjusted[HedgeFundStrategy.MARKET_NEUTRAL] *= 1.15

        # Dispersion (stock correlation)
        dispersion = conditions.get('dispersion', 0.5)
        if dispersion > 0.6:  # High dispersion
            # Boost long/short equity
            if HedgeFundStrategy.LONG_SHORT_EQUITY in adjusted:
                adjusted[HedgeFundStrategy.LONG_SHORT_EQUITY] *= 1.15

        return adjusted

    def _boost_defensive_strategies(self, scores: Dict) -> Dict:
        """Boost defensive strategies during severe events"""
        defensive_strategies = [
            HedgeFundStrategy.MARKET_NEUTRAL,
            HedgeFundStrategy.VOLATILITY_ARBITRAGE,
            HedgeFundStrategy.GLOBAL_MACRO
        ]

        boosted = scores.copy()
        for strategy in defensive_strategies:
            if strategy in boosted:
                boosted[strategy] *= 1.1

        return boosted

    def _generate_allocation(
        self,
        recommendations: List[StrategyRecommendation],
        severity: int
    ) -> List[StrategyAllocation]:
        """Generate portfolio allocation across strategies"""

        # Risk-adjusted allocation based on severity
        if severity >= 4:
            # Conservative allocation during severe events
            max_per_strategy = 25
            total_allocation = 80  # Hold 20% cash
        else:
            max_per_strategy = 35
            total_allocation = 95  # Hold 5% cash

        allocations = []
        total_score = sum(rec.suitability_score for rec in recommendations[:5])

        for rec in recommendations[:5]:
            # Weight by suitability score
            allocation_pct = (rec.suitability_score / total_score) * total_allocation
            allocation_pct = min(allocation_pct, max_per_strategy)

            allocations.append(StrategyAllocation(
                strategy=rec.strategy,
                allocation_pct=allocation_pct,
                position_sizing='25% of allocation per position, max 4 positions',
                entry_timing=self._get_entry_timing(rec.strategy, rec.time_horizon),
                exit_criteria=self._get_exit_criteria(rec.strategy)
            ))

        return allocations

    def _get_entry_timing(self, strategy: HedgeFundStrategy, time_horizon: str) -> str:
        """Determine optimal entry timing"""
        if time_horizon == 'short':
            return 'Immediate - event creates short-term mispricings'
        elif time_horizon == 'medium':
            return 'Scaled entry over 1-2 weeks'
        else:
            return 'Patient accumulation over 1-2 months'

    def _get_exit_criteria(self, strategy: HedgeFundStrategy) -> List[str]:
        """Define exit criteria for each strategy"""
        return [
            'Take profit at +15% for individual positions',
            'Stop loss at -7% for high-conviction trades',
            'Exit 50% of position when thesis plays out',
            'Reduce exposure if correlation to market exceeds 0.7',
            'Exit if strategy expected alpha drops below 5%'
        ]

    def _identify_opportunistic_plays(
        self,
        event_type: str,
        event_data: Dict,
        recommendations: List[StrategyRecommendation]
    ) -> List[Dict]:
        """Identify time-sensitive opportunistic plays"""
        plays = []

        # Volatility spike plays
        plays.append({
            'name': 'VIX Call Spread (0-3 days to act)',
            'strategy': 'Buy VIX 30/40 call spread',
            'max_allocation': '2-5% of portfolio',
            'expected_return': '+50% to +200% if crisis escalates',
            'risk': 'Total loss if volatility doesn\'t spike',
            'time_window': '24-72 hours from event'
        })

        # Dispersion trade
        plays.append({
            'name': 'Index vs Single Stock Vol Dispersion',
            'strategy': 'Long single-stock vol, short index vol',
            'max_allocation': '3-8% of portfolio',
            'expected_return': '+30% to +80% as correlations break down',
            'risk': 'Correlation spike during systemic crisis',
            'time_window': '1-2 weeks'
        })

        # Distressed opportunities
        if event_data.get('severity', 3) >= 4:
            plays.append({
                'name': 'Distressed Debt of Fallen Angels',
                'strategy': 'Buy senior secured debt trading at 40-60 cents on dollar',
                'max_allocation': '5-10% of portfolio',
                'expected_return': '+50% to +150% over 12-18 months',
                'risk': 'Extended bankruptcy, recovery rate uncertainty',
                'time_window': '1-3 months (accumulation phase)'
            })

        return plays

    def _determine_execution_priority(
        self,
        recommendations: List[StrategyRecommendation]
    ) -> Dict:
        """Determine execution priority and sequencing"""

        # Short-term first (capture immediate mispricings)
        short_term = [r for r in recommendations if r.time_horizon == 'short']
        medium_term = [r for r in recommendations if r.time_horizon == 'medium']
        long_term = [r for r in recommendations if r.time_horizon == 'long']

        return {
            'phase_1_immediate': {
                'timeframe': '0-24 hours',
                'strategies': [r.strategy.value for r in short_term[:2]],
                'focus': 'Capture volatility and immediate mispricings'
            },
            'phase_2_short_term': {
                'timeframe': '1-7 days',
                'strategies': [r.strategy.value for r in short_term[2:] + medium_term[:2]],
                'focus': 'Build core positions as market digests event'
            },
            'phase_3_medium_term': {
                'timeframe': '1-4 weeks',
                'strategies': [r.strategy.value for r in medium_term[2:] + long_term],
                'focus': 'Patient accumulation of longer-term opportunities'
            }
        }

    def _generate_risk_management_plan(self, event_type: str, severity: int) -> Dict:
        """Generate risk management guidelines"""

        base_var_limit = 10.0  # 10% portfolio VaR
        if severity >= 4:
            var_limit = base_var_limit * 0.7  # Reduce risk 30%
        else:
            var_limit = base_var_limit

        return {
            'var_limit': f'{var_limit}% of portfolio',
            'max_drawdown_limit': '15% portfolio-wide',
            'correlation_limit': 'Max 0.6 correlation to S&P 500',
            'liquidity_requirements': 'Maintain 20% in positions that can be liquidated within 48 hours',
            'stress_tests': [
                'Daily VaR calculation',
                'Weekly stress testing (3-sigma move)',
                'Monthly correlation analysis'
            ],
            'position_limits': {
                'single_strategy': '25% max',
                'single_position': '5% max',
                'sector_concentration': '20% max'
            },
            'stop_loss_protocols': [
                f'Strategy-level: Exit if down >12% in {severity*5} days',
                'Portfolio-level: Reduce gross exposure by 30% if down >8%',
                'Correlation spike: Reduce if portfolio beta to market >0.5'
            ]
        }
