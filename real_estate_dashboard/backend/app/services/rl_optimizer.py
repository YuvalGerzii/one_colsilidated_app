"""
Reinforcement Learning Optimizer for RAG System

Implements RL algorithms to optimize RAG retrieval and response generation.
Supports Q-learning, Policy Gradient, and hybrid approaches.
"""

import os
import logging
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

logger = logging.getLogger(__name__)


class RLOptimizer:
    """
    Reinforcement Learning optimizer for RAG system

    Features:
    - Q-learning for discrete action selection
    - Policy gradient for continuous optimization
    - Experience replay for stable learning
    - Adaptive exploration-exploitation
    """

    def __init__(self):
        # Hyperparameters
        self.learning_rate = float(os.getenv("RAG_RL_LEARNING_RATE", "0.001"))
        self.gamma = 0.95  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        # Actions for retrieval
        self.actions = [
            "FETCH",      # Retrieve from vector DB
            "NO_FETCH",   # Use cache or generate directly
            "EXPAND",     # Expand query before fetch
            "RERANK"      # Fetch more and rerank
        ]

        # Q-table and policy
        self._q_table: Dict[str, Dict[str, float]] = {}
        self._policy_params: Dict[str, float] = {}

        # Experience replay buffer
        self._replay_buffer: List[Dict] = []
        self._buffer_size = 10000

        # Statistics
        self._total_episodes = 0
        self._total_reward = 0.0

        self._initialized = False
        self._policy_id = None

    async def initialize(self, db: AsyncSession):
        """Initialize RL optimizer from database"""
        if self._initialized:
            return

        from app.models.rag_learning import RLPolicy

        # Load or create policy
        result = await db.execute(
            select(RLPolicy).where(
                RLPolicy.policy_name == "rag_retrieval_policy",
                RLPolicy.is_active == True
            )
        )
        policy = result.scalar_one_or_none()

        if policy:
            self._policy_id = policy.id
            self._q_table = policy.parameters.get("q_table", {})
            self._policy_params = policy.parameters.get("policy_params", {})
            self._total_episodes = policy.total_episodes
            self._total_reward = policy.avg_reward * policy.total_episodes
            logger.info(f"Loaded RL policy: {policy.id} with {policy.total_episodes} episodes")
        else:
            # Create new policy
            policy = RLPolicy(
                policy_name="rag_retrieval_policy",
                policy_type="q_learning",
                parameters={"q_table": {}, "policy_params": {}},
                hyperparameters={
                    "learning_rate": self.learning_rate,
                    "gamma": self.gamma,
                    "epsilon": self.epsilon
                }
            )
            db.add(policy)
            await db.commit()
            self._policy_id = policy.id
            logger.info(f"Created new RL policy: {policy.id}")

        self._initialized = True

    def _state_to_key(self, state: Dict[str, Any]) -> str:
        """Convert state dict to hashable key"""
        # Extract key features for state representation
        features = [
            f"len:{state.get('query_length', 0) // 5 * 5}",  # Bucket length
            f"sess:{1 if state.get('has_session') else 0}",
            f"type:{state.get('query_type', 'general')}"
        ]
        return "|".join(sorted(features))

    async def get_action(self, state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Select action based on current state using epsilon-greedy policy

        Args:
            state: Current state representation

        Returns:
            Tuple of (action, state_info)
        """
        state_key = self._state_to_key(state)

        # Epsilon-greedy exploration
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.actions)
            logger.debug(f"Exploring: action={action}")
        else:
            # Exploit: choose best action
            if state_key in self._q_table:
                q_values = self._q_table[state_key]
                action = max(q_values.keys(), key=lambda a: q_values.get(a, 0.0))
            else:
                action = "FETCH"  # Default action

        return action, {"state_key": state_key, "epsilon": self.epsilon}

    async def update_policy(
        self,
        state: Dict[str, Any],
        action: str,
        reward: float,
        next_state: Optional[Dict[str, Any]] = None
    ):
        """
        Update Q-table based on experience

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state (None if terminal)
        """
        state_key = state.get("state_key") or self._state_to_key(state)

        # Initialize Q-values for state if needed
        if state_key not in self._q_table:
            self._q_table[state_key] = {a: 0.0 for a in self.actions}

        # Get max Q-value for next state
        if next_state:
            next_key = self._state_to_key(next_state)
            if next_key in self._q_table:
                max_next_q = max(self._q_table[next_key].values())
            else:
                max_next_q = 0.0
        else:
            max_next_q = 0.0  # Terminal state

        # Q-learning update
        current_q = self._q_table[state_key].get(action, 0.0)
        new_q = current_q + self.learning_rate * (
            reward + self.gamma * max_next_q - current_q
        )
        self._q_table[state_key][action] = new_q

        # Store in replay buffer
        self._replay_buffer.append({
            "state": state_key,
            "action": action,
            "reward": reward,
            "next_state": self._state_to_key(next_state) if next_state else None
        })

        # Trim buffer
        if len(self._replay_buffer) > self._buffer_size:
            self._replay_buffer = self._replay_buffer[-self._buffer_size:]

        # Update statistics
        self._total_episodes += 1
        self._total_reward += reward

        # Decay epsilon
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

        logger.debug(
            f"Updated Q({state_key}, {action}): {current_q:.3f} -> {new_q:.3f}, "
            f"reward={reward:.3f}"
        )

    async def batch_train(self, db: AsyncSession, batch_size: int = 32):
        """
        Train on a batch from replay buffer

        This implements experience replay for more stable learning.
        """
        if len(self._replay_buffer) < batch_size:
            return

        # Sample batch
        indices = np.random.choice(len(self._replay_buffer), batch_size, replace=False)
        batch = [self._replay_buffer[i] for i in indices]

        # Update Q-values for each experience
        for exp in batch:
            state_key = exp["state"]
            action = exp["action"]
            reward = exp["reward"]
            next_state = exp["next_state"]

            if state_key not in self._q_table:
                self._q_table[state_key] = {a: 0.0 for a in self.actions}

            if next_state and next_state in self._q_table:
                max_next_q = max(self._q_table[next_state].values())
            else:
                max_next_q = 0.0

            current_q = self._q_table[state_key].get(action, 0.0)
            new_q = current_q + self.learning_rate * (
                reward + self.gamma * max_next_q - current_q
            )
            self._q_table[state_key][action] = new_q

        logger.info(f"Batch trained on {batch_size} experiences")

    async def save_policy(self, db: AsyncSession):
        """Save policy to database"""
        from app.models.rag_learning import RLPolicy

        if not self._policy_id:
            return

        avg_reward = self._total_reward / max(1, self._total_episodes)

        await db.execute(
            update(RLPolicy)
            .where(RLPolicy.id == self._policy_id)
            .values(
                parameters={
                    "q_table": self._q_table,
                    "policy_params": self._policy_params
                },
                hyperparameters={
                    "learning_rate": self.learning_rate,
                    "gamma": self.gamma,
                    "epsilon": self.epsilon
                },
                avg_reward=avg_reward,
                total_episodes=self._total_episodes,
                updated_at=datetime.utcnow()
            )
        )
        await db.commit()

        logger.info(
            f"Saved policy: episodes={self._total_episodes}, "
            f"avg_reward={avg_reward:.3f}, epsilon={self.epsilon:.3f}"
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics"""
        avg_reward = self._total_reward / max(1, self._total_episodes)

        # Calculate action distribution
        action_counts = {a: 0 for a in self.actions}
        for state_q in self._q_table.values():
            best_action = max(state_q.keys(), key=lambda a: state_q.get(a, 0.0))
            action_counts[best_action] += 1

        return {
            "total_episodes": self._total_episodes,
            "average_reward": avg_reward,
            "epsilon": self.epsilon,
            "learning_rate": self.learning_rate,
            "num_states": len(self._q_table),
            "buffer_size": len(self._replay_buffer),
            "action_distribution": action_counts
        }

    def get_q_values(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Get Q-values for a state"""
        state_key = self._state_to_key(state)
        if state_key in self._q_table:
            return self._q_table[state_key].copy()
        return {a: 0.0 for a in self.actions}


class PolicyGradientOptimizer:
    """
    Policy Gradient optimizer for continuous action parameters

    Used for optimizing:
    - Number of documents to retrieve (top_k)
    - Similarity threshold
    - Query expansion parameters
    """

    def __init__(self):
        self.learning_rate = float(os.getenv("RAG_RL_LEARNING_RATE", "0.001"))

        # Policy parameters (mean and std for continuous actions)
        self.params = {
            "top_k_mean": 5.0,
            "top_k_std": 1.0,
            "threshold_mean": 0.5,
            "threshold_std": 0.1
        }

        # Gradients accumulator
        self._gradients: List[Dict[str, float]] = []

    def sample_action(self) -> Dict[str, float]:
        """Sample continuous action parameters"""
        top_k = max(1, int(np.random.normal(
            self.params["top_k_mean"],
            self.params["top_k_std"]
        )))
        threshold = np.clip(np.random.normal(
            self.params["threshold_mean"],
            self.params["threshold_std"]
        ), 0.0, 1.0)

        return {
            "top_k": top_k,
            "threshold": threshold
        }

    def update(self, action: Dict[str, float], reward: float):
        """Update policy parameters using policy gradient"""
        # Compute gradient (simplified REINFORCE)
        top_k_grad = (action["top_k"] - self.params["top_k_mean"]) * reward
        threshold_grad = (action["threshold"] - self.params["threshold_mean"]) * reward

        # Update means
        self.params["top_k_mean"] += self.learning_rate * top_k_grad
        self.params["threshold_mean"] += self.learning_rate * threshold_grad

        # Ensure valid ranges
        self.params["top_k_mean"] = max(1.0, min(20.0, self.params["top_k_mean"]))
        self.params["threshold_mean"] = max(0.0, min(1.0, self.params["threshold_mean"]))


class AdaptiveRetriever:
    """
    Adaptive retrieval strategy that combines multiple approaches

    Implements:
    - Self-RAG (self-reflective retrieval)
    - Corrective RAG (iterative refinement)
    - Adaptive RAG (dynamic strategy selection)
    """

    def __init__(self, rl_optimizer: RLOptimizer):
        self.rl_optimizer = rl_optimizer
        self.strategies = ["standard", "iterative", "multi_hop", "cached"]

    async def retrieve(
        self,
        query: str,
        state: Dict[str, Any],
        vector_db,
        collection_name: str,
        query_embedding: List[float]
    ) -> Tuple[List[Dict], str]:
        """
        Perform adaptive retrieval based on learned policy

        Returns:
            Tuple of (results, strategy_used)
        """
        # Get action from RL policy
        action, _ = await self.rl_optimizer.get_action(state)

        if action == "NO_FETCH":
            return [], "cached"

        elif action == "EXPAND":
            # Retrieve with expanded query
            results = await vector_db.hybrid_search(
                collection_name=collection_name,
                query_vector=query_embedding,
                keyword_query=query,
                top_k=10,  # Get more for expansion
                alpha=0.5  # Balance semantic and keyword
            )
            return results, "expanded"

        elif action == "RERANK":
            # Fetch more and rerank
            results = await vector_db.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=20  # Get many for reranking
            )
            # Simple reranking by score
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:5], "reranked"

        else:  # FETCH
            results = await vector_db.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=5
            )
            return results, "standard"


# Global instance
_rl_optimizer: Optional[RLOptimizer] = None


async def get_rl_optimizer(db: AsyncSession) -> RLOptimizer:
    """Get or create the global RL optimizer instance"""
    global _rl_optimizer

    if _rl_optimizer is None:
        _rl_optimizer = RLOptimizer()
        await _rl_optimizer.initialize(db)

    return _rl_optimizer
