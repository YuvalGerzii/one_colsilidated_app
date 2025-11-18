"""
Backtesting Framework for Trading Agents

Allows testing trading strategies on historical data to evaluate performance
before deploying them in live trading.

Based on research:
- Systematic Trading: A unique new method for designing trading and investing systems (Robert Carver)
- Backtesting Trading Strategies (QuantStart)
- Algorithmic Trading Evaluation (ACM, 2024)
"""

import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from .base_agent import BaseTradingAgent, MarketData, SignalType


@dataclass
class BacktestConfig:
    """Configuration for backtesting"""
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1% per trade
    slippage: float = 0.0005  # 0.05% slippage
    position_size: float = 1.0  # Fraction of capital per trade
    max_positions: int = 1  # Maximum concurrent positions
    stop_loss_pct: Optional[float] = None  # Stop loss percentage
    take_profit_pct: Optional[float] = None  # Take profit percentage


@dataclass
class Trade:
    """Individual trade record"""
    entry_time: datetime
    exit_time: Optional[datetime]
    entry_price: float
    exit_price: Optional[float]
    quantity: int
    side: str  # "long" or "short"
    pnl: float = 0.0
    pnl_pct: float = 0.0
    commission_paid: float = 0.0
    is_open: bool = True
    exit_reason: str = ""  # "signal", "stop_loss", "take_profit", "end_of_data"


@dataclass
class BacktestResults:
    """Results from backtesting"""
    # Trade statistics
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0

    # Financial metrics
    initial_capital: float = 100000.0
    final_capital: float = 100000.0
    total_return: float = 0.0
    total_return_pct: float = 0.0
    annualized_return: float = 0.0

    # Risk metrics
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    volatility: float = 0.0

    # Trade analysis
    avg_win: float = 0.0
    avg_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    avg_trade_duration: float = 0.0  # in hours

    # Equity curve
    equity_curve: List[float] = field(default_factory=list)
    dates: List[datetime] = field(default_factory=list)

    # Trade history
    trades: List[Trade] = field(default_factory=list)

    # Additional metrics
    profit_factor: float = 0.0  # Gross profit / Gross loss
    recovery_factor: float = 0.0  # Net profit / Max drawdown
    calmar_ratio: float = 0.0  # Annualized return / Max drawdown


