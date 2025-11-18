"""
Backtesting engine for arbitrage trading strategies.
"""
import asyncio
import logging
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass, field
from enum import Enum
import statistics
import math

from ..models.types import (
    MarketData, ArbitrageOpportunity, TradingAction, Trade,
    ArbitrageType, MarketType, OrderSide, OrderStatus
)
from ..services.data_providers import DataProviderManager


class BacktestMode(Enum):
    """Backtesting execution modes."""
    FAST = "fast"  # No delays
    REALISTIC = "realistic"  # Simulated latency
    TICK_BY_TICK = "tick_by_tick"  # Process each tick


@dataclass
class BacktestConfig:
    """Configuration for backtesting."""
    initial_capital: Decimal = Decimal("100000")
    commission_rate: Decimal = Decimal("0.001")  # 0.1%
    slippage_rate: Decimal = Decimal("0.0005")  # 0.05%
    max_position_size: Decimal = Decimal("0.1")  # 10% of capital per trade
    risk_free_rate: Decimal = Decimal("0.02")  # 2% annual
    mode: BacktestMode = BacktestMode.FAST
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    symbols: List[str] = field(default_factory=list)


@dataclass
class BacktestTrade:
    """Record of a backtested trade."""
    timestamp: datetime
    symbol: str
    side: OrderSide
    quantity: Decimal
    entry_price: Decimal
    exit_price: Optional[Decimal] = None
    exit_timestamp: Optional[datetime] = None
    commission: Decimal = Decimal("0")
    slippage: Decimal = Decimal("0")
    pnl: Decimal = Decimal("0")
    pnl_percentage: Decimal = Decimal("0")
    strategy: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class BacktestResult:
    """Results from a backtest run."""
    start_date: datetime
    end_date: datetime
    initial_capital: Decimal
    final_capital: Decimal
    total_return: Decimal
    total_return_pct: Decimal
    annualized_return: Decimal
    sharpe_ratio: Decimal
    sortino_ratio: Decimal
    max_drawdown: Decimal
    max_drawdown_pct: Decimal
    win_rate: Decimal
    profit_factor: Decimal
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: Decimal
    avg_loss: Decimal
    avg_trade_duration: timedelta
    trades: List[BacktestTrade]
    equity_curve: List[Dict]
    daily_returns: List[Decimal]
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "initial_capital": float(self.initial_capital),
            "final_capital": float(self.final_capital),
            "total_return": float(self.total_return),
            "total_return_pct": float(self.total_return_pct),
            "annualized_return": float(self.annualized_return),
            "sharpe_ratio": float(self.sharpe_ratio),
            "sortino_ratio": float(self.sortino_ratio),
            "max_drawdown": float(self.max_drawdown),
            "max_drawdown_pct": float(self.max_drawdown_pct),
            "win_rate": float(self.win_rate),
            "profit_factor": float(self.profit_factor),
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "avg_win": float(self.avg_win),
            "avg_loss": float(self.avg_loss),
            "avg_trade_duration_hours": self.avg_trade_duration.total_seconds() / 3600,
            "metadata": self.metadata
        }


