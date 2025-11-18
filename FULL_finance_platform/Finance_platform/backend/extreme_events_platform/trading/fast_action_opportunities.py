"""
Fast-Action Opportunities Module (V4.0)

Identifies time-critical trading opportunities during extreme events.
These are asymmetric, high-conviction trades that require immediate action.

Based on 2025 hedge fund intelligence:
- 0-24 hour windows for optimal entry
- Volatility spikes and mispricings
- Forced liquidations and panic selling
- Gap fills and technical dislocations
- First-mover advantages
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class UrgencyLevel(Enum):
    """Trade urgency classification"""
    CRITICAL = "critical"      # 0-6 hours
    URGENT = "urgent"          # 6-24 hours
    HIGH = "high"              # 1-3 days
    MEDIUM = "medium"          # 3-7 days


@dataclass
class FastActionTrade:
    """Time-sensitive trading opportunity"""
    name: str
    urgency: UrgencyLevel
    time_window: str  # When to act
    expected_duration: str  # How long opportunity lasts
    entry_price: str
    target_price: str
    max_position_size: str  # % of portfolio
    expected_return: str
    win_probability: float
    trade_setup: str
    execution_instructions: List[str]
    catalysts: List[str]
    why_fast_action: str  # Why speed matters
    risks: List[str]
    historical_precedent: str


@dataclass
class MarketMispricing:
    """Temporary market mispricing"""
    asset: str
    fair_value: float
    current_price: float
    mispricing_pct: float
    reason_for_mispricing: str
    expected_convergence_time: str
    arbitrage_strategy: str


class FastActionOpportunities:
    """
    Identifies time-critical opportunities during extreme events.
    Focus: Act fast or miss the opportunity entirely.
    """

    def __init__(self):
        """Initialize fast action analyzer"""

        # Historical opportunities by event type
        self.historical_patterns = {
            'market_crash': {
                'vix_spike': 'VIX calls return 3-10x in first 24 hours',
                'put_options': 'ATM puts bought at open return 50-200% same day',
                'inverse_etfs': 'SPXU, SQQQ gain 10-20% in crash days',
                'safe_havens': 'Gold, treasuries gap up - buy on first dip'
            },
            'flash_crash': {
                'snap_back': '5-15 minute window to buy the dip before recovery',
                'mean_reversion': 'Stocks down >10% in minutes often recover 50-80%',
                'liquidity_gaps': 'Wide bid-ask spreads create arbitrage'
            },
            'earnings_shock': {
                'options_explosion': 'Options bought pre-announcement return 200-500%',
                'sector_contagion': 'Similar companies gap down, some unjustified',
                'pair_trades': 'Short weak peer, long strong peer'
            }
        }

    def identify_fast_opportunities(
        self,
        event_type: str,
        event_data: Dict,
        time_since_event: int = 0  # Hours since event started
    ) -> Dict:
        """
        Identify fast-action opportunities

        Args:
            event_type: Type of extreme event
            event_data: Event details
            time_since_event: Hours since event began

        Returns:
            Time-critical trading opportunities
        """

        severity = event_data.get('severity', 3)
        opportunities = []

        # Window 1: Immediate (0-6 hours) - Crisis begins
        if time_since_event < 6:
            immediate = self._generate_immediate_opportunities(event_type, severity)
            opportunities.extend(immediate)

        # Window 2: First day (6-24 hours) - Initial panic
        if time_since_event < 24:
            first_day = self._generate_first_day_opportunities(event_type, severity)
            opportunities.extend(first_day)

        # Window 3: First week (1-7 days) - Market digests
        if time_since_event < 168:  # 7 days in hours
            first_week = self._generate_first_week_opportunities(event_type, severity)
            opportunities.extend(first_week)

        # Identify mispricings
        mispricings = self._identify_mispricings(event_type, event_data, time_since_event)

        # Volatility arbitrage
        vol_arb = self._identify_volatility_arbitrage(event_type, severity)

        # Forced liquidation opportunities
        liquidations = self._identify_liquidation_opportunities(event_type, severity)

        return {
            'critical_opportunities': [o for o in opportunities if o.urgency == UrgencyLevel.CRITICAL],
            'urgent_opportunities': [o for o in opportunities if o.urgency == UrgencyLevel.URGENT],
            'all_opportunities': opportunities,
            'mispricings': mispricings,
            'volatility_arbitrage': vol_arb,
            'forced_liquidations': liquidations,
            'execution_timeline': self._create_execution_timeline(opportunities),
            'first_mover_advantages': self._identify_first_mover_advantages(event_type)
        }

    def _generate_immediate_opportunities(self, event_type: str, severity: int) -> List[FastActionTrade]:
        """Generate 0-6 hour opportunities (most time-critical)"""

        opportunities = []

        # 1. VIX explosion trade (most time-sensitive)
        if severity >= 4:
            opportunities.append(FastActionTrade(
                name='VIX Call Explosion Play',
                urgency=UrgencyLevel.CRITICAL,
                time_window='0-6 hours from event start',
                expected_duration='Same day (0DTE), or 30 DTE for longer play',
                entry_price='VIX 18-25 → Buy VIX 30/40 call spread',
                target_price='VIX 40-60 (crisis peak)',
                max_position_size='1-3% of portfolio',
                expected_return='+100% to +500% if VIX spikes to 50+',
                win_probability=0.60,
                trade_setup='Buy VIX call spreads before volatility explosion fully prices in. VIX calls have convexity - returns accelerate as VIX rises.',
                execution_instructions=[
                    '✓ Act within first 6 hours - after that, IV premium too expensive',
                    '✓ Use VIX call spreads (30/40 or 40/50) to cap cost',
                    '✓ Buy 30-45 DTE options for time to work',
                    '✓ Entry: VIX still under 25',
                    '✓ Exit: VIX > 40 (take profits), or decay after 2 weeks',
                    '✓ Size: 1-2% of portfolio (leveraged but defined risk)'
                ],
                catalysts=[
                    'Fear and panic accelerate',
                    'Forced delever aging by hedge funds',
                    'Systematic CTA selling',
                    'Retail capitulation'
                ],
                why_fast_action='VIX calls are CHEAPEST in first 6 hours before market realizes severity. March 2020: VIX went 15→80 in 2 weeks. Calls bought early returned 10-20x. After day 1, IV too expensive.',
                risks=[
                    'Event contained quickly → VIX drops, total loss',
                    'Time decay if crisis slow-burn',
                    'IV crush after initial spike'
                ],
                historical_precedent='COVID March 2020: VIX 15→80 (VIX calls +1000%). Aug 2024 flash crash: VIX 15→65 in 24h (calls +800%).'
            ))

        # 2. ATM put options on indices (6-24 hour window)
        opportunities.append(FastActionTrade(
            name='At-The-Money Put Options on SPY/QQQ',
            urgency=UrgencyLevel.CRITICAL,
            time_window='First 24 hours',
            expected_duration='20-45 DTE options',
            entry_price='SPY ATM puts (strike = current price)',
            target_price='+50% to +200% if market drops 5-10%',
            max_position_size='2-4% of portfolio',
            expected_return='+50% to +200%',
            win_probability=0.55,
            trade_setup='ATM puts offer best gamma exposure. As market falls, delta increases, profits accelerate. Buy before IV spikes too high.',
            execution_instructions=[
                '✓ Buy within first market open after event',
                '✓ ATM strikes (50 delta)',
                '✓ 20-45 DTE expiration',
                '✓ Exit at 50-100% profit or -50% stop loss',
                '✓ Roll down strikes if market drops quickly'
            ],
            catalysts=[
                'Initial panic selling',
                'Margin calls and forced selling',
                'Safe haven flows out of equities'
            ],
            why_fast_action='IV explodes quickly. Puts bought at 9:30am can be 30-50% more expensive by 11am. First hour is golden window.',
            risks=[
                'Market rallies on intervention',
                'Puts decay rapidly (theta)',
                'Overpay if bought after IV spike'
            ],
            historical_precedent='Feb 2020: SPY puts bought at open on first down day returned 150% in 2 weeks.'
        ))

        # 3. Inverse ETFs (SPXU, SQQQ, SH) - simplest short exposure
        if severity >= 3:
            opportunities.append(FastActionTrade(
                name='3x Inverse ETFs (SPXU, SQQQ)',
                urgency=UrgencyLevel.URGENT,
                time_window='0-24 hours',
                expected_duration='1-7 days (short-term trade)',
                entry_price='Buy on market open',
                target_price='+15% to +30% in 1-3 days',
                max_position_size='3-5% of portfolio',
                expected_return='+15% to +30% over 1-5 days',
                win_probability=0.65,
                trade_setup='3x leveraged inverse ETFs (SPXU = 3x short S&P 500). Simple, liquid, no options knowledge required. Act fast before rally.',
                execution_instructions=[
                    '✓ Buy at market open day 1',
                    '✓ SPXU (3x short S&P), SQQQ (3x short Nasdaq)',
                    '✓ Scale in: 50% at open, 50% on any bounce',
                    '✓ Exit target: +20-30%, or after 3-5 days',
                    '✓ Stop loss: -10% (market rallies)'
                ],
                catalysts=[
                    'Continued selling pressure',
                    'Negative news flow',
                    'Technical breakdown'
                ],
                why_fast_action='Inverse ETFs decay over time (volatility drag). Best for 1-7 day trades. After first week, returns diminish. Strike fast.',
                risks=[
                    'Market reversal erases gains',
                    'Volatility decay over time',
                    'Daily rebalancing can cause tracking error',
                    '3x leverage = 3x losses if wrong'
                ],
                historical_precedent='March 2020: SPXU gained 60% in 2 weeks. Oct 2022 bear market: SPXU +40% over month.'
            ))

        return opportunities

    def _generate_first_day_opportunities(self, event_type: str, severity: int) -> List[FastActionTrade]:
        """Generate 6-24 hour opportunities"""

        opportunities = []

        # Safe haven rotation
        opportunities.append(FastActionTrade(
            name='Safe Haven Rotation (Gold, Treasuries, USD)',
            urgency=UrgencyLevel.URGENT,
            time_window='First 24 hours',
            expected_duration='1-4 weeks',
            entry_price='GLD (gold ETF), TLT (treasuries), UUP (USD)',
            target_price='+5% to +15% over 2-4 weeks',
            max_position_size='5-10% of portfolio',
            expected_return='+5% to +15%',
            win_probability=0.75,
            trade_setup='Flight to safety. Investors flee risky assets for safe havens. Buy on first dips after initial gap up.',
            execution_instructions=[
                '✓ Buy gold (GLD, IAU) on first pullback',
                '✓ Buy long-term treasuries (TLT) if rates falling',
                '✓ Buy USD (UUP) if global crisis',
                '✓ Entry: First intraday dip after initial surge',
                '✓ Exit: When risk-on returns (VIX < 20)'
            ],
            catalysts=[
                'Continued risk-off sentiment',
                'Flight to liquidity',
                'Central bank easing (boosts gold)'
            ],
            why_fast_action='Safe havens gap up on day 1. Best entry is first dip (10am-12pm). Waiting days means paying up 3-5%.',
            risks=[
                'Fake out - risk-on returns quickly',
                'Fed hikes (negative for gold)',
                'Dollar strength hurts gold'
            ],
            historical_precedent='March 2020: Gold +10%, TLT +15%, USD +5% in first month of COVID.'
        ))

        # Volatility term structure arbitrage
        opportunities.append(FastActionTrade(
            name='VIX Term Structure Inversion Arbitrage',
            urgency=UrgencyLevel.HIGH,
            time_window='24-72 hours',
            expected_duration='1-2 weeks',
            entry_price='Long front-month VIX, short back-month VIX',
            target_price='+20% to +50%',
            max_position_size='2-3% of portfolio',
            expected_return='+20% to +50%',
            win_probability=0.60,
            trade_setup='Crisis inverts VIX term structure (front > back). As crisis subsides, curve normalizes. Profit from convergence.',
            execution_instructions=[
                '✓ Enter when VIX front month > back month by 5+ points',
                '✓ Long UVIX (front month), short SVIX (back month)',
                '✓ Or: Buy VIX futures spread',
                '✓ Exit when term structure normalizes',
                '✓ Advanced strategy - requires futures knowledge'
            ],
            catalysts=[
                'Volatility mean reversion',
                'Crisis subsides',
                'Term structure normalization'
            ],
            why_fast_action='VIX term structure inverts quickly (day 1-2) and normalizes within 1-2 weeks. Miss the window = miss the trade.',
            risks=[
                'Crisis worsens → backwardation persists',
                'Contango returns too slowly',
                'Futures rollover costs'
            ],
            historical_precedent='Feb 2018 VIXpocalypse: Term structure trades made 30-50% in 1 week.'
        ))

        return opportunities

    def _generate_first_week_opportunities(self, event_type: str, severity: int) -> List[FastActionTrade]:
        """Generate 1-7 day opportunities"""

        opportunities = []

        # Mean reversion plays
        opportunities.append(FastActionTrade(
            name='Oversold Bounce - Mean Reversion',
            urgency=UrgencyLevel.MEDIUM,
            time_window='3-7 days after initial crash',
            expected_duration='5-15 days',
            entry_price='Quality stocks down 15-25% (oversold)',
            target_price='+8% to +15% bounce',
            max_position_size='5-8% of portfolio',
            expected_return='+8% to +15%',
            win_probability=0.70,
            trade_setup='After initial panic, quality stocks bounce 50-70% of decline. Buy technically oversold (RSI < 30) high-quality names.',
            execution_instructions=[
                '✓ Wait 3-5 days for initial panic to subside',
                '✓ Buy quality stocks: AAPL, MSFT, GOOGL down 15-20%',
                '✓ Technical: RSI < 30, MACD oversold',
                '✓ Entry: Bullish reversal candle or first green day',
                '✓ Exit: +10-15% or resistance level',
                '✓ Stop: Below recent low (-7%)'
            ],
            catalysts=[
                'Short covering',
                'Dip buying returns',
                'Technical oversold bounce',
                'Fed intervention hopes'
            ],
            why_fast_action='Best entries are days 3-7. After week 1, either already bounced or still falling (catch falling knife). Sweet spot is mid-week 1.',
            risks=[
                'Dead cat bounce - selling resumes',
                'Crisis worsens',
                'Fundamentals deteriorate'
            ],
            historical_precedent='March 2020: AAPL down 30% → bounced 20% in week 2. Sept 2022: Meta down 25% → bounced 12% next week.'
        ))

        # Sector rotation winners
        opportunities.append(FastActionTrade(
            name='Sector Rotation into Defensives',
            urgency=UrgencyLevel.HIGH,
            time_window='Week 1 of crisis',
            expected_duration='1-3 months',
            entry_price='XLP (staples), XLU (utilities), XLV (healthcare)',
            target_price='+5% to +12% over 1-2 months',
            max_position_size='8-12% of portfolio',
            expected_return='+5% to +12%',
            win_probability=0.80,
            trade_setup='Sector rotation: out of cyclicals, into defensives. Staples, utilities, healthcare outperform in downturns.',
            execution_instructions=[
                '✓ Buy defensive ETFs: XLP, XLU, XLV',
                '✓ Or: Individual stocks (PG, JNJ, NEE)',
                '✓ Entry: Week 1 before rotation fully priced',
                '✓ Hold 1-3 months until cycle turns',
                '✓ Pair with short on cyclicals (XLY, XLF)'
            ],
            catalysts=[
                'Flight to safety',
                'Recession fears',
                'Defensive earnings hold up better'
            ],
            why_fast_action='Sector rotation happens weeks 1-2. By week 3, defensives already expensive vs cyclicals. Enter early for best risk/reward.',
            risks=[
                'Defensive valuations stretch',
                'Yield curve steepens (bad for utilities)',
                'Economic recovery comes faster than expected'
            ],
            historical_precedent='2022 bear: XLP +2% while SPY -18%. 2020 COVID: XLP -8% while SPY -35%.'
        ))

        return opportunities

    def _identify_mispricings(self, event_type: str, event_data: Dict, time_since_event: int) -> List[MarketMispricing]:
        """Identify temporary mispricings from panic selling"""

        mispricings = []

        # Example: Baby thrown out with bathwater
        if time_since_event < 48:  # First 2 days
            mispricings.append(MarketMispricing(
                asset='Quality stocks sold in panic',
                fair_value=100.0,
                current_price=82.0,
                mispricing_pct=-18.0,
                reason_for_mispricing='Indiscriminate selling. ETF redemptions, forced liquidations, margin calls. Good companies sold with bad.',
                expected_convergence_time='1-3 weeks',
                arbitrage_strategy='Buy quality names down 15-25% with strong balance sheets, positive FCF, low debt. Examples: AAPL, MSFT, V, MA down 20%+ = buy signal.'
            ))

        # Liquidity gaps in small/mid caps
        if time_since_event < 72:
            mispricings.append(MarketMispricing(
                asset='Small/mid cap stocks',
                fair_value=50.0,
                current_price=38.0,
                mispricing_pct=-24.0,
                reason_for_mispricing='Liquidity dries up in crisis. Small caps hit harder than fundamentals warrant. Bid-ask spreads widen 5-10x.',
                expected_convergence_time='2-6 weeks',
                arbitrage_strategy='Buy highest quality small caps (positive earnings, low debt) at 20-30% discounts. Use limit orders. Wait for liquidity to return.'
            ))

        # Options mispricing (IV skew)
        mispricings.append(MarketMispricing(
            asset='Out-of-the-money options',
            fair_value=5.0,
            current_price=12.0,
            mispricing_pct=+140.0,
            reason_for_mispricing='Fear premium. OTM puts and calls trade at inflated IV percentiles (90th+). Market overestimates tail risk.',
            expected_convergence_time='1-2 weeks',
            arbitrage_strategy='Sell OTM put spreads (collect premium on inflated IV). Sell iron condors. Short vol plays once IV > 80th percentile.'
        ))

        return mispricings

    def _identify_volatility_arbitrage(self, event_type: str, severity: int) -> List[Dict]:
        """Identify volatility arbitrage opportunities"""

        vol_arb = []

        # Dispersion trades
        vol_arb.append({
            'strategy': 'Dispersion Trade (Long single-stock vol, Short index vol)',
            'setup': 'Crisis breaks correlations. Individual stocks move more than index. Long AAPL/MSFT/GOOGL straddles, short SPY straddle.',
            'expected_return': '+25% to +60% over 2-4 weeks',
            'rationale': '2020: correlations dropped from 0.85 to 0.45. Dispersion trades made 40-80%. Stock-specific vol > index vol.',
            'time_window': 'Weeks 1-3 of crisis',
            'risk': 'Correlations spike back to 1.0 in extreme systemic crises'
        })

        # Volatility term structure
        vol_arb.append({
            'strategy': 'VIX Curve Flattening',
            'setup': 'Front-month VIX explodes, back months lag. Short the spread. Profit as curve normalizes.',
            'expected_return': '+20% to +40% in 1-2 weeks',
            'rationale': 'VIX term structure inverts in crisis (front > back). Always normalizes within 2-3 weeks as fear subsides.',
            'time_window': 'Days 2-10',
            'risk': 'Crisis persists longer than expected'
        })

        # Relative vol arbitrage
        vol_arb.append({
            'strategy': 'Relative Volatility: QQQ vs SPY',
            'setup': 'QQQ IV spikes more than SPY IV in tech-driven crises. Long SPY vol, short QQQ vol when spread is wide.',
            'expected_return': '+15% to +30%',
            'rationale': 'QQQ/SPY vol spread mean reverts. Normal spread: 1.2x. Crisis: 1.5-1.8x. Trade convergence.',
            'time_window': 'Weeks 1-2',
            'risk': 'Sector-specific issues keep tech vol elevated'
        })

        return vol_arb

    def _identify_liquidation_opportunities(self, event_type: str, severity: int) -> List[Dict]:
        """Identify opportunities from forced liquidations"""

        liquidations = []

        # Margin call selling
        liquidations.append({
            'trigger': 'Margin Calls & Forced Deleveraging',
            'opportunity': 'Buy quality stocks hit by forced selling',
            'timing': '24-72 hours after initial crash (margin calls T+2)',
            'indicators': [
                'High-volume down days',
                'Good stocks down >10% on no news',
                'NYSE margin debt data spikes'
            ],
            'strategy': 'Identify forced sellers (not fundamental). Buy what they dump. Exit when selling pressure ends (volume normalizes).',
            'historical': 'Oct 1987: Margin-call selling day 2-3. Buying day 3-4 = best entries. 2020 March: Day 3-5 = forced selling, then bounce.'
        })

        # ETF arbitrage
        liquidations.append({
            'trigger': 'ETF Redemptions Forcing Stock Sales',
            'opportunity': 'Buy underlying stocks cheaper than NAV',
            'timing': 'Same day as large ETF outflows',
            'indicators': [
                'QQQ, SPY, ARKK massive outflows',
                'Stocks trade below ETF NAV (discount)',
                'End-of-day selling pressure'
            ],
            'strategy': 'Buy individual stocks trading below their ETF-implied value. Arbitrage the disconnect. Sell when NAV converges.',
            'historical': '2022 ARKK outflows: Underlying stocks hit harder than NAV. Arb opportunity 1-2%.'
        })

        # Risk-parity unwind
        liquidations.append({
            'trigger': 'Risk Parity & Volatility Targeting Funds Selling',
            'opportunity': 'Buy bonds and stocks dumped mechanically',
            'timing': 'Days 1-5 of volatility spike',
            'indicators': [
                'VIX spike >40',
                'Both stocks AND bonds selling',
                'High correlation across assets'
            ],
            'strategy': 'Risk-parity funds must sell when volatility rises (mechanical, not fundamental). Buy what they dump. 2018 Feb: Risk-parity selling created opportunity.',
            'historical': 'Feb 2018 VIX spike: Risk parity sold $200B in 3 days. Best buying opp in years.'
        })

        return liquidations

    def _create_execution_timeline(self, opportunities: List[FastActionTrade]) -> Dict:
        """Create hour-by-hour execution timeline"""

        return {
            'hour_0_to_6': {
                'priority': 'CRITICAL - Act immediately or lose opportunity',
                'trades': [
                    '1. VIX calls (before IV spikes)',
                    '2. Inverse ETFs (SPXU, SQQQ)',
                    '3. Gold/TLT gap downs (buy dip)'
                ],
                'mindset': 'Speed > precision. Act decisively. Use market orders if needed.'
            },
            'hour_6_to_24': {
                'priority': 'URGENT - Window closing',
                'trades': [
                    '1. ATM put options',
                    '2. Safe haven entry on pullbacks',
                    '3. Sector rotation shorts (XLY, XLF)'
                ],
                'mindset': 'Still good opportunities but IV rising. Use limit orders, be patient for fills.'
            },
            'day_2_to_3': {
                'priority': 'HIGH - Good risk/reward still available',
                'trades': [
                    '1. Margin call opportunities (forced selling)',
                    '2. ETF arbitrage',
                    '3. VIX term structure trades'
                ],
                'mindset': 'Market stabilizing. Look for mispricings from forced flows.'
            },
            'day_3_to_7': {
                'priority': 'MEDIUM - Tactical trades',
                'trades': [
                    '1. Oversold bounce (mean reversion)',
                    '2. Sector rotation longs (defensives)',
                    '3. Dispersion trades'
                ],
                'mindset': 'Initial panic over. Focus on technical setups and value.'
            }
        }

    def _identify_first_mover_advantages(self, event_type: str) -> Dict:
        """Identify why being first matters"""

        return {
            'advantages': [
                'VIX options cheapest in first 6 hours (IV hasn\'t spiked yet)',
                'Safe havens best entry on first dip (gold, treasuries gap up, then pull back)',
                'Quality stocks at max discount day 1-3 (before value buyers step in)',
                'Short covering rallies start day 3-5 (early shorts make 2-3x late shorts)',
                'Margin call opportunities day 2-3 (forced sellers, not fundamental)',
                'Volatility trades best before term structure normalizes (1-2 week window)'
            ],
            'cost_of_delay': {
                '6_hour_delay': 'VIX options 30-50% more expensive, inverse ETFs already +5-8%',
                '24_hour_delay': 'Safe havens +3-5%, best short entries missed, IV too high',
                '3_day_delay': 'Oversold bounce already happened, mean reversion gone',
                '1_week_delay': 'Most opportunities exhausted, market in new regime'
            },
            'historical_proof': {
                'March_2020': 'VIX calls bought day 1 = +1000%. Day 3 = +300%. Day 7 = +50%. Massive decay.',
                'Feb_2018': 'VIX spike day 1 = best entries. Day 2+ = chasing.',
                'Oct_2022': 'Puts bought on first down day = +150%. Week later = +30%. First movers won.',
                'Aug_2024': 'Flash crash: First 15 minutes = best buying. 1 hour later = opportunity gone.'
            },
            'key_principle': 'In extreme events, act FAST with conviction. Hesitation costs 50-80% of potential returns. Have plan beforehand. Execute mechanically when trigger hits.'
        }
