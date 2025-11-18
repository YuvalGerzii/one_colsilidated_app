"""
Short Selling Opportunity Detector (V4.0)

Identifies profitable short selling opportunities during extreme events.
Based on 2025 market conditions and hedge fund short strategies.

Key short strategies:
- Event-driven shorts (earnings misses, guidance cuts)
- Sector rotation shorts (falling sectors)
- Technical breakdown shorts (support breaks)
- Fundamental deterioration shorts (margin compression)
- Pair trades (long/short relative value)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ShortStrategy(Enum):
    """Short selling strategy types"""
    OUTRIGHT_SHORT = "outright_short"
    PAIR_TRADE = "pair_trade"
    SECTOR_SHORT = "sector_short"
    INDEX_SHORT = "index_short"
    PUT_OPTIONS = "put_options"
    INVERSE_ETF = "inverse_etf"
    SHORT_ETF_BASKET = "short_etf_basket"


@dataclass
class ShortOpportunity:
    """Short selling opportunity"""
    ticker: str
    strategy: ShortStrategy
    entry_price: float
    target_price: float
    stop_loss: float
    expected_return: float  # %
    risk_reward_ratio: float
    time_horizon: str  # days
    conviction_level: str  # low, medium, high
    short_thesis: str
    catalysts: List[str]
    risks: List[str]
    borrow_cost: float  # Annual % cost to borrow shares
    short_interest_ratio: float  # Days to cover
    technical_breakdown: str
    fundamental_weakness: str


@dataclass
class PairTrade:
    """Long/short pair trade"""
    long_ticker: str
    short_ticker: str
    hedge_ratio: float  # shares short / shares long
    expected_spread_move: float  # %
    rationale: str
    correlation: float
    beta_neutral: bool


class ShortSellingDetector:
    """
    Detects short selling opportunities during extreme events.
    Focuses on asymmetric risk/reward with strong catalysts.
    """

    def __init__(self):
        """Initialize short selling detector"""

        # Sectors vulnerable by event type
        self.vulnerable_sectors = {
            'recession': ['XLY', 'XLF', 'XHB', 'XRT'],  # Consumer Disc, Financials, Homebuilders, Retail
            'inflation': ['XLK', 'XLY', 'ARKK'],  # Tech, Consumer Disc, Growth
            'interest_rate_hike': ['XLU', 'XLRE', 'TLT'],  # Utilities, Real Estate, Bonds
            'pandemic': ['XLB', 'XLE', 'IYT'],  # Materials, Energy, Transportation
            'geopolitical': ['EWG', 'EWU', 'FXI'],  # Affected countries
            'cyber_attack': ['XLF', 'FINX'],  # Financials if banking attack
            'economic_crisis': ['XLF', 'GS', 'MS', 'BAC'],  # Financial stocks
        }

        # High-beta / risky names vulnerable in downturns
        self.high_beta_targets = [
            'TSLA', 'NVDA', 'AMD', 'COIN', 'ROKU', 'ZM',  # High growth tech
            'ARKK', 'SARK',  # Innovation ETFs
            'Unprofitable tech with high valuations'
        ]

        # Short interest data (example - would be real-time in production)
        self.short_interest = {
            'TSLA': 3.2,  # Days to cover
            'GME': 15.0,  # High short interest - squeeze risk
            'AMC': 12.0,
        }

    def identify_short_opportunities(
        self,
        event_type: str,
        event_data: Dict,
        market_conditions: Optional[Dict] = None
    ) -> Dict:
        """
        Identify short selling opportunities for the event

        Args:
            event_type: Type of extreme event
            event_data: Event details
            market_conditions: Current market data

        Returns:
            Short opportunity recommendations
        """

        severity = event_data.get('severity', 3)

        # Generate different types of short opportunities
        opportunities = []

        # 1. Sector shorts (ETF level)
        sector_shorts = self._generate_sector_shorts(event_type, severity)
        opportunities.extend(sector_shorts)

        # 2. Individual stock shorts (high conviction)
        stock_shorts = self._generate_stock_shorts(event_type, event_data)
        opportunities.extend(stock_shorts)

        # 3. Index shorts (market-wide decline expected)
        if severity >= 4:
            index_shorts = self._generate_index_shorts(severity, market_conditions)
            opportunities.extend(index_shorts)

        # 4. Pair trades (long/short relative value)
        pair_trades = self._generate_pair_trades(event_type, event_data)

        # 5. Options-based shorts (put buying, put spreads)
        options_shorts = self._generate_options_shorts(event_type, severity)
        opportunities.extend(options_shorts)

        # Risk analysis
        risk_analysis = self._analyze_short_risks(opportunities, market_conditions)

        # Execution plan
        execution = self._create_short_execution_plan(opportunities, severity)

        return {
            'opportunities': opportunities[:10],  # Top 10
            'pair_trades': pair_trades[:5],
            'risk_analysis': risk_analysis,
            'execution_plan': execution,
            'position_sizing': self._calculate_position_sizing(opportunities, severity),
            'borrow_costs': self._estimate_borrow_costs(opportunities),
            'squeeze_risk_assessment': self._assess_squeeze_risk(opportunities)
        }

    def _generate_sector_shorts(self, event_type: str, severity: int) -> List[ShortOpportunity]:
        """Generate sector-level short opportunities"""

        shorts = []
        vulnerable = self.vulnerable_sectors.get(event_type, [])

        for sector_etf in vulnerable[:3]:  # Top 3 most vulnerable
            shorts.append(ShortOpportunity(
                ticker=sector_etf,
                strategy=ShortStrategy.SECTOR_SHORT,
                entry_price=100.0,  # Placeholder
                target_price=85.0,   # -15% expected
                stop_loss=105.0,     # -5% stop
                expected_return=-15.0,
                risk_reward_ratio=3.0,  # 15% gain vs 5% loss
                time_horizon='30-90 days',
                conviction_level='high',
                short_thesis=f"{sector_etf} sector disproportionately impacted by {event_type}. Historical precedent shows {sector_etf} underperforms broad market by 10-20% during similar events.",
                catalysts=[
                    f'{event_type} disrupts sector fundamentals',
                    'Earnings downgrades expected',
                    'Sector rotation out of high-risk areas',
                    'Institutional selling pressure'
                ],
                risks=[
                    'Short squeeze if market rallies',
                    'Sector-specific positive catalyst',
                    'Borrow costs increase',
                    'ETF rebalancing can cause short-term squeezes'
                ],
                borrow_cost=0.5,  # 0.5% annualized for ETFs
                short_interest_ratio=1.5,  # ETFs typically low short interest
                technical_breakdown='Support break at previous crisis lows',
                fundamental_weakness=f'Sector earnings expected to decline 15-25% due to {event_type}'
            ))

        return shorts

    def _generate_stock_shorts(self, event_type: str, event_data: Dict) -> List[ShortOpportunity]:
        """Generate individual stock short opportunities"""

        shorts = []

        # Example: Recession → short cyclicals
        if event_type in ['recession', 'economic_crisis']:
            # Consumer discretionary stocks
            shorts.append(ShortOpportunity(
                ticker='PTON (Peloton - example)',
                strategy=ShortStrategy.OUTRIGHT_SHORT,
                entry_price=10.0,
                target_price=6.0,   # -40%
                stop_loss=11.5,     # -15%
                expected_return=-40.0,
                risk_reward_ratio=2.7,
                time_horizon='60-120 days',
                conviction_level='high',
                short_thesis='Consumer discretionary spending collapses in recession. PTON has high debt, unprofitable, and relies on discretionary spending. Previous recessions saw similar companies decline 50-70%.',
                catalysts=[
                    'Recession reduces discretionary spending',
                    'High debt burden becomes unsustainable',
                    'Potential bankruptcy risk',
                    'Margin compression from promotional activity',
                    'Subscriber churn accelerates'
                ],
                risks=[
                    'Acquisition rumors',
                    'Restructuring success',
                    'Better-than-expected earnings',
                    'Short squeeze (current SI: 20%)'
                ],
                borrow_cost=8.0,  # 8% annualized - hard to borrow
                short_interest_ratio=6.5,
                technical_breakdown='Death cross (50 DMA < 200 DMA), broke key support at $8',
                fundamental_weakness='Negative FCF, declining revenue, high cash burn rate'
            ))

        # Inflation → short unprofitable tech
        if event_type == 'inflation':
            shorts.append(ShortOpportunity(
                ticker='Unprofitable SaaS (ARK Innovation ETF as proxy)',
                strategy=ShortStrategy.SHORT_ETF_BASKET,
                entry_price=50.0,
                target_price=35.0,   # -30%
                stop_loss=55.0,      # -10%
                expected_return=-30.0,
                risk_reward_ratio=3.0,
                time_horizon='90-180 days',
                conviction_level='high',
                short_thesis='Rising rates kill unprofitable growth stocks. DCF valuation drops 30-50% when discount rates rise from 5% to 8%. ARKK = basket of high duration, unprofitable tech.',
                catalysts=[
                    'Fed continues hiking rates',
                    'Higher discount rates compress valuations',
                    'Funding dries up for unprofitable companies',
                    'Forced seller ship from ETF outflows'
                ],
                risks=[
                    'Fed pivot to rate cuts',
                    'Tech rally on AI hype',
                    'Short covering rallies',
                    'Cathie Wood buying the dip'
                ],
                borrow_cost=2.5,
                short_interest_ratio=3.0,
                technical_breakdown='Multi-year downtrend, below all major moving averages',
                fundamental_weakness='Portfolio companies burn cash, need external financing in tough environment'
            ))

        # Cyber attack → short affected companies
        if event_type == 'cyber_attack':
            shorts.append(ShortOpportunity(
                ticker='Target company / sector',
                strategy=ShortStrategy.OUTRIGHT_SHORT,
                entry_price=100.0,
                target_price=70.0,   # -30%
                stop_loss=108.0,     # -8%
                expected_return=-30.0,
                risk_reward_ratio=3.75,
                time_horizon='14-60 days',
                conviction_level='medium',
                short_thesis='Cyber breach leads to: (1) Immediate remediation costs, (2) Customer trust erosion, (3) Regulatory fines, (4) Class action lawsuits. Equifax dropped 35% after 2017 breach.',
                catalysts=[
                    'Breach disclosure and extent of damage',
                    'Lawsuits and regulatory investigations',
                    'Customer churn',
                    'Credit rating downgrade',
                    'Quarterly earnings miss due to costs'
                ],
                risks=[
                    'Breach contained quickly',
                    'Insurance covers most costs',
                    'Market already priced in bad news',
                    'Management executes turnaround'
                ],
                borrow_cost=5.0,
                short_interest_ratio=4.0,
                technical_breakdown='Gap down on breach news, subsequent lower highs',
                fundamental_weakness='One-time costs $100M+, ongoing revenue impact 5-10%'
            ))

        return shorts

    def _generate_index_shorts(self, severity: int, market_conditions: Optional[Dict]) -> List[ShortOpportunity]:
        """Generate index-level short opportunities"""

        shorts = []

        if severity >= 4:
            # SPY short via put options or inverse ETF
            shorts.append(ShortOpportunity(
                ticker='SPY / SH (inverse ETF)',
                strategy=ShortStrategy.INDEX_SHORT,
                entry_price=450.0,
                target_price=380.0,  # -15% market decline
                stop_loss=465.0,     # -3% stop
                expected_return=-15.0,
                risk_reward_ratio=5.0,
                time_horizon='30-90 days',
                conviction_level='high' if severity >= 5 else 'medium',
                short_thesis=f'Systemic crisis (severity {severity}/5) triggers broad market decline. Historical precedent: 2008 (-37%), 2020 (-34%), 2022 (-25%). Expect 15-25% drawdown.',
                catalysts=[
                    'Crisis escalation',
                    'Corporate earnings collapse',
                    'Recession confirmation',
                    'Fed policy mistake',
                    'Forced de-leveraging by institutions'
                ],
                risks=[
                    'Fed intervention (rate cuts, QE)',
                    'Fiscal stimulus',
                    'Short-term oversold bounce',
                    'Index shorts = fighting the Fed'
                ],
                borrow_cost=0.3,  # Very low for SPY
                short_interest_ratio=1.0,
                technical_breakdown='SPY broke 200 DMA, death cross, RSI oversold bounce fading',
                fundamental_weakness='Forward P/E 22x vs 16x historical average in recessions'
            ))

            # QQQ short (Nasdaq) - higher beta
            shorts.append(ShortOpportunity(
                ticker='QQQ / PSQ (inverse)',
                strategy=ShortStrategy.INDEX_SHORT,
                entry_price=380.0,
                target_price=300.0,  # -21% decline
                stop_loss=395.0,     # -4% stop
                expected_return=-21.0,
                risk_reward_ratio=5.25,
                time_horizon='30-90 days',
                conviction_level='high',
                short_thesis='Tech-heavy QQQ declines 1.3-1.5x SPY in bear markets (higher beta). Current P/E 30x vs 18x in 2022 lows. Significant downside.',
                catalysts=[
                    'Big tech earnings disappointment',
                    'Multiple compression on rate hikes',
                    'AI bubble concerns',
                    'Antitrust regulatory pressure'
                ],
                risks=[
                    'Tech resilience (Mag 7 strength)',
                    'AI hype continues',
                    'Short squeeze from oversold',
                    'Relative strength to SPY'
                ],
                borrow_cost=0.5,
                short_interest_ratio=1.2,
                technical_breakdown='Below 50 DMA, trend lower, rising volatility',
                fundamental_weakness='Valuation stretched vs historical bear market troughs'
            ))

        return shorts

    def _generate_pair_trades(self, event_type: str, event_data: Dict) -> List[PairTrade]:
        """Generate long/short pair trades"""

        pairs = []

        # Recession: Long defensives, Short cyclicals
        if event_type in ['recession', 'economic_crisis']:
            pairs.append(PairTrade(
                long_ticker='XLP (Consumer Staples)',
                short_ticker='XLY (Consumer Discretionary)',
                hedge_ratio=1.0,  # Equal dollar amounts
                expected_spread_move=15.0,  # XLP outperforms XLY by 15%
                rationale='Recession drives sector rotation. Consumers shift spending from discretionary to staples. XLP historically outperforms XLY by 10-20% in recessions.',
                correlation=0.75,  # Moderately correlated
                beta_neutral=True
            ))

            pairs.append(PairTrade(
                long_ticker='WMT (Walmart)',
                short_ticker='TGT (Target)',
                hedge_ratio=1.0,
                expected_spread_move=12.0,
                rationale='Walmart wins in recession (low-price leader). Target loses (middle class discretionary). Walmart margins stable, Target margins compress.',
                correlation=0.68,
                beta_neutral=True
            ))

        # Inflation: Long commodities, Short tech
        if event_type == 'inflation':
            pairs.append(PairTrade(
                long_ticker='XLE (Energy)',
                short_ticker='XLK (Technology)',
                hedge_ratio=1.0,
                expected_spread_move=20.0,
                rationale='Inflation favors real assets (energy) over financial assets (tech). Energy has pricing power, tech faces margin compression. 1970s playbook.',
                correlation=0.45,  # Low correlation = good pair
                beta_neutral=False  # This is a factor bet, not beta-neutral
            ))

        # Interest rates: Long financials, Short REITs
        if event_type == 'interest_rate_change':
            pairs.append(PairTrade(
                long_ticker='XLF (Financials)',
                short_ticker='XLRE (Real Estate)',
                hedge_ratio=1.0,
                expected_spread_move=10.0,
                rationale='Rising rates = wider NIM for banks (XLF gains). Rising rates = higher cap rates for REITs (XLRE loses). Inverse relationship.',
                correlation=0.40,
                beta_neutral=True
            ))

        return pairs

    def _generate_options_shorts(self, event_type: str, severity: int) -> List[ShortOpportunity]:
        """Generate options-based short strategies (put buying)"""

        shorts = []

        # Put options instead of outright short (defined risk)
        shorts.append(ShortOpportunity(
            ticker='SPY Put Options',
            strategy=ShortStrategy.PUT_OPTIONS,
            entry_price=450.0,  # SPY price
            target_price=400.0,  # -11%
            stop_loss=455.0,     # Exit if SPY rallies
            expected_return=-11.0,
            risk_reward_ratio=5.0,  # Put options offer 5-10x leverage
            time_horizon='30-60 DTE',
            conviction_level='high',
            short_thesis='Put options provide leveraged short exposure with defined risk (premium paid). Better risk/reward than outright short. If SPY drops 10%, puts can return 50-100%.',
            catalysts=[
                'Market decline',
                'Volatility spike (vega gain)',
                'Safe haven flight'
            ],
            risks=[
                'Time decay (theta)',
                'Implied volatility crush',
                '100% loss if market rallies',
                'Options premium is expensive after event'
            ],
            borrow_cost=0.0,  # No borrow cost for options
            short_interest_ratio=0.0,
            technical_breakdown='Puts gain value as SPY declines',
            fundamental_weakness='N/A - pure derivative play'
        ))

        return shorts

    def _analyze_short_risks(self, opportunities: List[ShortOpportunity], market_conditions: Optional[Dict]) -> Dict:
        """Analyze risks specific to short selling"""

        return {
            'short_squeeze_risk': {
                'definition': 'Shorts forced to cover when price rises, causing accelerated buying',
                'high_risk_names': [opp.ticker for opp in opportunities if opp.short_interest_ratio > 5.0],
                'mitigation': [
                    'Avoid names with SI > 20% of float',
                    'Use tight stop losses (8-10%)',
                    'Reduce position size on high SI names',
                    'Consider put options instead of outright shorts'
                ]
            },
            'unlimited_loss_potential': {
                'risk': 'Shorting has unlimited upside risk (stock can go to infinity)',
                'mitigation': [
                    'Always use stop losses',
                    'Max position size: 3-5% per short',
                    'Hedge with long positions (pair trades)',
                    'Use options for defined risk'
                ]
            },
            'borrow_costs': {
                'risk': 'High borrow costs eat into returns (some stocks 20%+ annually)',
                'mitigation': [
                    'Monitor borrow rates daily',
                    'Exit if borrow costs spike above 10%',
                    'Use ETFs (lower borrow costs) instead of individual stocks',
                    'Factor borrow costs into P&L projections'
                ]
            },
            'market_reversal_risk': {
                'risk': f'Market can reverse quickly on Fed intervention, stimulus, etc.',
                'mitigation': [
                    'Scale into shorts over time (not all at once)',
                    'Take profits at targets (don\'t get greedy)',
                    'Reduce exposure if market technicals improve',
                    'Monitor Fed commentary closely'
                ]
            },
            'regulatory_risk': {
                'risk': 'Short selling bans during extreme crises (2008, 2020)',
                'mitigation': [
                    'Diversify across geographies',
                    'Use put options (not typically banned)',
                    'Monitor regulatory commentary',
                    'Have exit plan if ban rumors emerge'
                ]
            }
        }

    def _create_short_execution_plan(self, opportunities: List[ShortOpportunity], severity: int) -> Dict:
        """Create execution plan for short trades"""

        return {
            'entry_strategy': {
                'timing': 'Scale in over 1-2 weeks' if severity < 4 else 'Immediate entry on severe events',
                'size': 'Start with 1/3 position, add on strength',
                'price': 'Use limit orders, avoid chasing. Enter on bounces/strength.',
                'checklist': [
                    '✓ Confirm borrow availability',
                    '✓ Check short interest ratio (< 10 days ideal)',
                    '✓ Set stop loss at entry',
                    '✓ Calculate position size (max 3-5%)',
                    '✓ Monitor for squeeze risk'
                ]
            },
            'position_management': {
                'initial_stop': '7-10% above entry',
                'trailing_stop': 'Move to breakeven after 5% profit, then trail 5%',
                'profit_taking': 'Take 1/3 at 10% profit, 1/3 at 20%, let 1/3 run',
                'adding': 'Add on strength if thesis intact, max 2x original size'
            },
            'exit_strategy': {
                'target_hit': 'Exit 50-75% at target, trail rest',
                'stop_hit': 'Exit immediately, no exceptions',
                'thesis_broken': 'Exit even if not at stop (e.g., Fed pivot, stimulus)',
                'time_stop': f'Exit after {90 if severity >= 4 else 60} days if no progress',
                'squeeze_signs': [
                    'Exit if price rises >5% on heavy volume',
                    'Exit if borrow costs spike >15%',
                    'Exit if short interest drops rapidly (covering)'
                ]
            }
        }

    def _calculate_position_sizing(self, opportunities: List[ShortOpportunity], severity: int) -> Dict:
        """Calculate position sizing for shorts"""

        # More aggressive sizing in severe events
        base_allocation = 20 if severity >= 4 else 15  # % of portfolio in shorts

        return {
            'total_short_allocation': f'{base_allocation}% of portfolio',
            'max_single_short': '3-5% of portfolio',
            'max_sector_short': '8% of portfolio',
            'recommended_allocation': {
                'high_conviction_shorts': f'{base_allocation * 0.5}% (50% of short book)',
                'medium_conviction_shorts': f'{base_allocation * 0.3}% (30% of short book)',
                'pair_trades': f'{base_allocation * 0.2}% (20% of short book)'
            },
            'diversification': [
                'At least 5 different shorts',
                'No more than 3 in same sector',
                'Mix of ETFs, stocks, and options',
                'Include pair trades for hedging'
            ],
            'leverage': 'Avoid leverage on shorts - unlimited risk'
        }

    def _estimate_borrow_costs(self, opportunities: List[ShortOpportunity]) -> Dict:
        """Estimate total borrow costs for short positions"""

        total_borrow_cost = sum(opp.borrow_cost for opp in opportunities) / len(opportunities) if opportunities else 0

        return {
            'average_borrow_cost': f'{total_borrow_cost:.1f}% annually',
            'monthly_cost': f'{total_borrow_cost / 12:.2f}%',
            'impact_on_returns': f'Reduces returns by ~{total_borrow_cost:.1f}% per year',
            'mitigation': [
                'Prefer ETFs (0.3-1% borrow) over individual stocks (5-20%)',
                'Use put options (no borrow cost) for high-cost names',
                'Monitor borrow costs daily - they can spike in crises',
                'Exit shorts if borrow > 15% (eats all alpha)'
            ]
        }

    def _assess_squeeze_risk(self, opportunities: List[ShortOpportunity]) -> Dict:
        """Assess short squeeze risk across positions"""

        high_squeeze_risk = [
            opp for opp in opportunities
            if opp.short_interest_ratio > 5.0  # > 5 days to cover
        ]

        return {
            'high_risk_count': len(high_squeeze_risk),
            'high_risk_names': [opp.ticker for opp in high_squeeze_risk],
            'squeeze_indicators': {
                'short_interest_ratio': '> 5 days = high risk',
                'short_interest_pct_float': '> 20% = very high risk',
                'price_action': 'Sharp rises on high volume = squeeze starting',
                'social_media': 'Reddit/Twitter chatter = retail squeeze target'
            },
            'historical_squeezes': [
                'GME (Jan 2021): 140% SI → +1000% squeeze',
                'VW (2008): Porsche corner → +400% squeeze',
                'TSLA (2020): Persistent shorts squeezed → +700%'
            ],
            'protection': [
                'AVOID names with SI > 20% of float',
                'Use wide stops (10-15%) on high SI names',
                'Reduce position size by 50% if SI > 10 days to cover',
                'Monitor daily for unusual volume/price action',
                'Have mental stop at -15% regardless of technical stop'
            ]
        }
