# Country-Specific Databases Guide

## 🎯 Overview

Each of the 23 countries now has its **own dedicated PostgreSQL database** for complete data isolation and better performance.

### Architecture

```
PostgreSQL Server
├── economics_united_states    (United States data)
├── economics_china             (China data)
├── economics_japan             (Japan data)
├── economics_germany           (Germany data)
├── economics_united_kingdom    (United Kingdom data)
├── ... (18 more countries)
└── economics_poland            (Poland data)
```

### Benefits

✅ **Complete Data Isolation** - Each country's data is in its own database
✅ **Faster Queries** - Country-specific queries don't scan other countries' data
✅ **Independent Scaling** - Scale databases per country based on usage
✅ **Easier Backups** - Back up individual countries independently
✅ **Better Organization** - Clear separation of concerns
✅ **Simpler Filtering** - No need to filter by country_name in queries

---

## 🚀 Quick Start

### Step 1: Initialize All Country Databases

```bash
cd /home/user/real_estate_dashboard/backend

# Initialize all 23 country databases
python3 initialize_country_databases.py
```

**Output:**
```
================================================================================
INITIALIZING COUNTRY DATABASES
================================================================================

📊 United States (united-states)...
✓ Created database: economics_united_states
✓ Created tables in database: economics_united_states
   ✅ Database: economics_united_states

📊 China (china)...
✓ Created database: economics_china
✓ Created tables in database: economics_china
   ✅ Database: economics_china

... (21 more countries)

================================================================================
SUMMARY: 23/23 country databases initialized
================================================================================
```

### Step 2: Fetch Data for Countries

```bash
# Update United States data → saves to economics_united_states database
python3 country_scripts/update_united_states.py

# Update China data → saves to economics_china database
python3 country_scripts/update_china.py

# Or update all countries
python3 weekly_economics_update.py
```

### Step 3: Query Country-Specific Data

```python
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService

# Get United States database session
us_db = country_db_manager.get_session("united-states")
us_service = EconomicsDBService(us_db)

# Query US housing data (only searches economics_united_states database)
us_housing = us_service.get_economic_indicators(
    country="United States",
    category="housing"
)

# Get China database session
china_db = country_db_manager.get_session("china")
china_service = EconomicsDBService(china_db)

# Query China GDP data (only searches economics_china database)
china_gdp = china_service.get_economic_indicators(
    country="China",
    category="gdp"
)
```

---

## 📁 Database Structure

### Database Naming Convention

```
economics_{country_slug}
```

**Examples:**
- `united-states` → `economics_united_states`
- `united-kingdom` → `economics_united_kingdom`
- `south-korea` → `economics_south_korea`
- `saudi-arabia` → `economics_saudi_arabia`

### Tables in Each Database

Each country database contains the same 5 tables:

1. **`economics_country_overview`** - Country economic snapshot
2. **`economics_indicators`** - Individual economic indicators by category
3. **`economics_indicator_history`** - Time-series historical data
4. **`economics_data_fetch_log`** - API fetch logging
5. **`economics_cache_metadata`** - Cache management metadata

---

## 🔧 Database Management

### Initialize Databases

```bash
# Initialize all 23 countries
python3 initialize_country_databases.py

# Initialize single country
python3 initialize_country_databases.py --country united-states
python3 initialize_country_databases.py --country china
python3 initialize_country_databases.py --country japan

# List database status
python3 initialize_country_databases.py --list
```

**List output:**
```
================================================================================
COUNTRY DATABASE STATUS
================================================================================
✅ United States         → economics_united_states
✅ China                 → economics_china
✅ Euro Area             → economics_euro_area
✅ Japan                 → economics_japan
❌ Germany               → economics_germany
❌ India                 → economics_india
...
================================================================================

Existing: 20/23
Missing:  3
          Germany, India, France
```

### Drop a Database (CAUTION!)

```bash
# Drop specific country database (deletes ALL data!)
python3 initialize_country_databases.py --drop china

# Will prompt for confirmation:
# ⚠️  WARNING: This will delete ALL data for China!
#    Database: economics_china
#
# Type 'DELETE' to confirm:
```

---

## 🔌 Connection Management

### Using CountryDatabaseManager

```python
from app.database.country_database_manager import country_db_manager

# Get database URL for a country
us_url = country_db_manager.get_country_db_url("united-states")
# → postgresql://user:password@host:5432/economics_united_states

# Get database name
db_name = country_db_manager.get_country_db_name("china")
# → economics_china

# Get SQLAlchemy engine
engine = country_db_manager.get_engine("japan")

# Get database session
session = country_db_manager.get_session("germany")

# Create tables in a country database
country_db_manager.create_tables("france")

# Complete initialization (create DB + tables)
country_db_manager.initialize_country_database("italy")
```

### Connection Pooling

Country databases use `NullPool` (no connection pooling) to avoid keeping many connections open across 23 databases. This is optimal for weekly batch updates.