class BacktestEngine:
    """Engine for backtesting arbitrage strategies."""

    def __init__(self, config: BacktestConfig = None):
        """
        Initialize backtesting engine.

        Args:
            config: Backtesting configuration
        """
        self.config = config or BacktestConfig()
        self.logger = logging.getLogger(__name__)

        # Data provider
        self.data_provider = DataProviderManager()

        # State
        self.capital = self.config.initial_capital
        self.positions: Dict[str, Dict] = {}
        self.trades: List[BacktestTrade] = []
        self.equity_curve: List[Dict] = []
        self.daily_returns: List[Decimal] = []

        # Strategy callback
        self.strategy: Optional[Callable] = None

        # Historical data cache
        self.historical_data: Dict[str, List[Dict]] = {}

    async def load_data(
        self,
        symbols: List[str],
        market_type: str = "crypto",
        days: int = 365,
        provider: str = "binance"
    ):
        """
        Load historical data for backtesting.

        Args:
            symbols: List of symbols to load
            market_type: Type of market (crypto, stock, forex)
            days: Number of days of history
            provider: Data provider to use
        """
        self.logger.info(f"Loading historical data for {len(symbols)} symbols...")

        for symbol in symbols:
            try:
                if market_type == "crypto":
                    data = await self.data_provider.get_crypto_historical(
                        symbol=symbol,
                        days=days,
                        provider=provider
                    )
                elif market_type == "stock":
                    # Convert days to period
                    if days <= 30:
                        period = "1mo"
                    elif days <= 90:
                        period = "3mo"
                    elif days <= 180:
                        period = "6mo"
                    elif days <= 365:
                        period = "1y"
                    else:
                        period = "2y"

                    data = await self.data_provider.get_stock_historical(
                        symbol=symbol,
                        period=period,
                        provider=provider
                    )
                elif market_type == "forex":
                    # Parse forex pair
                    from_curr = symbol[:3]
                    to_curr = symbol[3:] if len(symbol) == 6 else symbol[4:]
                    data = await self.data_provider.get_forex_historical(
                        from_currency=from_curr,
                        to_currency=to_curr,
                        days=days
                    )
                else:
                    self.logger.warning(f"Unknown market type: {market_type}")
                    continue

                if data:
                    self.historical_data[symbol] = data
                    self.logger.info(f"Loaded {len(data)} data points for {symbol}")
                else:
                    self.logger.warning(f"No data loaded for {symbol}")

            except Exception as e:
                self.logger.error(f"Error loading data for {symbol}: {e}")

        self.logger.info(f"Data loading complete. {len(self.historical_data)} symbols loaded.")

    def set_strategy(self, strategy: Callable):
        """
        Set the trading strategy to backtest.

        Args:
            strategy: Strategy function that takes (data, positions, capital)
                     and returns list of signals
        """
        self.strategy = strategy

    async def run(self) -> BacktestResult:
        """
        Run the backtest.

        Returns:
            Backtest results
        """
        if not self.historical_data:
            raise ValueError("No historical data loaded. Call load_data() first.")

        if not self.strategy:
            raise ValueError("No strategy set. Call set_strategy() first.")

        self.logger.info("Starting backtest...")

        # Reset state
        self.capital = self.config.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.daily_returns = []

        # Get all timestamps across all symbols
        all_timestamps = set()
        for symbol, data in self.historical_data.items():
            for bar in data:
                if "timestamp" in bar:
                    all_timestamps.add(bar["timestamp"])

        # Sort timestamps
        sorted_timestamps = sorted(all_timestamps)

        if not sorted_timestamps:
            raise ValueError("No valid timestamps in historical data")

        # Track previous equity for daily returns
        prev_equity = self.config.initial_capital
        prev_date = None

        # Process each timestamp
        for i, timestamp in enumerate(sorted_timestamps):
            # Get current bar data for all symbols
            current_data = {}
            for symbol, data in self.historical_data.items():
                bar = next(
                    (b for b in data if b.get("timestamp") == timestamp),
                    None
                )
                if bar:
                    current_data[symbol] = bar

            if not current_data:
                continue

            # Run strategy
            signals = self.strategy(current_data, self.positions, self.capital)

            # Process signals
            for signal in signals:
                await self._process_signal(signal, current_data, timestamp)

            # Update positions with current prices
            self._update_positions(current_data)

            # Calculate equity
            equity = self._calculate_equity(current_data)

            # Record equity curve
            self.equity_curve.append({
                "timestamp": timestamp,
                "equity": float(equity),
                "capital": float(self.capital),
                "positions_value": float(equity - self.capital)
            })

            # Calculate daily return
            current_date = datetime.fromtimestamp(timestamp / 1000).date() if timestamp > 1e10 else datetime.fromtimestamp(timestamp).date()
            if prev_date and current_date != prev_date:
                daily_return = (equity - prev_equity) / prev_equity
                self.daily_returns.append(daily_return)
                prev_equity = equity
                prev_date = current_date
            elif not prev_date:
                prev_date = current_date

        # Close remaining positions
        if sorted_timestamps:
            final_timestamp = sorted_timestamps[-1]
            final_data = {}
            for symbol, data in self.historical_data.items():
                bar = next(
                    (b for b in data if b.get("timestamp") == final_timestamp),
                    None
                )
                if bar:
                    final_data[symbol] = bar

            await self._close_all_positions(final_data, final_timestamp)

        # Calculate results
        result = self._calculate_results(sorted_timestamps)

        self.logger.info(f"Backtest complete. Total return: {result.total_return_pct:.2f}%")

        return result

    async def _process_signal(
        self,
        signal: Dict,
        current_data: Dict,
        timestamp: int
    ):
        """Process a trading signal."""
        symbol = signal.get("symbol")
        action = signal.get("action")  # "buy", "sell", "close"
        quantity = Decimal(str(signal.get("quantity", 0)))

        if not symbol or symbol not in current_data:
            return

        bar = current_data[symbol]
        price = Decimal(str(bar.get("close", 0)))

        if action == "buy":
            await self._open_position(symbol, OrderSide.BUY, quantity, price, timestamp, signal)
        elif action == "sell":
            await self._open_position(symbol, OrderSide.SELL, quantity, price, timestamp, signal)
        elif action == "close":
            await self._close_position(symbol, price, timestamp)

    async def _open_position(
        self,
        symbol: str,
        side: OrderSide,
        quantity: Decimal,
        price: Decimal,
        timestamp: int,
        signal: Dict
    ):
        """Open a new position."""
        # Check if we already have a position
        if symbol in self.positions:
            # Close existing position first
            await self._close_position(symbol, price, timestamp)

        # Calculate costs
        position_value = quantity * price
        commission = position_value * self.config.commission_rate
        slippage = position_value * self.config.slippage_rate

        # Check capital
        total_cost = position_value + commission + slippage
        if total_cost > self.capital:
            # Reduce quantity to fit capital
            max_value = self.capital * (Decimal("1") - self.config.commission_rate - self.config.slippage_rate)
            quantity = max_value / price
            position_value = quantity * price
            commission = position_value * self.config.commission_rate
            slippage = position_value * self.config.slippage_rate
            total_cost = position_value + commission + slippage

        if quantity <= 0:
            return

        # Deduct capital
        self.capital -= total_cost

        # Create position
        self.positions[symbol] = {
            "side": side,
            "quantity": quantity,
            "entry_price": price,
            "entry_timestamp": timestamp,
            "commission": commission,
            "slippage": slippage,
            "strategy": signal.get("strategy", ""),
            "metadata": signal.get("metadata", {})
        }

        # Create trade record
        trade = BacktestTrade(
            timestamp=datetime.fromtimestamp(timestamp / 1000) if timestamp > 1e10 else datetime.fromtimestamp(timestamp),
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=price,
            commission=commission,
            slippage=slippage,
            strategy=signal.get("strategy", ""),
            metadata=signal.get("metadata", {})
        )

        self.trades.append(trade)

    async def _close_position(
        self,
        symbol: str,
        price: Decimal,
        timestamp: int
    ):
        """Close an existing position."""
        if symbol not in self.positions:
            return

        position = self.positions[symbol]

        # Calculate exit costs
        position_value = position["quantity"] * price
        exit_commission = position_value * self.config.commission_rate
        exit_slippage = position_value * self.config.slippage_rate

        # Calculate PnL
        if position["side"] == OrderSide.BUY:
            gross_pnl = (price - position["entry_price"]) * position["quantity"]
        else:
            gross_pnl = (position["entry_price"] - price) * position["quantity"]

        total_costs = position["commission"] + position["slippage"] + exit_commission + exit_slippage
        net_pnl = gross_pnl - total_costs

        # Return capital
        self.capital += position_value - exit_commission - exit_slippage + gross_pnl

        # Update trade record
        for trade in reversed(self.trades):
            if trade.symbol == symbol and trade.exit_price is None:
                trade.exit_price = price
                trade.exit_timestamp = datetime.fromtimestamp(timestamp / 1000) if timestamp > 1e10 else datetime.fromtimestamp(timestamp)
                trade.commission += exit_commission
                trade.slippage += exit_slippage
                trade.pnl = net_pnl
                entry_value = trade.entry_price * trade.quantity
                trade.pnl_percentage = (net_pnl / entry_value * 100) if entry_value else Decimal("0")
                break

        # Remove position
        del self.positions[symbol]

    async def _close_all_positions(
        self,
        current_data: Dict,
        timestamp: int
    ):
        """Close all open positions."""
        symbols = list(self.positions.keys())
        for symbol in symbols:
            if symbol in current_data:
                price = Decimal(str(current_data[symbol].get("close", 0)))
                await self._close_position(symbol, price, timestamp)

    def _update_positions(self, current_data: Dict):
        """Update position values with current prices."""
        for symbol, position in self.positions.items():
            if symbol in current_data:
                position["current_price"] = Decimal(str(current_data[symbol].get("close", 0)))

    def _calculate_equity(self, current_data: Dict) -> Decimal:
        """Calculate total equity."""
        equity = self.capital

        for symbol, position in self.positions.items():
            if symbol in current_data:
                price = Decimal(str(current_data[symbol].get("close", 0)))
                position_value = position["quantity"] * price

                if position["side"] == OrderSide.BUY:
                    pnl = (price - position["entry_price"]) * position["quantity"]
                else:
                    pnl = (position["entry_price"] - price) * position["quantity"]

                equity += position_value + pnl

        return equity

    def _calculate_results(self, timestamps: List[int]) -> BacktestResult:
        """Calculate backtest results."""
        # Basic metrics
        start_time = timestamps[0]
        end_time = timestamps[-1]

        start_date = datetime.fromtimestamp(start_time / 1000) if start_time > 1e10 else datetime.fromtimestamp(start_time)
        end_date = datetime.fromtimestamp(end_time / 1000) if end_time > 1e10 else datetime.fromtimestamp(end_time)

        final_capital = self.capital
        total_return = final_capital - self.config.initial_capital
        total_return_pct = (total_return / self.config.initial_capital) * 100

        # Annualized return
        days = (end_date - start_date).days
        if days > 0:
            annualized_return = ((final_capital / self.config.initial_capital) ** (Decimal("365") / Decimal(str(days))) - 1) * 100
        else:
            annualized_return = Decimal("0")

        # Trade analysis
        closed_trades = [t for t in self.trades if t.exit_price is not None]
        winning_trades = [t for t in closed_trades if t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl < 0]

        total_trades = len(closed_trades)
        num_winning = len(winning_trades)
        num_losing = len(losing_trades)

        win_rate = Decimal(str(num_winning / total_trades * 100)) if total_trades > 0 else Decimal("0")

        avg_win = (sum(t.pnl for t in winning_trades) / num_winning) if num_winning > 0 else Decimal("0")
        avg_loss = abs(sum(t.pnl for t in losing_trades) / num_losing) if num_losing > 0 else Decimal("0")

        # Profit factor
        gross_profit = sum(t.pnl for t in winning_trades)
        gross_loss = abs(sum(t.pnl for t in losing_trades))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else Decimal("999")

        # Average trade duration
        durations = []
        for trade in closed_trades:
            if trade.exit_timestamp:
                duration = trade.exit_timestamp - trade.timestamp
                durations.append(duration)

        avg_duration = sum(durations, timedelta()) / len(durations) if durations else timedelta()

        # Max drawdown
        max_drawdown, max_drawdown_pct = self._calculate_max_drawdown()

        # Sharpe and Sortino ratios
        sharpe_ratio = self._calculate_sharpe_ratio()
        sortino_ratio = self._calculate_sortino_ratio()

        return BacktestResult(
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.config.initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            total_return_pct=total_return_pct,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_pct=max_drawdown_pct,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=total_trades,
            winning_trades=num_winning,
            losing_trades=num_losing,
            avg_win=avg_win,
            avg_loss=avg_loss,
            avg_trade_duration=avg_duration,
            trades=self.trades,
            equity_curve=self.equity_curve,
            daily_returns=self.daily_returns
        )

    def _calculate_max_drawdown(self) -> tuple:
        """Calculate maximum drawdown."""
        if not self.equity_curve:
            return Decimal("0"), Decimal("0")

        peak = Decimal(str(self.equity_curve[0]["equity"]))
        max_dd = Decimal("0")
        max_dd_pct = Decimal("0")

        for point in self.equity_curve:
            equity = Decimal(str(point["equity"]))

            if equity > peak:
                peak = equity

            drawdown = peak - equity
            drawdown_pct = (drawdown / peak * 100) if peak > 0 else Decimal("0")

            if drawdown > max_dd:
                max_dd = drawdown
                max_dd_pct = drawdown_pct

        return max_dd, max_dd_pct

    def _calculate_sharpe_ratio(self) -> Decimal:
        """Calculate Sharpe ratio."""
        if len(self.daily_returns) < 2:
            return Decimal("0")

        returns = [float(r) for r in self.daily_returns]

        avg_return = statistics.mean(returns)
        std_return = statistics.stdev(returns)

        if std_return == 0:
            return Decimal("0")

        # Annualize
        daily_rf = float(self.config.risk_free_rate) / 252
        excess_return = avg_return - daily_rf

        sharpe = (excess_return / std_return) * math.sqrt(252)

        return Decimal(str(round(sharpe, 4)))

    def _calculate_sortino_ratio(self) -> Decimal:
        """Calculate Sortino ratio."""
        if len(self.daily_returns) < 2:
            return Decimal("0")

        returns = [float(r) for r in self.daily_returns]

        avg_return = statistics.mean(returns)

        # Downside deviation
        negative_returns = [r for r in returns if r < 0]

        if not negative_returns:
            return Decimal("999")  # No negative returns

        downside_std = statistics.stdev(negative_returns) if len(negative_returns) > 1 else abs(negative_returns[0])

        if downside_std == 0:
            return Decimal("999")

        # Annualize
        daily_rf = float(self.config.risk_free_rate) / 252
        excess_return = avg_return - daily_rf

        sortino = (excess_return / downside_std) * math.sqrt(252)

        return Decimal(str(round(sortino, 4)))


