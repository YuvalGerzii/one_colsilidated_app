# Backtesting System

This document describes the backtesting capabilities added to the arbitrage trading system.

## Overview

The backtesting system allows you to test arbitrage strategies against historical data before deploying them in live trading. It includes:

- **Free Data Providers** - No API keys required for basic usage
- **Backtesting Engine** - Comprehensive simulation engine
- **Data Storage** - Caching system to avoid repeated API calls
- **Performance Metrics** - Full suite of trading metrics

## Free Data Providers

### CoinGecko (Crypto)
- **Rate Limit**: 30 calls/minute (free tier)
- **No API Key Required** for demo usage
- **Data Available**: Historical OHLC, market charts

```python
from arbitrage_trader.services import CoinGeckoProvider

provider = CoinGeckoProvider()
data = await provider.get_historical_data("bitcoin", "usd", days=30)
```

### Binance Public API (Crypto)
- **Rate Limit**: 1200 requests/minute
- **No API Key Required** for public endpoints
- **Data Available**: Klines (OHLCV), order books, tickers

```python
from arbitrage_trader.services import BinancePublicProvider

provider = BinancePublicProvider()
data = await provider.get_klines("BTCUSDT", "1h", limit=500)
```

### Yahoo Finance (Stocks)
- **No Rate Limit** (reasonable usage)
- **No API Key Required**
- **Data Available**: Historical OHLCV for stocks

```python
from arbitrage_trader.services import YahooFinanceProvider

provider = YahooFinanceProvider()
data = await provider.get_historical_data("AAPL", period="1y", interval="1d")
```

