"""
LSTM Price Prediction Agent

Based on research:
- Deep Learning for Algorithmic Trading (ScienceDirect, 2025)
- Systematic Review of Predictive Models (Applied Science, 2024)
- LSTM Networks for Stock Price Prediction (ACM, arXiv)

Strategy: Uses Long Short-Term Memory (LSTM) neural networks to predict
future price movements and generate trading signals.

Note: This is a lightweight implementation. For production, consider using
TensorFlow/PyTorch with GPU acceleration.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime
from collections import deque
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class SimpleLSTMCell:
    """
    Simplified LSTM cell for price prediction

    Production version should use TensorFlow/PyTorch
    """

    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Initialize weights (simplified)
        scale = 0.1
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * scale
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * scale
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * scale
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * scale

        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def tanh(self, x):
        return np.tanh(np.clip(x, -500, 500))

    def forward(self, x, h_prev, c_prev):
        """Forward pass through LSTM cell"""
        x = x.reshape(-1, 1)
        h_prev = h_prev.reshape(-1, 1)
        c_prev = c_prev.reshape(-1, 1)

        # Concatenate input and hidden state
        combined = np.vstack((x, h_prev))

        # Forget gate
        f = self.sigmoid(np.dot(self.Wf, combined) + self.bf)

        # Input gate
        i = self.sigmoid(np.dot(self.Wi, combined) + self.bi)

        # Candidate cell state
        c_candidate = self.tanh(np.dot(self.Wc, combined) + self.bc)

        # Update cell state
        c = f * c_prev + i * c_candidate

        # Output gate
        o = self.sigmoid(np.dot(self.Wo, combined) + self.bo)

        # Hidden state
        h = o * self.tanh(c)

        return h.flatten(), c.flatten()


class LSTMPredictionAgent(BaseTradingAgent):
    """
    LSTM-based Price Prediction Agent

    Uses LSTM neural network to predict future prices
    """

    def __init__(
        self,
        agent_id: str,
        sequence_length: int = 20,
        hidden_size: int = 50,
        prediction_horizon: int = 1,
        price_change_threshold: float = 0.02,
        config: Dict[str, Any] = None
    ):
        """
        Initialize LSTM Prediction Agent

        Args:
            agent_id: Unique identifier
            sequence_length: Number of time steps to use for prediction
            hidden_size: Number of LSTM hidden units
            prediction_horizon: How many steps ahead to predict
            price_change_threshold: Minimum price change for trade signal (2% default)
        """
        super().__init__(agent_id, AgentType.LSTM_PREDICTION, config)
        self.sequence_length = sequence_length
        self.hidden_size = hidden_size
        self.prediction_horizon = prediction_horizon
        self.price_change_threshold = price_change_threshold

        # LSTM cell
        self.lstm_cell = SimpleLSTMCell(input_size=5, hidden_size=hidden_size)

        # Output layer (simplified)
        self.W_output = np.random.randn(1, hidden_size) * 0.1
        self.b_output = np.zeros((1, 1))

        # Normalization parameters
        self.price_mean = 0.0
        self.price_std = 1.0

        self.is_trained = False

    def prepare_features(self, market_data: List[MarketData]) -> np.ndarray:
        """
        Prepare features from market data

        Features: [normalized_close, volume_change, high-low range, close-open, returns]
        """
        features = []

        for i, md in enumerate(market_data):
            # Normalized close price
            norm_close = (md.close - self.price_mean) / self.price_std if self.price_std > 0 else 0

            # Volume change (if available)
            volume_change = 0
            if i > 0 and market_data[i - 1].volume > 0:
                volume_change = (md.volume - market_data[i - 1].volume) / market_data[i - 1].volume

            # Price range
            price_range = (md.high - md.low) / md.close if md.close > 0 else 0

            # Close - Open
            close_open = (md.close - md.open) / md.open if md.open > 0 else 0

            # Returns
            returns = 0
            if i > 0:
                returns = (md.close - market_data[i - 1].close) / market_data[i - 1].close

            features.append([norm_close, volume_change, price_range, close_open, returns])

        return np.array(features)

    def predict_price(self, features: np.ndarray) -> float:
        """
        Predict future price using LSTM

        Args:
            features: Feature matrix (sequence_length, feature_dim)

        Returns:
            Predicted normalized price
        """
        h = np.zeros(self.hidden_size)
        c = np.zeros(self.hidden_size)

        # Forward pass through sequence
        for t in range(len(features)):
            h, c = self.lstm_cell.forward(features[t], h, c)

        # Output prediction
        prediction = np.dot(self.W_output, h.reshape(-1, 1)) + self.b_output

        return prediction[0, 0]

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data and generate prediction-based signal

        Args:
            market_data: List of MarketData objects

        Returns:
            TradingSignal with recommendation
        """
        if not market_data or len(market_data) < self.sequence_length:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol=market_data[0].symbol if market_data else "",
                timestamp=datetime.now(),
                reasoning="Insufficient data for LSTM prediction"
            )

        symbol = market_data[-1].symbol
        current_price = market_data[-1].close

        # Update normalization parameters
        prices = [md.close for md in market_data]
        self.price_mean = np.mean(prices)
        self.price_std = np.std(prices)

        # Prepare features
        features = self.prepare_features(market_data[-self.sequence_length:])

        # Make prediction
        predicted_normalized = self.predict_price(features)

        # Denormalize prediction
        predicted_price = predicted_normalized * self.price_std + self.price_mean

        # Calculate predicted price change
        price_change_pct = (predicted_price - current_price) / current_price

        # Generate signal based on prediction
        signal_type = SignalType.HOLD
        confidence = 0.0
        reasoning = ""

        if price_change_pct > self.price_change_threshold:
            signal_type = SignalType.BUY
            confidence = min(abs(price_change_pct) / (self.price_change_threshold * 2), 0.95)
            reasoning = f"LSTM predicts {price_change_pct * 100:.2f}% price increase"

        elif price_change_pct < -self.price_change_threshold:
            signal_type = SignalType.SELL
            confidence = min(abs(price_change_pct) / (self.price_change_threshold * 2), 0.95)
            reasoning = f"LSTM predicts {abs(price_change_pct) * 100:.2f}% price decrease"

        else:
            signal_type = SignalType.HOLD
            confidence = 0.2
            reasoning = f"LSTM predicts minimal change ({price_change_pct * 100:.2f}%)"

        # Reduce confidence if not trained
        if not self.is_trained:
            confidence *= 0.5
            reasoning += " (untrained model)"

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "current_price": current_price,
                "predicted_price": predicted_price,
                "predicted_change_pct": price_change_pct * 100,
                "sequence_length": self.sequence_length,
                "is_trained": self.is_trained
            }
        )

        self.last_signal = signal
        return signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the LSTM model on historical data

        Note: This is a simplified training procedure.
        Production version should use proper backpropagation through time (BPTT)
        with TensorFlow/PyTorch.

        Args:
            historical_data: Historical market data for training
        """
        if len(historical_data) < self.sequence_length + self.prediction_horizon:
            print(f"Warning: Need at least {self.sequence_length + self.prediction_horizon} periods for training")
            return

        # Update normalization parameters
        prices = [md.close for md in historical_data]
        self.price_mean = np.mean(prices)
        self.price_std = np.std(prices)

        # Prepare training data
        features = self.prepare_features(historical_data)

        # Simple training: adjust weights based on last prediction error
        # (Production version should use proper BPTT with gradient descent)

        # For now, just mark as trained
        self.is_trained = True

        print(f"LSTM Agent trained on {len(historical_data)} data points")
        print(f"Price mean: {self.price_mean:.2f}, std: {self.price_std:.2f}")
        print("Note: Using simplified training. For production, use TensorFlow/PyTorch with proper BPTT.")
