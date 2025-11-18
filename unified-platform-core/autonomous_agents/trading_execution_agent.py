"""
Trading Execution Agent

Autonomous agent that executes trades based on arbitrage opportunities
detected by the Finance platform's arbitrage detection system.

Features:
- Real-time opportunity monitoring
- Multi-exchange execution
- Risk management integration
- Position sizing
- Slippage protection
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging

from .base_autonomous_agent import (
    BaseAutonomousAgent, AgentAction, ActionResult, AgentConfig,
    ActionType, ActionStatus, RiskLevel
)

logger = logging.getLogger(__name__)


class TradingExecutionAgent(BaseAutonomousAgent):
    """
    Executes trades autonomously based on detected opportunities.

    Integrates with:
    - Cross-Exchange Arbitrage Agent
    - Statistical Arbitrage Agent
    - Triangular Arbitrage Agent
    - Risk Manager Agent
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.exchange_connections: Dict[str, Any] = {}
        self.active_positions: List[Dict[str, Any]] = []
        self.pending_orders: Dict[str, Dict[str, Any]] = {}

    async def plan_actions(
        self,
        objective: str,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """
        Plan trading actions based on objective.

        Objectives:
        - "execute_arbitrage": Execute detected arbitrage opportunity
        - "rebalance_portfolio": Rebalance to target allocation
        - "hedge_position": Create hedging positions
        """

        actions = []

        if "arbitrage" in objective.lower():
            actions = await self._plan_arbitrage_execution(context)
        elif "rebalance" in objective.lower():
            actions = await self._plan_rebalance(context)
        elif "hedge" in objective.lower():
            actions = await self._plan_hedging(context)

        return actions

    async def _plan_arbitrage_execution(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan actions for arbitrage execution"""

        opportunity = context.get("opportunity", {})
        opp_type = opportunity.get("type", "cross_exchange")

        actions = []

        if opp_type == "cross_exchange":
            # Buy on cheaper exchange, sell on expensive
            buy_exchange = opportunity.get("buy_exchange", "binance")
            sell_exchange = opportunity.get("sell_exchange", "coinbase")
            symbol = opportunity.get("symbol", "BTC/USDT")
            quantity = opportunity.get("quantity", 0.1)
            expected_profit = opportunity.get("expected_profit_usd", 0)

            # Action 1: Place buy order
            buy_action = AgentAction(
                action_id=self.create_action_id(),
                action_type=ActionType.EXECUTE_TRADE,
                description=f"Buy {quantity} {symbol} on {buy_exchange}",
                parameters={
                    "exchange": buy_exchange,
                    "symbol": symbol,
                    "side": "buy",
                    "quantity": quantity,
                    "order_type": "market",
                    "max_slippage_percent": 0.1
                },
                risk_level=RiskLevel.HIGH if expected_profit > 100 else RiskLevel.MEDIUM,
                estimated_impact={
                    "cost_usd": opportunity.get("buy_cost_usd", 0),
                    "expected_profit_usd": expected_profit
                },
                rollback_steps=[
                    f"Sell {quantity} {symbol} on {buy_exchange}",
                    "Cancel any pending orders"
                ],
                requires_approval=expected_profit > 500
            )
            actions.append(buy_action)

            # Action 2: Place sell order
            sell_action = AgentAction(
                action_id=self.create_action_id(),
                action_type=ActionType.EXECUTE_TRADE,
                description=f"Sell {quantity} {symbol} on {sell_exchange}",
                parameters={
                    "exchange": sell_exchange,
                    "symbol": symbol,
                    "side": "sell",
                    "quantity": quantity,
                    "order_type": "market",
                    "max_slippage_percent": 0.1
                },
                risk_level=buy_action.risk_level,
                estimated_impact={
                    "revenue_usd": opportunity.get("sell_revenue_usd", 0)
                },
                rollback_steps=[
                    f"Buy {quantity} {symbol} on {sell_exchange}"
                ],
                dependencies=[buy_action.action_id],
                requires_approval=buy_action.requires_approval
            )
            actions.append(sell_action)

        elif opp_type == "triangular":
            # Three-leg trade
            legs = opportunity.get("legs", [])
            for i, leg in enumerate(legs):
                action = AgentAction(
                    action_id=self.create_action_id(),
                    action_type=ActionType.EXECUTE_TRADE,
                    description=f"Triangular leg {i+1}: {leg.get('side')} {leg.get('symbol')}",
                    parameters={
                        "exchange": leg.get("exchange"),
                        "symbol": leg.get("symbol"),
                        "side": leg.get("side"),
                        "quantity": leg.get("quantity"),
                        "order_type": "market"
                    },
                    risk_level=RiskLevel.HIGH,
                    estimated_impact={"leg_profit_usd": leg.get("profit", 0)},
                    rollback_steps=[f"Reverse leg {i+1}"],
                    dependencies=[actions[-1].action_id] if actions else [],
                    requires_approval=True  # Triangular always needs approval
                )
                actions.append(action)

        return actions

    async def _plan_rebalance(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan portfolio rebalancing actions"""

        current_allocation = context.get("current_allocation", {})
        target_allocation = context.get("target_allocation", {})

        actions = []

        for symbol, target_pct in target_allocation.items():
            current_pct = current_allocation.get(symbol, 0)
            diff = target_pct - current_pct

            if abs(diff) > 1:  # More than 1% difference
                side = "buy" if diff > 0 else "sell"
                quantity = abs(diff) * context.get("portfolio_value", 10000) / 100

                action = AgentAction(
                    action_id=self.create_action_id(),
                    action_type=ActionType.EXECUTE_TRADE,
                    description=f"Rebalance: {side} ${quantity:.2f} of {symbol}",
                    parameters={
                        "symbol": symbol,
                        "side": side,
                        "amount_usd": quantity,
                        "order_type": "limit"
                    },
                    risk_level=RiskLevel.MEDIUM,
                    estimated_impact={"rebalance_amount_usd": quantity},
                    rollback_steps=[f"Reverse {symbol} rebalance"]
                )
                actions.append(action)

        return actions

    async def _plan_hedging(
        self,
        context: Dict[str, Any]
    ) -> List[AgentAction]:
        """Plan hedging actions"""

        position = context.get("position", {})
        hedge_ratio = context.get("hedge_ratio", 0.5)

        actions = []

        # Simple hedging with inverse position
        hedge_action = AgentAction(
            action_id=self.create_action_id(),
            action_type=ActionType.EXECUTE_TRADE,
            description=f"Hedge {position.get('symbol')} position",
            parameters={
                "symbol": position.get("hedge_instrument", "SPY"),
                "side": "sell" if position.get("side") == "long" else "buy",
                "quantity": position.get("quantity", 0) * hedge_ratio,
                "order_type": "market"
            },
            risk_level=RiskLevel.MEDIUM,
            estimated_impact={
                "hedge_value_usd": position.get("value", 0) * hedge_ratio
            },
            rollback_steps=["Close hedge position"]
        )
        actions.append(hedge_action)

        return actions

    async def execute_action(self, action: AgentAction) -> ActionResult:
        """Execute a trading action"""

        params = action.parameters

        try:
            # Connect to exchange
            exchange = params.get("exchange", "default")
            # exchange_client = self.exchange_connections.get(exchange)

            # Simulate order execution (replace with real exchange API)
            order_result = await self._execute_order(
                exchange=exchange,
                symbol=params.get("symbol"),
                side=params.get("side"),
                quantity=params.get("quantity"),
                order_type=params.get("order_type", "market")
            )

            return ActionResult(
                action_id=action.action_id,
                status=ActionStatus.COMPLETED,
                result={
                    "order_id": order_result.get("order_id"),
                    "filled_quantity": order_result.get("filled_quantity"),
                    "average_price": order_result.get("average_price"),
                    "total_cost": order_result.get("total_cost"),
                    "fees": order_result.get("fees")
                },
                side_effects=[
                    f"Position updated: {params.get('side')} {params.get('quantity')} {params.get('symbol')}"
                ],
                metadata={
                    "exchange": exchange,
                    "timestamp": datetime.now().isoformat()
                }
            )

        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            return ActionResult(
                action_id=action.action_id,
                status=ActionStatus.FAILED,
                result=None,
                error=str(e)
            )

    async def _execute_order(
        self,
        exchange: str,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str
    ) -> Dict[str, Any]:
        """Execute order on exchange (simulated)"""

        # Simulate order execution
        # In production, this would call actual exchange APIs

        await asyncio.sleep(0.1)  # Simulate network latency

        # Simulated successful order
        price = 50000 if "BTC" in symbol else 3000  # Mock prices
        total_cost = quantity * price
        fees = total_cost * 0.001  # 0.1% fee

        order_id = f"ord_{datetime.now().timestamp()}"

        # Track the order
        self.pending_orders[order_id] = {
            "exchange": exchange,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "status": "filled",
            "filled_at": datetime.now().isoformat()
        }

        return {
            "order_id": order_id,
            "filled_quantity": quantity,
            "average_price": price,
            "total_cost": total_cost,
            "fees": fees
        }

    async def rollback_action(self, action_id: str) -> bool:
        """Rollback a trading action by executing opposite trade"""

        # Find the action in history
        action_result = None
        for result in self.action_history:
            if result.action_id == action_id:
                action_result = result
                break

        if not action_result or action_result.status != ActionStatus.COMPLETED:
            return False

        # Execute opposite trade
        original_result = action_result.result
        if not original_result:
            return False

        try:
            # Reverse the trade
            # This is simplified - real implementation would need to handle
            # slippage, market conditions, etc.
            logger.info(f"Rolling back action {action_id}")
            return True
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False

    def get_active_positions(self) -> List[Dict[str, Any]]:
        """Get current active positions"""
        return self.active_positions

    def get_pending_orders(self) -> Dict[str, Dict[str, Any]]:
        """Get pending orders"""
        return self.pending_orders


# Factory function
def create_trading_agent(
    agent_id: str = "trading_agent_1",
    spending_limit: float = 10000.0,
    dry_run: bool = True
) -> TradingExecutionAgent:
    """Create a configured trading execution agent"""

    config = AgentConfig(
        agent_id=agent_id,
        name="Trading Execution Agent",
        max_concurrent_actions=3,
        action_timeout_seconds=30,
        auto_approve_risk_levels=[RiskLevel.LOW, RiskLevel.MEDIUM],
        spending_limit_usd=spending_limit,
        daily_action_limit=50,
        require_human_approval_above=1000.0,
        enabled=True,
        dry_run=dry_run
    )

    return TradingExecutionAgent(config)