### Alpha Vantage (Stocks/Forex/Crypto)
- **Rate Limit**: 5 requests/minute, 500/day (free tier)
- **Requires Free API Key** - [Get one here](https://www.alphavantage.co/support/#api-key)
- **Data Available**: Stocks, forex, crypto daily data

```python
from arbitrage_trader.services import AlphaVantageProvider

provider = AlphaVantageProvider(api_key="YOUR_KEY")
data = await provider.get_daily_stock("MSFT")
```

### Unified Data Manager

```python
from arbitrage_trader.services import DataProviderManager

manager = DataProviderManager()

# Crypto
crypto_data = await manager.get_crypto_historical("BTCUSDT", days=30, provider="binance")

# Stocks
stock_data = await manager.get_stock_historical("AAPL", period="1y", provider="yahoo")

# Forex
forex_data = await manager.get_forex_historical("EUR", "USD", days=100)
```

## Backtesting Engine

### Basic Usage

```python
from arbitrage_trader.backtesting import (
    BacktestEngine,
    BacktestConfig,
    simple_momentum_strategy
)

# Configure backtest
config = BacktestConfig(
    initial_capital=Decimal("100000"),
    commission_rate=Decimal("0.001"),  # 0.1%
    slippage_rate=Decimal("0.0005"),   # 0.05%
)

# Create engine
engine = BacktestEngine(config)

# Load historical data
await engine.load_data(
    symbols=["BTCUSDT", "ETHUSDT"],
    market_type="crypto",
    days=365,
    provider="binance"
)

# Set strategy
engine.set_strategy(simple_momentum_strategy)

# Run backtest
result = await engine.run()

# View results
print(f"Total Return: {result.total_return_pct:.2f}%")
print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
print(f"Max Drawdown: {result.max_drawdown_pct:.2f}%")
print(f"Win Rate: {result.win_rate:.2f}%")
```

### Custom Strategy

```python
def my_arbitrage_strategy(current_data, positions, capital):
    """
    Custom strategy function.

    Args:
        current_data: Dict[symbol, bar_data] - Current market data
        positions: Dict[symbol, position] - Open positions
        capital: Decimal - Available capital

    Returns:
        List[Dict] - Trading signals
    """
    signals = []

    for symbol, bar in current_data.items():
        price = bar.get("close", 0)

        # Your strategy logic here
        if some_buy_condition:
            signals.append({
                "symbol": symbol,
                "action": "buy",
                "quantity": capital * 0.1 / price,
                "strategy": "my_strategy",
                "metadata": {"reason": "buy signal"}
            })
        elif some_sell_condition:
            signals.append({
                "symbol": symbol,
                "action": "close",
                "strategy": "my_strategy"
            })

    return signals

engine.set_strategy(my_arbitrage_strategy)
```

### Built-in Strategies

1. **simple_momentum_strategy** - Buy when price > SMA, sell when below
2. **mean_reversion_strategy** - Buy/sell based on z-score from mean
3. **cross_exchange_arbitrage_strategy** - Exploit price differences across exchanges

## Performance Metrics

The backtest result includes comprehensive metrics:

### Returns
- `total_return` - Total P&L in currency
- `total_return_pct` - Total return percentage
- `annualized_return` - Annualized return percentage

### Risk Metrics
- `sharpe_ratio` - Risk-adjusted return (annualized)
- `sortino_ratio` - Downside risk-adjusted return
- `max_drawdown` - Maximum peak-to-trough decline
- `max_drawdown_pct` - Maximum drawdown percentage

### Trade Statistics
- `total_trades` - Number of completed trades
- `winning_trades` - Number of profitable trades
- `losing_trades` - Number of unprofitable trades
- `win_rate` - Percentage of winning trades
- `profit_factor` - Gross profit / Gross loss
- `avg_win` - Average winning trade P&L
- `avg_loss` - Average losing trade P&L
- `avg_trade_duration` - Average time in trade

### Data
- `trades` - List of all trade records
- `equity_curve` - Equity over time
- `daily_returns` - Daily return series

## Data Storage

### File Storage (JSON)

```python
from arbitrage_trader.backtesting import FileStorage

storage = FileStorage(base_path="/path/to/data")

# Save data
storage.save("BTCUSDT_1h", data, metadata={"source": "binance"})

# Load data
data = storage.load("BTCUSDT_1h")

# Check existence
if storage.exists("BTCUSDT_1h"):
    print("Data found")

# List all keys
keys = storage.list_keys()
```

### SQLite Storage

Better for large datasets and efficient querying:

```python
from arbitrage_trader.backtesting import SQLiteStorage

storage = SQLiteStorage(db_path="/path/to/data.db")

# Save and load same as FileStorage
storage.save("BTCUSDT_1h", data)
data = storage.load("BTCUSDT_1h")

# Query with filters
filtered = storage.query(
    "BTCUSDT_1h",
    start_time=1640000000000,
    end_time=1650000000000,
    limit=1000
)
```

### Cached Data Provider

Automatically caches API responses:

```python
from arbitrage_trader.services import DataProviderManager
from arbitrage_trader.backtesting import CachedDataProvider, SQLiteStorage

# Create cached provider
provider = DataProviderManager()
storage = SQLiteStorage()
cached = CachedDataProvider(
    provider,
    storage,
    cache_duration_hours=24
)

# Data is automatically cached
data = await cached.get_crypto_historical("BTCUSDT", days=30)

# Force refresh cache
data = await cached.get_crypto_historical("BTCUSDT", days=30, force_refresh=True)

# Clear cache
cached.clear_cache(pattern="BTCUSDT")
```

## Configuration Options

```python
from arbitrage_trader.backtesting import BacktestConfig, BacktestMode

config = BacktestConfig(
    # Capital
    initial_capital=Decimal("100000"),

    # Costs
    commission_rate=Decimal("0.001"),   # 0.1%
    slippage_rate=Decimal("0.0005"),    # 0.05%

    # Position sizing
    max_position_size=Decimal("0.1"),   # 10% of capital per trade

    # Risk-free rate for Sharpe calculation
    risk_free_rate=Decimal("0.02"),     # 2% annual

    # Execution mode
    mode=BacktestMode.FAST,             # FAST, REALISTIC, or TICK_BY_TICK

    # Date filters (optional)
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31),

    # Symbols (optional)
    symbols=["BTCUSDT", "ETHUSDT"]
)
```

## Example: Full Backtest

```python
import asyncio
from decimal import Decimal
from arbitrage_trader.backtesting import (
    BacktestEngine,
    BacktestConfig,
    CachedDataProvider,
    SQLiteStorage
)
from arbitrage_trader.services import DataProviderManager

async def run_backtest():
    # Setup
    config = BacktestConfig(
        initial_capital=Decimal("50000"),
        commission_rate=Decimal("0.001")
    )

    engine = BacktestEngine(config)

    # Load data with caching
    storage = SQLiteStorage()
    cached_provider = CachedDataProvider(
        engine.data_provider,
        storage
    )

    # Override engine's provider with cached version
    engine.data_provider = cached_provider

    # Load data
    await engine.load_data(
        symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT"],
        market_type="crypto",
        days=180
    )

    # Define strategy
    def my_strategy(data, positions, capital):
        signals = []
        # Strategy implementation
        return signals

    engine.set_strategy(my_strategy)

    # Run
    result = await engine.run()

    # Report
    print("=" * 50)
    print("BACKTEST RESULTS")
    print("=" * 50)
    print(f"Period: {result.start_date} to {result.end_date}")
    print(f"Initial Capital: ${result.initial_capital:,.2f}")
    print(f"Final Capital: ${result.final_capital:,.2f}")
    print(f"Total Return: {result.total_return_pct:.2f}%")
    print(f"Annualized Return: {result.annualized_return:.2f}%")
    print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
    print(f"Sortino Ratio: {result.sortino_ratio:.2f}")
    print(f"Max Drawdown: {result.max_drawdown_pct:.2f}%")
    print(f"Total Trades: {result.total_trades}")
    print(f"Win Rate: {result.win_rate:.2f}%")
    print(f"Profit Factor: {result.profit_factor:.2f}")
    print("=" * 50)

    return result

if __name__ == "__main__":
    asyncio.run(run_backtest())
```

## Rate Limit Considerations

When fetching data from free APIs:

| Provider      | Rate Limit          | Daily Limit |
|---------------|---------------------|-------------|
| CoinGecko     | 30/minute           | ~10,000     |
| Binance       | 1,200/minute        | Unlimited   |
| Yahoo Finance | Reasonable usage    | Unlimited   |
| Alpha Vantage | 5/minute            | 500/day     |

**Best Practices:**
- Use the `CachedDataProvider` to avoid repeated API calls
- Load all needed data at once before running multiple backtests
- For Alpha Vantage, batch requests and add delays
- Store frequently used data in SQLite for fast access
