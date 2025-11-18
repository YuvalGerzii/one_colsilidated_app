# Market Intelligence Enhancement - Implementation Guide

**Created**: November 9, 2025
**Status**: In Progress
**Objective**: Enhance Market Intelligence with 7 government APIs, scrapers, database storage, and scheduled imports

---

## 📋 Overview

This guide provides a step-by-step implementation plan to transform the Market Intelligence dashboard into a comprehensive real estate data platform with multiple data sources, database storage, and automated daily imports.

## ✅ Completed

### 1. Database Models Created
**File**: [backend/app/models/market_intelligence.py](backend/app/models/market_intelligence.py)

**Models**:
- ✅ `CensusData` - Demographics & housing from Census Bureau
- ✅ `FREDIndicator` - Economic time series from Federal Reserve
- ✅ `HUDFairMarketRent` - Rental rates & income limits
- ✅ `BLSEmployment` - Employment & unemployment data
- ✅ `SECREITData` - REIT financial data from SEC filings
- ✅ `EPAEnvironmentalHazard` - Superfund sites & environmental risks
- ✅ `NOAAClimateData` - Weather data & climate risks
- ✅ `PropertyListing` - Scraped real estate listings
- ✅ `MarketDataImport` - Track import jobs & status

### 2. API Explorers Documented
**Location**: `scripts/api_explorers/`

**Available Data Sources**:
1. **Census API** - 50+ housing metrics, demographics, income data
2. **FRED API** - 800,000+ economic indicators
3. **HUD API** - Fair Market Rents (1983-present)
4. **BLS API** - Employment, CPI, construction data
5. **SEC EDGAR** - REIT financials, public company data
6. **EPA API** - Environmental hazards, Superfund sites
7. **NOAA API** - Historical weather, climate normals

---

## 🎯 Implementation Steps

### Step 1: Run Database Migration

```bash
cd backend

# Create migration
/opt/anaconda3/bin/alembic revision --autogenerate -m "Add market intelligence models"

# Apply migration
/opt/anaconda3/bin/alembic upgrade head
```

**Expected Output**: 9 new tables created

---

### Step 2: Create Data Import Services

Create `/backend/app/services/market_data_importers.py`:

