"""
Market Microstructure Analyzer

Analyzes market structure to detect:
- Dark pool activity and hidden liquidity
- Institutional order flow patterns
- HFT signatures
- Order book imbalances
- Smart money vs dumb money flow

Based on academic research and professional market microstructure analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import statistics
import math


class ParticipantType(Enum):
    """Market participant types"""
    RETAIL = "retail"
    INSTITUTIONAL = "institutional"
    HIGH_FREQUENCY = "high_frequency"
    MARKET_MAKER = "market_maker"
    UNKNOWN = "unknown"


class DarkPoolType(Enum):
    """Types of dark pool platforms"""
    SIGMA_X = "goldman_sigma_x"  # Goldman Sachs
    LIQUIDNET = "liquidnet"  # Institutional only
    CROSSFINDER = "credit_suisse_crossfinder"
    POSIT = "virtu_posit"
    IEX = "iex"  # D-limit orders
    GENERIC = "generic"


class OrderType(Enum):
    """Order types in market microstructure"""
    MARKET = "market"
    LIMIT = "limit"
    ICEBERG = "iceberg"
    HIDDEN = "hidden"
    PEGGED = "pegged"
    D_LIMIT = "d_limit"  # IEX discretionary limit


@dataclass
class DarkPoolPrint:
    """A dark pool trade print"""
    timestamp: datetime
    price: float
    size: int
    venue: str
    is_block: bool
    price_improvement: float  # vs NBBO midpoint


@dataclass
class OrderBookLevel:
    """Single level in order book"""
    price: float
    size: int
    num_orders: int
    is_hidden_liquidity: bool = False


@dataclass
class MicrostructureAnalysis:
    """Complete microstructure analysis result"""
    dark_pool_percentage: float
    institutional_flow_score: float  # 0-1
    hft_activity_score: float  # 0-1
    hidden_liquidity_detected: bool
    order_book_imbalance: float  # -1 (sell) to +1 (buy)
    smart_money_direction: str  # 'buying', 'selling', 'neutral'
    participant_breakdown: Dict[str, float]
    trading_signals: List[str]
    risk_warnings: List[str]
    recommendations: List[str]


class MicrostructureAnalyzer:
    """
    Analyzes market microstructure to understand:
    - Who is trading (retail vs institutional)
    - Where they're trading (lit vs dark)
    - How they're trading (algos, blocks, etc.)
    """

    def __init__(self):
        # Dark pool detection thresholds
        self.dark_pool_venues = {
            'SIGMA': DarkPoolType.SIGMA_X,
            'LQNT': DarkPoolType.LIQUIDNET,
            'CSFB': DarkPoolType.CROSSFINDER,
            'VIRT': DarkPoolType.POSIT,
            'IEXG': DarkPoolType.IEX
        }

        # Participant classification thresholds
        self.thresholds = {
            'block_trade_min': 10000,  # shares
            'hft_latency_ms': 1,  # milliseconds
            'institutional_min_size': 5000,
            'retail_max_size': 500,
            'odd_lot_threshold': 100
        }

        # Historical dark pool volume (approximately)
        self.typical_dark_pool_pct = 0.40  # 40% of US equity volume

    def analyze_microstructure(self,
                               lit_trades: List[Dict],
                               dark_prints: List[DarkPoolPrint],
                               order_book: Dict[str, List[OrderBookLevel]],
                               nbbo: Dict[str, float]) -> MicrostructureAnalysis:
        """
        Main microstructure analysis.

        Args:
            lit_trades: Trades from lit exchanges
            dark_prints: Prints from dark pools
            order_book: Current order book {'bids': [...], 'asks': [...]}
            nbbo: National Best Bid/Offer {'bid': x, 'ask': y}

        Returns:
            Complete microstructure analysis
        """
        # Calculate dark pool percentage
        lit_volume = sum(t.get('size', 0) for t in lit_trades)
        dark_volume = sum(dp.size for dp in dark_prints)
        total_volume = lit_volume + dark_volume
        dark_pool_pct = dark_volume / total_volume if total_volume > 0 else 0

        # Classify participants
        participant_breakdown = self._classify_participants(lit_trades, dark_prints)

        # Calculate institutional flow
        institutional_score = self._calculate_institutional_flow(
            dark_prints, lit_trades, participant_breakdown
        )

        # Detect HFT activity
        hft_score = self._detect_hft_activity(lit_trades)

        # Detect hidden liquidity
        hidden_liquidity = self._detect_hidden_liquidity(
            order_book, lit_trades, dark_prints
        )

        # Calculate order book imbalance
        book_imbalance = self._calculate_book_imbalance(order_book)

        # Determine smart money direction
        smart_money = self._determine_smart_money_direction(
            dark_prints, institutional_score, participant_breakdown
        )

        # Generate signals and warnings
        signals = self._generate_signals(
            dark_pool_pct, institutional_score, hft_score,
            hidden_liquidity, book_imbalance, smart_money
        )

        warnings = self._generate_warnings(
            dark_pool_pct, hft_score, hidden_liquidity, book_imbalance
        )

        recommendations = self._generate_recommendations(
            smart_money, institutional_score, book_imbalance, signals
        )

        return MicrostructureAnalysis(
            dark_pool_percentage=dark_pool_pct,
            institutional_flow_score=institutional_score,
            hft_activity_score=hft_score,
            hidden_liquidity_detected=hidden_liquidity,
            order_book_imbalance=book_imbalance,
            smart_money_direction=smart_money,
            participant_breakdown=participant_breakdown,
            trading_signals=signals,
            risk_warnings=warnings,
            recommendations=recommendations
        )

    def _classify_participants(self, lit_trades: List[Dict],
                               dark_prints: List[DarkPoolPrint]) -> Dict[str, float]:
        """
        Classify market participants by trade characteristics.

        Based on academic research using trader-level data.
        """
        if not lit_trades and not dark_prints:
            return {
                'retail': 0.0,
                'institutional': 0.0,
                'hft': 0.0,
                'market_maker': 0.0
            }

        total_volume = sum(t.get('size', 0) for t in lit_trades) + \
                      sum(dp.size for dp in dark_prints)

        if total_volume == 0:
            return {
                'retail': 0.0,
                'institutional': 0.0,
                'hft': 0.0,
                'market_maker': 0.0
            }

        retail_vol = 0
        institutional_vol = 0
        hft_vol = 0
        mm_vol = 0

        # Classify lit trades
        for trade in lit_trades:
            size = trade.get('size', 0)

            # Small trades with round lots = likely retail
            if size <= self.thresholds['retail_max_size']:
                # Check for odd lots (algorithmic retail like Robinhood)
                if size % 100 != 0:
                    # Could be retail via algo or HFT
                    retail_vol += size * 0.7
                    hft_vol += size * 0.3
                else:
                    retail_vol += size

            # Medium trades
            elif size <= self.thresholds['institutional_min_size']:
                # Could be any participant
                retail_vol += size * 0.3
                institutional_vol += size * 0.5
                mm_vol += size * 0.2

            # Large trades
            else:
                institutional_vol += size * 0.8
                mm_vol += size * 0.2

        # Dark pool prints are primarily institutional
        for dp in dark_prints:
            if dp.is_block:
                institutional_vol += dp.size
            else:
                institutional_vol += dp.size * 0.8
                mm_vol += dp.size * 0.2

        return {
            'retail': retail_vol / total_volume,
            'institutional': institutional_vol / total_volume,
            'hft': hft_vol / total_volume,
            'market_maker': mm_vol / total_volume
        }

    def _calculate_institutional_flow(self,
                                      dark_prints: List[DarkPoolPrint],
                                      lit_trades: List[Dict],
                                      participants: Dict[str, float]) -> float:
        """
        Calculate institutional flow score (0-1).

        Higher score = more institutional activity = follow the smart money.
        """
        score = 0.0

        # Dark pool volume indicates institutional activity
        if dark_prints:
            dark_vol = sum(dp.size for dp in dark_prints)
            lit_vol = sum(t.get('size', 0) for t in lit_trades)
            total = dark_vol + lit_vol

            if total > 0:
                dark_ratio = dark_vol / total
                # Above-average dark pool usage is bullish for institutional
                if dark_ratio > self.typical_dark_pool_pct:
                    score += 0.3

        # Block trades indicate institutions
        block_volume = sum(
            dp.size for dp in dark_prints if dp.is_block
        )
        if dark_prints:
            total_dark = sum(dp.size for dp in dark_prints)
            if total_dark > 0:
                block_ratio = block_volume / total_dark
                score += block_ratio * 0.3

        # Price improvement indicates smart routing
        if dark_prints:
            avg_improvement = statistics.mean(
                [dp.price_improvement for dp in dark_prints]
            )
            if avg_improvement > 0:
                score += min(avg_improvement / 0.01, 0.2)  # Cap at 0.2

        # Direct institutional percentage
        score += participants.get('institutional', 0) * 0.2

        return min(score, 1.0)

    def _detect_hft_activity(self, lit_trades: List[Dict]) -> float:
        """
        Detect high-frequency trading activity.

        HFT signatures:
        - Sub-millisecond timing
        - Quote stuffing (rapid order additions/cancellations)
        - Consistent small sizes
        - Latency arbitrage patterns
        """
        if len(lit_trades) < 10:
            return 0.0

        score = 0.0

        # Check trade timing intervals
        timestamps = [t.get('timestamp') for t in lit_trades if t.get('timestamp')]
        if len(timestamps) >= 2:
            intervals = []
            for i in range(1, len(timestamps)):
                if isinstance(timestamps[i], datetime) and isinstance(timestamps[i-1], datetime):
                    interval_ms = (timestamps[i] - timestamps[i-1]).total_seconds() * 1000
                    intervals.append(interval_ms)

            if intervals:
                # Very fast intervals suggest HFT
                fast_trades = sum(1 for i in intervals if i < 10)  # <10ms
                fast_ratio = fast_trades / len(intervals)
                score += fast_ratio * 0.4

        # Check for consistent sizes (algorithmic)
        sizes = [t.get('size', 0) for t in lit_trades]
        if len(sizes) > 5:
            try:
                cv = statistics.stdev(sizes) / statistics.mean(sizes)
                if cv < 0.1:  # Very consistent
                    score += 0.3
                elif cv < 0.3:
                    score += 0.1
            except (statistics.StatisticsError, ZeroDivisionError):
                pass

        # Check for odd lots (common in HFT)
        odd_lots = sum(1 for s in sizes if s % 100 != 0)
        odd_lot_ratio = odd_lots / len(sizes) if sizes else 0
        if odd_lot_ratio > 0.5:
            score += 0.2

        return min(score, 1.0)

    def _detect_hidden_liquidity(self,
                                 order_book: Dict[str, List[OrderBookLevel]],
                                 lit_trades: List[Dict],
                                 dark_prints: List[DarkPoolPrint]) -> bool:
        """
        Detect hidden liquidity in the market.

        Signs:
        - Price doesn't move despite aggressive volume
        - Large fills with no matching visible orders
        - Repeated fills at same price (icebergs)
        """
        if not order_book or not lit_trades:
            return False

        # Check for price stability with high volume
        bids = order_book.get('bids', [])
        asks = order_book.get('asks', [])

        if not bids or not asks:
            return False

        # Get visible liquidity at top of book
        visible_bid_size = bids[0].size if bids else 0
        visible_ask_size = asks[0].size if asks else 0

        # Compare to traded volume
        trade_volume = sum(t.get('size', 0) for t in lit_trades[-20:])  # Recent trades

        # If trade volume >> visible liquidity but price stable = hidden orders
        if trade_volume > (visible_bid_size + visible_ask_size) * 3:
            # Check price stability
            prices = [t.get('price', 0) for t in lit_trades[-20:] if t.get('price')]
            if prices:
                price_range = max(prices) - min(prices)
                avg_price = sum(prices) / len(prices)
                if price_range / avg_price < 0.001:  # <0.1% movement
                    return True

        # Check for iceberg patterns (repeated fills at same price)
        price_counts = {}
        for trade in lit_trades:
            price = round(trade.get('price', 0), 2)
            size = trade.get('size', 0)
            if price not in price_counts:
                price_counts[price] = {'count': 0, 'volume': 0}
            price_counts[price]['count'] += 1
            price_counts[price]['volume'] += size

        # Many fills at same price with large total = iceberg
        for price, data in price_counts.items():
            if data['count'] >= 5 and data['volume'] > self.thresholds['block_trade_min']:
                return True

        return False

    def _calculate_book_imbalance(self,
                                  order_book: Dict[str, List[OrderBookLevel]]) -> float:
        """
        Calculate order book imbalance.

        Returns: -1 (heavy selling pressure) to +1 (heavy buying pressure)
        """
        bids = order_book.get('bids', [])
        asks = order_book.get('asks', [])

        if not bids and not asks:
            return 0.0

        # Sum volume at top levels (typically top 5)
        bid_volume = sum(level.size for level in bids[:5])
        ask_volume = sum(level.size for level in asks[:5])

        total = bid_volume + ask_volume
        if total == 0:
            return 0.0

        # Imbalance = (bids - asks) / (bids + asks)
        imbalance = (bid_volume - ask_volume) / total

        return imbalance

    def _determine_smart_money_direction(self,
                                         dark_prints: List[DarkPoolPrint],
                                         institutional_score: float,
                                         participants: Dict[str, float]) -> str:
        """
        Determine which way smart money is positioned.

        Smart money = institutional investors and informed traders
        """
        if not dark_prints and institutional_score < 0.3:
            return 'neutral'

        # Calculate net direction from dark pool prints
        buy_volume = 0
        sell_volume = 0

        for dp in dark_prints:
            # Use price improvement as proxy for direction
            # Positive improvement on buys, negative on sells (typically)
            if dp.price_improvement > 0:
                buy_volume += dp.size
            else:
                sell_volume += dp.size

        net_direction = buy_volume - sell_volume
        total = buy_volume + sell_volume

        if total == 0:
            return 'neutral'

        direction_pct = net_direction / total

        if direction_pct > 0.2 and institutional_score > 0.4:
            return 'buying'
        elif direction_pct < -0.2 and institutional_score > 0.4:
            return 'selling'
        else:
            return 'neutral'

    def _generate_signals(self, dark_pool_pct: float,
                          institutional_score: float,
                          hft_score: float,
                          hidden_liquidity: bool,
                          book_imbalance: float,
                          smart_money: str) -> List[str]:
        """Generate trading signals from microstructure analysis"""
        signals = []

        # Dark pool signals
        if dark_pool_pct > 0.5:
            signals.append(f"High dark pool activity ({dark_pool_pct:.0%}) - institutional accumulation/distribution likely")

        # Institutional flow signals
        if institutional_score > 0.7:
            signals.append(f"Strong institutional flow ({institutional_score:.0%}) - follow smart money")
            if smart_money == 'buying':
                signals.append("Smart money accumulating - bullish")
            elif smart_money == 'selling':
                signals.append("Smart money distributing - bearish")

        # HFT signals
        if hft_score > 0.6:
            signals.append(f"High HFT activity ({hft_score:.0%}) - expect rapid price movements")

        # Hidden liquidity signals
        if hidden_liquidity:
            signals.append("Hidden liquidity detected - potential support/resistance")
            signals.append("Watch for iceberg orders absorbing flow")

        # Order book signals
        if book_imbalance > 0.4:
            signals.append(f"Strong bid-side imbalance ({book_imbalance:+.0%}) - buying pressure")
        elif book_imbalance < -0.4:
            signals.append(f"Strong ask-side imbalance ({book_imbalance:+.0%}) - selling pressure")

        return signals

    def _generate_warnings(self, dark_pool_pct: float,
                           hft_score: float,
                           hidden_liquidity: bool,
                           book_imbalance: float) -> List[str]:
        """Generate risk warnings from microstructure analysis"""
        warnings = []

        # Dark pool warnings
        if dark_pool_pct > 0.6:
            warnings.append("Very high dark pool percentage - reduced price discovery")

        # HFT warnings
        if hft_score > 0.7:
            warnings.append("Extreme HFT activity - increased adverse selection risk")
            warnings.append("Consider using limit orders to avoid slippage")

        # Hidden liquidity warnings
        if hidden_liquidity:
            warnings.append("Hidden liquidity may cause unexpected resistance/support")

        # Book imbalance warnings
        if abs(book_imbalance) > 0.6:
            warnings.append("Extreme order book imbalance - potential for rapid price movement")

        return warnings

    def _generate_recommendations(self, smart_money: str,
                                   institutional_score: float,
                                   book_imbalance: float,
                                   signals: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Smart money recommendations
        if smart_money == 'buying' and institutional_score > 0.5:
            recommendations.append("Align with institutional buying - consider long positions")
            recommendations.append("Wait for pullbacks to key support levels")
        elif smart_money == 'selling' and institutional_score > 0.5:
            recommendations.append("Institutions are selling - reduce long exposure")
            recommendations.append("Consider short positions on bounces to resistance")

        # Order book recommendations
        if book_imbalance > 0.4:
            recommendations.append("Strong bid support - buy dips with tight stops")
        elif book_imbalance < -0.4:
            recommendations.append("Heavy ask pressure - sell rallies with tight stops")

        # General recommendations
        if institutional_score > 0.6:
            recommendations.append("Use dark pools or algos for large orders to minimize impact")
        else:
            recommendations.append("Lit markets preferred - adequate liquidity visible")

        return recommendations

    def analyze_dark_pool_prints(self,
                                 prints: List[DarkPoolPrint]) -> Dict:
        """
        Detailed analysis of dark pool activity.

        Dark pool activity often reveals institutional intent before
        it shows up in lit markets.
        """
        if not prints:
            return {'status': 'no_data'}

        total_volume = sum(p.size for p in prints)
        block_volume = sum(p.size for p in prints if p.is_block)

        # Group by venue
        venue_breakdown = {}
        for p in prints:
            if p.venue not in venue_breakdown:
                venue_breakdown[p.venue] = {'volume': 0, 'count': 0, 'avg_improvement': []}
            venue_breakdown[p.venue]['volume'] += p.size
            venue_breakdown[p.venue]['count'] += 1
            venue_breakdown[p.venue]['avg_improvement'].append(p.price_improvement)

        # Calculate average improvement per venue
        for venue in venue_breakdown:
            improvements = venue_breakdown[venue]['avg_improvement']
            venue_breakdown[venue]['avg_improvement'] = \
                statistics.mean(improvements) if improvements else 0

        # Price improvement analysis
        avg_improvement = statistics.mean([p.price_improvement for p in prints])

        # Time analysis
        prints_sorted = sorted(prints, key=lambda x: x.timestamp)
        if len(prints_sorted) >= 2:
            time_span = (prints_sorted[-1].timestamp - prints_sorted[0].timestamp).total_seconds()
            volume_rate = total_volume / time_span if time_span > 0 else 0
        else:
            volume_rate = 0

        return {
            'total_volume': total_volume,
            'block_volume': block_volume,
            'block_percentage': block_volume / total_volume if total_volume else 0,
            'num_prints': len(prints),
            'venue_breakdown': venue_breakdown,
            'avg_price_improvement': avg_improvement,
            'volume_rate_per_second': volume_rate,
            'interpretation': self._interpret_dark_pool_activity(
                block_volume / total_volume if total_volume else 0,
                avg_improvement,
                len(venue_breakdown)
            )
        }

    def _interpret_dark_pool_activity(self, block_pct: float,
                                      avg_improvement: float,
                                      num_venues: int) -> str:
        """Interpret dark pool activity patterns"""

        if block_pct > 0.5:
            return "Heavy block trading suggests major institutional repositioning"
        elif block_pct > 0.3:
            return "Moderate block activity indicates institutional interest"

        if avg_improvement > 0.005:  # Half a cent
            return "Good price improvement suggests favorable execution quality"

        if num_venues >= 3:
            return "Multi-venue execution suggests sophisticated institutional algo"

        return "Normal dark pool activity - typical institutional flow"


class OrderBookAnalyzer:
    """
    Analyzes order book dynamics for trading signals.

    Key concepts:
    - Spoofing detection (fake orders)
    - Absorption (large orders holding levels)
    - Momentum ignition (triggering stops)
    """

    def __init__(self):
        self.spoof_threshold = 0.8  # Order cancellation rate
        self.absorption_ratio = 5.0  # Volume absorbed vs order size

    def analyze_book_dynamics(self,
                              book_snapshots: List[Dict]) -> Dict:
        """
        Analyze order book changes over time.

        Args:
            book_snapshots: List of order book states over time

        Returns:
            Analysis of book dynamics
        """
        if len(book_snapshots) < 2:
            return {'status': 'insufficient_data'}

        # Track level changes
        bid_changes = []
        ask_changes = []

        for i in range(1, len(book_snapshots)):
            prev = book_snapshots[i-1]
            curr = book_snapshots[i]

            # Top of book changes
            prev_bid = prev.get('bids', [{}])[0].get('price', 0)
            curr_bid = curr.get('bids', [{}])[0].get('price', 0)
            prev_ask = prev.get('asks', [{}])[0].get('price', 0)
            curr_ask = curr.get('asks', [{}])[0].get('price', 0)

            bid_changes.append(curr_bid - prev_bid)
            ask_changes.append(curr_ask - prev_ask)

        # Analyze patterns
        avg_bid_change = statistics.mean(bid_changes) if bid_changes else 0
        avg_ask_change = statistics.mean(ask_changes) if ask_changes else 0

        # Spoofing detection: many additions followed by cancellations
        # Momentum ignition: aggressive orders triggering stops

        return {
            'avg_bid_change': avg_bid_change,
            'avg_ask_change': avg_ask_change,
            'spread_trend': avg_ask_change - avg_bid_change,
            'volatility': statistics.stdev(bid_changes) if len(bid_changes) > 1 else 0,
            'pressure': 'buy' if avg_bid_change > avg_ask_change else 'sell'
        }

    def detect_spoofing(self, order_events: List[Dict]) -> List[Dict]:
        """
        Detect potential spoofing activity.

        Spoofing: Placing large orders with intent to cancel before execution
        to manipulate prices.
        """
        if not order_events:
            return []

        spoofs = []

        # Group orders by price level
        level_orders = {}
        for event in order_events:
            price = event.get('price', 0)
            if price not in level_orders:
                level_orders[price] = {'adds': 0, 'cancels': 0, 'fills': 0}

            event_type = event.get('type', '')
            if event_type == 'add':
                level_orders[price]['adds'] += event.get('size', 0)
            elif event_type == 'cancel':
                level_orders[price]['cancels'] += event.get('size', 0)
            elif event_type == 'fill':
                level_orders[price]['fills'] += event.get('size', 0)

        # High cancel/add ratio with low fills = potential spoof
        for price, counts in level_orders.items():
            if counts['adds'] > 0:
                cancel_ratio = counts['cancels'] / counts['adds']
                fill_ratio = counts['fills'] / counts['adds']

                if cancel_ratio > self.spoof_threshold and fill_ratio < 0.1:
                    spoofs.append({
                        'price': price,
                        'cancel_ratio': cancel_ratio,
                        'fill_ratio': fill_ratio,
                        'total_added': counts['adds'],
                        'confidence': min((cancel_ratio - 0.8) * 5, 1.0)
                    })

        return spoofs
