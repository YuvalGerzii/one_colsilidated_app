"""
Portfolio Management Agent for position tracking, optimization, and capital allocation.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

from .base_agent import BaseAgent
from ..models.types import (
    MarketData,
    ArbitrageOpportunity,
    Trade,
    MarketType,
    ArbitrageType
)


class Position:
    """Represents a trading position."""

    def __init__(
        self,
        symbol: str,
        exchange: str,
        quantity: Decimal,
        entry_price: Decimal,
        entry_time: datetime,
        position_id: str = None
    ):
        """Initialize position."""
        self.position_id = position_id or f"{symbol}_{exchange}_{entry_time.timestamp()}"
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.current_price = entry_price
        self.unrealized_pnl = Decimal(0)
        self.realized_pnl = Decimal(0)

    def update_price(self, current_price: Decimal):
        """Update current price and unrealized P&L."""
        self.current_price = current_price
        self.unrealized_pnl = (current_price - self.entry_price) * self.quantity

    def close(self, exit_price: Decimal) -> Decimal:
        """Close position and return realized P&L."""
        self.realized_pnl = (exit_price - self.entry_price) * self.quantity
        return self.realized_pnl

    @property
    def market_value(self) -> Decimal:
        """Current market value of position."""
        return self.current_price * self.quantity

    @property
    def cost_basis(self) -> Decimal:
        """Cost basis of position."""
        return self.entry_price * self.quantity

    @property
    def pnl_percentage(self) -> Decimal:
        """P&L as percentage of cost basis."""
        if self.cost_basis == 0:
            return Decimal(0)
        return (self.unrealized_pnl / self.cost_basis) * Decimal(100)


class Portfolio:
    """Portfolio container."""

    def __init__(self, initial_capital: Decimal):
        """Initialize portfolio."""
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.closed_positions: List[Position] = []
        self.trade_history: List[Trade] = []

    @property
    def total_value(self) -> Decimal:
        """Total portfolio value (cash + positions)."""
        positions_value = sum(pos.market_value for pos in self.positions.values())
        return self.cash + positions_value

    @property
    def total_pnl(self) -> Decimal:
        """Total P&L (realized + unrealized)."""
        unrealized = sum(pos.unrealized_pnl for pos in self.positions.values())
        realized = sum(pos.realized_pnl for pos in self.closed_positions)
        return unrealized + realized

    @property
    def total_return(self) -> Decimal:
        """Total return percentage."""
        if self.initial_capital == 0:
            return Decimal(0)
        return (self.total_pnl / self.initial_capital) * Decimal(100)

    @property
    def leverage(self) -> Decimal:
        """Portfolio leverage ratio."""
        if self.total_value == 0:
            return Decimal(0)
        gross_exposure = sum(pos.market_value for pos in self.positions.values())
        return gross_exposure / self.total_value


class PortfolioManagerAgent(BaseAgent):
    """Agent for portfolio management and optimization."""

    def __init__(self, agent_id: str = "portfolio_manager", config: dict = None):
        """
        Initialize portfolio manager agent.

        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        super().__init__(
            agent_id=agent_id,
            agent_type="PortfolioManagerAgent",
            supported_arbitrage_types=list(ArbitrageType),
            supported_market_types=list(MarketType),
            config=config
        )

        # Initialize portfolio
        initial_capital = Decimal(
            str(config.get("initial_capital", 100000)) if config else "100000"
        )
        self.portfolio = Portfolio(initial_capital)

        # Position limits
        self.max_position_size = Decimal(
            str(config.get("max_position_size", 10000)) if config else "10000"
        )
        self.max_positions = config.get("max_positions", 20) if config else 20
        self.max_leverage = Decimal(
            str(config.get("max_leverage", 2.0)) if config else "2.0"
        )

        # Diversification settings
        self.max_concentration = Decimal(
            str(config.get("max_concentration", 0.2)) if config else "0.2"
        )  # 20% per position

        # Rebalancing
        self.rebalance_threshold = Decimal(
            str(config.get("rebalance_threshold", 0.05)) if config else "0.05"
        )  # 5%

        # Performance tracking
        self.performance_history: List[Dict] = []
        self.daily_returns: List[Decimal] = []

    async def on_start(self):
        """Called when agent starts."""
        self.logger.info(f"{self.agent_type} started - managing portfolio")
        self.logger.info(f"  Initial Capital: ${float(self.portfolio.initial_capital):,.2f}")
        self.logger.info(f"  Max Positions: {self.max_positions}")

        # Start monitoring task
        asyncio.create_task(self._monitor_portfolio())

    async def on_stop(self):
        """Called when agent stops."""
        self.logger.info(f"{self.agent_type} stopped")

    async def analyze_market_data(
        self,
        market_data: List[MarketData]
    ) -> List[ArbitrageOpportunity]:
        """
        Update positions with current market data.

        Args:
            market_data: List of market data snapshots

        Returns:
            Empty list (portfolio manager doesn't detect opportunities)
        """
        # Update position prices
        for data in market_data:
            key = f"{data.symbol}_{data.exchange}"
            if key in self.portfolio.positions:
                self.portfolio.positions[key].update_price(data.mid_price)

        return []

    async def evaluate_opportunity(
        self,
        opportunity: ArbitrageOpportunity
    ) -> Dict:
        """
        Evaluate if opportunity fits portfolio constraints.

        Args:
            opportunity: Opportunity to evaluate

        Returns:
            Evaluation results
        """
        evaluation = {
            "approved": False,
            "reasons": [],
            "suggested_size": Decimal(0),
            "allocation_percentage": Decimal(0)
        }

        # Check number of positions
        if len(self.portfolio.positions) >= self.max_positions:
            evaluation["reasons"].append("Max positions limit reached")
            return evaluation

        # Check leverage
        if self.portfolio.leverage >= self.max_leverage:
            evaluation["reasons"].append("Max leverage limit reached")
            return evaluation

        # Calculate suggested position size
        available_capital = self.portfolio.cash
        max_allocation = self.portfolio.total_value * self.max_concentration

        suggested_size = min(
            available_capital * Decimal("0.1"),  # 10% of cash per trade
            max_allocation,
            self.max_position_size
        )

        if suggested_size < Decimal(100):
            evaluation["reasons"].append("Insufficient capital")
            return evaluation

        # Check diversification
        symbol_exposure = self._get_symbol_exposure(opportunity.symbol)
        if symbol_exposure + suggested_size > max_allocation:
            evaluation["reasons"].append("Concentration limit exceeded")
            return evaluation

        # Approved
        evaluation["approved"] = True
        evaluation["suggested_size"] = suggested_size
        evaluation["allocation_percentage"] = (
            suggested_size / self.portfolio.total_value * Decimal(100)
        )
        evaluation["reasons"].append("Approved within risk limits")

        return evaluation

    def _get_symbol_exposure(self, symbol: str) -> Decimal:
        """Get current exposure to a symbol."""
        exposure = Decimal(0)
        for pos in self.portfolio.positions.values():
            if pos.symbol == symbol:
                exposure += pos.market_value
        return exposure

    async def add_trade(self, trade: Trade, opportunity_id: str = None):
        """
        Add executed trade to portfolio.

        Args:
            trade: Executed trade
            opportunity_id: Associated opportunity ID
        """
        self.portfolio.trade_history.append(trade)

        position_key = f"{trade.symbol}_{trade.exchange}"

        if trade.side.value == "buy":
            # Open or add to position
            if position_key in self.portfolio.positions:
                # Add to existing position (average price)
                existing = self.portfolio.positions[position_key]
                total_quantity = existing.quantity + trade.quantity
                avg_price = (
                    (existing.entry_price * existing.quantity +
                     trade.price * trade.quantity) / total_quantity
                )
                existing.quantity = total_quantity
                existing.entry_price = avg_price
            else:
                # New position
                self.portfolio.positions[position_key] = Position(
                    symbol=trade.symbol,
                    exchange=trade.exchange,
                    quantity=trade.quantity,
                    entry_price=trade.price,
                    entry_time=trade.timestamp
                )

            # Deduct from cash
            self.portfolio.cash -= trade.quantity * trade.price + trade.fees

        elif trade.side.value == "sell":
            # Close or reduce position
            if position_key in self.portfolio.positions:
                position = self.portfolio.positions[position_key]

                if trade.quantity >= position.quantity:
                    # Close entire position
                    realized_pnl = position.close(trade.price)
                    self.portfolio.closed_positions.append(position)
                    del self.portfolio.positions[position_key]

                    self.logger.info(
                        f"Closed position {position_key}: "
                        f"P&L: ${float(realized_pnl):,.2f} ({float(position.pnl_percentage):.2f}%)"
                    )
                else:
                    # Reduce position
                    partial_pnl = (trade.price - position.entry_price) * trade.quantity
                    position.quantity -= trade.quantity
                    position.realized_pnl += partial_pnl

                # Add to cash
                self.portfolio.cash += trade.quantity * trade.price - trade.fees

    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary."""
        return {
            "total_value": float(self.portfolio.total_value),
            "cash": float(self.portfolio.cash),
            "total_pnl": float(self.portfolio.total_pnl),
            "total_return_pct": float(self.portfolio.total_return),
            "leverage": float(self.portfolio.leverage),
            "num_positions": len(self.portfolio.positions),
            "positions": {
                key: {
                    "symbol": pos.symbol,
                    "exchange": pos.exchange,
                    "quantity": float(pos.quantity),
                    "entry_price": float(pos.entry_price),
                    "current_price": float(pos.current_price),
                    "market_value": float(pos.market_value),
                    "unrealized_pnl": float(pos.unrealized_pnl),
                    "pnl_pct": float(pos.pnl_percentage)
                }
                for key, pos in self.portfolio.positions.items()
            }
        }

    def get_performance_metrics(self) -> Dict:
        """Calculate portfolio performance metrics."""
        if not self.daily_returns:
            return {
                "sharpe_ratio": 0,
                "sortino_ratio": 0,
                "max_drawdown": 0,
                "win_rate": 0,
                "profit_factor": 0
            }

        returns_array = np.array([float(r) for r in self.daily_returns])

        # Sharpe Ratio
        if len(returns_array) > 1:
            sharpe = np.mean(returns_array) / np.std(returns_array) * np.sqrt(252)
        else:
            sharpe = 0

        # Sortino Ratio (downside deviation)
        downside_returns = returns_array[returns_array < 0]
        if len(downside_returns) > 1:
            downside_std = np.std(downside_returns)
            sortino = np.mean(returns_array) / downside_std * np.sqrt(252) if downside_std > 0 else 0
        else:
            sortino = 0

        # Max Drawdown
        cumulative = np.cumprod(1 + returns_array)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0

        # Win rate from closed positions
        if self.portfolio.closed_positions:
            winners = sum(1 for p in self.portfolio.closed_positions if p.realized_pnl > 0)
            win_rate = winners / len(self.portfolio.closed_positions)
        else:
            win_rate = 0

        # Profit factor
        gross_profit = sum(
            float(p.realized_pnl) for p in self.portfolio.closed_positions
            if p.realized_pnl > 0
        )
        gross_loss = abs(sum(
            float(p.realized_pnl) for p in self.portfolio.closed_positions
            if p.realized_pnl < 0
        ))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        return {
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "max_drawdown_pct": float(max_drawdown * 100),
            "win_rate": float(win_rate),
            "profit_factor": float(profit_factor),
            "total_trades": len(self.portfolio.closed_positions),
            "winners": sum(1 for p in self.portfolio.closed_positions if p.realized_pnl > 0),
            "losers": sum(1 for p in self.portfolio.closed_positions if p.realized_pnl < 0)
        }

    def get_position_sizing_recommendation(
        self,
        opportunity: ArbitrageOpportunity,
        method: str = "kelly"
    ) -> Decimal:
        """
        Calculate optimal position size.

        Args:
            opportunity: Opportunity to size
            method: Sizing method (kelly, fixed_fraction, volatility)

        Returns:
            Recommended position size
        """
        if method == "kelly":
            # Kelly Criterion: f = (bp - q) / b
            # f = fraction of capital to bet
            # b = odds received (profit/loss ratio)
            # p = probability of winning
            # q = probability of losing (1-p)

            p = float(opportunity.confidence_score)
            q = 1 - p
            b = 2.0  # Simplified profit/loss ratio

            kelly_fraction = (b * p - q) / b
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%

            return self.portfolio.total_value * Decimal(str(kelly_fraction))

        elif method == "fixed_fraction":
            # Fixed fraction of portfolio
            return self.portfolio.total_value * Decimal("0.02")  # 2%

        elif method == "volatility":
            # Volatility-based sizing
            # Higher volatility = smaller position
            risk_per_trade = Decimal("0.01")  # 1% risk
            return self.portfolio.total_value * risk_per_trade

        else:
            return self.max_position_size

    async def _monitor_portfolio(self):
        """Monitor portfolio and track performance."""
        last_value = self.portfolio.total_value

        while self.is_active:
            await asyncio.sleep(86400)  # Daily

            current_value = self.portfolio.total_value
            daily_return = (current_value - last_value) / last_value if last_value > 0 else Decimal(0)
            self.daily_returns.append(daily_return)

            # Store performance snapshot
            self.performance_history.append({
                "timestamp": datetime.now(),
                "total_value": float(current_value),
                "cash": float(self.portfolio.cash),
                "pnl": float(self.portfolio.total_pnl),
                "num_positions": len(self.portfolio.positions)
            })

            last_value = current_value

            # Log daily performance
            self.logger.info(
                f"Daily Performance - Value: ${float(current_value):,.2f}, "
                f"Return: {float(daily_return)*100:.2f}%, "
                f"Positions: {len(self.portfolio.positions)}"
            )

    def should_rebalance(self) -> bool:
        """Check if portfolio needs rebalancing."""
        if not self.portfolio.positions:
            return False

        # Check if any position exceeds concentration limit
        for position in self.portfolio.positions.values():
            weight = position.market_value / self.portfolio.total_value
            if weight > self.max_concentration + self.rebalance_threshold:
                return True

        return False

    def get_rebalancing_trades(self) -> List[Dict]:
        """Get trades needed to rebalance portfolio."""
        trades = []

        target_weight = Decimal(1) / Decimal(len(self.portfolio.positions))

        for position in self.portfolio.positions.values():
            current_weight = position.market_value / self.portfolio.total_value
            weight_diff = current_weight - target_weight

            if abs(weight_diff) > self.rebalance_threshold:
                # Need to adjust
                target_value = self.portfolio.total_value * target_weight
                adjustment = position.market_value - target_value

                if abs(adjustment) > Decimal(100):  # Minimum trade size
                    trades.append({
                        "symbol": position.symbol,
                        "exchange": position.exchange,
                        "action": "sell" if adjustment > 0 else "buy",
                        "quantity": abs(adjustment / position.current_price)
                    })

        return trades
