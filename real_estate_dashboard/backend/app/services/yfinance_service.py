"""
YFinance Service for Market Intelligence

Provides comprehensive market data integration using Yahoo Finance API.
Includes stock data, REIT information, market indices, and financial metrics.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import yfinance as yf
import pandas as pd
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class YFinanceService:
    """Service for fetching market data from Yahoo Finance"""

    # Common Real Estate ETFs and REITs
    REIT_TICKERS = [
        "VNQ",    # Vanguard Real Estate ETF
        "IYR",    # iShares U.S. Real Estate ETF
        "XLRE",   # Real Estate Select Sector SPDR Fund
        "RWR",    # SPDR Dow Jones REIT ETF
        "SCHH",   # Schwab US REIT ETF
        "AMT",    # American Tower REIT
        "PLD",    # Prologis REIT
        "CCI",    # Crown Castle REIT
        "EQIX",   # Equinix REIT
        "PSA",    # Public Storage REIT
        "SPG",    # Simon Property Group REIT
        "O",      # Realty Income REIT
        "WELL",   # Welltower REIT
        "AVB",    # AvalonBay Communities REIT
        "EQR",    # Equity Residential REIT
    ]

    # Major Market Indices
    MARKET_INDICES = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones Industrial Average",
        "^IXIC": "NASDAQ Composite",
        "^RUT": "Russell 2000",
        "^VIX": "CBOE Volatility Index",
    }

    # Key interest rate and treasury indicators
    RATE_INDICATORS = {
        "^IRX": "13 Week Treasury Bill",
        "^FVX": "5 Year Treasury Yield",
        "^TNX": "10 Year Treasury Yield",
        "^TYX": "30 Year Treasury Yield",
    }

    def __init__(self):
        self.cache = CacheService()
        self.cache_ttl = 900  # 15 minutes

    async def get_stock_data(
        self,
        ticker: str,
        period: str = "1mo",
        interval: str = "1d",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get historical stock data for a ticker

        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            use_cache: Whether to use cached data

        Returns:
            Dict with stock data including history, info, and metrics
        """
        cache_key = f"yfinance:stock:{ticker}:{period}:{interval}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            stock = yf.Ticker(ticker)

            # Get historical data
            hist = stock.history(period=period, interval=interval)

            # Get basic info
            info = stock.info

            # Calculate metrics
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            price_change = None
            price_change_pct = None

            if not hist.empty and len(hist) > 1:
                prev_price = hist['Close'].iloc[0]
                if prev_price and current_price:
                    price_change = current_price - prev_price
                    price_change_pct = (price_change / prev_price) * 100

            result = {
                "ticker": ticker,
                "current_price": float(current_price) if current_price else None,
                "currency": info.get("currency", "USD"),
                "price_change": float(price_change) if price_change else None,
                "price_change_pct": float(price_change_pct) if price_change_pct else None,
                "volume": int(hist['Volume'].iloc[-1]) if not hist.empty else None,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "company_name": info.get("longName", info.get("shortName")),
                "history": hist.to_dict('records') if not hist.empty else [],
                "timestamp": datetime.now().isoformat(),
                "period": period,
                "interval": interval,
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

    async def get_reit_data(
        self,
        ticker: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get REIT data for a specific ticker or all major REITs

        Args:
            ticker: Optional specific REIT ticker
            use_cache: Whether to use cached data

        Returns:
            Dict with REIT data and metrics
        """
        tickers = [ticker] if ticker else self.REIT_TICKERS
        cache_key = f"yfinance:reit:{ticker if ticker else 'all'}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            reit_data = []

            for tick in tickers:
                stock_data = await self.get_stock_data(tick, period="1mo", use_cache=use_cache)

                if "error" not in stock_data:
                    # Add REIT-specific metrics
                    reit_info = {
                        **stock_data,
                        "type": "REIT",
                        "is_reit": True,
                    }
                    reit_data.append(reit_info)

            result = {
                "reits": reit_data,
                "count": len(reit_data),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching REIT data: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

    async def get_market_indices(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get data for major market indices

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with market index data
        """
        cache_key = "yfinance:indices:all"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            indices_data = []

            for symbol, name in self.MARKET_INDICES.items():
                index_data = await self.get_stock_data(symbol, period="5d", use_cache=use_cache)

                if "error" not in index_data:
                    indices_data.append({
                        "symbol": symbol,
                        "name": name,
                        "value": index_data.get("current_price"),
                        "change": index_data.get("price_change"),
                        "change_pct": index_data.get("price_change_pct"),
                        "timestamp": index_data.get("timestamp"),
                    })

            result = {
                "indices": indices_data,
                "count": len(indices_data),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching market indices: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

    async def get_treasury_rates(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get current treasury rates and yields

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with treasury rate data
        """
        cache_key = "yfinance:treasury:rates"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            rates_data = []

            for symbol, name in self.RATE_INDICATORS.items():
                rate_data = await self.get_stock_data(symbol, period="5d", use_cache=use_cache)

                if "error" not in rate_data:
                    rates_data.append({
                        "symbol": symbol,
                        "name": name,
                        "rate": rate_data.get("current_price"),
                        "change": rate_data.get("price_change"),
                        "change_pct": rate_data.get("price_change_pct"),
                        "timestamp": rate_data.get("timestamp"),
                    })

            result = {
                "rates": rates_data,
                "count": len(rates_data),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching treasury rates: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

    async def get_market_summary(
        self,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive market summary including indices, REITs, and rates

        Args:
            use_cache: Whether to use cached data

        Returns:
            Dict with comprehensive market data
        """
        cache_key = "yfinance:market:summary"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            # Fetch all data in parallel would be ideal, but for now sequential
            indices = await self.get_market_indices(use_cache=use_cache)
            reits = await self.get_reit_data(use_cache=use_cache)
            rates = await self.get_treasury_rates(use_cache=use_cache)

            result = {
                "market_indices": indices,
                "reits": reits,
                "treasury_rates": rates,
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

    async def search_ticker(
        self,
        query: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Search for ticker symbols

        Args:
            query: Search query
            use_cache: Whether to use cached data

        Returns:
            Dict with search results
        """
        cache_key = f"yfinance:search:{query}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        try:
            # Try to get ticker info
            ticker = yf.Ticker(query.upper())
            info = ticker.info

            result = {
                "query": query,
                "found": bool(info.get("symbol")),
                "ticker": info.get("symbol"),
                "name": info.get("longName", info.get("shortName")),
                "type": info.get("quoteType"),
                "exchange": info.get("exchange"),
                "currency": info.get("currency"),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }

            await self.cache.set(cache_key, result, ttl=self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Error searching for ticker {query}: {str(e)}")
            return {
                "query": query,
                "found": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance",
            }
