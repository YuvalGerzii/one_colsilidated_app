"""
Advanced execution algorithms for optimal trade execution.
Includes TWAP, VWAP, Implementation Shortfall, and POV strategies.
"""
from typing import List, Dict, Optional, Callable
from decimal import Decimal
from datetime import datetime, timedelta
import asyncio
import numpy as np
import uuid

from ..models.types import (
    TradingAction,
    Trade,
    OrderSide,
    OrderStatus,
    MarketData
)


class ExecutionAlgorithm:
    """Base class for execution algorithms."""

    def __init__(self, config: dict = None):
        """
        Initialize execution algorithm.

        Args:
            config: Algorithm configuration
        """
        self.config = config or {}
        self.trades: List[Trade] = []
        self.is_running = False

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable
    ) -> List[Trade]:
        """
        Execute the algorithm.

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback function for actual execution

        Returns:
            List of executed trades
        """
        raise NotImplementedError


class TWAPExecutor(ExecutionAlgorithm):
    """Time-Weighted Average Price execution algorithm."""

    def __init__(self, config: dict = None):
        """
        Initialize TWAP executor.

        Args:
            config: Configuration with 'duration_minutes' and 'num_slices'
        """
        super().__init__(config)
        self.duration_minutes = config.get("duration_minutes", 60) if config else 60
        self.num_slices = config.get("num_slices", 10) if config else 10

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable
    ) -> List[Trade]:
        """
        Execute TWAP strategy.

        Splits order into equal slices executed at regular intervals.

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback for actual execution

        Returns:
            List of executed trades
        """
        self.is_running = True
        self.trades = []

        # Calculate slice parameters
        slice_quantity = total_quantity / Decimal(self.num_slices)
        interval_seconds = (self.duration_minutes * 60) / self.num_slices

        print(f"TWAP Execution: {total_quantity} {symbol} over {self.duration_minutes} min")
        print(f"  Slices: {self.num_slices}, Each: {slice_quantity}, Interval: {interval_seconds}s")

        for i in range(self.num_slices):
            if not self.is_running:
                break

            # Execute slice
            trade = await execution_callback(
                symbol=symbol,
                exchange=exchange,
                side=side,
                quantity=slice_quantity,
                order_type="market"
            )

            if trade:
                self.trades.append(trade)
                print(f"  Slice {i+1}/{self.num_slices} executed: {slice_quantity} @ {trade.price}")

            # Wait for next interval (except for last slice)
            if i < self.num_slices - 1:
                await asyncio.sleep(interval_seconds)

        return self.trades

    def get_average_price(self) -> Decimal:
        """Get volume-weighted average execution price."""
        if not self.trades:
            return Decimal(0)

        total_value = sum(trade.quantity * trade.price for trade in self.trades)
        total_quantity = sum(trade.quantity for trade in self.trades)

        return total_value / total_quantity if total_quantity > 0 else Decimal(0)


class VWAPExecutor(ExecutionAlgorithm):
    """Volume-Weighted Average Price execution algorithm."""

    def __init__(self, config: dict = None):
        """
        Initialize VWAP executor.

        Args:
            config: Configuration with 'duration_minutes' and 'participation_rate'
        """
        super().__init__(config)
        self.duration_minutes = config.get("duration_minutes", 60) if config else 60
        self.participation_rate = Decimal(
            str(config.get("participation_rate", 0.1)) if config else "0.1"
        )  # 10% of market volume

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable,
        volume_feed: Callable = None
    ) -> List[Trade]:
        """
        Execute VWAP strategy.

        Trades in proportion to market volume to track VWAP benchmark.

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback for actual execution
            volume_feed: Optional callback to get current market volume

        Returns:
            List of executed trades
        """
        self.is_running = True
        self.trades = []

        remaining_quantity = total_quantity
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=self.duration_minutes)

        print(f"VWAP Execution: {total_quantity} {symbol} over {self.duration_minutes} min")
        print(f"  Participation Rate: {float(self.participation_rate)*100:.1f}%")

        while self.is_running and remaining_quantity > 0 and datetime.now() < end_time:
            # Get current market volume
            if volume_feed:
                market_volume = await volume_feed(symbol, exchange)
            else:
                market_volume = Decimal(100)  # Default if no feed

            # Calculate slice based on participation rate
            slice_quantity = min(
                market_volume * self.participation_rate,
                remaining_quantity
            )

            if slice_quantity > 0:
                # Execute slice
                trade = await execution_callback(
                    symbol=symbol,
                    exchange=exchange,
                    side=side,
                    quantity=slice_quantity,
                    order_type="market"
                )

                if trade:
                    self.trades.append(trade)
                    remaining_quantity -= slice_quantity
                    print(f"  Executed: {slice_quantity} @ {trade.price} (Remaining: {remaining_quantity})")

            # Check every 5 seconds
            await asyncio.sleep(5)

        return self.trades


