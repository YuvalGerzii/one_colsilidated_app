"""
Advanced opportunity scoring and ranking system.
Evaluates and prioritizes arbitrage opportunities based on multiple factors.
"""
from typing import List, Dict, Tuple
from decimal import Decimal
from datetime import datetime
import numpy as np

from ..models.types import ArbitrageOpportunity, MarketData


class OpportunityScorer:
    """Scores and ranks arbitrage opportunities."""

    def __init__(self, config: dict = None):
        """
        Initialize opportunity scorer.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}

        # Scoring weights
        self.weights = {
            "profitability": Decimal(self.config.get("weight_profitability", "0.30")),
            "confidence": Decimal(self.config.get("weight_confidence", "0.25")),
            "risk": Decimal(self.config.get("weight_risk", "0.20")),
            "execution_quality": Decimal(self.config.get("weight_execution", "0.15")),
            "timing": Decimal(self.config.get("weight_timing", "0.10"))
        }

    def score_opportunity(
        self,
        opportunity: ArbitrageOpportunity,
        market_context: Dict = None
    ) -> Tuple[Decimal, Dict]:
        """
        Calculate comprehensive score for an opportunity.

        Args:
            opportunity: Arbitrage opportunity to score
            market_context: Additional market context

        Returns:
            Tuple of (total_score, score_breakdown)
        """
        scores = {}
        market_context = market_context or {}

        # 1. Profitability Score (0-1)
        profitability_score = self._score_profitability(opportunity)
        scores['profitability'] = float(profitability_score)

        # 2. Confidence Score (already in opportunity)
        confidence_score = opportunity.confidence_score
        scores['confidence'] = float(confidence_score)

        # 3. Risk Score (inverse - lower risk = higher score)
        risk_score = Decimal(1) - opportunity.risk_score
        scores['risk'] = float(risk_score)

        # 4. Execution Quality Score
        execution_score = self._score_execution_quality(opportunity, market_context)
        scores['execution_quality'] = float(execution_score)

        # 5. Timing Score
        timing_score = self._score_timing(opportunity, market_context)
        scores['timing'] = float(timing_score)

        # Calculate weighted total score
        total_score = (
            profitability_score * self.weights['profitability'] +
            confidence_score * self.weights['confidence'] +
            risk_score * self.weights['risk'] +
            execution_score * self.weights['execution_quality'] +
            timing_score * self.weights['timing']
        )

        scores['total_score'] = float(total_score)
        scores['rating'] = self._get_rating(total_score)

        return total_score, scores

    def _score_profitability(self, opportunity: ArbitrageOpportunity) -> Decimal:
        """
        Score opportunity profitability.

        Considers:
        - Expected profit percentage
        - Absolute profit amount
        - Profit-to-risk ratio

        Args:
            opportunity: Opportunity to score

        Returns:
            Profitability score (0-1)
        """
        # Normalize profit percentage (0.1% = 0, 2% = 1)
        profit_pct = opportunity.expected_profit_percentage
        normalized_profit = min(profit_pct / Decimal("2"), Decimal(1))

        # Consider absolute profit (larger profits = better)
        # Normalize using logarithmic scale
        if opportunity.expected_profit > 0:
            log_profit = Decimal(str(np.log10(float(opportunity.expected_profit) + 1)))
            normalized_absolute = min(log_profit / Decimal("3"), Decimal(1))
        else:
            normalized_absolute = Decimal(0)

        # Profit-to-risk ratio
        if opportunity.risk_score > 0:
            profit_risk_ratio = opportunity.expected_profit_percentage / (opportunity.risk_score * 10)
            normalized_ratio = min(profit_risk_ratio / Decimal("2"), Decimal(1))
        else:
            normalized_ratio = Decimal(1)

        # Weighted average
        score = (
            normalized_profit * Decimal("0.5") +
            normalized_absolute * Decimal("0.3") +
            normalized_ratio * Decimal("0.2")
        )

        return min(score, Decimal(1))

    def _score_execution_quality(
        self,
        opportunity: ArbitrageOpportunity,
        market_context: Dict
    ) -> Decimal:
        """
        Score execution quality.

        Considers:
        - Market liquidity
        - Expected slippage
        - Number of execution steps
        - Market conditions

        Args:
            opportunity: Opportunity to score
            market_context: Market context information

        Returns:
            Execution quality score (0-1)
        """
        score = Decimal(0)

        # Liquidity score
        if opportunity.market_data:
            total_liquidity = sum(
                data.bid_volume + data.ask_volume
                for data in opportunity.market_data
            )
            liquidity_score = min(total_liquidity / Decimal(1000), Decimal(1))
            score += liquidity_score * Decimal("0.4")
        else:
            score += Decimal("0.2")  # Neutral if unknown

        # Complexity score (fewer steps = better)
        num_actions = len(opportunity.suggested_actions)
        if num_actions == 1:
            complexity_score = Decimal(1)
        elif num_actions == 2:
            complexity_score = Decimal("0.8")
        elif num_actions == 3:
            complexity_score = Decimal("0.6")
        else:
            complexity_score = Decimal("0.4")

        score += complexity_score * Decimal("0.3")

        # Spread quality (tighter spreads = better execution)
        if opportunity.market_data:
            avg_spread_pct = sum(
                data.spread_percentage
                for data in opportunity.market_data
            ) / len(opportunity.market_data)

            spread_score = max(Decimal(0), Decimal(1) - avg_spread_pct / 2)
            score += spread_score * Decimal("0.3")
        else:
            score += Decimal("0.15")

        return min(score, Decimal(1))

    def _score_timing(
        self,
        opportunity: ArbitrageOpportunity,
        market_context: Dict
    ) -> Decimal:
        """
        Score opportunity timing.

        Considers:
        - Market volatility (moderate = better)
        - Time of day
        - Market trends
        - Opportunity freshness

        Args:
            opportunity: Opportunity to score
            market_context: Market context information

        Returns:
            Timing score (0-1)
        """
        score = Decimal(0)

        # Freshness score (newer = better)
        age_seconds = (datetime.now() - opportunity.timestamp).total_seconds()
        freshness_score = max(Decimal(0), Decimal(1) - Decimal(age_seconds) / 10)
        score += freshness_score * Decimal("0.4")

        # Detection latency score (faster = better)
        if opportunity.detection_latency_ms < 100:
            latency_score = Decimal(1)
        elif opportunity.detection_latency_ms < 500:
            latency_score = Decimal("0.7")
        elif opportunity.detection_latency_ms < 1000:
            latency_score = Decimal("0.5")
        else:
            latency_score = Decimal("0.3")

        score += latency_score * Decimal("0.3")

        # Market condition score (from context)
        if market_context.get("market_conditions"):
            conditions = market_context["market_conditions"]

            # Moderate volatility is best for arbitrage
            volatility = conditions.get("volatility", "moderate")
            if volatility == "moderate":
                volatility_score = Decimal(1)
            elif volatility == "low":
                volatility_score = Decimal("0.7")
            elif volatility == "high":
                volatility_score = Decimal("0.5")
            else:  # extreme
                volatility_score = Decimal("0.3")

            score += volatility_score * Decimal("0.3")
        else:
            score += Decimal("0.15")  # Neutral if unknown

        return min(score, Decimal(1))

    def _get_rating(self, score: Decimal) -> str:
        """Get quality rating from score."""
        if score >= Decimal("0.8"):
            return "excellent"
        elif score >= Decimal("0.6"):
            return "good"
        elif score >= Decimal("0.4"):
            return "fair"
        elif score >= Decimal("0.2"):
            return "poor"
        else:
            return "very_poor"

    def rank_opportunities(
        self,
        opportunities: List[ArbitrageOpportunity],
        market_context: Dict = None
    ) -> List[Tuple[ArbitrageOpportunity, Decimal, Dict]]:
        """
        Rank opportunities by score.

        Args:
            opportunities: List of opportunities to rank
            market_context: Market context information

        Returns:
            List of tuples (opportunity, score, score_breakdown) sorted by score
        """
        scored_opportunities = []

        for opportunity in opportunities:
            score, breakdown = self.score_opportunity(opportunity, market_context)
            scored_opportunities.append((opportunity, score, breakdown))

        # Sort by score (descending)
        scored_opportunities.sort(key=lambda x: x[1], reverse=True)

        return scored_opportunities

    def filter_opportunities(
        self,
        opportunities: List[ArbitrageOpportunity],
        min_score: Decimal = None,
        max_risk: Decimal = None,
        min_profit: Decimal = None,
        market_context: Dict = None
    ) -> List[ArbitrageOpportunity]:
        """
        Filter opportunities based on criteria.

        Args:
            opportunities: List of opportunities
            min_score: Minimum score threshold
            max_risk: Maximum risk score
            min_profit: Minimum profit percentage
            market_context: Market context

        Returns:
            Filtered list of opportunities
        """
        filtered = []

        min_score = min_score or Decimal("0.4")
        max_risk = max_risk or Decimal("0.7")
        min_profit = min_profit or Decimal("0.001")

        for opportunity in opportunities:
            # Check profit threshold
            if opportunity.expected_profit_percentage < min_profit:
                continue

            # Check risk threshold
            if opportunity.risk_score > max_risk:
                continue

            # Check score threshold
            score, _ = self.score_opportunity(opportunity, market_context)
            if score < min_score:
                continue

            filtered.append(opportunity)

        return filtered

    def compare_opportunities(
        self,
        opp1: ArbitrageOpportunity,
        opp2: ArbitrageOpportunity,
        market_context: Dict = None
    ) -> Dict:
        """
        Compare two opportunities.

        Args:
            opp1: First opportunity
            opp2: Second opportunity
            market_context: Market context

        Returns:
            Comparison results
        """
        score1, breakdown1 = self.score_opportunity(opp1, market_context)
        score2, breakdown2 = self.score_opportunity(opp2, market_context)

        return {
            "opportunity1": {
                "id": opp1.opportunity_id,
                "symbol": opp1.symbol,
                "type": opp1.arbitrage_type.value,
                "score": float(score1),
                "breakdown": breakdown1
            },
            "opportunity2": {
                "id": opp2.opportunity_id,
                "symbol": opp2.symbol,
                "type": opp2.arbitrage_type.value,
                "score": float(score2),
                "breakdown": breakdown2
            },
            "winner": "opportunity1" if score1 > score2 else "opportunity2",
            "score_difference": float(abs(score1 - score2)),
            "recommendation": self._generate_comparison_recommendation(
                opp1, opp2, score1, score2
            )
        }

    def _generate_comparison_recommendation(
        self,
        opp1: ArbitrageOpportunity,
        opp2: ArbitrageOpportunity,
        score1: Decimal,
        score2: Decimal
    ) -> str:
        """Generate recommendation from comparison."""
        score_diff = abs(score1 - score2)

        if score_diff < Decimal("0.1"):
            return "Opportunities are similar in quality. Consider executing both if capital allows."
        elif score_diff < Decimal("0.3"):
            winner = opp1 if score1 > score2 else opp2
            return f"Opportunity {winner.opportunity_id} has a moderate advantage. Recommended."
        else:
            winner = opp1 if score1 > score2 else opp2
            return f"Opportunity {winner.opportunity_id} is significantly better. Strongly recommended."

    def generate_opportunity_report(
        self,
        opportunities: List[ArbitrageOpportunity],
        market_context: Dict = None
    ) -> Dict:
        """
        Generate comprehensive report on opportunities.

        Args:
            opportunities: List of opportunities
            market_context: Market context

        Returns:
            Detailed report
        """
        if not opportunities:
            return {
                "total_opportunities": 0,
                "average_score": 0,
                "distribution": {},
                "top_opportunities": []
            }

        # Rank all opportunities
        ranked = self.rank_opportunities(opportunities, market_context)

        # Calculate statistics
        scores = [float(score) for _, score, _ in ranked]
        avg_score = np.mean(scores)
        median_score = np.median(scores)
        std_score = np.std(scores)

        # Distribution by rating
        distribution = {}
        for _, score, breakdown in ranked:
            rating = breakdown['rating']
            distribution[rating] = distribution.get(rating, 0) + 1

        # Distribution by arbitrage type
        type_distribution = {}
        for opp, _, _ in ranked:
            arb_type = opp.arbitrage_type.value
            type_distribution[arb_type] = type_distribution.get(arb_type, 0) + 1

        # Top opportunities
        top_opportunities = []
        for opp, score, breakdown in ranked[:10]:  # Top 10
            top_opportunities.append({
                "id": opp.opportunity_id,
                "symbol": opp.symbol,
                "type": opp.arbitrage_type.value,
                "expected_profit_pct": float(opp.expected_profit_percentage),
                "confidence": float(opp.confidence_score),
                "risk": float(opp.risk_score),
                "score": float(score),
                "rating": breakdown['rating']
            })

        return {
            "total_opportunities": len(opportunities),
            "average_score": float(avg_score),
            "median_score": float(median_score),
            "std_score": float(std_score),
            "rating_distribution": distribution,
            "type_distribution": type_distribution,
            "top_opportunities": top_opportunities,
            "best_opportunity": top_opportunities[0] if top_opportunities else None,
            "timestamp": datetime.now().isoformat()
        }
