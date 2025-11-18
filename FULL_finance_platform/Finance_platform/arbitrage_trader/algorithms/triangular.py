"""
Triangular arbitrage detection algorithms.
Commonly used in cryptocurrency and forex markets.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import uuid
from itertools import permutations

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class TriangularArbitrageDetector:
    """Detects triangular arbitrage opportunities in currency/crypto markets."""

    def __init__(self, min_profit_threshold: Decimal = Decimal("0.001")):
        """
        Initialize triangular arbitrage detector.

        Args:
            min_profit_threshold: Minimum profit percentage threshold
        """
        self.min_profit_threshold = min_profit_threshold

    def detect_opportunities(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Detect triangular arbitrage opportunities.

        Example: BTC/USD, ETH/USD, BTC/ETH
        - Buy BTC with USD
        - Buy ETH with BTC
        - Sell ETH for USD
        If final USD > initial USD, there's an arbitrage opportunity.

        Args:
            market_data: List of market data

        Returns:
            List of arbitrage opportunities
        """
        opportunities = []

        # Group market data by exchange
        exchange_data = self._group_by_exchange(market_data)

        for exchange, data_list in exchange_data.items():
            # Find triangular paths
            triangles = self._find_triangular_paths(data_list)

            for triangle in triangles:
                opportunity = self._calculate_triangular_opportunity(
                    triangle, exchange
                )
                if opportunity:
                    opportunities.append(opportunity)

        return opportunities

    def _group_by_exchange(
        self,
        market_data: List[MarketData]
    ) -> Dict[str, List[MarketData]]:
        """Group market data by exchange."""
        grouped = {}
        for data in market_data:
            if data.exchange not in grouped:
                grouped[data.exchange] = []
            grouped[data.exchange].append(data)
        return grouped

    def _find_triangular_paths(
        self,
        market_data: List[MarketData]
    ) -> List[Tuple[MarketData, MarketData, MarketData]]:
        """
        Find potential triangular arbitrage paths.

        Returns triangles of the form (pair1, pair2, pair3) where:
        - pair1: BASE/QUOTE1
        - pair2: BASE/QUOTE2
        - pair3: QUOTE1/QUOTE2
        """
        triangles = []

        # Parse trading pairs into base and quote currencies
        parsed_pairs = []
        for data in market_data:
            parts = data.symbol.split('/')
            if len(parts) == 2:
                parsed_pairs.append({
                    'data': data,
                    'base': parts[0],
                    'quote': parts[1]
                })

        # Find triangular relationships
        for i, pair1 in enumerate(parsed_pairs):
            for j, pair2 in enumerate(parsed_pairs):
                if i == j:
                    continue

                # Check if pair1 and pair2 share a base currency
                if pair1['base'] != pair2['base']:
                    continue

                # Look for a third pair that connects the two quote currencies
                for k, pair3 in enumerate(parsed_pairs):
                    if k == i or k == j:
                        continue

                    # Check if pair3 connects quote1 and quote2
                    if ((pair3['base'] == pair1['quote'] and pair3['quote'] == pair2['quote']) or
                        (pair3['base'] == pair2['quote'] and pair3['quote'] == pair1['quote'])):

                        triangle = (pair1['data'], pair2['data'], pair3['data'])
                        triangles.append(triangle)

        return triangles

    def _calculate_triangular_opportunity(
        self,
        triangle: Tuple[MarketData, MarketData, MarketData],
        exchange: str
    ) -> Optional[ArbitrageOpportunity]:
        """
        Calculate profit for a triangular arbitrage opportunity.

        Args:
            triangle: Tuple of three market data objects forming a triangle
            exchange: Exchange name

        Returns:
            ArbitrageOpportunity if profitable, None otherwise
        """
        pair1, pair2, pair3 = triangle

        # Parse currency pairs
        base1, quote1 = pair1.symbol.split('/')
        base2, quote2 = pair2.symbol.split('/')
        base3, quote3 = pair3.symbol.split('/')

        # Starting with 1 unit of the common base currency
        initial_amount = Decimal(1000)  # Start with 1000 units

        # Try both directions
        forward_profit = self._calculate_path_profit(
            initial_amount, pair1, pair2, pair3, forward=True
        )
        backward_profit = self._calculate_path_profit(
            initial_amount, pair1, pair2, pair3, forward=False
        )

        # Choose the more profitable direction
        if forward_profit > backward_profit:
            final_amount = forward_profit
            is_forward = True
        else:
            final_amount = backward_profit
            is_forward = False

        profit = final_amount - initial_amount
        profit_percentage = (profit / initial_amount) * Decimal(100)

        if profit_percentage < self.min_profit_threshold:
            return None

        # Calculate confidence and risk
        confidence = self._calculate_confidence(pair1, pair2, pair3, profit_percentage)
        risk = self._calculate_risk(pair1, pair2, pair3)

        # Create trading actions
        actions = self._create_trading_actions(
            pair1, pair2, pair3, initial_amount, is_forward
        )

        opportunity = ArbitrageOpportunity(
            opportunity_id=str(uuid.uuid4()),
            arbitrage_type=ArbitrageType.TRIANGULAR,
            market_type=pair1.market_type,
            symbol=f"{pair1.symbol}:{pair2.symbol}:{pair3.symbol}",
            timestamp=datetime.now(),
            expected_profit=profit,
            expected_profit_percentage=profit_percentage,
            confidence_score=confidence,
            risk_score=risk,
            detection_latency_ms=0,
            market_data=[pair1, pair2, pair3],
            suggested_actions=actions,
            metadata={
                "exchange": exchange,
                "initial_amount": float(initial_amount),
                "final_amount": float(final_amount),
                "direction": "forward" if is_forward else "backward",
                "path": f"{pair1.symbol} -> {pair2.symbol} -> {pair3.symbol}"
            }
        )

        return opportunity

    def _calculate_path_profit(
        self,
        initial_amount: Decimal,
        pair1: MarketData,
        pair2: MarketData,
        pair3: MarketData,
        forward: bool
    ) -> Decimal:
        """
        Calculate profit for a specific triangular path.

        Args:
            initial_amount: Starting amount
            pair1, pair2, pair3: Market data for the three pairs
            forward: Direction of the triangle

        Returns:
            Final amount after completing the triangle
        """
        try:
            if forward:
                # Step 1: Trade using pair1
                amount1 = initial_amount / pair1.ask_price

                # Step 2: Trade using pair3
                amount2 = amount1 * pair3.bid_price

                # Step 3: Trade using pair2
                final_amount = amount2 * pair2.bid_price

            else:
                # Step 1: Trade using pair2
                amount1 = initial_amount / pair2.ask_price

                # Step 2: Trade using pair3
                amount2 = amount1 / pair3.ask_price

                # Step 3: Trade using pair1
                final_amount = amount2 * pair1.bid_price

            return final_amount

        except (ZeroDivisionError, Exception):
            return Decimal(0)

    def _create_trading_actions(
        self,
        pair1: MarketData,
        pair2: MarketData,
        pair3: MarketData,
        initial_amount: Decimal,
        is_forward: bool
    ) -> List[TradingAction]:
        """Create trading actions for triangular arbitrage."""
        actions = []

        if is_forward:
            # Action 1: Buy pair1
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-1",
                exchange=pair1.exchange,
                symbol=pair1.symbol,
                side=OrderSide.BUY,
                quantity=initial_amount / pair1.ask_price,
                price=pair1.ask_price,
                order_type="market",
                priority=1
            ))

            # Action 2: Trade using pair3
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-2",
                exchange=pair3.exchange,
                symbol=pair3.symbol,
                side=OrderSide.SELL,
                quantity=initial_amount / pair1.ask_price,
                price=pair3.bid_price,
                order_type="market",
                priority=2
            ))

            # Action 3: Trade using pair2
            amount2 = (initial_amount / pair1.ask_price) * pair3.bid_price
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-3",
                exchange=pair2.exchange,
                symbol=pair2.symbol,
                side=OrderSide.SELL,
                quantity=amount2,
                price=pair2.bid_price,
                order_type="market",
                priority=3
            ))

        else:
            # Backward path
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-1",
                exchange=pair2.exchange,
                symbol=pair2.symbol,
                side=OrderSide.BUY,
                quantity=initial_amount / pair2.ask_price,
                price=pair2.ask_price,
                order_type="market",
                priority=1
            ))

            amount1 = initial_amount / pair2.ask_price
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-2",
                exchange=pair3.exchange,
                symbol=pair3.symbol,
                side=OrderSide.BUY,
                quantity=amount1 / pair3.ask_price,
                price=pair3.ask_price,
                order_type="market",
                priority=2
            ))

            amount2 = amount1 / pair3.ask_price
            actions.append(TradingAction(
                action_id=f"{str(uuid.uuid4())}-3",
                exchange=pair1.exchange,
                symbol=pair1.symbol,
                side=OrderSide.SELL,
                quantity=amount2,
                price=pair1.bid_price,
                order_type="market",
                priority=3
            ))

        return actions

    def _calculate_confidence(
        self,
        pair1: MarketData,
        pair2: MarketData,
        pair3: MarketData,
        profit_percentage: Decimal
    ) -> Decimal:
        """Calculate confidence score."""
        # Higher profit = higher confidence
        profit_factor = min(profit_percentage / Decimal(5), Decimal("0.4"))

        # Higher liquidity = higher confidence
        min_volume = min(
            pair1.bid_volume, pair1.ask_volume,
            pair2.bid_volume, pair2.ask_volume,
            pair3.bid_volume, pair3.ask_volume
        )
        liquidity_factor = min(min_volume / Decimal(100), Decimal("0.3"))

        # Tighter spreads = higher confidence
        avg_spread = (
            pair1.spread_percentage +
            pair2.spread_percentage +
            pair3.spread_percentage
        ) / Decimal(3)
        spread_factor = Decimal("0.3") - min(avg_spread / Decimal(10), Decimal("0.3"))

        return profit_factor + liquidity_factor + spread_factor

    def _calculate_risk(
        self,
        pair1: MarketData,
        pair2: MarketData,
        pair3: MarketData
    ) -> Decimal:
        """Calculate risk score."""
        # Execution risk (multiple trades required)
        execution_risk = Decimal("0.3")

        # Liquidity risk
        min_volume = min(
            pair1.bid_volume, pair1.ask_volume,
            pair2.bid_volume, pair2.ask_volume,
            pair3.bid_volume, pair3.ask_volume
        )
        liquidity_risk = Decimal("0.4") - min(min_volume / Decimal(100), Decimal("0.4"))

        # Price movement risk (3 trades = 3x exposure)
        price_risk = Decimal("0.2")

        return execution_risk + liquidity_risk + price_risk
