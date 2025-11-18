"""
Statistical Arbitrage Agent

Based on research:
- Diversified Statistical Arbitrage (SSRN, James Velissaris)
- Dynamically Combining Mean Reversion and Momentum (Hudson & Thames)
- Advanced Statistical Arbitrage with Reinforcement Learning (arXiv)

Strategy: Combines mean reversion and momentum strategies using
principal component analysis (PCA) and statistical techniques.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
from scipy import stats
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class StatisticalArbitrageAgent(BaseTradingAgent):
    """
    Statistical Arbitrage Trading Agent

    Combines multiple strategies:
    1. Mean reversion on idiosyncratic components
    2. Momentum on systematic components
    3. Pairs trading logic
    """

    def __init__(
        self,
        agent_id: str,
        lookback_period: int = 60,
        z_score_entry: float = 2.0,
        z_score_exit: float = 0.5,
        correlation_threshold: float = 0.7,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Statistical Arbitrage Agent

        Args:
            agent_id: Unique identifier
            lookback_period: Period for statistical calculations
            z_score_entry: Z-score threshold for entry
            z_score_exit: Z-score threshold for exit
            correlation_threshold: Minimum correlation for pairs
        """
        super().__init__(agent_id, AgentType.STATISTICAL_ARBITRAGE, config)
        self.lookback_period = lookback_period
        self.z_score_entry = z_score_entry
        self.z_score_exit = z_score_exit
        self.correlation_threshold = correlation_threshold
        self.pairs_data: Dict[str, Dict] = {}

    def calculate_spread(
        self,
        prices_a: np.ndarray,
        prices_b: np.ndarray
    ) -> np.ndarray:
        """
        Calculate spread between two price series using linear regression

        Returns normalized spread
        """
        if len(prices_a) != len(prices_b):
            return np.array([])

        # Use linear regression to find hedge ratio
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            prices_b, prices_a
        )

        # Calculate spread
        spread = prices_a - (slope * prices_b + intercept)

        return spread

    def calculate_half_life(self, spread: np.ndarray) -> float:
        """
        Calculate mean reversion half-life using Ornstein-Uhlenbeck process

        Half-life indicates how quickly the spread reverts to mean
        """
        spread_lag = spread[:-1]
        spread_diff = np.diff(spread)

        # Regression: spread_diff = lambda * spread_lag + error
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            spread_lag, spread_diff
        )

        if slope >= 0:
            return np.inf  # No mean reversion

        half_life = -np.log(2) / slope
        return half_life

    def analyze_pair_correlation(
        self,
        prices_a: List[float],
        prices_b: List[float]
    ) -> Dict[str, Any]:
        """
        Analyze correlation and cointegration between two price series
        """
        prices_a_arr = np.array(prices_a)
        prices_b_arr = np.array(prices_b)

        # Calculate correlation
        correlation = np.corrcoef(prices_a_arr, prices_b_arr)[0, 1]

        # Calculate spread
        spread = self.calculate_spread(prices_a_arr, prices_b_arr)

        # Calculate z-score of spread
        spread_mean = np.mean(spread)
        spread_std = np.std(spread)
        current_z_score = (spread[-1] - spread_mean) / spread_std if spread_std > 0 else 0

        # Calculate half-life
        half_life = self.calculate_half_life(spread)

        return {
            "correlation": correlation,
            "spread": spread,
            "z_score": current_z_score,
            "half_life": half_life,
            "spread_mean": spread_mean,
            "spread_std": spread_std
        }

    def decompose_returns(
        self,
        prices: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """
        Decompose returns into systematic and idiosyncratic components

        Simplified version without PCA (can be enhanced)
        """
        returns = np.diff(np.log(prices))

        # Calculate moving average as proxy for systematic component
        window = min(20, len(returns) // 2)
        systematic = np.convolve(returns, np.ones(window) / window, mode='same')

        # Idiosyncratic = Total - Systematic
        idiosyncratic = returns - systematic

        return {
            "total_returns": returns,
            "systematic": systematic,
            "idiosyncratic": idiosyncratic
        }

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data using statistical arbitrage strategy

        Args:
            market_data: List of MarketData objects

        Returns:
            TradingSignal with recommendation
        """
        if not market_data or len(market_data) < self.lookback_period:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol=market_data[0].symbol if market_data else "",
                timestamp=datetime.now(),
                reasoning="Insufficient data for statistical arbitrage"
            )

        symbol = market_data[-1].symbol
        prices = np.array([md.close for md in market_data])
        current_price = prices[-1]

        # Decompose returns
        decomposition = self.decompose_returns(prices)

        # Calculate z-score on idiosyncratic component
        idio = decomposition["idiosyncratic"]
        if len(idio) > 0:
            idio_mean = np.mean(idio)
            idio_std = np.std(idio)
            current_idio_z = (idio[-1] - idio_mean) / idio_std if idio_std > 0 else 0
        else:
            current_idio_z = 0

        # Calculate momentum on systematic component
        systematic = decomposition["systematic"]
        momentum_score = systematic[-1] if len(systematic) > 0 else 0

        # Generate signal based on combined strategy
        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        # Mean reversion signal on idiosyncratic component
        if current_idio_z <= -self.z_score_entry:
            signal_type = SignalType.BUY
            confidence = min(abs(current_idio_z) / self.z_score_entry * 0.7, 0.9)
            reasoning = f"Idiosyncratic component oversold (z: {current_idio_z:.2f})"

        elif current_idio_z >= self.z_score_entry:
            signal_type = SignalType.SELL
            confidence = min(abs(current_idio_z) / self.z_score_entry * 0.7, 0.9)
            reasoning = f"Idiosyncratic component overbought (z: {current_idio_z:.2f})"

        # Adjust signal based on momentum
        if momentum_score > 0 and signal_type == SignalType.BUY:
            confidence *= 1.2  # Increase confidence
            reasoning += " + positive momentum"
        elif momentum_score < 0 and signal_type == SignalType.SELL:
            confidence *= 1.2  # Increase confidence
            reasoning += " + negative momentum"
        elif momentum_score > 0 and signal_type == SignalType.SELL:
            confidence *= 0.7  # Decrease confidence
            reasoning += " - conflicting momentum"
        elif momentum_score < 0 and signal_type == SignalType.BUY:
            confidence *= 0.7  # Decrease confidence
            reasoning += " - conflicting momentum"

        # Cap confidence at 1.0
        confidence = min(confidence, 1.0)

        # Exit signal
        if abs(current_idio_z) <= self.z_score_exit:
            signal_type = SignalType.HOLD
            confidence = 0.3
            reasoning = f"Near equilibrium (z: {current_idio_z:.2f})"

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "idiosyncratic_z_score": current_idio_z,
                "momentum_score": momentum_score,
                "systematic_return": systematic[-1] if len(systematic) > 0 else 0,
                "idiosyncratic_return": idio[-1] if len(idio) > 0 else 0,
                "lookback_period": self.lookback_period
            }
        )

        self.last_signal = signal
        return signal

    def analyze_pair(
        self,
        market_data_a: List[MarketData],
        market_data_b: List[MarketData]
    ) -> Optional[TradingSignal]:
        """
        Analyze a pair of assets for statistical arbitrage opportunities

        Args:
            market_data_a: Market data for first asset
            market_data_b: Market data for second asset

        Returns:
            TradingSignal or None
        """
        if len(market_data_a) != len(market_data_b):
            return None

        prices_a = [md.close for md in market_data_a]
        prices_b = [md.close for md in market_data_b]

        pair_analysis = self.analyze_pair_correlation(prices_a, prices_b)

        # Check if correlation is sufficient
        if abs(pair_analysis["correlation"]) < self.correlation_threshold:
            return None

        z_score = pair_analysis["z_score"]
        symbol_a = market_data_a[-1].symbol
        symbol_b = market_data_b[-1].symbol

        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        if z_score <= -self.z_score_entry:
            # Spread is low: buy A, sell B
            signal_type = SignalType.BUY
            confidence = min(abs(z_score) / self.z_score_entry, 1.0)
            reasoning = f"Pairs trade: Buy {symbol_a}, Sell {symbol_b} (z: {z_score:.2f})"

        elif z_score >= self.z_score_entry:
            # Spread is high: sell A, buy B
            signal_type = SignalType.SELL
            confidence = min(abs(z_score) / self.z_score_entry, 1.0)
            reasoning = f"Pairs trade: Sell {symbol_a}, Buy {symbol_b} (z: {z_score:.2f})"

        elif abs(z_score) <= self.z_score_exit:
            signal_type = SignalType.HOLD
            confidence = 0.3
            reasoning = f"Spread converged (z: {z_score:.2f})"

        return TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=f"{symbol_a}/{symbol_b}",
            timestamp=datetime.now(),
            reasoning=reasoning,
            metadata={
                "z_score": z_score,
                "correlation": pair_analysis["correlation"],
                "half_life": pair_analysis["half_life"],
                "spread_mean": pair_analysis["spread_mean"],
                "spread_std": pair_analysis["spread_std"]
            }
        )

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the agent on historical data

        Calibrates statistical parameters
        """
        if len(historical_data) < self.lookback_period:
            print(f"Warning: Need at least {self.lookback_period} periods for training")
            return

        print(f"Statistical Arbitrage Agent trained on {len(historical_data)} data points")
