# Real Estate Data Source API Explorers

Comprehensive exploration scripts for government and commercial real estate data APIs.

## 📚 Overview

This directory contains Python scripts to explore, test, and understand various data source APIs relevant to real estate analysis. Each script demonstrates API capabilities, available fields, and real estate use cases.

## 🗂️ Available Explorers

### Government APIs (FREE)

1. **`census_api_explorer.py`** - US Census Bureau
   - Demographics, housing, economic data
   - American Community Survey (ACS)
   - Historical data back to 1790
   - Geographic levels: nation, state, county, tract, block group

2. **`fred_api_explorer.py`** - Federal Reserve Economic Data
   - 800,000+ economic time series
   - Housing market indicators
   - Mortgage rates and interest rates
   - Commercial real estate metrics

3. **`hud_api_explorer.py`** - HUD USER
   - Fair Market Rents (1983-present)
   - Income Limits by area
   - USPS geographic crosswalks
   - Housing affordability data

4. **`bls_api_explorer.py`** - Bureau of Labor Statistics
   - Employment and unemployment
   - Consumer Price Index (CPI)
   - Producer Price Index (PPI)
   - Construction industry data

5. **`sec_edgar_api_explorer.py`** - SEC EDGAR
   - REIT financial data
   - Company filings (10-K, 10-Q, 8-K)
   - XBRL structured financial data
   - Insider trading information

6. **`epa_api_explorer.py`** - EPA Envirofacts
   - Superfund sites (SEMS)
   - Toxic Release Inventory (TRI)
   - Environmental hazards
   - Property risk assessment

7. **`noaa_api_explorer.py`** - NOAA Climate Data
   - Historical weather data
   - Climate normals
   - Extreme weather events
   - Flood and storm risk

## 🚀 Quick Start

### Prerequisites

```bash
pip install requests
```

### Running an Explorer

```bash
# Make scripts executable
chmod +x *.py

# Run any explorer
python3 census_api_explorer.py
python3 fred_api_explorer.py
python3 hud_api_explorer.py
# ... etc
```

### API Keys

Most APIs require free registration for an API key:

| API | Key Required? | Registration URL |
|-----|---------------|------------------|
| Census | Yes (Free) | https://api.census.gov/data/key_signup.html |
| FRED | Yes (Free) | https://fredaccount.stlouisfed.org/apikeys |
| HUD | Yes (Free) | https://www.huduser.gov/hudapi/public/register |
| BLS | Optional (Free) | https://data.bls.gov/registrationEngine/ |
| SEC EDGAR | No | N/A |
| EPA | No | N/A |
| NOAA | Yes (Free) | https://www.ncdc.noaa.gov/cdo-web/token |

**Note:** Scripts will run in demonstration mode without API keys, showing available endpoints and capabilities.

## 📊 What Each Explorer Does

### Interactive Features

Each explorer provides:

- ✅ **Capabilities Summary**: Overview of available data
- ✅ **Field Exploration**: List all available fields and variables
- ✅ **Sample Queries**: Example API calls with real data
- ✅ **Historical Data**: Access to past records
- ✅ **Export Functions**: Save data to JSON files
- ✅ **Real Estate Use Cases**: Specific applications for property analysis

### Example Usage

```python
from census_api_explorer import CensusAPIExplorer

# Initialize with API key
explorer = CensusAPIExplorer(api_key="your_key_here")

# Get housing data for California counties
data = explorer.get_real_estate_data_sample(state_fips="06", year=2023)

# Export variable catalog
explorer.export_variable_catalog(year=2023)
```

## 🏡 Real Estate Use Cases

### Market Analysis
- **Census**: Demographics, population trends, income levels
- **FRED**: Housing starts, home price indices, mortgage rates
- **HUD**: Fair market rents, income qualification thresholds

### Risk Assessment
- **EPA**: Superfund sites, environmental hazards
- **NOAA**: Flood history, climate risks
- **Census**: Vacancy rates, tenure patterns

### Financial Analysis
- **SEC EDGAR**: REIT performance, public company data
- **BLS**: Construction costs, wage inflation
- **FRED**: Economic indicators, interest rate trends

