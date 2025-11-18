"""
Statistical arbitrage detection algorithms.
Includes pairs trading and mean reversion strategies.
"""
from typing import List, Dict, Tuple, Optional
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


class StatisticalArbitrageDetector:
    """Detects statistical arbitrage opportunities using pairs trading and mean reversion."""

    def __init__(
        self,
        lookback_period: int = 20,
        z_score_entry_threshold: float = 2.0,
        z_score_exit_threshold: float = 0.5,
        correlation_threshold: float = 0.7
    ):
        """
        Initialize statistical arbitrage detector.

        Args:
            lookback_period: Number of periods to use for calculating statistics
            z_score_entry_threshold: Z-score threshold for entering trades
            z_score_exit_threshold: Z-score threshold for exiting trades
            correlation_threshold: Minimum correlation for pair selection
        """
        self.lookback_period = lookback_period
        self.z_score_entry_threshold = z_score_entry_threshold
        self.z_score_exit_threshold = z_score_exit_threshold
        self.correlation_threshold = correlation_threshold

        # Historical price data storage
        self.price_history: Dict[str, deque] = {}

    def detect_opportunities(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Detect statistical arbitrage opportunities.

        Args:
            market_data: List of market data

        Returns:
            List of arbitrage opportunities
        """
        opportunities = []

        # Update price history
        self._update_price_history(market_data)

        # Find cointegrated pairs
        pairs = self._find_pairs(market_data)

        for pair in pairs:
            symbol1, symbol2 = pair
            data1 = next((d for d in market_data if d.symbol == symbol1), None)
            data2 = next((d for d in market_data if d.symbol == symbol2), None)

            if not data1 or not data2:
                continue

            # Calculate spread and z-score
            spread_info = self._calculate_spread_zscore(symbol1, symbol2)

            if not spread_info:
                continue

            z_score, spread, hedge_ratio = spread_info

            # Check for entry signals
            if abs(z_score) >= self.z_score_entry_threshold:
                opportunity = self._create_pairs_opportunity(
                    data1, data2, z_score, spread, hedge_ratio
                )
                if opportunity:
                    opportunities.append(opportunity)

        # Mean reversion opportunities for individual symbols
        mean_reversion_opps = self._detect_mean_reversion(market_data)
        opportunities.extend(mean_reversion_opps)

        return opportunities

    def _update_price_history(self, market_data: List[MarketData]):
        """Update historical price data."""
        for data in market_data:
            if data.symbol not in self.price_history:
                self.price_history[data.symbol] = deque(maxlen=self.lookback_period)

            self.price_history[data.symbol].append({
                'timestamp': data.timestamp,
                'price': float(data.mid_price),
                'volume': float(data.bid_volume + data.ask_volume) / 2
            })

    def _find_pairs(self, market_data: List[MarketData]) -> List[Tuple[str, str]]:
        """
        Find pairs of symbols for pairs trading.

        In a real implementation, this would use cointegration tests.
        For now, we use a simplified correlation-based approach.
        """
        pairs = []
        symbols = [d.symbol for d in market_data]

        # Check if we have enough historical data
        valid_symbols = [
            s for s in symbols
            if s in self.price_history and len(self.price_history[s]) >= self.lookback_period
        ]

        for i, symbol1 in enumerate(valid_symbols):
            for symbol2 in valid_symbols[i + 1:]:
                # Calculate correlation
                prices1 = [p['price'] for p in self.price_history[symbol1]]
                prices2 = [p['price'] for p in self.price_history[symbol2]]

                if len(prices1) < 2 or len(prices2) < 2:
                    continue

                correlation = np.corrcoef(prices1, prices2)[0, 1]

                if abs(correlation) >= self.correlation_threshold:
                    pairs.append((symbol1, symbol2))

        return pairs

    def _calculate_spread_zscore(
        self,
        symbol1: str,
        symbol2: str
    ) -> Optional[Tuple[float, float, float]]:
        """
        Calculate spread and z-score for a pair.

        Returns:
            Tuple of (z_score, current_spread, hedge_ratio) or None
        """
        if (symbol1 not in self.price_history or
            symbol2 not in self.price_history or
            len(self.price_history[symbol1]) < self.lookback_period or
            len(self.price_history[symbol2]) < self.lookback_period):
            return None

        prices1 = np.array([p['price'] for p in self.price_history[symbol1]])
        prices2 = np.array([p['price'] for p in self.price_history[symbol2]])

        # Calculate hedge ratio using linear regression
        hedge_ratio = np.polyfit(prices2, prices1, 1)[0]

        # Calculate spread
        spread = prices1 - hedge_ratio * prices2

        # Calculate z-score
        mean_spread = np.mean(spread)
        std_spread = np.std(spread)

        if std_spread == 0:
            return None

        current_spread = spread[-1]
        z_score = (current_spread - mean_spread) / std_spread

        return (float(z_score), float(current_spread), float(hedge_ratio))

    def _create_pairs_opportunity(
        self,
        data1: MarketData,
        data2: MarketData,
        z_score: float,
        spread: float,
        hedge_ratio: float
    ) -> Optional[ArbitrageOpportunity]:
        """Create a pairs trading opportunity."""
        # If z-score is positive, short symbol1 and long symbol2
        # If z-score is negative, long symbol1 and short symbol2

        if z_score > 0:
            # Spread is above mean: short symbol1, long symbol2
            action1_side = OrderSide.SELL
            action2_side = OrderSide.BUY
        else:
            # Spread is below mean: long symbol1, short symbol2
            action1_side = OrderSide.BUY
            action2_side = OrderSide.SELL

        # Calculate position sizes based on hedge ratio
        base_quantity = Decimal(100)  # Base position size
        quantity1 = base_quantity
        quantity2 = base_quantity * Decimal(str(abs(hedge_ratio)))

        # Calculate expected profit (simplified)
        expected_profit_pct = Decimal(abs(z_score)) * Decimal("0.5")  # Rough estimate

        # Calculate confidence based on z-score magnitude and historical stats
        confidence = min(Decimal(abs(z_score)) / Decimal(5), Decimal("0.95"))

        # Calculate risk
        risk = Decimal("0.3") + min(Decimal(abs(z_score)) / Decimal(10), Decimal("0.2"))

        opportunity = ArbitrageOpportunity(
            opportunity_id=str(uuid.uuid4()),
            arbitrage_type=ArbitrageType.STATISTICAL,
            market_type=data1.market_type,
            symbol=f"{data1.symbol}/{data2.symbol}",
            timestamp=datetime.now(),
            expected_profit=expected_profit_pct * base_quantity,
            expected_profit_percentage=expected_profit_pct,
            confidence_score=confidence,
            risk_score=risk,
            detection_latency_ms=0,
            market_data=[data1, data2],
            suggested_actions=[
                TradingAction(
                    action_id=f"{str(uuid.uuid4())}-1",
                    exchange=data1.exchange,
                    symbol=data1.symbol,
                    side=action1_side,
                    quantity=quantity1,
                    price=data1.ask_price if action1_side == OrderSide.BUY else data1.bid_price,
                    order_type="market",
                    priority=1
                ),
                TradingAction(
                    action_id=f"{str(uuid.uuid4())}-2",
                    exchange=data2.exchange,
                    symbol=data2.symbol,
                    side=action2_side,
                    quantity=quantity2,
                    price=data2.ask_price if action2_side == OrderSide.BUY else data2.bid_price,
                    order_type="market",
                    priority=1
                )
            ],
            metadata={
                "z_score": z_score,
                "spread": spread,
                "hedge_ratio": hedge_ratio,
                "strategy": "pairs_trading"
            }
        )

        return opportunity

    def _detect_mean_reversion(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """Detect mean reversion opportunities for individual symbols."""
        opportunities = []

        for data in market_data:
            if (data.symbol not in self.price_history or
                len(self.price_history[data.symbol]) < self.lookback_period):
                continue

            prices = np.array([p['price'] for p in self.price_history[data.symbol]])
            current_price = float(data.mid_price)

            # Calculate Bollinger Bands
            mean_price = np.mean(prices)
            std_price = np.std(prices)

            if std_price == 0:
                continue

            upper_band = mean_price + 2 * std_price
            lower_band = mean_price - 2 * std_price

            # Check for mean reversion signals
            if current_price > upper_band:
                # Price above upper band - potential short opportunity
                z_score = (current_price - mean_price) / std_price
                opportunity = self._create_mean_reversion_opportunity(
                    data, OrderSide.SELL, z_score, mean_price
                )
                if opportunity:
                    opportunities.append(opportunity)

            elif current_price < lower_band:
                # Price below lower band - potential long opportunity
                z_score = (current_price - mean_price) / std_price
                opportunity = self._create_mean_reversion_opportunity(
                    data, OrderSide.BUY, abs(z_score), mean_price
                )
                if opportunity:
                    opportunities.append(opportunity)

        return opportunities

    def _create_mean_reversion_opportunity(
        self,
        data: MarketData,
        side: OrderSide,
        z_score: float,
        mean_price: float
    ) -> Optional[ArbitrageOpportunity]:
        """Create a mean reversion opportunity."""
        current_price = float(data.mid_price)
        expected_price_move = abs(current_price - mean_price) * 0.5  # Expect 50% reversion

        expected_profit_pct = Decimal(expected_price_move / current_price * 100)
        confidence = min(Decimal(z_score) / Decimal(4), Decimal("0.9"))
        risk = Decimal("0.4")

        base_quantity = Decimal(50)

        opportunity = ArbitrageOpportunity(
            opportunity_id=str(uuid.uuid4()),
            arbitrage_type=ArbitrageType.STATISTICAL,
            market_type=data.market_type,
            symbol=data.symbol,
            timestamp=datetime.now(),
            expected_profit=expected_profit_pct * base_quantity,
            expected_profit_percentage=expected_profit_pct,
            confidence_score=confidence,
            risk_score=risk,
            detection_latency_ms=0,
            market_data=[data],
            suggested_actions=[
                TradingAction(
                    action_id=str(uuid.uuid4()),
                    exchange=data.exchange,
                    symbol=data.symbol,
                    side=side,
                    quantity=base_quantity,
                    price=data.ask_price if side == OrderSide.BUY else data.bid_price,
                    order_type="limit",
                    priority=1
                )
            ],
            metadata={
                "z_score": z_score,
                "mean_price": mean_price,
                "current_price": current_price,
                "strategy": "mean_reversion"
            }
        )

        return opportunity
