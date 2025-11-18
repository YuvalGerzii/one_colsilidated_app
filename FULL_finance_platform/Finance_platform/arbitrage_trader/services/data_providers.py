"""
Free data providers for cryptocurrency, stocks, and forex data.
No API keys required for basic usage (some providers have optional keys for higher limits).
"""
import asyncio
import aiohttp
import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import json

from ..models.types import MarketData, MarketType


class CoinGeckoProvider:
    """
    CoinGecko API - Free cryptocurrency data.

    Free tier: 30 calls/min
    Features: Historical OHLC, market data, 10,000+ coins
    No API key required for demo usage.
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key: str = None):
        """
        Initialize CoinGecko provider.

        Args:
            api_key: Optional API key for higher rate limits
        """
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    async def get_price(
        self,
        coin_ids: List[str],
        vs_currencies: List[str] = ["usd"]
    ) -> Dict:
        """
        Get current prices for coins.

        Args:
            coin_ids: List of coin IDs (e.g., ["bitcoin", "ethereum"])
            vs_currencies: Target currencies

        Returns:
            Price data
        """
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": ",".join(vs_currencies)
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/simple/price",
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"CoinGecko error: {response.status}")
                    return {}

    async def get_historical_data(
        self,
        coin_id: str,
        vs_currency: str = "usd",
        days: int = 30
    ) -> List[Dict]:
        """
        Get historical market data.

        Args:
            coin_id: Coin ID (e.g., "bitcoin")
            vs_currency: Target currency
            days: Number of days (max 365 for free)

        Returns:
            List of OHLC data
        """
        params = {
            "vs_currency": vs_currency,
            "days": days
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/coins/{coin_id}/ohlc",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Format: [[timestamp, open, high, low, close], ...]
                    return [
                        {
                            "timestamp": datetime.fromtimestamp(item[0] / 1000),
                            "open": Decimal(str(item[1])),
                            "high": Decimal(str(item[2])),
                            "low": Decimal(str(item[3])),
                            "close": Decimal(str(item[4]))
                        }
                        for item in data
                    ]
                else:
                    self.logger.error(f"CoinGecko OHLC error: {response.status}")
                    return []

    async def get_market_chart(
        self,
        coin_id: str,
        vs_currency: str = "usd",
        days: int = 30
    ) -> Dict:
        """
        Get market chart data (prices, market caps, volumes).

        Args:
            coin_id: Coin ID
            vs_currency: Target currency
            days: Number of days

        Returns:
            Chart data with prices, market_caps, volumes
        """
        params = {
            "vs_currency": vs_currency,
            "days": days
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/coins/{coin_id}/market_chart",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "prices": [
                            {
                                "timestamp": datetime.fromtimestamp(item[0] / 1000),
                                "price": Decimal(str(item[1]))
                            }
                            for item in data.get("prices", [])
                        ],
                        "volumes": [
                            {
                                "timestamp": datetime.fromtimestamp(item[0] / 1000),
                                "volume": Decimal(str(item[1]))
                            }
                            for item in data.get("total_volumes", [])
                        ]
                    }
                else:
                    return {}

    async def get_coin_list(self) -> List[Dict]:
        """Get list of all supported coins."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/coins/list") as response:
                if response.status == 200:
                    return await response.json()
                return []


