"""
Triangular arbitrage agent.
"""
from typing import List
from decimal import Decimal

from .base_agent import BaseAgent
from ..algorithms.triangular import TriangularArbitrageDetector
from ..models.types import (
    ArbitrageOpportunity,
    MarketData,
    ArbitrageType,
    MarketType
)


class TriangularArbitrageAgent(BaseAgent):
    """Agent specialized in detecting triangular arbitrage opportunities."""

    def __init__(self, agent_id: str = "triangular_agent", config: dict = None):
        """
        Initialize triangular arbitrage agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="TriangularArbitrageAgent",
            supported_arbitrage_types=[ArbitrageType.TRIANGULAR],
            supported_market_types=[
                MarketType.CRYPTO,
                MarketType.FOREX
            ],
            config=config
        )

        # Initialize detector
        min_profit = Decimal(self.config.get("min_profit_threshold", "0.001"))
        self.detector = TriangularArbitrageDetector(min_profit_threshold=min_profit)

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(
            f"{self.agent_type} started with min profit threshold: "
            f"{self.detector.min_profit_threshold}"
        )

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data for triangular arbitrage opportunities.

        Args:
            market_data: List of market data snapshots

        Returns:
            List of detected arbitrage opportunities
        """
        # Detect opportunities using triangular arbitrage algorithm
        opportunities = self.detector.detect_opportunities(market_data)

        # Filter opportunities based on agent configuration
        filtered_opportunities = []
        for opp in opportunities:
            if self.validate_opportunity(opp):
                filtered_opportunities.append(opp)

        return filtered_opportunities