class Backtester:
    """
    Backtesting engine for trading agents
    """

    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig()
        self.results = BacktestResults(initial_capital=self.config.initial_capital)
        self.current_capital = self.config.initial_capital
        self.open_trades: List[Trade] = []
        self.closed_trades: List[Trade] = []

    def run(
        self,
        agent: BaseTradingAgent,
        market_data: List[MarketData],
        train_period: int = 0
    ) -> BacktestResults:
        """
        Run backtest on historical data

        Args:
            agent: Trading agent to backtest
            market_data: Historical market data
            train_period: Number of initial periods to use for training (not traded)

        Returns:
            BacktestResults with performance metrics
        """
        # Train agent if needed
        if train_period > 0 and train_period < len(market_data):
            print(f"Training agent on first {train_period} periods...")
            agent.train(market_data[:train_period])

        # Start backtesting
        start_index = max(train_period, 20)  # Need some data for analysis
        equity_curve = [self.current_capital]
        dates = []

        print(f"Backtesting from period {start_index} to {len(market_data)}...")

        for i in range(start_index, len(market_data)):
            current_data = market_data[:i + 1]
            current_bar = market_data[i]

            # Update dates
            dates.append(current_bar.timestamp)

            # Check open positions for stop loss / take profit
            self._check_exit_conditions(current_bar)

            # Get trading signal from agent
            signal = agent.analyze(current_data)

            # Execute trades based on signal
            self._execute_signal(signal, current_bar)

            # Track equity
            equity = self._calculate_equity(current_bar.close)
            equity_curve.append(equity)

        # Close any remaining open positions
        if market_data:
            final_bar = market_data[-1]
            for trade in self.open_trades[:]:
                self._close_trade(trade, final_bar.close, final_bar.timestamp, "end_of_data")

        # Calculate final results
        self.results = self._calculate_results(
            equity_curve,
            dates,
            market_data[start_index].timestamp,
            market_data[-1].timestamp if market_data else datetime.now()
        )

        return self.results

    def _execute_signal(self, signal, current_bar: MarketData):
        """Execute trading signal"""
        # Skip if at position limit
        if len(self.open_trades) >= self.config.max_positions:
            return

        # Execute based on signal type
        if signal.signal_type == SignalType.BUY and signal.confidence > 0.5:
            # Open long position
            self._open_trade("long", current_bar)

        elif signal.signal_type == SignalType.SELL and signal.confidence > 0.5:
            # Close any long positions
            for trade in self.open_trades[:]:
                if trade.side == "long":
                    self._close_trade(trade, current_bar.close, current_bar.timestamp, "signal")

        elif signal.signal_type == SignalType.HOLD:
            # Do nothing or close positions
            pass

    def _open_trade(self, side: str, current_bar: MarketData):
        """Open a new trade"""
        # Calculate position size
        position_value = self.current_capital * self.config.position_size
        price = current_bar.close * (1 + self.config.slippage)  # Account for slippage
        quantity = int(position_value / price)

        if quantity == 0:
            return

        # Calculate commission
        commission = position_value * self.config.commission

        trade = Trade(
            entry_time=current_bar.timestamp,
            exit_time=None,
            entry_price=price,
            exit_price=None,
            quantity=quantity,
            side=side,
            commission_paid=commission
        )

        self.open_trades.append(trade)
        self.current_capital -= commission

    def _close_trade(
        self,
        trade: Trade,
        exit_price: float,
        exit_time: datetime,
        reason: str
    ):
        """Close an existing trade"""
        # Account for slippage
        actual_exit_price = exit_price * (1 - self.config.slippage)

        # Calculate PnL
        if trade.side == "long":
            pnl = (actual_exit_price - trade.entry_price) * trade.quantity
        else:  # short
            pnl = (trade.entry_price - actual_exit_price) * trade.quantity

        # Subtract commission
        commission = actual_exit_price * trade.quantity * self.config.commission
        pnl -= commission
        pnl -= trade.commission_paid

        # Update trade
        trade.exit_price = actual_exit_price
        trade.exit_time = exit_time
        trade.pnl = pnl
        trade.pnl_pct = (pnl / (trade.entry_price * trade.quantity)) * 100
        trade.commission_paid += commission
        trade.is_open = False
        trade.exit_reason = reason

        # Update capital
        self.current_capital += pnl

        # Move to closed trades
        self.open_trades.remove(trade)
        self.closed_trades.append(trade)

    def _check_exit_conditions(self, current_bar: MarketData):
        """Check stop loss and take profit conditions"""
        for trade in self.open_trades[:]:
            if trade.side == "long":
                # Check stop loss
                if self.config.stop_loss_pct:
                    stop_price = trade.entry_price * (1 - self.config.stop_loss_pct)
                    if current_bar.low <= stop_price:
                        self._close_trade(trade, stop_price, current_bar.timestamp, "stop_loss")
                        continue

                # Check take profit
                if self.config.take_profit_pct:
                    target_price = trade.entry_price * (1 + self.config.take_profit_pct)
                    if current_bar.high >= target_price:
                        self._close_trade(trade, target_price, current_bar.timestamp, "take_profit")
                        continue

    def _calculate_equity(self, current_price: float) -> float:
        """Calculate current equity including open positions"""
        equity = self.current_capital

        for trade in self.open_trades:
            if trade.side == "long":
                unrealized_pnl = (current_price - trade.entry_price) * trade.quantity
            else:
                unrealized_pnl = (trade.entry_price - current_price) * trade.quantity

            equity += unrealized_pnl

        return equity

    def _calculate_results(
        self,
        equity_curve: List[float],
        dates: List[datetime],
        start_date: datetime,
        end_date: datetime
    ) -> BacktestResults:
        """Calculate final backtest results"""
        results = BacktestResults(
            initial_capital=self.config.initial_capital,
            equity_curve=equity_curve,
            dates=dates,
            trades=self.closed_trades
        )

        # Basic stats
        results.total_trades = len(self.closed_trades)

        if results.total_trades == 0:
            return results

        # Win/loss stats
        winning_trades = [t for t in self.closed_trades if t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl < 0]

        results.winning_trades = len(winning_trades)
        results.losing_trades = len(losing_trades)
        results.win_rate = results.winning_trades / results.total_trades if results.total_trades > 0 else 0

        # Financial metrics
        results.final_capital = equity_curve[-1]
        results.total_return = results.final_capital - results.initial_capital
        results.total_return_pct = (results.total_return / results.initial_capital) * 100

        # Annualized return
        days = (end_date - start_date).days
        years = days / 365.25
        if years > 0:
            results.annualized_return = ((results.final_capital / results.initial_capital) ** (1 / years) - 1) * 100

        # Trade analysis
        if winning_trades:
            results.avg_win = np.mean([t.pnl for t in winning_trades])
            results.largest_win = max([t.pnl for t in winning_trades])

        if losing_trades:
            results.avg_loss = np.mean([t.pnl for t in losing_trades])
            results.largest_loss = min([t.pnl for t in losing_trades])

        # Average trade duration
        durations = [
            (t.exit_time - t.entry_time).total_seconds() / 3600
            for t in self.closed_trades if t.exit_time
        ]
        if durations:
            results.avg_trade_duration = np.mean(durations)

        # Risk metrics
        returns = np.diff(equity_curve) / equity_curve[:-1]

        if len(returns) > 0:
            results.volatility = np.std(returns) * np.sqrt(252)  # Annualized

            # Sharpe ratio (assuming 2% risk-free rate)
            mean_return = np.mean(returns)
            if results.volatility > 0:
                results.sharpe_ratio = (mean_return * 252 - 0.02) / results.volatility

            # Sortino ratio
            downside_returns = returns[returns < 0]
            if len(downside_returns) > 0:
                downside_std = np.std(downside_returns) * np.sqrt(252)
                if downside_std > 0:
                    results.sortino_ratio = (mean_return * 252 - 0.02) / downside_std

        # Maximum drawdown
        peak = equity_curve[0]
        max_dd = 0
        for value in equity_curve:
            if value > peak:
                peak = value
            dd = peak - value
            if dd > max_dd:
                max_dd = dd

        results.max_drawdown = max_dd
        results.max_drawdown_pct = (max_dd / peak) * 100 if peak > 0 else 0

        # Profit factor
        gross_profit = sum([t.pnl for t in winning_trades]) if winning_trades else 0
        gross_loss = abs(sum([t.pnl for t in losing_trades])) if losing_trades else 0
        results.profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        # Recovery factor
        results.recovery_factor = results.total_return / max_dd if max_dd > 0 else 0

        # Calmar ratio
        if results.max_drawdown_pct > 0:
            results.calmar_ratio = results.annualized_return / results.max_drawdown_pct

        return results


