# Economics API Integration Guide

## Overview

This document describes the integration of the **Sugra AI Economics API** into the Real Estate Dashboard platform. The Economics API provides comprehensive macroeconomic data including GDP, employment, inflation, trade, housing, and other economic indicators for countries worldwide.

## API Configuration

### 1. Get Your API Key

You need to obtain an API key from Sugra AI to use the Economics API.

### 2. Configure Environment Variables

Add the following to your `.env` file:

```bash
# Economics API Configuration (Sugra AI)
ECONOMICS_API_BASE_URL=https://api.sugra.ai
ECONOMICS_API_KEY=your_actual_api_key_here
ENABLE_ECONOMICS_API=True
```

**Important:** Replace `your_actual_api_key_here` with your real API key.

## Available Endpoints

### Backend API Endpoints

The following REST API endpoints are available:

#### 1. Countries Overview
```
GET /api/v1/economics/countries-overview
```
Returns economic overview for all countries (GDP, inflation, unemployment, etc.)

#### 2. Country-Specific Overview
```
GET /api/v1/economics/country/{country}/overview
```
Example: `/api/v1/economics/country/united-states/overview`

#### 3. GDP Indicators
```
GET /api/v1/economics/gdp/{country}
```
Returns GDP growth rates, per capita, sectoral breakdowns

#### 4. Labour Indicators
```
GET /api/v1/economics/labour/{country}
```
Returns unemployment, payrolls, wages, job claims data

#### 5. Prices/Inflation Indicators
```
GET /api/v1/economics/country/{country}/prices
```
Returns inflation, CPI, producer prices, deflators

#### 6. Housing Indicators
```
GET /api/v1/economics/housing/{country}
```
Returns housing starts, permits, prices, mortgage rates

#### 7. Interest Rates / Money Indicators
```
GET /api/v1/economics/interest-rates/{country}
```
Returns interest rates, money supply, central bank metrics

#### 8. Trade Indicators
```
GET /api/v1/economics/country/{country}/trade
```
Returns balance of trade, exports/imports, FDI, reserves

#### 9. Government Indicators
```
GET /api/v1/economics/country/{country}/government
```
Returns government debt, budget, spending, tax rates

#### 10. Business Indicators
```
GET /api/v1/economics/country/{country}/business
```
Returns PMI, industrial production, inventories, confidence

#### 11. Consumer Indicators
```
GET /api/v1/economics/country/{country}/consumer
```
Returns retail sales, confidence, spending, debt levels

#### 12. Compare Countries
```
GET /api/v1/economics/compare?countries=united-states&countries=china
```
Compare economic indicators across multiple countries

#### 13. Market Intelligence Summary
```
GET /api/v1/economics/summary
```
Returns comprehensive economic data for key countries

#### 14. Comprehensive Market Intelligence
```
GET /api/v1/market-intelligence/comprehensive
```
Combines YFinance market data with economics data

## Country Names Format

Countries should be specified in lowercase with hyphens:
- `united-states`
- `united-kingdom`
- `israel`
- `china`
- `japan`
- `germany`
- `france`
- `canada`
- `australia`

## Testing the Integration

### Option 1: Run the Test Script

We've created a comprehensive test script that tests all endpoints:

```bash
cd /home/user/real_estate_dashboard/backend

# Run with API key from .env file
python3 test_economics_api.py

# Or run with API key as argument
python3 test_economics_api.py YOUR_API_KEY
```

The test script will:
- Test all 12 economic indicator categories
- Test both direct HTTP calls and service wrapper calls
- Test multiple countries (US, Israel, China, etc.)
- Generate a detailed test report (`economics_api_test_results.json`)
- Show pass/fail status for each test

### Option 2: Test with cURL

Test the countries overview endpoint directly:

```bash
curl -X GET "https://api.sugra.ai/v1/economics/countries-overview?country=null" \
  -H "x-api-key: YOUR_API_KEY"
```

Test a specific country (United States):

```bash
curl -X GET "https://api.sugra.ai/v1/economics/united-states/overview" \
  -H "x-api-key: YOUR_API_KEY"
```

### Option 3: Test via Backend API

Start the backend server:

```bash
cd /home/user/real_estate_dashboard/backend
uvicorn app.main:app --reload --port 8000
```

Then test the endpoints:

```bash
# Get all countries overview
curl http://localhost:8000/api/v1/economics/countries-overview

# Get US GDP data
curl http://localhost:8000/api/v1/economics/gdp/united-states

# Get US housing data
curl http://localhost:8000/api/v1/economics/housing/united-states

# Compare countries
curl "http://localhost:8000/api/v1/economics/compare?countries=united-states&countries=israel"
```

## Python Service Usage

You can use the `EconomicsAPIService` directly in your Python code:

```python
from app.services.economics_api_service import EconomicsAPIService

# Initialize service (uses API key from settings)
service = EconomicsAPIService()

# Get countries overview
countries_data = await service.get_countries_overview()

# Get US housing data
us_housing = await service.get_housing_data("united-states")

# Get GDP data for multiple countries
us_gdp = await service.get_gdp_data("united-states")
israel_gdp = await service.get_gdp_data("israel")

# Compare countries
comparison = await service.compare_countries(
    countries=["united-states", "israel", "china"],
    indicators=["gdp", "housing", "labour"]
)

# Get comprehensive market intelligence
summary = await service.get_market_intelligence_summary()
```