### Property Valuation
- **Census**: Comparable housing values
- **HUD**: Rent benchmarks
- **BLS**: Cost inflation adjustments

### Development Planning
- **Census**: Housing needs, demographic projections
- **NOAA**: Climate considerations
- **EPA**: Environmental constraints

## 📈 Data Coverage Comparison

| API | Historical Range | Update Frequency | Geographic Granularity |
|-----|-----------------|------------------|----------------------|
| Census | 1790-present | Annual (ACS) | Block Group |
| FRED | 1940s-present | Daily/Monthly | National/State |
| HUD | 1983-present | Annual | ZIP/County/Metro |
| BLS | 1940s-present | Monthly | National/State/Metro |
| SEC EDGAR | 1994-present | Real-time | Company-level |
| EPA | Varies | Continuous | Site-specific |
| NOAA | 1950-present | Daily | Station-level |

## 🔧 Customization

### Adding Your Own Queries

Each explorer can be imported as a module:

```python
from fred_api_explorer import FREDAPIExplorer

explorer = FREDAPIExplorer(api_key="your_key")

# Custom time series request
data = explorer.get_time_series_data(
    series_id='HOUST',
    start_date='2020-01-01',
    end_date='2024-12-31'
)
```

### Extending Functionality

Each explorer follows a consistent pattern:

```python
class APIExplorer:
    def __init__(self, api_key=None):
        # Initialize with optional API key

    def check_api_key(self):
        # Validate API key

    def get_data(self, **params):
        # Fetch data from API

    def show_capabilities_summary(self):
        # Display what the API offers

    def export_to_json(self, data, filename):
        # Save results
```

## 📝 Output Examples

### Console Output
Each explorer provides formatted console output showing:
- Available datasets and endpoints
- Sample data with field descriptions
- Query examples and syntax
- Error handling and troubleshooting

### JSON Exports
Export capabilities include:
- Variable catalogs
- Time series data
- Geographic lookups
- Historical trends

## 🎯 Next Steps

After exploring the APIs:

1. **Review** the comprehensive documentation in `/docs/API_RESEARCH_DATA_SOURCES.md`
2. **Implement** integrations in the main application (see `/docs/INTEGRATION_RECOMMENDATIONS.md`)
3. **Test** API endpoints with your use cases
4. **Integrate** selected APIs into your data pipeline

## 🔒 Security & Best Practices

### API Key Management
- **Never commit API keys** to version control
- Store keys in environment variables
- Use `.env` files (excluded from git)
- Rotate keys periodically

### Rate Limiting
- Respect API rate limits (documented in each script)
- Implement exponential backoff for retries
- Cache responses when appropriate
- Monitor usage against quotas

### Error Handling
All explorers include:
- Try/except blocks for network errors
- Timeout handling
- Response validation
- Graceful degradation

## 📖 Additional Resources

### Official Documentation
- Census API: https://www.census.gov/data/developers.html
- FRED API: https://fred.stlouisfed.org/docs/api/fred/
- HUD API: https://www.huduser.gov/portal/dataset/api.html
- BLS API: https://www.bls.gov/developers/
- SEC EDGAR: https://www.sec.gov/edgar/sec-api-documentation
- EPA: https://www.epa.gov/enviro/envirofacts-data-service-api
- NOAA: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

### Community Resources
- Census API examples: https://github.com/datamade/census
- FRED Python library: https://github.com/mortada/fredapi
- SEC EDGAR tools: https://github.com/sec-edgar

## 🤝 Contributing

To add a new API explorer:

1. Follow the existing script pattern
2. Include comprehensive docstrings
3. Add capability summary
4. Provide real estate use cases
5. Include error handling
6. Update this README

## ⚠️ Disclaimer

These explorers are for research and development purposes. When using in production:

- Verify data accuracy
- Check API terms of service
- Monitor for API changes
- Implement proper error handling
- Add logging and monitoring
- Consider data caching strategies

## 📞 Support

For issues or questions:
- Check official API documentation
- Review error messages and logs
- Verify API keys are valid
- Ensure network connectivity
- Check rate limit compliance

---

**Last Updated:** 2025-11-09
**Version:** 1.0
**Status:** Ready for exploration and testing