# Example strategies

def simple_momentum_strategy(
    current_data: Dict,
    positions: Dict,
    capital: Decimal
) -> List[Dict]:
    """
    Simple momentum strategy for backtesting.

    Buys when price is above 20-period SMA, sells when below.
    """
    signals = []

    for symbol, bar in current_data.items():
        # This is simplified - real implementation would track historical prices
        if "sma_20" in bar:
            price = bar.get("close", 0)
            sma = bar.get("sma_20", 0)

            if symbol not in positions:
                if price > sma:
                    # Buy signal
                    quantity = capital * Decimal("0.1") / Decimal(str(price))
                    signals.append({
                        "symbol": symbol,
                        "action": "buy",
                        "quantity": quantity,
                        "strategy": "momentum"
                    })
            else:
                if price < sma:
                    # Sell signal
                    signals.append({
                        "symbol": symbol,
                        "action": "close",
                        "strategy": "momentum"
                    })

    return signals


def mean_reversion_strategy(
    current_data: Dict,
    positions: Dict,
    capital: Decimal,
    z_score_threshold: float = 2.0
) -> List[Dict]:
    """
    Mean reversion strategy for backtesting.

    Buys when price is z_score_threshold below mean, sells when above.
    """
    signals = []

    for symbol, bar in current_data.items():
        if "z_score" in bar:
            z_score = bar.get("z_score", 0)
            price = bar.get("close", 0)

            if symbol not in positions:
                if z_score < -z_score_threshold:
                    # Oversold - buy
                    quantity = capital * Decimal("0.1") / Decimal(str(price))
                    signals.append({
                        "symbol": symbol,
                        "action": "buy",
                        "quantity": quantity,
                        "strategy": "mean_reversion"
                    })
                elif z_score > z_score_threshold:
                    # Overbought - short
                    quantity = capital * Decimal("0.1") / Decimal(str(price))
                    signals.append({
                        "symbol": symbol,
                        "action": "sell",
                        "quantity": quantity,
                        "strategy": "mean_reversion"
                    })
            else:
                # Close when returning to mean
                if abs(z_score) < 0.5:
                    signals.append({
                        "symbol": symbol,
                        "action": "close",
                        "strategy": "mean_reversion"
                    })

    return signals


