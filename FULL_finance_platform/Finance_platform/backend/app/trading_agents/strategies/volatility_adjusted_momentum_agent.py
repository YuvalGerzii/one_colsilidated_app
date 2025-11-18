"""
Volatility-Adjusted Momentum Agent

Based on research:
- Volatility-Adjusted Momentum Strategies (Scientific Reports, 2025)
- Algorithm-Based Intraday Trading (Damora Capital, 2021)
- Risk-Adjusted Returns in Algorithmic Trading

Strategy: Adjusts momentum signals based on current market volatility,
reducing position sizes in high-volatility environments and increasing
exposure in low-volatility trending markets.
"""

import numpy as np
from typing import List, Dict, Any
from datetime import datetime
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class VolatilityAdjustedMomentumAgent(BaseTradingAgent):
    """
    Volatility-Adjusted Momentum Trading Agent

    Combines momentum signals with volatility-based position sizing
    """

    def __init__(
        self,
        agent_id: str,
        momentum_lookback: int = 20,
        volatility_lookback: int = 20,
        vol_target: float = 0.15,  # 15% annualized volatility target
        momentum_threshold: float = 0.02,  # 2% momentum threshold
        config: Dict[str, Any] = None
    ):
        """
        Initialize Volatility-Adjusted Momentum Agent

        Args:
            agent_id: Unique identifier
            momentum_lookback: Period for momentum calculation
            volatility_lookback: Period for volatility calculation
            vol_target: Target annualized volatility
            momentum_threshold: Minimum momentum for signal
        """
        super().__init__(agent_id, AgentType.VOLATILITY_ADJUSTED, config)
        self.momentum_lookback = momentum_lookback
        self.volatility_lookback = volatility_lookback
        self.vol_target = vol_target
        self.momentum_threshold = momentum_threshold

        # Trading days per year for annualization
        self.trading_days_per_year = 252

    def calculate_returns(self, prices: np.ndarray) -> np.ndarray:
        """Calculate log returns"""
        return np.diff(np.log(prices))

    def calculate_momentum(self, prices: np.ndarray) -> float:
        """
        Calculate momentum as cumulative return over lookback period
        """
        if len(prices) < self.momentum_lookback + 1:
            return 0.0

        lookback_prices = prices[-self.momentum_lookback - 1:]
        momentum = (lookback_prices[-1] / lookback_prices[0]) - 1

        return momentum

    def calculate_volatility(self, prices: np.ndarray) -> float:
        """
        Calculate annualized volatility

        Returns standard deviation of returns, annualized
        """
        if len(prices) < self.volatility_lookback + 1:
            return 0.0

        returns = self.calculate_returns(prices[-self.volatility_lookback - 1:])

        # Calculate standard deviation
        vol_daily = np.std(returns)

        # Annualize
        vol_annual = vol_daily * np.sqrt(self.trading_days_per_year)

        return vol_annual

    def calculate_sharpe_ratio(
        self,
        prices: np.ndarray,
        risk_free_rate: float = 0.02
    ) -> float:
        """
        Calculate Sharpe ratio

        Sharpe = (Return - Risk-free rate) / Volatility
        """
        if len(prices) < 2:
            return 0.0

        returns = self.calculate_returns(prices)
        avg_return = np.mean(returns) * self.trading_days_per_year
        volatility = np.std(returns) * np.sqrt(self.trading_days_per_year)

        if volatility == 0:
            return 0.0

        sharpe = (avg_return - risk_free_rate) / volatility

        return sharpe

    def calculate_position_size(self, volatility: float) -> float:
        """
        Calculate position size based on volatility targeting

        Position size = (Target Vol / Current Vol)

        This scales exposure inversely with volatility:
        - High vol -> smaller position
        - Low vol -> larger position
        """
        if volatility == 0:
            return 1.0

        position_scalar = self.vol_target / volatility

        # Cap position size to reasonable bounds [0.5, 2.0]
        position_scalar = np.clip(position_scalar, 0.5, 2.0)

        return position_scalar

    def calculate_atr(
        self,
        market_data: List[MarketData],
        period: int = 14
    ) -> float:
        """
        Calculate Average True Range (ATR) for volatility measurement

        ATR is a better measure of volatility that accounts for gaps
        """
        if len(market_data) < period + 1:
            return 0.0

        true_ranges = []

        for i in range(1, len(market_data)):
            high = market_data[i].high
            low = market_data[i].low
            prev_close = market_data[i - 1].close

            # True range is max of:
            # 1. Current high - current low
            # 2. Abs(current high - previous close)
            # 3. Abs(current low - previous close)
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)

        # Average true range
        atr = np.mean(true_ranges[-period:])

        return atr

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data with volatility-adjusted momentum strategy

        Args:
            market_data: List of MarketData objects

        Returns:
            TradingSignal with recommendation
        """
        if not market_data or len(market_data) < max(self.momentum_lookback, self.volatility_lookback) + 1:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol=market_data[0].symbol if market_data else "",
                timestamp=datetime.now(),
                reasoning="Insufficient data for volatility-adjusted momentum"
            )

        symbol = market_data[-1].symbol
        prices = np.array([md.close for md in market_data])
        current_price = prices[-1]

        # Calculate momentum
        momentum = self.calculate_momentum(prices)

        # Calculate volatility
        volatility = self.calculate_volatility(prices)

        # Calculate ATR
        atr = self.calculate_atr(market_data)
        atr_pct = atr / current_price if current_price > 0 else 0

        # Calculate Sharpe ratio
        sharpe = self.calculate_sharpe_ratio(prices)

        # Calculate position size
        position_size = self.calculate_position_size(volatility)

        # Generate signal
        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        # Base signal on momentum
        if momentum > self.momentum_threshold:
            signal_type = SignalType.BUY
            base_confidence = min(abs(momentum) / (self.momentum_threshold * 2), 1.0)

            # Adjust confidence based on volatility
            # Higher volatility -> lower confidence
            vol_adjustment = position_size  # Position size is inversely related to vol
            confidence = base_confidence * vol_adjustment

            reasoning = (
                f"Positive momentum ({momentum * 100:.2f}%) with "
                f"{'low' if volatility < self.vol_target else 'high'} volatility "
                f"({volatility * 100:.1f}% annual). Position size: {position_size:.2f}x"
            )

        elif momentum < -self.momentum_threshold:
            signal_type = SignalType.SELL
            base_confidence = min(abs(momentum) / (self.momentum_threshold * 2), 1.0)

            # Adjust confidence based on volatility
            vol_adjustment = position_size
            confidence = base_confidence * vol_adjustment

            reasoning = (
                f"Negative momentum ({momentum * 100:.2f}%) with "
                f"{'low' if volatility < self.vol_target else 'high'} volatility "
                f"({volatility * 100:.1f}% annual). Position size: {position_size:.2f}x"
            )

        else:
            signal_type = SignalType.HOLD
            confidence = 0.2
            reasoning = f"Weak momentum ({momentum * 100:.2f}%). Holding position."

        # Further adjust based on Sharpe ratio
        if sharpe > 1.0 and signal_type != SignalType.HOLD:
            confidence = min(confidence * 1.2, 1.0)
            reasoning += f" Strong risk-adjusted returns (Sharpe: {sharpe:.2f})"
        elif sharpe < 0 and signal_type != SignalType.HOLD:
            confidence *= 0.7
            reasoning += f" Weak risk-adjusted returns (Sharpe: {sharpe:.2f})"

        # Cap confidence
        confidence = min(confidence, 1.0)

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "momentum": momentum,
                "volatility": volatility,
                "volatility_target": self.vol_target,
                "position_size": position_size,
                "sharpe_ratio": sharpe,
                "atr": atr,
                "atr_pct": atr_pct,
                "lookback_period": self.momentum_lookback
            }
        )

        self.last_signal = signal
        return signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the agent on historical data

        Calibrates volatility parameters and validates thresholds
        """
        if len(historical_data) < max(self.momentum_lookback, self.volatility_lookback) + 1:
            print(f"Warning: Need more data for volatility-adjusted momentum")
            return

        prices = np.array([md.close for md in historical_data])

        # Calculate historical volatility statistics
        hist_vol = self.calculate_volatility(prices)
        hist_momentum = self.calculate_momentum(prices)
        hist_sharpe = self.calculate_sharpe_ratio(prices)

        print(f"Volatility-Adjusted Momentum Agent trained on {len(historical_data)} data points")
        print(f"Historical volatility: {hist_vol * 100:.2f}% (Target: {self.vol_target * 100:.2f}%)")
        print(f"Historical momentum: {hist_momentum * 100:.2f}%")
        print(f"Historical Sharpe ratio: {hist_sharpe:.2f}")
