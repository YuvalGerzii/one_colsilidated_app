"""
Cross-exchange arbitrage agent.
"""
from typing import List
from decimal import Decimal

from .base_agent import BaseAgent
from ..algorithms.cross_exchange import CrossExchangeDetector
from ..models.types import (
    ArbitrageOpportunity,
    MarketData,
    ArbitrageType,
    MarketType
)


class CrossExchangeAgent(BaseAgent):
    """Agent specialized in detecting cross-exchange arbitrage opportunities."""

    def __init__(self, agent_id: str = "cross_exchange_agent", config: dict = None):
        """
        Initialize cross-exchange agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="CrossExchangeAgent",
            supported_arbitrage_types=[ArbitrageType.CROSS_EXCHANGE],
            supported_market_types=[
                MarketType.CRYPTO,
                MarketType.FOREX,
                MarketType.STOCKS
            ],
            config=config
        )

        # Initialize detector
        min_spread = Decimal(self.config.get("min_spread_threshold", "0.001"))
        self.detector = CrossExchangeDetector(min_spread_threshold=min_spread)

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(
            f"{self.agent_type} started with min spread threshold: "
            f"{self.detector.min_spread_threshold}"
        )

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data for cross-exchange arbitrage opportunities.

        Args:
            market_data: List of market data snapshots

        Returns:
            List of detected arbitrage opportunities
        """
        # Detect opportunities using the cross-exchange algorithm
        opportunities = self.detector.detect_opportunities(market_data)

        # Filter opportunities based on agent configuration
        filtered_opportunities = []
        for opp in opportunities:
            if self.validate_opportunity(opp):
                filtered_opportunities.append(opp)

        return filtered_opportunities
