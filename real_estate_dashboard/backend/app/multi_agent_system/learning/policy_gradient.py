"""
Policy Gradient methods for advanced reinforcement learning.

Implements modern MARL techniques from 2025 research.
"""

import numpy as np
import pickle
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from collections import deque
from loguru import logger

from app.multi_agent_system.core.types import Experience


class PolicyGradientEngine:
    """
    Policy Gradient learning engine with modern enhancements.

    Features:
    - REINFORCE algorithm
    - Actor-Critic architecture
    - Advantage estimation
    - Human feedback integration (MARLHF)
    """

    def __init__(
        self,
        agent_id: str,
        learning_rate: float = 0.001,
        discount_factor: float = 0.99,
        entropy_coef: float = 0.01,
        value_coef: float = 0.5,
    ):
        """
        Initialize policy gradient engine.

        Args:
            agent_id: ID of the agent
            learning_rate: Learning rate
            discount_factor: Discount factor (gamma)
            entropy_coef: Entropy coefficient for exploration
            value_coef: Value function coefficient
        """
        self.agent_id = agent_id
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef

        # Policy parameters (state -> action probabilities)
        self.policy: Dict[str, Dict[str, float]] = {}

        # Value function (state -> value estimate)
        self.value_function: Dict[str, float] = {}

        # Experience buffer for batch updates
        self.episode_buffer: List[Experience] = []

        # Human feedback integration
        self.human_feedback: List[Tuple[str, str, float]] = []  # (state, action, preference)

        # Statistics
        self.stats = {
            "episodes": 0,
            "updates": 0,
            "total_reward": 0.0,
            "average_reward": 0.0,
            "policy_entropy": 0.0,
        }

        logger.info(f"PolicyGradient engine initialized for {agent_id}")

    def get_action_probabilities(
        self, state: Dict[str, Any], available_actions: List[str]
    ) -> Dict[str, float]:
        """
        Get action probabilities for a state.

        Args:
            state: Current state
            available_actions: List of available actions

        Returns:
            Dictionary mapping actions to probabilities
        """
        state_key = self._state_to_key(state)

        if state_key not in self.policy:
            # Initialize with uniform distribution
            self.policy[state_key] = {
                action: 1.0 / len(available_actions) for action in available_actions
            }

        # Get probabilities (filtered to available actions)
        probs = {}
        total = 0.0

        for action in available_actions:
            prob = self.policy[state_key].get(action, 1.0 / len(available_actions))
            probs[action] = prob
            total += prob

        # Normalize
        if total > 0:
            probs = {action: prob / total for action, prob in probs.items()}

        return probs

    def select_action(
        self, state: Dict[str, Any], available_actions: List[str]
    ) -> str:
        """
        Select action using current policy.

        Args:
            state: Current state
            available_actions: Available actions

        Returns:
            Selected action
        """
        probs = self.get_action_probabilities(state, available_actions)

        # Sample action from distribution
        actions = list(probs.keys())
        probabilities = list(probs.values())

        action = np.random.choice(actions, p=probabilities)

        return action

    def add_experience(self, experience: Experience) -> None:
        """
        Add experience to episode buffer.

        Args:
            experience: Experience to add
        """
        self.episode_buffer.append(experience)

    def end_episode(self) -> Dict[str, float]:
        """
        End episode and update policy.

        Returns:
            Update metrics
        """
        if not self.episode_buffer:
            return {}

        # Calculate returns
        returns = self._calculate_returns(self.episode_buffer)

        # Update policy using returns
        metrics = self._update_policy(self.episode_buffer, returns)

        # Clear buffer
        self.episode_buffer.clear()

        self.stats["episodes"] += 1

        # Update average reward after incrementing episodes
        if self.stats["episodes"] > 0:
            self.stats["average_reward"] = self.stats["total_reward"] / self.stats["episodes"]

        return metrics

    def _calculate_returns(self, experiences: List[Experience]) -> List[float]:
        """
        Calculate discounted returns.

        Args:
            experiences: List of experiences

        Returns:
            List of returns for each timestep
        """
        returns = []
        G = 0.0

        # Calculate returns backward
        for exp in reversed(experiences):
            G = exp.reward + self.discount_factor * G
            returns.insert(0, G)

        return returns

    def _update_policy(
        self, experiences: List[Experience], returns: List[float]
    ) -> Dict[str, float]:
        """
        Update policy using policy gradient.

        Args:
            experiences: Episode experiences
            returns: Calculated returns

        Returns:
            Update metrics
        """
        total_loss = 0.0
        policy_loss = 0.0
        value_loss = 0.0
        entropy_loss = 0.0

        for exp, G in zip(experiences, returns):
            state_key = self._state_to_key(exp.state)

            # Update value function
            if state_key not in self.value_function:
                self.value_function[state_key] = 0.0

            baseline = self.value_function[state_key]
            advantage = G - baseline

            # Update value function (TD error)
            value_error = G - baseline
            self.value_function[state_key] += self.learning_rate * value_error
            value_loss += value_error ** 2

            # Update policy (policy gradient with advantage)
            if state_key in self.policy and exp.action in self.policy[state_key]:
                # Get current probability
                prob = self.policy[state_key][exp.action]

                # Policy gradient update
                # Increase probability of actions with positive advantage
                gradient = advantage * (1.0 - prob)  # Simplified gradient
                new_prob = prob + self.learning_rate * gradient

                # Clip to valid range
                new_prob = np.clip(new_prob, 0.01, 0.99)

                self.policy[state_key][exp.action] = float(new_prob)

                # Normalize probabilities
                self._normalize_policy(state_key)

                policy_loss += -np.log(prob + 1e-8) * advantage

            # Calculate entropy for exploration
            if state_key in self.policy:
                probs = list(self.policy[state_key].values())
                entropy = -sum(p * np.log(p + 1e-8) for p in probs if p > 0)
                entropy_loss += entropy

        # Calculate average losses
        n = len(experiences)
        if n > 0:
            policy_loss /= n
            value_loss /= n
            entropy_loss /= n
            total_loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy_loss

        # Update statistics
        self.stats["updates"] += 1
        total_reward = sum(exp.reward for exp in experiences)
        self.stats["total_reward"] += total_reward
        self.stats["policy_entropy"] = entropy_loss

        logger.debug(
            f"Policy update: loss={total_loss:.4f}, "
            f"policy_loss={policy_loss:.4f}, "
            f"value_loss={value_loss:.4f}"
        )

        return {
            "total_loss": float(total_loss),
            "policy_loss": float(policy_loss),
            "value_loss": float(value_loss),
            "entropy": float(entropy_loss),
            "episode_return": total_reward,
        }

    def _normalize_policy(self, state_key: str) -> None:
        """Normalize policy probabilities for a state."""
        if state_key not in self.policy:
            return

        total = sum(self.policy[state_key].values())
        if total > 0:
            for action in self.policy[state_key]:
                self.policy[state_key][action] /= total

    def add_human_feedback(
        self, state: Dict[str, Any], action: str, preference: float
    ) -> None:
        """
        Add human feedback (MARLHF).

        Args:
            state: State
            action: Action taken
            preference: Human preference score (-1.0 to 1.0)
        """
        state_key = self._state_to_key(state)
        self.human_feedback.append((state_key, action, preference))

        # Immediately update policy based on feedback
        if state_key in self.policy and action in self.policy[state_key]:
            # Adjust probability based on feedback
            current_prob = self.policy[state_key][action]

            # Positive feedback increases probability
            adjustment = self.learning_rate * preference * (1.0 - current_prob)
            new_prob = current_prob + adjustment

            self.policy[state_key][action] = float(np.clip(new_prob, 0.01, 0.99))
            self._normalize_policy(state_key)

            logger.info(
                f"Human feedback incorporated: {action} "
                f"(preference={preference:.2f})"
            )

    def save_model(self, path: str) -> None:
        """
        Save policy and value function.

        Args:
            path: Path to save the model
        """
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            "agent_id": self.agent_id,
            "policy": dict(self.policy),
            "value_function": dict(self.value_function),
            "stats": self.stats,
            "human_feedback": self.human_feedback,
        }

        try:
            with open(save_path, "wb") as f:
                pickle.dump(model_data, f)
            logger.info(f"Saved policy gradient model to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def load_model(self, path: str) -> bool:
        """
        Load policy and value function.

        Args:
            path: Path to load from

        Returns:
            True if successful
        """
        load_path = Path(path)

        if not load_path.exists():
            logger.warning(f"Model file not found: {load_path}")
            return False

        try:
            with open(load_path, "rb") as f:
                model_data = pickle.load(f)

            self.policy = model_data.get("policy", {})
            self.value_function = model_data.get("value_function", {})
            self.stats = model_data.get("stats", self.stats)
            self.human_feedback = model_data.get("human_feedback", [])

            logger.info(f"Loaded policy gradient model from {load_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            **self.stats,
            "policy_size": len(self.policy),
            "value_function_size": len(self.value_function),
            "human_feedback_count": len(self.human_feedback),
        }

    def _state_to_key(self, state: Dict[str, Any]) -> str:
        """Convert state to string key."""
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
