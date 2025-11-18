"""
Trading Agents API Endpoints

RESTful API for managing and interacting with trading agents
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.trading_agents import (
    agent_registry,
    AgentType,
    SignalType,
    MarketData,
    MeanReversionAgent,
    MomentumAgent,
    StatisticalArbitrageAgent,
    LSTMPredictionAgent,
    ReinforcementLearningAgent,
    PairsTradingAgent,
    VolatilityAdjustedMomentumAgent,
    EnsembleAgent,
    EnsembleMethod
)
from app.trading_agents.models import (
    TradingAgent as TradingAgentModel,
    TradingSignalRecord,
    Trade,
    AgentTypeEnum,
    SignalTypeEnum
)
from pydantic import BaseModel, Field

router = APIRouter()


# Pydantic schemas
class AgentCreate(BaseModel):
    """Schema for creating a new agent"""
    agent_type: str = Field(..., description="Type of agent to create")
    name: str = Field(..., description="Agent name")
    description: Optional[str] = Field(None, description="Agent description")
    config: Dict[str, Any] = Field(default_factory=dict, description="Agent configuration")


class AgentResponse(BaseModel):
    """Schema for agent response"""
    id: int
    agent_id: str
    agent_type: str
    name: str
    description: Optional[str]
    is_active: bool
    is_trained: bool
    total_trades: int
    win_rate: float
    total_pnl: float
    sharpe_ratio: float
    created_at: datetime
    last_signal_at: Optional[datetime]

    class Config:
        from_attributes = True


class MarketDataInput(BaseModel):
    """Schema for market data input"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    additional_data: Dict[str, Any] = Field(default_factory=dict)


class SignalResponse(BaseModel):
    """Schema for trading signal response"""
    signal_type: str
    confidence: float
    symbol: str
    timestamp: datetime
    price: Optional[float]
    quantity: Optional[int]
    reasoning: str
    metadata: Dict[str, Any]


class BacktestRequest(BaseModel):
    """Schema for backtest request"""
    agent_id: str
    symbol: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0


# API Endpoints

