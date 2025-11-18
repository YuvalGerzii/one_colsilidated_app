"""
Advanced order book analysis for detecting micro-arbitrage opportunities.
Analyzes order book depth, imbalances, and liquidity.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import uuid
import numpy as np
from collections import deque

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class OrderBookLevel:
    """Represents a single order book level."""

    def __init__(self, price: Decimal, volume: Decimal, side: str):
        self.price = price
        self.volume = volume
        self.side = side  # 'bid' or 'ask'


class OrderBook:
    """Full order book representation."""

    def __init__(self, symbol: str, exchange: str, timestamp: datetime):
        self.symbol = symbol
        self.exchange = exchange
        self.timestamp = timestamp
        self.bids: List[OrderBookLevel] = []
        self.asks: List[OrderBookLevel] = []

    @property
    def best_bid(self) -> Optional[OrderBookLevel]:
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self) -> Optional[OrderBookLevel]:
        return self.asks[0] if self.asks else None

    @property
    def mid_price(self) -> Optional[Decimal]:
        if self.best_bid and self.best_ask:
            return (self.best_bid.price + self.best_ask.price) / Decimal(2)
        return None

    @property
    def spread(self) -> Optional[Decimal]:
        if self.best_bid and self.best_ask:
            return self.best_ask.price - self.best_bid.price
        return None


class OrderBookAnalyzer:
    """Analyzes order books for trading opportunities."""

    def __init__(self, config: dict = None):
        """
        Initialize order book analyzer.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}
        self.min_imbalance_threshold = Decimal(
            self.config.get("min_imbalance_threshold", "0.3")
        )
        self.depth_levels = self.config.get("depth_levels", 10)

        # Historical order books for analysis
        self.order_book_history: Dict[str, deque] = {}
        self.max_history = 100

    def analyze_order_book_imbalance(
        self,
        order_book: OrderBook
    ) -> Tuple[Decimal, str]:
        """
        Calculate order book imbalance.

        Imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)
        Positive = bullish pressure, Negative = bearish pressure

        Args:
            order_book: Order book to analyze

        Returns:
            Tuple of (imbalance_ratio, direction)
        """
        total_bid_volume = sum(level.volume for level in order_book.bids[:self.depth_levels])
        total_ask_volume = sum(level.volume for level in order_book.asks[:self.depth_levels])

        total_volume = total_bid_volume + total_ask_volume

        if total_volume == 0:
            return Decimal(0), "neutral"

        imbalance = (total_bid_volume - total_ask_volume) / total_volume

        if imbalance > self.min_imbalance_threshold:
            direction = "bullish"
        elif imbalance < -self.min_imbalance_threshold:
            direction = "bearish"
        else:
            direction = "neutral"

        return imbalance, direction

    def calculate_volume_weighted_price(
        self,
        order_book: OrderBook,
        side: str,
        target_volume: Decimal
    ) -> Optional[Decimal]:
        """
        Calculate the volume-weighted average price for executing a given volume.

        Args:
            order_book: Order book
            side: 'buy' (use asks) or 'sell' (use bids)
            target_volume: Target volume to execute

        Returns:
            Volume-weighted average price or None
        """
        levels = order_book.asks if side == "buy" else order_book.bids

        remaining_volume = target_volume
        total_cost = Decimal(0)
        filled_volume = Decimal(0)

        for level in levels:
            if remaining_volume <= 0:
                break

            volume_at_level = min(remaining_volume, level.volume)
            total_cost += volume_at_level * level.price
            filled_volume += volume_at_level
            remaining_volume -= volume_at_level

        if filled_volume == 0:
            return None

        return total_cost / filled_volume

    def calculate_market_depth(
        self,
        order_book: OrderBook,
        depth_levels: int = 5
    ) -> Dict[str, Decimal]:
        """
        Calculate market depth metrics.

        Args:
            order_book: Order book
            depth_levels: Number of levels to analyze

        Returns:
            Dictionary with depth metrics
        """
        bid_depth = sum(
            level.volume for level in order_book.bids[:depth_levels]
        )
        ask_depth = sum(
            level.volume for level in order_book.asks[:depth_levels]
        )

        total_depth = bid_depth + ask_depth

        # Calculate depth ratio
        depth_ratio = (
            bid_depth / total_depth if total_depth > 0 else Decimal(0.5)
        )

        # Calculate average spread across levels
        spreads = []
        for i in range(min(depth_levels, len(order_book.bids), len(order_book.asks))):
            if i < len(order_book.asks) and i < len(order_book.bids):
                spread = order_book.asks[i].price - order_book.bids[i].price
                spreads.append(spread)

        avg_spread = (
            sum(spreads) / len(spreads) if spreads else Decimal(0)
        )

        return {
            "bid_depth": bid_depth,
            "ask_depth": ask_depth,
            "total_depth": total_depth,
            "depth_ratio": depth_ratio,
            "avg_spread": avg_spread
        }

    def detect_liquidity_gaps(
        self,
        order_book: OrderBook
    ) -> List[Dict]:
        """
        Detect liquidity gaps in the order book.

        Large price gaps between levels can indicate low liquidity
        and potential for price manipulation or large slippage.

        Args:
            order_book: Order book

        Returns:
            List of detected gaps
        """
        gaps = []

        # Analyze bid side gaps
        for i in range(len(order_book.bids) - 1):
            price_gap = order_book.bids[i].price - order_book.bids[i + 1].price
            avg_price = (order_book.bids[i].price + order_book.bids[i + 1].price) / 2

            if avg_price > 0:
                gap_percentage = (price_gap / avg_price) * Decimal(100)

                # Flag gaps larger than 0.5%
                if gap_percentage > Decimal("0.5"):
                    gaps.append({
                        "side": "bid",
                        "level": i,
                        "price_gap": price_gap,
                        "gap_percentage": gap_percentage,
                        "upper_price": order_book.bids[i].price,
                        "lower_price": order_book.bids[i + 1].price
                    })

        # Analyze ask side gaps
        for i in range(len(order_book.asks) - 1):
            price_gap = order_book.asks[i + 1].price - order_book.asks[i].price
            avg_price = (order_book.asks[i].price + order_book.asks[i + 1].price) / 2

            if avg_price > 0:
                gap_percentage = (price_gap / avg_price) * Decimal(100)

                if gap_percentage > Decimal("0.5"):
                    gaps.append({
                        "side": "ask",
                        "level": i,
                        "price_gap": price_gap,
                        "gap_percentage": gap_percentage,
                        "lower_price": order_book.asks[i].price,
                        "upper_price": order_book.asks[i + 1].price
                    })

        return gaps

    def calculate_order_flow_toxicity(
        self,
        order_book: OrderBook,
        recent_trades: List[Dict]
    ) -> Decimal:
        """
        Calculate order flow toxicity (VPIN - Volume-Synchronized Probability of Informed Trading).

        High toxicity indicates informed trading and potential adverse selection.

        Args:
            order_book: Current order book
            recent_trades: Recent trades with {'price', 'volume', 'side', 'timestamp'}

        Returns:
            Toxicity score (0-1, higher = more toxic)
        """
        if not recent_trades:
            return Decimal(0)

        # Separate buy and sell volumes
        buy_volume = sum(
            Decimal(str(trade['volume']))
            for trade in recent_trades
            if trade.get('side') == 'buy'
        )
        sell_volume = sum(
            Decimal(str(trade['volume']))
            for trade in recent_trades
            if trade.get('side') == 'sell'
        )

        total_volume = buy_volume + sell_volume

        if total_volume == 0:
            return Decimal(0)

        # VPIN = |buy_volume - sell_volume| / total_volume
        vpin = abs(buy_volume - sell_volume) / total_volume

        return vpin

    def detect_spoofing_patterns(
        self,
        order_book_snapshots: List[OrderBook]
    ) -> List[Dict]:
        """
        Detect potential spoofing patterns.

        Spoofing: Large orders placed and quickly cancelled to manipulate price.

        Args:
            order_book_snapshots: Series of order book snapshots

        Returns:
            List of potential spoofing events
        """
        if len(order_book_snapshots) < 3:
            return []

        spoofing_events = []

        for i in range(1, len(order_book_snapshots) - 1):
            prev_book = order_book_snapshots[i - 1]
            curr_book = order_book_snapshots[i]
            next_book = order_book_snapshots[i + 1]

            # Check for large orders that appear and disappear quickly
            # Check bid side
            if (len(curr_book.bids) > 0 and len(prev_book.bids) > 0 and
                len(next_book.bids) > 0):

                curr_best_bid_vol = curr_book.bids[0].volume
                prev_best_bid_vol = prev_book.bids[0].volume
                next_best_bid_vol = next_book.bids[0].volume

                # Large spike in volume that disappears
                if (curr_best_bid_vol > prev_best_bid_vol * 3 and
                    curr_best_bid_vol > next_best_bid_vol * 3):

                    spoofing_events.append({
                        "type": "bid_spoofing",
                        "timestamp": curr_book.timestamp,
                        "price": curr_book.bids[0].price,
                        "volume": curr_best_bid_vol,
                        "confidence": min(
                            curr_best_bid_vol / prev_best_bid_vol / 10,
                            Decimal(1)
                        )
                    })

            # Check ask side
            if (len(curr_book.asks) > 0 and len(prev_book.asks) > 0 and
                len(next_book.asks) > 0):

                curr_best_ask_vol = curr_book.asks[0].volume
                prev_best_ask_vol = prev_book.asks[0].volume
                next_best_ask_vol = next_book.asks[0].volume

                if (curr_best_ask_vol > prev_best_ask_vol * 3 and
                    curr_best_ask_vol > next_best_ask_vol * 3):

                    spoofing_events.append({
                        "type": "ask_spoofing",
                        "timestamp": curr_book.timestamp,
                        "price": curr_book.asks[0].price,
                        "volume": curr_best_ask_vol,
                        "confidence": min(
                            curr_best_ask_vol / prev_best_ask_vol / 10,
                            Decimal(1)
                        )
                    })

        return spoofing_events

    def calculate_execution_quality_score(
        self,
        order_book: OrderBook,
        target_volume: Decimal,
        side: str
    ) -> Decimal:
        """
        Calculate execution quality score (0-1, higher = better).

        Considers:
        - Available liquidity
        - Expected slippage
        - Order book depth
        - Spread

        Args:
            order_book: Order book
            target_volume: Desired execution volume
            side: 'buy' or 'sell'

        Returns:
            Quality score (0-1)
        """
        # Calculate VWAP
        vwap = self.calculate_volume_weighted_price(order_book, side, target_volume)

        if not vwap or not order_book.mid_price:
            return Decimal(0)

        # Calculate slippage percentage
        if side == "buy":
            slippage_pct = ((vwap - order_book.mid_price) / order_book.mid_price) * 100
        else:
            slippage_pct = ((order_book.mid_price - vwap) / order_book.mid_price) * 100

        # Lower slippage = higher score
        slippage_score = max(Decimal(0), Decimal(1) - slippage_pct / 2)

        # Calculate depth score
        depth_metrics = self.calculate_market_depth(order_book)
        depth_score = min(depth_metrics['total_depth'] / target_volume / 5, Decimal(1))

        # Calculate spread score
        if order_book.spread and order_book.mid_price:
            spread_pct = (order_book.spread / order_book.mid_price) * 100
            spread_score = max(Decimal(0), Decimal(1) - spread_pct / 2)
        else:
            spread_score = Decimal(0)

        # Weighted average
        quality_score = (
            slippage_score * Decimal("0.4") +
            depth_score * Decimal("0.3") +
            spread_score * Decimal("0.3")
        )

        return quality_score

    def detect_order_book_opportunities(
        self,
        order_book: OrderBook
    ) -> List[ArbitrageOpportunity]:
        """
        Detect opportunities based on order book analysis.

        Args:
            order_book: Order book to analyze

        Returns:
            List of detected opportunities
        """
        opportunities = []

        # Analyze imbalance
        imbalance, direction = self.analyze_order_book_imbalance(order_book)

        # Significant imbalance can predict short-term price movement
        if abs(imbalance) > self.min_imbalance_threshold:
            # Predict price movement based on imbalance
            expected_move_pct = abs(imbalance) * Decimal("0.5")  # Simplified

            confidence = min(abs(imbalance), Decimal("0.95"))
            risk = Decimal("0.5") - min(abs(imbalance) / 4, Decimal("0.2"))

            # Create opportunity
            side = OrderSide.BUY if direction == "bullish" else OrderSide.SELL
            price = order_book.best_ask.price if side == OrderSide.BUY else order_book.best_bid.price

            opportunity = ArbitrageOpportunity(
                opportunity_id=str(uuid.uuid4()),
                arbitrage_type=ArbitrageType.STATISTICAL,
                market_type=MarketData(
                    symbol=order_book.symbol,
                    exchange=order_book.exchange,
                    market_type=None,  # Would need to be passed in
                    bid_price=order_book.best_bid.price if order_book.best_bid else Decimal(0),
                    ask_price=order_book.best_ask.price if order_book.best_ask else Decimal(0),
                    bid_volume=order_book.best_bid.volume if order_book.best_bid else Decimal(0),
                    ask_volume=order_book.best_ask.volume if order_book.best_ask else Decimal(0),
                    timestamp=order_book.timestamp
                ).market_type,
                symbol=order_book.symbol,
                timestamp=datetime.now(),
                expected_profit=expected_move_pct * Decimal(100),
                expected_profit_percentage=expected_move_pct,
                confidence_score=confidence,
                risk_score=risk,
                detection_latency_ms=0,
                market_data=[],
                suggested_actions=[
                    TradingAction(
                        action_id=str(uuid.uuid4()),
                        exchange=order_book.exchange,
                        symbol=order_book.symbol,
                        side=side,
                        quantity=Decimal(10),
                        price=price,
                        order_type="limit",
                        priority=1
                    )
                ],
                metadata={
                    "strategy": "order_book_imbalance",
                    "imbalance": float(imbalance),
                    "direction": direction,
                    "depth_analysis": self.calculate_market_depth(order_book)
                }
            )

            opportunities.append(opportunity)

        return opportunities
