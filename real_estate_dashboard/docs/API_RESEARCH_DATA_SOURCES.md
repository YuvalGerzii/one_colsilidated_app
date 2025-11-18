# Real Estate Data Sources - Comprehensive API Research

**Date:** 2025-11-09
**Purpose:** Deep dive analysis of data source integrations for real estate dashboard

---

## Table of Contents

1. [Government & Official Data Sources (FREE)](#government--official-data-sources-free)
2. [Commercial Real Estate APIs (PAID)](#commercial-real-estate-apis-paid)
3. [Residential Real Estate APIs](#residential-real-estate-apis)
4. [Environmental & Risk Data](#environmental--risk-data)
5. [Implementation Priority](#implementation-priority)
6. [API Comparison Matrix](#api-comparison-matrix)

---

## Government & Official Data Sources (FREE)

### 1. US Census Bureau API

**Official Documentation:** https://www.census.gov/data/developers/guidance/api-user-guide.html
**API Key:** Required (Free) - https://api.census.gov/data/key_signup.html
**Rate Limits:** None specified publicly
**Historical Data:** Extensive - back to 1790 for decennial census

#### Available Datasets

**A. American Community Survey (ACS)**
- **ACS 5-Year Data (2009-2023)**: Most comprehensive, smallest geographic areas
- **ACS 1-Year Data (2005-2024)**: Most current, areas 65,000+ population
- **ACS 1-Year Supplemental (2014-2023)**: Areas 20,000+ population

**Table Types:**
- **Detailed Tables**: Most granular estimates on all topics
- **Subject Tables**: Information on specific topics with estimates and percentages
- **Data Profiles**: Broad social, economic, housing, demographic info
- **Comparison Profiles**: Data profiles with year-over-year comparisons

#### Key Real Estate Variables

**Demographics:**
- Population density and growth
- Age distribution
- Household composition
- Income levels and distribution
- Education levels
- Employment status

**Housing:**
- Housing units (total, occupied, vacant)
- Tenure (owner vs renter)
- Housing values and prices
- Gross rent
- Year structure built
- Number of bedrooms/rooms
- Heating fuel type
- Kitchen/plumbing facilities
- Occupants per room

**Economics:**
- Median household income
- Per capita income
- Poverty rates
- Industry employment
- Commute times
- Health insurance coverage

#### API Endpoints

```
Base URL: https://api.census.gov/data/{year}/acs/acs5
```

**Example Calls:**
```
# Get median household income and population for all states
GET https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E,B01003_001E&for=state:*&key=YOUR_KEY

# Get housing values for specific county
GET https://api.census.gov/data/2023/acs/acs5?get=NAME,B25077_001E&for=county:*&in=state:06&key=YOUR_KEY
```

#### Real Estate Use Cases

✅ **Market Analysis:** Demographic trends, income levels, population growth
✅ **Property Valuation:** Neighborhood characteristics, comparable housing data
✅ **Investment Decisions:** Economic indicators, employment data
✅ **Risk Assessment:** Vacancy rates, tenure patterns
✅ **Development Planning:** Housing needs, demographic projections

---

### 2. Bureau of Labor Statistics (BLS) API

**Official Documentation:** https://www.bls.gov/developers/home.htm
**API Key:** Required (Free) - https://data.bls.gov/registrationEngine/
**Rate Limits:**
- V2 (Registered): 500 queries/day, 50 series/query, 20 years/query
- V1 (Unregistered): 25 queries/day, 25 series/query, 10 years/query
**Historical Data:** Varies by series - most go back 10-30 years

#### Available Data Series

**A. Employment & Wages**
- State and Area Employment, Hours, and Earnings (SAE)
- Quarterly Census of Employment and Wages (QCEW)
- Occupational Employment and Wage Statistics (OEWS)
- Current Employment Statistics (CES)

**B. Consumer Price Index (CPI)**
- All Urban Consumers (CPI-U)
- Urban Wage Earners and Clerical Workers (CPI-W)
- Housing component: Shelter, Rent, Owners' equivalent rent

**C. Producer Price Index (PPI)**
- Construction materials
- Commercial real estate services

**D. Construction Industry Data**
- Employment in construction sector
- Wages in construction occupations

#### Series ID Format

```
Example: CUUR0000SA0
  CU = CPI-U
  U = Not seasonally adjusted
  R = Regular monthly publication
  0000 = U.S. city average
  SA0 = All items
```

#### API Endpoints

```
Base URL: https://api.bls.gov/publicAPI/v2/timeseries/data/
```

**Example Call:**
```json
POST https://api.bls.gov/publicAPI/v2/timeseries/data/

{
  "seriesid": ["CUUR0000SA0", "CUUR0000SAH1"],
  "startyear": "2020",
  "endyear": "2024",
  "registrationkey": "YOUR_KEY"
}
```

#### Key Series IDs for Real Estate

| Series ID | Description |
|-----------|-------------|
| CUUR0000SAH1 | CPI - Housing |
| CUUR0000SEHA | CPI - Rent of primary residence |
| CUUR0000SAH21 | CPI - Household furnishings and operations |
| WPUSI012011 | PPI - Office buildings |
| WPUSI012012 | PPI - Warehouse and storage |
| CEU2023600001 | Construction employment |

#### Real Estate Use Cases

✅ **Cost Analysis:** Track construction material costs, labor costs
✅ **Rent Trends:** Monitor rental price inflation
✅ **Economic Indicators:** Employment trends affecting housing demand
✅ **Operating Expenses:** Track utilities, maintenance cost trends
✅ **Investment Returns:** Adjust for inflation in real estate valuations

---

### 3. SEC EDGAR API

**Official Documentation:** https://www.sec.gov/search-filings/edgar-application-programming-interfaces
**API Key:** Not required
**Rate Limits:** 10 requests/second per IP
**Historical Data:** Company filings back to 1994 (older filings may be images)

#### Available APIs

**A. Submissions API**
```
GET https://data.sec.gov/submissions/CIK##########.json
```
Returns all filings for a company by CIK number

**B. Company Concepts API**
```
GET https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/AccountsPayableCurrent.json
```
Returns all XBRL disclosures for a single concept

**C. Company Facts API**
```
GET https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
```
Returns all company concepts in one call

**D. Frames API**
```
GET https://data.sec.gov/api/xbrl/frames/us-gaap/AccountsPayable/USD/CY2023Q1I.json
```
Aggregates one fact across multiple companies

#### Key Filing Types for Real Estate

| Form Type | Description | Use Case |
|-----------|-------------|----------|
| 10-K | Annual report | Financial statements, business operations |
| 10-Q | Quarterly report | Quarterly financial data |
| 8-K | Current events | Major transactions, acquisitions |
| S-11 | REIT registration | New REIT offerings |
| DEF 14A | Proxy statement | Corporate governance, compensation |
| 13F | Institutional holdings | Large investor positions |

#### XBRL Concepts for Real Estate

**REIT-Specific Tags:**
- `RealEstateInvestmentPropertyNet` - Property value
- `RealEstateProperties` - Property details
- `RealEstateRevenue` - Rental and property income
- `DepreciationAndAmortization` - Property depreciation
- `LongTermDebt` - Mortgage and other debt
- `OccupancyRate` - Property occupancy

#### Real Estate Use Cases

✅ **REIT Analysis:** Track public REIT financial performance
✅ **Competitor Intelligence:** Monitor competitor filings and transactions
✅ **Market Research:** Analyze trends in commercial real estate sector
✅ **Investment Due Diligence:** Access detailed financial statements
✅ **Insider Trading:** Track insider buying/selling (Form 4)

---

### 4. HUD USER API

**Official Documentation:** https://www.huduser.gov/portal/dataset/fmr-api.html
**API Key:** Required (Free) - https://www.huduser.gov/hudapi/public/register
**Rate Limits:** Not specified
**Historical Data:** Fair Market Rents back to 1983

#### Available APIs

**A. Fair Market Rents (FMR) API**
```
GET https://www.huduser.gov/hudapi/public/fmr/data/{zip_code}?year={year}
```

**Fields Returned:**
- `fmr_0`: Efficiency apartment FMR
- `fmr_1`: 1-bedroom FMR
- `fmr_2`: 2-bedroom FMR
- `fmr_3`: 3-bedroom FMR
- `fmr_4`: 4-bedroom FMR
- `fmr_type`: Type of FMR (40th/50th percentile)
- `metro_code`: Metropolitan area code
- `areaname`: Geographic area name

**B. Income Limits API**
```
GET https://www.huduser.gov/hudapi/public/il/data/{state}/{year}
```

**Fields:**
- Median family income
- Very low income (50% MFI)
- Extremely low income (30% MFI)
- Low income (80% MFI)

**C. USPS Crosswalk API**
```
GET https://www.huduser.gov/hudapi/public/usps?type=1&query={zip_code}
```
Maps ZIP codes to census tracts, counties, metropolitan areas

**D. CHAS (Comprehensive Housing Affordability Strategy)**
```
GET https://www.huduser.gov/hudapi/public/chas
```
Housing needs and market conditions data

#### Historical Data Coverage

- **FMR:** 1983-present (40+ years)
- **Income Limits:** 1998-present
- **CHAS:** Based on ACS 5-year estimates (rolling)

#### Real Estate Use Cases

✅ **Rent Analysis:** Compare rents to HUD Fair Market Rents
✅ **Affordable Housing:** Determine income qualification thresholds
✅ **Market Research:** Geographic crosswalks for market analysis
✅ **Subsidy Programs:** Section 8 rent calculations
✅ **Investment Screening:** Identify underserved markets

---

### 5. FRED API (Federal Reserve Economic Data)

**Official Documentation:** https://fred.stlouisfed.org/docs/api/fred/
**API Key:** Required (Free) - https://fredaccount.stlouisfed.org/apikeys
**Rate Limits:** None specified
**Historical Data:** Extensive - many series back 50+ years

#### Key Real Estate Data Series

**Housing Market Indicators:**

| Series ID | Description | History |
|-----------|-------------|---------|
| HOUST | Housing Starts: Total New Privately Owned | 1959-present |
| PERMIT | New Private Housing Units Authorized | 1960-present |
| CSUSHPINSA | S&P/Case-Shiller U.S. Home Price Index | 1987-present |
| MSPUS | Median Sales Price of Houses Sold | 1963-present |
| MSACSR | Monthly Supply of Houses | 1963-present |
| HSN1F | New One Family Houses Sold | 1963-present |
| USSTHPI | All-Transactions House Price Index | 1991-present |

**Mortgage & Interest Rates:**

| Series ID | Description | History |
|-----------|-------------|---------|
| MORTGAGE30US | 30-Year Fixed Rate Mortgage Average | 1971-present |
| MORTGAGE15US | 15-Year Fixed Rate Mortgage Average | 1991-present |
| FEDFUNDS | Federal Funds Effective Rate | 1954-present |
| DGS10 | 10-Year Treasury Constant Maturity Rate | 1962-present |
| DEXCHUS | China / U.S. Foreign Exchange Rate | 1981-present |

**Economic Indicators:**

| Series ID | Description | History |
|-----------|-------------|---------|
| UNRATE | Unemployment Rate | 1948-present |
| GDP | Gross Domestic Product | 1947-present |
| CPIAUCSL | Consumer Price Index for All Urban Consumers | 1947-present |
| PAYEMS | All Employees, Total Nonfarm | 1939-present |
| POPTHM | Population | 1952-present |
| PCEPILFE | Core PCE Price Index | 1959-present |

**Commercial Real Estate:**

| Series ID | Description | History |
|-----------|-------------|---------|
| BOGZ1FL075035503Q | Commercial Real Estate Loans, All Commercial Banks | 1951-present |
| TLCOMCON | Construction Spending: Commercial | 1993-present |
| TLOFFCON | Construction Spending: Office | 1993-present |

#### API Endpoints

**Get Series Data:**
```
GET https://api.stlouisfed.org/fred/series/observations?series_id=HOUST&api_key=YOUR_KEY&file_type=json
```

**Get Multiple Series:**
```
GET https://api.stlouisfed.org/fred/series?series_id=HOUST;PERMIT;MSACSR&api_key=YOUR_KEY
```

**Search Series:**
```
GET https://api.stlouisfed.org/fred/series/search?search_text=housing&api_key=YOUR_KEY
```

#### Real Estate Use Cases

✅ **Market Forecasting:** Analyze housing starts, permits, inventory
✅ **Pricing Models:** Incorporate Case-Shiller and HPI data
✅ **Interest Rate Analysis:** Model mortgage rate impacts
✅ **Economic Correlation:** Link employment, GDP to real estate demand
✅ **Investment Timing:** Track market cycles and indicators

---

### 6. EPA Envirofacts API

**Official Documentation:** https://www.epa.gov/enviro/envirofacts-data-service-api
**API Key:** Not required
**Rate Limits:** Not specified
**Historical Data:** Varies by dataset

#### Available Data Models

**A. Superfund Sites (SEMS)**
```
GET https://data.epa.gov/efservice/SEMS/{column}/{value}/JSON
```

**Fields:**
- `site_id`: EPA Site ID
- `site_name`: Name of site
- `address`: Street address
- `city`, `state`, `zip_code`: Location
- `latitude`, `longitude`: Coordinates
- `npl_status`: National Priorities List status
- `site_listing_narrative`: Description
- `contaminants`: List of contaminants found

**B. Air Quality (AQS)**
```
GET https://aqs.epa.gov/data/api/
```
Air quality measurements by location

**C. Toxic Release Inventory (TRI)**
```
GET https://data.epa.gov/efservice/TRI_{table}/
```
Chemical releases from facilities

**D. Radiation (RADInfo)**
```
GET https://data.epa.gov/efservice/RAD_
```
Radiation monitoring data

**E. Safe Drinking Water (SDWIS)**
```
GET https://data.epa.gov/efservice/SDWIS/
```
Public water system violations

#### Real Estate Use Cases

✅ **Environmental Due Diligence:** Check properties near Superfund sites
✅ **Risk Assessment:** Identify environmental hazards
✅ **Disclosure Requirements:** Environmental issues affecting value
✅ **Development Planning:** Avoid contaminated areas
✅ **Property Valuation:** Factor in environmental liabilities

---

### 7. NOAA Climate Data API

**Official Documentation:** https://www.ncdc.noaa.gov/cdo-web/webservices/v2
**New API:** https://www.ncei.noaa.gov/access/services/data/v1
**API Key:** Required (Free) - https://www.ncdc.noaa.gov/cdo-web/token
**Rate Limits:** 5 requests/second, 10,000 requests/day
**Historical Data:** 1950-present for most data

#### Available Datasets

**A. Global Historical Climatology Network (GHCN-Daily)**
- Daily temperature (min, max, average)
- Precipitation
- Snowfall
- Wind speed

**B. Storm Events Database**
- Historical extreme weather events
- Flood events
- Hurricane/tornado data
- Damage assessments

**C. Climate Normals**
- 30-year averages (1991-2020)
- Temperature normals
- Precipitation normals

#### API Endpoints

```
Base URL: https://www.ncdc.noaa.gov/cdo-web/api/v2/
```

**Get Weather Data:**
```
GET https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=FIPS:06&startdate=2020-01-01&enddate=2024-12-31
```

**Get Storm Events:**
```
GET https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=SEVEREWEATHER&locationid=ZIP:90210
```

#### Real Estate Use Cases

✅ **Climate Risk Assessment:** Historical flood/storm frequency
✅ **Insurance Underwriting:** Weather event history
✅ **Development Planning:** Flood zones, extreme weather
✅ **Property Valuation:** Climate-related risks
✅ **Long-term Investment:** Climate change impacts

---

## Commercial Real Estate APIs (PAID)

### 8. CoStar

**Website:** https://www.costar.com
**API Access:** Enterprise only, contact sales
**Pricing:** Custom enterprise pricing

#### Data Coverage

- **Properties:** 5.8M+ commercial properties
- **Leases:** Detailed lease comps and transaction data
- **Analytics:** Market trends, cap rates, occupancy
- **Tenants:** Tenant information and requirements
- **Sales Comps:** Transaction data

#### Features

- Comprehensive commercial property database
- Market analytics and reports
- Property valuations
- Tenant and lease data
- Space available listings

#### Access Model

❌ No public API
✅ Enterprise API available for customers
✅ Data exports and integrations available
⚠️ High cost - typically $1,000+/month per user

---

### 9. Yardi Voyager API

**Website:** https://www.yardi.com
**API Access:** Available to Yardi clients
**Documentation:** Requires partnership/client access

#### Capabilities

- Property management data
- Lease data and rent rolls
- Maintenance and work orders
- Accounting and financial data
- Tenant information
- Real-time synchronization

#### Integration Methods

- REST API
- SOAP Web Services
- CSV/XML file imports
- Taskrunner automation

#### Access Model

⚠️ Requires Yardi Voyager subscription
✅ Standard Interface Partnership Program (SIPP) available
✅ Custom integrations supported

---

### 10. Real Capital Analytics (RCA)

**Website:** https://www.msci.com/real-capital-analytics
**Owned By:** MSCI
**API Access:** Enterprise clients only

#### Data Coverage

- **Transactions:** 1.8M+ commercial transactions
- **Volume:** $16T+ in transaction data
- **Coverage:** 172 countries globally
- **Entities:** 155,000+ investor and lender profiles
- **Property Types:** Office, retail, industrial, multifamily, hotel, land

#### Features

- Global transaction database
- Ownership history
- Pricing and loan data
- Climate risk data
- Real-time deal tracking
- Market trends and analytics

#### Access Model

❌ No public API
✅ Enterprise platform access
✅ Third-party integrations (e.g., Dealpath)
⚠️ Custom pricing - enterprise level

---

## Residential Real Estate APIs

### 11. Zillow Data

**Status:** Public API deprecated (Sept 2021)
**Alternative:** Bridge Interactive API (invite only)
**Free Data:** https://www.zillow.com/research/data/

#### Available Through Bridge API

- Property records (148M properties)
- Tax assessments
- Transaction history (15 years)
- Zestimates
- Rental estimates
- County data (3,200 counties)

#### Free Public Data (CSV Downloads)

- Zillow Home Value Index (ZHVI)
- Zillow Observed Rent Index (ZORI)
- Market temperature
- Inventory metrics
- Sales data

#### Access Model

❌ No public API
⚠️ Bridge API - invite only (api@bridgeinteractive.com)
✅ Free CSV downloads for research

---

### 12. Redfin Data

**Status:** No official API
**Data Center:** https://www.redfin.com/news/data-center/
**Contact:** econdata@redfin.com

#### Available Data (CSV Downloads)

- Median sale prices
- Homes sold
- New listings
- Inventory
- Months of supply
- Median days on market
- Sale-to-list price ratio

#### Geographic Coverage

- Metropolitan areas
- Cities
- Neighborhoods
- ZIP codes

#### Access Model

❌ No official API
⚠️ Third-party scraper APIs available (questionable legality)
✅ Free CSV downloads

---

## Environmental & Risk Data

### 13. USGS National Map API

**Official Documentation:** https://www.usgs.gov/the-national-map-data-delivery
**API:** TNMAccess API
**API Key:** Not required
**Data:** Elevation, hydrography, boundaries, structures, transportation

#### What It DOES NOT Include

❌ Property parcel boundaries (county-level data)
❌ Individual property ownership

#### What It DOES Include

✅ Topographic maps
✅ Elevation data (DEM)
✅ Orthoimagery
✅ Land cover
✅ Government boundaries
✅ Hydrography (water bodies, streams)

---

## Implementation Priority

### Tier 1: Immediate Implementation (Free, High Value)

1. **FRED API** - Critical economic indicators
2. **Census API** - Demographics and housing data
3. **HUD USER API** - Fair market rents and income limits

### Tier 2: Near-term Implementation (Free, Government)

4. **BLS API** - Employment and CPI data
5. **SEC EDGAR API** - REIT and public company data
6. **EPA Envirofacts** - Environmental risk screening

### Tier 3: Medium-term (Free, Specialized)

7. **NOAA Climate API** - Weather and climate risk
8. **Census Microdata** - Detailed demographic analysis

### Tier 4: Evaluation Phase (Commercial, Paid)

9. **Zillow Research Data** - Market trends (CSV)
10. **Redfin Data Center** - Market metrics (CSV)
11. **Bridge API** - Property records (requires approval)

### Tier 5: Enterprise Partnerships (High Cost)

12. **CoStar** - Commercial property data
13. **Yardi** - Property management integration
14. **RCA/MSCI** - Transaction data

---

## API Comparison Matrix

| API | Cost | Auth | Rate Limit | Historical | Real Estate Relevance |
|-----|------|------|------------|------------|----------------------|
| **Census** | Free | API Key | None | 1790+ | ⭐⭐⭐⭐⭐ Demographics |
| **BLS** | Free | API Key | 500/day | 1940s+ | ⭐⭐⭐⭐ Employment, CPI |
| **FRED** | Free | API Key | None | 1940s+ | ⭐⭐⭐⭐⭐ Economics |
| **HUD** | Free | API Key | Unknown | 1983+ | ⭐⭐⭐⭐⭐ FMR, Income |
| **SEC EDGAR** | Free | None | 10/sec | 1994+ | ⭐⭐⭐⭐ REITs, Public Cos |
| **EPA** | Free | None | Unknown | Varies | ⭐⭐⭐ Environmental |
| **NOAA** | Free | API Key | 5/sec | 1950+ | ⭐⭐⭐ Climate Risk |
| **CoStar** | $$$$ | Enterprise | N/A | Extensive | ⭐⭐⭐⭐⭐ Commercial |
| **RCA** | $$$$ | Enterprise | N/A | Extensive | ⭐⭐⭐⭐⭐ Transactions |
| **Yardi** | $$$ | Client | N/A | Current | ⭐⭐⭐⭐ Property Mgmt |
| **Zillow** | Free (CSV) | None | N/A | 1996+ | ⭐⭐⭐⭐ Residential |
| **Redfin** | Free (CSV) | None | N/A | 2012+ | ⭐⭐⭐ Residential |

---

## Next Steps

### Phase 1: API Exploration Scripts
Create Python scripts to:
1. Test each API endpoint
2. Retrieve sample data
3. Map available fields
4. Understand data structures
5. Identify relevant metrics

### Phase 2: Integration Architecture
1. Extend existing integration framework
2. Create new integration classes for each API
3. Implement caching strategies
4. Design database schema for new data
5. Build ETL pipelines

### Phase 3: Data Analysis
1. Correlate multiple data sources
2. Build composite indicators
3. Create predictive models
4. Generate insights and reports

---

**Document Status:** Initial Research Complete
**Last Updated:** 2025-11-09
**Next Action:** Create API exploration scripts
