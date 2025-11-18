# Multi-Agent Arbitrage Trading System

A sophisticated, production-ready arbitrage detection and trading system using multiple specialized AI agents for different arbitrage strategies across various markets.

## 🎯 Overview

This system implements a multi-agent architecture where specialized agents work collaboratively to detect, analyze, and execute arbitrage opportunities across different markets (crypto, forex, stocks) and arbitrage types.

## 🏗️ Architecture

### Multi-Agent System

The system employs multiple specialized agents, each focusing on specific arbitrage strategies:

1. **Cross-Exchange Agent** - Detects spatial arbitrage across different exchanges
2. **Statistical Arbitrage Agent** - Implements pairs trading and mean reversion strategies
3. **Triangular Arbitrage Agent** - Finds triangular arbitrage in currency/crypto markets
4. **Risk Manager Agent** - Monitors positions, exposure, and enforces risk limits

### System Components

```
arbitrage_trader/
├── agents/              # Specialized trading agents
│   ├── base_agent.py
│   ├── cross_exchange_agent.py
│   ├── statistical_agent.py
│   ├── triangular_agent.py
│   └── risk_manager_agent.py
├── algorithms/          # Detection algorithms
│   ├── cross_exchange.py
│   ├── statistical.py
│   └── triangular.py
├── services/            # Core services
│   ├── market_data_service.py
│   └── execution_service.py
├── models/              # Data models
│   └── types.py
├── config/              # Configuration
│   └── default_config.py
├── orchestrator.py      # Main orchestrator
└── main.py              # Entry point
```

## 🚀 Features

### Arbitrage Types Supported

1. **Cross-Exchange Arbitrage**
   - Spatial arbitrage across different exchanges
   - Real-time price comparison
   - Automatic execution on price discrepancies
   - Sub-second detection latency

2. **Statistical Arbitrage**
   - Pairs trading with cointegration analysis
   - Mean reversion strategies
   - Z-score based entry/exit signals
   - Dynamic hedge ratio calculation
   - Bollinger Bands for individual securities

3. **Triangular Arbitrage**
   - Currency/crypto triangle detection
   - Multi-step execution planning
   - Bi-directional path analysis
   - Automated profit calculation

### Key Capabilities

- **Real-time Market Data Processing**: Sub-second data updates from multiple exchanges
- **Multi-Market Support**: Crypto, Forex, Stocks, Commodities, Options, Futures
- **Risk Management**:
  - Position size limits
  - Daily loss limits
  - Total exposure monitoring
  - Risk score evaluation
- **Performance Tracking**:
  - Detection latency monitoring
  - Execution latency tracking
  - Profit/loss analytics
  - Success rate metrics
- **Async Architecture**: High-performance async/await pattern
- **Extensible Design**: Easy to add new agents and strategies

## 📊 Performance Metrics

The system tracks comprehensive metrics:

- **Detection Metrics**:
  - Total opportunities detected
  - Viable opportunities (passing filters)
  - Average detection latency
  - Confidence scores

- **Execution Metrics**:
  - Total trades executed
  - Success/failure rates
  - Average execution latency
  - Slippage tracking

- **Financial Metrics**:
  - Total profit/loss
  - Profit per trade
  - Sharpe ratio (planned)
  - Maximum drawdown (planned)

- **Risk Metrics**:
  - Current exposure
  - Daily P&L
  - Position utilization
  - Risk score distribution

## 🔧 Configuration

### Default Configuration

The system comes with sensible defaults in `config/default_config.py`:

```python
config = {
    "market_data": {
        "update_interval_ms": 1000,  # 1 second updates
    },
    "exchanges": {
        "binance": ["BTC/USDT", "ETH/USDT", ...],
        "coinbase": ["BTC/USD", "ETH/USD", ...],
        "kraken": ["BTC/USD", "ETH/USD", ...]
    },
    "agents": {
        "risk_manager": {
            "max_position_size": "10000",
            "max_daily_loss": "1000",
            "max_total_exposure": "50000"
        },
        "cross_exchange": {
            "min_spread_threshold": "0.001",  # 0.1%
            "min_profit_threshold": "0.002"   # 0.2%
        },
        # ... more agent configs
    }
}
```

### Custom Configuration

You can override defaults:

```python
from arbitrage_trader import ArbitrageOrchestrator, get_config

custom_config = {
    "agents": {
        "cross_exchange": {
            "min_profit_threshold": "0.005"  # 0.5%
        }
    }
}

config = get_config(custom_config)
orchestrator = ArbitrageOrchestrator(config)
```

## 💻 Usage

### Running the System

```bash
python arbitrage_trader/main.py
```

### Programmatic Usage

```python
import asyncio
from arbitrage_trader import ArbitrageOrchestrator, get_config

async def main():
    # Create orchestrator with config
    config = get_config()
    orchestrator = ArbitrageOrchestrator(config)

    # Initialize
    await orchestrator.initialize()

    # Start trading
    await orchestrator.start()

    # Get status
    status = orchestrator.get_status()
    print(f"Active agents: {len(status['agents'])}")

    # Get performance metrics
    metrics = orchestrator.get_performance_metrics()
    print(f"Net profit: ${metrics.net_profit}")

    # Stop
    await orchestrator.stop()

asyncio.run(main())
```