```python
"""
Market Data Import Services
Fetches data from APIs and stores in database with fallback mechanisms
"""

import logging
from datetime import datetime, date
from typing import List, Optional, Dict, Any
import requests
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.market_intelligence import (
    CensusData, FREDIndicator, HUDFairMarketRent, BLSEmployment,
    SECREITData, EPAEnvironmentalHazard, NOAAClimateData,
    PropertyListing, MarketDataImport
)

logger = logging.getLogger(__name__)


class CensusImporter:
    """Import Census Bureau data with fallback"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('CENSUS_API_KEY')
        self.base_url = "https://api.census.gov/data"

    async def import_state_data(self, db: Session, state_fips: str, year: int = 2023):
        """Import census data for a state with error handling"""
        import_job = MarketDataImport(
            data_source="census",
            import_type="incremental",
            status="running",
            start_date=date(year, 1, 1),
            started_at=datetime.now()
        )
        db.add(import_job)
        db.commit()

        try:
            # Fetch data from Census API
            variables = [
                "B25001_001E",  # Total housing units
                "B25002_002E",  # Occupied
                "B25002_003E",  # Vacant
                "B25077_001E",  # Median home value
                "B25064_001E",  # Median rent
                "B01003_001E",  # Population
                "B19013_001E",  # Median income
            ]

            url = f"{self.base_url}/{year}/acs/acs5"
            params = {
                "get": ",".join(variables + ["NAME"]),
                "for": f"county:*",
                "in": f"state:{state_fips}",
                "key": self.api_key
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            headers = data[0]
            rows = data[1:]

            records_inserted = 0
            for row in rows:
                try:
                    census_data = CensusData(
                        geo_level="county",
                        geo_id=f"{row[-2]}{row[-1]}",  # state+county FIPS
                        geo_name=row[7],  # NAME field
                        state_code=state_fips,
                        year=year,
                        dataset="acs5",
                        total_housing_units=int(row[0]) if row[0] not in ['-666666666', 'null'] else None,
                        occupied_units=int(row[1]) if row[1] not in ['-666666666', 'null'] else None,
                        vacant_units=int(row[2]) if row[2] not in ['-666666666', 'null'] else None,
                        median_home_value=int(row[3]) if row[3] not in ['-666666666', 'null'] else None,
                        median_gross_rent=int(row[4]) if row[4] not in ['-666666666', 'null'] else None,
                        total_population=int(row[5]) if row[5] not in ['-666666666', 'null'] else None,
                        median_household_income=int(row[6]) if row[6] not in ['-666666666', 'null'] else None,
                        data_date=date(year, 12, 31)
                    )
                    db.add(census_data)
                    records_inserted += 1
                except Exception as e:
                    logger.error(f"Error processing row: {e}")
                    import_job.records_failed += 1

            db.commit()

            import_job.status = "completed"
            import_job.records_processed = len(rows)
            import_job.records_inserted = records_inserted
            import_job.completed_at = datetime.now()
            import_job.duration_seconds = (import_job.completed_at - import_job.started_at).total_seconds()
            db.commit()

            logger.info(f"Census import completed: {records_inserted} records")
            return {"success": True, "records": records_inserted}

        except Exception as e:
            logger.error(f"Census import failed: {e}")
            import_job.status = "failed"
            import_job.error_message = str(e)
            import_job.completed_at = datetime.now()
            db.commit()

            # FALLBACK: Return empty success to prevent crashes
            return {"success": False, "error": str(e), "fallback": True}


class FREDImporter:
    """Import FRED economic data with fallback"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FRED_API_KEY')
        self.base_url = "https://api.stlouisfed.org/fred"

    async def import_series(self, db: Session, series_id: str, start_date: date):
        """Import FRED time series with error handling"""
        # Similar structure to CensusImporter
        # Fetch data, store in FREDIndicator table, handle errors
        pass


# Similar importers for HUD, BLS, SEC, EPA, NOAA...
```

**Key Features**:
- ✅ Error handling with try-catch
- ✅ Import job tracking
- ✅ Fallback mechanisms
- ✅ Logging for debugging
- ✅ Transaction management

---

### Step 3: Create Enhanced API Endpoints

Update `/backend/app/api/v1/endpoints/market_intelligence.py`:

```python
@router.get("/census/demographics")
async def get_census_demographics(
    state_code: str = Query(..., description="2-letter state code"),
    year: int = Query(2023, description="Data year"),
    db: Session = Depends(get_db)
):
    """
    Get Census demographics data from database

    **Fallback**: Returns mock data if no data in database
    """
    try:
        # Query database
        results = db.query(CensusData).filter(
            CensusData.state_code == state_code.upper(),
            CensusData.year == year
        ).all()

        if results:
            return {
                "success": True,
                "data_source": "database",
                "count": len(results),
                "data": [
                    {
                        "county": r.geo_name,
                        "population": r.total_population,
                        "median_income": r.median_household_income,
                        "median_home_value": r.median_home_value,
                        "housing_units": r.total_housing_units,
                        "occupancy_rate": round((r.occupied_units / r.total_housing_units * 100), 2) if r.total_housing_units else None
                    }
                    for r in results
                ]
            }
        else:
            # FALLBACK: No data in database
            logger.warning(f"No census data for {state_code} {year}")
            return {
                "success": True,
                "data_source": "fallback",
                "message": "No data available. Run data import or check back later.",
                "data": []
            }

    except Exception as e:
        logger.error(f"Error fetching census data: {e}")
        # FALLBACK: Return empty result, don't crash
        return {
            "success": False,
            "data_source": "error",
            "error": str(e),
            "data": []
        }


@router.get("/property-listings")
async def get_property_listings(
    city: Optional[str] = None,
    state_code: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db)
):
    """Get scraped property listings with filters"""
    try:
        query = db.query(PropertyListing)

        if state_code:
            query = query.filter(PropertyListing.state_code == state_code.upper())
        if city:
            query = query.filter(PropertyListing.city.ilike(f"%{city}%"))
        if property_type:
            query = query.filter(PropertyListing.property_type == property_type)
        if min_price:
            query = query.filter(PropertyListing.price >= min_price)
        if max_price:
            query = query.filter(PropertyListing.price <= max_price)

        results = query.order_by(PropertyListing.scraped_at.desc()).limit(limit).all()

        return {
            "success": True,
            "count": len(results),
            "data": [
                {
                    "address": r.address,
                    "city": r.city,
                    "state": r.state_code,
                    "price": float(r.price) if r.price else None,
                    "bedrooms": r.bedrooms,
                    "bathrooms": float(r.bathrooms) if r.bathrooms else None,
                    "sqft": r.square_footage,
                    "property_type": r.property_type,
                    "listing_type": r.listing_type,
                    "source": r.source,
                    "url": r.source_url
                }
                for r in results
            ]
        }

    except Exception as e:
        logger.error(f"Error fetching listings: {e}")
        return {
            "success": False,
            "error": str(e),
            "data": []
        }


# Add endpoints for:
# - /fred/indicators
# - /hud/fair-market-rents
# - /bls/employment
# - /sec/reits
# - /epa/environmental-hazards
# - /noaa/climate-risk
```

