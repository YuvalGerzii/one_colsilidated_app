# No API Key Required - Data Sources & Scrapers

**Date:** 2025-11-09
**Purpose:** Comprehensive guide to getting real estate data WITHOUT API keys

---

## Table of Contents

1. [Government Bulk Data Downloads](#government-bulk-data-downloads)
2. [Web Scrapers - Residential Real Estate](#web-scrapers---residential-real-estate)
3. [MCP Servers for Real Estate](#mcp-servers-for-real-estate)
4. [Docker Containers](#docker-containers)
5. [Python Libraries](#python-libraries)
6. [Already Implemented in Codebase](#already-implemented-in-codebase)
7. [Implementation Guide](#implementation-guide)

---

## Government Bulk Data Downloads

### ✅ No API Key, No Rate Limits, Free Forever

---

### 1. Census Bureau FTP Downloads

**URL:** `ftp2.census.gov` or `www2.census.gov/programs-surveys/acs/`
**No API Key Required**
**Format:** CSV, DBF, SAS files

#### Available Data

**American Community Survey (ACS) PUMS:**
- Housing files: csv_hak, sas_hak
- Person files: csv_pus, sas_pus
- Microdata on individual housing units
- Full demographic and housing characteristics

**Data Files:**
```
ftp://ftp2.census.gov/programs-surveys/acs/data/pums/
├── 2023/
│   ├── 1-Year/
│   │   ├── csv_hus.zip (Housing records)
│   │   └── csv_pus.zip (Person records)
│   └── 5-Year/
│       ├── csv_hus.zip
│       └── csv_pus.zip
└── [2009-2022 archives]
```

#### Usage Example
```python
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

# Download ACS housing data
url = "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_hus.zip"
response = requests.get(url)

# Extract and load CSV
with ZipFile(BytesIO(response.content)) as zip_file:
    csv_name = zip_file.namelist()[0]
    with zip_file.open(csv_name) as csv_file:
        df = pd.read_csv(csv_file)

print(f"Loaded {len(df)} housing records")
```

---

### 2. HUD USER - Fair Market Rent Downloads

**URL:** https://www.huduser.gov/portal/datasets/fmr.html
**No API Key for Downloads**
**Format:** Excel, DBF, ZIP

#### Available Files

**Historical FMR Data (1983-Present):**
- `FY{YEAR}_FMRs.zip` - All FMRs for fiscal year
- `FY{YEAR}_4050_FMRs.zip` - 40th and 50th percentile rents
- DBF format (dBASE III) - works with Excel, Pandas

**Direct Download Links:**
```
https://www.huduser.gov/portal/datasets/fmr/fmr2024/FY24_FMRs.zip
https://www.huduser.gov/portal/datasets/fmr/fmr2023/FY23_FMRs.zip
https://www.huduser.gov/portal/datasets/fmr/fmr2022/FY22_FMRs.zip
```

#### Fields Included
- Efficiency, 1BR, 2BR, 3BR, 4BR rents
- Metro area codes
- County codes
- ZIP codes (in crosswalk files)

#### Python Example
```python
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO

url = "https://www.huduser.gov/portal/datasets/fmr/fmr2024/FY24_FMRs.zip"
response = requests.get(url)

with ZipFile(BytesIO(response.content)) as zip_file:
    # Find the DBF file
    dbf_files = [f for f in zip_file.namelist() if f.endswith('.dbf')]

    # Read DBF with pandas (requires simpledbf or dbfread)
    # Or extract and use dbfread library
    print(f"Available files: {zip_file.namelist()}")
```

---

### 3. Data.gov - Real Estate Datasets

**URL:** https://catalog.data.gov/dataset/?tags=real-estate
**No API Key Required**
**Format:** CSV, JSON, XML, Shapefile

#### Key Datasets

**Federal Real Property:**
- GSA Federal Real Property dataset
- Format: CSV
- Fields: Property location, value, square footage, agency

**State/Local Real Estate Sales:**
- Connecticut Real Estate Sales (2001-2024)
- Format: CSV
- Direct download available
- Fields: Sale price, property type, assessment, location

**Affordable Housing:**
- HUD affordable housing locations
- Format: CSV, GeoJSON
- Direct download

#### Direct Download Pattern
```python
import pandas as pd

# Connecticut Real Estate Sales
url = "https://data.ct.gov/api/views/5mzw-sjtu/rows.csv?accessType=DOWNLOAD"
df = pd.read_csv(url)

print(f"Loaded {len(df)} real estate transactions")
print(df.columns.tolist())
```

---

### 4. SEC EDGAR - Bulk Data

**URL:** https://www.sec.gov/dera/data/financial-statement-data-sets.html
**No API Key Required**
**Format:** ZIP files with TSV data

#### Available Data

**Financial Statement Datasets:**
- Quarterly ZIP files (2009-present)
- All company filings in structured format
- XBRL-tagged data
- REIT financial statements included

**Files in Each ZIP:**
- `sub.txt` - Submission info
- `tag.txt` - XBRL tags
- `num.txt` - Numeric data
- `pre.txt` - Presentation info

#### Download Pattern
```python
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO

# Download Q1 2024 data
url = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/2024q1.zip"
response = requests.get(url, headers={'User-Agent': 'YourCompany info@example.com'})

with ZipFile(BytesIO(response.content)) as zip_file:
    # Read numeric data
    with zip_file.open('num.txt') as f:
        df = pd.read_csv(f, sep='\t', low_memory=False)

    print(f"Loaded {len(df)} data points")
```

---

### 5. FHFA House Price Index

**URL:** https://www.fhfa.gov/DataTools/Downloads/Pages/House-Price-Index-Datasets.aspx
**No API Key Required**
**Format:** CSV, Excel

#### Available Files

**All-Transactions Index:**
- National, state, metro, ZIP
- Quarterly data (1975-present)
- Direct CSV download

**Purchase-Only Index:**
- Same geographic levels
- Excludes refinance appraisals

**Direct Links:**
```
https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_AT_3zip.xlsx
https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_AT_metro.xlsx
https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_AT_state.xlsx
```

---

### 6. CORGIS Real Estate Dataset

**URL:** https://corgis-edu.github.io/corgis/csv/real_estate/
**No API Key Required**
**Format:** CSV

**Direct Download:**
```
https://corgis-edu.github.io/corgis/datasets/csv/real_estate/real_estate.csv
```

**Fields:**
- Property details
- PBS building inventory
- Owned and leased buildings
- Active and excess status

---

## Web Scrapers - Residential Real Estate

### ⚠️ Legal Considerations

**Important:** Web scraping may violate Terms of Service. Use responsibly:
- Respect robots.txt
- Add delays between requests
- Use for personal/research only
- Don't overload servers
- Consider using official APIs when available

---

### 1. HomeHarvest - Multi-Site Scraper

**GitHub:** https://github.com/ZacharyHampton/HomeHarvest
**PyPI:** `pip install homeharvest`
**Python:** >= 3.10 required

#### Features

✅ **Scrapes:** Zillow, Realtor.com, Redfin
✅ **No API Key Required**
✅ **Output:** Pandas DataFrame → CSV/Excel
✅ **Listing Types:** for_sale, for_rent, sold, pending

#### Installation
```bash
pip install homeharvest
```

#### Basic Usage
```python
from homeharvest import scrape_property
import pandas as pd

# Scrape properties
properties = scrape_property(
    location="San Francisco, CA",
    listing_type="for_sale",  # for_rent, sold, pending
    past_days=30,  # sold/pending only
)

# Save to file
properties.to_csv('properties.csv', index=False)
properties.to_excel('properties.xlsx', index=False)

print(f"Found {len(properties)} properties")
```

#### Command Line Usage
```bash
homeharvest "90210" -s zillow realtor redfin -l for_sale -o csv -f results
```

#### Advanced Filtering
```python
# Filter by criteria
expensive_homes = properties[
    (properties['price'] > 1000000) &
    (properties['beds'] >= 4) &
    (properties['baths'] >= 3)
]

# Calculate metrics
avg_price_per_sqft = properties['price'] / properties['sqft']
```

#### Rate Limiting
```python
import time
from homeharvest import scrape_property

zip_codes = ['90210', '10001', '60601', '33101']
all_properties = []

for zip_code in zip_codes:
    print(f"Scraping {zip_code}...")

    props = scrape_property(
        location=zip_code,
        listing_type="for_sale"
    )

    all_properties.append(props)

    # Wait 5 seconds between requests
    time.sleep(5)

# Combine all data
combined = pd.concat(all_properties, ignore_index=True)
combined.to_csv('all_properties.csv', index=False)
```

---

### 2. Real-Estate-Scrape (Zillow + Redfin)

**GitHub:** https://github.com/mikepqr/real-estate-scrape
**PyPI:** `pip install real-estate-scrape`

#### Features
- Scrapes Zillow and Redfin
- Get estimated property values
- Simple command-line interface
- Outputs JSON

#### Usage
```bash
pip install real-estate-scrape

# Get property value
real-estate-scrape "123 Main St, San Francisco, CA"
```

---

### 3. Zillow-Scraper

**GitHub:** https://github.com/scrapehero/zillow_real_estate
**No Package** - Clone and run

#### Features
- Specifically for Zillow
- Search by ZIP code
- Uses Python + LXML
- Outputs to JSON/CSV

#### Usage
```bash
git clone https://github.com/scrapehero/zillow_real_estate.git
cd zillow_real_estate
pip install -r requirements.txt

python zillow.py --zipcode 90210
```

---

## MCP Servers for Real Estate

**Model Context Protocol** - Connect AI assistants to real estate data

---

### 1. Zillow MCP Server

**GitHub:** https://github.com/sap156/zillow-mcp-server
**Language:** Python + FastMCP
**No API Key Required** (uses web scraping)

#### Features

**Tools Available:**
1. `search_properties` - Search Zillow by criteria
2. `get_property_details` - Detailed property info
3. `get_zestimate` - Zillow's estimated value
4. `get_market_trends` - Market trends by location
5. `calculate_mortgage` - Mortgage payment calculator

#### Installation
```bash
git clone https://github.com/sap156/zillow-mcp-server.git
cd zillow-mcp-server
pip install -r requirements.txt
```

#### Configuration (Claude Desktop)
```json
{
  "mcpServers": {
    "zillow": {
      "command": "python",
      "args": ["/path/to/zillow-mcp-server/server.py"]
    }
  }
}
```

#### Usage Examples
```python
# Search for properties
search_properties(
    location="San Francisco, CA",
    type="house",
    min_price=500000,
    max_price=1500000,
    bedrooms=3,
    bathrooms=2
)

# Get property details
get_property_details(
    address="123 Main St, San Francisco, CA 94102"
)

# Get Zestimate
get_zestimate(
    address="123 Main St, San Francisco, CA 94102"
)

# Market trends
get_market_trends(
    location="San Francisco, CA",
    metrics=["median_price", "inventory", "days_on_market"],
    time_period="6_months"
)

# Calculate mortgage
calculate_mortgage(
    home_price=800000,
    down_payment=160000,
    interest_rate=6.5,
    loan_term_years=30
)
```

---

### 2. BatchData Real Estate MCP Server

**Source:** PulseMCP
**Purpose:** Batch processing for real estate data
**Features:**
- Property listings management
- Market analytics
- Property management workflows
- Efficient batch operations

---

### 3. Finding More MCP Servers

**Directories:**
- https://www.mcpserverfinder.com/
- https://mcpnodes.com/
- https://github.com/modelcontextprotocol/servers

**Official MCP Servers (by Anthropic):**
- PostgreSQL (store scraped data)
- Google Drive (for data files)
- GitHub (version control for scripts)
- Puppeteer (web scraping)

---

## Docker Containers

### Real Estate Scrapers

---

### 1. Estate-Crawler

**GitHub:** https://github.com/nstapelbroek/estate-crawler
**Purpose:** Real estate agency scraping
**Features:** Up-to-date listings, notifications

```bash
git clone https://github.com/nstapelbroek/estate-crawler.git
cd estate-crawler
docker-compose up
```

---

### 2. Scrape-REC

**GitHub:** https://github.com/danielacraciun/scrape-rec
**Purpose:** Real estate data gathering
**Features:** Multiple scrapers, Docker support

```bash
git clone https://github.com/danielacraciun/scrape-rec.git
cd scrape-rec

# Build all scrapers
docker-compose build

# Run specific scraper
docker-compose run scraper-zillow
```

---

### 3. Generic Python Scraper Containers

**cigolpl/web-scraper**
```bash
docker pull cigolpl/web-scraper
```

**rdempsey/python-scraper**
```bash
docker pull rdempsey/python-scraper
```

---

## Python Libraries

### Core Scraping Libraries

---

### 1. BeautifulSoup4
```bash
pip install beautifulsoup4 requests lxml
```

```python
import requests
from bs4 import BeautifulSoup

url = "https://example-real-estate-site.com/listings"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Extract property data
properties = soup.find_all('div', class_='property-card')
for prop in properties:
    price = prop.find('span', class_='price').text
    address = prop.find('div', class_='address').text
    print(f"{address}: {price}")
```

---

### 2. Selenium (for JavaScript-heavy sites)
```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.zillow.com")

# Wait for JavaScript to load
time.sleep(3)

# Extract data
listings = driver.find_elements(By.CLASS_NAME, "list-card-info")
for listing in listings:
    print(listing.text)

driver.quit()
```

---

### 3. Scrapy (Full Framework)
```bash
pip install scrapy
```

```python
import scrapy

class RealEstateSpider(scrapy.Spider):
    name = 'real_estate'
    start_urls = ['https://example.com/listings']

    def parse(self, response):
        for property in response.css('div.property'):
            yield {
                'address': property.css('span.address::text').get(),
                'price': property.css('span.price::text').get(),
                'beds': property.css('span.beds::text').get(),
            }

        # Follow pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

---

## Already Implemented in Codebase

### ✅ Currently Available (No API Keys Needed)

---

### 1. Data.gov Integration

**File:** `/backend/app/integrations/official_data/datagov_us.py`
**Status:** ✅ Implemented
**API Key:** ❌ Not required

```python
from app.integrations.official_data.datagov_us import DataGovUSIntegration

datagov = DataGovUSIntegration(config)

# Search for real estate datasets
datasets = await datagov.search_datasets(query="real estate")

# Get specific dataset
dataset = await datagov.get_dataset(dataset_id="...")

# Get download URL for resource
resource_url = await datagov.download_dataset_resource(
    dataset_id="...",
    resource_id="..."
)
```

---

### 2. SEC EDGAR API

**File:** `/backend/app/integrations/official_data/sec_edgar.py`
**Status:** ✅ Framework exists (needs completion)
**API Key:** ❌ Not required

**Available Endpoints:**
- Company submissions
- Company facts (XBRL)
- Bulk data downloads

---

### 3. FHFA Integration

**File:** `/backend/app/integrations/official_data/fhfa.py`
**Status:** ✅ Implemented
**API Key:** ❌ Not required

```python
from app.integrations.official_data.fhfa import FHFAIntegration

fhfa = FHFAIntegration(config)

# Get House Price Index
hpi = await fhfa.get_house_price_index(
    geography="national",
    frequency="quarterly"
)

# Get download links for bulk data
links = await fhfa.get_download_links()
# Returns URLs to CSV/Excel files
```

---

## Implementation Guide

### Step-by-Step: Adding HomeHarvest Scraper

---

#### 1. Install Dependencies
```bash
cd /home/user/real_estate_dashboard/backend
pip install homeharvest
```

#### 2. Create Integration Class

**File:** `/backend/app/integrations/scrapers/homeharvest.py`

```python
from homeharvest import scrape_property
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HomeHarvestIntegration:
    """Real estate property scraper using HomeHarvest"""

    def __init__(self):
        self.name = "HomeHarvest"
        self.sources = ["zillow", "realtor", "redfin"]

    async def scrape_properties(
        self,
        location: str,
        listing_type: str = "for_sale",
        past_days: Optional[int] = None
    ) -> List[Dict]:
        """
        Scrape properties from multiple sources

        Args:
            location: ZIP code, city, or full address
            listing_type: for_sale, for_rent, sold, pending
            past_days: Days of sold/pending history (optional)

        Returns:
            List of property dictionaries
        """
        try:
            logger.info(f"Scraping {listing_type} properties in {location}")

            # Scrape data
            df = scrape_property(
                location=location,
                listing_type=listing_type,
                past_days=past_days
            )

            # Convert to list of dicts
            properties = df.to_dict('records')

            logger.info(f"Found {len(properties)} properties")
            return properties

        except Exception as e:
            logger.error(f"Error scraping properties: {e}")
            raise

    async def scrape_comps(
        self,
        address: str,
        radius_miles: float = 0.5,
        min_beds: int = None,
        max_beds: int = None
    ) -> List[Dict]:
        """
        Scrape comparable properties near an address
        """
        try:
            # Scrape sold properties
            df = scrape_property(
                location=address,
                listing_type="sold",
                past_days=180  # 6 months
            )

            # Filter by bedrooms if specified
            if min_beds:
                df = df[df['beds'] >= min_beds]
            if max_beds:
                df = df[df['beds'] <= max_beds]

            # Sort by most recent
            df = df.sort_values('sold_date', ascending=False)

            return df.to_dict('records')

        except Exception as e:
            logger.error(f"Error scraping comps: {e}")
            raise
```

#### 3. Create API Endpoint

**File:** `/backend/app/api/v1/endpoints/scrapers.py`

```python
from fastapi import APIRouter, HTTPException, Query
from app.integrations.scrapers.homeharvest import HomeHarvestIntegration
from typing import List, Optional

router = APIRouter()


@router.get("/scrape/properties")
async def scrape_properties(
    location: str = Query(..., description="ZIP code, city, or address"),
    listing_type: str = Query("for_sale", regex="^(for_sale|for_rent|sold|pending)$"),
    past_days: Optional[int] = Query(None, ge=1, le=365)
):
    """Scrape real estate properties"""
    try:
        scraper = HomeHarvestIntegration()
        properties = await scraper.scrape_properties(
            location=location,
            listing_type=listing_type,
            past_days=past_days
        )

        return {
            "success": True,
            "count": len(properties),
            "location": location,
            "listing_type": listing_type,
            "properties": properties
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scrape/comps")
async def scrape_comps(
    address: str = Query(..., description="Property address"),
    radius_miles: float = Query(0.5, ge=0.1, le=5.0),
    min_beds: Optional[int] = Query(None, ge=0),
    max_beds: Optional[int] = Query(None, le=10)
):
    """Scrape comparable sold properties"""
    try:
        scraper = HomeHarvestIntegration()
        comps = await scraper.scrape_comps(
            address=address,
            radius_miles=radius_miles,
            min_beds=min_beds,
            max_beds=max_beds
        )

        return {
            "success": True,
            "count": len(comps),
            "address": address,
            "comparables": comps
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 4. Register Router

**File:** `/backend/app/api/v1/api.py`

```python
from app.api.v1.endpoints import scrapers

api_router.include_router(
    scrapers.router,
    prefix="/scrapers",
    tags=["scrapers"]
)
```

---

### Best Practices

#### Rate Limiting
```python
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, requests_per_minute: int = 10):
        self.rpm = requests_per_minute
        self.requests = []

    async def wait_if_needed(self):
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Remove old requests
        self.requests = [r for r in self.requests if r > minute_ago]

        # Check if at limit
        if len(self.requests) >= self.rpm:
            sleep_time = 60 - (now - self.requests[0]).total_seconds()
            await asyncio.sleep(sleep_time)

        self.requests.append(now)
```

#### Error Handling
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def scrape_with_retry(location: str):
    """Retry scraping with exponential backoff"""
    return await scraper.scrape_properties(location)
```

#### Caching
```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=100)
def get_cached_properties(location: str, listing_type: str):
    cache_key = hashlib.md5(
        f"{location}:{listing_type}".encode()
    ).hexdigest()

    # Check cache (Redis, file, etc.)
    # Return if found, None otherwise
    pass
```

---

## Legal & Ethical Considerations

### ⚠️ Important Warnings

1. **Terms of Service**
   - Many websites prohibit scraping in their ToS
   - Read and understand before scraping
   - Violation may result in legal action

2. **robots.txt**
   - Always respect robots.txt
   - Check before scraping: `website.com/robots.txt`

3. **Rate Limiting**
   - Don't overload servers
   - Add delays between requests (2-5 seconds minimum)
   - Use during off-peak hours

4. **User-Agent**
   - Identify yourself properly
   - Use descriptive User-Agent string
   - Include contact email

5. **Data Usage**
   - Personal/research use only
   - Don't republish scraped data commercially
   - Respect copyright and intellectual property

6. **Prefer Official APIs**
   - Always use official APIs when available
   - Scrapers are last resort
   - APIs are more reliable and legal

### Recommended Approach

**Priority Order:**
1. ✅ Official APIs (even with keys)
2. ✅ Government bulk downloads
3. ✅ MCP servers (when available)
4. ⚠️ Web scraping (with caution)

---

## Summary

### No API Key Solutions Available:

✅ **Government Data** - Completely free, bulk downloads
✅ **MCP Servers** - Modern integration protocol
✅ **Web Scrapers** - Last resort, use carefully
✅ **Docker Containers** - Easy deployment
✅ **Already Implemented** - Many integrations ready

### Quick Start Recommendations:

1. **Start with Government Data**
   - Census FTP downloads
   - HUD Fair Market Rents
   - Data.gov datasets
   - SEC EDGAR bulk files

2. **Use MCP Servers**
   - Zillow MCP Server
   - BatchData Real Estate

3. **Add Scrapers Carefully**
   - HomeHarvest for property data
   - Rate limit properly
   - Respect ToS

4. **Leverage Existing Code**
   - Data.gov integration ready
   - FHFA implemented
   - Framework in place

---

**Document Status:** Complete
**Last Updated:** 2025-11-09
**Next Steps:** Implement scrapers and bulk downloaders
