# USA Economics Data Synchronization

## Overview

Comprehensive data synchronization script that populates the `economics_united_states` database with real economic indicators from official sources.

## Data Sources

### 1. **BLS (Bureau of Labor Statistics)** - FREE, No API Key Required
- **Employment Data**: Total nonfarm employment, hours worked, earnings
- **Labor Force**: Unemployment rate, participation rate, employment-population ratio
- **Consumer Prices**: CPI for all items, food, housing, gasoline, core CPI
- **Producer Prices**: PPI for final demand

**Categories**: `labour`, `prices`

**API**: https://api.bls.gov/publicAPI/v2/timeseries/data/

### 2. **FRED (Federal Reserve Economic Data)** - FREE API Key Required
- **GDP**: Gross Domestic Product, Real GDP, GDP growth rate
- **Interest Rates**: Federal Funds Rate, Treasury rates, mortgage rates
- **Money Supply**: M1, M2 money supply
- **Housing**: Case-Shiller index, housing starts, building permits
- **Trade**: Trade balance, imports, exports
- **Government**: Federal debt, budget deficit/surplus
- **Business**: Industrial production, consumer sentiment, retail sales

**Categories**: `gdp`, `money`, `housing`, `trade`, `government`, `business`

**API**: https://api.stlouisfed.org/fred/series

## Setup

### 1. Install Dependencies

All dependencies are already included in the project:
- `requests` - HTTP client for API calls
- `sqlalchemy` - Database ORM
- `psycopg2` - PostgreSQL adapter

### 2. Get FRED API Key (Optional but Recommended)

1. Visit: https://fred.stlouisfed.org/
2. Create free account
3. Go to: https://fred.stlouisfed.org/docs/api/api_key.html
4. Copy your API key
5. Set environment variable:
   ```bash
   export FRED_API_KEY="your_api_key_here"
   ```

**Note**: BLS data works without any API key. FRED data requires a free API key.

## Usage

### Run the Script

```bash
cd backend
python -m app.scripts.populate_usa_economics
```

### Expected Output

```
================================================================================
USA ECONOMICS DATA POPULATION
================================================================================

Country: United States
Database: economics_united_states

📊 BUREAU OF LABOR STATISTICS (BLS)
--------------------------------------------------------------------------------
✓ Stored: Unemployment Rate
✓ Stored: Labor Force Participation Rate
✓ Stored: Employment-Population Ratio
✓ Stored: Total Nonfarm Employment
✓ Stored: Average Weekly Hours - All Employees
✓ Stored: Average Hourly Earnings - All Employees
✓ Stored: Consumer Price Index (All Items)
✓ Stored: CPI - All Items Less Food & Energy
✓ Stored: CPI - Food
✓ Stored: CPI - Housing
✓ Stored: CPI - Gasoline (All Types)
✓ Stored: Producer Price Index - Final Demand

📈 FEDERAL RESERVE ECONOMIC DATA (FRED)
--------------------------------------------------------------------------------
✓ Stored: Gross Domestic Product
✓ Stored: Real Gross Domestic Product
✓ Stored: GDP Growth Rate
✓ Stored: Federal Funds Effective Rate
... (20+ more indicators)

================================================================================
SUMMARY
================================================================================
BLS indicators:  12
FRED indicators: 24
TOTAL:           36
================================================================================

✅ USA economics data populated successfully!
```

## Data Structure

Each indicator is stored with:

```python
EconomicIndicator(
    country_name="United States",
    category="labour" | "prices" | "gdp" | "money" | "housing" | "trade" | "government" | "business",
    indicator_name="Unemployment Rate",

    # Values
    last_value="4.3",              # String representation
    last_value_numeric=4.3,        # Numeric value for calculations
    previous_value="4.2",
    previous_value_numeric=4.2,
    highest_value="14.7",          # Historical high
    highest_value_numeric=14.7,
    lowest_value="3.5",            # Historical low
    lowest_value_numeric=3.5,

    # Metadata
    unit="%",                      # Unit of measurement
    frequency="Monthly",           # Update frequency
    reference_period="Oct/25",     # Period this data represents
    data_date=datetime(2025, 10, 1),
    source="U.S. Bureau of Labor Statistics",
    data_source_api="bls-api",
)
```

## Accessing the Data

### 1. API Endpoints

**List All Indicators:**
```bash
curl "http://localhost:8001/api/v1/market-intelligence/data/usa-economics?limit=20"
```

**Category Analysis:**
```bash
curl "http://localhost:8001/api/v1/market-intelligence/data/usa-economics/analysis"
```

**By Category:**
```bash
curl "http://localhost:8001/api/v1/market-intelligence/data/usa-economics/categories"
```

**Trends:**
```bash
curl "http://localhost:8001/api/v1/market-intelligence/data/usa-economics/trends"
```

### 2. Frontend Dashboard

Navigate to: **United States Economic Indicators** in the Market Intelligence section

**Features:**
- Economic health score (0-100)
- Category breakdowns (Labour, Prices, GDP, etc.)
- Key indicator trends with sparklines
- Detailed indicator tables
- Historical data visualization

## Indicators Collected

### BLS Indicators (12 total)

#### Labour (6)
- Unemployment Rate
- Labor Force Participation Rate
- Employment-Population Ratio
- Total Nonfarm Employment
- Average Weekly Hours - All Employees
- Average Hourly Earnings - All Employees

#### Prices (6)
- Consumer Price Index (All Items)
- CPI - All Items Less Food & Energy (Core CPI)
- CPI - Food
- CPI - Housing
- CPI - Gasoline (All Types)
- Producer Price Index - Final Demand

