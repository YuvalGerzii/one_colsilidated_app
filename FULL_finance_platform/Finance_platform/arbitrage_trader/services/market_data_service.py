"""
Market data service for collecting real-time market data from various sources.
"""
import asyncio
import logging
from typing import List, Dict, Set, Optional
from datetime import datetime
from decimal import Decimal
import random

from ..models.types import MarketData, MarketType


class MarketDataService:
    """Service for collecting and distributing market data."""

    def __init__(self, config: dict = None):
        """
        Initialize market data service.

        Args:
            config: Service configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Subscribers
        self.subscribers: List = []

        # Market data cache
        self.latest_data: Dict[str, MarketData] = {}

        # Active exchanges and symbols
        self.exchanges: Set[str] = set()
        self.symbols: Set[str] = set()

        self.is_running = False

    def add_exchange(self, exchange: str, symbols: List[str]):
        """
        Add an exchange to monitor.

        Args:
            exchange: Exchange name
            symbols: List of symbols to monitor on this exchange
        """
        self.exchanges.add(exchange)
        self.symbols.update(symbols)
        self.logger.info(f"Added exchange {exchange} with {len(symbols)} symbols")

    def subscribe(self, callback):
        """
        Subscribe to market data updates.

        Args:
            callback: Async callback function to receive market data updates
        """
        self.subscribers.append(callback)
        self.logger.info(f"Added subscriber: {callback}")

    async def start(self):
        """Start the market data service."""
        self.is_running = True
        self.logger.info("Market data service started")

        # Start data collection task
        asyncio.create_task(self._collect_market_data())

    async def stop(self):
        """Stop the market data service."""
        self.is_running = False
        self.logger.info("Market data service stopped")

    async def _collect_market_data(self):
        """Collect market data from exchanges (main loop)."""
        while self.is_running:
            try:
                # Collect data from all exchanges
                all_data = []

                for exchange in self.exchanges:
                    for symbol in self.symbols:
                        data = await self._fetch_market_data(exchange, symbol)
                        if data:
                            all_data.append(data)
                            self.latest_data[f"{exchange}:{symbol}"] = data

                # Notify subscribers
                if all_data:
                    await self._notify_subscribers(all_data)

                # Sleep interval based on config
                interval = self.config.get("update_interval_ms", 1000) / 1000
                await asyncio.sleep(interval)

            except Exception as e:
                self.logger.error(f"Error collecting market data: {e}", exc_info=True)
                await asyncio.sleep(1)

    async def _fetch_market_data(
        self,
        exchange: str,
        symbol: str
    ) -> Optional[MarketData]:
        """
        Fetch market data from an exchange.

        In a real implementation, this would connect to exchange APIs.
        For now, we simulate data.

        Args:
            exchange: Exchange name
            symbol: Trading symbol

        Returns:
            MarketData or None
        """
        try:
            # Simulate fetching data
            # In production, this would use exchange APIs like:
            # - Binance API
            # - Coinbase API
            # - Kraken API
            # - Interactive Brokers
            # etc.

            # Determine market type based on symbol
            market_type = self._determine_market_type(symbol)

            # Simulate realistic price data
            base_price = self._get_simulated_base_price(symbol)

            # Add some random variation
            spread_pct = Decimal(random.uniform(0.001, 0.01))
            mid_price = Decimal(str(base_price)) * Decimal(str(random.uniform(0.99, 1.01)))

            spread = mid_price * spread_pct
            bid_price = mid_price - spread / 2
            ask_price = mid_price + spread / 2

            # Simulate volume
            volume = Decimal(str(random.uniform(100, 10000)))

            market_data = MarketData(
                symbol=symbol,
                exchange=exchange,
                market_type=market_type,
                bid_price=bid_price,
                ask_price=ask_price,
                bid_volume=volume * Decimal(str(random.uniform(0.8, 1.0))),
                ask_volume=volume * Decimal(str(random.uniform(0.8, 1.0))),
                timestamp=datetime.now(),
                last_trade_price=mid_price,
                volume_24h=volume * Decimal(100),
                metadata={
                    "simulated": True,
                    "exchange": exchange
                }
            )

            return market_data

        except Exception as e:
            self.logger.error(
                f"Error fetching data for {exchange}:{symbol}: {e}",
                exc_info=True
            )
            return None

    def _determine_market_type(self, symbol: str) -> MarketType:
        """Determine market type from symbol."""
        if any(crypto in symbol for crypto in ["BTC", "ETH", "USDT", "BNB", "SOL"]):
            return MarketType.CRYPTO
        elif any(fx in symbol for fx in ["USD", "EUR", "GBP", "JPY"]):
            return MarketType.FOREX
        elif "/" in symbol:
            return MarketType.CRYPTO  # Assume crypto for pairs
        else:
            return MarketType.STOCKS

    def _get_simulated_base_price(self, symbol: str) -> float:
        """Get simulated base price for a symbol."""
        # Simplified price simulation
        price_map = {
            "BTC/USD": 50000,
            "BTC/USDT": 50000,
            "ETH/USD": 3000,
            "ETH/USDT": 3000,
            "ETH/BTC": 0.06,
            "BTC/ETH": 16.67,
            "SOL/USD": 100,
            "SOL/USDT": 100,
            "AAPL": 180,
            "GOOGL": 140,
            "TSLA": 250,
            "EUR/USD": 1.08,
            "GBP/USD": 1.26,
        }

        return price_map.get(symbol, 100.0)

    async def _notify_subscribers(self, market_data: List[MarketData]):
        """Notify all subscribers of new market data."""
        for subscriber in self.subscribers:
            try:
                await subscriber(market_data)
            except Exception as e:
                self.logger.error(
                    f"Error notifying subscriber {subscriber}: {e}",
                    exc_info=True
                )

    def get_latest_data(self, exchange: str = None, symbol: str = None) -> List[MarketData]:
        """
        Get latest market data.

        Args:
            exchange: Filter by exchange (optional)
            symbol: Filter by symbol (optional)

        Returns:
            List of latest market data
        """
        data = list(self.latest_data.values())

        if exchange:
            data = [d for d in data if d.exchange == exchange]

        if symbol:
            data = [d for d in data if d.symbol == symbol]

        return data
