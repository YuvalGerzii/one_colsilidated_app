"""
Derivatives and Options Strategist (V4.0)

Advanced derivatives strategies for extreme events.
Based on 2025 market intelligence:
- Zero-day options (0DTE) iron condors
- Put protection strategies
- Volatility capture with covered calls
- Crisis hedging with tail risk protection
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class OptionsStrategy(Enum):
    """Options strategy types"""
    LONG_PUT = "long_put"
    LONG_CALL = "long_call"
    PUT_SPREAD = "put_spread"
    CALL_SPREAD = "call_spread"
    IRON_CONDOR = "iron_condor"
    STRADDLE = "straddle"
    STRANGLE = "strangle"
    BUTTERFLY = "butterfly"
    COVERED_CALL = "covered_call"
    PROTECTIVE_PUT = "protective_put"
    COLLAR = "collar"
    CALENDAR_SPREAD = "calendar_spread"
    RATIO_SPREAD = "ratio_spread"
    VIX_CALLS = "vix_calls"
    ZERO_DTE = "zero_dte"


@dataclass
class OptionsRecommendation:
    """Options strategy recommendation"""
    strategy: OptionsStrategy
    underlying: str
    strike_prices: List[float]
    expiration: str  # DTE (days to expiration)
    max_cost: float  # As % of portfolio
    max_profit: str
    max_loss: str
    breakeven: List[float]
    implied_vol_required: float  # IV percentile
    probability_profit: float
    rationale: str
    execution_timing: str
    greeks: Dict[str, float]  # delta, gamma, theta, vega


@dataclass
class DerivativesPosition:
    """Derivatives position specification"""
    instrument: str
    direction: str  # long/short
    quantity: str
    entry_price: str
    target_price: str
    stop_loss: str
    time_decay_impact: str
    vega_exposure: str


class DerivativesStrategist:
    """
    Recommends options and derivatives strategies for extreme events.
    Optimized for 2025 market conditions with high volatility opportunities.
    """

    def __init__(self):
        """Initialize derivatives strategist"""

        # Current market IV levels (2025 baseline)
        self.baseline_iv = {
            'SPY': 18,  # S&P 500 ETF
            'QQQ': 22,  # Nasdaq ETF
            'IWM': 24,  # Russell 2000
            'VIX': 16,  # Volatility index
            'TLT': 12,  # 20Y Treasury
            'GLD': 14,  # Gold
            'USO': 35,  # Oil
        }

        # IV spike multipliers by event type
        self.iv_multipliers = {
            'market_crash': 2.5,
            'recession': 1.8,
            'geopolitical': 1.6,
            'inflation': 1.4,
            'interest_rate_change': 1.3,
            'pandemic': 2.0,
            'terrorism': 1.7,
            'cyber_attack': 1.5,
        }

    def analyze_derivatives_opportunities(
        self,
        event_type: str,
        event_data: Dict,
        portfolio_value: float,
        risk_tolerance: str = 'medium'
    ) -> Dict:
        """
        Analyze derivatives opportunities for the event

        Args:
            event_type: Type of extreme event
            event_data: Event details
            portfolio_value: Total portfolio value
            risk_tolerance: low, medium, high

        Returns:
            Comprehensive derivatives strategy recommendations
        """

        severity = event_data.get('severity', 3)
        time_horizon = event_data.get('time_horizon_days', 30)

        # Estimate IV environment
        iv_environment = self._estimate_iv_environment(event_type, severity)

        # Generate strategy recommendations
        recommendations = []

        # 1. Protective strategies (always recommend for severe events)
        if severity >= 3:
            protective = self._generate_protective_strategies(
                severity,
                portfolio_value,
                iv_environment
            )
            recommendations.extend(protective)

        # 2. Volatility capture strategies
        vol_strategies = self._generate_volatility_strategies(
            event_type,
            severity,
            iv_environment,
            portfolio_value
        )
        recommendations.extend(vol_strategies)

        # 3. Directional strategies (if clear market direction)
        directional = self._generate_directional_strategies(
            event_type,
            event_data,
            iv_environment,
            portfolio_value
        )
        recommendations.extend(directional)

        # 4. Income strategies (in elevated IV)
        if iv_environment['current_iv_percentile'] > 50:
            income = self._generate_income_strategies(
                iv_environment,
                portfolio_value,
                risk_tolerance
            )
            recommendations.extend(income)

        # 5. Fast-action 0DTE strategies
        if severity >= 4:
            fast_action = self._generate_fast_action_strategies(
                event_type,
                severity,
                iv_environment,
                portfolio_value
            )
            recommendations.extend(fast_action)

        # Generate portfolio allocation
        allocation = self._generate_derivatives_allocation(
            recommendations,
            portfolio_value,
            risk_tolerance,
            severity
        )

        # Greeks management
        greeks_analysis = self._analyze_portfolio_greeks(recommendations)

        return {
            'recommendations': recommendations,
            'allocation': allocation,
            'iv_environment': iv_environment,
            'greeks_analysis': greeks_analysis,
            'execution_plan': self._create_execution_plan(recommendations, severity),
            'risk_management': self._create_derivatives_risk_plan(severity, iv_environment),
            'expected_pnl_scenarios': self._generate_pnl_scenarios(recommendations, event_type)
        }

    def _estimate_iv_environment(self, event_type: str, severity: int) -> Dict:
        """Estimate implied volatility environment"""

        base_iv = self.baseline_iv['SPY']
        multiplier = self.iv_multipliers.get(event_type, 1.5)

        # Severity adjustment
        severity_boost = 1.0 + (severity - 3) * 0.15

        expected_iv = base_iv * multiplier * severity_boost
        expected_vix = expected_iv * 1.4  # VIX typically 1.4x higher than SPX IV

        return {
            'current_iv_percentile': min(95, expected_iv * 2),  # Rough percentile
            'expected_iv': expected_iv,
            'expected_vix': expected_vix,
            'iv_regime': 'extreme' if expected_iv > 40 else ('high' if expected_iv > 25 else 'elevated'),
            'term_structure': 'inverted' if severity >= 4 else 'normal',
            'skew': 'steep' if severity >= 3 else 'moderate'
        }

    def _generate_protective_strategies(
        self,
        severity: int,
        portfolio_value: float,
        iv_environment: Dict
    ) -> List[OptionsRecommendation]:
        """Generate protective/hedging strategies"""

        strategies = []

        # 1. Protective puts (downside protection)
        max_cost_pct = 1.5 if severity >= 4 else 1.0
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.PROTECTIVE_PUT,
            underlying='SPY',
            strike_prices=[self._get_otm_put_strike('SPY', -5)],  # 5% OTM
            expiration='30-60 DTE',
            max_cost=portfolio_value * (max_cost_pct / 100),
            max_profit='Unlimited upside, protected downside',
            max_loss=f'{max_cost_pct}% of portfolio (premium paid)',
            breakeven=[],
            implied_vol_required=iv_environment['expected_iv'],
            probability_profit=65.0,
            rationale='Classic portfolio insurance. Provides defined downside protection while maintaining upside participation. Cost is 1-2% of portfolio for 30-60 days of protection.',
            execution_timing='Immediate - protection value highest early in event',
            greeks={'delta': -0.30, 'gamma': 0.05, 'theta': -0.02, 'vega': 0.15}
        ))

        # 2. Put spread (cheaper protection)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.PUT_SPREAD,
            underlying='SPY',
            strike_prices=[
                self._get_otm_put_strike('SPY', -5),   # Buy
                self._get_otm_put_strike('SPY', -15)   # Sell
            ],
            expiration='30-45 DTE',
            max_cost=portfolio_value * 0.5 / 100,
            max_profit='10% portfolio protection',
            max_loss='0.5% of portfolio',
            breakeven=[self._get_otm_put_strike('SPY', -5) - 0.5],
            implied_vol_required=iv_environment['expected_iv'] * 0.9,
            probability_profit=60.0,
            rationale='Cost-efficient protection. Cheaper than straight puts (0.5% vs 1.5%) but caps protection at the short strike. Good for moderate drawdown protection.',
            execution_timing='Within 48 hours',
            greeks={'delta': -0.25, 'gamma': 0.04, 'theta': -0.015, 'vega': 0.10}
        ))

        # 3. Collar (zero-cost protection)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.COLLAR,
            underlying='SPY or portfolio holdings',
            strike_prices=[
                self._get_otm_put_strike('SPY', -5),   # Buy put
                self._get_otm_call_strike('SPY', 8)     # Sell call
            ],
            expiration='60-90 DTE',
            max_cost=0,  # Zero or near-zero cost
            max_profit='~8% upside (capped at short call)',
            max_loss='~5% downside (protected by long put)',
            breakeven=[],
            implied_vol_required=iv_environment['expected_iv'],
            probability_profit=55.0,
            rationale='Zero-cost hedge by selling upside to buy downside protection. Limits gains to ~8% but protects against losses beyond 5%. Ideal for defensive positioning.',
            execution_timing='Within 1 week',
            greeks={'delta': -0.10, 'gamma': 0.02, 'theta': -0.005, 'vega': 0.05}
        ))

        return strategies

    def _generate_volatility_strategies(
        self,
        event_type: str,
        severity: int,
        iv_environment: Dict,
        portfolio_value: float
    ) -> List[OptionsRecommendation]:
        """Generate volatility-focused strategies"""

        strategies = []

        # 1. Long VIX calls (pure volatility play)
        if severity >= 4:
            strategies.append(OptionsRecommendation(
                strategy=OptionsStrategy.VIX_CALLS,
                underlying='VIX',
                strike_prices=[30, 40],  # VIX 30/40 call spread
                expiration='30-45 DTE',
                max_cost=portfolio_value * 2.0 / 100,
                max_profit='+50% to +200% if VIX spikes to 50+',
                max_loss='100% of premium (2% of portfolio)',
                breakeven=[33.0],  # VIX at 33
                implied_vol_required=100,  # VIX options have high IV
                probability_profit=35.0,
                rationale='Asymmetric payoff during crisis. VIX calls can return 3-5x if volatility explodes (e.g., VIX 50+). March 2020: VIX spiked from 15 to 80, VIX calls returned 10-20x. High risk but massive upside.',
                execution_timing='IMMEDIATE - within 24 hours of event',
                greeks={'delta': 0.40, 'gamma': 0.08, 'theta': -0.04, 'vega': 0.30}
            ))

        # 2. Straddle (bet on large move either direction)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.STRADDLE,
            underlying='SPY',
            strike_prices=[self._get_atm_strike('SPY')],  # ATM strike
            expiration='20-30 DTE',
            max_cost=portfolio_value * 3.0 / 100,
            max_profit='Unlimited (if large move occurs)',
            max_loss='3% of portfolio if no move',
            breakeven=[
                self._get_atm_strike('SPY') - 3.0,
                self._get_atm_strike('SPY') + 3.0
            ],
            implied_vol_required=iv_environment['expected_iv'],
            probability_profit=45.0,
            rationale='Profits from large moves in either direction. Requires ~7-8% move to breakeven. Works best when you expect volatility explosion but direction uncertain. 2020: straddles bought pre-crisis returned 200-300%.',
            execution_timing='Within 48 hours before IV spikes further',
            greeks={'delta': 0.0, 'gamma': 0.15, 'theta': -0.06, 'vega': 0.40}
        ))

        # 3. Dispersion trade (long single stock vol, short index vol)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.STRANGLE,
            underlying='Individual stocks (tech: AAPL, MSFT, NVDA)',
            strike_prices=[
                self._get_otm_put_strike('QQQ', -5),
                self._get_otm_call_strike('QQQ', 5)
            ],
            expiration='30-45 DTE',
            max_cost=portfolio_value * 2.0 / 100,
            max_profit='+30% to +80% if dispersion increases',
            max_loss='100% of premium if correlations rise',
            breakeven=[],
            implied_vol_required=iv_environment['expected_iv'] * 1.2,
            probability_profit=55.0,
            rationale='Dispersion trade: correlations break down during crises, single stocks move more than index. Long individual stock options, short index options. Works when market fragments (2020, 2022).',
            execution_timing='1-2 weeks into event',
            greeks={'delta': 0.0, 'gamma': 0.10, 'theta': -0.04, 'vega': 0.25}
        ))

        return strategies

    def _generate_directional_strategies(
        self,
        event_type: str,
        event_data: Dict,
        iv_environment: Dict,
        portfolio_value: float
    ) -> List[OptionsRecommendation]:
        """Generate directional strategies based on event analysis"""

        strategies = []

        # Determine market direction from event
        expected_direction = self._determine_market_direction(event_type, event_data)

        if expected_direction == 'down':
            # Bear put spreads
            strategies.append(OptionsRecommendation(
                strategy=OptionsStrategy.PUT_SPREAD,
                underlying='SPY',
                strike_prices=[
                    self._get_otm_put_strike('SPY', 0),   # ATM
                    self._get_otm_put_strike('SPY', -10)  # 10% OTM
                ],
                expiration='30-60 DTE',
                max_cost=portfolio_value * 2.0 / 100,
                max_profit='+150% to +300% if market drops 10%',
                max_loss='100% of premium (2% of portfolio)',
                breakeven=[self._get_otm_put_strike('SPY', 0) - 2.0],
                implied_vol_required=iv_environment['expected_iv'] * 0.85,
                probability_profit=40.0,
                rationale=f'Bearish directional play. {event_type} expected to push markets down 5-15%. Bear put spread offers leveraged downside with defined risk. Max profit if SPY drops 10%+.',
                execution_timing='Within 3-5 days',
                greeks={'delta': -0.40, 'gamma': 0.06, 'theta': -0.02, 'vega': 0.12}
            ))

        # Sector-specific plays
        sector_plays = self._get_sector_directional_plays(event_type, iv_environment, portfolio_value)
        strategies.extend(sector_plays)

        return strategies

    def _generate_income_strategies(
        self,
        iv_environment: Dict,
        portfolio_value: float,
        risk_tolerance: str
    ) -> List[OptionsRecommendation]:
        """Generate income strategies in high IV environment"""

        strategies = []

        # Covered calls (generate income on existing positions)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.COVERED_CALL,
            underlying='Portfolio holdings or SPY',
            strike_prices=[self._get_otm_call_strike('SPY', 5)],  # 5% OTM
            expiration='30-45 DTE',
            max_cost=0,  # No upfront cost (selling options)
            max_profit='+2% to +4% monthly income',
            max_loss='Opportunity cost if stock rallies past strike',
            breakeven=[],
            implied_vol_required=iv_environment['expected_iv'],
            probability_profit=75.0,
            rationale=f"High IV environment (IV: {iv_environment['expected_iv']}) = fat premiums. Covered calls can generate 2-4% monthly income. Caps upside but excellent for range-bound markets. 2025: IV spike makes this very attractive.",
            execution_timing='Any time during elevated IV',
            greeks={'delta': -0.30, 'gamma': -0.03, 'theta': 0.03, 'vega': -0.12}
        ))

        # Cash-secured puts (generate income, acquire stocks cheaper)
        if risk_tolerance in ['medium', 'high']:
            strategies.append(OptionsRecommendation(
                strategy=OptionsStrategy.LONG_PUT,
                underlying='Quality stocks (AAPL, MSFT, etc.) or SPY',
                strike_prices=[self._get_otm_put_strike('SPY', -5)],  # 5% below current
                expiration='30-45 DTE',
                max_cost=0,
                max_profit='+1.5% to +3% monthly income',
                max_loss='Assigned stock at strike (obligation to buy)',
                breakeven=[],
                implied_vol_required=iv_environment['expected_iv'],
                probability_profit=70.0,
                rationale='Sell puts on stocks you want to own at lower prices. Collect premium (1.5-3% monthly) while waiting. If assigned, you bought the dip. If not assigned, keep premium. Win-win in volatile markets.',
                execution_timing='After initial panic selling subsides',
                greeks={'delta': 0.25, 'gamma': -0.04, 'theta': 0.025, 'vega': -0.10}
            ))

        return strategies

    def _generate_fast_action_strategies(
        self,
        event_type: str,
        severity: int,
        iv_environment: Dict,
        portfolio_value: float
    ) -> List[OptionsRecommendation]:
        """Generate time-sensitive, fast-action strategies (0DTE, weekly options)"""

        strategies = []

        # Zero-day options (0DTE) - extremely time-sensitive
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.ZERO_DTE,
            underlying='SPX (S&P 500 Index)',
            strike_prices=[
                self._get_atm_strike('SPX') - 20,  # Slightly OTM iron condor
                self._get_atm_strike('SPX') - 10,
                self._get_atm_strike('SPX') + 10,
                self._get_atm_strike('SPX') + 20
            ],
            expiration='0-1 DTE (same-day or next-day expiration)',
            max_cost=portfolio_value * 1.0 / 100,
            max_profit='+20% to +50% if market stays range-bound',
            max_loss='100% of premium (but limited to 1%)',
            breakeven=[],
            implied_vol_required=iv_environment['expected_iv'] * 1.3,
            probability_profit=65.0,
            rationale='0DTE iron condors are HOT in 2025. Bet on market staying within range for next 24 hours. Theta decay is extreme (options lose value every hour). Popular with systematic hedge funds. High win rate but requires precision timing.',
            execution_timing='IMMEDIATE - morning of trading day, close by 2pm ET',
            greeks={'delta': 0.0, 'gamma': 0.20, 'theta': -0.15, 'vega': 0.08}
        ))

        # Weekly puts (short-term crash protection)
        strategies.append(OptionsRecommendation(
            strategy=OptionsStrategy.LONG_PUT,
            underlying='SPY',
            strike_prices=[self._get_otm_put_strike('SPY', -3)],  # 3% OTM
            expiration='3-7 DTE (weekly options)',
            max_cost=portfolio_value * 0.5 / 100,
            max_profit='+100% to +500% if flash crash occurs',
            max_loss='100% of premium (0.5% of portfolio)',
            breakeven=[self._get_otm_put_strike('SPY', -3) - 0.5],
            implied_vol_required=iv_environment['expected_iv'] * 1.1,
            probability_profit=30.0,
            rationale='Lottery ticket for flash crash. Weeklies are cheap but can explode 5-10x if market gaps down 5%+ in single day. Feb 2018 VIXpocalypse: weekly puts returned 10-20x. Low probability but massive asymmetry.',
            execution_timing='First 48 hours after event - before IV spikes too high',
            greeks={'delta': -0.20, 'gamma': 0.10, 'theta': -0.08, 'vega': 0.18}
        ))

        return strategies

    def _get_sector_directional_plays(
        self,
        event_type: str,
        iv_environment: Dict,
        portfolio_value: float
    ) -> List[OptionsRecommendation]:
        """Get sector-specific directional plays"""

        plays = []

        sector_map = {
            'recession': {
                'short': ['XLY (Consumer Discretionary)', 'XLF (Financials)'],
                'long': ['XLP (Consumer Staples)', 'XLU (Utilities)']
            },
            'inflation': {
                'short': ['XLK (Technology)', 'TLT (Long Bonds)'],
                'long': ['XLE (Energy)', 'GLD (Gold)']
            },
            'cyber_attack': {
                'short': ['XLF (Financials)', 'HACK (Cybersecurity if breach)'],
                'long': ['CIBR (Cybersecurity if rally)']
            }
        }

        sectors = sector_map.get(event_type, {})

        # Short sectors
        for sector in sectors.get('short', [])[:2]:
            plays.append(OptionsRecommendation(
                strategy=OptionsStrategy.LONG_PUT,
                underlying=sector.split()[0],
                strike_prices=[self._get_otm_put_strike(sector.split()[0], -2)],
                expiration='45-60 DTE',
                max_cost=portfolio_value * 1.0 / 100,
                max_profit='+50% to +150% if sector drops',
                max_loss='100% of premium',
                breakeven=[],
                implied_vol_required=iv_environment['expected_iv'],
                probability_profit=50.0,
                rationale=f'{event_type} negatively impacts {sector}. Targeted bearish play.',
                execution_timing='Within 1 week',
                greeks={'delta': -0.35, 'gamma': 0.05, 'theta': -0.02, 'vega': 0.14}
            ))

        return plays

    def _generate_derivatives_allocation(
        self,
        recommendations: List[OptionsRecommendation],
        portfolio_value: float,
        risk_tolerance: str,
        severity: int
    ) -> Dict:
        """Generate allocation across derivatives strategies"""

        # Risk budgets by risk tolerance
        risk_budgets = {
            'low': 3.0,      # Max 3% in options
            'medium': 5.0,   # Max 5% in options
            'high': 8.0      # Max 8% in options
        }

        max_allocation = risk_budgets[risk_tolerance]

        # Adjust for severity
        if severity >= 4:
            max_allocation *= 1.2  # Increase options exposure in severe events

        # Categorize strategies
        protective = [r for r in recommendations if r.strategy in [
            OptionsStrategy.PROTECTIVE_PUT, OptionsStrategy.PUT_SPREAD, OptionsStrategy.COLLAR
        ]]
        volatility = [r for r in recommendations if r.strategy in [
            OptionsStrategy.VIX_CALLS, OptionsStrategy.STRADDLE, OptionsStrategy.STRANGLE
        ]]
        income = [r for r in recommendations if r.strategy in [
            OptionsStrategy.COVERED_CALL, OptionsStrategy.IRON_CONDOR
        ]]
        directional = [r for r in recommendations if r.strategy in [
            OptionsStrategy.LONG_PUT, OptionsStrategy.LONG_CALL
        ]]

        # Allocate budget
        allocation = {
            'protective': min(max_allocation * 0.4, 3.0),  # 40% to protection, max 3%
            'volatility': min(max_allocation * 0.3, 2.5),  # 30% to vol plays, max 2.5%
            'income': min(max_allocation * 0.2, 2.0),      # 20% to income, max 2%
            'directional': min(max_allocation * 0.1, 1.5), # 10% to directional, max 1.5%
            'total_max': max_allocation
        }

        return allocation

    def _analyze_portfolio_greeks(self, recommendations: List[OptionsRecommendation]) -> Dict:
        """Analyze aggregate portfolio Greeks"""

        total_delta = sum(r.greeks.get('delta', 0) for r in recommendations)
        total_gamma = sum(r.greeks.get('gamma', 0) for r in recommendations)
        total_theta = sum(r.greeks.get('theta', 0) for r in recommendations)
        total_vega = sum(r.greeks.get('vega', 0) for r in recommendations)

        return {
            'portfolio_delta': total_delta,
            'delta_interpretation': self._interpret_delta(total_delta),
            'portfolio_gamma': total_gamma,
            'gamma_interpretation': 'High convexity - profits accelerate with moves',
            'portfolio_theta': total_theta,
            'theta_interpretation': f'Time decay: ${abs(total_theta)*1000:.0f}/day on $100k portfolio',
            'portfolio_vega': total_vega,
            'vega_interpretation': self._interpret_vega(total_vega),
            'risk_summary': self._summarize_greeks_risk(total_delta, total_gamma, total_theta, total_vega)
        }

    def _interpret_delta(self, delta: float) -> str:
        """Interpret portfolio delta"""
        if delta > 0.3:
            return 'Bullish bias - portfolio gains if market rises'
        elif delta < -0.3:
            return 'Bearish bias - portfolio gains if market falls'
        else:
            return 'Market neutral - minimal directional exposure'

    def _interpret_vega(self, vega: float) -> str:
        """Interpret portfolio vega"""
        if vega > 0.2:
            return 'Long volatility - gains if IV rises (good for crisis)'
        elif vega < -0.2:
            return 'Short volatility - loses if IV rises (risky in crisis)'
        else:
            return 'Vega neutral - minimal IV sensitivity'

    def _summarize_greeks_risk(self, delta, gamma, theta, vega) -> str:
        """Summarize overall Greeks risk"""
        risks = []

        if abs(delta) > 0.4:
            risks.append(f'High directional risk (delta: {delta:.2f})')
        if abs(gamma) > 0.15:
            risks.append('High convexity - large moves amplify P&L')
        if theta < -0.05:
            risks.append(f'Bleeding {abs(theta)*100:.1f}% per day to time decay')
        if vega > 0.3:
            risks.append('Very sensitive to volatility changes')

        return '; '.join(risks) if risks else 'Balanced risk profile'

    def _create_execution_plan(self, recommendations: List[OptionsRecommendation], severity: int) -> Dict:
        """Create execution plan for derivatives trades"""

        # Separate by timing urgency
        immediate = [r for r in recommendations if 'IMMEDIATE' in r.execution_timing.upper()]
        short_term = [r for r in recommendations if 'hour' in r.execution_timing.lower() or 'day' in r.execution_timing.lower()]
        medium_term = [r for r in recommendations if 'week' in r.execution_timing.lower()]

        return {
            'phase_1_immediate': {
                'timeframe': '0-6 hours',
                'strategies': [r.strategy.value for r in immediate],
                'priority': 'CRITICAL - VIX calls and 0DTE must be executed immediately',
                'execution_tips': [
                    'Use limit orders (bid-ask spreads widen in volatility)',
                    'Split large orders into smaller chunks',
                    'Trade during liquid hours (9:45am-3:30pm ET)',
                    'Consider using market-on-close (MOC) for better fills'
                ]
            },
            'phase_2_short_term': {
                'timeframe': '6-48 hours',
                'strategies': [r.strategy.value for r in short_term],
                'priority': 'HIGH - Protective puts and volatility plays',
                'execution_tips': [
                    'Wait for intraday volatility to subside for better entry',
                    'Use GTC (good-till-canceled) limit orders',
                    'Monitor IV levels - enter on IV dips if possible'
                ]
            },
            'phase_3_medium_term': {
                'timeframe': '1-2 weeks',
                'strategies': [r.strategy.value for r in medium_term],
                'priority': 'MEDIUM - Income and longer-dated protection',
                'execution_tips': [
                    'Patient execution - no rush',
                    'Scale into positions over several days',
                    'Consider calendar spreads to reduce cost'
                ]
            }
        }

    def _create_derivatives_risk_plan(self, severity: int, iv_environment: Dict) -> Dict:
        """Create risk management plan for derivatives"""

        return {
            'position_limits': {
                'max_single_trade': '2% of portfolio',
                'max_strategy_category': '3% of portfolio',
                'max_total_options': f"{3 + severity}% of portfolio",
                'max_0dte': '1% of portfolio'
            },
            'greeks_limits': {
                'max_portfolio_delta': 0.5,
                'max_portfolio_vega': 0.4,
                'max_daily_theta_bleed': '-0.05 (5% per day)'
            },
            'liquidity_requirements': {
                'min_open_interest': '1,000 contracts for entry',
                'min_volume': '500 contracts daily',
                'max_bid_ask_spread': '5% for entry, 10% for exit'
            },
            'exit_rules': [
                'Take profits at 50-75% of max profit potential',
                'Cut losses at 50% of premium paid',
                'Close 0DTE positions by 2pm ET (avoid pin risk)',
                'Roll protective puts 2 weeks before expiration',
                'Exit if IV drops 30% from entry (volatility collapse)'
            ],
            'monitoring': {
                'intraday': 'Monitor Greeks every 2 hours during market hours',
                'daily': 'Recalculate portfolio Greeks and P&L scenarios',
                'weekly': 'Review IV levels and adjust strategies',
                'alerts': [
                    'VIX > 40: Consider taking profits on volatility plays',
                    'Portfolio delta > 0.5: Rebalance to reduce directional risk',
                    'Theta bleed > $500/day: Consider closing or rolling positions'
                ]
            }
        }

    def _generate_pnl_scenarios(self, recommendations: List[OptionsRecommendation], event_type: str) -> Dict:
        """Generate P&L scenarios for different market outcomes"""

        return {
            'scenario_1_crisis_deepens': {
                'market_move': '-15% SPX, VIX 50+',
                'protective_pnl': '+8% to +12% (puts pay off)',
                'volatility_pnl': '+50% to +200% (VIX calls explode)',
                'income_pnl': '-3% to -5% (covered calls assigned, puts ITM)',
                'total_portfolio_impact': '+3% to +5% (hedges offset losses)'
            },
            'scenario_2_moderate_decline': {
                'market_move': '-5% to -8% SPX, VIX 30',
                'protective_pnl': '+2% to +4%',
                'volatility_pnl': '+10% to +30%',
                'income_pnl': '-1% to -2%',
                'total_portfolio_impact': '+1% to +2%'
            },
            'scenario_3_range_bound': {
                'market_move': '-2% to +2% SPX, VIX 20',
                'protective_pnl': '-1% (theta decay)',
                'volatility_pnl': '-1% to -2% (straddles decay)',
                'income_pnl': '+2% to +3% (premium collected)',
                'total_portfolio_impact': '-0.5% to +0.5% (mixed)'
            },
            'scenario_4_v_shaped_recovery': {
                'market_move': '+5% to +10% SPX, VIX 15',
                'protective_pnl': '-1.5% (puts expire worthless)',
                'volatility_pnl': '-2% (vol plays lose)',
                'income_pnl': '+1% (some premium kept)',
                'total_portfolio_impact': '-2% to -3% (hedges cost, but portfolio rallies)'
            }
        }

    # Helper methods for strike calculations
    def _get_atm_strike(self, underlying: str) -> float:
        """Get at-the-money strike (simplified)"""
        base_prices = {'SPY': 450, 'QQQ': 380, 'SPX': 4500, 'VIX': 18}
        return base_prices.get(underlying, 100)

    def _get_otm_put_strike(self, underlying: str, pct_otm: float) -> float:
        """Get out-of-the-money put strike"""
        atm = self._get_atm_strike(underlying)
        return atm * (1 + pct_otm / 100)

    def _get_otm_call_strike(self, underlying: str, pct_otm: float) -> float:
        """Get out-of-the-money call strike"""
        atm = self._get_atm_strike(underlying)
        return atm * (1 + pct_otm / 100)

    def _determine_market_direction(self, event_type: str, event_data: Dict) -> str:
        """Determine expected market direction from event"""
        bearish_events = ['recession', 'market_crash', 'pandemic', 'economic_crisis', 'terrorism']
        if event_type in bearish_events:
            return 'down'
        elif event_type in ['cyber_attack', 'geopolitical']:
            return 'volatile'
        else:
            return 'uncertain'