class ImplementationShortfallExecutor(ExecutionAlgorithm):
    """Implementation Shortfall (Almgren-Chriss) execution algorithm."""

    def __init__(self, config: dict = None):
        """
        Initialize Implementation Shortfall executor.

        Args:
            config: Configuration with risk aversion and urgency parameters
        """
        super().__init__(config)
        self.risk_aversion = Decimal(
            str(config.get("risk_aversion", 0.01)) if config else "0.01"
        )
        self.duration_minutes = config.get("duration_minutes", 60) if config else 60

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable,
        arrival_price: Decimal = None,
        volatility: Decimal = None
    ) -> List[Trade]:
        """
        Execute Implementation Shortfall strategy.

        Minimizes expected cost + risk penalty using Almgren-Chriss model.

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback for actual execution
            arrival_price: Price at decision time
            volatility: Estimated volatility

        Returns:
            List of executed trades
        """
        self.is_running = True
        self.trades = []

        # Default values if not provided
        volatility = volatility or Decimal("0.01")  # 1% volatility

        # Calculate optimal trajectory using simplified Almgren-Chriss
        num_periods = 10
        trajectory = self._calculate_optimal_trajectory(
            total_quantity,
            num_periods,
            volatility
        )

        print(f"Implementation Shortfall: {total_quantity} {symbol}")
        print(f"  Risk Aversion: {self.risk_aversion}, Periods: {num_periods}")

        interval_seconds = (self.duration_minutes * 60) / num_periods

        for i, target_quantity in enumerate(trajectory):
            if not self.is_running or target_quantity <= 0:
                break

            # Execute slice
            trade = await execution_callback(
                symbol=symbol,
                exchange=exchange,
                side=side,
                quantity=target_quantity,
                order_type="market"
            )

            if trade:
                self.trades.append(trade)
                print(f"  Period {i+1}/{num_periods}: {target_quantity} @ {trade.price}")

            if i < num_periods - 1:
                await asyncio.sleep(interval_seconds)

        # Calculate implementation shortfall
        if arrival_price and self.trades:
            avg_exec_price = self.get_average_price()
            shortfall = abs(avg_exec_price - arrival_price) / arrival_price * 100
            print(f"  Implementation Shortfall: {shortfall:.3f}%")

        return self.trades

    def _calculate_optimal_trajectory(
        self,
        total_quantity: Decimal,
        num_periods: int,
        volatility: Decimal
    ) -> List[Decimal]:
        """
        Calculate optimal trading trajectory.

        Simplified Almgren-Chriss model.
        """
        # Decay parameter based on risk aversion
        kappa = float(self.risk_aversion) * float(volatility)

        # Calculate trajectory
        trajectory = []
        remaining = float(total_quantity)

        for t in range(num_periods):
            # Optimal trade size decreases exponentially
            time_left = num_periods - t
            trade_size = remaining * (1 - np.exp(-kappa)) / (1 - np.exp(-kappa * time_left))

            trajectory.append(Decimal(str(trade_size)))
            remaining -= trade_size

        return trajectory

    def get_average_price(self) -> Decimal:
        """Get volume-weighted average execution price."""
        if not self.trades:
            return Decimal(0)

        total_value = sum(trade.quantity * trade.price for trade in self.trades)
        total_quantity = sum(trade.quantity for trade in self.trades)

        return total_value / total_quantity if total_quantity > 0 else Decimal(0)