---

### Step 4: Create Scheduled Task System

Create `/backend/app/scheduler/market_data_scheduler.py`:

```python
"""
Scheduled Tasks for Market Data Imports
Uses APScheduler for daily/weekly/monthly data imports
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from app.db.session import SessionLocal
from app.services.market_data_importers import (
    CensusImporter, FREDImporter, HUDImporter, BLSImporter,
    SECImporter, EPAImporter, NOAAImporter, PropertyScraper
)

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def daily_fred_import():
    """Import FRED data daily at 7 AM"""
    logger.info("Starting daily FRED import...")
    db = SessionLocal()
    try:
        importer = FREDImporter()

        # Import key housing indicators
        series_ids = [
            "HOUST",        # Housing starts
            "MORTGAGE30US",  # 30-year mortgage rate
            "CSUSHPISA",    # Case-Shiller home price index
            "RRVRUSQ156N",  # Rental vacancy rate
        ]

        for series_id in series_ids:
            try:
                await importer.import_series(db, series_id, start_date=datetime.now().date())
                logger.info(f"✅ Imported {series_id}")
            except Exception as e:
                logger.error(f"❌ Failed to import {series_id}: {e}")
                # Continue with next series (don't crash)

    except Exception as e:
        logger.error(f"Daily FRED import failed: {e}")
    finally:
        db.close()


async def weekly_census_import():
    """Import Census data weekly on Sundays"""
    logger.info("Starting weekly Census import...")
    db = SessionLocal()
    try:
        importer = CensusImporter()

        # Import data for top 10 states
        states = ["06", "36", "48", "12", "17", "39", "42", "04", "13", "51"]

        for state_fips in states:
            try:
                await importer.import_state_data(db, state_fips, year=2023)
                logger.info(f"✅ Imported state {state_fips}")
            except Exception as e:
                logger.error(f"❌ Failed to import state {state_fips}: {e}")

    except Exception as e:
        logger.error(f"Weekly Census import failed: {e}")
    finally:
        db.close()


async def daily_property_scrape():
    """Scrape property listings daily at 2 AM"""
    logger.info("Starting daily property scrape...")
    db = SessionLocal()
    try:
        scraper = PropertyScraper()

        # Scrape top markets
        locations = [
            "San Francisco, CA",
            "New York, NY",
            "Los Angeles, CA",
            "Chicago, IL",
            "Austin, TX"
        ]

        for location in locations:
            try:
                await scraper.scrape_and_save(db, location)
                logger.info(f"✅ Scraped {location}")
            except Exception as e:
                logger.error(f"❌ Failed to scrape {location}: {e}")

    except Exception as e:
        logger.error(f"Daily property scrape failed: {e}")
    finally:
        db.close()


def start_scheduler():
    """Initialize and start the scheduler"""

    # Daily imports (7 AM)
    scheduler.add_job(
        daily_fred_import,
        CronTrigger(hour=7, minute=0),
        id="daily_fred_import",
        name="Daily FRED data import",
        replace_existing=True
    )

    # Daily scraping (2 AM)
    scheduler.add_job(
        daily_property_scrape,
        CronTrigger(hour=2, minute=0),
        id="daily_property_scrape",
        name="Daily property listing scrape",
        replace_existing=True
    )

    # Weekly imports (Sunday 3 AM)
    scheduler.add_job(
        weekly_census_import,
        CronTrigger(day_of_week='sun', hour=3, minute=0),
        id="weekly_census_import",
        name="Weekly Census data import",
        replace_existing=True
    )

    # Start scheduler
    scheduler.start()
    logger.info("✅ Market data scheduler started")


def stop_scheduler():
    """Stop the scheduler gracefully"""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
```

