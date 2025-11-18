# Integrations Configuration & Troubleshooting Guide

## Executive Summary

This guide provides a comprehensive analysis of the integrations tab configuration, identifies issues causing timeouts and data retrieval failures, and provides step-by-step instructions for proper configuration and testing.

**Critical Issues Found:**
1. 🔴 **HUD Integration** - Missing required API key authentication
2. 🟡 **FHFA Integration** - Returns placeholder data, not actual API data
3. 🟡 **Data.gov US** - Disabled despite being free and functional
4. 🟡 **Bank of Israel** - Returns placeholder data instead of actual API calls
5. 🟡 **BLS Integration** - Missing recommended API key for higher rate limits

---

## Table of Contents

1. [Current Configuration Analysis](#current-configuration-analysis)
2. [Integration-by-Integration Review](#integration-by-integration-review)
3. [Timeout Analysis & Causes](#timeout-analysis--causes)
4. [Configuration Instructions](#configuration-instructions)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Current Configuration Analysis

### Currently Enabled Integrations

| Integration | Status | API Key Required | Implementation Status |
|------------|--------|------------------|----------------------|
| BLS | ✅ Enabled | Optional | ✅ Working |
| Bank of Israel | ✅ Enabled | No | ⚠️ Placeholder data |
| HUD | ✅ Enabled | **YES (Missing!)** | ❌ Will fail for data |
| FHFA | ✅ Enabled | No | ⚠️ Placeholder data |

### Currently Disabled (But Should Work)

| Integration | Status | Reason Disabled | Should Enable? |
|------------|--------|-----------------|----------------|
| Data.gov US | ❌ Disabled | "API issues" | ✅ Yes - Free, no key |
| Data.gov IL | ❌ Disabled | "API issues" | ✅ Yes - Free, no key |
| Census | ❌ Disabled | "API errors" | ⚠️ After getting key |
| FRED | ❌ Disabled | Requires API key | ✅ Yes - Free key |

---

## Integration-by-Integration Review

### 1. Data.gov US Integration 🟢 FREE (No Key Required)

**Official Documentation:**
- Base URL: `https://catalog.data.gov/api/3/action/`
- Alternative: `https://api.gsa.gov/technology/datagov/v3/action/`
- API Type: CKAN API (Open Data Platform)
- Authentication: **None required**
- Rate Limit: No strict limit (be respectful)
- Documentation: https://data.gov/developers/apis/

**Current Implementation Status:**
- ✅ Code: Correctly implemented in `datagov_us.py`
- ✅ Base URL: Correct
- ✅ Authentication: Correctly doesn't use API key
- ❌ **Issue: Disabled in settings** (`ENABLE_DATAGOV_US_INTEGRATION: bool = False`)
- Comment says: "Temporarily disabled due to API issues"

**What Data It Provides:**
- 300,000+ government datasets
- Federal real property data
- Housing and urban development data
- Economic indicators
- State and local government data
- Real estate and property records
- Downloadable datasets in multiple formats

**Configuration:**
```bash
# In .env file
ENABLE_DATAGOV_US_INTEGRATION=True
# No API key needed!
```

**Timeout Configuration:**
- Test connection: 10 seconds ✅
- Search datasets: 30 seconds ✅
- Get dataset: 10 seconds ✅

**Potential Timeout Causes:**
1. Large dataset searches (>1000 results)
2. Network latency to government servers
3. Server-side processing time for complex queries

**Testing:**
```bash
# Test the integration
curl http://localhost:8000/api/v1/integrations/test/datagov_us

# Search for real estate data
curl http://localhost:8000/api/v1/integrations/official-data/datagov-us/search?query=real%20estate&limit=10
```

---

### 2. HUD (Housing & Urban Development) Integration 🔴 REQUIRES API KEY

**Official Documentation:**
- Base URL: `https://www.huduser.gov/hudapi/public/`
- API Endpoints:
  - FMR: `https://www.huduser.gov/hudapi/public/fmr`
  - Income Limits: `https://www.huduser.gov/hudapi/public/il`
  - USPS Crosswalk: `https://www.huduser.gov/hudapi/public/usps`
- Authentication: **Bearer Token Required**
- Rate Limit: **60 queries per minute**
- Documentation: https://www.huduser.gov/portal/dataset/fmr-api.html

**CRITICAL ISSUE:**
The current implementation tests against `https://www.hud.gov` (the public website) but **DOES NOT implement the actual API authentication** required by the HUD User API.

**Required Setup:**
1. Register at: https://www.huduser.gov/hudapi/public/register
2. Select which datasets you want (FMR, Income Limits, CHAS, USPS)
3. Confirm email
4. Login at: https://www.huduser.gov/hudapi/public/login
5. Click "Create New Token"
6. Copy the token

**What Data It Provides:**
- Fair Market Rents (FMR) by ZIP code
- Area Median Income (AMI) data
- Income limits for affordable housing programs
- Housing Choice Voucher data
- Public housing statistics
- Homelessness Point-in-Time (PIT) count data
- USPS ZIP Code to County crosswalk

**Current Code Issues:**
```python
# Current implementation (WRONG):
async def test_connection(self) -> IntegrationResponse:
    response = await client.get(
        "https://www.hud.gov",  # ❌ Wrong - this is just the website
        timeout=10.0,
        follow_redirects=True
    )
```

**Correct Implementation Needed:**
```python
# Should be (CORRECT):
async def test_connection(self) -> IntegrationResponse:
    headers = {"Authorization": f"Bearer {self.config.api_key}"}
    response = await client.get(
        "https://www.huduser.gov/hudapi/public/fmr/data/2025/12345",  # Test with real endpoint
        headers=headers,
        timeout=10.0
    )
```

**Configuration:**
```bash
# In .env file
ENABLE_HUD_INTEGRATION=True
HUD_API_KEY=your_token_from_huduser_portal

# In settings.py - Need to add:
HUD_API_KEY: Optional[str] = None
```

**Example API Call:**
```bash
# Get FMR for ZIP code 90210
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://www.huduser.gov/hudapi/public/fmr/data/2025/90210?format=json"
```

**Timeout Configuration:**
- Current: 10 seconds (should be adequate)
- Recommended: 15 seconds for data queries

**Why It Times Out:**
1. ❌ Not using actual API endpoints (testing wrong URL)
2. ❌ Missing Bearer token authentication
3. ❌ API returns 401 Unauthorized (which might timeout differently)

---

### 3. FHFA (Federal Housing Finance Agency) Integration 🟡 NO REST API

**Official Documentation:**
- Base URL: https://www.fhfa.gov/data/hpi
- Data Access: **CSV/Excel Downloads Only** (No REST API)
- Authentication: None required
- Format: Downloadable datasets
- Documentation: https://www.fhfa.gov/data/hpi/datasets

**Current Implementation Status:**
- ⚠️ Code returns **placeholder data** only
- ✅ Website connectivity test works
- ❌ No actual data retrieval implemented

**What Data It Provides:**
- House Price Index (HPI) - National, State, Metro, ZIP
- Purchase-Only HPI
- All-Transactions HPI
- Distress-Free HPI
- Historical data from 1975 to present
- Quarterly updates

**Data Formats:**
- CSV files
- Excel spreadsheets
- Text files

**Current Code:**
```python
async def get_house_price_index(self, geography_type: str = "national") -> IntegrationResponse:
    return self._success_response({
        "geography_type": geography_type,
        "message": "FHFA House Price Index data",
        "description": "HPI measures average price changes...",
        "data_source": "https://www.fhfa.gov/...",
        "note": "Data available as CSV downloads",  # ⚠️ No actual data returned!
    })
```

**Why It's Placeholder:**
FHFA doesn't provide a REST API. Data must be:
1. Downloaded as CSV files
2. Parsed and imported into database
3. Served from your own database

**Recommended Implementation:**
1. Create a scheduled job to download CSV files monthly/quarterly
2. Parse and store in PostgreSQL
3. Create database models for HPI data
4. Serve from local database via API endpoints

**Download URLs:**
- National HPI: https://www.fhfa.gov/data/hpi/datasets#qat
- State HPI: https://www.fhfa.gov/data/hpi/datasets#qpo
- Metro HPI: https://www.fhfa.gov/data/hpi/datasets#mpo
- ZIP HPI: https://www.fhfa.gov/data/hpi/datasets#zip

**Configuration:**
```bash
# In .env file
ENABLE_FHFA_INTEGRATION=True
# No API key needed - but data import job needed
```

**Testing:**
```bash
# Current test only checks website connectivity
curl http://localhost:8000/api/v1/integrations/test/fhfa

# Returns placeholder data (not actual HPI values)
curl http://localhost:8000/api/v1/integrations/official-data/fhfa/house-price-index
```

---

### 4. BLS (Bureau of Labor Statistics) Integration 🟢 FREE (Key Recommended)

**Official Documentation:**
- Base URL: `https://api.bls.gov/publicAPI/v2`
- Authentication: Optional API key (strongly recommended)
- Rate Limits:
  - **Without key:** 25 queries per day, 10 years of data per query
  - **With key:** 500 queries per day, 20 years of data per query
- Documentation: https://www.bls.gov/developers/

**Current Implementation Status:**
- ✅ Code: Properly implemented
- ✅ Authentication: Supports optional API key
- ✅ Timeout: 30 seconds (appropriate)
- ⚠️ Missing API key (limits to 25 queries/day)

**What Data It Provides:**
- Unemployment rates by area
- Employment statistics
- Consumer Price Index (CPI)
- Producer Price Index (PPI)
- Average hourly earnings
- Job growth metrics

**API Key Registration:**
1. Visit: https://data.bls.gov/registrationEngine/
2. Fill out registration form
3. Verify email
4. Receive API key immediately

**Configuration:**
```bash
# In .env file
ENABLE_BLS_INTEGRATION=True
BLS_API_KEY=your_api_key_here  # Optional but recommended
```

**Timeout Configuration:**
- Current: 30 seconds ✅
- Recommended: Keep at 30 seconds

**Why It Might Timeout:**
1. ✅ 30-second timeout is appropriate per BLS recommendations
2. Complex queries with multiple series can be slow
3. BLS monitors and may throttle aggressive requests
4. Peak usage times (business hours) may be slower

**Best Practices:**
- ✅ Use API key to increase limits
- ✅ Limit queries to 25 series at a time
- ✅ Use date ranges (don't request all historical data)
- ✅ Implement caching for frequently accessed data
- ✅ Respect the daily query limit

**Testing:**
```bash
# Test connection
curl http://localhost:8000/api/v1/integrations/test/bls

# Get unemployment rate
curl http://localhost:8000/api/v1/integrations/market-data/bls/unemployment
```

---

### 5. Bank of Israel Integration 🟡 PLACEHOLDER DATA

**Official Documentation:**
- Base URL: `https://www.boi.org.il/PublicApi/GetData`
- Alternative: `https://edge.boi.org.il`
- Authentication: None required
- Documentation: https://www.boi.org.il/en/economic-roles/statistics/

**Current Implementation Status:**
- ⚠️ Returns **placeholder data** only
- ✅ Website connectivity test works
- ❌ No actual data retrieval implemented

**What Data It Should Provide:**
- Consumer Price Index (CPI)
- Interest rates
- Exchange rates
- Housing price index
- Economic indicators
- GDP data
- Employment statistics
- Balance of payments

**Current Code Issues:**
```python
async def get_interest_rate(self) -> IntegrationResponse:
    return self._success_response({
        "message": "Interest rate data",
        "note": "Bank of Israel provides this data through their statistical portal",
        # ❌ No actual data returned!
    })
```

**Why It's Placeholder:**
The Bank of Israel API endpoints are not fully documented in English. The actual API structure needs to be researched.

**Recommended Actions:**
1. Research actual API endpoints (Hebrew documentation may be needed)
2. Test actual data retrieval endpoints
3. Implement proper data fetching
4. Document the API structure

**Configuration:**
```bash
# In .env file
ENABLE_BANK_OF_ISRAEL_INTEGRATION=True
# No API key needed
```

---

### 6. FRED Integration 🟢 FREE (Key Required)

**Official Documentation:**
- Base URL: `https://api.stlouisfed.org/fred/`
- Authentication: **API key required** (free)
- Rate Limit: No strict limit (be respectful)
- Documentation: https://fred.stlouisfed.org/docs/api/

**Current Implementation Status:**
- ✅ Code: Properly implemented
- ❌ **Disabled:** Requires API key
- Status: `ENABLE_FRED_INTEGRATION: bool = False`

**What Data It Provides:**
- Mortgage rates (30-year, 15-year, etc.)
- Housing indicators
- Interest rates
- Economic indicators
- GDP data
- Unemployment data
- Inflation data

**API Key Registration:**
1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Create free account or login
3. Request API key (instant approval)
4. Copy your API key

**Configuration:**
```bash
# In .env file
ENABLE_FRED_INTEGRATION=True
FRED_API_KEY=your_api_key_here
```

**Why You Should Enable:**
- ✅ Completely free
- ✅ No rate limits (within reason)
- ✅ High-quality economic data
- ✅ Includes mortgage rates (critical for real estate)
- ✅ Regularly updated data

---

## Timeout Analysis & Causes

### Current Timeout Configuration

| Operation Type | Current Timeout | Recommended | Notes |
|---------------|----------------|-------------|-------|
| Test connections | 10 seconds | 10-15 seconds | ✅ Adequate |
| Data fetches | 10-30 seconds | 30 seconds | ✅ Adequate |
| Large uploads | 60 seconds | 60 seconds | ✅ Adequate |
| Frontend API calls | 10 seconds | 15-30 seconds | ⚠️ May be too short |

### Common Timeout Causes

#### 1. **HUD Integration Timeouts**
**Root Causes:**
- ❌ Testing wrong URL (website vs API endpoint)
- ❌ Missing authentication causes 401 errors
- ❌ 401 errors may not fail gracefully, leading to timeout

**Solution:**
- Implement Bearer token authentication
- Use actual API endpoints
- Handle 401 errors properly

#### 2. **Data.gov Timeouts**
**Root Causes:**
- Complex search queries with many results
- Government servers may be slow during peak hours
- Network latency

**Solutions:**
- ✅ Increase timeout to 30 seconds (already done)
- ✅ Implement pagination (already done)
- ✅ Limit initial queries to 20 results (already done)
- Add retry logic with exponential backoff
- Cache search results

#### 3. **BLS Timeouts**
**Root Causes:**
- Requesting too many series at once
- Requesting large date ranges
- Peak usage times
- BLS throttling aggressive requests

**Solutions:**
- ✅ 30-second timeout (already appropriate)
- Use API key to avoid being flagged
- Limit to 25 series per request
- Implement request caching
- Space out requests (don't burst)

#### 4. **Frontend 10-Second Timeout**
**Issue:** Frontend aborts requests after 10 seconds

```typescript
// frontend/src/pages/IntegrationsPage.tsx:132
const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
```

**Problem:** Backend calls to government APIs can take 15-30 seconds, causing frontend to abort early.

**Solution:**
```typescript
// Increase to 30 seconds for integration status
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
```

### Retry and Fallback Mechanism

**Current Implementation:** ✅ Good!

The frontend implements:
1. ✅ Retry logic (up to 2 retries)
2. ✅ 15-minute cache
3. ✅ Fallback to cached data on error
4. ✅ Hardcoded fallback data if cache unavailable

```typescript
// Frontend retry logic
if (retryCount < 2 && (err.code === 'ECONNABORTED' || err.message?.includes('Network Error'))) {
  setTimeout(() => fetchIntegrationStatus(retryCount + 1), 1000 * (retryCount + 1));
  return;
}
```

**Backend Implementation:** ✅ Good!

```python
# Backend retry with exponential backoff
async def _retry_with_exponential_backoff(self, func, max_retries: int = 3):
    for attempt in range(max_retries):
        delay = min(base_delay * (2 ** attempt), max_delay)
        await asyncio.sleep(delay)
```

---

## Configuration Instructions

### Step 1: Enable Free Integrations (No API Key Required)

**Quick Win - Enable These Immediately:**

```bash
# Edit backend/.env file
ENABLE_INTEGRATIONS=True

# Free integrations (no key needed):
ENABLE_DATAGOV_US_INTEGRATION=True      # 300,000+ datasets
ENABLE_DATAGOV_IL_INTEGRATION=True       # Israeli government data
ENABLE_BANK_OF_ISRAEL_INTEGRATION=True   # Economic indicators (placeholder for now)
ENABLE_BLS_INTEGRATION=True              # Employment data
ENABLE_FHFA_INTEGRATION=True             # House price index (placeholder for now)
```

### Step 2: Get Free API Keys

**2a. BLS API Key** (5 minutes)
1. Visit: https://data.bls.gov/registrationEngine/
2. Fill out form (name, email, organization)
3. Verify email
4. Add to `.env`:
```bash
BLS_API_KEY=your_bls_api_key_here
```

**2b. FRED API Key** (5 minutes)
1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Create account or login
3. Request API key (instant)
4. Add to `.env`:
```bash
FRED_API_KEY=your_fred_api_key_here
ENABLE_FRED_INTEGRATION=True
```

**2c. HUD User API** (10 minutes + email verification)
1. Visit: https://www.huduser.gov/hudapi/public/register
2. Select datasets: Fair Market Rent, Income Limits
3. Verify email
4. Login: https://www.huduser.gov/hudapi/public/login
5. Click "Create New Token"
6. Add to `.env`:
```bash
HUD_API_KEY=your_token_here
```

**⚠️ NOTE:** HUD integration code needs to be fixed to use the API key!

### Step 3: Update Settings.py

Add missing setting for HUD API key:

```python
# backend/app/settings.py
# Add after line 172:
HUD_API_KEY: Optional[str] = None  # Free - requires registration
```

### Step 4: Fix HUD Integration Code

The HUD integration needs to be updated to use Bearer token authentication.

**File:** `backend/app/integrations/official_data/hud.py`

**Changes Needed:**
1. Accept API key in config
2. Use Bearer token in headers
3. Call actual API endpoints
4. Handle authentication errors

### Step 5: Increase Frontend Timeout

**File:** `frontend/src/pages/IntegrationsPage.tsx`

Change line 132:
```typescript
// Before:
const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

// After:
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
```

### Step 6: Restart Services

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

---

## Testing & Verification

### Automated Testing Script

Save as `test_integrations.sh`:

```bash
#!/bin/bash
BASE_URL="http://localhost:8000/api/v1/integrations"

echo "🧪 Testing Integrations..."
echo ""

# Test overall status
echo "1. Testing Integration Status:"
curl -s "$BASE_URL/status" | jq '.active_count, .total_count'
echo ""

# Test each integration
integrations=("bls" "datagov_us" "bank_of_israel" "hud" "fhfa")

for integration in "${integrations[@]}"; do
    echo "2. Testing $integration:"
    curl -s "$BASE_URL/test/$integration" | jq '.success, .message // .error'
    echo ""
done

echo "✅ Testing complete!"
```

Usage:
```bash
chmod +x test_integrations.sh
./test_integrations.sh
```

### Manual Testing Steps

#### Test 1: Check Integration Status
```bash
curl http://localhost:8000/api/v1/integrations/status | jq
```

**Expected Output:**
```json
{
  "integrations": {
    "bls": {"status": "active", "available": true},
    "datagov_us": {"status": "active", "available": true},
    "hud": {"status": "active", "available": true},
    "fhfa": {"status": "active", "available": true},
    "bank_of_israel": {"status": "active", "available": true}
  },
  "total_count": 5,
  "active_count": 5
}
```

#### Test 2: Test Individual Connections
```bash
# BLS
curl http://localhost:8000/api/v1/integrations/test/bls | jq

# Data.gov
curl http://localhost:8000/api/v1/integrations/test/datagov_us | jq

# HUD (will fail without API key fix)
curl http://localhost:8000/api/v1/integrations/test/hud | jq

# FHFA
curl http://localhost:8000/api/v1/integrations/test/fhfa | jq
```

#### Test 3: Fetch Actual Data
```bash
# BLS Unemployment Rate
curl http://localhost:8000/api/v1/integrations/market-data/bls/unemployment | jq

# Data.gov Search
curl "http://localhost:8000/api/v1/integrations/official-data/datagov-us/search?query=housing&limit=5" | jq

# FHFA House Price Index (returns placeholder)
curl http://localhost:8000/api/v1/integrations/official-data/fhfa/house-price-index | jq
```

### Frontend Testing

1. Open browser: http://localhost:3000/integrations
2. Check "Total Integrations" count
3. Check "Active" count
4. Click "Test Connection" on each integration
5. Click "More" to see features and documentation links
6. Verify no timeout errors in browser console

### Success Criteria

✅ **All integrations should:**
- Show as "active" in status
- Test connection successfully
- Return data (or clear placeholder message)
- Complete within 30 seconds
- Not show timeout errors

⚠️ **Expected Limitations:**
- FHFA returns placeholder data (needs CSV import implementation)
- Bank of Israel returns placeholder data (needs API research)
- HUD needs code fix before working

---

## Troubleshooting Common Issues

### Issue 1: "Integration not available"

**Symptoms:**
```json
{"success": false, "error": "Integration not available"}
```

**Causes:**
- Integration disabled in settings
- Missing API key (for integrations that require it)
- Integration failed to initialize

**Solutions:**
1. Check `.env` file:
```bash
grep ENABLE_.*_INTEGRATION backend/.env
```

2. Verify API keys are set (if required):
```bash
grep "_API_KEY" backend/.env
```

3. Check backend logs for initialization errors:
```bash
tail -f backend/logs/app.log
```

4. Restart backend:
```bash
cd backend
uvicorn app.main:app --reload
```

---

### Issue 2: Timeout Errors

**Symptoms:**
- Frontend shows "API unavailable" after 10 seconds
- Browser console shows "AbortError"
- Backend logs show incomplete requests

**Causes:**
- Frontend timeout too short (10 seconds)
- Government API servers slow
- Network latency
- Complex queries taking too long

**Solutions:**

**1. Increase Frontend Timeout:**
Edit `frontend/src/pages/IntegrationsPage.tsx`:
```typescript
const timeoutId = setTimeout(() => controller.abort(), 30000); // Increase to 30s
```

**2. Check Backend Timeouts:**
Verify timeout values in integration files:
```python
# Should be 30 seconds for data fetches
timeout=30.0
```

**3. Enable Caching:**
The frontend already has 15-minute caching. Verify it's working:
```typescript
const CACHE_EXPIRY_MS = 15 * 60 * 1000; // 15 minutes
```

**4. Test with Direct API Call:**
Bypass frontend to test backend timeout:
```bash
time curl http://localhost:8000/api/v1/integrations/status
```

**5. Check Network:**
```bash
# Test government API reachability
time curl -I https://catalog.data.gov/api/3/action/status_show
time curl -I https://api.bls.gov/publicAPI/v2/
```

---

### Issue 3: HUD Integration Fails

**Symptoms:**
```json
{"success": true, "message": "Successfully connected to HUD services"}
```
But actual data calls fail with 401 Unauthorized.

**Cause:**
HUD integration tests the website (www.hud.gov) instead of the API (huduser.gov/hudapi), and doesn't implement Bearer token authentication.

**Solution:**

**Step 1: Get API Token**
1. Register: https://www.huduser.gov/hudapi/public/register
2. Verify email
3. Login and create token

**Step 2: Add to Settings**
Edit `backend/app/settings.py`:
```python
# Add after line 172:
HUD_API_KEY: Optional[str] = None  # Free - requires registration
```

**Step 3: Update .env**
```bash
HUD_API_KEY=your_token_here
```

**Step 4: Fix Integration Code**
Edit `backend/app/integrations/official_data/hud.py`:

```python
def __init__(self, config: IntegrationConfig):
    config.is_free = True
    config.requires_api_key = True  # Change from False to True
    super().__init__(config)

async def test_connection(self) -> IntegrationResponse:
    """Test HUD API connection"""
    try:
        # Check if API key is available
        if not self.config.api_key:
            return IntegrationResponse(
                success=False,
                error="HUD API key required. Register at https://www.huduser.gov/hudapi/public/register"
            )

        # Test with actual API endpoint
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        async with httpx.AsyncClient() as client:
            # Test with FMR endpoint for a known ZIP code
            response = await client.get(
                f"{self.HUD_USER_API}/fmr/listYears",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()

            return self._success_response({
                "message": "Successfully connected to HUD User API",
                "status": "operational",
                "available_years": response.json()
            })

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return IntegrationResponse(
                success=False,
                error="Invalid HUD API key. Check your token at https://www.huduser.gov/hudapi/public/login"
            )
        return self._handle_error(e, "HUD connection test")
    except Exception as e:
        return self._handle_error(e, "HUD connection test")
```

**Step 5: Update Data Methods**
Add headers to all data fetching methods:
```python
async def get_fair_market_rent(self, zip_code: str, year: Optional[int] = None) -> IntegrationResponse:
    if not self.is_available:
        return IntegrationResponse(success=False, error="HUD integration not available")

    if not self.config.api_key:
        return IntegrationResponse(success=False, error="HUD API key required")

    try:
        from datetime import datetime
        if not year:
            year = datetime.now().year

        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.FMR_API}/data/{year}/{zip_code}",
                headers=headers,
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()

            return self._success_response({
                "zip_code": zip_code,
                "year": year,
                "data": data
            })
    except Exception as e:
        return self._handle_error(e, "get_fair_market_rent")
```

**Step 6: Restart and Test**
```bash
# Restart backend
cd backend
uvicorn app.main:app --reload

# Test
curl http://localhost:8000/api/v1/integrations/test/hud | jq
```

---

### Issue 4: "API unavailable - showing cached data"

**Symptoms:**
Yellow warning banner in frontend showing cached data with timestamp.

**Causes:**
- Backend server not running
- Backend returning errors
- Network connectivity issues
- CORS issues

**This is actually a FEATURE, not a bug!** The caching prevents repeated failures.

**To Verify Backend:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check integration status
curl http://localhost:8000/api/v1/integrations/status

# Check for errors
curl -v http://localhost:8000/api/v1/integrations/status 2>&1 | grep "HTTP"
```

**To Clear Cache:**
1. Open browser DevTools (F12)
2. Go to Application → Local Storage
3. Delete `integrations_status_cache` and `integrations_cache_timestamp`
4. Refresh page

---

### Issue 5: Data.gov Returns "Package_list Disabled"

**Symptoms:**
```json
{"success": false, "error": "Endpoint action/package_list is disabled"}
```

**Cause:**
Data.gov disabled the `package_list` endpoint. Should use `package_search` instead.

**Solution:**
The code already uses `package_search` correctly. If you see this error, check you're not using `package_list` anywhere.

---

### Issue 6: BLS "Daily Query Limit Exceeded"

**Symptoms:**
```json
{"status": "REQUEST_FAILED", "message": ["Daily query limit exceeded"]}
```

**Cause:**
Without API key: 25 queries/day limit
With API key: 500 queries/day limit

**Solutions:**

**1. Register for API Key** (increases limit to 500/day)
https://data.bls.gov/registrationEngine/

**2. Implement Caching**
Cache BLS data for 24 hours to reduce API calls:
```python
# Add to BLS integration
@lru_cache(maxsize=100, ttl=86400)  # 24 hours
async def get_series_data(self, series_ids: List[str]):
    # ... existing code
```

**3. Check Query Count**
Monitor how many queries your app makes:
```bash
# Check backend logs
grep "BLS API" backend/logs/app.log | wc -l
```

**4. Reduce Query Frequency**
- Don't fetch on every page load
- Use cached data from database
- Fetch only during off-peak hours
- Implement rate limiting

---

### Issue 7: FHFA Returns Placeholder Data

**Symptoms:**
```json
{
  "message": "FHFA House Price Index data",
  "note": "Data available as CSV downloads"
}
```
No actual HPI values returned.

**Cause:**
FHFA doesn't provide a REST API. Data must be downloaded as CSV files.

**This is NOT a bug** - it's by design. FHFA only provides downloadable datasets.

**Solutions:**

**Option 1: Manual Download & Import** (Quick)
1. Download CSV: https://www.fhfa.gov/data/hpi/datasets
2. Create database table for HPI data
3. Import CSV into database
4. Update integration to query database

**Option 2: Automated Download** (Better)
Create a scheduled job:
```python
# backend/app/tasks/fhfa_import.py
import httpx
import pandas as pd
from datetime import datetime

async def import_fhfa_hpi_data():
    """Download and import FHFA HPI data monthly"""
    csv_url = "https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_master.csv"

    async with httpx.AsyncClient() as client:
        response = await client.get(csv_url, timeout=60.0)

    df = pd.read_csv(io.StringIO(response.text))

    # Import to database
    for _, row in df.iterrows():
        # Save to database
        await db.execute(
            "INSERT INTO fhfa_hpi (date, state, value) VALUES ($1, $2, $3)",
            row['date'], row['state'], row['value']
        )
```

**Option 3: Use FRED Instead**
FRED (Federal Reserve Economic Data) has FHFA data available via API:
```python
# Use FRED integration to get FHFA HPI
series_id = "HPIPONM226S"  # FHFA Purchase-Only House Price Index
result = await fred_integration.get_series(series_id)
```

---

### Issue 8: Bank of Israel Returns Placeholder Data

**Symptoms:**
```json
{
  "message": "Interest rate data",
  "note": "Bank of Israel provides this data through their statistical portal"
}
```

**Cause:**
The Bank of Israel API endpoints are not fully documented in English, and the actual data fetching is not implemented.

**Solution:**

**Research Needed:**
1. The Bank of Israel has a public API but documentation is primarily in Hebrew
2. Actual API endpoint structure needs to be discovered
3. Test different endpoints to find working data sources

**Known Endpoint:**
```
https://www.boi.org.il/PublicApi/GetData
```

**Parameters (needs research):**
- Dataset ID
- Date range
- Format (JSON/XML)

**Temporary Solution:**
Mark this integration as "partial" or "research needed" in the UI, or disable it until proper implementation is available.

---

## Summary & Recommendations

### Priority Actions

#### 🔴 **High Priority** (Do First)

1. **Enable Data.gov US** - Free, no key, 300k+ datasets
   ```bash
   ENABLE_DATAGOV_US_INTEGRATION=True
   ```

2. **Get FRED API Key** - Free, instant, mortgage rates
   - Register: https://fred.stlouisfed.org/docs/api/api_key.html
   - Enable integration

3. **Get BLS API Key** - Free, instant, increases limits
   - Register: https://data.bls.gov/registrationEngine/
   - Increases daily limit from 25 to 500

4. **Increase Frontend Timeout** - Prevent premature aborts
   ```typescript
   const timeoutId = setTimeout(() => controller.abort(), 30000);
   ```

5. **Fix HUD Integration** - Implement Bearer token auth
   - Get API key: https://www.huduser.gov/hudapi/public/register
   - Update code to use Bearer token
   - Test actual API endpoints

#### 🟡 **Medium Priority** (Do Later)

6. **Implement FHFA Data Import** - Scheduled CSV downloads
   - Create database schema
   - Build import script
   - Schedule monthly/quarterly updates

7. **Research Bank of Israel API** - Document actual endpoints
   - Find English documentation
   - Test API endpoints
   - Implement proper data fetching

8. **Add Request Caching** - Reduce API calls
   - Cache BLS data for 24 hours
   - Cache Data.gov searches for 1 hour
   - Cache FRED data for 6 hours

#### 🟢 **Low Priority** (Nice to Have)

9. **Add Census API Key** - Optional, increases limits
   - Register: https://api.census.gov/data/key_signup.html

10. **Implement Rate Limiting** - Protect against hitting limits
    - Track API call counts
    - Queue requests during peak times
    - Show remaining quota in UI

### Expected Results After Fixes

| Integration | Before | After |
|------------|--------|-------|
| Data.gov US | ❌ Disabled | ✅ Working with 300k+ datasets |
| BLS | ⚠️ 25 queries/day | ✅ 500 queries/day |
| FRED | ❌ Disabled | ✅ Working with mortgage data |
| HUD | ❌ Fails (no auth) | ✅ Working with FMR data |
| FHFA | ⚠️ Placeholder | ⚠️ Needs CSV import (documented) |
| Bank of Israel | ⚠️ Placeholder | ⚠️ Needs research (documented) |

### Success Metrics

After implementing these fixes, you should see:
- ✅ **5-6 active integrations** (up from 4)
- ✅ **Zero timeout errors** (with 30s timeout)
- ✅ **Actual data retrieval** from HUD
- ✅ **Higher BLS rate limits** (500/day vs 25/day)
- ✅ **FRED mortgage rates** available
- ✅ **Clear documentation** for placeholder integrations

---

## Quick Start Checklist

Use this checklist to get all integrations working:

### ✅ Immediate (No API Keys Needed)
- [ ] Set `ENABLE_DATAGOV_US_INTEGRATION=True`
- [ ] Set `ENABLE_DATAGOV_IL_INTEGRATION=True`
- [ ] Increase frontend timeout to 30 seconds
- [ ] Restart backend and frontend
- [ ] Test Data.gov integration

### ✅ Day 1 (5 minutes each)
- [ ] Register for BLS API key
- [ ] Add BLS key to `.env`
- [ ] Register for FRED API key
- [ ] Add FRED key to `.env`
- [ ] Set `ENABLE_FRED_INTEGRATION=True`
- [ ] Test both integrations

### ✅ Day 2 (30 minutes)
- [ ] Register for HUD User API
- [ ] Verify email and get token
- [ ] Add `HUD_API_KEY` to settings.py
- [ ] Add token to `.env`
- [ ] Update HUD integration code (see Issue 3 fix)
- [ ] Test HUD integration

### ✅ Week 1 (2-3 hours)
- [ ] Create FHFA database schema
- [ ] Build CSV import script
- [ ] Download and import initial data
- [ ] Update FHFA integration to use database
- [ ] Schedule monthly updates
- [ ] Test FHFA data retrieval

### ✅ Week 2 (Research)
- [ ] Research Bank of Israel API endpoints
- [ ] Document API structure
- [ ] Implement data fetching
- [ ] Test with actual data
- [ ] Update documentation

---

## Support & Resources

### Official Documentation Links

- **Data.gov:** https://data.gov/developers/apis/
- **HUD User API:** https://www.huduser.gov/portal/dataset/fmr-api.html
- **HUD Registration:** https://www.huduser.gov/hudapi/public/register
- **FHFA Data Downloads:** https://www.fhfa.gov/data/hpi/datasets
- **BLS API:** https://www.bls.gov/developers/
- **BLS Registration:** https://data.bls.gov/registrationEngine/
- **FRED API:** https://fred.stlouisfed.org/docs/api/
- **FRED API Key:** https://fred.stlouisfed.org/docs/api/api_key.html
- **Census API:** https://api.census.gov/data/key_signup.html

### Code References

- Integration base class: `backend/app/integrations/base.py`
- Integration manager: `backend/app/integrations/manager.py`
- Settings: `backend/app/settings.py` (lines 150-190)
- Frontend page: `frontend/src/pages/IntegrationsPage.tsx`
- API endpoints: `backend/app/api/v1/endpoints/integrations.py`

### Testing Tools

```bash
# Quick test script
curl http://localhost:8000/api/v1/integrations/status | jq '.active_count'

# Detailed test
curl http://localhost:8000/api/v1/integrations/test/[integration_name] | jq

# Frontend in browser
http://localhost:3000/integrations
```

---

## Conclusion

This guide identified **6 critical configuration issues** and provided **step-by-step solutions** for each. The main problems are:

1. **HUD Integration** - Missing Bearer token authentication (fix required)
2. **Data.gov** - Unnecessarily disabled (enable immediately)
3. **FHFA** - Needs CSV import implementation (documented approach)
4. **Frontend Timeout** - Too short at 10 seconds (increase to 30s)
5. **Missing API Keys** - BLS, FRED could increase functionality (free registration)
6. **Bank of Israel** - Needs API research (documented as placeholder)

With these fixes, you'll have **5-6 fully functional integrations** providing real-time data from government sources, with proper timeout handling and comprehensive error recovery.

**Estimated Time to Full Functionality:**
- 🟢 **Quick wins (30 min):** Enable Data.gov, increase timeouts
- 🟡 **Day 1 (1 hour):** Get BLS and FRED API keys
- 🔴 **Day 2 (2-3 hours):** Fix HUD integration
- 🟣 **Week 1 (half day):** Implement FHFA CSV import
- 🔵 **Week 2 (research):** Bank of Israel API documentation

---

**Generated:** 2025-11-11
**Author:** Claude Code Integration Analysis
**Version:** 1.0