## Economic Categories

The API provides data in these categories:

| Category | Description | Example Indicators |
|----------|-------------|-------------------|
| **Overview** | General economic snapshot | Currency, stock market, GDP growth, unemployment, inflation |
| **GDP** | Economic output | Growth rates, per capita, sectoral breakdowns |
| **Labour** | Employment data | Unemployment rate, payrolls, wages, job claims |
| **Prices** | Inflation metrics | CPI, producer prices, deflators |
| **Money** | Monetary policy | Interest rates, money supply, central bank rates |
| **Trade** | International trade | Balance of trade, exports/imports, FDI, reserves |
| **Government** | Fiscal policy | Debt, budget, spending, tax rates |
| **Business** | Business activity | PMI, industrial production, inventories, confidence |
| **Consumer** | Consumer metrics | Retail sales, confidence, spending, debt |
| **Housing** | Real estate market | Starts, permits, prices, mortgage rates |

## Response Format

All endpoints return data in this format:

```json
{
  "country": "united-states",
  "category": "housing",
  "data": [
    {
      "Country": "United States",
      "Category": "Housing Starts",
      "LatestValue": "1.37M",
      "Frequency": "Monthly",
      "Unit": "Thousands",
      "LastUpdate": "2024-01-01",
      "Source": "U.S. Census Bureau"
    }
  ],
  "timestamp": "2025-11-13T10:30:00",
  "data_source": "economics-api"
}
```

## Caching

- All economics data is cached for **1 hour** by default (configurable)
- Cache uses Redis if enabled, otherwise in-memory cache
- To bypass cache, use `use_cache=False` parameter

## Error Handling

The service includes comprehensive error handling:

- Network errors are logged and returned in response
- Invalid countries or categories return helpful error messages
- API rate limits are respected (cached responses reduce API calls)
- Timeout after 10 seconds (configurable)

## Integration with Market Intelligence

The economics data integrates with the existing market intelligence system:

```python
# Get comprehensive market data (stocks + economics)
response = requests.get(
    "http://localhost:8000/api/v1/market-intelligence/comprehensive",
    params={"countries": ["united-states", "israel"]}
)
```

This combines:
- YFinance stock/REIT/treasury data
- Economics API macroeconomic indicators
- Unified timestamp and caching

## Performance Considerations

1. **Caching**: Use caching to reduce API calls and improve response times
2. **Batch Requests**: Use the comparison or summary endpoints to get data for multiple countries in one call
3. **Selective Data**: Request only the categories you need
4. **Background Jobs**: For scheduled updates, use Celery tasks to fetch and cache data periodically

## Troubleshooting

### API Key Not Working

1. Verify your API key is correct
2. Check the key has proper permissions
3. Ensure the key is not expired
4. Test with direct cURL call first

### No Data Returned

1. Check if the country name is formatted correctly (lowercase, hyphens)
2. Verify the category exists
3. Check API logs for errors
4. Test with a known working country like "united-states"

### Timeout Errors

1. Increase timeout in settings: `CACHE_ECONOMIC_INDICATORS_TTL`
2. Check network connectivity to api.sugra.ai
3. Enable caching to reduce API calls

### Cache Issues

1. Ensure Redis is running: `redis-cli ping`
2. Check Redis connection: `REDIS_URL` in .env
3. Clear cache: `redis-cli FLUSHDB`

## Files Modified/Created

### Modified Files:
- `backend/app/settings.py` - Added economics API configuration
- `backend/app/services/economics_api_service.py` - Updated base URL and added authentication
- `backend/.env.example` - Added economics API variables

### Created Files:
- `backend/test_economics_api.py` - Comprehensive test script
- `docs/ECONOMICS_API_INTEGRATION.md` - This documentation file

## Example Response Data

### Countries Overview Response:
```json
[
  {
    "Country": "United States",
    "Current Account": "-3.70",
    "Debt/GDP": "129.00",
    "GDP": "25440",
    "GDP Growth": "3.30",
    "Gov. Budget": "-5.80",
    "Inflation Rate": "3.40",
    "Interest Rate": "5.50",
    "Jobless Rate": "3.70",
    "Population": "334.23"
  },
  {
    "Country": "China",
    "Current Account": "2.20",
    "Debt/GDP": "77.10",
    "GDP": "17963",
    "GDP Growth": "1.00",
    "Gov. Budget": "-7.40",
    "Inflation Rate": "-0.30",
    "Interest Rate": "3.45",
    "Jobless Rate": "5.10",
    "Population": "1409.67"
  }
]
```

## Next Steps

1. **Get your API key** from Sugra AI
2. **Update .env file** with your API key
3. **Run the test script** to verify everything works
4. **Start using** the economics endpoints in your application
5. **Monitor usage** and adjust caching as needed

## Support

For issues with the Economics API:
- Check the test script output
- Review API logs: `backend/logs/app.log`
- Consult Sugra AI documentation
- Contact Sugra AI support for API-specific issues

## Future Enhancements

Potential improvements:
- [ ] Add historical data endpoints
- [ ] Implement webhooks for real-time updates
- [ ] Add more country-specific indicators
- [ ] Create visualization dashboard for economic data
- [ ] Add alerts for significant economic changes
- [ ] Integrate with property valuation models
