"""
Pairs Trading Agent

Based on research:
- Statistical Arbitrage (Wikipedia)
- Pairs Trading: A Cointegration Approach (SSRN)
- Advanced Statistical Arbitrage (arXiv, 2024)

Strategy: Identifies pairs of correlated assets and trades on temporary
divergences from their historical relationship, expecting convergence.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from scipy import stats
from scipy.optimize import minimize
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class PairsTradingAgent(BaseTradingAgent):
    """
    Pairs Trading Agent

    Identifies and trades co-integrated pairs of assets
    """

    def __init__(
        self,
        agent_id: str,
        lookback_period: int = 60,
        z_score_entry: float = 2.0,
        z_score_exit: float = 0.5,
        min_correlation: float = 0.7,
        min_half_life: float = 1.0,
        max_half_life: float = 30.0,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Pairs Trading Agent

        Args:
            agent_id: Unique identifier
            lookback_period: Period for calculating statistics
            z_score_entry: Z-score threshold for entry
            z_score_exit: Z-score threshold for exit
            min_correlation: Minimum correlation for pair selection
            min_half_life: Minimum mean reversion half-life (days)
            max_half_life: Maximum mean reversion half-life (days)
        """
        super().__init__(agent_id, AgentType.PAIRS_TRADING, config)
        self.lookback_period = lookback_period
        self.z_score_entry = z_score_entry
        self.z_score_exit = z_score_exit
        self.min_correlation = min_correlation
        self.min_half_life = min_half_life
        self.max_half_life = max_half_life

        # Store pair relationships
        self.pairs: Dict[str, Dict[str, Any]] = {}

    def test_cointegration(
        self,
        prices_a: np.ndarray,
        prices_b: np.ndarray
    ) -> Tuple[bool, float, np.ndarray]:
        """
        Test for cointegration between two price series

        Returns:
            (is_cointegrated, p_value, spread)
        """
        # Linear regression to find hedge ratio
        slope, intercept, r_value, p_value, std_err = stats.linregress(prices_b, prices_a)

        # Calculate spread
        spread = prices_a - (slope * prices_b + intercept)

        # Augmented Dickey-Fuller test (simplified)
        # Check if spread is stationary
        spread_diff = np.diff(spread)
        spread_lag = spread[:-1]

        # Regression: spread_diff = alpha + beta * spread_lag
        beta, alpha, _, adf_p_value, _ = stats.linregress(spread_lag, spread_diff)

        # Series is stationary if beta < 0 and p_value < 0.05
        is_cointegrated = (beta < 0) and (adf_p_value < 0.05)

        return is_cointegrated, adf_p_value, spread

    def calculate_hedge_ratio(
        self,
        prices_a: np.ndarray,
        prices_b: np.ndarray
    ) -> float:
        """
        Calculate optimal hedge ratio using linear regression
        """
        slope, intercept, _, _, _ = stats.linregress(prices_b, prices_a)
        return slope

    def calculate_half_life(self, spread: np.ndarray) -> float:
        """
        Calculate mean reversion half-life

        Half-life indicates how quickly spread reverts to mean
        """
        spread_lag = spread[:-1]
        spread_diff = np.diff(spread)

        # Ornstein-Uhlenbeck: spread_diff = lambda * spread_lag + error
        slope, _, _, _, _ = stats.linregress(spread_lag, spread_diff)

        if slope >= 0:
            return np.inf  # No mean reversion

        half_life = -np.log(2) / slope
        return half_life

    def identify_pair(
        self,
        market_data_a: List[MarketData],
        market_data_b: List[MarketData]
    ) -> Optional[Dict[str, Any]]:
        """
        Identify if two assets form a valid trading pair

        Returns:
            Pair information dictionary or None
        """
        if len(market_data_a) != len(market_data_b):
            return None

        if len(market_data_a) < self.lookback_period:
            return None

        prices_a = np.array([md.close for md in market_data_a])
        prices_b = np.array([md.close for md in market_data_b])

        symbol_a = market_data_a[0].symbol
        symbol_b = market_data_b[0].symbol

        # Calculate correlation
        correlation = np.corrcoef(prices_a, prices_b)[0, 1]

        if abs(correlation) < self.min_correlation:
            return None

        # Test cointegration
        is_cointegrated, p_value, spread = self.test_cointegration(prices_a, prices_b)

        if not is_cointegrated:
            return None

        # Calculate hedge ratio
        hedge_ratio = self.calculate_hedge_ratio(prices_a, prices_b)

        # Calculate half-life
        half_life = self.calculate_half_life(spread)

        # Check half-life constraints
        if half_life < self.min_half_life or half_life > self.max_half_life:
            return None

        # Calculate current spread statistics
        spread_mean = np.mean(spread)
        spread_std = np.std(spread)
        current_spread = spread[-1]
        z_score = (current_spread - spread_mean) / spread_std if spread_std > 0 else 0

        pair_info = {
            "symbol_a": symbol_a,
            "symbol_b": symbol_b,
            "correlation": correlation,
            "cointegration_p_value": p_value,
            "hedge_ratio": hedge_ratio,
            "half_life": half_life,
            "spread_mean": spread_mean,
            "spread_std": spread_std,
            "current_z_score": z_score,
            "last_updated": datetime.now()
        }

        return pair_info

    def analyze_pair_signal(
        self,
        market_data_a: List[MarketData],
        market_data_b: List[MarketData]
    ) -> Optional[TradingSignal]:
        """
        Analyze a pair and generate trading signal

        Args:
            market_data_a: Market data for asset A
            market_data_b: Market data for asset B

        Returns:
            TradingSignal or None
        """
        pair_info = self.identify_pair(market_data_a, market_data_b)

        if pair_info is None:
            return None

        z_score = pair_info["current_z_score"]
        symbol_a = pair_info["symbol_a"]
        symbol_b = pair_info["symbol_b"]
        pair_symbol = f"{symbol_a}/{symbol_b}"

        # Store pair info
        self.pairs[pair_symbol] = pair_info

        # Generate signal based on z-score
        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        if z_score <= -self.z_score_entry:
            # Spread is low: buy A, sell B
            signal_type = SignalType.BUY
            confidence = min(abs(z_score) / self.z_score_entry, 1.0)
            reasoning = (
                f"Pairs divergence detected. Buy {symbol_a}, Sell {symbol_b}. "
                f"Z-score: {z_score:.2f}, Half-life: {pair_info['half_life']:.1f} days"
            )

        elif z_score >= self.z_score_entry:
            # Spread is high: sell A, buy B
            signal_type = SignalType.SELL
            confidence = min(abs(z_score) / self.z_score_entry, 1.0)
            reasoning = (
                f"Pairs divergence detected. Sell {symbol_a}, Buy {symbol_b}. "
                f"Z-score: {z_score:.2f}, Half-life: {pair_info['half_life']:.1f} days"
            )

        elif abs(z_score) <= self.z_score_exit:
            # Spread has converged
            signal_type = SignalType.HOLD
            confidence = 0.4
            reasoning = f"Spread converged (z: {z_score:.2f}). Close positions."

        else:
            signal_type = SignalType.HOLD
            confidence = 0.2
            reasoning = f"Spread in neutral zone (z: {z_score:.2f})"

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=pair_symbol,
            timestamp=datetime.now(),
            reasoning=reasoning,
            metadata={
                "z_score": z_score,
                "correlation": pair_info["correlation"],
                "hedge_ratio": pair_info["hedge_ratio"],
                "half_life": pair_info["half_life"],
                "cointegration_p_value": pair_info["cointegration_p_value"],
                "spread_mean": pair_info["spread_mean"],
                "spread_std": pair_info["spread_std"]
            }
        )

        self.last_signal = signal
        return signal

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze single asset data

        Note: Pairs trading requires two assets. Use analyze_pair_signal instead.
        """
        return TradingSignal(
            signal_type=SignalType.HOLD,
            confidence=0.0,
            symbol=market_data[0].symbol if market_data else "",
            timestamp=datetime.now(),
            reasoning="Pairs trading requires two assets. Use analyze_pair_signal()."
        )

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the agent on historical data

        For pairs trading, this validates the lookback period
        """
        if len(historical_data) < self.lookback_period:
            print(f"Warning: Need at least {self.lookback_period} periods for pairs trading")
        else:
            print(f"Pairs Trading Agent ready with {len(historical_data)} data points")

    def get_active_pairs(self) -> List[Dict[str, Any]]:
        """Get all identified trading pairs"""
        return list(self.pairs.values())

    def get_pair_info(self, symbol_pair: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific pair"""
        return self.pairs.get(symbol_pair)