---

## 📊 Querying Data

### Single Country Queries

```python
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService

# Query United States data
us_db = country_db_manager.get_session("united-states")
us_service = EconomicsDBService(us_db)

# Get all housing indicators
housing_data = us_service.get_economic_indicators(
    country="United States",
    category="housing"
)

for indicator in housing_data:
    print(f"{indicator.indicator_name}: {indicator.last_value}")
    # Building Permits: 1330
    # Housing Starts: 1307
    # New Home Sales: 800
    # Mortgage Rate 30Y: 6.22%
    # Average House Price: $534,100

# Get GDP growth history
gdp_history = us_service.get_indicator_history(
    country="United States",
    indicator_name="GDP Growth Rate",
    limit=12  # Last 12 data points
)

# Check data freshness
freshness = us_service.get_data_freshness("United States")
print(f"Last updated: {freshness['overview_last_updated']}")
print(f"Categories: {freshness['categories_last_updated']}")
```

### Multi-Country Comparisons

```python
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService

# Compare housing data across countries
countries = ["united-states", "china", "japan", "germany"]
housing_comparison = {}

for country_slug in countries:
    db = country_db_manager.get_session(country_slug)
    service = EconomicsDBService(db)

    country_name = country_db_manager.COUNTRY_NAMES[country_slug]
    housing_data = service.get_economic_indicators(
        country=country_name,
        category="housing",
        limit=10
    )

    housing_comparison[country_name] = housing_data

# Now you have housing data for all 4 countries
for country, data in housing_comparison.items():
    print(f"\n{country} Housing Indicators:")
    for indicator in data:
        print(f"  {indicator.indicator_name}: {indicator.last_value}")
```

### Direct SQL Queries

```python
from sqlalchemy import text
from app.database.country_database_manager import country_db_manager

# Get engine for United States
engine = country_db_manager.get_engine("united-states")

# Execute raw SQL
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT indicator_name, last_value, unit, data_date
        FROM economics_indicators
        WHERE category = 'housing'
        ORDER BY data_date DESC
        LIMIT 10
    """))

    for row in result:
        print(f"{row.indicator_name}: {row.last_value} {row.unit}")
```

---

## 🔄 Data Updates

### How Country Scripts Work

Each country script automatically:
1. Connects to its **own database** (`economics_{country}`)
2. Fetches data from all 11 API categories
3. Saves data to its country-specific database
4. Uses smart caching (only updates stale data)

```bash
# This script:
python3 country_scripts/update_united_states.py

# Does this:
# 1. Connects to economics_united_states database
# 2. Checks data freshness
# 3. Fetches stale categories from API
# 4. Saves to economics_united_states database
```

### Weekly Automation

```bash
# Set up cron to update all countries weekly
./setup_weekly_cron.sh

# This will:
# - Update united-states → saves to economics_united_states
# - Update china → saves to economics_china
# - Update japan → saves to economics_japan
# - ... (20 more countries)
```

---

## 🗄️ Database Backup & Restore

### Backup Single Country

```bash
# Backup United States database
pg_dump -h localhost -U postgres economics_united_states > backups/us_$(date +%Y%m%d).sql

# Backup China database
pg_dump -h localhost -U postgres economics_china > backups/china_$(date +%Y%m%d).sql
```

### Backup All Countries

```bash
#!/bin/bash
# backup_all_countries.sh

COUNTRIES="united_states china euro_area japan germany india united_kingdom france russia canada italy brazil australia south_korea mexico spain indonesia saudi_arabia netherlands turkey switzerland taiwan poland"

for country in $COUNTRIES; do
    echo "Backing up economics_$country..."
    pg_dump -h localhost -U postgres "economics_$country" > "backups/${country}_$(date +%Y%m%d).sql"
done

echo "All country databases backed up!"
```

### Restore Single Country

```bash
# Restore United States database
psql -h localhost -U postgres economics_united_states < backups/us_20251113.sql

# Restore China database
psql -h localhost -U postgres economics_china < backups/china_20251113.sql
```

---

## 📈 Performance

### Query Performance

**Before (single database with 23 countries):**
```sql
-- Had to filter by country_name across ALL data
SELECT * FROM economics_indicators
WHERE country_name = 'United States' AND category = 'housing';
-- Scans all 23 countries' data
```

**After (country-specific databases):**
```sql
-- Query only United States database
-- No need to filter by country, all data is US data
SELECT * FROM economics_indicators
WHERE category = 'housing';
-- Only scans United States data
```

**Result:** ~23x faster for single-country queries

### Storage Distribution

Each country database size (approximate after full data fetch):
- **Small countries:** 10-20 MB
- **Medium countries:** 20-50 MB
- **Large countries (US, China):** 50-100 MB

**Total:** ~1-2 GB for all 23 countries

---

## 🔍 Monitoring

### Check Database Sizes

