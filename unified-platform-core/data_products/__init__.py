"""
Vertical-Specific Data Products

Monetizable data products and APIs across all platforms:

Finance Platform:
- Extreme Events Alerts API ($100K+/year enterprise)
- Market Regime Indicators
- Arbitrage Signals Feed

Real Estate:
- Property Valuation API
- Market Trend Predictions
- Rent Forecast Data

Bond.AI:
- Network Intelligence API
- Relationship Scoring Service
- Opportunity Detection Feed

Labor:
- Career Trajectory Data
- Skills Market Intelligence
- Salary Benchmarks

Revenue Potential: $50M+ ARR from data products alone
"""

__version__ = "1.0.0"

from .api_gateway import DataProductGateway, ProductType
from .metering import UsageMetering, PricingTier
from .products.finance_data_products import (
    ExtremeEventsAlertsAPI,
    MarketRegimeIndicators,
    ArbitrageSignalsFeed,
    create_finance_data_products_router
)
from .products.real_estate_data_products import (
    PropertyValuationAPI,
    MarketIntelligenceFeed,
    DealFlowAlertsAPI,
    create_real_estate_data_products_router
)
from .products.labor_data_products import (
    SkillDemandForecastsAPI,
    SalaryIntelligenceAPI,
    WorkforceAnalyticsAPI,
    create_labor_data_products_router
)

__all__ = [
    "DataProductGateway",
    "ProductType",
    "UsageMetering",
    "PricingTier",
    # Finance Products
    "ExtremeEventsAlertsAPI",
    "MarketRegimeIndicators",
    "ArbitrageSignalsFeed",
    "create_finance_data_products_router",
    # Real Estate Products
    "PropertyValuationAPI",
    "MarketIntelligenceFeed",
    "DealFlowAlertsAPI",
    "create_real_estate_data_products_router",
    # Labor Products
    "SkillDemandForecastsAPI",
    "SalaryIntelligenceAPI",
    "WorkforceAnalyticsAPI",
    "create_labor_data_products_router"
]
