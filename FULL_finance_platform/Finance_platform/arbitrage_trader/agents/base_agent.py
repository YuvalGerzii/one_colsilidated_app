"""
Base agent class for the multi-agent arbitrage system.
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
import asyncio

from ..models.types import (
    ArbitrageOpportunity,
    MarketData,
    AgentStatus,
    ArbitrageType,
    MarketType
)


class BaseAgent(ABC):
    """Base class for all arbitrage detection agents."""

    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        supported_arbitrage_types: List[ArbitrageType],
        supported_market_types: List[MarketType],
        config: dict = None
    ):
        """
        Initialize base agent.

        Args:
            agent_id: Unique identifier for the agent
            agent_type: Type of the agent
            supported_arbitrage_types: Types of arbitrage this agent can detect
            supported_market_types: Types of markets this agent monitors
            config: Agent configuration
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.supported_arbitrage_types = supported_arbitrage_types
        self.supported_market_types = supported_market_types
        self.config = config or {}

        # State
        self.is_active = False
        self.opportunities_detected = 0
        self.trades_executed = 0
        self.total_profit = Decimal(0)
        self.total_loss = Decimal(0)
        self.last_activity = datetime.now()

        # Logger
        self.logger = logging.getLogger(f"{__name__}.{agent_type}.{agent_id}")

    async def start(self):
        """Start the agent."""
        self.is_active = True
        self.logger.info(f"Agent {self.agent_id} started")
        await self.on_start()

    async def stop(self):
        """Stop the agent."""
        self.is_active = False
        self.logger.info(f"Agent {self.agent_id} stopped")
        await self.on_stop()

    @abstractmethod
    async def on_start(self):
        """Called when agent starts. Override in subclasses."""
        pass

    @abstractmethod
    async def on_stop(self):
        """Called when agent stops. Override in subclasses."""
        pass

    @abstractmethod
    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Analyze market data and detect arbitrage opportunities.

        Args:
            market_data: List of market data snapshots

        Returns:
            List of detected arbitrage opportunities
        """
        pass

    async def process_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Process market data and update agent state.

        Args:
            market_data: List of market data snapshots

        Returns:
            List of detected arbitrage opportunities
        """
        if not self.is_active:
            return []

        start_time = datetime.now()

        # Filter market data for supported market types
        filtered_data = [
            data for data in market_data
            if data.market_type in self.supported_market_types
        ]

        if not filtered_data:
            return []

        # Analyze market data
        opportunities = await self.analyze_market_data(filtered_data)

        # Update agent state
        self.opportunities_detected += len(opportunities)
        self.last_activity = datetime.now()

        # Log detection latency
        detection_latency = (datetime.now() - start_time).total_seconds() * 1000

        for opp in opportunities:
            opp.detection_latency_ms = detection_latency
            self.logger.info(
                f"Detected {opp.arbitrage_type.value} opportunity: "
                f"{opp.symbol} - Expected profit: {opp.expected_profit_percentage:.4f}% "
                f"(Confidence: {opp.confidence_score:.2f}, Risk: {opp.risk_score:.2f})"
            )

        return opportunities

    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        success_rate = Decimal(0)
        if self.trades_executed > 0:
            successful_trades = self.trades_executed - (
                self.total_loss / (self.total_profit + self.total_loss)
                if (self.total_profit + self.total_loss) > 0 else 0
            )
            success_rate = Decimal(successful_trades) / Decimal(self.trades_executed)

        return AgentStatus(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            is_active=self.is_active,
            opportunities_detected=self.opportunities_detected,
            trades_executed=self.trades_executed,
            total_profit=self.total_profit,
            total_loss=self.total_loss,
            success_rate=success_rate,
            last_activity=self.last_activity,
            metadata={
                "supported_arbitrage_types": [t.value for t in self.supported_arbitrage_types],
                "supported_market_types": [t.value for t in self.supported_market_types]
            }
        )

    def update_trade_result(self, profit: Decimal):
        """
        Update agent with trade result.

        Args:
            profit: Profit/loss from the trade (negative for loss)
        """
        self.trades_executed += 1
        if profit >= 0:
            self.total_profit += profit
        else:
            self.total_loss += abs(profit)

    def validate_opportunity(
        self,
        opportunity: ArbitrageOpportunity,
        min_profit_threshold: Optional[Decimal] = None,
        min_confidence: Optional[Decimal] = None,
        max_risk: Optional[Decimal] = None
    ) -> bool:
        """
        Validate if opportunity meets thresholds.

        Args:
            opportunity: Opportunity to validate
            min_profit_threshold: Minimum profit percentage threshold
            min_confidence: Minimum confidence score
            max_risk: Maximum acceptable risk score

        Returns:
            True if opportunity is valid
        """
        min_profit_threshold = min_profit_threshold or self.config.get(
            "min_profit_threshold", Decimal("0.001")
        )
        min_confidence = min_confidence or self.config.get(
            "min_confidence", Decimal("0.7")
        )
        max_risk = max_risk or self.config.get(
            "max_risk", Decimal("0.5")
        )

        return (
            opportunity.expected_profit_percentage >= min_profit_threshold and
            opportunity.confidence_score >= min_confidence and
            opportunity.risk_score <= max_risk
        )
