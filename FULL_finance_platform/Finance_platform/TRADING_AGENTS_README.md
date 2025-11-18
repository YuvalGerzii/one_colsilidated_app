# Trading Agents System

## Overview

A comprehensive, research-based algorithmic trading system with 8 different trading agents implementing state-of-the-art strategies from academic literature (2020-2025).

## Research-Based Agents

### 1. Mean Reversion Agent
**Strategy**: Statistical arbitrage using z-score analysis
**Research**:
- Statistical Arbitrage (SSRN)
- Mean Reversion Strategies (QuantInsti, 2024)

**Key Features**:
- Z-score calculation for overbought/oversold detection
- Configurable entry/exit thresholds
- Historical mean and standard deviation tracking

**Use Case**: Best for range-bound markets and assets that tend to revert to historical averages

### 2. Momentum Trading Agent
**Strategy**: Technical analysis using multiple indicators
**Research**:
- Dynamically Combining Mean Reversion and Momentum (Hudson & Thames)
- Technical Trading Rules (RoboForex, 2024)

**Key Features**:
- Moving average crossovers (SMA/EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Composite signal aggregation

**Use Case**: Trending markets with clear directional moves

### 3. Statistical Arbitrage Agent
**Strategy**: Combined mean reversion + momentum using decomposition
**Research**:
- Diversified Statistical Arbitrage (SSRN, James Velissaris)
- Advanced Statistical Arbitrage with RL (arXiv, 2024)

**Key Features**:
- Return decomposition (systematic vs idiosyncratic)
- Mean reversion on idiosyncratic components
- Momentum on systematic components
- PCA-ready architecture

**Use Case**: Complex markets requiring multi-strategy approach

### 4. LSTM Price Prediction Agent
**Strategy**: Deep learning neural networks for price forecasting
**Research**:
- Deep Learning for Algorithmic Trading (ScienceDirect, 2025)
- LSTM Networks for Stock Price Prediction (ACM)

**Key Features**:
- Simplified LSTM implementation (production: use TensorFlow/PyTorch)
- Multi-feature engineering
- Confidence-based prediction
- Normalization and preprocessing

**Use Case**: Markets with complex non-linear patterns

**Note**: Current implementation is lightweight. For production, upgrade to TensorFlow/PyTorch with GPU acceleration.

### 5. Reinforcement Learning Agent
**Strategy**: Deep Q-Network (DQN) with experience replay
**Research**:
- FinRL: Deep RL Library (arXiv, 2020)
- Multi-Agent DRL for Trading (ScienceDirect, 2022)
- Deep RL Strategies in Finance (arXiv, 2024)

**Key Features**:
- Deep Q-Network with target network
- Experience replay buffer
- Epsilon-greedy exploration
- Adaptive learning from market feedback
- State features: momentum, volatility, RSI, position, PnL

**Use Case**: Adaptive trading in dynamic market conditions

**Note**: Simplified implementation. Production version should use stable-baselines3 or FinRL library.

### 6. Pairs Trading Agent
**Strategy**: Correlation and cointegration-based arbitrage
**Research**:
- Pairs Trading: A Cointegration Approach (SSRN)
- Advanced Statistical Arbitrage (arXiv, 2024)

**Key Features**:
- Cointegration testing (ADF test)
- Hedge ratio calculation
- Mean reversion half-life estimation
- Spread z-score analysis
- Pair quality metrics

**Use Case**: Trading related assets (e.g., stocks in same sector, correlated commodities)

**Note**: Requires two asset data streams

### 7. Volatility-Adjusted Momentum Agent
**Strategy**: Momentum with volatility-based position sizing
**Research**:
- Volatility-Adjusted Momentum Strategies (Scientific Reports, 2025)
- Risk-Adjusted Returns in Algorithmic Trading

**Key Features**:
- Volatility targeting for position sizing
- ATR (Average True Range) calculation
- Sharpe ratio optimization
- Dynamic exposure adjustment
- Risk-adjusted confidence scoring

**Use Case**: Trending markets with varying volatility regimes

### 8. Ensemble Agent (Multi-Agent Orchestrator)
**Strategy**: Combines multiple agents using weighted voting
**Research**:
- Multi-Agent Deep RL (ScienceDirect, 2022)
- Ensemble Methods in Algorithmic Trading (ACM, 2024)
- Collective Intelligence for Trading (Frontiers in AI, 2025)

**Key Features**:
- Multiple aggregation methods:
  - Majority voting
  - Weighted average
  - Confidence-weighted
  - Performance-weighted
  - Adaptive weighting
- Individual agent performance tracking
- Agent ranking by accuracy
- Configurable agreement thresholds

**Use Case**: Robust trading in all market conditions by leveraging collective intelligence

## System Architecture

```
trading_agents/
├── base_agent.py              # Base classes and interfaces
├── backtesting.py             # Backtesting framework
├── __init__.py
├── strategies/
│   ├── mean_reversion_agent.py
│   ├── momentum_agent.py
│   ├── statistical_arbitrage_agent.py
│   ├── lstm_prediction_agent.py
│   ├── reinforcement_learning_agent.py
│   ├── pairs_trading_agent.py
│   ├── volatility_adjusted_momentum_agent.py
│   ├── ensemble_agent.py
│   └── __init__.py
└── models/
    ├── agent_models.py         # Database models
    └── __init__.py
```

## Database Schema

### TradingAgent
- Agent configuration and metadata
- Performance metrics (win rate, PnL, Sharpe ratio)
- Status tracking (active, trained)

### TradingSignalRecord
- All signals generated by agents
- Signal details (type, confidence, price)
- Outcome tracking (executed, profitable)

### Trade
- Executed trade records
- Entry/exit prices and times
- PnL and risk metrics
- Stop loss / take profit levels

### BacktestResult
- Backtesting performance data
- Equity curves
- Trade history
- Risk-adjusted metrics

### AgentPerformanceSnapshot
- Periodic performance tracking
- Market condition correlation
- Time-series analytics

## API Endpoints

### Agent Management
- `POST /api/v1/trading-agents/agents` - Create new agent
- `GET /api/v1/trading-agents/agents` - List all agents
- `GET /api/v1/trading-agents/agents/{agent_id}` - Get agent details
- `POST /api/v1/trading-agents/agents/{agent_id}/start` - Start agent
- `POST /api/v1/trading-agents/agents/{agent_id}/stop` - Stop agent
- `DELETE /api/v1/trading-agents/agents/{agent_id}` - Delete agent

### Trading Operations
- `POST /api/v1/trading-agents/agents/{agent_id}/analyze` - Generate signal
- `GET /api/v1/trading-agents/agents/{agent_id}/signals` - Get signal history
- `GET /api/v1/trading-agents/agents/{agent_id}/performance` - Get performance metrics

### System Status
- `GET /api/v1/trading-agents/status` - System overview

## Quick Start

### 1. Create a Mean Reversion Agent

```python
from app.trading_agents import MeanReversionAgent, MarketData

# Create agent
agent = MeanReversionAgent(
    agent_id="mean_rev_001",
    lookback_period=20,
    entry_threshold=2.0,
    exit_threshold=0.5
)

# Prepare market data
market_data = [
    MarketData(
        symbol="AAPL",
        timestamp=datetime.now(),
        open=150.0,
        high=152.0,
        low=149.0,
        close=151.0,
        volume=1000000
    ),
    # ... more data
]

# Train agent (optional)
agent.train(market_data)

# Start agent
agent.start()

# Generate signal
signal = agent.analyze(market_data)
print(f"Signal: {signal.signal_type.value}, Confidence: {signal.confidence}")
print(f"Reasoning: {signal.reasoning}")
```

### 2. Create an Ensemble Agent

```python
from app.trading_agents import (
    EnsembleAgent,
    MeanReversionAgent,
    MomentumAgent,
    LSTMPredictionAgent,
    EnsembleMethod
)

# Create individual agents
agents = [
    MeanReversionAgent("mr_001"),
    MomentumAgent("mom_001"),
    LSTMPredictionAgent("lstm_001")
]

# Create ensemble
ensemble = EnsembleAgent(
    agent_id="ensemble_001",
    agents=agents,
    ensemble_method=EnsembleMethod.CONFIDENCE_WEIGHTED,
    min_agreement=0.5
)

# Train all agents
ensemble.train(market_data)

# Generate consensus signal
signal = ensemble.analyze(market_data)
```

### 3. Backtest an Agent

```python
from app.trading_agents.backtesting import Backtester, BacktestConfig, print_backtest_results

# Configure backtest
config = BacktestConfig(
    initial_capital=100000.0,
    commission=0.001,  # 0.1%
    slippage=0.0005,   # 0.05%
    stop_loss_pct=0.05,  # 5% stop loss
    take_profit_pct=0.10  # 10% take profit
)

# Create backtester
backtester = Backtester(config)

# Run backtest
results = backtester.run(
    agent=agent,
    market_data=historical_data,
    train_period=100  # First 100 periods for training
)

# Print results
print_backtest_results(results)
```

### 4. Using the REST API

```bash
# Create agent
curl -X POST http://localhost:8000/api/v1/trading-agents/agents \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "momentum",
    "name": "My Momentum Agent",
    "description": "Testing momentum strategy",
    "config": {
      "short_window": 12,
      "long_window": 26,
      "rsi_period": 14
    }
  }'

# Start agent
curl -X POST http://localhost:8000/api/v1/trading-agents/agents/{agent_id}/start

# Generate signal
curl -X POST http://localhost:8000/api/v1/trading-agents/agents/{agent_id}/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "market_data": [
      {
        "symbol": "AAPL",
        "timestamp": "2025-01-01T10:00:00",
        "open": 150.0,
        "high": 152.0,
        "low": 149.0,
        "close": 151.0,
        "volume": 1000000
      }
    ]
  }'
```

## Configuration Examples

### Mean Reversion Agent
```json
{
  "lookback_period": 20,
  "entry_threshold": 2.0,
  "exit_threshold": 0.5
}
```

### Momentum Agent
```json
{
  "short_window": 12,
  "long_window": 26,
  "rsi_period": 14,
  "rsi_overbought": 70.0,
  "rsi_oversold": 30.0
}
```

### Volatility-Adjusted Momentum Agent
```json
{
  "momentum_lookback": 20,
  "volatility_lookback": 20,
  "vol_target": 0.15,
  "momentum_threshold": 0.02
}
```

### Ensemble Agent
```json
{
  "ensemble_method": "confidence_weighted",
  "min_agreement": 0.5
}
```

## Performance Metrics

All agents track:
- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of profitable trades
- **Total PnL**: Cumulative profit/loss
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Average Trade Duration**: How long positions are held

Backtesting provides additional metrics:
- **Sortino Ratio**: Downside risk-adjusted returns
- **Profit Factor**: Gross profit / Gross loss
- **Recovery Factor**: Net profit / Max drawdown
- **Calmar Ratio**: Annualized return / Max drawdown
- **Volatility**: Annualized standard deviation of returns

## Best Practices

1. **Always Backtest**: Test strategies on historical data before live trading
2. **Use Ensemble Agents**: Combine multiple strategies for robustness
3. **Monitor Performance**: Track metrics and adjust configurations
4. **Risk Management**: Set stop losses and position size limits
5. **Train Regularly**: Retrain ML/RL agents with recent data
6. **Validate Signals**: Check confidence levels before executing
7. **Paper Trade First**: Test in simulation before real money

## Research References

1. **Statistical Arbitrage**
   - Diversified Statistical Arbitrage (SSRN, Velissaris)
   - Advanced Statistical Arbitrage with RL (arXiv, 2024)

2. **Deep Learning**
   - Deep Learning for Algorithmic Trading (ScienceDirect, 2025)
   - Systematic Review of Predictive Models (Applied Science, 2024)

3. **Reinforcement Learning**
   - FinRL: Financial RL Library (arXiv, 2020)
   - Multi-Agent DRL for Trading (ScienceDirect, 2022)
   - Deep RL Strategies in Finance (arXiv, 2024)

4. **General Algorithmic Trading**
   - Algorithmic Trading and AI Review (ResearchGate, 2024)
   - Technology-driven Advancements (ScienceDirect, 2024)
   - Market Impact Studies (Scientific Reports, 2025)

## Production Considerations

### For Production Deployment:

1. **Upgrade ML/DL Agents**:
   - Replace LSTM with TensorFlow/Keras/PyTorch implementation
   - Replace RL with stable-baselines3 or FinRL library
   - Add GPU acceleration

2. **Add Real-Time Features**:
   - WebSocket for live market data
   - Redis for caching and pub/sub
   - Celery for async task processing

3. **Enhance Risk Management**:
   - Real-time portfolio tracking
   - Position limits and exposure controls
   - Circuit breakers for extreme events

4. **Broker Integration**:
   - Connect to actual brokers (Interactive Brokers, Alpaca, etc.)
   - Order management system (OMS)
   - Trade execution optimization

5. **Monitoring & Alerts**:
   - Real-time dashboards
   - Performance alerts
   - System health monitoring

## License

See main project LICENSE file.

## Support

For issues or questions, please open an issue on GitHub.
