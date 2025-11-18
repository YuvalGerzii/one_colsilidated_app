"""
Multi-Agent Ensemble Orchestrator

Based on research:
- Multi-Agent Deep Reinforcement Learning (ScienceDirect, 2022)
- Ensemble Methods in Algorithmic Trading (ACM, 2024)
- Collective Intelligence for Trading (Frontiers in AI, 2025)

Strategy: Combines signals from multiple specialized agents using
weighted voting, confidence-based aggregation, and meta-learning.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict
from ..base_agent import (
    BaseTradingAgent,
    AgentType,
    TradingSignal,
    SignalType,
    MarketData
)


class EnsembleMethod:
    """Ensemble aggregation methods"""
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_AVERAGE = "weighted_average"
    CONFIDENCE_WEIGHTED = "confidence_weighted"
    PERFORMANCE_WEIGHTED = "performance_weighted"
    ADAPTIVE = "adaptive"


class EnsembleAgent(BaseTradingAgent):
    """
    Multi-Agent Ensemble Orchestrator

    Combines signals from multiple trading agents to generate
    a robust consensus signal
    """

    def __init__(
        self,
        agent_id: str,
        agents: List[BaseTradingAgent],
        ensemble_method: str = EnsembleMethod.CONFIDENCE_WEIGHTED,
        min_agreement: float = 0.5,
        config: Dict[str, Any] = None
    ):
        """
        Initialize Ensemble Agent

        Args:
            agent_id: Unique identifier
            agents: List of agent instances to ensemble
            ensemble_method: Method for combining signals
            min_agreement: Minimum agreement threshold (0.0 to 1.0)
        """
        super().__init__(agent_id, AgentType.ENSEMBLE, config)
        self.agents = agents
        self.ensemble_method = ensemble_method
        self.min_agreement = min_agreement

        # Agent weights (can be adjusted based on performance)
        self.agent_weights = {agent.agent_id: 1.0 for agent in agents}

        # Track agent performance for adaptive weighting
        self.agent_performance = {
            agent.agent_id: {
                "correct_predictions": 0,
                "total_predictions": 0,
                "cumulative_pnl": 0.0
            }
            for agent in agents
        }

    def aggregate_signals_majority_vote(
        self,
        signals: List[TradingSignal]
    ) -> TradingSignal:
        """
        Aggregate signals using majority voting

        Returns the signal type with most votes
        """
        votes = defaultdict(int)

        for signal in signals:
            votes[signal.signal_type] += 1

        # Get majority signal
        majority_signal = max(votes.items(), key=lambda x: x[1])[0]

        # Calculate agreement percentage
        agreement = votes[majority_signal] / len(signals)

        # Average confidence from agents voting for majority
        majority_confidences = [
            s.confidence for s in signals
            if s.signal_type == majority_signal
        ]
        avg_confidence = np.mean(majority_confidences) if majority_confidences else 0.0

        # Adjust confidence by agreement level
        final_confidence = avg_confidence * agreement

        return TradingSignal(
            signal_type=majority_signal,
            confidence=final_confidence,
            symbol=signals[0].symbol if signals else "",
            timestamp=datetime.now(),
            reasoning=f"Majority vote: {votes[majority_signal]}/{len(signals)} agents, {agreement * 100:.1f}% agreement",
            metadata={
                "votes": dict(votes),
                "agreement": agreement,
                "num_agents": len(signals)
            }
        )

    def aggregate_signals_weighted_average(
        self,
        signals: List[TradingSignal]
    ) -> TradingSignal:
        """
        Aggregate signals using weighted average

        Converts signals to numerical scores and averages
        """
        signal_scores = {
            SignalType.STRONG_SELL: -2,
            SignalType.SELL: -1,
            SignalType.HOLD: 0,
            SignalType.BUY: 1,
            SignalType.STRONG_BUY: 2
        }

        weighted_sum = 0.0
        total_weight = 0.0

        for signal in signals:
            agent_id = next(
                (a.agent_id for a in self.agents if a.last_signal == signal),
                None
            )
            weight = self.agent_weights.get(agent_id, 1.0) if agent_id else 1.0

            score = signal_scores.get(signal.signal_type, 0)
            weighted_sum += score * weight * signal.confidence
            total_weight += weight

        # Calculate weighted average score
        avg_score = weighted_sum / total_weight if total_weight > 0 else 0

        # Convert score back to signal
        if avg_score >= 1.5:
            final_signal = SignalType.STRONG_BUY
        elif avg_score >= 0.5:
            final_signal = SignalType.BUY
        elif avg_score <= -1.5:
            final_signal = SignalType.STRONG_SELL
        elif avg_score <= -0.5:
            final_signal = SignalType.SELL
        else:
            final_signal = SignalType.HOLD

        final_confidence = min(abs(avg_score) / 2, 1.0)

        return TradingSignal(
            signal_type=final_signal,
            confidence=final_confidence,
            symbol=signals[0].symbol if signals else "",
            timestamp=datetime.now(),
            reasoning=f"Weighted average score: {avg_score:.2f}",
            metadata={
                "weighted_score": avg_score,
                "total_weight": total_weight,
                "num_agents": len(signals)
            }
        )

    def aggregate_signals_confidence_weighted(
        self,
        signals: List[TradingSignal]
    ) -> TradingSignal:
        """
        Aggregate signals weighted by confidence levels

        Higher confidence signals have more influence
        """
        signal_scores = {
            SignalType.STRONG_SELL: -2,
            SignalType.SELL: -1,
            SignalType.HOLD: 0,
            SignalType.BUY: 1,
            SignalType.STRONG_BUY: 2
        }

        weighted_sum = 0.0
        total_confidence = 0.0

        for signal in signals:
            score = signal_scores.get(signal.signal_type, 0)
            weighted_sum += score * signal.confidence
            total_confidence += signal.confidence

        # Calculate confidence-weighted average
        avg_score = weighted_sum / total_confidence if total_confidence > 0 else 0

        # Convert to signal
        if avg_score >= 1.0:
            final_signal = SignalType.BUY
        elif avg_score <= -1.0:
            final_signal = SignalType.SELL
        else:
            final_signal = SignalType.HOLD

        final_confidence = min(abs(avg_score), 1.0)

        # Calculate agreement (signals in same direction)
        same_direction = sum(
            1 for s in signals
            if (signal_scores.get(s.signal_type, 0) * avg_score) > 0
        )
        agreement = same_direction / len(signals) if signals else 0

        return TradingSignal(
            signal_type=final_signal,
            confidence=final_confidence * agreement,
            symbol=signals[0].symbol if signals else "",
            timestamp=datetime.now(),
            reasoning=f"Confidence-weighted: {avg_score:.2f}, {agreement * 100:.1f}% agreement",
            metadata={
                "weighted_score": avg_score,
                "agreement": agreement,
                "total_confidence": total_confidence,
                "num_agents": len(signals)
            }
        )

    def aggregate_signals_performance_weighted(
        self,
        signals: List[TradingSignal]
    ) -> TradingSignal:
        """
        Aggregate signals weighted by historical performance

        Better performing agents have more influence
        """
        signal_scores = {
            SignalType.STRONG_SELL: -2,
            SignalType.SELL: -1,
            SignalType.HOLD: 0,
            SignalType.BUY: 1,
            SignalType.STRONG_BUY: 2
        }

        weighted_sum = 0.0
        total_weight = 0.0

        for signal in signals:
            # Find agent that generated this signal
            agent_id = next(
                (a.agent_id for a in self.agents if a.last_signal == signal),
                None
            )

            if not agent_id:
                continue

            # Calculate performance weight
            perf = self.agent_performance.get(agent_id, {})
            total_preds = perf.get("total_predictions", 0)

            if total_preds > 0:
                accuracy = perf.get("correct_predictions", 0) / total_preds
                weight = accuracy * self.agent_weights.get(agent_id, 1.0)
            else:
                weight = 0.5  # Default weight for untested agents

            score = signal_scores.get(signal.signal_type, 0)
            weighted_sum += score * weight * signal.confidence
            total_weight += weight

        avg_score = weighted_sum / total_weight if total_weight > 0 else 0

        # Convert to signal
        if avg_score >= 1.0:
            final_signal = SignalType.BUY
        elif avg_score <= -1.0:
            final_signal = SignalType.SELL
        else:
            final_signal = SignalType.HOLD

        final_confidence = min(abs(avg_score), 1.0)

        return TradingSignal(
            signal_type=final_signal,
            confidence=final_confidence,
            symbol=signals[0].symbol if signals else "",
            timestamp=datetime.now(),
            reasoning=f"Performance-weighted: {avg_score:.2f}",
            metadata={
                "weighted_score": avg_score,
                "total_weight": total_weight,
                "num_agents": len(signals)
            }
        )

    def analyze(self, market_data: List[MarketData]) -> TradingSignal:
        """
        Analyze market data using ensemble of agents

        Args:
            market_data: List of MarketData objects

        Returns:
            Aggregated TradingSignal
        """
        if not market_data:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol="",
                timestamp=datetime.now(),
                reasoning="No market data available"
            )

        # Collect signals from all agents
        signals = []
        agent_signals = {}

        for agent in self.agents:
            if agent.is_active:
                signal = agent.analyze(market_data)
                signals.append(signal)
                agent_signals[agent.agent_id] = signal

        if not signals:
            return TradingSignal(
                signal_type=SignalType.HOLD,
                confidence=0.0,
                symbol=market_data[0].symbol,
                timestamp=datetime.now(),
                reasoning="No active agents in ensemble"
            )

        # Aggregate signals based on method
        if self.ensemble_method == EnsembleMethod.MAJORITY_VOTE:
            ensemble_signal = self.aggregate_signals_majority_vote(signals)
        elif self.ensemble_method == EnsembleMethod.WEIGHTED_AVERAGE:
            ensemble_signal = self.aggregate_signals_weighted_average(signals)
        elif self.ensemble_method == EnsembleMethod.CONFIDENCE_WEIGHTED:
            ensemble_signal = self.aggregate_signals_confidence_weighted(signals)
        elif self.ensemble_method == EnsembleMethod.PERFORMANCE_WEIGHTED:
            ensemble_signal = self.aggregate_signals_performance_weighted(signals)
        else:
            # Default to confidence-weighted
            ensemble_signal = self.aggregate_signals_confidence_weighted(signals)

        # Add individual agent signals to metadata
        ensemble_signal.metadata["individual_signals"] = {
            agent_id: {
                "signal": signal.signal_type.value,
                "confidence": signal.confidence,
                "reasoning": signal.reasoning
            }
            for agent_id, signal in agent_signals.items()
        }

        self.last_signal = ensemble_signal
        return ensemble_signal

    def train(self, historical_data: List[MarketData]) -> None:
        """
        Train all agents in the ensemble

        Args:
            historical_data: Historical market data
        """
        print(f"Training ensemble of {len(self.agents)} agents...")

        for agent in self.agents:
            print(f"\nTraining {agent.agent_type.value} agent ({agent.agent_id})...")
            agent.train(historical_data)

        print("\nEnsemble training complete")

    def update_agent_performance(
        self,
        agent_id: str,
        was_correct: bool,
        pnl: float
    ) -> None:
        """
        Update performance metrics for an agent

        Args:
            agent_id: Agent identifier
            was_correct: Whether prediction was correct
            pnl: Profit/loss from trade
        """
        if agent_id in self.agent_performance:
            perf = self.agent_performance[agent_id]
            perf["total_predictions"] += 1

            if was_correct:
                perf["correct_predictions"] += 1

            perf["cumulative_pnl"] += pnl

            # Update agent weight based on performance
            if perf["total_predictions"] >= 10:
                accuracy = perf["correct_predictions"] / perf["total_predictions"]
                # Weight between 0.5 and 2.0 based on accuracy
                self.agent_weights[agent_id] = 0.5 + (accuracy * 1.5)

    def get_agent_rankings(self) -> List[Dict[str, Any]]:
        """
        Get agents ranked by performance

        Returns:
            List of agent performance dictionaries, sorted by accuracy
        """
        rankings = []

        for agent in self.agents:
            perf = self.agent_performance.get(agent.agent_id, {})
            total = perf.get("total_predictions", 0)
            correct = perf.get("correct_predictions", 0)
            accuracy = correct / total if total > 0 else 0

            rankings.append({
                "agent_id": agent.agent_id,
                "agent_type": agent.agent_type.value,
                "accuracy": accuracy,
                "total_predictions": total,
                "cumulative_pnl": perf.get("cumulative_pnl", 0.0),
                "weight": self.agent_weights.get(agent.agent_id, 1.0)
            })

        # Sort by accuracy
        rankings.sort(key=lambda x: x["accuracy"], reverse=True)

        return rankings