**Install APScheduler**:
```bash
/opt/anaconda3/bin/pip install apscheduler
```

**Add to main.py**:
```python
from app.scheduler.market_data_scheduler import start_scheduler, stop_scheduler

@app.on_event("startup")
async def startup_event():
    # Existing startup code...
    start_scheduler()  # Start scheduled tasks

@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()
```

---

### Step 5: Add New Frontend Tabs

Update [frontend/src/pages/RealEstate/MarketIntelligenceDashboard.tsx](frontend/src/pages/RealEstate/MarketIntelligenceDashboard.tsx:433-450):

**Add New Tab Definitions** (line 433):
```tsx
<Tabs value={tabValue} onChange={handleTabChange}>
  <Tab label="🇺🇸 US Official Data" />
  <Tab label="🇮🇱 Israeli Official Data" />
  <Tab label="📊 Demographics" />           {/* NEW */}
  <Tab label="🏠 Property Listings" />      {/* NEW */}
  <Tab label="🌍 Environmental Risk" />     {/* NEW */}
  <Tab label="☁️ Climate Risk" />          {/* NEW */}
  <Tab label="🏢 REIT Performance" />       {/* NEW */}
  <Tab label="💹 Economic Indicators" />
  <Tab label="🏘️ Housing Data" />
  <Tab label="📍 Market Presets" />
</Tabs>
```

**Add Demographics Tab** (after line 831):
```tsx
<TabPanel value={tabValue} index={2}>
  <Box sx={{ px: 2 }}>
    <DemographicsTab stateCode={selectedState} year={selectedYear} />
  </Box>
</TabPanel>
```

**Create Demographics Component** (`frontend/src/components/market-intelligence/DemographicsTab.tsx`):
```tsx
import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Grid, Card, CardContent, Typography, CircularProgress } from '@mui/material';

export const DemographicsTab: React.FC<{stateCode: string, year: number}> = ({ stateCode, year }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`/market-intelligence/census/demographics`, {
          params: { state_code: stateCode, year }
        });
        setData(response.data);
      } catch (error) {
        console.error('Error fetching demographics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [stateCode, year]);

  if (loading) return <CircularProgress />;

  return (
    <Grid container spacing={3}>
      {data?.data?.map((county: any, index: number) => (
        <Grid item xs={12} md={6} lg={4} key={index}>
          <Card>
            <CardContent>
              <Typography variant="h6">{county.county}</Typography>
              <Typography>Population: {county.population?.toLocaleString()}</Typography>
              <Typography>Median Income: ${county.median_income?.toLocaleString()}</Typography>
              <Typography>Median Home Value: ${county.median_home_value?.toLocaleString()}</Typography>
              <Typography>Occupancy Rate: {county.occupancy_rate}%</Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
```

**Repeat similar structure for**:
- Property Listings Tab
- Environmental Risk Tab
- Climate Risk Tab
- REIT Performance Tab

