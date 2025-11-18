# Official Government Data Integrations

Comprehensive guide to accessing official government data through the Real Estate Dashboard.

## Overview

The dashboard now includes **5 FREE official government data sources** that require **NO API keys**:

### 🇺🇸 **US Government Data**
1. **Data.gov** - 300,000+ federal, state, and local datasets
2. **HUD** - Housing and Urban Development data
3. **FHFA** - Federal Housing Finance Agency house price data

### 🇮🇱 **Israeli Government Data**
4. **Data.gov.il** - Israeli government open data portal
5. **Bank of Israel** - Central bank economic data

---

## Quick Start

### 1. Enable Official Data Integrations (Enabled by Default)

The official data integrations are **enabled by default** and require **no API keys**:

```bash
# In backend/.env
ENABLE_DATAGOV_US_INTEGRATION=True
ENABLE_DATAGOV_IL_INTEGRATION=True
ENABLE_BANK_OF_ISRAEL_INTEGRATION=True
ENABLE_HUD_INTEGRATION=True
ENABLE_FHFA_INTEGRATION=True
```

### 2. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 3. Access Official Data

Visit the Integrations page or use the API:
```bash
# Check status
curl http://localhost:8000/api/v1/integrations/status

# Search US datasets
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/search?query=real%20estate"
```

---

## US Government Data Sources

### 📊 Data.gov (US)

**300,000+ datasets** from federal, state, and local governments

#### Features
- Search across all government datasets
- Filter by tags and organizations
- Real estate and housing datasets
- Federal property data
- Economic indicators
- Free, no API key required

#### API Endpoints

**Search Datasets**:
```bash
GET /api/v1/integrations/official-data/datagov-us/search

Parameters:
- query: Search query (e.g., "real estate", "housing")
- tags: Comma-separated tags (e.g., "real-estate,housing")
- limit: Number of results (1-1000, default: 20)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/search?query=housing&tags=real-estate&limit=50"
```

**Get Dataset Details**:
```bash
GET /api/v1/integrations/official-data/datagov-us/dataset/{dataset_id}

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/dataset/federal-real-property-profile"
```

**Get Real Estate Datasets**:
```bash
GET /api/v1/integrations/official-data/datagov-us/real-estate

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/real-estate?limit=100"
```

**List Organizations**:
```bash
GET /api/v1/integrations/official-data/datagov-us/organizations

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/organizations"
```

---

### 🏘️ HUD (Housing & Urban Development)

**Official US housing data** including Fair Market Rents and income limits

#### Features
- Fair Market Rents (FMR) by ZIP code
- Area Median Income (AMI) data
- Income limits for affordable housing programs
- Public housing statistics
- Homelessness data
- Free, no API key required

#### API Endpoints

**Get Fair Market Rent**:
```bash
GET /api/v1/integrations/official-data/hud/fair-market-rent

Parameters:
- zip_code: 5-digit ZIP code (required)
- year: Year (optional, defaults to current year)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/hud/fair-market-rent?zip_code=10001&year=2024"
```

**Get Income Limits**:
```bash
GET /api/v1/integrations/official-data/hud/income-limits

Parameters:
- state_code: 2-letter state code (required)
- county: County name (optional)
- year: Year (optional)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/hud/income-limits?state_code=CA&county=Los%20Angeles&year=2024"
```

**Get Public Housing Data**:
```bash
GET /api/v1/integrations/official-data/hud/public-housing

Parameters:
- state: State code (optional)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/hud/public-housing?state=NY"
```

---

### 📈 FHFA (Federal Housing Finance Agency)

**Official US House Price Index** from 1975 to present

#### Features
- National, state, metro, and ZIP code level data
- Purchase-Only Index
- All-Transactions Index
- Quarterly updates
- Historical data from 1975
- Free downloadable CSV datasets
- No API key required

#### API Endpoints

**Get House Price Index**:
```bash
GET /api/v1/integrations/official-data/fhfa/house-price-index

Parameters:
- geography_type: "national", "state", "metro", or "zip" (default: national)
- frequency: "monthly", "quarterly", or "annual" (default: quarterly)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/house-price-index?geography_type=state&frequency=quarterly"
```

**Get State HPI**:
```bash
GET /api/v1/integrations/official-data/fhfa/state-hpi/{state_code}

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/state-hpi/CA"
```

**Get ZIP Code HPI**:
```bash
GET /api/v1/integrations/official-data/fhfa/zip-hpi/{zip_code}

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/zip-hpi/90210"
```

**Get Download Links**:
```bash
GET /api/v1/integrations/official-data/fhfa/download-links

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/download-links"
```

---

## Israeli Government Data Sources

### 🇮🇱 Data.gov.il (Israel)

**Israeli government open data portal** with thousands of datasets

#### Features
- Search Israeli government datasets
- Property and land registry data
- Economic indicators
- Municipal and infrastructure data
- Real estate permits and approvals
- Hebrew and English support
- Free, no API key required

#### API Endpoints

**Search Datasets**:
```bash
GET /api/v1/integrations/official-data/datagov-il/search

Parameters:
- query: Search query (Hebrew or English)
- limit: Number of results (1-1000, default: 20)

Examples:
# English
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-il/search?query=real%20estate"

# Hebrew
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-il/search?query=נדל״ן"
```

**Get Dataset Details**:
```bash
GET /api/v1/integrations/official-data/datagov-il/dataset/{dataset_id}

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-il/dataset/property-permits"
```

**Get Real Estate Datasets**:
```bash
GET /api/v1/integrations/official-data/datagov-il/real-estate

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-il/real-estate"
```

**List Tags**:
```bash
GET /api/v1/integrations/official-data/datagov-il/tags

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-il/tags"
```

---

### 🏦 Bank of Israel

