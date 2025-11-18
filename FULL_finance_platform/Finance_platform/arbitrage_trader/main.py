"""
Main entry point for the arbitrage trading system.
"""
import asyncio
import signal
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from arbitrage_trader.orchestrator import ArbitrageOrchestrator
from arbitrage_trader.config.default_config import get_config


class ArbitrageSystem:
    """Main arbitrage trading system."""

    def __init__(self, config: dict = None):
        """
        Initialize the system.

        Args:
            config: Optional custom configuration
        """
        self.config = get_config(config)
        self.orchestrator = ArbitrageOrchestrator(self.config)
        self.shutdown_event = asyncio.Event()

    async def run(self):
        """Run the arbitrage trading system."""
        print("=" * 80)
        print("Multi-Agent Arbitrage Trading System")
        print("=" * 80)
        print()

        # Initialize system
        print("Initializing system...")
        await self.orchestrator.initialize()
        print("✓ System initialized")
        print()

        # Start system
        print("Starting trading system...")
        await self.orchestrator.start()
        print("✓ Trading system started")
        print()

        # Print status
        self._print_status()

        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda: asyncio.create_task(self.shutdown())
            )

        # Wait for shutdown signal
        await self.shutdown_event.wait()

        # Stop system
        print("\nShutting down...")
        await self.orchestrator.stop()
        print("✓ System stopped gracefully")

    async def shutdown(self):
        """Trigger shutdown."""
        print("\n\n[Shutdown signal received]")
        self.shutdown_event.set()

    def _print_status(self):
        """Print system status."""
        status = self.orchestrator.get_status()

        print("System Status:")
        print(f"  Running: {status['is_running']}")
        print(f"  Active Agents: {len(status['agents'])}")
        print()

        print("Active Agents:")
        for agent_id, agent_status in status['agents'].items():
            print(f"  • {agent_id}")
            print(f"    Type: {agent_status.agent_type}")
            print(f"    Active: {agent_status.is_active}")
            print(f"    Opportunities Detected: {agent_status.opportunities_detected}")
            print()

        print("Monitoring:")
        exchanges = self.config.get("exchanges", {})
        total_symbols = sum(len(symbols) for symbols in exchanges.values())
        print(f"  Exchanges: {len(exchanges)}")
        print(f"  Total Symbols: {total_symbols}")
        print()

        print("Press Ctrl+C to stop the system")
        print("=" * 80)
        print()


async def run_demo():
    """Run a demo of the system."""
    # Custom configuration for demo
    demo_config = {
        "log_level": "INFO",
        "market_data": {
            "update_interval_ms": 2000,  # Update every 2 seconds for demo
        }
    }

    system = ArbitrageSystem(demo_config)
    await system.run()


async def run_monitoring_loop(orchestrator: ArbitrageOrchestrator, interval: int = 10):
    """
    Run a monitoring loop to display system statistics.

    Args:
        orchestrator: The orchestrator to monitor
        interval: Update interval in seconds
    """
    while orchestrator.is_running:
        await asyncio.sleep(interval)

        # Get and display metrics
        metrics = orchestrator.get_performance_metrics()
        status = orchestrator.get_status()

        print("\n" + "=" * 80)
        print(f"SYSTEM METRICS - {metrics.metadata.get('start_time', 'N/A')}")
        print("=" * 80)

        print(f"\nOpportunities:")
        print(f"  Total Detected:        {metrics.total_opportunities}")
        print(f"  Viable:                {metrics.viable_opportunities}")
        print(f"  Viability Rate:        {metrics.viable_opportunities / metrics.total_opportunities * 100 if metrics.total_opportunities > 0 else 0:.2f}%")

        print(f"\nTrades:")
        print(f"  Total Executed:        {metrics.executed_trades}")
        print(f"  Successful:            {metrics.successful_trades}")
        print(f"  Failed:                {metrics.failed_trades}")
        print(f"  Success Rate:          {float(metrics.success_rate) * 100:.2f}%")

        print(f"\nProfit/Loss:")
        print(f"  Total Profit:          ${float(metrics.total_profit):.2f}")
        print(f"  Total Loss:            ${float(metrics.total_loss):.2f}")
        print(f"  Net Profit:            ${float(metrics.net_profit):.2f}")
        print(f"  Avg Per Trade:         ${float(metrics.average_profit_per_trade):.2f}")

        print(f"\nLatency:")
        print(f"  Avg Detection:         {metrics.average_detection_latency_ms:.2f}ms")
        print(f"  Avg Execution:         {metrics.average_execution_latency_ms:.2f}ms")

        # Risk metrics
        if "risk_report" in status:
            risk = status["risk_report"]
            print(f"\nRisk Metrics:")
            print(f"  Current Exposure:      ${risk.get('current_exposure', 0):.2f}")
            print(f"  Exposure Limit:        ${risk.get('max_total_exposure', 0):.2f}")
            print(f"  Exposure Utilization:  {risk.get('exposure_utilization', 0):.2f}%")
            print(f"  Daily PnL:             ${risk.get('daily_pnl', 0):.2f}")
            print(f"  Daily Loss:            ${risk.get('daily_loss', 0):.2f}")
            print(f"  Active Positions:      {risk.get('active_positions', 0)}")

        print("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
