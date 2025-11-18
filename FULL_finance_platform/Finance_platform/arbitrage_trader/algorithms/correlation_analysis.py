"""
Correlation analysis for multi-asset arbitrage and risk management.
"""
from typing import List, Dict, Tuple, Optional
from decimal import Decimal
from datetime import datetime
import numpy as np
from scipy import stats
from collections import deque
import uuid

from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    ArbitrageType,
    TradingAction,
    OrderSide
)


class CorrelationAnalyzer:
    """Analyzes correlations between assets for arbitrage and risk management."""

    def __init__(self, config: dict = None):
        """
        Initialize correlation analyzer.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}
        self.lookback_period = self.config.get("lookback_period", 50)

        # Historical price storage
        self.price_history: Dict[str, deque] = {}

        # Correlation matrix cache
        self.correlation_matrix: Dict[Tuple[str, str], Decimal] = {}
        self.last_update: Optional[datetime] = None

    def update_prices(self, market_data: List[MarketData]):
        """
        Update price history with new market data.

        Args:
            market_data: List of market data
        """
        for data in market_data:
            key = f"{data.exchange}:{data.symbol}"

            if key not in self.price_history:
                self.price_history[key] = deque(maxlen=self.lookback_period)

            self.price_history[key].append({
                "timestamp": data.timestamp,
                "price": float(data.mid_price)
            })

    def calculate_correlation(
        self,
        asset1: str,
        asset2: str
    ) -> Optional[Decimal]:
        """
        Calculate correlation between two assets.

        Args:
            asset1: First asset key (exchange:symbol)
            asset2: Second asset key (exchange:symbol)

        Returns:
            Correlation coefficient (-1 to 1) or None
        """
        if (asset1 not in self.price_history or
            asset2 not in self.price_history):
            return None

        prices1 = [p["price"] for p in self.price_history[asset1]]
        prices2 = [p["price"] for p in self.price_history[asset2]]

        if len(prices1) < 2 or len(prices2) < 2:
            return None

        # Align lengths
        min_len = min(len(prices1), len(prices2))
        prices1 = prices1[-min_len:]
        prices2 = prices2[-min_len:]

        # Calculate Pearson correlation
        correlation = np.corrcoef(prices1, prices2)[0, 1]

        return Decimal(str(correlation))

    def calculate_rolling_correlation(
        self,
        asset1: str,
        asset2: str,
        window: int = 20
    ) -> List[Dict]:
        """
        Calculate rolling correlation over time.

        Args:
            asset1: First asset
            asset2: Second asset
            window: Rolling window size

        Returns:
            List of correlation values over time
        """
        if (asset1 not in self.price_history or
            asset2 not in self.price_history):
            return []

        prices1 = [p["price"] for p in self.price_history[asset1]]
        prices2 = [p["price"] for p in self.price_history[asset2]]
        timestamps = [p["timestamp"] for p in self.price_history[asset1]]

        if len(prices1) < window or len(prices2) < window:
            return []

        # Align lengths
        min_len = min(len(prices1), len(prices2))
        prices1 = prices1[-min_len:]
        prices2 = prices2[-min_len:]
        timestamps = timestamps[-min_len:]

        rolling_correlations = []

        for i in range(window, len(prices1)):
            window_prices1 = prices1[i-window:i]
            window_prices2 = prices2[i-window:i]

            corr = np.corrcoef(window_prices1, window_prices2)[0, 1]

            rolling_correlations.append({
                "timestamp": timestamps[i],
                "correlation": float(corr)
            })

        return rolling_correlations

    def build_correlation_matrix(self) -> Dict[Tuple[str, str], Decimal]:
        """
        Build correlation matrix for all assets.

        Returns:
            Dictionary of (asset1, asset2) -> correlation
        """
        assets = list(self.price_history.keys())

        matrix = {}

        for i, asset1 in enumerate(assets):
            for asset2 in assets[i:]:
                if asset1 == asset2:
                    matrix[(asset1, asset2)] = Decimal(1)
                else:
                    corr = self.calculate_correlation(asset1, asset2)
                    if corr is not None:
                        matrix[(asset1, asset2)] = corr
                        matrix[(asset2, asset1)] = corr  # Symmetric

        self.correlation_matrix = matrix
        self.last_update = datetime.now()

        return matrix

    def find_highly_correlated_pairs(
        self,
        threshold: Decimal = Decimal("0.8")
    ) -> List[Dict]:
        """
        Find pairs with high correlation.

        Args:
            threshold: Minimum correlation threshold

        Returns:
            List of highly correlated pairs
        """
        if not self.correlation_matrix:
            self.build_correlation_matrix()

        pairs = []

        processed = set()

        for (asset1, asset2), corr in self.correlation_matrix.items():
            if asset1 == asset2:
                continue

            pair_key = tuple(sorted([asset1, asset2]))
            if pair_key in processed:
                continue

            if abs(corr) >= threshold:
                pairs.append({
                    "asset1": asset1,
                    "asset2": asset2,
                    "correlation": float(corr),
                    "type": "positive" if corr > 0 else "negative"
                })
                processed.add(pair_key)

        # Sort by absolute correlation
        pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

        return pairs

    def detect_correlation_breakdown(
        self,
        asset1: str,
        asset2: str,
        expected_correlation: float = 0.9,
        threshold: float = 0.3
    ) -> Optional[Dict]:
        """
        Detect breakdown in expected correlation.

        Args:
            asset1: First asset
            asset2: Second asset
            expected_correlation: Expected correlation
            threshold: Maximum deviation before flagging

        Returns:
            Breakdown information or None
        """
        current_corr = self.calculate_correlation(asset1, asset2)

        if current_corr is None:
            return None

        deviation = abs(float(current_corr) - expected_correlation)

        if deviation > threshold:
            # Calculate short-term vs long-term correlation
            short_term_prices1 = list(self.price_history[asset1])[-10:]
            short_term_prices2 = list(self.price_history[asset2])[-10:]

            if len(short_term_prices1) >= 2 and len(short_term_prices2) >= 2:
                short_prices1 = [p["price"] for p in short_term_prices1]
                short_prices2 = [p["price"] for p in short_term_prices2]
                short_corr = np.corrcoef(short_prices1, short_prices2)[0, 1]
            else:
                short_corr = float(current_corr)

            return {
                "asset1": asset1,
                "asset2": asset2,
                "expected_correlation": expected_correlation,
                "current_correlation": float(current_corr),
                "short_term_correlation": float(short_corr),
                "deviation": deviation,
                "severity": "high" if deviation > 0.5 else "medium",
                "opportunity": "mean_reversion" if abs(short_corr - expected_correlation) < threshold else "trend_change"
            }

        return None

    def calculate_cointegration(
        self,
        asset1: str,
        asset2: str
    ) -> Optional[Dict]:
        """
        Test for cointegration between two assets.

        Uses Engle-Granger test.

        Args:
            asset1: First asset
            asset2: Second asset

        Returns:
            Cointegration test results
        """
        if (asset1 not in self.price_history or
            asset2 not in self.price_history):
            return None

        prices1 = np.array([p["price"] for p in self.price_history[asset1]])
        prices2 = np.array([p["price"] for p in self.price_history[asset2]])

        if len(prices1) < 20 or len(prices2) < 20:
            return None

        # Align lengths
        min_len = min(len(prices1), len(prices2))
        prices1 = prices1[-min_len:]
        prices2 = prices2[-min_len:]

        # Linear regression to find hedge ratio
        hedge_ratio = np.polyfit(prices2, prices1, 1)[0]

        # Calculate spread
        spread = prices1 - hedge_ratio * prices2

        # Test spread for stationarity (simplified ADF test)
        # In production, use statsmodels.tsa.stattools.adfuller
        spread_mean = np.mean(spread)
        spread_std = np.std(spread)

        # Z-score of current spread
        current_z_score = (spread[-1] - spread_mean) / spread_std if spread_std > 0 else 0

        # Half-life of mean reversion
        spread_lag = spread[:-1]
        spread_ret = spread[1:] - spread_lag
        spread_lag_mean = spread_lag - spread_mean

        if len(spread_lag_mean) > 0:
            slope = np.polyfit(spread_lag_mean, spread_ret, 1)[0]
            half_life = -np.log(2) / slope if slope < 0 else float('inf')
        else:
            half_life = float('inf')

        return {
            "asset1": asset1,
            "asset2": asset2,
            "hedge_ratio": float(hedge_ratio),
            "current_spread": float(spread[-1]),
            "mean_spread": float(spread_mean),
            "spread_std": float(spread_std),
            "z_score": float(current_z_score),
            "half_life": float(half_life),
            "cointegrated": abs(current_z_score) < 3 and half_life < 50,
            "trading_signal": self._get_cointegration_signal(current_z_score)
        }

    def _get_cointegration_signal(self, z_score: float) -> str:
        """Get trading signal from z-score."""
        if z_score > 2:
            return "short_spread"  # Spread too high, short asset1/long asset2
        elif z_score < -2:
            return "long_spread"  # Spread too low, long asset1/short asset2
        elif abs(z_score) < 0.5:
            return "close"  # Near mean, close positions
        else:
            return "hold"

    def find_cointegrated_pairs(
        self,
        min_confidence: float = 0.7
    ) -> List[Dict]:
        """
        Find cointegrated pairs.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            List of cointegrated pairs
        """
        assets = list(self.price_history.keys())
        cointegrated_pairs = []

        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                result = self.calculate_cointegration(asset1, asset2)

                if result and result["cointegrated"]:
                    # Calculate confidence based on half-life and z-score stability
                    confidence = min(1.0, 1.0 / (1.0 + result["half_life"] / 20.0))

                    if confidence >= min_confidence:
                        result["confidence"] = confidence
                        cointegrated_pairs.append(result)

        # Sort by confidence
        cointegrated_pairs.sort(key=lambda x: x["confidence"], reverse=True)

        return cointegrated_pairs

    def calculate_beta(
        self,
        asset: str,
        market_index: str
    ) -> Optional[Decimal]:
        """
        Calculate beta (systematic risk) of asset relative to market.

        Args:
            asset: Asset to analyze
            market_index: Market index/benchmark

        Returns:
            Beta coefficient
        """
        if (asset not in self.price_history or
            market_index not in self.price_history):
            return None

        asset_prices = np.array([p["price"] for p in self.price_history[asset]])
        market_prices = np.array([p["price"] for p in self.price_history[market_index]])

        if len(asset_prices) < 2 or len(market_prices) < 2:
            return None

        # Align lengths
        min_len = min(len(asset_prices), len(market_prices))
        asset_prices = asset_prices[-min_len:]
        market_prices = market_prices[-min_len:]

        # Calculate returns
        asset_returns = np.diff(asset_prices) / asset_prices[:-1]
        market_returns = np.diff(market_prices) / market_prices[:-1]

        # Beta = Cov(asset, market) / Var(market)
        covariance = np.cov(asset_returns, market_returns)[0, 1]
        market_variance = np.var(market_returns)

        if market_variance == 0:
            return None

        beta = covariance / market_variance

        return Decimal(str(beta))

    def detect_divergence(
        self,
        asset1: str,
        asset2: str,
        threshold: float = 2.0
    ) -> Optional[Dict]:
        """
        Detect price divergence in correlated pairs.

        Args:
            asset1: First asset
            asset2: Second asset
            threshold: Z-score threshold for divergence

        Returns:
            Divergence information
        """
        coint_result = self.calculate_cointegration(asset1, asset2)

        if not coint_result:
            return None

        z_score = coint_result["z_score"]

        if abs(z_score) > threshold:
            return {
                "asset1": asset1,
                "asset2": asset2,
                "z_score": z_score,
                "direction": "asset1_overvalued" if z_score > 0 else "asset1_undervalued",
                "magnitude": abs(z_score),
                "severity": "extreme" if abs(z_score) > 3 else "high",
                "expected_convergence": True,
                "hedge_ratio": coint_result["hedge_ratio"],
                "signal": coint_result["trading_signal"]
            }

        return None

    def generate_pairs_trading_opportunities(
        self,
        min_z_score: float = 2.0
    ) -> List[ArbitrageOpportunity]:
        """
        Generate pairs trading opportunities.

        Args:
            min_z_score: Minimum z-score for entry

        Returns:
            List of opportunities
        """
        opportunities = []

        # Find cointegrated pairs
        pairs = self.find_cointegrated_pairs()

        for pair in pairs:
            z_score = pair["z_score"]

            if abs(z_score) >= min_z_score:
                # Create opportunity
                asset1_parts = pair["asset1"].split(":")
                asset2_parts = pair["asset2"].split(":")

                # Determine trading direction
                if z_score > 0:
                    # Short asset1, long asset2
                    action1_side = OrderSide.SELL
                    action2_side = OrderSide.BUY
                else:
                    # Long asset1, short asset2
                    action1_side = OrderSide.BUY
                    action2_side = OrderSide.SELL

                expected_profit_pct = Decimal(abs(z_score)) * Decimal("0.5")

                opportunity = ArbitrageOpportunity(
                    opportunity_id=str(uuid.uuid4()),
                    arbitrage_type=ArbitrageType.STATISTICAL,
                    market_type=None,  # Would need market data
                    symbol=f"{asset1_parts[1]}/{asset2_parts[1]}",
                    timestamp=datetime.now(),
                    expected_profit=expected_profit_pct * Decimal(100),
                    expected_profit_percentage=expected_profit_pct,
                    confidence_score=Decimal(str(pair["confidence"])),
                    risk_score=Decimal(1) - Decimal(str(pair["confidence"])),
                    detection_latency_ms=0,
                    market_data=[],
                    suggested_actions=[],
                    metadata={
                        "strategy": "pairs_trading",
                        "asset1": pair["asset1"],
                        "asset2": pair["asset2"],
                        "hedge_ratio": pair["hedge_ratio"],
                        "z_score": z_score,
                        "half_life": pair["half_life"],
                        "signal": pair["trading_signal"]
                    }
                )

                opportunities.append(opportunity)

        return opportunities
