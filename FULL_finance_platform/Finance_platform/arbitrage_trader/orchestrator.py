"""
Orchestrator for the multi-agent arbitrage trading system.
Coordinates all agents, services, and manages the overall workflow.
"""
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal

from .agents.base_agent import BaseAgent
from .agents.cross_exchange_agent import CrossExchangeAgent
from .agents.statistical_agent import StatisticalArbitrageAgent
from .agents.triangular_agent import TriangularArbitrageAgent
from .agents.risk_manager_agent import RiskManagerAgent

from .services.market_data_service import MarketDataService
from .services.execution_service import ExecutionService

from .models.types import (
    ArbitrageOpportunity,
    MarketData,
    PerformanceMetrics,
    Trade
)


class ArbitrageOrchestrator:
    """Orchestrator for the multi-agent arbitrage system."""

    def __init__(self, config: dict = None):
        """
        Initialize the orchestrator.

        Args:
            config: System configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Services
        self.market_data_service: Optional[MarketDataService] = None
        self.execution_service: Optional[ExecutionService] = None

        # Agents
        self.agents: Dict[str, BaseAgent] = {}
        self.risk_manager: Optional[RiskManagerAgent] = None

        # State
        self.is_running = False
        self.detected_opportunities: List[ArbitrageOpportunity] = []
        self.executed_opportunities: List[ArbitrageOpportunity] = []

        # Performance tracking
        self.total_opportunities = 0
        self.viable_opportunities = 0
        self.executed_trades = 0
        self.total_detection_latency = 0
        self.total_execution_latency = 0

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = self.config.get("log_level", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    async def initialize(self):
        """Initialize all components of the system."""
        self.logger.info("Initializing arbitrage trading system...")

        # Initialize market data service
        market_config = self.config.get("market_data", {})
        self.market_data_service = MarketDataService(config=market_config)

        # Add exchanges to monitor
        exchanges_config = self.config.get("exchanges", {})
        for exchange, symbols in exchanges_config.items():
            self.market_data_service.add_exchange(exchange, symbols)

        # Initialize execution service
        execution_config = self.config.get("execution", {})
        self.execution_service = ExecutionService(config=execution_config)

        # Initialize agents
        await self._initialize_agents()

        # Subscribe agents to market data
        self.market_data_service.subscribe(self._on_market_data)

        self.logger.info("Arbitrage trading system initialized successfully")

    async def _initialize_agents(self):
        """Initialize all trading agents."""
        agents_config = self.config.get("agents", {})

        # Initialize risk manager
        risk_config = agents_config.get("risk_manager", {})
        self.risk_manager = RiskManagerAgent(config=risk_config)
        self.agents["risk_manager"] = self.risk_manager

        # Initialize cross-exchange agent
        if agents_config.get("cross_exchange", {}).get("enabled", True):
            cross_config = agents_config.get("cross_exchange", {})
            agent = CrossExchangeAgent(config=cross_config)
            self.agents["cross_exchange"] = agent

        # Initialize statistical arbitrage agent
        if agents_config.get("statistical", {}).get("enabled", True):
            stat_config = agents_config.get("statistical", {})
            agent = StatisticalArbitrageAgent(config=stat_config)
            self.agents["statistical"] = agent

        # Initialize triangular arbitrage agent
        if agents_config.get("triangular", {}).get("enabled", True):
            tri_config = agents_config.get("triangular", {})
            agent = TriangularArbitrageAgent(config=tri_config)
            self.agents["triangular"] = agent

        self.logger.info(f"Initialized {len(self.agents)} agents")

    async def start(self):
        """Start the orchestrator and all components."""
        if self.is_running:
            self.logger.warning("Orchestrator is already running")
            return

        self.logger.info("Starting arbitrage trading system...")

        self.is_running = True

        # Start services
        await self.market_data_service.start()
        await self.execution_service.start()

        # Start all agents
        for agent_id, agent in self.agents.items():
            await agent.start()
            self.logger.info(f"Started agent: {agent_id}")

        self.logger.info("Arbitrage trading system started successfully")

    async def stop(self):
        """Stop the orchestrator and all components."""
        if not self.is_running:
            self.logger.warning("Orchestrator is not running")
            return

        self.logger.info("Stopping arbitrage trading system...")

        self.is_running = False

        # Stop all agents
        for agent_id, agent in self.agents.items():
            await agent.stop()
            self.logger.info(f"Stopped agent: {agent_id}")

        # Stop services
        await self.market_data_service.stop()
        await self.execution_service.stop()

        self.logger.info("Arbitrage trading system stopped successfully")

    async def _on_market_data(self, market_data: List[MarketData]):
        """
        Handle incoming market data.

        Args:
            market_data: List of market data updates
        """
        if not self.is_running:
            return

        # Process market data with all agents (except risk manager)
        all_opportunities = []

        for agent_id, agent in self.agents.items():
            if agent_id == "risk_manager":
                # Risk manager monitors but doesn't detect opportunities
                await agent.process_market_data(market_data)
                continue

            try:
                opportunities = await agent.process_market_data(market_data)
                all_opportunities.extend(opportunities)

            except Exception as e:
                self.logger.error(
                    f"Error processing data with agent {agent_id}: {e}",
                    exc_info=True
                )

        # Process detected opportunities
        if all_opportunities:
            await self._process_opportunities(all_opportunities)

    async def _process_opportunities(
        self,
        opportunities: List[ArbitrageOpportunity]
    ):
        """
        Process detected arbitrage opportunities.

        Args:
            opportunities: List of detected opportunities
        """
        self.total_opportunities += len(opportunities)

        for opportunity in opportunities:
            # Check if opportunity is viable
            if not opportunity.is_viable():
                continue

            self.viable_opportunities += 1

            # Check with risk manager
            should_execute, reason = self.risk_manager.should_execute_opportunity(
                opportunity
            )

            if not should_execute:
                self.logger.info(
                    f"Opportunity {opportunity.opportunity_id} rejected by risk manager: {reason}"
                )
                continue

            # Execute the opportunity
            await self._execute_opportunity(opportunity)

    async def _execute_opportunity(self, opportunity: ArbitrageOpportunity):
        """
        Execute an arbitrage opportunity.

        Args:
            opportunity: Opportunity to execute
        """
        self.logger.info(
            f"Executing opportunity {opportunity.opportunity_id}: "
            f"{opportunity.arbitrage_type.value} - {opportunity.symbol} "
            f"(Expected profit: {opportunity.expected_profit_percentage:.4f}%)"
        )

        try:
            # Execute trades
            trades = await self.execution_service.execute_opportunity(opportunity)

            if trades:
                self.executed_trades += len(trades)
                self.executed_opportunities.append(opportunity)

                # Update risk manager with executed trades
                self.risk_manager.update_position(opportunity.opportunity_id, trades)

                # Calculate actual profit
                actual_profit = self._calculate_actual_profit(trades)

                # Update agent that detected this opportunity
                agent_id = self._get_opportunity_agent(opportunity)
                if agent_id and agent_id in self.agents:
                    self.agents[agent_id].update_trade_result(actual_profit)

                self.logger.info(
                    f"Successfully executed opportunity {opportunity.opportunity_id}: "
                    f"Actual profit: {actual_profit:.4f}"
                )

                # Track latencies
                self.total_detection_latency += opportunity.detection_latency_ms
                for trade in trades:
                    self.total_execution_latency += trade.execution_latency_ms

            else:
                self.logger.warning(
                    f"Failed to execute opportunity {opportunity.opportunity_id}"
                )

        except Exception as e:
            self.logger.error(
                f"Error executing opportunity {opportunity.opportunity_id}: {e}",
                exc_info=True
            )

    def _get_opportunity_agent(self, opportunity: ArbitrageOpportunity) -> Optional[str]:
        """Get the agent that detected this opportunity."""
        type_to_agent = {
            "CROSS_EXCHANGE": "cross_exchange",
            "STATISTICAL": "statistical",
            "TRIANGULAR": "triangular"
        }
        return type_to_agent.get(opportunity.arbitrage_type.name)

    def _calculate_actual_profit(self, trades: List[Trade]) -> Decimal:
        """Calculate actual profit from executed trades."""
        total_revenue = Decimal(0)
        total_cost = Decimal(0)
        total_fees = Decimal(0)

        for trade in trades:
            trade_value = trade.quantity * trade.price

            if trade.side.value == "buy":
                total_cost += trade_value
            else:
                total_revenue += trade_value

            total_fees += trade.fees

        return total_revenue - total_cost - total_fees

    def get_status(self) -> Dict:
        """Get current system status."""
        return {
            "is_running": self.is_running,
            "total_opportunities": self.total_opportunities,
            "viable_opportunities": self.viable_opportunities,
            "executed_trades": self.executed_trades,
            "agents": {
                agent_id: agent.get_status()
                for agent_id, agent in self.agents.items()
            },
            "risk_report": self.risk_manager.get_risk_report() if self.risk_manager else {},
            "execution_metrics": self.execution_service.get_performance_metrics()
            if self.execution_service else {}
        }

    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get comprehensive performance metrics."""
        execution_metrics = self.execution_service.get_performance_metrics()

        avg_detection_latency = (
            self.total_detection_latency / self.total_opportunities
            if self.total_opportunities > 0 else 0
        )

        avg_execution_latency = (
            self.total_execution_latency / self.executed_trades
            if self.executed_trades > 0 else 0
        )

        return PerformanceMetrics(
            total_opportunities=self.total_opportunities,
            viable_opportunities=self.viable_opportunities,
            executed_trades=execution_metrics.get("total_trades", 0),
            successful_trades=execution_metrics.get("successful_trades", 0),
            failed_trades=execution_metrics.get("failed_trades", 0),
            total_profit=Decimal(str(execution_metrics.get("total_profit", 0))),
            total_loss=Decimal(str(execution_metrics.get("total_loss", 0))),
            net_profit=Decimal(str(execution_metrics.get("net_profit", 0))),
            average_profit_per_trade=Decimal(str(
                execution_metrics.get("net_profit", 0) / execution_metrics.get("total_trades", 1)
            )),
            average_detection_latency_ms=avg_detection_latency,
            average_execution_latency_ms=avg_execution_latency,
            success_rate=Decimal(str(execution_metrics.get("success_rate", 0))),
            metadata={
                "start_time": datetime.now().isoformat(),
                "total_agents": len(self.agents)
            }
        )
