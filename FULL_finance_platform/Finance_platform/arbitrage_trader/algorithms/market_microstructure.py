"""
Market microstructure analysis algorithms.
Analyzes market efficiency, price discovery, liquidity, and transaction costs.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
from collections import deque

from ..models.types import MarketData, ArbitrageOpportunity


class MicrostructureAnalyzer:
    """Analyzes market microstructure for inefficiencies and opportunities."""

    def __init__(self, config: dict = None):
        """
        Initialize microstructure analyzer.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}

        # Historical data storage
        self.price_history: Dict[str, deque] = {}
        self.trade_history: Dict[str, deque] = {}
        self.quote_history: Dict[str, deque] = {}

        self.max_history = self.config.get("max_history", 1000)

    def calculate_effective_spread(
        self,
        trade_price: Decimal,
        mid_quote: Decimal,
        side: str
    ) -> Decimal:
        """
        Calculate effective spread.

        Effective Spread = 2 * |trade_price - mid_quote|

        Args:
            trade_price: Actual execution price
            mid_quote: Mid-quote at time of trade
            side: 'buy' or 'sell'

        Returns:
            Effective spread
        """
        return 2 * abs(trade_price - mid_quote)

    def calculate_realized_spread(
        self,
        trade_price: Decimal,
        mid_quote_at_trade: Decimal,
        mid_quote_after: Decimal,
        side: str
    ) -> Decimal:
        """
        Calculate realized spread (measures immediacy cost).

        For buy: Realized Spread = 2 * (trade_price - mid_quote_after)
        For sell: Realized Spread = 2 * (mid_quote_after - trade_price)

        Args:
            trade_price: Execution price
            mid_quote_at_trade: Mid-quote at execution
            mid_quote_after: Mid-quote after some time (e.g., 5 min)
            side: 'buy' or 'sell'

        Returns:
            Realized spread
        """
        if side == "buy":
            return 2 * (trade_price - mid_quote_after)
        else:
            return 2 * (mid_quote_after - trade_price)

    def calculate_price_impact(
        self,
        pre_trade_mid: Decimal,
        post_trade_mid: Decimal,
        side: str
    ) -> Decimal:
        """
        Calculate permanent price impact.

        Impact = (post_trade_mid - pre_trade_mid) * direction

        Args:
            pre_trade_mid: Mid-quote before trade
            post_trade_mid: Mid-quote after trade
            side: 'buy' or 'sell'

        Returns:
            Price impact
        """
        direction = Decimal(1) if side == "buy" else Decimal(-1)
        return (post_trade_mid - pre_trade_mid) * direction

    def calculate_amihud_illiquidity(
        self,
        price_changes: List[Decimal],
        volumes: List[Decimal]
    ) -> Decimal:
        """
        Calculate Amihud illiquidity measure.

        ILLIQ = average(|return| / volume)

        Higher values indicate lower liquidity.

        Args:
            price_changes: List of price changes (returns)
            volumes: List of trading volumes

        Returns:
            Illiquidity measure
        """
        if not price_changes or not volumes or len(price_changes) != len(volumes):
            return Decimal(0)

        illiquidity_values = []

        for price_change, volume in zip(price_changes, volumes):
            if volume > 0:
                illiq = abs(price_change) / volume
                illiquidity_values.append(illiq)

        if not illiquidity_values:
            return Decimal(0)

        return sum(illiquidity_values) / len(illiquidity_values)

    def calculate_roll_spread(
        self,
        price_changes: List[Decimal]
    ) -> Decimal:
        """
        Calculate Roll's spread estimator.

        Roll Spread = 2 * sqrt(-cov(ΔP_t, ΔP_{t-1}))

        Based on bid-ask bounce causing negative serial correlation.

        Args:
            price_changes: List of consecutive price changes

        Returns:
            Estimated spread
        """
        if len(price_changes) < 2:
            return Decimal(0)

        # Calculate autocovariance
        price_changes_array = np.array([float(pc) for pc in price_changes])

        # Lag-1 autocovariance
        autocov = np.cov(price_changes_array[:-1], price_changes_array[1:])[0, 1]

        if autocov >= 0:
            # Roll's model assumes negative autocov due to bid-ask bounce
            return Decimal(0)

        spread = 2 * Decimal(str(np.sqrt(abs(autocov))))

        return spread

    def calculate_kyle_lambda(
        self,
        price_changes: List[Decimal],
        order_flows: List[Decimal]
    ) -> Decimal:
        """
        Calculate Kyle's lambda (measure of adverse selection).

        Lambda measures how much price moves per unit of order flow.
        ΔP = λ * Q + noise

        Args:
            price_changes: List of price changes
            order_flows: List of signed order flows (positive for buys)

        Returns:
            Kyle's lambda
        """
        if not price_changes or not order_flows or len(price_changes) != len(order_flows):
            return Decimal(0)

        # Simple linear regression: price_change ~ order_flow
        price_array = np.array([float(p) for p in price_changes])
        flow_array = np.array([float(f) for f in order_flows])

        if len(price_array) < 2:
            return Decimal(0)

        # Calculate lambda as covariance / variance
        covariance = np.cov(price_array, flow_array)[0, 1]
        variance = np.var(flow_array)

        if variance == 0:
            return Decimal(0)

        lambda_value = covariance / variance

        return Decimal(str(lambda_value))

    def detect_quote_stuffing(
        self,
        quote_updates: List[Dict],
        time_window: timedelta = timedelta(seconds=1)
    ) -> Dict:
        """
        Detect quote stuffing (excessive quote updates).

        Quote stuffing floods the market with orders to slow down competitors.

        Args:
            quote_updates: List of quote updates with {'timestamp', 'type', ...}
            time_window: Time window to analyze

        Returns:
            Detection results
        """
        if not quote_updates:
            return {"detected": False, "rate": 0, "severity": "none"}

        # Sort by timestamp
        sorted_updates = sorted(quote_updates, key=lambda x: x['timestamp'])

        # Count updates per time window
        window_counts = []
        start_idx = 0

        for i, update in enumerate(sorted_updates):
            # Find all updates within time window
            window_end = update['timestamp'] + time_window

            while start_idx < len(sorted_updates):
                if sorted_updates[start_idx]['timestamp'] < update['timestamp']:
                    start_idx += 1
                else:
                    break

            # Count updates in window
            count = 0
            for j in range(start_idx, len(sorted_updates)):
                if sorted_updates[j]['timestamp'] <= window_end:
                    count += 1
                else:
                    break

            window_counts.append(count)

        if not window_counts:
            return {"detected": False, "rate": 0, "severity": "none"}

        max_rate = max(window_counts)
        avg_rate = sum(window_counts) / len(window_counts)

        # Thresholds (updates per second)
        # Normal: < 10, Suspicious: 10-50, High: 50-100, Critical: > 100
        if max_rate > 100:
            severity = "critical"
            detected = True
        elif max_rate > 50:
            severity = "high"
            detected = True
        elif max_rate > 10:
            severity = "suspicious"
            detected = True
        else:
            severity = "normal"
            detected = False

        return {
            "detected": detected,
            "max_rate": max_rate,
            "avg_rate": avg_rate,
            "severity": severity
        }

    def calculate_variance_ratio(
        self,
        prices: List[Decimal],
        short_period: int = 1,
        long_period: int = 10
    ) -> Decimal:
        """
        Calculate variance ratio test for market efficiency.

        VR = Var(long_period_returns) / (long_period * Var(short_period_returns))

        VR = 1 indicates random walk (efficient market)
        VR < 1 indicates mean reversion
        VR > 1 indicates momentum/trending

        Args:
            prices: Price series
            short_period: Short period (typically 1)
            long_period: Long period (typically 5-10)

        Returns:
            Variance ratio
        """
        if len(prices) < long_period + 1:
            return Decimal(1)

        prices_array = np.array([float(p) for p in prices])

        # Calculate short period returns
        short_returns = np.diff(prices_array, n=short_period)

        # Calculate long period returns
        long_returns = np.diff(prices_array, n=long_period)

        if len(short_returns) < 2 or len(long_returns) < 2:
            return Decimal(1)

        # Calculate variances
        var_short = np.var(short_returns)
        var_long = np.var(long_returns)

        if var_short == 0:
            return Decimal(1)

        variance_ratio = Decimal(str(var_long / (long_period * var_short)))

        return variance_ratio

    def detect_price_discovery_inefficiency(
        self,
        market_data_list: List[MarketData]
    ) -> Dict:
        """
        Detect price discovery inefficiencies across markets.

        Args:
            market_data_list: Market data from different sources

        Returns:
            Analysis results
        """
        if len(market_data_list) < 2:
            return {"inefficiency_detected": False}

        # Group by symbol
        symbol_groups: Dict[str, List[MarketData]] = {}
        for data in market_data_list:
            if data.symbol not in symbol_groups:
                symbol_groups[data.symbol] = []
            symbol_groups[data.symbol].append(data)

        inefficiencies = []

        for symbol, data_list in symbol_groups.items():
            if len(data_list) < 2:
                continue

            # Calculate price dispersion
            mid_prices = [data.mid_price for data in data_list]
            avg_price = sum(mid_prices) / len(mid_prices)

            # Calculate coefficient of variation
            std_dev = Decimal(str(np.std([float(p) for p in mid_prices])))
            cv = (std_dev / avg_price) * 100 if avg_price > 0 else Decimal(0)

            # Check timestamp differences (stale prices indicate inefficiency)
            timestamps = [data.timestamp for data in data_list]
            max_time_diff = max(timestamps) - min(timestamps)

            if cv > Decimal("0.1") or max_time_diff.total_seconds() > 5:
                inefficiencies.append({
                    "symbol": symbol,
                    "price_dispersion_pct": float(cv),
                    "max_time_lag_seconds": max_time_diff.total_seconds(),
                    "exchanges": [data.exchange for data in data_list],
                    "severity": "high" if cv > Decimal("0.5") else "medium"
                })

        return {
            "inefficiency_detected": len(inefficiencies) > 0,
            "inefficiencies": inefficiencies,
            "count": len(inefficiencies)
        }

    def calculate_market_quality_score(
        self,
        market_data: MarketData,
        recent_trades: List[Dict] = None
    ) -> Dict:
        """
        Calculate comprehensive market quality score.

        Considers:
        - Spread
        - Depth
        - Volatility
        - Trading activity
        - Quote quality

        Args:
            market_data: Current market data
            recent_trades: Recent trades

        Returns:
            Quality metrics
        """
        scores = {}

        # 1. Spread Score (tighter = better)
        spread_pct = market_data.spread_percentage
        spread_score = max(Decimal(0), Decimal(1) - spread_pct / 2)
        scores['spread_score'] = float(spread_score)

        # 2. Depth Score (higher liquidity = better)
        total_depth = market_data.bid_volume + market_data.ask_volume
        depth_score = min(total_depth / Decimal(1000), Decimal(1))
        scores['depth_score'] = float(depth_score)

        # 3. Balance Score (balanced book = better)
        if total_depth > 0:
            balance = abs(market_data.bid_volume - market_data.ask_volume) / total_depth
            balance_score = Decimal(1) - min(balance, Decimal(1))
        else:
            balance_score = Decimal(0)
        scores['balance_score'] = float(balance_score)

        # 4. Freshness Score (recent data = better)
        age_seconds = (datetime.now() - market_data.timestamp).total_seconds()
        freshness_score = max(Decimal(0), Decimal(1) - Decimal(age_seconds) / 10)
        scores['freshness_score'] = float(freshness_score)

        # 5. Activity Score (more trades = better, if provided)
        if recent_trades:
            activity_score = min(Decimal(len(recent_trades)) / 100, Decimal(1))
        else:
            activity_score = Decimal(0.5)  # Neutral if unknown
        scores['activity_score'] = float(activity_score)

        # Overall quality score (weighted average)
        overall_score = (
            spread_score * Decimal("0.3") +
            depth_score * Decimal("0.25") +
            balance_score * Decimal("0.2") +
            freshness_score * Decimal("0.15") +
            activity_score * Decimal("0.1")
        )

        scores['overall_quality'] = float(overall_score)
        scores['rating'] = self._get_quality_rating(overall_score)

        return scores

    def _get_quality_rating(self, score: Decimal) -> str:
        """Get quality rating from score."""
        if score >= Decimal("0.8"):
            return "excellent"
        elif score >= Decimal("0.6"):
            return "good"
        elif score >= Decimal("0.4"):
            return "fair"
        elif score >= Decimal("0.2"):
            return "poor"
        else:
            return "very_poor"

    def analyze_transaction_costs(
        self,
        market_data: MarketData,
        target_volume: Decimal,
        side: str
    ) -> Dict:
        """
        Analyze expected transaction costs.

        Args:
            market_data: Market data
            target_volume: Target execution volume
            side: 'buy' or 'sell'

        Returns:
            Cost analysis
        """
        # 1. Explicit costs (spread)
        spread_cost = market_data.spread / 2

        # 2. Estimated slippage (simplified)
        available_volume = (
            market_data.ask_volume if side == "buy" else market_data.bid_volume
        )

        if available_volume == 0:
            slippage_pct = Decimal(10)  # Very high if no liquidity
        else:
            liquidity_ratio = target_volume / available_volume
            slippage_pct = liquidity_ratio * market_data.spread_percentage

        # 3. Market impact (simplified)
        market_impact_pct = slippage_pct * Decimal("0.5")

        # 4. Total expected cost
        total_cost_pct = (
            market_data.spread_percentage / 2 +
            slippage_pct +
            market_impact_pct
        )

        return {
            "spread_cost": float(spread_cost),
            "spread_cost_pct": float(market_data.spread_percentage / 2),
            "estimated_slippage_pct": float(slippage_pct),
            "estimated_market_impact_pct": float(market_impact_pct),
            "total_cost_pct": float(total_cost_pct),
            "executable": available_volume >= target_volume,
            "liquidity_adequacy": float(available_volume / target_volume) if target_volume > 0 else 0
        }
