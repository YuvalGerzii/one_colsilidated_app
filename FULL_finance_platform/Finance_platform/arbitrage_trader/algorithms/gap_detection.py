"""
Gap detection algorithms for identifying various types of arbitrage gaps.
"""
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import uuid
import numpy as np

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class GapDetector:
    """Detects various types of arbitrage gaps."""

    def __init__(self, config: dict = None):
        """
        Initialize gap detector.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}
        self.min_gap_threshold = Decimal(self.config.get("min_gap_threshold", "0.001"))

    def detect_price_gaps(
        self,
        market_data_list: List[MarketData]
    ) -> List[Dict]:
        """
        Detect price gaps across markets.

        Args:
            market_data_list: Market data from multiple sources

        Returns:
            List of detected price gaps
        """
        gaps = []

        # Group by symbol
        symbol_groups: Dict[str, List[MarketData]] = {}
        for data in market_data_list:
            if data.symbol not in symbol_groups:
                symbol_groups[data.symbol] = []
            symbol_groups[data.symbol].append(data)

        # Detect gaps within each symbol
        for symbol, data_list in symbol_groups.items():
            if len(data_list) < 2:
                continue

            # Compare all pairs
            for i in range(len(data_list)):
                for j in range(i + 1, len(data_list)):
                    data1 = data_list[i]
                    data2 = data_list[j]

                    # Calculate gap
                    gap_info = self._calculate_price_gap(data1, data2)

                    if gap_info and gap_info["gap_percentage"] >= self.min_gap_threshold:
                        gaps.append({
                            "symbol": symbol,
                            "gap_type": "price_gap",
                            "exchange1": data1.exchange,
                            "exchange2": data2.exchange,
                            "price1": float(data1.mid_price),
                            "price2": float(data2.mid_price),
                            "gap_amount": float(gap_info["gap_amount"]),
                            "gap_percentage": float(gap_info["gap_percentage"]),
                            "direction": gap_info["direction"],
                            "exploitable": gap_info["exploitable"],
                            "timestamp": datetime.now()
                        })

        return gaps

    def _calculate_price_gap(
        self,
        data1: MarketData,
        data2: MarketData
    ) -> Optional[Dict]:
        """Calculate price gap between two market data points."""
        mid1 = data1.mid_price
        mid2 = data2.mid_price

        gap_amount = mid2 - mid1
        gap_percentage = (abs(gap_amount) / mid1) * Decimal(100) if mid1 > 0 else Decimal(0)

        # Determine if gap is exploitable (considering spreads)
        combined_spread = data1.spread + data2.spread
        exploitable = abs(gap_amount) > combined_spread

        direction = "data2_higher" if gap_amount > 0 else "data1_higher"

        return {
            "gap_amount": gap_amount,
            "gap_percentage": gap_percentage,
            "direction": direction,
            "exploitable": exploitable,
            "spread1": data1.spread,
            "spread2": data2.spread
        }

    def detect_temporal_gaps(
        self,
        current_data: MarketData,
        historical_data: List[MarketData]
    ) -> List[Dict]:
        """
        Detect temporal gaps (price jumps over time).

        Args:
            current_data: Current market data
            historical_data: Historical market data

        Returns:
            List of detected temporal gaps
        """
        if not historical_data:
            return []

        gaps = []

        # Get most recent historical data
        recent_data = historical_data[-1]

        # Calculate price change
        price_change = current_data.mid_price - recent_data.mid_price
        price_change_pct = (price_change / recent_data.mid_price) * Decimal(100) \
            if recent_data.mid_price > 0 else Decimal(0)

        # Calculate time gap
        time_gap = current_data.timestamp - recent_data.timestamp

        # Check for significant price jump
        if abs(price_change_pct) > Decimal("0.5"):  # More than 0.5% move
            gap_type = "price_jump_up" if price_change > 0 else "price_jump_down"

            gaps.append({
                "symbol": current_data.symbol,
                "exchange": current_data.exchange,
                "gap_type": gap_type,
                "price_change": float(price_change),
                "price_change_pct": float(price_change_pct),
                "time_gap_seconds": time_gap.total_seconds(),
                "previous_price": float(recent_data.mid_price),
                "current_price": float(current_data.mid_price),
                "severity": self._classify_gap_severity(abs(price_change_pct)),
                "timestamp": current_data.timestamp
            })

        # Check for volume gaps
        current_volume = current_data.bid_volume + current_data.ask_volume
        recent_volume = recent_data.bid_volume + recent_data.ask_volume

        if recent_volume > 0:
            volume_change_pct = ((current_volume - recent_volume) / recent_volume) * Decimal(100)

            if abs(volume_change_pct) > Decimal("100"):  # Volume doubled or halved
                gaps.append({
                    "symbol": current_data.symbol,
                    "exchange": current_data.exchange,
                    "gap_type": "volume_gap",
                    "volume_change_pct": float(volume_change_pct),
                    "previous_volume": float(recent_volume),
                    "current_volume": float(current_volume),
                    "severity": "high" if abs(volume_change_pct) > Decimal("200") else "medium",
                    "timestamp": current_data.timestamp
                })

        return gaps

    def detect_liquidity_gaps(
        self,
        market_data: MarketData
    ) -> List[Dict]:
        """
        Detect liquidity gaps (imbalances in order book).

        Args:
            market_data: Market data

        Returns:
            List of detected liquidity gaps
        """
        gaps = []

        total_volume = market_data.bid_volume + market_data.ask_volume

        if total_volume == 0:
            return gaps

        # Calculate liquidity imbalance
        imbalance = (market_data.bid_volume - market_data.ask_volume) / total_volume
        imbalance_pct = imbalance * Decimal(100)

        # Significant imbalance
        if abs(imbalance_pct) > Decimal("30"):  # More than 30% imbalance
            side = "bid_heavy" if imbalance > 0 else "ask_heavy"

            gaps.append({
                "symbol": market_data.symbol,
                "exchange": market_data.exchange,
                "gap_type": "liquidity_imbalance",
                "imbalance_pct": float(imbalance_pct),
                "side": side,
                "bid_volume": float(market_data.bid_volume),
                "ask_volume": float(market_data.ask_volume),
                "severity": self._classify_imbalance_severity(abs(imbalance_pct)),
                "predicted_direction": "up" if side == "bid_heavy" else "down",
                "timestamp": market_data.timestamp
            })

        # Check for low absolute liquidity
        if total_volume < Decimal("10"):  # Very low liquidity threshold
            gaps.append({
                "symbol": market_data.symbol,
                "exchange": market_data.exchange,
                "gap_type": "low_liquidity",
                "total_volume": float(total_volume),
                "severity": "high",
                "risk": "high_slippage",
                "timestamp": market_data.timestamp
            })

        return gaps

    def detect_spread_gaps(
        self,
        market_data_list: List[MarketData]
    ) -> List[Dict]:
        """
        Detect abnormal spread gaps.

        Args:
            market_data_list: List of market data

        Returns:
            List of detected spread gaps
        """
        gaps = []

        # Group by symbol
        symbol_groups: Dict[str, List[MarketData]] = {}
        for data in market_data_list:
            if data.symbol not in symbol_groups:
                symbol_groups[data.symbol] = []
            symbol_groups[data.symbol].append(data)

        for symbol, data_list in symbol_groups.items():
            if len(data_list) < 2:
                continue

            # Calculate spread statistics
            spreads = [data.spread_percentage for data in data_list]
            avg_spread = sum(spreads) / len(spreads)
            max_spread = max(spreads)
            min_spread = min(spreads)

            # Detect abnormal spreads
            for data in data_list:
                # Spread significantly wider than average
                if data.spread_percentage > avg_spread * Decimal("2"):
                    gaps.append({
                        "symbol": symbol,
                        "exchange": data.exchange,
                        "gap_type": "wide_spread",
                        "spread_pct": float(data.spread_percentage),
                        "avg_spread_pct": float(avg_spread),
                        "deviation_factor": float(data.spread_percentage / avg_spread),
                        "severity": "high" if data.spread_percentage > avg_spread * 3 else "medium",
                        "implication": "low_liquidity_or_high_volatility",
                        "timestamp": data.timestamp
                    })

            # Detect spread dispersion across exchanges
            if len(data_list) > 1:
                spread_range = max_spread - min_spread
                spread_dispersion = (spread_range / avg_spread) * Decimal(100) if avg_spread > 0 else Decimal(0)

                if spread_dispersion > Decimal("50"):  # Spreads vary by more than 50%
                    gaps.append({
                        "symbol": symbol,
                        "gap_type": "spread_dispersion",
                        "spread_range_pct": float(spread_range),
                        "dispersion_pct": float(spread_dispersion),
                        "min_spread": float(min_spread),
                        "max_spread": float(max_spread),
                        "avg_spread": float(avg_spread),
                        "exchanges": [data.exchange for data in data_list],
                        "severity": "medium",
                        "opportunity": "potential_arbitrage",
                        "timestamp": datetime.now()
                    })

        return gaps

    def detect_correlation_gaps(
        self,
        asset1_data: List[MarketData],
        asset2_data: List[MarketData],
        expected_correlation: float = 0.9
    ) -> List[Dict]:
        """
        Detect gaps in correlated asset pairs.

        Args:
            asset1_data: Price data for first asset
            asset2_data: Price data for second asset
            expected_correlation: Expected correlation between assets

        Returns:
            List of detected correlation gaps
        """
        if len(asset1_data) < 10 or len(asset2_data) < 10:
            return []

        gaps = []

        # Get prices
        prices1 = np.array([float(d.mid_price) for d in asset1_data])
        prices2 = np.array([float(d.mid_price) for d in asset2_data])

        # Ensure same length
        min_len = min(len(prices1), len(prices2))
        prices1 = prices1[-min_len:]
        prices2 = prices2[-min_len:]

        # Calculate correlation
        correlation = np.corrcoef(prices1, prices2)[0, 1]

        # Detect correlation breakdown
        if abs(correlation) < expected_correlation * 0.7:  # Significant deviation
            gaps.append({
                "gap_type": "correlation_breakdown",
                "asset1": asset1_data[0].symbol,
                "asset2": asset2_data[0].symbol,
                "current_correlation": float(correlation),
                "expected_correlation": expected_correlation,
                "deviation": float(expected_correlation - abs(correlation)),
                "severity": "high" if abs(correlation) < 0.5 else "medium",
                "opportunity": "pairs_trading_reversal",
                "timestamp": datetime.now()
            })

        # Calculate spread between normalized prices
        norm_prices1 = (prices1 - np.mean(prices1)) / np.std(prices1)
        norm_prices2 = (prices2 - np.mean(prices2)) / np.std(prices2)
        spread = norm_prices1 - norm_prices2

        current_spread = spread[-1]
        mean_spread = np.mean(spread)
        std_spread = np.std(spread)

        # Z-score of current spread
        if std_spread > 0:
            z_score = (current_spread - mean_spread) / std_spread

            # Significant deviation from mean spread
            if abs(z_score) > 2:
                gaps.append({
                    "gap_type": "spread_deviation",
                    "asset1": asset1_data[0].symbol,
                    "asset2": asset2_data[0].symbol,
                    "z_score": float(z_score),
                    "current_spread": float(current_spread),
                    "mean_spread": float(mean_spread),
                    "std_spread": float(std_spread),
                    "severity": "high" if abs(z_score) > 3 else "medium",
                    "predicted_reversion": "mean_reversion_expected",
                    "timestamp": datetime.now()
                })

        return gaps

    def _classify_gap_severity(self, gap_pct: Decimal) -> str:
        """Classify gap severity."""
        if gap_pct > Decimal("5"):
            return "critical"
        elif gap_pct > Decimal("2"):
            return "high"
        elif gap_pct > Decimal("1"):
            return "medium"
        else:
            return "low"

    def _classify_imbalance_severity(self, imbalance_pct: Decimal) -> str:
        """Classify imbalance severity."""
        if imbalance_pct > Decimal("70"):
            return "critical"
        elif imbalance_pct > Decimal("50"):
            return "high"
        else:
            return "medium"

    def generate_gap_opportunities(
        self,
        gaps: List[Dict]
    ) -> List[ArbitrageOpportunity]:
        """
        Generate arbitrage opportunities from detected gaps.

        Args:
            gaps: List of detected gaps

        Returns:
            List of arbitrage opportunities
        """
        opportunities = []

        for gap in gaps:
            # Only create opportunities for exploitable gaps
            if gap["gap_type"] == "price_gap" and gap.get("exploitable", False):
                opportunity = self._create_price_gap_opportunity(gap)
                if opportunity:
                    opportunities.append(opportunity)

            elif gap["gap_type"] in ["price_jump_up", "price_jump_down"]:
                opportunity = self._create_momentum_opportunity(gap)
                if opportunity:
                    opportunities.append(opportunity)

            elif gap["gap_type"] == "liquidity_imbalance":
                opportunity = self._create_imbalance_opportunity(gap)
                if opportunity:
                    opportunities.append(opportunity)

        return opportunities

    def _create_price_gap_opportunity(self, gap: Dict) -> Optional[ArbitrageOpportunity]:
        """Create opportunity from price gap."""
        # Implementation would create a cross-exchange arbitrage opportunity
        # Simplified for brevity
        return None

    def _create_momentum_opportunity(self, gap: Dict) -> Optional[ArbitrageOpportunity]:
        """Create opportunity from price jump (momentum)."""
        # Implementation would create a momentum trading opportunity
        return None

    def _create_imbalance_opportunity(self, gap: Dict) -> Optional[ArbitrageOpportunity]:
        """Create opportunity from liquidity imbalance."""
        # Implementation would create an order book imbalance opportunity
        return None