@router.post("/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_create: AgentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create a new trading agent

    Supported agent types:
    - mean_reversion
    - momentum
    - statistical_arbitrage
    - lstm_prediction
    - reinforcement_learning
    - pairs_trading
    - volatility_adjusted
    - ensemble
    """
    # Map agent type to class
    agent_classes = {
        "mean_reversion": MeanReversionAgent,
        "momentum": MomentumAgent,
        "statistical_arbitrage": StatisticalArbitrageAgent,
        "lstm_prediction": LSTMPredictionAgent,
        "reinforcement_learning": ReinforcementLearningAgent,
        "pairs_trading": PairsTradingAgent,
        "volatility_adjusted": VolatilityAdjustedMomentumAgent,
    }

    if agent_create.agent_type not in agent_classes and agent_create.agent_type != "ensemble":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid agent type: {agent_create.agent_type}"
        )

    # Generate unique agent_id
    agent_id = f"{agent_create.agent_type}_{datetime.utcnow().timestamp()}"

    # Create agent instance
    if agent_create.agent_type == "ensemble":
        # For ensemble, create with all available agents
        agents = [
            cls(f"{name}_sub_{agent_id}", **agent_create.config.get(name, {}))
            for name, cls in agent_classes.items()
        ]
        agent_instance = EnsembleAgent(
            agent_id,
            agents,
            ensemble_method=agent_create.config.get("ensemble_method", EnsembleMethod.CONFIDENCE_WEIGHTED),
            config=agent_create.config
        )
    else:
        agent_class = agent_classes[agent_create.agent_type]
        agent_instance = agent_class(agent_id, **agent_create.config)

    # Register agent
    agent_registry.register(agent_instance)

    # Save to database
    db_agent = TradingAgentModel(
        agent_id=agent_id,
        agent_type=AgentTypeEnum[agent_create.agent_type.upper()],
        name=agent_create.name,
        description=agent_create.description,
        config=agent_create.config,
        is_active=False,
        is_trained=False
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    return db_agent


@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    agent_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    List all trading agents with optional filters
    """
    query = db.query(TradingAgentModel)

    if agent_type:
        query = query.filter(TradingAgentModel.agent_type == AgentTypeEnum[agent_type.upper()])

    if is_active is not None:
        query = query.filter(TradingAgentModel.is_active == is_active)

    agents = query.offset(skip).limit(limit).all()
    return agents


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get a specific agent by ID
    """
    agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    return agent


@router.post("/agents/{agent_id}/start")
async def start_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db)
) -> Dict[str, Any]:
    """
    Start an agent
    """
    # Get agent from registry
    agent_instance = agent_registry.get_agent(agent_id)

    if not agent_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found in registry"
        )

    # Start agent
    agent_instance.start()

    # Update database
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if db_agent:
        db_agent.is_active = True
        db_agent.updated_at = datetime.utcnow()
        db.commit()

    return {"message": f"Agent {agent_id} started", "status": "active"}


@router.post("/agents/{agent_id}/stop")
async def stop_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db)
) -> Dict[str, Any]:
    """
    Stop an agent
    """
    agent_instance = agent_registry.get_agent(agent_id)

    if not agent_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    agent_instance.stop()

    # Update database
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if db_agent:
        db_agent.is_active = False
        db_agent.updated_at = datetime.utcnow()
        db.commit()

    return {"message": f"Agent {agent_id} stopped", "status": "inactive"}


@router.post("/agents/{agent_id}/analyze", response_model=SignalResponse)
async def analyze_market(
    agent_id: str,
    market_data: List[MarketDataInput],
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Analyze market data and generate trading signal
    """
    agent_instance = agent_registry.get_agent(agent_id)

    if not agent_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    # Convert input to MarketData objects
    market_data_objs = [
        MarketData(
            symbol=md.symbol,
            timestamp=md.timestamp,
            open=md.open,
            high=md.high,
            low=md.low,
            close=md.close,
            volume=md.volume,
            additional_data=md.additional_data
        )
        for md in market_data
    ]

    # Generate signal
    signal = agent_instance.analyze(market_data_objs)

    # Save signal to database
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if db_agent:
        signal_record = TradingSignalRecord(
            agent_id=db_agent.id,
            signal_type=SignalTypeEnum[signal.signal_type.value.upper()],
            confidence=signal.confidence,
            symbol=signal.symbol,
            price=signal.price,
            quantity=signal.quantity,
            reasoning=signal.reasoning,
            metadata=signal.metadata
        )
        db.add(signal_record)

        db_agent.last_signal_at = datetime.utcnow()
        db.commit()

    return SignalResponse(
        signal_type=signal.signal_type.value,
        confidence=signal.confidence,
        symbol=signal.symbol,
        timestamp=signal.timestamp,
        price=signal.price,
        quantity=signal.quantity,
        reasoning=signal.reasoning,
        metadata=signal.metadata
    )


@router.get("/agents/{agent_id}/signals", response_model=List[Dict[str, Any]])
async def get_agent_signals(
    agent_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get signal history for an agent
    """
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    signals = db.query(TradingSignalRecord).filter(
        TradingSignalRecord.agent_id == db_agent.id
    ).order_by(
        TradingSignalRecord.created_at.desc()
    ).offset(skip).limit(limit).all()

    return [
        {
            "id": s.id,
            "signal_type": s.signal_type.value,
            "confidence": s.confidence,
            "symbol": s.symbol,
            "price": s.price,
            "reasoning": s.reasoning,
            "created_at": s.created_at,
            "metadata": s.metadata
        }
        for s in signals
    ]


@router.get("/agents/{agent_id}/performance")
async def get_agent_performance(
    agent_id: str,
    db: Session = Depends(deps.get_db)
) -> Dict[str, Any]:
    """
    Get performance metrics for an agent
    """
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    return {
        "agent_id": db_agent.agent_id,
        "agent_type": db_agent.agent_type.value,
        "total_trades": db_agent.total_trades,
        "winning_trades": db_agent.winning_trades,
        "losing_trades": db_agent.losing_trades,
        "win_rate": db_agent.win_rate,
        "total_pnl": db_agent.total_pnl,
        "sharpe_ratio": db_agent.sharpe_ratio,
        "max_drawdown": db_agent.max_drawdown,
        "last_signal_at": db_agent.last_signal_at
    }


@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db)
) -> Dict[str, Any]:
    """
    Delete an agent
    """
    db_agent = db.query(TradingAgentModel).filter(
        TradingAgentModel.agent_id == agent_id
    ).first()

    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )

    # Unregister from agent registry
    agent_registry.unregister(agent_id)

    # Delete from database
    db.delete(db_agent)
    db.commit()

    return {"message": f"Agent {agent_id} deleted"}


@router.get("/status")
async def get_system_status() -> Dict[str, Any]:
    """
    Get overall trading system status
    """
    all_agents = agent_registry.get_all_agents()
    active_agents = agent_registry.get_active_agents()

    return {
        "total_agents": len(all_agents),
        "active_agents": len(active_agents),
        "agent_types": {
            agent_type.value: len(agent_registry.get_agents_by_type(agent_type))
            for agent_type in AgentType
        },
        "status": "operational"
    }
