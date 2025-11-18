# Trading Agents - File Reference Guide

## Critical Backend Files for Trading Agent Integration

### Core Architecture Files
| File Path | Purpose | Lines | Status |
|-----------|---------|-------|--------|
| `/backend/app/main.py` | FastAPI entry point with lifecycle management | 270 | Production |
| `/backend/app/config.py` | Configuration & environment management | - | Production |
| `/backend/app/api/router.py` | Main API router aggregator | 80 | Production |
| `/backend/app/core/database.py` | PostgreSQL connection & session management | 274 | Production |
| `/backend/app/core/security.py` | Authentication & security utilities | - | Production |

### Models (Database Schemas)
| File Path | Table Name | Purpose | Status |
|-----------|-----------|---------|--------|
| `/backend/app/models/__init__.py` | - | Model exports | Production |
| `/backend/app/models/fund.py` | funds | PE fund data | Production |
| `/backend/app/models/company.py` | portfolio_companies | Company info | Production |
| `/backend/app/models/financial_metric.py` | financial_metrics | Time-series financials | Production |
| `/backend/app/models/company_kpi.py` | company_kpis | KPI tracking | Production |
| `/backend/app/models/market_data.py` | market_data | Cached market data | Production |
| `/backend/app/models/audit_log.py` | audit_logs | Activity tracking | Production |
| `/backend/app/models/valuation.py` | valuations | Valuation data | Production |

### Services Layer (Business Logic)
| File Path | Purpose | Integration Points |
|-----------|---------|-------------------|
| `/backend/app/services/market_data_service.py` | Orchestrates market data fetching & caching | Aggregator, Repository, DB |
| `/backend/app/services/market_data_aggregator.py` | Combines multiple data sources | CoStar, Zillow, Census, WalkScore |
| `/backend/app/services/costar_service.py` | CoStar API integration | Real estate market data |
| `/backend/app/services/zillow_service.py` | Zillow/Redfin integration | Property valuations |
| `/backend/app/services/census_service.py` | Census Bureau integration | Demographics |
| `/backend/app/services/walkscore_service.py` | Walk Score integration | Walkability metrics |

### Repository Layer (Data Access)
| File Path | Purpose | Database |
|-----------|---------|----------|
| `/backend/app/repositories/market_data_repository.py` | Market data CRUD operations | market_data table |

### API Endpoints
| File Path | Endpoints | Prefix | Status |
|-----------|-----------|--------|--------|
| `/backend/app/api/v1/endpoints/market_data.py` | comprehensive, investment-summary | /market-data | Production |
| `/backend/app/api/v1/endpoints/companies.py` | list, create, get, update, delete | /companies | Production |
| `/backend/app/api/v1/endpoints/funds.py` | list, create, get, update | /funds | Production |
| `/backend/app/api/v1/endpoints/finance_models.py` | dcf, lbo, merger | /finance | Production |
| `/backend/app/api/v1/endpoints/real_estate_tools.py` | Various calculators | /real-estate | Production |
| `/backend/app/api/v1/endpoints/health.py` | Health checks | /health | Production |

### Scripts & Modeling Logic
| File Path | Type | Purpose |
|-----------|------|---------|
| `/backend/app/scripts/corporate_finance/dcf_model.py` | Model | DCF valuation |
| `/backend/app/scripts/corporate_finance/lbo_model.py` | Model | Leveraged buyout |
| `/backend/app/scripts/corporate_finance/comparative_analysis.py` | Analysis | Comparable analysis |
| `/backend/app/scripts/real_estate/base.py` | Base Class | Real estate modeling base |
| `/backend/app/scripts/real_estate/single_family_rental_cli.py` | Model | SFR investment |
| `/backend/app/scripts/real_estate/fix_and_flip_cli.py` | Model | Fix & flip analysis |
| `/backend/app/scripts/real_estate/hotel_model_cli.py` | Model | Hotel investment |

---

## Where to Add Trading Agent Code

### Recommended New Directories