class POVExecutor(ExecutionAlgorithm):
    """Percentage of Volume execution algorithm."""

    def __init__(self, config: dict = None):
        """
        Initialize POV executor.

        Args:
            config: Configuration with 'target_percentage' and 'duration_minutes'
        """
        super().__init__(config)
        self.target_percentage = Decimal(
            str(config.get("target_percentage", 0.15)) if config else "0.15"
        )  # 15% of volume
        self.duration_minutes = config.get("duration_minutes", 60) if config else 60

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable,
        volume_feed: Callable = None
    ) -> List[Trade]:
        """
        Execute POV strategy.

        Maintains constant percentage of market volume.

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback for actual execution
            volume_feed: Callback to get current market volume

        Returns:
            List of executed trades
        """
        self.is_running = True
        self.trades = []

        remaining_quantity = total_quantity
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=self.duration_minutes)

        print(f"POV Execution: {total_quantity} {symbol}")
        print(f"  Target: {float(self.target_percentage)*100:.1f}% of volume")

        measurement_window = []  # Track recent volume measurements

        while self.is_running and remaining_quantity > 0 and datetime.now() < end_time:
            # Get current market volume
            if volume_feed:
                market_volume = await volume_feed(symbol, exchange)
            else:
                market_volume = Decimal(100)  # Default

            measurement_window.append(float(market_volume))

            # Calculate average market volume
            if len(measurement_window) > 10:
                measurement_window.pop(0)
            avg_market_volume = Decimal(str(np.mean(measurement_window)))

            # Calculate our share
            our_volume = avg_market_volume * self.target_percentage
            slice_quantity = min(our_volume, remaining_quantity)

            if slice_quantity > 0:
                trade = await execution_callback(
                    symbol=symbol,
                    exchange=exchange,
                    side=side,
                    quantity=slice_quantity,
                    order_type="market"
                )

                if trade:
                    self.trades.append(trade)
                    remaining_quantity -= slice_quantity

                    # Calculate actual POV
                    actual_pov = slice_quantity / avg_market_volume * 100 if avg_market_volume > 0 else 0
                    print(f"  Executed: {slice_quantity} @ {trade.price} (POV: {actual_pov:.1f}%)")

            await asyncio.sleep(5)

        return self.trades


