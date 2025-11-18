"""
Cross-exchange arbitrage detection algorithms.
"""
from typing import List, Dict
from decimal import Decimal
from datetime import datetime
import uuid

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class CrossExchangeDetector:
    """Detects arbitrage opportunities across different exchanges."""

    def __init__(self, min_spread_threshold: Decimal = Decimal("0.001")):
        """
        Initialize cross-exchange detector.

        Args:
            min_spread_threshold: Minimum spread percentage to consider (e.g., 0.1%)
        """
        self.min_spread_threshold = min_spread_threshold

    def detect_opportunities(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Detect cross-exchange arbitrage opportunities.

        Strategy: Buy on exchange with lower ask price, sell on exchange with higher bid price.

        Args:
            market_data: List of market data from different exchanges

        Returns:
            List of arbitrage opportunities
        """
        opportunities = []

        # Group market data by symbol
        symbol_data = self._group_by_symbol(market_data)

        for symbol, data_list in symbol_data.items():
            if len(data_list) < 2:
                continue

            # Find best buy and sell prices across exchanges
            for i, buy_data in enumerate(data_list):
                for j, sell_data in enumerate(data_list):
                    if i == j or buy_data.exchange == sell_data.exchange:
                        continue

                    # Calculate potential profit
                    # Buy at ask price on buy_exchange, sell at bid price on sell_exchange
                    buy_price = buy_data.ask_price
                    sell_price = sell_data.bid_price

                    if sell_price <= buy_price:
                        continue

                    # Calculate profit percentage
                    profit_per_unit = sell_price - buy_price
                    profit_percentage = (profit_per_unit / buy_price) * Decimal(100)

                    if profit_percentage < self.min_spread_threshold:
                        continue

                    # Estimate transaction volume based on available liquidity
                    max_volume = min(buy_data.ask_volume, sell_data.bid_volume)

                    if max_volume <= 0:
                        continue

                    # Calculate expected profit (simplified, not accounting for fees)
                    expected_profit = profit_per_unit * max_volume

                    # Calculate confidence and risk scores
                    confidence = self._calculate_confidence(
                        buy_data, sell_data, profit_percentage
                    )
                    risk = self._calculate_risk(
                        buy_data, sell_data, profit_percentage
                    )

                    # Create opportunity
                    opportunity = ArbitrageOpportunity(
                        opportunity_id=str(uuid.uuid4()),
                        arbitrage_type=ArbitrageType.CROSS_EXCHANGE,
                        market_type=buy_data.market_type,
                        symbol=symbol,
                        timestamp=datetime.now(),
                        expected_profit=expected_profit,
                        expected_profit_percentage=profit_percentage,
                        confidence_score=confidence,
                        risk_score=risk,
                        detection_latency_ms=0,  # Will be set by agent
                        market_data=[buy_data, sell_data],
                        suggested_actions=[
                            TradingAction(
                                action_id=f"{str(uuid.uuid4())}-buy",
                                exchange=buy_data.exchange,
                                symbol=symbol,
                                side=OrderSide.BUY,
                                quantity=max_volume,
                                price=buy_price,
                                order_type="limit",
                                priority=1
                            ),
                            TradingAction(
                                action_id=f"{str(uuid.uuid4())}-sell",
                                exchange=sell_data.exchange,
                                symbol=symbol,
                                side=OrderSide.SELL,
                                quantity=max_volume,
                                price=sell_price,
                                order_type="limit",
                                priority=2
                            )
                        ],
                        metadata={
                            "buy_exchange": buy_data.exchange,
                            "sell_exchange": sell_data.exchange,
                            "buy_price": float(buy_price),
                            "sell_price": float(sell_price),
                            "max_volume": float(max_volume)
                        }
                    )

                    opportunities.append(opportunity)

        return opportunities

    def _group_by_symbol(
        self,
        market_data: List[MarketData]
    ) -> Dict[str, List[MarketData]]:
        """Group market data by symbol."""
        grouped = {}
        for data in market_data:
            if data.symbol not in grouped:
                grouped[data.symbol] = []
            grouped[data.symbol].append(data)
        return grouped

    def _calculate_confidence(
        self,
        buy_data: MarketData,
        sell_data: MarketData,
        profit_percentage: Decimal
    ) -> Decimal:
        """
        Calculate confidence score for the opportunity.

        Factors:
        - Higher profit percentage = higher confidence
        - Higher liquidity = higher confidence
        - Smaller spread on individual exchanges = higher confidence
        """
        # Profit factor (0-0.4)
        profit_factor = min(profit_percentage / Decimal(10), Decimal("0.4"))

        # Liquidity factor (0-0.3)
        min_volume = min(buy_data.ask_volume, sell_data.bid_volume)
        liquidity_factor = min(min_volume / Decimal(100), Decimal("0.3"))

        # Spread factor (0-0.3) - tighter spreads are better
        avg_spread_pct = (
            buy_data.spread_percentage + sell_data.spread_percentage
        ) / Decimal(2)
        spread_factor = Decimal("0.3") - min(avg_spread_pct / Decimal(10), Decimal("0.3"))

        return profit_factor + liquidity_factor + spread_factor

    def _calculate_risk(
        self,
        buy_data: MarketData,
        sell_data: MarketData,
        profit_percentage: Decimal
    ) -> Decimal:
        """
        Calculate risk score for the opportunity.

        Factors:
        - Lower liquidity = higher risk
        - Wider spreads = higher risk
        - Older data = higher risk
        """
        # Liquidity risk (0-0.4)
        min_volume = min(buy_data.ask_volume, sell_data.bid_volume)
        liquidity_risk = Decimal("0.4") - min(min_volume / Decimal(100), Decimal("0.4"))

        # Spread risk (0-0.3)
        avg_spread_pct = (
            buy_data.spread_percentage + sell_data.spread_percentage
        ) / Decimal(2)
        spread_risk = min(avg_spread_pct / Decimal(5), Decimal("0.3"))

        # Data freshness risk (0-0.3)
        now = datetime.now()
        max_age = max(
            (now - buy_data.timestamp).total_seconds(),
            (now - sell_data.timestamp).total_seconds()
        )
        freshness_risk = min(Decimal(max_age) / Decimal(10), Decimal("0.3"))

        return liquidity_risk + spread_risk + freshness_risk
