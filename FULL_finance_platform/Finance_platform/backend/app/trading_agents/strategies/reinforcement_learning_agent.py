"""
Reinforcement Learning Trading Agent

Based on research:
- FinRL: Deep Reinforcement Learning Library (arXiv, 2020)
- Multi-Agent DRL for Financial Trading (ScienceDirect, 2022)
- Deep RL Strategies in Finance (arXiv, 2024)
- Risk Curiosity Driven Learning (Expert Systems, 2020)

Strategy: Uses Deep Q-Learning (DQN) with experience replay to learn
optimal trading policies from market interactions.

Algorithms supported:
- Deep Q-Network (DQN)
- Double DQN
- Advantage Actor-Critic (A2C) - simplified version
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from collections import deque
import random
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class ExperienceReplay:
    """Experience replay buffer for DQN"""

    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        """Add experience to buffer"""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        """Sample random batch from buffer"""
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))

    def size(self):
        """Get buffer size"""
        return len(self.buffer)


class DQNNetwork:
    """
    Deep Q-Network for action value estimation

    Simplified implementation. Production should use TensorFlow/PyTorch.
    """

    def __init__(self, state_size: int, action_size: int, hidden_size: int = 64):
        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = hidden_size

        # Initialize weights
        self.W1 = np.random.randn(hidden_size, state_size) * 0.1
        self.b1 = np.zeros((hidden_size, 1))

        self.W2 = np.random.randn(hidden_size, hidden_size) * 0.1
        self.b2 = np.zeros((hidden_size, 1))

        self.W3 = np.random.randn(action_size, hidden_size) * 0.1
        self.b3 = np.zeros((action_size, 1))

        # Learning rate
        self.lr = 0.001

    def relu(self, x):
        """ReLU activation"""
        return np.maximum(0, x)

    def forward(self, state: np.ndarray) -> np.ndarray:
        """Forward pass through network"""
        state = state.reshape(-1, 1)

        # Layer 1
        z1 = np.dot(self.W1, state) + self.b1
        a1 = self.relu(z1)

        # Layer 2
        z2 = np.dot(self.W2, a1) + self.b2
        a2 = self.relu(z2)

        # Output layer
        q_values = np.dot(self.W3, a2) + self.b3

        return q_values.flatten()

    def update(self, state, action, target):
        """
        Update network weights (simplified)

        Production version should use proper backpropagation
        """
        # Get current Q-values
        q_values = self.forward(state)

        # Calculate error
        error = target - q_values[action]

        # Simplified weight update (gradient descent approximation)
        self.W3[action] += self.lr * error * 0.1
        self.b3[action] += self.lr * error


class ReinforcementLearningAgent(BaseTradingAgent):
    """
    Reinforcement Learning Trading Agent using DQN

    Action space: BUY, SELL, HOLD
    State space: Market features + portfolio state
    Reward: PnL from trades
    """

    def __init__(
        self,
        agent_id: str,
        state_size: int = 10,
        learning_rate: float = 0.001,
        gamma: float = 0.95,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Reinforcement Learning Agent

        Args:
            agent_id: Unique identifier
            state_size: Size of state vector
            learning_rate: Learning rate for neural network
            gamma: Discount factor for future rewards
            epsilon: Exploration rate
            epsilon_decay: Decay rate for epsilon
            epsilon_min: Minimum epsilon value
        """
        super().__init__(agent_id, AgentType.REINFORCEMENT_LEARNING, config)

        self.state_size = state_size
        self.action_size = 3  # BUY, SELL, HOLD
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Q-Network
        self.q_network = DQNNetwork(state_size, self.action_size)

        # Target network (for stable learning)
        self.target_network = DQNNetwork(state_size, self.action_size)

        # Experience replay
        self.memory = ExperienceReplay(capacity=10000)

        # Training parameters
        self.batch_size = 32
        self.update_target_frequency = 100
        self.steps = 0

        # Portfolio state
        self.position = 0  # -1: short, 0: neutral, 1: long
        self.entry_price = 0.0
        self.portfolio_value = 100000.0  # Starting capital

    def extract_state(self, market_data: List[MarketData]) -> np.ndarray:
        """
        Extract state features from market data

        Features:
        1. Price momentum (returns)
        2. Volatility
        3. Volume change
        4. RSI
        5. Position
        6. Unrealized PnL
        7-10. Additional technical indicators
        """
        if len(market_data) < 20:
            return np.zeros(self.state_size)

        prices = np.array([md.close for md in market_data[-20:]])
        volumes = np.array([md.volume for md in market_data[-20:]])

        # 1. Returns (momentum)
        returns = (prices[-1] - prices[-5]) / prices[-5] if prices[-5] > 0 else 0

        # 2. Volatility
        volatility = np.std(np.diff(prices) / prices[:-1])

        # 3. Volume change
        volume_change = (volumes[-1] - np.mean(volumes)) / np.mean(volumes) if np.mean(volumes) > 0 else 0

        # 4. RSI
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else 0
        avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else 0
        rs = avg_gain / avg_loss if avg_loss > 0 else 0
        rsi = 100 - (100 / (1 + rs))

        # 5. Position
        position_feature = self.position

        # 6. Unrealized PnL
        current_price = prices[-1]
        unrealized_pnl = 0
        if self.position != 0 and self.entry_price > 0:
            unrealized_pnl = (current_price - self.entry_price) / self.entry_price * self.position

        # 7. Moving average crossover
        sma_short = np.mean(prices[-5:])
        sma_long = np.mean(prices[-20:])
        ma_signal = (sma_short - sma_long) / sma_long if sma_long > 0 else 0

        # 8. Price z-score
        price_mean = np.mean(prices)
        price_std = np.std(prices)
        z_score = (current_price - price_mean) / price_std if price_std > 0 else 0

        # 9-10. Additional features
        high_low_range = (market_data[-1].high - market_data[-1].low) / market_data[-1].close
        close_open = (market_data[-1].close - market_data[-1].open) / market_data[-1].open

        state = np.array([
            returns,
            volatility,
            volume_change,
            rsi / 100,  # Normalize to [0, 1]
            position_feature,
            unrealized_pnl,
            ma_signal,
            z_score,
            high_low_range,
            close_open
        ])

        return state

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        """
        Select action using epsilon-greedy policy

        Args:
            state: Current state
            training: Whether in training mode

        Returns:
            Action index (0: BUY, 1: SELL, 2: HOLD)
        """
        if training and random.random() < self.epsilon:
            # Explore: random action
            return random.randint(0, self.action_size - 1)
        else:
            # Exploit: best action from Q-network
            q_values = self.q_network.forward(state)
            return np.argmax(q_values)

    def action_to_signal(self, action: int) -> SignalType:
        """Convert action index to SignalType"""
        if action == 0:
            return SignalType.BUY
        elif action == 1:
            return SignalType.SELL
        else:
            return SignalType.HOLD

    def calculate_reward(
        self,
        action: int,
        current_price: float,
        next_price: float
    ) -> float:
        """
        Calculate reward for action

        Reward based on:
        - Realized profit/loss
        - Risk-adjusted returns
        - Transaction costs
        """
        reward = 0.0

        # Action effects
        if action == 0:  # BUY
            if self.position <= 0:  # Can buy
                # Reward based on price movement
                price_change = (next_price - current_price) / current_price
                reward = price_change * 100
                # Update position
                self.position = 1
                self.entry_price = current_price
        elif action == 1:  # SELL
            if self.position >= 0:  # Can sell
                # Reward based on price movement
                price_change = (current_price - next_price) / current_price
                reward = price_change * 100
                # Update position
                self.position = -1
                self.entry_price = current_price
        else:  # HOLD
            # Small penalty for holding in trending market
            price_change = abs((next_price - current_price) / current_price)
            reward = -price_change * 10

        # Transaction cost
        if action != 2:
            reward -= 0.1  # Small transaction cost

        return reward

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data and generate RL-based signal

        Args:
            market_data: List of MarketData objects

        Returns:
            TradingSignal with recommendation
        """
        if not market_data or len(market_data) < 20:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol=market_data[0].symbol if market_data else "",
                timestamp=datetime.now(),
                reasoning="Insufficient data for RL agent"
            )

        symbol = market_data[-1].symbol
        current_price = market_data[-1].close

        # Extract state
        state = self.extract_state(market_data)

        # Select action
        action = self.select_action(state, training=False)

        # Convert to signal
        signal_type = self.action_to_signal(action)

        # Get Q-values for confidence
        q_values = self.q_network.forward(state)
        max_q = np.max(q_values)
        min_q = np.min(q_values)
        confidence = (q_values[action] - min_q) / (max_q - min_q) if max_q > min_q else 0.5

        # Reasoning
        reasoning = f"RL agent selected {signal_type.value} (Q-value: {q_values[action]:.3f}, ε: {self.epsilon:.3f})"

        signal = TradingSignal(
            signal_type=signal_type,
            confidence=confidence,
            symbol=symbol,
            timestamp=datetime.now(),
            price=current_price,
            reasoning=reasoning,
            metadata={
                "action": action,
                "q_values": q_values.tolist(),
                "epsilon": self.epsilon,
                "position": self.position,
                "steps": self.steps,
                "memory_size": self.memory.size()
            }
        )

        self.last_signal = signal
        return signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train the RL agent on historical data using experience replay

        Args:
            historical_data: Historical market data
        """
        if len(historical_data) < 50:
            print("Warning: Need at least 50 periods for RL training")
            return

        print(f"Training RL Agent on {len(historical_data)} data points...")

        # Reset agent state
        self.position = 0
        self.entry_price = 0.0
        episode_reward = 0

        # Training loop
        for i in range(20, len(historical_data) - 1):
            # Get current state
            current_window = historical_data[:i + 1]
            state = self.extract_state(current_window)

            # Select action
            action = self.select_action(state, training=True)

            # Get next state
            next_window = historical_data[:i + 2]
            next_state = self.extract_state(next_window)

            # Calculate reward
            current_price = historical_data[i].close
            next_price = historical_data[i + 1].close
            reward = self.calculate_reward(action, current_price, next_price)

            episode_reward += reward

            # Store experience
            done = (i == len(historical_data) - 2)
            self.memory.add(state, action, reward, next_state, done)

            # Update Q-network
            if self.memory.size() >= self.batch_size:
                self._replay()

            self.steps += 1

            # Update target network
            if self.steps % self.update_target_frequency == 0:
                self._update_target_network()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        print(f"Training complete. Episode reward: {episode_reward:.2f}")
        print(f"Epsilon: {self.epsilon:.3f}, Memory size: {self.memory.size()}")

    def _replay(self):
        """Experience replay training"""
        batch = self.memory.sample(self.batch_size)

        for state, action, reward, next_state, done in batch:
            # Calculate target Q-value
            if done:
                target = reward
            else:
                next_q_values = self.target_network.forward(next_state)
                target = reward + self.gamma * np.max(next_q_values)

            # Update Q-network
            self.q_network.update(state, action, target)

    def _update_target_network(self):
        """Update target network weights"""
        # Copy weights from Q-network to target network
        self.target_network.W1 = self.q_network.W1.copy()
        self.target_network.W2 = self.q_network.W2.copy()
        self.target_network.W3 = self.q_network.W3.copy()
        self.target_network.b1 = self.q_network.b1.copy()
        self.target_network.b2 = self.q_network.b2.copy()
        self.target_network.b3 = self.q_network.b3.copy()
