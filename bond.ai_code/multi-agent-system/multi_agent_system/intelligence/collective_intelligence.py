"""
Collective intelligence for multi-agent systems.

Enables emergent behavior through:
- Knowledge aggregation from multiple agents
- Collaborative problem-solving
- Swarm intelligence
- Collective decision-making
- Emergent patterns and insights
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Callable, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum
from loguru import logger
import statistics


class AggregationMethod(Enum):
    """Methods for aggregating agent outputs."""
    AVERAGE = "average"
    WEIGHTED_AVERAGE = "weighted_average"
    MAJORITY_VOTE = "majority_vote"
    CONSENSUS = "consensus"
    BEST_QUALITY = "best_quality"
    ENSEMBLE = "ensemble"


@dataclass
class AgentContribution:
    """A contribution from an agent to collective intelligence."""
    agent_id: str
    data: Any
    quality_score: float = 0.0
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CollectiveKnowledge:
    """Aggregated knowledge from multiple agents."""
    topic: str
    contributions: List[AgentContribution] = field(default_factory=list)
    aggregated_result: Optional[Any] = None
    confidence_score: float = 0.0
    quality_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CollectiveIntelligence:
    """
    System for collective intelligence among agents.

    Features:
    - Aggregate knowledge from multiple agents
    - Identify emergent patterns
    - Collaborative problem-solving
    - Quality-weighted decision making
    - Knowledge synthesis
    """

    def __init__(self):
        """Initialize the collective intelligence system."""
        self.knowledge_base: Dict[str, CollectiveKnowledge] = {}

        # Agent performance tracking
        self.agent_performance: Dict[str, Dict[str, float]] = defaultdict(
            lambda: {"quality_avg": 0.0, "contribution_count": 0}
        )

        # Emergent patterns
        self.patterns: List[Dict[str, Any]] = []

        # Statistics
        self.stats = {
            "total_contributions": 0,
            "total_topics": 0,
            "total_aggregations": 0,
            "patterns_discovered": 0,
        }

        logger.info("CollectiveIntelligence initialized")

    async def contribute(
        self,
        agent_id: str,
        topic: str,
        data: Any,
        quality_score: float = 0.0,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a contribution from an agent.

        Args:
            agent_id: ID of the contributing agent
            topic: Topic of the contribution
            data: The contribution data
            quality_score: Quality of the contribution (0-1)
            confidence: Confidence level (0-1)
            metadata: Additional metadata
        """
        contribution = AgentContribution(
            agent_id=agent_id,
            data=data,
            quality_score=quality_score,
            confidence=confidence,
            metadata=metadata or {}
        )

        # Create or update knowledge base entry
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = CollectiveKnowledge(topic=topic)
            self.stats["total_topics"] += 1

        knowledge = self.knowledge_base[topic]
        knowledge.contributions.append(contribution)
        knowledge.updated_at = datetime.now()

        # Update agent performance
        perf = self.agent_performance[agent_id]
        count = perf["contribution_count"]
        perf["quality_avg"] = (
            perf["quality_avg"] * count + quality_score
        ) / (count + 1)
        perf["contribution_count"] = count + 1

        self.stats["total_contributions"] += 1

        logger.debug(
            f"Agent {agent_id} contributed to '{topic}' "
            f"(quality={quality_score:.2f}, confidence={confidence:.2f})"
        )

    async def aggregate(
        self,
        topic: str,
        method: AggregationMethod = AggregationMethod.WEIGHTED_AVERAGE,
        min_contributions: int = 1
    ) -> Optional[Any]:
        """
        Aggregate contributions on a topic.

        Args:
            topic: Topic to aggregate
            method: Aggregation method
            min_contributions: Minimum contributions required

        Returns:
            Aggregated result, or None if insufficient contributions
        """
        if topic not in self.knowledge_base:
            logger.warning(f"No knowledge found for topic '{topic}'")
            return None

        knowledge = self.knowledge_base[topic]

        if len(knowledge.contributions) < min_contributions:
            logger.info(
                f"Insufficient contributions for '{topic}' "
                f"({len(knowledge.contributions)}/{min_contributions})"
            )
            return None

        # Apply aggregation method
        result = None
        confidence = 0.0
        quality = 0.0

        if method == AggregationMethod.AVERAGE:
            result, confidence, quality = self._aggregate_average(knowledge.contributions)

        elif method == AggregationMethod.WEIGHTED_AVERAGE:
            result, confidence, quality = self._aggregate_weighted_average(
                knowledge.contributions
            )

        elif method == AggregationMethod.MAJORITY_VOTE:
            result, confidence, quality = self._aggregate_majority_vote(
                knowledge.contributions
            )

        elif method == AggregationMethod.BEST_QUALITY:
            result, confidence, quality = self._aggregate_best_quality(
                knowledge.contributions
            )

        elif method == AggregationMethod.CONSENSUS:
            result, confidence, quality = self._aggregate_consensus(
                knowledge.contributions
            )

        elif method == AggregationMethod.ENSEMBLE:
            result, confidence, quality = self._aggregate_ensemble(
                knowledge.contributions
            )

        # Update knowledge base
        knowledge.aggregated_result = result
        knowledge.confidence_score = confidence
        knowledge.quality_score = quality

        self.stats["total_aggregations"] += 1

        logger.info(
            f"Aggregated '{topic}' using {method.value}: "
            f"quality={quality:.2f}, confidence={confidence:.2f}"
        )

        return result

    def _aggregate_average(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Simple average of all contributions."""
        if not contributions:
            return None, 0.0, 0.0

        # For numeric data
        numeric_data = []
        for contrib in contributions:
            if isinstance(contrib.data, (int, float)):
                numeric_data.append(contrib.data)

        if numeric_data:
            result = statistics.mean(numeric_data)
            confidence = statistics.mean([c.confidence for c in contributions])
            quality = statistics.mean([c.quality_score for c in contributions])
            return result, confidence, quality

        # For non-numeric, just return most common or first
        return contributions[0].data, 0.5, 0.5

    def _aggregate_weighted_average(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Weighted average based on quality and confidence."""
        if not contributions:
            return None, 0.0, 0.0

        # For numeric data
        numeric_data = []
        weights = []

        for contrib in contributions:
            if isinstance(contrib.data, (int, float)):
                numeric_data.append(contrib.data)
                # Weight by quality * confidence
                weight = contrib.quality_score * contrib.confidence
                weights.append(weight)

        if numeric_data and sum(weights) > 0:
            result = sum(d * w for d, w in zip(numeric_data, weights)) / sum(weights)
            confidence = sum(c.confidence * w for c, w in zip(contributions, weights)) / sum(weights)
            quality = sum(c.quality_score * w for c, w in zip(contributions, weights)) / sum(weights)
            return result, confidence, quality

        # For non-numeric, return highest quality contribution
        best = max(contributions, key=lambda c: c.quality_score * c.confidence)
        return best.data, best.confidence, best.quality_score

    def _aggregate_majority_vote(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Majority voting."""
        if not contributions:
            return None, 0.0, 0.0

        # Count votes
        votes: Dict[str, List[AgentContribution]] = defaultdict(list)

        for contrib in contributions:
            # Convert data to string for voting
            vote_key = str(contrib.data)
            votes[vote_key].append(contrib)

        # Find majority
        majority_key = max(votes.items(), key=lambda x: len(x[1]))[0]
        majority_contribs = votes[majority_key]

        # Calculate confidence and quality
        confidence = statistics.mean([c.confidence for c in majority_contribs])
        quality = statistics.mean([c.quality_score for c in majority_contribs])

        # Return the actual data (not string key)
        return majority_contribs[0].data, confidence, quality

    def _aggregate_best_quality(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Select contribution with best quality."""
        if not contributions:
            return None, 0.0, 0.0

        best = max(contributions, key=lambda c: c.quality_score)
        return best.data, best.confidence, best.quality_score

    def _aggregate_consensus(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Require consensus (all contributions similar)."""
        if not contributions:
            return None, 0.0, 0.0

        # For numeric data, check if standard deviation is low
        numeric_data = []
        for contrib in contributions:
            if isinstance(contrib.data, (int, float)):
                numeric_data.append(contrib.data)

        if numeric_data and len(numeric_data) > 1:
            mean_val = statistics.mean(numeric_data)
            stdev = statistics.stdev(numeric_data)

            # If stdev is less than 10% of mean, consider it consensus
            if stdev < abs(mean_val) * 0.1:
                confidence = 1.0  # High confidence due to consensus
                quality = statistics.mean([c.quality_score for c in contributions])
                return mean_val, confidence, quality
            else:
                # No consensus
                return None, 0.0, 0.0

        # For non-numeric, all must be identical
        first_data = str(contributions[0].data)
        if all(str(c.data) == first_data for c in contributions):
            confidence = 1.0
            quality = statistics.mean([c.quality_score for c in contributions])
            return contributions[0].data, confidence, quality

        return None, 0.0, 0.0

    def _aggregate_ensemble(
        self,
        contributions: List[AgentContribution]
    ) -> Tuple[Any, float, float]:
        """Ensemble of multiple methods."""
        # Try weighted average first, fall back to majority vote
        result, conf, qual = self._aggregate_weighted_average(contributions)

        if result is None:
            result, conf, qual = self._aggregate_majority_vote(contributions)

        # Boost confidence if multiple methods agree
        conf *= 1.1  # 10% boost for ensemble
        conf = min(conf, 1.0)

        return result, conf, qual

    async def detect_patterns(
        self,
        min_occurrences: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Detect emergent patterns from contributions.

        Args:
            min_occurrences: Minimum occurrences to consider a pattern

        Returns:
            List of detected patterns
        """
        patterns = []

        # Look for common topics
        topic_counts = defaultdict(int)
        for topic in self.knowledge_base.keys():
            topic_counts[topic] = len(self.knowledge_base[topic].contributions)

        # Look for agent collaboration patterns
        agent_pairs: Dict[Tuple[str, str], int] = defaultdict(int)

        for knowledge in self.knowledge_base.values():
            agents = set(c.agent_id for c in knowledge.contributions)

            # Count co-occurrences
            for a1 in agents:
                for a2 in agents:
                    if a1 < a2:  # Avoid duplicates
                        agent_pairs[(a1, a2)] += 1

        # Patterns: frequent collaborations
        for (a1, a2), count in agent_pairs.items():
            if count >= min_occurrences:
                pattern = {
                    "type": "collaboration",
                    "agents": [a1, a2],
                    "frequency": count,
                    "detected_at": datetime.now(),
                }
                patterns.append(pattern)
                self.stats["patterns_discovered"] += 1

        # Patterns: high-performing agent pairs
        for (a1, a2), count in agent_pairs.items():
            if count >= 2:
                # Check average quality when they work together
                joint_topics = []

                for topic, knowledge in self.knowledge_base.items():
                    agents_in_topic = set(c.agent_id for c in knowledge.contributions)
                    if a1 in agents_in_topic and a2 in agents_in_topic:
                        joint_topics.append(knowledge.quality_score)

                if joint_topics:
                    avg_quality = statistics.mean(joint_topics)

                    if avg_quality > 0.8:  # High quality threshold
                        pattern = {
                            "type": "high_performance_pair",
                            "agents": [a1, a2],
                            "average_quality": avg_quality,
                            "collaborations": count,
                            "detected_at": datetime.now(),
                        }
                        patterns.append(pattern)

        self.patterns.extend(patterns)

        logger.info(f"Detected {len(patterns)} emergent patterns")

        return patterns

    def get_collective_knowledge(self, topic: str) -> Optional[CollectiveKnowledge]:
        """Get collective knowledge on a topic."""
        return self.knowledge_base.get(topic)

    def get_agent_reputation(self, agent_id: str) -> Dict[str, Any]:
        """
        Get reputation metrics for an agent.

        Args:
            agent_id: ID of the agent

        Returns:
            Reputation metrics
        """
        if agent_id not in self.agent_performance:
            return {
                "agent_id": agent_id,
                "quality_average": 0.0,
                "contribution_count": 0,
                "reputation_score": 0.0,
            }

        perf = self.agent_performance[agent_id]

        # Calculate reputation score (combines quality and quantity)
        quality_avg = perf["quality_avg"]
        contribution_count = perf["contribution_count"]

        # Reputation = quality * log(1 + contributions)
        import math
        reputation = quality_avg * math.log(1 + contribution_count)

        return {
            "agent_id": agent_id,
            "quality_average": quality_avg,
            "contribution_count": contribution_count,
            "reputation_score": reputation,
        }

    def get_top_contributors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top contributing agents by reputation."""
        reputations = [
            self.get_agent_reputation(agent_id)
            for agent_id in self.agent_performance.keys()
        ]

        # Sort by reputation score
        reputations.sort(key=lambda x: x["reputation_score"], reverse=True)

        return reputations[:limit]

    def get_system_intelligence(self) -> Dict[str, Any]:
        """Get overall system intelligence metrics."""
        total_contribs = sum(
            len(k.contributions) for k in self.knowledge_base.values()
        )

        avg_quality = 0.0
        if self.knowledge_base:
            qualities = [
                k.quality_score
                for k in self.knowledge_base.values()
                if k.quality_score > 0
            ]
            avg_quality = statistics.mean(qualities) if qualities else 0.0

        return {
            "total_topics": len(self.knowledge_base),
            "total_contributions": total_contribs,
            "total_agents": len(self.agent_performance),
            "average_quality": avg_quality,
            "patterns_discovered": len(self.patterns),
            "statistics": self.stats,
            "top_contributors": self.get_top_contributors(5),
        }

    def list_topics(self) -> List[Dict[str, Any]]:
        """List all topics with summary information."""
        return [
            {
                "topic": topic,
                "contributions": len(knowledge.contributions),
                "quality_score": knowledge.quality_score,
                "confidence_score": knowledge.confidence_score,
                "updated_at": knowledge.updated_at.isoformat(),
            }
            for topic, knowledge in self.knowledge_base.items()
        ]

    async def synthesize_knowledge(
        self,
        topics: List[str],
        synthesis_method: str = "combine"
    ) -> Dict[str, Any]:
        """
        Synthesize knowledge from multiple topics.

        Args:
            topics: List of topics to synthesize
            synthesis_method: Method for synthesis

        Returns:
            Synthesized knowledge
        """
        knowledge_items = []

        for topic in topics:
            if topic in self.knowledge_base:
                knowledge_items.append(self.knowledge_base[topic])

        if not knowledge_items:
            return {"success": False, "error": "No knowledge found for topics"}

        # Combine all contributions
        all_contributions = []
        for knowledge in knowledge_items:
            all_contributions.extend(knowledge.contributions)

        # Aggregate
        synthesized = CollectiveKnowledge(
            topic=f"synthesis_{'+'.join(topics)}",
            contributions=all_contributions
        )

        # Calculate combined metrics
        if all_contributions:
            synthesized.quality_score = statistics.mean(
                [c.quality_score for c in all_contributions]
            )
            synthesized.confidence_score = statistics.mean(
                [c.confidence for c in all_contributions]
            )

        logger.info(f"Synthesized knowledge from {len(topics)} topics")

        return {
            "success": True,
            "topics": topics,
            "total_contributions": len(all_contributions),
            "quality_score": synthesized.quality_score,
            "confidence_score": synthesized.confidence_score,
            "unique_agents": len(set(c.agent_id for c in all_contributions)),
        }