class BinancePublicProvider:
    """
    Binance Public API - Free cryptocurrency data.

    No API key required for public endpoints.
    Features: Real-time prices, OHLC, order books
    """

    BASE_URL = "https://api.binance.com/api/v3"

    def __init__(self):
        """Initialize Binance provider."""
        self.logger = logging.getLogger(__name__)

    async def get_ticker_price(self, symbol: str = None) -> Dict:
        """
        Get current ticker prices.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT") or None for all

        Returns:
            Price data
        """
        params = {}
        if symbol:
            params["symbol"] = symbol

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/ticker/price",
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}

    async def get_klines(
        self,
        symbol: str,
        interval: str = "1h",
        limit: int = 500,
        start_time: int = None,
        end_time: int = None
    ) -> List[Dict]:
        """
        Get OHLCV candlestick data.

        Args:
            symbol: Trading pair (e.g., "BTCUSDT")
            interval: Candlestick interval (1m, 5m, 15m, 1h, 4h, 1d, 1w)
            limit: Number of candles (max 1000)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds

        Returns:
            List of OHLCV data
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/klines",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Format: [open_time, open, high, low, close, volume, close_time, ...]
                    return [
                        {
                            "timestamp": datetime.fromtimestamp(item[0] / 1000),
                            "open": Decimal(str(item[1])),
                            "high": Decimal(str(item[2])),
                            "low": Decimal(str(item[3])),
                            "close": Decimal(str(item[4])),
                            "volume": Decimal(str(item[5])),
                            "close_time": datetime.fromtimestamp(item[6] / 1000),
                            "quote_volume": Decimal(str(item[7])),
                            "trades": int(item[8])
                        }
                        for item in data
                    ]
                else:
                    self.logger.error(f"Binance klines error: {response.status}")
                    return []

    async def get_order_book(
        self,
        symbol: str,
        limit: int = 100
    ) -> Dict:
        """
        Get order book depth.

        Args:
            symbol: Trading pair
            limit: Number of levels (5, 10, 20, 50, 100, 500, 1000, 5000)

        Returns:
            Order book with bids and asks
        """
        params = {
            "symbol": symbol,
            "limit": limit
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/depth",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "bids": [
                            {"price": Decimal(item[0]), "quantity": Decimal(item[1])}
                            for item in data.get("bids", [])
                        ],
                        "asks": [
                            {"price": Decimal(item[0]), "quantity": Decimal(item[1])}
                            for item in data.get("asks", [])
                        ],
                        "last_update_id": data.get("lastUpdateId")
                    }
                return {}

    async def get_24h_ticker(self, symbol: str = None) -> Dict:
        """Get 24h price change statistics."""
        params = {}
        if symbol:
            params["symbol"] = symbol

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/ticker/24hr",
                params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                return {}


class YahooFinanceProvider:
    """
    Yahoo Finance - Free stock market data.

    No API key required (uses yfinance-compatible endpoints).
    Features: Historical stock data, dividends, splits
    """

    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

    def __init__(self):
        """Initialize Yahoo Finance provider."""
        self.logger = logging.getLogger(__name__)

    async def get_historical_data(
        self,
        symbol: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> List[Dict]:
        """
        Get historical stock data.

        Args:
            symbol: Stock symbol (e.g., "AAPL", "GOOGL")
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            List of OHLCV data
        """
        params = {
            "period1": 0,
            "period2": int(datetime.now().timestamp()),
            "interval": interval,
            "range": period
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/{symbol}",
                params=params,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("chart", {}).get("result", [])

                    if not result:
                        return []

                    timestamps = result[0].get("timestamp", [])
                    indicators = result[0].get("indicators", {})
                    quote = indicators.get("quote", [{}])[0]

                    return [
                        {
                            "timestamp": datetime.fromtimestamp(ts),
                            "open": Decimal(str(quote["open"][i])) if quote["open"][i] else None,
                            "high": Decimal(str(quote["high"][i])) if quote["high"][i] else None,
                            "low": Decimal(str(quote["low"][i])) if quote["low"][i] else None,
                            "close": Decimal(str(quote["close"][i])) if quote["close"][i] else None,
                            "volume": int(quote["volume"][i]) if quote["volume"][i] else 0
                        }
                        for i, ts in enumerate(timestamps)
                        if quote["close"][i] is not None
                    ]
                else:
                    self.logger.error(f"Yahoo Finance error: {response.status}")
                    return []

    async def get_quote(self, symbol: str) -> Dict:
        """Get current stock quote."""
        params = {
            "interval": "1d",
            "range": "1d"
        }

        headers = {"User-Agent": "Mozilla/5.0"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/{symbol}",
                params=params,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("chart", {}).get("result", [])

                    if result:
                        meta = result[0].get("meta", {})
                        return {
                            "symbol": meta.get("symbol"),
                            "price": Decimal(str(meta.get("regularMarketPrice", 0))),
                            "previous_close": Decimal(str(meta.get("previousClose", 0))),
                            "currency": meta.get("currency"),
                            "exchange": meta.get("exchangeName")
                        }
                return {}


class AlphaVantageProvider:
    """
    Alpha Vantage API - Free stocks, forex, crypto data.

    Free tier: 5 requests/min, 500/day
    Requires free API key from: https://www.alphavantage.co/support/#api-key
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str = "demo"):
        """
        Initialize Alpha Vantage provider.

        Args:
            api_key: API key (get free key from alphavantage.co)
        """
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    async def get_daily_stock(
        self,
        symbol: str,
        outputsize: str = "compact"
    ) -> List[Dict]:
        """
        Get daily stock data.

        Args:
            symbol: Stock symbol (e.g., "IBM", "AAPL")
            outputsize: "compact" (100 days) or "full" (20+ years)

        Returns:
            List of daily OHLCV data
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    time_series = data.get("Time Series (Daily)", {})

                    return [
                        {
                            "timestamp": datetime.strptime(date, "%Y-%m-%d"),
                            "open": Decimal(values["1. open"]),
                            "high": Decimal(values["2. high"]),
                            "low": Decimal(values["3. low"]),
                            "close": Decimal(values["4. close"]),
                            "volume": int(values["5. volume"])
                        }
                        for date, values in sorted(time_series.items())
                    ]
                return []

    async def get_forex_daily(
        self,
        from_currency: str,
        to_currency: str,
        outputsize: str = "compact"
    ) -> List[Dict]:
        """
        Get daily forex data.

        Args:
            from_currency: Base currency (e.g., "EUR")
            to_currency: Quote currency (e.g., "USD")
            outputsize: "compact" or "full"

        Returns:
            List of daily OHLC data
        """
        params = {
            "function": "FX_DAILY",
            "from_symbol": from_currency,
            "to_symbol": to_currency,
            "outputsize": outputsize,
            "apikey": self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    time_series = data.get("Time Series FX (Daily)", {})

                    return [
                        {
                            "timestamp": datetime.strptime(date, "%Y-%m-%d"),
                            "open": Decimal(values["1. open"]),
                            "high": Decimal(values["2. high"]),
                            "low": Decimal(values["3. low"]),
                            "close": Decimal(values["4. close"])
                        }
                        for date, values in sorted(time_series.items())
                    ]
                return []

    async def get_crypto_daily(
        self,
        symbol: str,
        market: str = "USD"
    ) -> List[Dict]:
        """
        Get daily cryptocurrency data.

        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH")
            market: Market currency

        Returns:
            List of daily OHLCV data
        """
        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": market,
            "apikey": self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    time_series = data.get("Time Series (Digital Currency Daily)", {})

                    return [
                        {
                            "timestamp": datetime.strptime(date, "%Y-%m-%d"),
                            "open": Decimal(values.get(f"1a. open ({market})", 0)),
                            "high": Decimal(values.get(f"2a. high ({market})", 0)),
                            "low": Decimal(values.get(f"3a. low ({market})", 0)),
                            "close": Decimal(values.get(f"4a. close ({market})", 0)),
                            "volume": Decimal(values.get("5. volume", 0))
                        }
                        for date, values in sorted(time_series.items())
                    ]
                return []


class DataProviderManager:
    """Unified manager for all data providers."""

    def __init__(self, config: dict = None):
        """
        Initialize data provider manager.

        Args:
            config: Configuration with API keys
        """
        self.config = config or {}

        # Initialize providers
        self.coingecko = CoinGeckoProvider(
            api_key=self.config.get("coingecko_api_key")
        )
        self.binance = BinancePublicProvider()
        self.yahoo = YahooFinanceProvider()
        self.alphavantage = AlphaVantageProvider(
            api_key=self.config.get("alphavantage_api_key", "demo")
        )

        self.logger = logging.getLogger(__name__)

    async def get_crypto_historical(
        self,
        symbol: str,
        days: int = 30,
        provider: str = "binance"
    ) -> List[Dict]:
        """
        Get historical cryptocurrency data.

        Args:
            symbol: Symbol (e.g., "BTCUSDT" for Binance, "bitcoin" for CoinGecko)
            days: Number of days
            provider: "binance" or "coingecko"

        Returns:
            Historical OHLC data
        """
        if provider == "binance":
            return await self.binance.get_klines(
                symbol=symbol,
                interval="1d",
                limit=days
            )
        elif provider == "coingecko":
            return await self.coingecko.get_historical_data(
                coin_id=symbol,
                days=days
            )
        else:
            raise ValueError(f"Unknown crypto provider: {provider}")

    async def get_stock_historical(
        self,
        symbol: str,
        period: str = "1y",
        provider: str = "yahoo"
    ) -> List[Dict]:
        """
        Get historical stock data.

        Args:
            symbol: Stock symbol (e.g., "AAPL")
            period: Time period
            provider: "yahoo" or "alphavantage"

        Returns:
            Historical OHLC data
        """
        if provider == "yahoo":
            return await self.yahoo.get_historical_data(
                symbol=symbol,
                period=period
            )
        elif provider == "alphavantage":
            return await self.alphavantage.get_daily_stock(
                symbol=symbol,
                outputsize="full" if period in ["5y", "10y", "max"] else "compact"
            )
        else:
            raise ValueError(f"Unknown stock provider: {provider}")

    async def get_forex_historical(
        self,
        from_currency: str,
        to_currency: str,
        days: int = 100
    ) -> List[Dict]:
        """
        Get historical forex data.

        Args:
            from_currency: Base currency
            to_currency: Quote currency
            days: Number of days

        Returns:
            Historical OHLC data
        """
        data = await self.alphavantage.get_forex_daily(
            from_currency=from_currency,
            to_currency=to_currency,
            outputsize="full" if days > 100 else "compact"
        )

        # Filter to requested days
        if len(data) > days:
            return data[-days:]
        return data

    async def get_current_prices(
        self,
        symbols: List[str],
        market_type: str = "crypto"
    ) -> Dict[str, Decimal]:
        """
        Get current prices for multiple symbols.

        Args:
            symbols: List of symbols
            market_type: "crypto", "stock", or "forex"

        Returns:
            Dictionary of symbol -> price
        """
        prices = {}

        if market_type == "crypto":
            for symbol in symbols:
                ticker = await self.binance.get_ticker_price(symbol)
                if ticker and "price" in ticker:
                    prices[symbol] = Decimal(ticker["price"])

        elif market_type == "stock":
            for symbol in symbols:
                quote = await self.yahoo.get_quote(symbol)
                if quote and "price" in quote:
                    prices[symbol] = quote["price"]

        return prices
