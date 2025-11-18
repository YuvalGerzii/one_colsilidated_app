"""
Q-Learning engine for reinforcement learning.

Implements Q-Learning algorithm for agent policy optimization.
"""

import pickle
import random
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import numpy as np
from loguru import logger

from app.multi_agent_system.core.types import Experience


class QLearningEngine:
    """
    Q-Learning engine for agent improvement through reinforcement learning.

    Implements:
    - Q-Learning algorithm
    - Experience replay buffer
    - Epsilon-greedy exploration
    - Policy persistence
    """

    def __init__(
        self,
        agent_id: str,
        learning_rate: float = 0.1,
        discount_factor: float = 0.95,
        exploration_rate: float = 0.2,
        exploration_decay: float = 0.995,
        min_exploration_rate: float = 0.01,
        replay_buffer_size: int = 10000,
    ):
        """
        Initialize Q-Learning engine.

        Args:
            agent_id: ID of the agent
            learning_rate: Learning rate (alpha)
            discount_factor: Discount factor (gamma)
            exploration_rate: Initial exploration rate (epsilon)
            exploration_decay: Exploration decay rate
            min_exploration_rate: Minimum exploration rate
            replay_buffer_size: Size of experience replay buffer
        """
        self.agent_id = agent_id
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate

        # Q-table: state_key -> {action: q_value}
        self.q_table: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

        # Experience replay buffer
        self.replay_buffer: deque = deque(maxlen=replay_buffer_size)

        # Statistics
        self.stats = {
            "updates": 0,
            "episodes": 0,
            "total_reward": 0.0,
            "average_reward": 0.0,
        }

        logger.info(f"Q-Learning engine initialized for agent {agent_id}")

    def get_best_action(self, state: Dict[str, Any], available_actions: List[str]) -> str:
        """
        Get the best action for a given state.

        Uses epsilon-greedy strategy: explore with probability epsilon,
        exploit with probability 1-epsilon.

        Args:
            state: Current state
            available_actions: List of available actions

        Returns:
            Selected action
        """
        if not available_actions:
            raise ValueError("No available actions")

        state_key = self._state_to_key(state)

        # Exploration: choose random action
        if random.random() < self.exploration_rate:
            action = random.choice(available_actions)
            logger.debug(f"Exploring: chose random action '{action}'")
            return action

        # Exploitation: choose best action based on Q-values
        q_values = self.q_table[state_key]

        # If we have Q-values for this state, choose the best one
        if q_values:
            # Filter to only available actions
            available_q_values = {
                action: q_values.get(action, 0.0)
                for action in available_actions
            }
            if available_q_values:
                best_action = max(available_q_values.items(), key=lambda x: x[1])[0]
                logger.debug(
                    f"Exploiting: chose best action '{best_action}' "
                    f"(Q={available_q_values[best_action]:.3f})"
                )
                return best_action

        # If no Q-values yet, choose randomly
        action = random.choice(available_actions)
        logger.debug(f"No Q-values yet: chose random action '{action}'")
        return action

    def update_policy(
        self,
        state: Dict[str, Any],
        action: str,
        reward: float,
        next_state: Dict[str, Any],
        done: bool = False,
    ) -> float:
        """
        Update Q-value using Q-Learning update rule.

        Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode is done

        Returns:
            TD error (temporal difference error)
        """
        state_key = self._state_to_key(state)
        next_state_key = self._state_to_key(next_state)

        # Current Q-value
        current_q = self.q_table[state_key][action]

        # Maximum Q-value for next state (0 if terminal state)
        if done:
            max_next_q = 0.0
        else:
            next_q_values = self.q_table[next_state_key]
            max_next_q = max(next_q_values.values()) if next_q_values else 0.0

        # Q-Learning update rule
        td_target = reward + self.discount_factor * max_next_q
        td_error = td_target - current_q
        new_q = current_q + self.learning_rate * td_error

        # Update Q-table
        self.q_table[state_key][action] = new_q

        # Update statistics
        self.stats["updates"] += 1
        self.stats["total_reward"] += reward
        self.stats["average_reward"] = (
            self.stats["total_reward"] / self.stats["updates"]
        )

        logger.debug(
            f"Updated Q({state_key[:20]}..., {action}): "
            f"{current_q:.3f} -> {new_q:.3f} (reward={reward:.3f})"
        )

        return td_error

    def add_experience(self, experience: Experience) -> None:
        """
        Add an experience to the replay buffer.

        Args:
            experience: Experience to add
        """
        self.replay_buffer.append(experience)
        logger.debug(f"Added experience to replay buffer (size={len(self.replay_buffer)})")

    def train_from_replay(self, batch_size: int = 32, iterations: int = 1) -> float:
        """
        Train from experiences in replay buffer.

        Args:
            batch_size: Number of experiences to sample
            iterations: Number of training iterations

        Returns:
            Average TD error
        """
        if len(self.replay_buffer) < batch_size:
            logger.debug("Not enough experiences in replay buffer for training")
            return 0.0

        total_td_error = 0.0
        samples_processed = 0

        for _ in range(iterations):
            # Sample random batch
            batch = random.sample(list(self.replay_buffer), batch_size)

            # Update policy for each experience
            for exp in batch:
                td_error = self.update_policy(
                    state=exp.state,
                    action=exp.action,
                    reward=exp.reward,
                    next_state=exp.next_state,
                    done=exp.done,
                )
                total_td_error += abs(td_error)
                samples_processed += 1

        avg_td_error = total_td_error / samples_processed if samples_processed > 0 else 0.0

        logger.info(
            f"Trained on {samples_processed} experiences, "
            f"avg TD error: {avg_td_error:.4f}"
        )

        return avg_td_error

    def decay_exploration(self) -> None:
        """Decay exploration rate."""
        old_rate = self.exploration_rate
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.exploration_decay,
        )
        if old_rate != self.exploration_rate:
            logger.debug(f"Exploration rate: {old_rate:.4f} -> {self.exploration_rate:.4f}")

    def end_episode(self) -> None:
        """Mark the end of an episode."""
        self.stats["episodes"] += 1
        self.decay_exploration()
        logger.debug(f"Episode {self.stats['episodes']} ended")

    def save_model(self, path: str) -> None:
        """
        Save Q-table and model state to disk.

        Args:
            path: Path to save the model
        """
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            "agent_id": self.agent_id,
            "q_table": dict(self.q_table),
            "stats": self.stats,
            "exploration_rate": self.exploration_rate,
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
        }

        try:
            with open(save_path, "wb") as f:
                pickle.dump(model_data, f)
            logger.info(f"Saved Q-Learning model to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def load_model(self, path: str) -> bool:
        """
        Load Q-table and model state from disk.

        Args:
            path: Path to load the model from

        Returns:
            True if successful, False otherwise
        """
        load_path = Path(path)

        if not load_path.exists():
            logger.warning(f"Model file not found: {load_path}")
            return False

        try:
            with open(load_path, "rb") as f:
                model_data = pickle.load(f)

            # Restore Q-table
            self.q_table = defaultdict(
                lambda: defaultdict(float),
                {k: defaultdict(float, v) for k, v in model_data["q_table"].items()}
            )

            # Restore other parameters
            self.stats = model_data.get("stats", self.stats)
            self.exploration_rate = model_data.get("exploration_rate", self.exploration_rate)

            logger.info(
                f"Loaded Q-Learning model from {load_path} "
                f"({len(self.q_table)} states, {self.stats['updates']} updates)"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    def get_q_value(self, state: Dict[str, Any], action: str) -> float:
        """
        Get Q-value for a state-action pair.

        Args:
            state: State
            action: Action

        Returns:
            Q-value
        """
        state_key = self._state_to_key(state)
        return self.q_table[state_key][action]

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            **self.stats,
            "exploration_rate": self.exploration_rate,
            "q_table_size": len(self.q_table),
            "replay_buffer_size": len(self.replay_buffer),
        }

    def _state_to_key(self, state: Dict[str, Any]) -> str:
        """
        Convert state dictionary to a hashable key.

        Args:
            state: State dictionary

        Returns:
            String key representation
        """
        # Simple approach: sort keys and create string representation
        # For more complex states, you might want a better encoding
        sorted_items = sorted(state.items())
        key_parts = []

        for k, v in sorted_items:
            if isinstance(v, (int, float, str, bool)):
                key_parts.append(f"{k}={v}")
            elif isinstance(v, (list, tuple)):
                key_parts.append(f"{k}={len(v)}")
            else:
                key_parts.append(f"{k}={type(v).__name__}")

        return "|".join(key_parts)

    def clear_replay_buffer(self) -> None:
        """Clear the experience replay buffer."""
        self.replay_buffer.clear()
        logger.debug("Cleared replay buffer")

    def to_dict(self) -> Dict[str, Any]:
        """Convert learning state to dictionary."""
        return {
            "agent_id": self.agent_id,
            "statistics": self.get_statistics(),
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "exploration_rate": self.exploration_rate,
        }