def print_backtest_results(results: BacktestResults):
    """Print formatted backtest results"""
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)

    print(f"\nCapital:")
    print(f"  Initial: ${results.initial_capital:,.2f}")
    print(f"  Final:   ${results.final_capital:,.2f}")
    print(f"  Return:  ${results.total_return:,.2f} ({results.total_return_pct:.2f}%)")
    print(f"  Annualized Return: {results.annualized_return:.2f}%")

    print(f"\nTrade Statistics:")
    print(f"  Total Trades:   {results.total_trades}")
    print(f"  Winning Trades: {results.winning_trades}")
    print(f"  Losing Trades:  {results.losing_trades}")
    print(f"  Win Rate:       {results.win_rate * 100:.2f}%")

    print(f"\nTrade Analysis:")
    print(f"  Average Win:    ${results.avg_win:,.2f}")
    print(f"  Average Loss:   ${results.avg_loss:,.2f}")
    print(f"  Largest Win:    ${results.largest_win:,.2f}")
    print(f"  Largest Loss:   ${results.largest_loss:,.2f}")
    print(f"  Avg Duration:   {results.avg_trade_duration:.1f} hours")

    print(f"\nRisk Metrics:")
    print(f"  Sharpe Ratio:     {results.sharpe_ratio:.2f}")
    print(f"  Sortino Ratio:    {results.sortino_ratio:.2f}")
    print(f"  Max Drawdown:     ${results.max_drawdown:,.2f} ({results.max_drawdown_pct:.2f}%)")
    print(f"  Volatility:       {results.volatility * 100:.2f}%")
    print(f"  Profit Factor:    {results.profit_factor:.2f}")
    print(f"  Recovery Factor:  {results.recovery_factor:.2f}")
    print(f"  Calmar Ratio:     {results.calmar_ratio:.2f}")

    print("\n" + "=" * 60)