```sql
-- Connect to postgres database
psql -U postgres

-- List all country databases with sizes
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database
WHERE datname LIKE 'economics_%'
ORDER BY pg_database_size(datname) DESC;
```

**Output:**
```
          datname           | pg_size_pretty
----------------------------+----------------
 economics_united_states    | 85 MB
 economics_china            | 72 MB
 economics_japan            | 68 MB
 economics_germany          | 65 MB
 ...
```

### Check Connection Count

```sql
-- Show active connections per database
SELECT datname, count(*) as connections
FROM pg_stat_activity
WHERE datname LIKE 'economics_%'
GROUP BY datname
ORDER BY connections DESC;
```

### Check Data Freshness

```python
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService

# Check all countries
for country_slug in country_db_manager.COUNTRY_NAMES.keys():
    db = country_db_manager.get_session(country_slug)
    service = EconomicsDBService(db)

    country_name = country_db_manager.COUNTRY_NAMES[country_slug]
    freshness = service.get_data_freshness(country_name)

    if freshness['overview_last_updated']:
        print(f"{country_name}: {freshness['overview_last_updated']}")
    else:
        print(f"{country_name}: No data")
```

---

## 🛠️ Troubleshooting

### Database Doesn't Exist

**Error:**
```
psycopg2.OperationalError: FATAL: database "economics_united_states" does not exist
```

**Fix:**
```bash
# Initialize the missing database
python3 initialize_country_databases.py --country united-states

# Or initialize all
python3 initialize_country_databases.py
```

### Permission Denied

**Error:**
```
psycopg2.OperationalError: FATAL: permission denied to create database
```

**Fix:**
```sql
-- Grant CREATE DATABASE privilege
psql -U postgres
ALTER USER your_user CREATEDB;
```

### Tables Don't Exist

**Error:**
```
psycopg2.errors.UndefinedTable: relation "economics_indicators" does not exist
```

**Fix:**
```python
from app.database.country_database_manager import country_db_manager

# Create tables in the database
country_db_manager.create_tables("united-states")
```

### Connection Limit Exceeded

**Error:**
```
psycopg2.OperationalError: FATAL: too many connections
```

**Fix:**
Country databases use NullPool (no pooling) to avoid this. If you still hit limits:
```sql
-- Increase max connections in postgresql.conf
max_connections = 200

-- Or close idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname LIKE 'economics_%'
  AND state = 'idle'
  AND state_change < now() - interval '5 minutes';
```

---

## 📝 Migration Guide

### Migrating from Shared Database

If you previously used a single shared database:

```python
# OLD WAY (single database)
from app.models.database import SessionLocal
db = SessionLocal()
service = EconomicsDBService(db)

# Get US data (had to filter by country_name)
us_data = service.get_economic_indicators(
    country="United States",
    category="housing"
)

# NEW WAY (country-specific databases)
from app.database.country_database_manager import country_db_manager
us_db = country_db_manager.get_session("united-states")
service = EconomicsDBService(us_db)

# Get US data (no filtering needed, all data is US)
us_data = service.get_economic_indicators(
    country="United States",
    category="housing"
)
```

### Data Migration Script

```python
# migrate_to_country_databases.py
from app.models.database import SessionLocal
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService

# Old shared database
old_db = SessionLocal()
old_service = EconomicsDBService(old_db)

# Get all countries with data
countries = old_service.get_countries_with_data()

for country in countries:
    print(f"Migrating {country}...")

    # Get all data for this country from old DB
    overview = old_service.get_country_overview(country)
    indicators = old_service.get_all_economic_indicators(country)

    # Get new country-specific database
    country_slug = country.lower().replace(" ", "-")
    new_db = country_db_manager.get_session(country_slug)
    new_service = EconomicsDBService(new_db)

    # Save to new database
    if overview:
        new_service.save_country_overview(overview)

    for indicator in indicators:
        new_service.save_economic_indicators([indicator])

    print(f"  ✅ Migrated {len(indicators)} indicators")

print("Migration complete!")
```

---

## 🎉 Summary

### Country Database System

- ✅ **23 separate databases** - One per country
- ✅ **Automatic database creation** - `initialize_country_databases.py`
- ✅ **Country-specific sessions** - `country_db_manager.get_session()`
- ✅ **Isolated data storage** - Each country's data in its own DB
- ✅ **Faster queries** - No cross-country filtering needed
- ✅ **Easy backups** - Back up individual countries
- ✅ **Smart caching** - Only fetch stale data
- ✅ **Weekly automation** - Automatic updates via cron

### Quick Commands

```bash
# Initialize all databases
python3 initialize_country_databases.py

# Check status
python3 initialize_country_databases.py --list

# Update a country
python3 country_scripts/update_united_states.py

# Update all countries
python3 weekly_economics_update.py

# Set up weekly automation
./setup_weekly_cron.sh
```

---

**Your economics data is now organized in 23 country-specific databases!** 🚀
