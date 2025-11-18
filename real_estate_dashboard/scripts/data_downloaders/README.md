# Data Downloaders & Scrapers

**Purpose:** Download real estate data without API keys

---

## 📥 Available Scripts

### 1. **government_bulk_downloader.py**

Downloads bulk data from government sources (NO API key required)

**Sources:**
- HUD Fair Market Rents (1983-present)
- Census ACS PUMS Housing Data
- FHFA House Price Index
- SEC EDGAR Quarterly Data
- Data.gov Real Estate Sales
- CORGIS Real Estate Dataset

**Usage:**
```bash
python government_bulk_downloader.py
```

**Interactive Menu:**
```
📊 Available Datasets:
  1. HUD Fair Market Rents
  2. Census ACS PUMS (Housing)
  3. FHFA House Price Index
  4. SEC EDGAR Quarterly Data
  5. Data.gov Real Estate Sales
  6. CORGIS Real Estate Dataset
  7. Download ALL (quick datasets only)
```

**Output:** Files saved to `./government_data/` directory

---

### 2. **real_estate_scraper.py**

Scrapes Zillow, Realtor.com, and Redfin using HomeHarvest

**⚠️ Requires:** `pip install homeharvest` (Python >= 3.10)

**Features:**
- Scrape single or multiple locations
- Find comparable sales
- Market analysis
- Export to CSV/Excel

**Usage:**
```bash
# Install dependency
pip install homeharvest

# Run scraper
python real_estate_scraper.py
```

**Programmatic Usage:**
```python
from real_estate_scraper import RealEstateScraper

scraper = RealEstateScraper(output_dir="./my_data")

# Scrape properties
df = scraper.scrape_location(
    location="90210",
    listing_type="for_sale"
)

# Save results
scraper.save_results(df, "beverly_hills", "csv")
```

---

## 🚀 Quick Start

### Download Government Data

```bash
cd /home/user/real_estate_dashboard/scripts/data_downloaders

# Make executable
chmod +x government_bulk_downloader.py

# Run
python3 government_bulk_downloader.py
```

### Scrape Real Estate Listings

```bash
# Install HomeHarvest
pip install homeharvest

# Run scraper
python3 real_estate_scraper.py
```

---

## 📊 Data Sources Comparison

| Source | API Key | Size | Update Freq | Historical |
|--------|---------|------|-------------|------------|
| HUD FMR | ❌ No | ~10MB | Annual | 1983+ |
| Census PUMS | ❌ No | 500MB+ | Annual | 2005+ |
| FHFA HPI | ❌ No | ~5MB | Quarterly | 1975+ |
| SEC EDGAR | ❌ No | 100MB+ | Quarterly | 2009+ |
| Data.gov | ❌ No | Varies | Varies | Varies |
| CORGIS | ❌ No | <1MB | Static | N/A |
| HomeHarvest | ❌ No | N/A | Real-time | Live |

---

## 💡 Best Practices

### Government Downloads

✅ **DO:**
- Download during off-peak hours
- Store files locally for reuse
- Process incrementally for large files
- Check file sizes before downloading

❌ **DON'T:**
- Download same file multiple times
- Skip virus scanning on ZIP files
- Ignore file format documentation

### Web Scraping

✅ **DO:**
- Add delays between requests (3-5 seconds)
- Use during off-peak hours
- Respect robots.txt
- Personal/research use only
- Cache results

❌ **DON'T:**
- Overload servers
- Scrape too frequently
- Republish scraped data
- Violate Terms of Service
- Ignore HTTP 403/429 errors

---

## 🔧 Installation

### Requirements

```bash
# Core dependencies
pip install requests pandas

# For Excel support
pip install openpyxl

# For DBF files (HUD data)
pip install dbfread
# OR
pip install simpledbf

# For web scraping
pip install homeharvest  # Python >= 3.10 required
```

### Full Installation

```bash
cd /home/user/real_estate_dashboard

# Install all dependencies
pip install requests pandas openpyxl dbfread homeharvest

# Make scripts executable
chmod +x scripts/data_downloaders/*.py
```

---

## 📁 Output Structure

```
data/
├── government_data/
│   ├── hud_fmr_2024/
│   │   ├── FY24_FMRs.dbf
│   │   └── FY24_documentation.txt
│   ├── fhfa_hpi_state.xlsx
│   ├── ct_real_estate_sales.csv
│   ├── corgis_real_estate.csv
│   └── sec_edgar_2024q1/
│       ├── num.txt
│       ├── sub.txt
│       ├── tag.txt
│       └── pre.txt
│
└── scraped_data/
    ├── san_francisco_20241109_143022.csv
    ├── comps_123_main_st_20241109_145633.csv
    └── multi_location_20241109_150245.xlsx
```

---

## 🐛 Troubleshooting

### "homeharvest not found"

```bash
# Check Python version
python --version  # Must be >= 3.10

# Install homeharvest
pip install homeharvest

# If still failing, use pip3
pip3 install homeharvest
```

### "SSL Certificate Error"

```bash
# Update certificates
pip install --upgrade certifi

# Use --trusted-host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org homeharvest
```

### "403 Forbidden" when scraping

This means you've been blocked:
- Wait 24 hours before trying again
- Use VPN to change IP address
- Increase delay between requests
- Try different location

### Census PUMS download slow

Large files (500MB+) take time:
- Use wired internet connection
- Download during off-peak hours
- Consider using Census FTP client
- Split by state if available

---

## 📖 Examples

### Download HUD Data for Multiple Years

```python
from government_bulk_downloader import GovernmentBulkDownloader

downloader = GovernmentBulkDownloader()

for year in range(2020, 2025):
    print(f"Downloading {year}...")
    downloader.download_hud_fair_market_rents(year)
```

### Scrape Multiple ZIP Codes

```python
from real_estate_scraper import RealEstateScraper

scraper = RealEstateScraper()

zip_codes = ['90210', '10001', '60601', '33139', '94102']

df = scraper.scrape_multiple_locations(
    locations=zip_codes,
    listing_type="for_sale",
    delay_seconds=5
)

scraper.save_results(df, "top_zip_codes", "excel")
```

### Market Analysis for City

```python
from real_estate_scraper import RealEstateScraper

scraper = RealEstateScraper()

# Scrape data
df = scraper.scrape_location(
    location="Austin, TX",
    listing_type="for_sale"
)

# Analyze
stats = scraper.analyze_market(df)

print(f"Median Price: ${stats['median_price']:,.0f}")
print(f"Avg $/sqft: ${stats['avg_price_per_sqft']:.2f}")
```

---

## 🔐 Legal & Ethical Use

### Government Data
✅ **Legal:** Public domain
✅ **Free:** No restrictions
✅ **Use:** Any purpose

### Web Scraping
⚠️ **Legal:** Questionable (check ToS)
⚠️ **Restrictions:** May violate website ToS
⚠️ **Use:** Personal/research only

**Recommendation:**
1. Prefer government data when available
2. Use official APIs when possible
3. Scrape only as last resort
4. Always respect rate limits
5. Don't republish scraped data

---

## 📞 Support

For issues:
1. Check requirements are installed
2. Verify Python version >= 3.10 (for HomeHarvest)
3. Check internet connection
4. Review error messages
5. Add delays if getting 403/429 errors

---

**Last Updated:** 2025-11-09
**Python Required:** >= 3.10 (for HomeHarvest)
**Dependencies:** requests, pandas, openpyxl, homeharvest