### Using Individual Agents

```python
from arbitrage_trader.agents import CrossExchangeAgent
from arbitrage_trader.models.types import MarketData, MarketType
from decimal import Decimal
from datetime import datetime

# Create agent
agent = CrossExchangeAgent(config={
    "min_spread_threshold": "0.001"
})

# Start agent
await agent.start()

# Feed market data
market_data = [
    MarketData(
        symbol="BTC/USD",
        exchange="binance",
        market_type=MarketType.CRYPTO,
        bid_price=Decimal("50000"),
        ask_price=Decimal("50010"),
        bid_volume=Decimal("10"),
        ask_volume=Decimal("10"),
        timestamp=datetime.now()
    ),
    # ... more market data
]

# Detect opportunities
opportunities = await agent.process_market_data(market_data)

for opp in opportunities:
    print(f"Found opportunity: {opp.symbol}")
    print(f"Expected profit: {opp.expected_profit_percentage}%")
```

## 🔬 Research-Based Implementation

This system is built on research from:

- Real-time arbitrage detection systems (ArbiSim - sub-50 microsecond detection)
- Multi-agent reinforcement learning for HFT
- Statistical arbitrage methodologies
- Cross-exchange latency arbitrage strategies
- Hierarchical multi-agent systems (HMARL)

## 📈 Arbitrage Strategies Explained

### Cross-Exchange Arbitrage

Exploits price differences for the same asset across different exchanges:

```
Exchange A: BTC/USD = $50,000 (ask)
Exchange B: BTC/USD = $50,200 (bid)

Action: Buy on A, Sell on B
Profit: $200 - fees
```

### Statistical Arbitrage (Pairs Trading)

Trades on statistical relationships between correlated assets:

```
Stock A and Stock B historically move together
Currently: Spread is 2.5 standard deviations above mean

Action: Short A, Long B (expecting reversion to mean)
Exit: When spread returns to mean
```

### Triangular Arbitrage

Exploits pricing inefficiencies in currency/crypto triangles:

```
BTC/USD = $50,000
ETH/USD = $3,000
BTC/ETH = 16.8

Path: USD → BTC → ETH → USD
If final USD > initial USD → Profit!
```

## 🛡️ Risk Management

The system implements comprehensive risk controls:

1. **Position Limits**: Maximum size per trade
2. **Exposure Limits**: Total capital at risk
3. **Daily Loss Limits**: Stop trading if daily loss exceeds threshold
4. **Risk Score Filtering**: Only execute low-risk opportunities
5. **Confidence Thresholds**: Minimum confidence requirements

## 🔄 Workflow

1. **Market Data Collection**: Continuous streaming from exchanges
2. **Opportunity Detection**: Agents analyze data in parallel
3. **Risk Evaluation**: Risk manager validates opportunities
4. **Execution**: Automated trade execution
5. **Monitoring**: Real-time P&L and position tracking
6. **Reporting**: Comprehensive performance analytics

## 🎓 Learning Resources

Key concepts used in this system:

- **Cointegration**: Statistical relationship for pairs trading
- **Z-score**: Standard deviation measure for entry/exit
- **Hedge Ratio**: Position sizing in pairs trading
- **Latency Arbitrage**: Speed-based trading advantages
- **Mean Reversion**: Tendency for prices to return to average
- **Bollinger Bands**: Volatility-based technical indicator

## ⚠️ Important Notes

### Production Deployment

For production use:

1. **Exchange Integration**: Replace simulated data with real exchange APIs
2. **Order Management**: Implement proper order routing and management
3. **Fee Calculation**: Accurate fee models for each exchange
4. **Slippage Modeling**: Account for realistic market impact
5. **API Rate Limits**: Implement rate limiting and throttling
6. **Error Handling**: Robust error recovery and logging
7. **Monitoring**: Production-grade monitoring and alerting
8. **Backtesting**: Comprehensive historical testing
9. **Paper Trading**: Live testing without real capital

### Disclaimer

This system is for educational and research purposes. Real arbitrage trading involves:
- Significant capital requirements
- Technical infrastructure costs
- Market risks
- Execution risks
- Regulatory considerations

Always test thoroughly in simulation before deploying real capital.

## 🔮 Future Enhancements

Planned features:

- [ ] Options arbitrage detection
- [ ] Index arbitrage strategies
- [ ] Merger arbitrage analysis
- [ ] Machine learning price prediction
- [ ] Reinforcement learning for strategy optimization
- [ ] Advanced backtesting framework
- [ ] Real exchange API integrations
- [ ] Web dashboard for monitoring
- [ ] Alerting system
- [ ] Historical data analysis
- [ ] Strategy optimization tools

## 📝 License

This project is part of the Finance Platform.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional arbitrage strategies
- Exchange integrations
- Performance optimizations
- Risk management enhancements
- Testing and validation

## 📞 Support

For issues or questions, please open an issue in the repository.

---

**Built with Python 3.8+, asyncio, and modern software engineering practices.**
