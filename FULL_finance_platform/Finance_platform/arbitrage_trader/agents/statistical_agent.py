"""
Statistical arbitrage agent.
"""
from typing import List
from decimal import Decimal

from .base_agent import BaseAgent
from ..algorithms.statistical import StatisticalArbitrageDetector
from ..models.types import (
    ArbitrageOpportunity,
    MarketData,
    ArbitrageType,
    MarketType
)


class StatisticalArbitrageAgent(BaseAgent):
    """Agent specialized in detecting statistical arbitrage opportunities."""

    def __init__(self, agent_id: str = "statistical_agent", config: dict = None):
        """
        Initialize statistical arbitrage agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="StatisticalArbitrageAgent",
            supported_arbitrage_types=[ArbitrageType.STATISTICAL],
            supported_market_types=[
                MarketType.CRYPTO,
                MarketType.STOCKS,
                MarketType.FOREX
            ],
            config=config
        )

        # Initialize detector
        self.detector = StatisticalArbitrageDetector(
            lookback_period=self.config.get("lookback_period", 20),
            z_score_entry_threshold=self.config.get("z_score_entry_threshold", 2.0),
            z_score_exit_threshold=self.config.get("z_score_exit_threshold", 0.5),
            correlation_threshold=self.config.get("correlation_threshold", 0.7)
        )

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(
            f"{self.agent_type} started with lookback period: "
            f"{self.detector.lookback_period}, z-score threshold: "
            f"{self.detector.z_score_entry_threshold}"
        )

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data for statistical arbitrage opportunities.

        Args:
            market_data: List of market data snapshots

        Returns:
            List of detected arbitrage opportunities
        """
        # Detect opportunities using statistical algorithms
        opportunities = self.detector.detect_opportunities(market_data)

        # Filter opportunities based on agent configuration
        filtered_opportunities = []
        for opp in opportunities:
            if self.validate_opportunity(opp):
                filtered_opportunities.append(opp)

        return filtered_opportunities