---

## 📅 Schedule

### Daily Tasks (Automated)
- 2:00 AM - Property listing scraping
- 7:00 AM - FRED economic indicators
- 8:00 AM - BLS employment data
- 9:00 AM - HUD Fair Market Rents

### Weekly Tasks (Automated)
- Sunday 3:00 AM - Census demographics
- Monday 4:00 AM - EPA environmental data

### Monthly Tasks (Automated)
- 1st of month, 5:00 AM - NOAA climate data
- 1st of month, 6:00 AM - SEC EDGAR REIT data

---

## 🔒 Error Handling & Fallbacks

### API Call Failures
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    # Process data...
except requests.RequestException as e:
    logger.error(f"API call failed: {e}")
    # FALLBACK: Return cached data or empty result
    return {"success": False, "fallback": True, "data": []}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # FALLBACK: Never crash, always return something
    return {"success": False, "error": "system_error", "data": []}
```

### Database Failures
```python
try:
    db.add(record)
    db.commit()
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    db.rollback()
    # FALLBACK: Log error, continue processing other records
    import_job.records_failed += 1
```

### Missing Data
```python
if not results:
    # FALLBACK: Return empty result with message
    return {
        "success": True,
        "message": "No data available. Run import or check back later.",
        "data": []
    }
```

---

## 🧪 Testing Checklist

### Database
- [ ] All tables created successfully
- [ ] Indexes working properly
- [ ] Sample data inserts correctly

### API Endpoints
- [ ] Census demographics returns data
- [ ] FRED indicators endpoint works
- [ ] HUD rental data accessible
- [ ] Property listings query works
- [ ] All endpoints handle missing data gracefully

### Scheduled Tasks
- [ ] Scheduler starts without errors
- [ ] Daily tasks execute at correct times
- [ ] Weekly tasks execute on schedule
- [ ] Failed imports don't crash scheduler
- [ ] Import logs are readable

### Frontend
- [ ] New tabs render correctly
- [ ] Data loads without errors
- [ ] Loading states work
- [ ] Empty states display properly
- [ ] Error messages are user-friendly

---

## 🚀 Deployment Steps

1. **Install Dependencies**:
   ```bash
   /opt/anaconda3/bin/pip install apscheduler
   ```

2. **Run Database Migration**:
   ```bash
   cd backend
   /opt/anaconda3/bin/alembic upgrade head
   ```

3. **Set API Keys** (optional, demo mode works without):
   ```bash
   export CENSUS_API_KEY="your_key_here"
   export FRED_API_KEY="your_key_here"
   export HUD_API_KEY="your_key_here"
   ```

4. **Restart Backend**:
   ```bash
   cd /Users/yuvalgerzi/Documents/personal\ projects/real_estate_dashboard
   bash start.sh
   ```

5. **Verify Scheduler**:
   - Check logs for "Market data scheduler started"
   - Verify scheduled jobs are registered

6. **Test Endpoints**:
   ```bash
   curl http://localhost:8001/api/v1/market-intelligence/census/demographics?state_code=CA&year=2023
   ```

---

## 📖 Next Steps

1. Complete Step 2 (Data Import Services)
2. Complete Step 3 (Enhanced API Endpoints)
3. Complete Step 4 (Scheduled Tasks)
4. Complete Step 5 (Frontend Tabs)
5. Test all functionality
6. Monitor scheduled imports for 1 week
7. Optimize slow queries
8. Add caching layer if needed

---

## 📊 Expected Results

After full implementation:

- **9 new database tables** storing millions of data points
- **5+ new Market Intelligence tabs** with rich visualizations
- **Automated daily imports** from 7 government APIs
- **Property listing database** updated nightly
- **Zero downtime** with comprehensive fallback mechanisms
- **Historical data** going back years for trend analysis

---

**Status**: Database models complete, implementation guide ready
**Next**: Begin Step 2 (Data Import Services)
**Estimated Completion**: 2-3 days for full implementation
