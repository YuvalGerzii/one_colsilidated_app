# Backend Scripts

Utility scripts for database population, data synchronization, and maintenance.

## Available Scripts

### 1. `populate_usa_economics.py` - USA Economics Data Sync

**Purpose**: Fetches real economic indicators from BLS and FRED APIs and populates the USA economics database.

**Usage**:
```bash
cd backend
python -m app.scripts.populate_usa_economics
```

**Features**:
- 12 BLS indicators (free, no API key required)
- 24 FRED indicators (requires free API key)
- Categories: Labour, Prices, GDP, Money, Housing, Trade, Government, Business
- Automatic database initialization
- Duplicate prevention and update logic
- Comprehensive error handling

**Setup**:
```bash
# Optional: Get free FRED API key
export FRED_API_KEY="your_key_here"

# Run the script
python -m app.scripts.populate_usa_economics
```

**Documentation**: See [USA_ECONOMICS_DATA_SYNC.md](../../../USA_ECONOMICS_DATA_SYNC.md)

---

### 2. `seed_automation_data.py` - Automation Seed Data

**Purpose**: Seeds initial automation data for the application.

**Usage**:
```bash
python -m app.scripts.seed_automation_data
```

---

### 3. `real_estate/` - Real Estate Scripts

Various real estate data population and maintenance scripts.

---

## Adding New Scripts

When creating new scripts:

1. **Location**: Place in `backend/app/scripts/`
2. **Module**: Make it runnable as a module: `python -m app.scripts.your_script`
3. **Imports**: Use absolute imports from `app.*`
4. **Logging**: Include comprehensive logging
5. **Error Handling**: Handle errors gracefully
6. **Documentation**: Add entry to this README
7. **Help**: Include docstring with usage instructions

**Template**:
```python
"""
Script Name

Description of what this script does.

Usage:
    python -m app.scripts.script_name
"""

import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    try:
        # Your code here
        logger.info("✅ Script completed successfully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Script failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Script Conventions

- **Exit Codes**:
  - `0`: Success
  - `1`: Failure or error
- **Logging Levels**:
  - `INFO`: Progress updates
  - `WARNING`: Non-fatal issues
  - `ERROR`: Errors and failures
- **Output**:
  - Use logging for status messages
  - Use print() for user-facing output
  - Include summary at the end
- **Database**:
  - Always close sessions in finally blocks
  - Handle IntegrityError for duplicates
  - Log all database operations

## Environment Variables

Scripts may require environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `FRED_API_KEY`: FRED API key (for economics data)
- `BLS_API_KEY`: BLS API registration key (optional, increases rate limits)

Set in `.env` file or export in shell:
```bash
export FRED_API_KEY="your_key_here"
```
