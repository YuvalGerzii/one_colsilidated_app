"""
Trade execution service for executing arbitrage trades.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal
import uuid

from ..models.types import (
    TradingAction,
    Trade,
    OrderStatus,
    ArbitrageOpportunity
)


class ExecutionService:
    """Service for executing trades on exchanges."""

    def __init__(self, config: dict = None):
        """
        Initialize execution service.

        Args:
            config: Service configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Trade history
        self.trades: Dict[str, Trade] = {}

        # Active orders
        self.active_orders: Dict[str, Trade] = {}

        # Performance tracking
        self.total_profit = Decimal(0)
        self.total_loss = Decimal(0)
        self.successful_trades = 0
        self.failed_trades = 0

        self.is_running = False

        # Exchange connections (simulated)
        self.exchange_connections: Dict[str, bool] = {}

    async def start(self):
        """Start the execution service."""
        self.is_running = True
        self.logger.info("Execution service started")

        # Connect to exchanges
        await self._connect_exchanges()

    async def stop(self):
        """Stop the execution service."""
        self.is_running = False
        self.logger.info("Execution service stopped")

        # Disconnect from exchanges
        await self._disconnect_exchanges()

    async def _connect_exchanges(self):
        """Connect to configured exchanges."""
        exchanges = self.config.get("exchanges", [])

        for exchange in exchanges:
            try:
                # In production, this would establish real connections
                # For now, simulate successful connection
                self.exchange_connections[exchange] = True
                self.logger.info(f"Connected to exchange: {exchange}")

            except Exception as e:
                self.logger.error(f"Failed to connect to {exchange}: {e}")

    async def _disconnect_exchanges(self):
        """Disconnect from exchanges."""
        for exchange in list(self.exchange_connections.keys()):
            self.exchange_connections[exchange] = False
            self.logger.info(f"Disconnected from exchange: {exchange}")

    async def execute_opportunity(
        self,
        opportunity: ArbitrageOpportunity
    ) -> List[Trade]:
        """
        Execute an arbitrage opportunity.

        Args:
            opportunity: Arbitrage opportunity to execute

        Returns:
            List of executed trades
        """
        if not self.is_running:
            self.logger.warning("Execution service not running")
            return []

        self.logger.info(
            f"Executing opportunity {opportunity.opportunity_id}: "
            f"{opportunity.arbitrage_type.value} - {opportunity.symbol}"
        )

        # Execute all actions in the opportunity
        trades = []

        # Sort actions by priority
        sorted_actions = sorted(
            opportunity.suggested_actions,
            key=lambda x: x.priority
        )

        for action in sorted_actions:
            trade = await self._execute_action(action, opportunity.opportunity_id)
            if trade:
                trades.append(trade)
            else:
                # If any action fails, we may need to reverse previous trades
                self.logger.error(
                    f"Failed to execute action {action.action_id}, "
                    f"may need to reverse previous trades"
                )
                # In production, implement proper rollback logic
                break

        # Calculate total profit/loss
        if trades:
            total_profit = self._calculate_profit(trades, opportunity)
            if total_profit >= 0:
                self.total_profit += total_profit
                self.successful_trades += 1
            else:
                self.total_loss += abs(total_profit)
                self.failed_trades += 1

            self.logger.info(
                f"Opportunity {opportunity.opportunity_id} completed: "
                f"Profit: {total_profit:.4f}"
            )

        return trades

    async def _execute_action(
        self,
        action: TradingAction,
        opportunity_id: str
    ) -> Optional[Trade]:
        """
        Execute a single trading action.

        Args:
            action: Trading action to execute
            opportunity_id: Associated opportunity ID

        Returns:
            Trade if successful, None otherwise
        """
        start_time = datetime.now()

        try:
            # Check exchange connection
            if not self.exchange_connections.get(action.exchange, False):
                self.logger.error(f"Not connected to exchange: {action.exchange}")
                return None

            # In production, this would:
            # 1. Place order on exchange via API
            # 2. Monitor order status
            # 3. Handle partial fills
            # 4. Handle order rejections

            # For now, simulate order execution
            await asyncio.sleep(0.1)  # Simulate network latency

            # Simulate order filling
            execution_price = action.price
            filled_quantity = action.quantity

            # Simulate slippage
            if action.order_type == "market":
                slippage = Decimal(str(0.001))  # 0.1% slippage
                if action.side.value == "buy":
                    execution_price = execution_price * (Decimal(1) + slippage)
                else:
                    execution_price = execution_price * (Decimal(1) - slippage)

            # Calculate fees (typical 0.1%)
            fee_rate = Decimal(self.config.get("fee_rate", "0.001"))
            fees = filled_quantity * execution_price * fee_rate

            execution_latency = (datetime.now() - start_time).total_seconds() * 1000

            trade = Trade(
                trade_id=str(uuid.uuid4()),
                opportunity_id=opportunity_id,
                action_id=action.action_id,
                exchange=action.exchange,
                symbol=action.symbol,
                side=action.side,
                quantity=filled_quantity,
                price=execution_price,
                status=OrderStatus.FILLED,
                timestamp=datetime.now(),
                execution_latency_ms=execution_latency,
                fees=fees,
                metadata={
                    "order_type": action.order_type,
                    "original_price": float(action.price),
                    "slippage": float(execution_price - action.price) if action.order_type == "market" else 0
                }
            )

            self.trades[trade.trade_id] = trade

            self.logger.info(
                f"Executed {action.side.value} {filled_quantity} {action.symbol} "
                f"on {action.exchange} at {execution_price} "
                f"(latency: {execution_latency:.2f}ms)"
            )

            return trade

        except Exception as e:
            self.logger.error(
                f"Error executing action {action.action_id}: {e}",
                exc_info=True
            )
            return None

    def _calculate_profit(
        self,
        trades: List[Trade],
        opportunity: ArbitrageOpportunity
    ) -> Decimal:
        """
        Calculate profit from executed trades.

        Args:
            trades: List of executed trades
            opportunity: Original opportunity

        Returns:
            Profit (or loss if negative)
        """
        # Simplified profit calculation
        # In production, this would be more sophisticated based on arbitrage type

        total_revenue = Decimal(0)
        total_cost = Decimal(0)
        total_fees = Decimal(0)

        for trade in trades:
            trade_value = trade.quantity * trade.price

            if trade.side.value == "buy":
                total_cost += trade_value
            else:
                total_revenue += trade_value

            total_fees += trade.fees

        profit = total_revenue - total_cost - total_fees

        return profit

    def get_performance_metrics(self) -> Dict:
        """Get execution performance metrics."""
        total_trades = self.successful_trades + self.failed_trades
        success_rate = (
            self.successful_trades / total_trades
            if total_trades > 0 else 0
        )

        net_profit = self.total_profit - self.total_loss

        return {
            "total_trades": total_trades,
            "successful_trades": self.successful_trades,
            "failed_trades": self.failed_trades,
            "success_rate": float(success_rate),
            "total_profit": float(self.total_profit),
            "total_loss": float(self.total_loss),
            "net_profit": float(net_profit),
            "active_orders": len(self.active_orders)
        }

    async def cancel_order(self, trade_id: str) -> bool:
        """
        Cancel an active order.

        Args:
            trade_id: Trade ID to cancel

        Returns:
            True if successful
        """
        if trade_id in self.active_orders:
            # In production, would cancel on exchange
            trade = self.active_orders[trade_id]
            trade.status = OrderStatus.CANCELLED
            del self.active_orders[trade_id]
            self.logger.info(f"Cancelled order {trade_id}")
            return True

        return False