def cross_exchange_arbitrage_strategy(
    current_data: Dict,
    positions: Dict,
    capital: Decimal,
    min_spread: float = 0.005  # 0.5%
) -> List[Dict]:
    """
    Cross-exchange arbitrage strategy for backtesting.

    Looks for price differences between exchanges.
    """
    signals = []

    # Group by base symbol
    symbol_prices = {}
    for symbol, bar in current_data.items():
        # Extract base symbol (e.g., "BTCUSDT_binance" -> "BTCUSDT")
        base = symbol.split("_")[0] if "_" in symbol else symbol
        if base not in symbol_prices:
            symbol_prices[base] = []
        symbol_prices[base].append({
            "symbol": symbol,
            "price": bar.get("close", 0),
            "exchange": symbol.split("_")[1] if "_" in symbol else "default"
        })

    # Find arbitrage opportunities
    for base, prices in symbol_prices.items():
        if len(prices) < 2:
            continue

        # Find min and max prices
        sorted_prices = sorted(prices, key=lambda x: x["price"])
        min_price_data = sorted_prices[0]
        max_price_data = sorted_prices[-1]

        spread = (max_price_data["price"] - min_price_data["price"]) / min_price_data["price"]

        if spread >= min_spread:
            # Buy on low exchange, sell on high exchange
            buy_symbol = min_price_data["symbol"]
            sell_symbol = max_price_data["symbol"]

            if buy_symbol not in positions:
                quantity = capital * Decimal("0.05") / Decimal(str(min_price_data["price"]))
                signals.append({
                    "symbol": buy_symbol,
                    "action": "buy",
                    "quantity": quantity,
                    "strategy": "cross_exchange_arb",
                    "metadata": {
                        "spread": float(spread),
                        "paired_symbol": sell_symbol
                    }
                })

    return signals