class AdaptiveExecutor(ExecutionAlgorithm):
    """Adaptive execution algorithm that adjusts based on market conditions."""

    def __init__(self, config: dict = None):
        """
        Initialize Adaptive executor.

        Args:
            config: Configuration parameters
        """
        super().__init__(config)
        self.duration_minutes = config.get("duration_minutes", 60) if config else 60
        self.aggressiveness = Decimal(
            str(config.get("aggressiveness", 0.5)) if config else "0.5"
        )  # 0-1

    async def execute(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        total_quantity: Decimal,
        execution_callback: Callable,
        market_data_feed: Callable = None
    ) -> List[Trade]:
        """
        Execute adaptive strategy.

        Adjusts execution speed based on:
        - Market volatility
        - Spread
        - Volume
        - Price momentum

        Args:
            symbol: Trading symbol
            exchange: Exchange name
            side: Buy or sell
            total_quantity: Total quantity to execute
            execution_callback: Callback for actual execution
            market_data_feed: Callback to get market conditions

        Returns:
            List of executed trades
        """
        self.is_running = True
        self.trades = []

        remaining_quantity = total_quantity
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=self.duration_minutes)

        print(f"Adaptive Execution: {total_quantity} {symbol}")
        print(f"  Aggressiveness: {float(self.aggressiveness):.1f}")

        while self.is_running and remaining_quantity > 0 and datetime.now() < end_time:
            # Get market conditions
            if market_data_feed:
                market_data = await market_data_feed(symbol, exchange)
                urgency = self._calculate_urgency(market_data)
            else:
                urgency = self.aggressiveness

            # Time urgency (speed up near end)
            time_elapsed = (datetime.now() - start_time).total_seconds()
            time_remaining = (end_time - datetime.now()).total_seconds()
            time_urgency = Decimal(1) - Decimal(str(time_remaining / (self.duration_minutes * 60)))

            # Combined urgency
            total_urgency = (urgency + time_urgency) / 2

            # Calculate slice size based on urgency
            baseline_slice = remaining_quantity / Decimal(10)  # 10% baseline
            adjusted_slice = baseline_slice * (Decimal(1) + total_urgency)
            slice_quantity = min(adjusted_slice, remaining_quantity)

            if slice_quantity > 0:
                trade = await execution_callback(
                    symbol=symbol,
                    exchange=exchange,
                    side=side,
                    quantity=slice_quantity,
                    order_type="market"
                )

                if trade:
                    self.trades.append(trade)
                    remaining_quantity -= slice_quantity
                    print(f"  Executed: {slice_quantity} @ {trade.price} (Urgency: {total_urgency:.2f})")

            # Adaptive wait time (faster when more urgent)
            wait_time = 10 * float(Decimal(1) - total_urgency)
            await asyncio.sleep(max(wait_time, 1))

        return self.trades

    def _calculate_urgency(self, market_data: MarketData) -> Decimal:
        """Calculate urgency based on market conditions."""
        urgency_score = Decimal(0)

        # Favorable spread = higher urgency
        if market_data.spread_percentage < Decimal("0.1"):
            urgency_score += Decimal("0.3")

        # High volume = higher urgency (better liquidity)
        total_volume = market_data.bid_volume + market_data.ask_volume
        if total_volume > Decimal(1000):
            urgency_score += Decimal("0.3")

        # Additional factors could include:
        # - Price momentum
        # - Volatility
        # - Time of day

        return min(urgency_score, Decimal(1))


class ExecutionManager:
    """Manager for execution algorithms."""

    def __init__(self):
        """Initialize execution manager."""
        self.algorithms = {
            "twap": TWAPExecutor,
            "vwap": VWAPExecutor,
            "is": ImplementationShortfallExecutor,
            "pov": POVExecutor,
            "adaptive": AdaptiveExecutor
        }

    def get_executor(self, algorithm: str, config: dict = None) -> ExecutionAlgorithm:
        """
        Get execution algorithm instance.

        Args:
            algorithm: Algorithm name (twap, vwap, is, pov, adaptive)
            config: Algorithm configuration

        Returns:
            Execution algorithm instance
        """
        if algorithm.lower() not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return self.algorithms[algorithm.lower()](config)

    async def execute_with_algorithm(
        self,
        algorithm: str,
        symbol: str,
        exchange: str,
        side: OrderSide,
        quantity: Decimal,
        execution_callback: Callable,
        config: dict = None,
        **kwargs
    ) -> List[Trade]:
        """
        Execute order using specified algorithm.

        Args:
            algorithm: Algorithm name
            symbol: Trading symbol
            exchange: Exchange
            side: Buy or sell
            quantity: Total quantity
            execution_callback: Execution callback
            config: Algorithm config
            **kwargs: Additional algorithm-specific parameters

        Returns:
            List of executed trades
        """
        executor = self.get_executor(algorithm, config)

        return await executor.execute(
            symbol=symbol,
            exchange=exchange,
            side=side,
            total_quantity=quantity,
            execution_callback=execution_callback,
            **kwargs
        )
