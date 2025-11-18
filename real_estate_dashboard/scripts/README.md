# Real Estate Data Scripts

Automated data collection scripts for the Real Estate Dashboard platform.

## Scripts

### 1. Zillow Data Downloader (`zillow_data_downloader.py`)

Downloads Zillow Research CSV files including:
- ZHVI (Zillow Home Value Index)
- ZORI (Zillow Observed Rent Index)
- Inventory data
- Sales data

**Usage:**
```bash
# Download all datasets
python zillow_data_downloader.py

# Download priority datasets only
python zillow_data_downloader.py --priority-only

# Download specific categories
python zillow_data_downloader.py --categories zhvi zori

# Show cron setup instructions
python zillow_data_downloader.py --setup-cron
```

**Monthly Automation (Cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs 1st of each month at 2 AM)
0 2 1 * * /usr/bin/python3 /path/to/zillow_data_downloader.py
```

### 2. Zillow Mortgage Rates (`zillow_mortgage_rates.py`)

Fetches current mortgage rates from Zillow's API.

**Usage:**
```bash
# Get current national rates
python zillow_mortgage_rates.py --current-only

# Get rates for specific criteria
python zillow_mortgage_rates.py --loan-amount 300000 --credit-score 740 --state CA

# Run daily fetch and save
python zillow_mortgage_rates.py --daily-fetch

# Save results
python zillow_mortgage_rates.py --save
```

### 3. Dotloop API Client (`dotloop_api_client.py`)

Interfaces with Dotloop's real estate transaction management API.

**Setup:**
1. Register at https://info.dotloop.com/developers
2. Set environment variables:
   ```bash
   export DOTLOOP_CLIENT_ID="your_client_id"
   export DOTLOOP_CLIENT_SECRET="your_client_secret"
   ```

**Usage:**
```bash
# Show setup instructions
python dotloop_api_client.py --setup

# Authorize (opens browser)
python dotloop_api_client.py --authorize

# Get profiles
python dotloop_api_client.py --get-profiles

# Get loops for a profile
python dotloop_api_client.py --get-loops --profile-id 12345

# Fetch all data
python dotloop_api_client.py --fetch-all

# Refresh token manually
python dotloop_api_client.py --refresh
```

## Storage Structure

```
storage/
├── zillow/
│   ├── zhvi/                    # Home value index data
│   ├── zori/                    # Rent index data
│   ├── inventory/               # For-sale inventory
│   ├── sales/                   # Sales data
│   ├── download_manifest.json   # Download log
│   └── download.log             # Detailed log
├── dotloop/
│   ├── dotloop_tokens.json      # OAuth tokens (auto-refreshed)
│   ├── dotloop_data_*.json      # Fetched data
│   └── dotloop.log              # API log
└── upload/                      # For file uploads
```

## Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

## Dependencies

Install required packages:

```bash
pip install requests python-dotenv
```

## Notes

- Zillow API may require additional authentication for some endpoints
- Dotloop access tokens expire after 12 hours (auto-refreshed)
- Run `--setup` flag on any script for detailed instructions
