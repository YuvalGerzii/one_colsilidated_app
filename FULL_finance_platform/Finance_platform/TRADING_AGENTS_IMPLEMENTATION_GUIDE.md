# Trading Agents - Implementation Starter Guide

## Quick Context

The Finance Platform is a **Portfolio Management System** with NO existing trading agents or algorithmic trading strategies. The `claude/add-trading-agents-01QmQ58AhLjFKJ44LhKY8Fx3` branch is empty and waiting for implementation.

---

## What Needs to Be Built

### 1. Agent Framework
```python
# backend/app/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class TradingAgent(ABC):
    """Abstract base class for trading agents."""
    
    def __init__(self, agent_id: str, name: str, agent_type: str):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type  # 'analyzer', 'executor', 'monitor'
        self.status = 'initialized'
        self.last_execution = None
        self.metrics = {}
    
    @abstractmethod
    async def analyze(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market conditions."""
        pass
    
    @abstractmethod
    async def execute(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute on trading signal."""
        pass
    
    @abstractmethod
    async def report(self) -> Dict[str, Any]:
        """Generate performance report."""
        pass
```

### 2. Market Analysis Agent
```python
# backend/app/agents/market_analysis_agent.py
from app.agents.base_agent import TradingAgent
from app.services.market_data_service import MarketDataService

class MarketAnalysisAgent(TradingAgent):
    """Analyzes market data and generates signals."""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "Market Analyzer", "analyzer")
        self.market_service = MarketDataService()
        self.signals = []
    
    async def analyze(self, market_data: Dict) -> Dict:
        """
        Analyze market data from aggregator.
        
        Uses existing MarketDataService to get:
        - CoStar cap rates and trends
        - Zillow valuations
        - Census demographics
        - Walk Score metrics
        """
        analysis_result = {
            'timestamp': datetime.utcnow().isoformat(),
            'agent_id': self.agent_id,
            'signals': [],
            'metrics': {}
        }
        
        # Example: Analyze cap rate trend
        costar = market_data.get('costar_data', {})
        cap_rate = costar.get('cap_rate')
        market_trend = costar.get('market_trend')
        
        # Generate signal if trend is favorable
        if market_trend == 'positive' and cap_rate and cap_rate > 5.0:
            analysis_result['signals'].append({
                'type': 'BUY_SIGNAL',
                'strength': 'medium',
                'reason': 'Favorable cap rate with positive market trend'
            })
        
        self.signals = analysis_result['signals']
        return analysis_result
    
    async def execute(self, signal: Dict) -> Dict:
        """Not applicable for analyzer agent."""
        return {'status': 'analyzer_only'}
    
    async def report(self) -> Dict:
        """Return analysis metrics."""
        return {
            'agent_id': self.agent_id,
            'signals_generated': len(self.signals),
            'last_execution': self.last_execution
        }
```

### 3. Trading Strategy
```python
# backend/app/trading/strategies/momentum_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, List

class TradingStrategy(ABC):
    """Abstract base class for trading strategies."""
    
    @abstractmethod
    async def evaluate(self, market_data: Dict) -> Dict:
        """Evaluate market conditions for trade signals."""
        pass
    
    @abstractmethod
    def get_signal_strength(self) -> float:
        """Return confidence score 0-1."""
        pass

class MomentumStrategy(TradingStrategy):
    """Buy when market is trending up, sell on reversal."""
    
    def __init__(self, lookback_period: int = 20):
        self.lookback_period = lookback_period
        self.signal_strength = 0.0
        self.positions = []
    
    async def evaluate(self, market_data: Dict) -> Dict:
        """
        Evaluate momentum from market data.
        
        Input: Historical price data (from market_data table)
        Output: Trade signal
        """
        # Example with real estate prices
        costar = market_data.get('costar_data', {})
        zillow = market_data.get('zillow_redfin_data', {}).get('zillow', {})
        
        price_change = zillow.get('price_change_30d', 0)
        cap_rate = costar.get('cap_rate', 0)
        
        signal = {
            'strategy': 'momentum',
            'action': 'HOLD',
            'confidence': 0.0
        }
        
        if price_change > 5.0 and cap_rate > 4.0:
            signal['action'] = 'BUY'
            self.signal_strength = 0.75
            signal['confidence'] = 0.75
        elif price_change < -5.0:
            signal['action'] = 'SELL'
            self.signal_strength = 0.6
            signal['confidence'] = 0.6
        
        return signal
    
    def get_signal_strength(self) -> float:
        return self.signal_strength
```

### 4. Database Models for Trading
```python
# backend/app/models/trading/agent.py
from app.models.database import Base, TimestampMixin, UUIDMixin
from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

class TradingAgent(Base, TimestampMixin, UUIDMixin):
    """Stores trading agent configurations and state."""
    __tablename__ = "trading_agents"
    
    agent_name = Column(String(255), unique=True, nullable=False)
    agent_type = Column(String(50))  # 'analyzer', 'executor', 'monitor'
    strategy_type = Column(String(100))
    status = Column(String(20), default='active')
    is_active = Column(Boolean, default=True)
    config = Column(JSON)  # Store agent configuration
    
    # Performance metrics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    total_return = Column(Float, default=0.0)
    win_rate = Column(Float, default=0.0)

# backend/app/models/trading/order.py
class Order(Base, TimestampMixin, UUIDMixin):
    """Stores all trade orders."""
    __tablename__ = "orders"
    
    agent_id = Column(UUID, ForeignKey("trading_agents.id"))
    order_type = Column(String(20))  # 'BUY', 'SELL'
    symbol = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)
    status = Column(String(20), default='pending')  # pending, filled, cancelled
    filled_at = Column(DateTime, nullable=True)

# backend/app/models/trading/trade.py
class Trade(Base, TimestampMixin, UUIDMixin):
    """Stores completed trades."""
    __tablename__ = "trades"
    
    agent_id = Column(UUID, ForeignKey("trading_agents.id"))
    entry_price = Column(Float)
    exit_price = Column(Float)
    quantity = Column(Integer)
    profit_loss = Column(Float)
    return_pct = Column(Float)
    days_held = Column(Integer)
```

