"""
Momentum Trading Agent

Based on research:
- Dynamically Combining Mean Reversion and Momentum (Hudson & Thames)
- Technical Trading Rules (RoboForex, 2024)
- Volatility-Adjusted Momentum Strategies (Scientific Reports, 2025)

Strategy: Identifies and follows price trends using technical indicators
including moving averages, RSI, and MACD.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class MomentumAgent(BaseTradingAgent):
    """
    Momentum Trading Agent

    Uses multiple technical indicators to identify and follow trends
    """

    def __init__(
        self,
        agent_id: str,
        short_window: int = 12,
        long_window: int = 26,
        rsi_period: int = 14,
        rsi_overbought: float = 70.0,
        rsi_oversold: float = 30.0,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Momentum Agent

        Args:
            agent_id: Unique identifier
            short_window: Short-term moving average period
            long_window: Long-term moving average period
            rsi_period: RSI calculation period
            rsi_overbought: RSI overbought threshold
            rsi_oversold: RSI oversold threshold
        """
        super().__init__(agent_id, AgentType.MOMENTUM, config)
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold

    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return 0.0
        return np.mean(prices[-period:])

    def calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return 0.0

        prices_array = np.array(prices)
        ema = prices_array[-period:].mean()  # Start with SMA

        multiplier = 2 / (period + 1)
        for price in prices_array[-period:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI)

        RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss
        """
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI

        # Calculate price changes
        deltas = np.diff(prices[-period - 1:])

        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        # Calculate average gain and loss
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_macd(
        self,
        prices: List[float]
    ) -> Tuple[float, float, float]:
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        if len(prices) < self.long_window:
            return 0.0, 0.0, 0.0

        # MACD = 12-day EMA - 26-day EMA
        ema_short = self.calculate_ema(prices, self.short_window)
        ema_long = self.calculate_ema(prices, self.long_window)
        macd_line = ema_short - ema_long

        # Signal line = 9-day EMA of MACD
        # Simplified: using 9-period average
        signal_line = macd_line * 0.9  # Simplified

        # Histogram = MACD - Signal
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data using momentum indicators

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

        prices = [md.close for md in market_data]
        symbol = market_data[-1].symbol
        current_price = market_data[-1].close

        # Calculate indicators
        sma_short = self.calculate_sma(prices, self.short_window)
        sma_long = self.calculate_sma(prices, self.long_window)
        rsi = self.calculate_rsi(prices, self.rsi_period)
        macd_line, signal_line, histogram = self.calculate_macd(prices)

        # Generate composite signal
        signals = []
        confidences = []

        # 1. Moving Average Crossover
        if sma_short > sma_long and len(prices) >= self.long_window:
            signals.append(SignalType.BUY)
            ma_diff_pct = ((sma_short - sma_long) / sma_long) * 100
            confidences.append(min(ma_diff_pct / 2, 1.0))
        elif sma_short < sma_long and len(prices) >= self.long_window:
            signals.append(SignalType.SELL)
            ma_diff_pct = ((sma_long - sma_short) / sma_long) * 100
            confidences.append(min(ma_diff_pct / 2, 1.0))

        # 2. RSI
        if rsi < self.rsi_oversold:
            signals.append(SignalType.BUY)
            confidences.append((self.rsi_oversold - rsi) / self.rsi_oversold)
        elif rsi > self.rsi_overbought:
            signals.append(SignalType.SELL)
            confidences.append((rsi - self.rsi_overbought) / (100 - self.rsi_overbought))

        # 3. MACD
        if histogram > 0:
            signals.append(SignalType.BUY)
            confidences.append(min(abs(histogram) / 10, 1.0))
        elif histogram < 0:
            signals.append(SignalType.SELL)
            confidences.append(min(abs(histogram) / 10, 1.0))

        # Aggregate signals
        if not signals:
            final_signal = SignalType.HOLD
            final_confidence = 0.0
            reasoning = "No clear momentum signal"
        else:
            buy_count = signals.count(SignalType.BUY)
            sell_count = signals.count(SignalType.SELL)

            if buy_count > sell_count:
                final_signal = SignalType.BUY
                final_confidence = np.mean([c for s, c in zip(signals, confidences) if s == SignalType.BUY])
                reasoning = f"Bullish momentum: {buy_count} buy signals vs {sell_count} sell signals"
            elif sell_count > buy_count:
                final_signal = SignalType.SELL
                final_confidence = np.mean([c for s, c in zip(signals, confidences) if s == SignalType.SELL])
                reasoning = f"Bearish momentum: {sell_count} sell signals vs {buy_count} buy signals"
            else:
                final_signal = SignalType.HOLD
                final_confidence = 0.3
                reasoning = f"Mixed signals: {buy_count} buy vs {sell_count} sell"

        signal = TradingSignal(
            signal_type=final_signal,
            confidence=final_confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "sma_short": sma_short,
                "sma_long": sma_long,
                "rsi": rsi,
                "macd_line": macd_line,
                "signal_line": signal_line,
                "histogram": histogram,
                "buy_signals": buy_count if signals else 0,
                "sell_signals": sell_count if signals else 0
            }
        )

        self.last_signal = signal
        return signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the agent on historical data

        Momentum agent doesn't require training but validates parameters
        """
        if len(historical_data) < self.long_window:
            print(f"Warning: Insufficient data for momentum analysis. Need at least {self.long_window} periods.")
        else:
            print(f"Momentum Agent ready with {len(historical_data)} data points")