### FRED Indicators (24 total, requires API key)

#### GDP (3)
- Gross Domestic Product
- Real Gross Domestic Product
- GDP Growth Rate

#### Money (5)
- Federal Funds Effective Rate
- Federal Funds Rate (Daily)
- 10-Year Treasury Rate
- 2-Year Treasury Rate
- M2 Money Supply
- M1 Money Supply

#### Housing (4)
- 30-Year Fixed Rate Mortgage Average
- S&P/Case-Shiller U.S. National Home Price Index
- Housing Starts
- New Private Housing Units Authorized (Building Permits)

#### Trade (3)
- Trade Balance: Goods and Services
- Imports of Goods and Services
- Exports of Goods and Services

#### Government (2)
- Federal Debt: Total Public Debt
- Federal Surplus or Deficit

#### Business (3)
- Industrial Production Index
- University of Michigan Consumer Sentiment
- Retail Sales

## Update Frequency

**Manual Updates:**
```bash
cd backend
python -m app.scripts.populate_usa_economics
```

**Automated Updates (Optional):**
Set up a cron job to run the script daily/weekly:
```bash
# Run every Monday at 8am
0 8 * * 1 cd /path/to/backend && /path/to/python -m app.scripts.populate_usa_economics
```

## Error Handling

The script includes:
- **Duplicate Prevention**: Updates existing records instead of creating duplicates
- **API Retry Logic**: Handles transient network errors
- **Database Logging**: Tracks all fetch operations in `economics_fetch_log` table
- **Graceful Degradation**: BLS data works even if FRED API key is missing

## Performance

- **BLS API**: ~2-3 seconds for batch of 12 indicators
- **FRED API**: ~30-45 seconds for 24 indicators (1-2 seconds per series)
- **Database Storage**: ~100ms per indicator
- **Total Runtime**: ~60-90 seconds for complete update

## Database Schema

Tables in `economics_united_states` database:

1. **economics_indicators** - Current indicator values
2. **economics_indicator_history** - Time series data (future enhancement)
3. **economics_fetch_log** - API fetch logs
4. **economics_cache_metadata** - Cache management

## Troubleshooting

### No FRED Data

**Problem**: Script shows "Skipping FRED indicators (no API key)"

**Solution**:
1. Get free API key from https://fred.stlouisfed.org/docs/api/api_key.html
2. Set environment variable:
   ```bash
   export FRED_API_KEY="your_key_here"
   ```
3. Re-run the script

### BLS API Errors

**Problem**: BLS API returning errors or no data

**Solutions**:
- Check internet connection
- Verify BLS API is accessible: https://api.bls.gov/publicAPI/v2/timeseries/data/
- BLS API has rate limits: wait a few minutes and retry
- Check BLS API status: https://www.bls.gov/

### Database Connection Errors

**Problem**: Cannot connect to database

**Solutions**:
- Verify PostgreSQL is running: `pg_isready -h localhost -p 5432`
- Check DATABASE_URL in settings
- Ensure user has permissions to create databases

### Empty Results in Frontend

**Problem**: Frontend shows "No data available"

**Solutions**:
1. Verify data was populated:
   ```bash
   curl "http://localhost:8001/api/v1/market-intelligence/data/usa-economics?limit=5"
   ```
2. Check backend logs for errors
3. Refresh the frontend page
4. Clear browser cache

## Future Enhancements

### Planned Features

1. **Historical Data Collection**
   - Store complete time series in `economics_indicator_history`
   - Enable trend analysis and forecasting
   - Support historical comparisons

2. **Additional Data Sources**
   - Census Bureau (housing, demographics)
   - World Bank (international comparisons)
   - IMF (global economic indicators)

3. **Automated Scheduling**
   - Built-in scheduler for automatic updates
   - Configurable update frequency
   - Email notifications on failures

4. **Enhanced Analysis**
   - Correlation analysis between indicators
   - Predictive modeling (ARIMA, Prophet)
   - Economic recession probability scores

5. **Data Quality**
   - Validation rules for data integrity
   - Anomaly detection
   - Data quality scores

## API Rate Limits

### BLS API
- **Public**: 25 queries per day
- **Registered** (free): 500 queries per day
- **Batch Size**: Up to 50 series per request
- **Years**: Up to 20 years per request

### FRED API
- **Free Key**: 120 requests per minute
- **No Daily Limit**: Generous rate limits
- **Series Access**: Over 800,000 series available

## Script Architecture

```
USAEconomicsDataFetcher
├── initialize_database()      # Create database and tables
├── fetch_bls_data()           # Call BLS API
│   ├── parse_bls_series()     # Transform BLS → EconomicIndicator
│   └── fetch_bls_indicators() # Fetch all BLS series
├── fetch_fred_series()        # Call FRED API
│   ├── parse_fred_series()    # Transform FRED → EconomicIndicator
│   └── fetch_fred_indicators()# Fetch all FRED series
├── log_fetch_result()         # Log to database
└── populate_all_data()        # Main orchestration
```

## Support

For issues or questions:
1. Check logs: `backend/logs/` (if logging configured)
2. Check database logs: Query `economics_fetch_log` table
3. Review BLS API docs: https://www.bls.gov/developers/api_signature_v2.htm
4. Review FRED API docs: https://fred.stlouisfed.org/docs/api/fred/

---

**Created**: November 14, 2025
**Status**: ✅ Complete and tested
**Script**: `backend/app/scripts/populate_usa_economics.py`
**Indicators**: 12 from BLS (free), 24 from FRED (requires free API key)
**Total**: 36 economic indicators for United States
**License**: FREE - No restrictions
