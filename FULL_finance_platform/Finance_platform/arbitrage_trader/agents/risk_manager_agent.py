"""
Risk management agent for monitoring and controlling risk.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta

from .base_agent import BaseAgent
from ..models.types import (
    ArbitrageOpportunity,
    MarketData,
    ArbitrageType,
    MarketType,
    Trade
)


class RiskManagerAgent(BaseAgent):
    """Agent specialized in risk management and position monitoring."""

    def __init__(self, agent_id: str = "risk_manager_agent", config: dict = None):
        """
        Initialize risk manager agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="RiskManagerAgent",
            supported_arbitrage_types=list(ArbitrageType),  # Monitors all types
            supported_market_types=list(MarketType),  # Monitors all markets
            config=config
        )

        # Risk limits
        self.max_position_size = Decimal(self.config.get("max_position_size", "10000"))
        self.max_daily_loss = Decimal(self.config.get("max_daily_loss", "1000"))
        self.max_total_exposure = Decimal(self.config.get("max_total_exposure", "50000"))
        self.max_risk_score = Decimal(self.config.get("max_risk_score", "0.7"))

        # Current state
        self.current_exposure = Decimal(0)
        self.daily_pnl = Decimal(0)
        self.daily_loss = Decimal(0)
        self.positions: Dict[str, Dict] = {}

        # Daily reset
        self.last_reset_date = datetime.now().date()

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(
            f"{self.agent_type} started with limits: "
            f"max_position={self.max_position_size}, "
            f"max_daily_loss={self.max_daily_loss}, "
            f"max_exposure={self.max_total_exposure}"
        )

        # Start daily reset task
        asyncio.create_task(self._daily_reset_task())

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Risk manager doesn't detect opportunities.

        Args:
            market_data: List of market data snapshots

        Returns:
            Empty list
        """
        # Monitor market conditions for risk
        await self._monitor_market_conditions(market_data)
        return []

    def should_execute_opportunity(
        self,
        opportunity: ArbitrageOpportunity
    ) -> tuple[bool, str]:
        """
        Determine if an opportunity should be executed based on risk limits.

        Args:
            opportunity: Opportunity to evaluate

        Returns:
            Tuple of (should_execute, reason)
        """
        # Check daily loss limit
        if self.daily_loss >= self.max_daily_loss:
            return False, f"Daily loss limit reached: {self.daily_loss}/{self.max_daily_loss}"

        # Check risk score
        if opportunity.risk_score > self.max_risk_score:
            return False, f"Risk score too high: {opportunity.risk_score} > {self.max_risk_score}"

        # Check total exposure
        estimated_exposure = self._estimate_opportunity_exposure(opportunity)
        if self.current_exposure + estimated_exposure > self.max_total_exposure:
            return (
                False,
                f"Exposure limit would be exceeded: "
                f"{self.current_exposure + estimated_exposure}/{self.max_total_exposure}"
            )

        # Check position size
        if estimated_exposure > self.max_position_size:
            return False, f"Position size too large: {estimated_exposure} > {self.max_position_size}"

        return True, "Approved"

    def _estimate_opportunity_exposure(
        self,
        opportunity: ArbitrageOpportunity
    ) -> Decimal:
        """Estimate total exposure for an opportunity."""
        total_exposure = Decimal(0)

        for action in opportunity.suggested_actions:
            exposure = action.quantity * action.price
            total_exposure += exposure

        return total_exposure

    def update_position(
        self,
        opportunity_id: str,
        trades: List[Trade]
    ):
        """
        Update positions and exposure based on executed trades.

        Args:
            opportunity_id: Opportunity ID
            trades: Executed trades
        """
        # Calculate position value
        position_value = Decimal(0)
        pnl = Decimal(0)

        for trade in trades:
            trade_value = trade.quantity * trade.price

            if trade.side.value == "buy":
                position_value += trade_value
            else:
                position_value -= trade_value
                pnl += trade_value

            pnl -= trade.fees

        # Update exposure
        self.current_exposure += abs(position_value)

        # Update daily PnL
        self.daily_pnl += pnl
        if pnl < 0:
            self.daily_loss += abs(pnl)

        # Store position
        self.positions[opportunity_id] = {
            "value": position_value,
            "pnl": pnl,
            "trades": trades,
            "timestamp": datetime.now()
        }

        self.logger.info(
            f"Position updated for {opportunity_id}: "
            f"PnL={pnl:.4f}, Exposure={self.current_exposure:.2f}, "
            f"Daily Loss={self.daily_loss:.2f}"
        )

    def close_position(self, opportunity_id: str):
        """
        Close a position and update exposure.

        Args:
            opportunity_id: Opportunity ID to close
        """
        if opportunity_id in self.positions:
            position = self.positions[opportunity_id]
            self.current_exposure -= abs(position["value"])
            del self.positions[opportunity_id]

            self.logger.info(
                f"Closed position {opportunity_id}, "
                f"remaining exposure: {self.current_exposure:.2f}"
            )

    async def _monitor_market_conditions(self, market_data: List[MarketData]):
        """Monitor market conditions for systemic risk."""
        # Check for unusual volatility
        # Check for liquidity issues
        # Check for correlation changes
        # This is a simplified version
        pass

    async def _daily_reset_task(self):
        """Task to reset daily counters."""
        while self.is_active:
            current_date = datetime.now().date()

            if current_date > self.last_reset_date:
                self.logger.info(
                    f"Daily reset - Previous day PnL: {self.daily_pnl:.2f}, "
                    f"Loss: {self.daily_loss:.2f}"
                )

                self.daily_pnl = Decimal(0)
                self.daily_loss = Decimal(0)
                self.last_reset_date = current_date

            # Check every hour
            await asyncio.sleep(3600)

    def get_risk_report(self) -> Dict:
        """Get current risk metrics."""
        return {
            "current_exposure": float(self.current_exposure),
            "max_total_exposure": float(self.max_total_exposure),
            "exposure_utilization": float(
                self.current_exposure / self.max_total_exposure * 100
                if self.max_total_exposure > 0 else 0
            ),
            "daily_pnl": float(self.daily_pnl),
            "daily_loss": float(self.daily_loss),
            "max_daily_loss": float(self.max_daily_loss),
            "loss_limit_utilization": float(
                self.daily_loss / self.max_daily_loss * 100
                if self.max_daily_loss > 0 else 0
            ),
            "active_positions": len(self.positions),
            "positions": {
                opp_id: {
                    "value": float(pos["value"]),
                    "pnl": float(pos["pnl"]),
                    "age_seconds": (datetime.now() - pos["timestamp"]).total_seconds()
                }
                for opp_id, pos in self.positions.items()
            }
        }
