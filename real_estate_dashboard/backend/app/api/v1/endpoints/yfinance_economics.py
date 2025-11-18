"""
YFinance and Economics API Endpoints for Market Intelligence

Provides endpoints for fetching market data from Yahoo Finance and macroeconomic
data from economics-api microservice.
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.yfinance_service import YFinanceService
from app.services.economics_api_service import EconomicsAPIService

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# Response Models
# ============================================================================

class StockDataResponse(BaseModel):
    """Stock data response model"""
    ticker: str
    current_price: Optional[float]
    currency: str = "USD"
    price_change: Optional[float]
    price_change_pct: Optional[float]
    volume: Optional[int]
    market_cap: Optional[int]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    sector: Optional[str]
    industry: Optional[str]
    company_name: Optional[str]
    timestamp: str
    data_source: str = "yfinance"
    error: Optional[str] = None


class REITDataResponse(BaseModel):
    """REIT data response model"""
    reits: List[StockDataResponse]
    count: int
    timestamp: str
    data_source: str = "yfinance"


class MarketIndicesResponse(BaseModel):
    """Market indices response model"""
    indices: List[dict]
    count: int
    timestamp: str
    data_source: str = "yfinance"


class TreasuryRatesResponse(BaseModel):
    """Treasury rates response model"""
    rates: List[dict]
    count: int
    timestamp: str
    data_source: str = "yfinance"


class MarketSummaryResponse(BaseModel):
    """Comprehensive market summary response model"""
    market_indices: MarketIndicesResponse
    reits: REITDataResponse
    treasury_rates: TreasuryRatesResponse
    timestamp: str
    data_source: str = "yfinance"


class EconomicIndicatorResponse(BaseModel):
    """Economic indicator response model"""
    country: str
    category: str
    data: dict
    timestamp: str
    data_source: str = "economics-api"
    error: Optional[str] = None


class EconomicSummaryResponse(BaseModel):
    """Economic summary response model"""
    countries: List[dict]
    count: int
    timestamp: str
    data_source: str = "economics-api"


# ============================================================================
# YFinance Endpoints
# ============================================================================

@router.get(
    "/yfinance/stock/{ticker}",
    response_model=StockDataResponse,
    summary="Get stock data from Yahoo Finance",
    description="Fetch historical and current data for a specific stock ticker"
)
async def get_stock_data(
    ticker: str,
    period: str = Query("1mo", description="Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"),
    interval: str = Query("1d", description="Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get stock data for a specific ticker"""
    try:
        service = YFinanceService()
        data = await service.get_stock_data(
            ticker=ticker.upper(),
            period=period,
            interval=interval,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
        # Return graceful fallback instead of raising exception
        return StockDataResponse(
            ticker=ticker.upper(),
            current_price=None,
            currency="USD",
            price_change=None,
            price_change_pct=None,
            volume=None,
            market_cap=None,
            pe_ratio=None,
            dividend_yield=None,
            sector=None,
            industry=None,
            company_name=None,
            timestamp=datetime.now().isoformat(),
            data_source="yfinance",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/yfinance/reits",
    response_model=REITDataResponse,
    summary="Get REIT data from Yahoo Finance",
    description="Fetch data for major REITs and Real Estate ETFs"
)
async def get_reit_data(
    ticker: Optional[str] = Query(None, description="Specific REIT ticker (optional)"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get REIT data for all major REITs or a specific ticker"""
    try:
        service = YFinanceService()
        data = await service.get_reit_data(ticker=ticker, use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching REIT data: {str(e)}")
        # Return graceful fallback
        return REITDataResponse(
            reits=[],
            count=0,
            timestamp=datetime.now().isoformat(),
            data_source="yfinance"
        )


@router.get(
    "/yfinance/indices",
    response_model=MarketIndicesResponse,
    summary="Get market indices from Yahoo Finance",
    description="Fetch current data for major market indices (S&P 500, Dow Jones, NASDAQ, Russell 2000, VIX)"
)
async def get_market_indices(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get data for major market indices"""
    try:
        service = YFinanceService()
        data = await service.get_market_indices(use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching market indices: {str(e)}")
        # Return graceful fallback
        return MarketIndicesResponse(
            indices=[],
            count=0,
            timestamp=datetime.now().isoformat(),
            data_source="yfinance"
        )


@router.get(
    "/yfinance/treasury-rates",
    response_model=TreasuryRatesResponse,
    summary="Get treasury rates from Yahoo Finance",
    description="Fetch current treasury rates and yields (13-week, 5-year, 10-year, 30-year)"
)
async def get_treasury_rates(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get current treasury rates and yields"""
    try:
        service = YFinanceService()
        data = await service.get_treasury_rates(use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching treasury rates: {str(e)}")
        # Return graceful fallback
        return TreasuryRatesResponse(
            rates=[],
            count=0,
            timestamp=datetime.now().isoformat(),
            data_source="yfinance"
        )


@router.get(
    "/yfinance/market-summary",
    response_model=MarketSummaryResponse,
    summary="Get comprehensive market summary",
    description="Fetch comprehensive market data including indices, REITs, and treasury rates"
)
async def get_market_summary(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get comprehensive market summary"""
    try:
        service = YFinanceService()
        data = await service.get_market_summary(use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching market summary: {str(e)}")
        # Return graceful fallback with empty data structures
        timestamp = datetime.now().isoformat()
        return MarketSummaryResponse(
            market_indices=MarketIndicesResponse(
                indices=[],
                count=0,
                timestamp=timestamp,
                data_source="yfinance"
            ),
            reits=REITDataResponse(
                reits=[],
                count=0,
                timestamp=timestamp,
                data_source="yfinance"
            ),
            treasury_rates=TreasuryRatesResponse(
                rates=[],
                count=0,
                timestamp=timestamp,
                data_source="yfinance"
            ),
            timestamp=timestamp,
            data_source="yfinance"
        )


@router.get(
    "/yfinance/search",
    summary="Search for ticker symbols",
    description="Search for ticker symbols and get basic information"
)
async def search_ticker(
    query: str = Query(..., description="Search query (ticker symbol)"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Search for ticker symbols"""
    try:
        service = YFinanceService()
        data = await service.search_ticker(query=query, use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error searching for ticker {query}: {str(e)}")
        # Return graceful fallback
        return {
            "query": query,
            "found": False,
            "error": f"Can't extract data: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "data_source": "yfinance"
        }


# ============================================================================
# Economics API Endpoints
# ============================================================================

@router.get(
    "/economics/country/{country}/overview",
    response_model=EconomicIndicatorResponse,
    summary="Get country economic overview",
    description="Fetch economic overview for a specific country"
)
async def get_country_overview(
    country: str,
    related: Optional[str] = Query(None, description="Filter for related indicators (e.g., 'Inflation Rate')"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get economic overview for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_country_overview(
            country=country.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching country overview for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category="overview",
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/country/{country}/{category}",
    response_model=EconomicIndicatorResponse,
    summary="Get economic indicator by category",
    description="Fetch specific economic indicator data for a country"
)
async def get_economic_indicator(
    country: str,
    category: str,
    related: Optional[str] = Query(None, description="Filter for related indicators"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get specific economic indicator data for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_economic_indicator(
            country=country.lower(),
            category=category.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching {category} data for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category=category.lower(),
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/gdp/{country}",
    response_model=EconomicIndicatorResponse,
    summary="Get GDP data",
    description="Fetch GDP data for a specific country"
)
async def get_gdp_data(
    country: str,
    related: Optional[str] = Query(None, description="Filter for related indicators"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get GDP data for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_gdp_data(
            country=country.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching GDP data for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category="gdp",
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/labour/{country}",
    response_model=EconomicIndicatorResponse,
    summary="Get labour/employment data",
    description="Fetch labour and employment data for a specific country"
)
async def get_labour_data(
    country: str,
    related: Optional[str] = Query(None, description="Filter for related indicators"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get labour/employment data for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_labour_data(
            country=country.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching labour data for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category="labour",
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/housing/{country}",
    response_model=EconomicIndicatorResponse,
    summary="Get housing market data",
    description="Fetch housing market data for a specific country"
)
async def get_housing_data(
    country: str,
    related: Optional[str] = Query(None, description="Filter for related indicators"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get housing market data for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_housing_data(
            country=country.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching housing data for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category="housing",
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/interest-rates/{country}",
    response_model=EconomicIndicatorResponse,
    summary="Get interest rate data",
    description="Fetch interest rate and monetary data for a specific country"
)
async def get_interest_rates(
    country: str,
    related: Optional[str] = Query(None, description="Filter for related indicators"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get interest rate and monetary data for a country"""
    try:
        service = EconomicsAPIService()
        data = await service.get_interest_rates(
            country=country.lower(),
            related=related,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching interest rate data for {country}: {str(e)}")
        # Return graceful fallback
        return EconomicIndicatorResponse(
            country=country.lower(),
            category="money",
            data={},
            timestamp=datetime.now().isoformat(),
            data_source="economics-api",
            error=f"Can't extract data: {str(e)}"
        )


@router.get(
    "/economics/calendar",
    summary="Get economic calendar",
    description="Fetch economic calendar with upcoming events"
)
async def get_economic_calendar(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get economic calendar with upcoming events"""
    try:
        service = EconomicsAPIService()
        data = await service.get_economic_calendar(use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching economic calendar: {str(e)}")
        # Return graceful fallback
        return {
            "calendar": [],
            "error": f"Can't extract data: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "data_source": "economics-api"
        }


@router.get(
    "/economics/countries-overview",
    summary="Get overview for all countries",
    description="Fetch economic overview data for all available countries"
)
async def get_countries_overview(
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get overview data for all countries"""
    try:
        service = EconomicsAPIService()
        data = await service.get_countries_overview(use_cache=use_cache)
        return data
    except Exception as e:
        logger.error(f"Error fetching countries overview: {str(e)}")
        # Return graceful fallback
        return {
            "countries": [],
            "count": 0,
            "error": f"Can't extract data: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "data_source": "economics-api"
        }


@router.get(
    "/economics/summary",
    response_model=EconomicSummaryResponse,
    summary="Get comprehensive economic summary",
    description="Fetch comprehensive economic data for key countries"
)
async def get_economic_summary(
    countries: Optional[List[str]] = Query(None, description="List of countries (default: key countries)"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get comprehensive economic summary for key countries"""
    try:
        service = EconomicsAPIService()
        data = await service.get_market_intelligence_summary(
            countries=countries,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error fetching economic summary: {str(e)}")
        # Return graceful fallback
        return EconomicSummaryResponse(
            countries=[],
            count=0,
            timestamp=datetime.now().isoformat(),
            data_source="economics-api"
        )


@router.get(
    "/economics/compare",
    summary="Compare countries",
    description="Compare economic indicators across multiple countries"
)
async def compare_countries(
    countries: List[str] = Query(..., description="List of countries to compare"),
    indicators: Optional[List[str]] = Query(None, description="List of indicators to compare (default: overview, gdp, labour, housing)"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Compare economic indicators across multiple countries"""
    try:
        service = EconomicsAPIService()
        data = await service.compare_countries(
            countries=countries,
            indicators=indicators,
            use_cache=use_cache
        )
        return data
    except Exception as e:
        logger.error(f"Error comparing countries: {str(e)}")
        # Return graceful fallback
        return {
            "comparison": {},
            "countries": countries,
            "indicators": indicators or ["overview", "gdp", "labour", "housing"],
            "error": f"Can't extract data: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "data_source": "economics-api"
        }


# ============================================================================
# Combined Market Intelligence Endpoint
# ============================================================================

@router.get(
    "/market-intelligence/comprehensive",
    summary="Get comprehensive market intelligence",
    description="Fetch comprehensive market intelligence including stocks, REITs, indices, treasury rates, and economic indicators"
)
async def get_comprehensive_market_intelligence(
    countries: Optional[List[str]] = Query(None, description="Countries for economic data"),
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """Get comprehensive market intelligence from all sources"""
    try:
        yfinance_service = YFinanceService()
        economics_service = EconomicsAPIService()

        # Fetch all data with individual error handling
        try:
            market_summary = await yfinance_service.get_market_summary(use_cache=use_cache)
        except Exception as market_err:
            logger.error(f"Error fetching market data: {str(market_err)}")
            timestamp = datetime.now().isoformat()
            market_summary = {
                "market_indices": {"indices": [], "count": 0, "timestamp": timestamp},
                "reits": {"reits": [], "count": 0, "timestamp": timestamp},
                "treasury_rates": {"rates": [], "count": 0, "timestamp": timestamp},
                "error": f"Can't extract market data: {str(market_err)}",
                "timestamp": timestamp
            }

        try:
            economic_summary = await economics_service.get_market_intelligence_summary(
                countries=countries,
                use_cache=use_cache
            )
        except Exception as econ_err:
            logger.error(f"Error fetching economic data: {str(econ_err)}")
            economic_summary = {
                "countries": [],
                "count": 0,
                "error": f"Can't extract economic data: {str(econ_err)}",
                "timestamp": datetime.now().isoformat()
            }

        result = {
            "market_data": market_summary,
            "economic_data": economic_summary,
            "timestamp": datetime.now().isoformat(),
            "data_sources": ["yfinance", "economics-api"],
            "has_errors": "error" in market_summary or "error" in economic_summary
        }

        return result
    except Exception as e:
        logger.error(f"Error fetching comprehensive market intelligence: {str(e)}")
        # Return comprehensive fallback
        timestamp = datetime.now().isoformat()
        return {
            "market_data": {
                "market_indices": {"indices": [], "count": 0, "timestamp": timestamp},
                "reits": {"reits": [], "count": 0, "timestamp": timestamp},
                "treasury_rates": {"rates": [], "count": 0, "timestamp": timestamp},
                "error": f"Can't extract market data",
                "timestamp": timestamp
            },
            "economic_data": {
                "countries": [],
                "count": 0,
                "error": f"Can't extract economic data",
                "timestamp": timestamp
            },
            "timestamp": timestamp,
            "data_sources": ["yfinance", "economics-api"],
            "has_errors": True,
            "error": f"Can't extract data: {str(e)}"
        }