```
backend/app/agents/                     # NEW - Agent framework
  ├── __init__.py
  ├── base_agent.py                    # Abstract base class
  ├── agent_registry.py                # Agent lifecycle
  ├── agent_state.py                   # State management
  ├── types.py                         # Type definitions
  ├── market_analysis_agent.py         # Market data analysis
  ├── trading_strategy_agent.py        # Strategy execution
  └── risk_management_agent.py         # Risk controls

backend/app/trading/                    # NEW - Trading logic
  ├── strategies/
  │   ├── __init__.py
  │   ├── base_strategy.py             # Strategy interface
  │   ├── momentum_strategy.py         # Example: momentum-based
  │   ├── mean_reversion_strategy.py   # Example: mean reversion
  │   └── arbitrage_strategy.py        # Example: arbitrage
  ├── execution/
  │   ├── __init__.py
  │   ├── order_manager.py             # Order creation/tracking
  │   ├── position_tracker.py          # Position management
  │   └── trade_journal.py             # Trade logging
  ├── risk/
  │   ├── __init__.py
  │   ├── portfolio_risk.py            # Risk calculation
  │   ├── position_limits.py           # Position constraints
  │   └── drawdown_monitor.py          # Drawdown tracking
  └── models/
      ├── __init__.py
      ├── order.py                     # Order models
      ├── position.py                  # Position models
      └── trade.py                     # Trade records

backend/app/models/trading/             # NEW - Trading DB tables
  ├── __init__.py
  ├── agent.py                         # Agent instances
  ├── strategy.py                      # Strategy versions
  ├── order.py                         # Orders
  ├── position.py                      # Open positions
  ├── trade.py                         # Completed trades
  └── trade_signal.py                  # Market signals

backend/app/api/v1/endpoints/agents/    # NEW - Agent API
  ├── __init__.py
  ├── agents.py                        # Agent lifecycle
  ├── strategies.py                    # Strategy management
  ├── orders.py                        # Order endpoints
  ├── positions.py                     # Position endpoints
  └── performance.py                   # Performance analytics
```

---

## Integration Points in Existing Code

### Using Market Data Service
```python
# Existing service already aggregates data
from app.services.market_data_service import MarketDataService

service = MarketDataService()
market_data = await service.get_comprehensive_market_data(
    db=db,
    address="123 Main St",
    city="New York",
    state="NY",
    zip_code="10001",
    property_type="Multifamily"
)
```

### Accessing Database
```python
# Dependency injection pattern already in place
from app.api.deps import get_db
from sqlalchemy.orm import Session

async def my_agent_endpoint(db: Session = Depends(get_db)):
    # Use db to query existing tables and create new agent tables
    pass
```

### Adding New Models
```python
# Follow existing SQLAlchemy pattern
from app.models.database import Base, TimestampMixin, UUIDMixin
from sqlalchemy import Column, String, Integer, Float

class TradingAgent(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "trading_agents"
    
    agent_name = Column(String(255), unique=True)
    strategy_type = Column(String(100))
    status = Column(String(20))
```

### Creating New Endpoints
```python
# Follow existing endpoint pattern
from fastapi import APIRouter, Depends
from app.api.deps import get_db

router = APIRouter()

@router.get("/agents")
async def list_agents(db: Session = Depends(get_db)):
    # Endpoint logic
    pass
```

---

## Current Data Flow Useful for Trading Agents

### For Real-time Market Monitoring
```
1. MarketDataAggregator: Fetches from multiple APIs
2. MarketDataService: Orchestrates + caches
3. MarketDataRepository: Persists to DB
4. API Endpoint: Serves to consumers
5. Database: 24-hour cache

Agent can:
- Subscribe to market_data updates
- Trigger on threshold crossings
- Aggregate signals from multiple sources
```

### For Historical Analysis
```
1. PostgreSQL: Stores all financial_metrics
2. Time-series: Query by date ranges
3. Aggregation: Portfolio-level metrics
4. Repository: Fast access to cached data

Agent can:
- Analyze historical patterns
- Backtest strategies
- Track performance
```

---

## Dependencies Already in Requirements

Check `/backend/requirements.txt` for:
- FastAPI (already installed)
- SQLAlchemy (already installed)
- Pydantic (already installed)
- numpy (check if needed)
- pandas (likely needed for time-series)
- scikit-learn (if ML strategies needed)

---

## File Sizes Reference

| Directory | File Count | Total Size |
|-----------|-----------|-----------|
| `/backend/app/models/` | 11 files | ~15 KB |
| `/backend/app/services/` | 6 files | ~25 KB |
| `/backend/app/api/v1/endpoints/` | 7 files | ~45 KB |
| `/backend/app/scripts/` | 13 files | ~150 KB |

---

## Important Notes

1. **No Trading Code Currently Exists**: The platform is 100% real estate/portfolio analysis
2. **Branch is Empty**: `claude/add-trading-agents-01QmQ58AhLjFKJ44LhKY8Fx3` has zero custom commits
3. **Good Integration Point**: Market data pipeline can feed agents
4. **Database Ready**: Schema can be extended with trading tables
5. **API Structure Ready**: Router pattern established, easy to add agent endpoints

---