**Israeli central bank economic and statistical data**

#### Features
- Interest rates
- Consumer Price Index (CPI)
- Housing price index
- Exchange rates
- Composite economic index
- GDP data
- Employment statistics
- Free, no API key required

#### API Endpoints

**Get Interest Rate**:
```bash
GET /api/v1/integrations/official-data/bank-of-israel/interest-rate

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/interest-rate"
```

**Get CPI (Consumer Price Index)**:
```bash
GET /api/v1/integrations/official-data/bank-of-israel/cpi

Parameters:
- start_date: Start date in YYYY-MM format (optional)
- end_date: End date in YYYY-MM format (optional)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/cpi?start_date=2023-01&end_date=2024-01"
```

**Get Housing Price Index**:
```bash
GET /api/v1/integrations/official-data/bank-of-israel/housing-price-index

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/housing-price-index"
```

**Get Exchange Rates**:
```bash
GET /api/v1/integrations/official-data/bank-of-israel/exchange-rates

Parameters:
- currency: Currency code (default: USD)

Example:
curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/exchange-rates?currency=EUR"
```

---

## Database Storage

All official data can be saved to the database for caching and analysis:

### Database Models

```python
# Official Dataset Metadata
OfficialDataset
- source (datagov_us, datagov_il, etc.)
- dataset_id, name, description
- organization, publisher
- tags, categories
- resources (list of files/APIs)
- dataset_url, api_url

# Data Records
OfficialDataRecord
- dataset_id (foreign key)
- data_type, category
- geographic info (country, state, county, city, ZIP)
- temporal info (year, quarter, month, date)
- value, value_type
- full data payload (JSON)

# Housing Price Index
HousingPriceIndex
- source (fhfa, fred, boi)
- geography (national, state, metro, ZIP)
- index values and changes
- quarterly/monthly data

# Economic Indicators
EconomicIndicator
- source, country
- indicator (interest_rate, cpi, gdp, unemployment)
- temporal data
- values and changes

# Fair Market Rents
FairMarketRent
- geographic info
- FMR values by bedroom count
- year, percentile
```

### Example: Saving Data.gov Dataset to Database

```python
from app.models.official_data import OfficialDataset
from app.integrations.manager import integration_manager

# Get dataset from Data.gov
datagov = integration_manager.get("datagov_us")
result = await datagov.get_dataset("federal-real-property")

# Save to database
if result.success:
    dataset = OfficialDataset(
        source="datagov_us",
        dataset_id=result.data["dataset"]["id"],
        name=result.data["dataset"]["title"],
        description=result.data["dataset"]["notes"],
        organization=result.data["dataset"]["organization"]["title"],
        tags=result.data["dataset"]["tags"],
        resources=result.data["dataset"]["resources"],
        dataset_url=result.data["dataset"]["url"]
    )
    db.add(dataset)
    db.commit()
```

---

## Use Cases

### Real Estate Investment Analysis

1. **Market Research**:
   ```bash
   # Get housing datasets
   curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/real-estate"

   # Get house price trends
   curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/state-hpi/CA"
   ```

2. **Rental Market Analysis**:
   ```bash
   # Get Fair Market Rents for area
   curl "http://localhost:8000/api/v1/integrations/official-data/hud/fair-market-rent?zip_code=90210"
   ```

3. **Economic Indicators**:
   ```bash
   # Get interest rates
   curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/interest-rate"
   ```

### Affordable Housing Development

1. **Income Limits**:
   ```bash
   # Get AMI and income limits
   curl "http://localhost:8000/api/v1/integrations/official-data/hud/income-limits?state_code=CA"
   ```

2. **Property Data**:
   ```bash
   # Search for affordable housing datasets
   curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/search?query=affordable%20housing"
   ```

### Market Intelligence

1. **Price Trends**:
   ```bash
   # National HPI
   curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/house-price-index?geography_type=national"

   # Metro HPI
   curl "http://localhost:8000/api/v1/integrations/official-data/fhfa/house-price-index?geography_type=metro"
   ```

2. **Economic Data**:
   ```bash
   # Israeli CPI
   curl "http://localhost:8000/api/v1/integrations/official-data/bank-of-israel/cpi"
   ```

---

## Benefits

### ✅ Completely Free
- No API keys required
- No usage limits
- No subscription fees
- Official government data

### ✅ Authoritative Data
- Direct from government sources
- Official statistics
- Regularly updated
- High quality and accuracy

### ✅ Comprehensive Coverage
- 300,000+ US datasets
- Thousands of Israeli datasets
- Federal, state, and local data
- Historical and current data

### ✅ Real Estate Focus
- Housing price indexes
- Fair market rents
- Property datasets
- Economic indicators
- Market trends

### ✅ Easy Integration
- Simple REST API
- JSON responses
- Database storage models
- Automatic initialization

---

## Data Sources

### US Sources
- **Data.gov**: https://catalog.data.gov/
- **HUD**: https://www.hud.gov/
- **FHFA**: https://www.fhfa.gov/DataTools/Downloads

### Israeli Sources
- **Data.gov.il**: https://data.gov.il/
- **Bank of Israel**: https://www.boi.org.il/en/economic-roles/statistics/

---

## Future Enhancements

Potential additions:
- State-level open data portals
- City/municipal data sources
- International government data
- Automated data refreshing
- Data visualization dashboards
- Trend analysis tools
- Predictive analytics

---

## Support

For issues or questions:
1. Check the integration status: `GET /api/v1/integrations/status`
2. Test individual integrations: `GET /api/v1/integrations/test/{integration_key}`
3. Review server logs for errors
4. Consult official data source documentation

---

## License

All data sources are provided by government agencies and are public domain or openly licensed. Check individual data source licenses for specific terms.
