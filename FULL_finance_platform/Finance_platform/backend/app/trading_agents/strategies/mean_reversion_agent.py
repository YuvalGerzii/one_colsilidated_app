"""
Mean Reversion Trading Agent

Based on research:
- Statistical Arbitrage (Wikipedia, SSRN)
- Mean Reversion Strategies (QuantInsti, 2024)
- Algorithm-Based Intraday Trading (Damora Capital)

Strategy: Identifies assets that have deviated from their historical mean
and expects them to revert back, generating buy/sell signals accordingly.
"""

import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class MeanReversionAgent(BaseTradingAgent):
    """
    Mean Reversion Trading Agent

    Uses statistical measures (z-score) to identify overbought/oversold conditions
    """

    def __init__(
        self,
        agent_id: str,
        lookback_period: int = 20,
        entry_threshold: float = 2.0,
        exit_threshold: float = 0.5,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Mean Reversion Agent

        Args:
            agent_id: Unique identifier for agent
            lookback_period: Number of periods for calculating mean (default: 20)
            entry_threshold: Z-score threshold for entry signals (default: 2.0)
            exit_threshold: Z-score threshold for exit signals (default: 0.5)
            config: Additional configuration
        """
        super().__init__(agent_id, AgentType.MEAN_REVERSION, config)
        self.lookback_period = lookback_period
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold
        self.historical_means: Dict[str, float] = {}
        self.historical_stds: Dict[str, float] = {}

    def calculate_z_score(self, prices: List[float]) -> float:
        """
        Calculate z-score for current price

        Z-score = (Current Price - Mean) / Standard Deviation
        """
        if len(prices) < self.lookback_period:
            return 0.0

        recent_prices = prices[-self.lookback_period:]
        mean = np.mean(recent_prices)
        std = np.std(recent_prices)

        if std == 0:
            return 0.0

        current_price = prices[-1]
        z_score = (current_price - mean) / std

        return z_score

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data and generate mean reversion signal

        Args:
            market_data: List of MarketData objects

        Returns:
            TradingSignal with recommendation
        """
        if not market_data:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol="",
                timestamp=datetime.now(),
                reasoning="No market data available"
            )

        # Extract closing prices
        prices = [md.close for md in market_data]
        symbol = market_data[-1].symbol
        current_price = market_data[-1].close

        # Calculate z-score
        z_score = self.calculate_z_score(prices)

        # Store historical statistics
        if len(prices) >= self.lookback_period:
            recent_prices = prices[-self.lookback_period:]
            self.historical_means[symbol] = np.mean(recent_prices)
            self.historical_stds[symbol] = np.std(recent_prices)

        # Generate signal based on z-score
        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        if z_score <= -self.entry_threshold:
            # Price is significantly below mean - expect upward reversion
            signal_type = SignalType.BUY
            confidence = min(abs(z_score) / self.entry_threshold, 1.0)
            reasoning = f"Price significantly below mean (z-score: {z_score:.2f}). Expecting upward reversion."

        elif z_score >= self.entry_threshold:
            # Price is significantly above mean - expect downward reversion
            signal_type = SignalType.SELL
            confidence = min(abs(z_score) / self.entry_threshold, 1.0)
            reasoning = f"Price significantly above mean (z-score: {z_score:.2f}). Expecting downward reversion."

        elif abs(z_score) <= self.exit_threshold:
            # Price has reverted to mean
            signal_type = SignalType.HOLD
            confidence = 0.3
            reasoning = f"Price near mean (z-score: {z_score:.2f}). Holding position."

        else:
            # Price in neutral zone
            signal_type = SignalType.HOLD
            confidence = 0.2
            reasoning = f"Price in neutral zone (z-score: {z_score:.2f})."

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "z_score": z_score,
                "mean": self.historical_means.get(symbol, 0.0),
                "std": self.historical_stds.get(symbol, 0.0),
                "lookback_period": self.lookback_period
            }
        )

        self.last_signal = signal
        return signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the agent on historical data

        For mean reversion, this updates the historical statistics
        """
        if not historical_data:
            return

        symbol = historical_data[0].symbol
        prices = [md.close for md in historical_data]

        if len(prices) >= self.lookback_period:
            self.historical_means[symbol] = np.mean(prices[-self.lookback_period:])
            self.historical_stds[symbol] = np.std(prices[-self.lookback_period:])

        print(f"Mean Reversion Agent trained on {len(historical_data)} data points for {symbol}")