### 5. API Endpoints for Agents
```python
# backend/app/api/v1/endpoints/agents.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.agents.market_analysis_agent import MarketAnalysisAgent

router = APIRouter()

@router.get("/agents")
async def list_agents(db: Session = Depends(get_db)):
    """List all trading agents."""
    # Query from database
    agents = db.query(TradingAgent).filter(TradingAgent.is_active == True).all()
    return {
        "count": len(agents),
        "agents": [agent.to_dict() for agent in agents]
    }

@router.post("/agents")
async def create_agent(
    agent_config: AgentCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new trading agent."""
    agent = TradingAgent(
        agent_name=agent_config.name,
        agent_type=agent_config.type,
        strategy_type=agent_config.strategy,
        config=agent_config.config
    )
    db.add(agent)
    db.commit()
    return {"id": agent.id, "status": "created"}

@router.post("/agents/{agent_id}/run")
async def run_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Execute an agent immediately."""
    agent_config = db.query(TradingAgent).filter(
        TradingAgent.id == agent_id
    ).first()
    
    if not agent_config:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get latest market data
    from app.services.market_data_service import MarketDataService
    market_service = MarketDataService()
    market_data = db.query(MarketData).order_by(
        MarketData.created_at.desc()
    ).first()
    
    # Run analyzer
    analyzer = MarketAnalysisAgent(str(agent_id))
    result = await analyzer.analyze(market_data.to_dict())
    
    return {
        "agent_id": agent_id,
        "execution": result,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/agents/{agent_id}/performance")
async def get_agent_performance(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent performance metrics."""
    agent = db.query(TradingAgent).filter(TradingAgent.id == agent_id).first()
    trades = db.query(Trade).filter(Trade.agent_id == agent_id).all()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    total_profit = sum(t.profit_loss for t in trades)
    
    return {
        "agent_id": agent_id,
        "total_trades": len(trades),
        "total_profit_loss": total_profit,
        "win_rate": agent.win_rate,
        "return_pct": agent.total_return
    }
```

### 6. Integration with Market Data
```python
# Example: How agents consume existing market data

async def agent_market_data_loop(db: Session):
    """Background loop that feeds agents market data."""
    from app.services.market_data_service import MarketDataService
    from app.agents.market_analysis_agent import MarketAnalysisAgent
    
    market_service = MarketDataService()
    
    while True:
        # Fetch latest market data (uses existing aggregator)
        market_data = await market_service.get_comprehensive_market_data(
            db=db,
            address="123 Main St",
            city="New York", 
            state="NY",
            zip_code="10001",
            property_type="Multifamily"
        )
        
        # Create analyzer agent
        analyzer = MarketAnalysisAgent("analyzer_001")
        
        # Run analysis
        analysis = await analyzer.analyze(market_data)
        
        # Check for signals
        for signal in analysis.get('signals', []):
            # Store signal in database
            signal_record = TradeSignal(
                agent_id="analyzer_001",
                signal_type=signal['type'],
                strength=signal['strength']
            )
            db.add(signal_record)
            db.commit()
        
        # Wait before next check
        await asyncio.sleep(300)  # 5 minutes
```

---

## Directory Structure to Create

```bash
# Create agent directories
mkdir -p backend/app/agents
mkdir -p backend/app/trading/strategies
mkdir -p backend/app/trading/execution
mkdir -p backend/app/trading/risk
mkdir -p backend/app/models/trading
mkdir -p backend/app/api/v1/endpoints/agents

# Create __init__.py files
touch backend/app/agents/__init__.py
touch backend/app/trading/__init__.py
touch backend/app/trading/strategies/__init__.py
touch backend/app/models/trading/__init__.py
```

---

## Integration Checklist

- [ ] Create agent base classes
- [ ] Implement market analysis agent
- [ ] Create trading strategy interface
- [ ] Implement first strategy (momentum)
- [ ] Create database models for agents/trades
- [ ] Add agent API endpoints
- [ ] Add market data integration
- [ ] Create agent registry
- [ ] Add background task runner
- [ ] Create monitoring dashboard
- [ ] Add performance tracking
- [ ] Implement risk management
- [ ] Add order execution (simulation)
- [ ] Create backtesting framework
- [ ] Write unit tests

---

## Running the First Agent

```python
# In a Python script or FastAPI endpoint
from app.agents.market_analysis_agent import MarketAnalysisAgent
from app.services.market_data_service import MarketDataService

async def test_agent():
    service = MarketDataService()
    
    # Get market data (uses existing service)
    market_data = await service.get_comprehensive_market_data(
        db=db,
        address="123 Main St",
        city="San Francisco",
        state="CA",
        zip_code="94103",
        property_type="Multifamily"
    )
    
    # Create and run agent
    agent = MarketAnalysisAgent("agent_001")
    result = await agent.analyze(market_data)
    
    print(f"Signals: {result['signals']}")
```

---

## Next Steps

1. **Implement Phase 1**: Create agent framework and base classes
2. **Test with Market Data**: Feed agents existing market data
3. **Build First Strategy**: Implement momentum-based strategy
4. **Database Models**: Add trading tables
5. **API Endpoints**: Create agent management endpoints
6. **Integration Test**: End-to-end test with real market data

