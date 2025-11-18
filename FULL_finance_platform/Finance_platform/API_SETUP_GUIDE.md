# Market Data Integration - API Setup Guide

This guide will help you set up API credentials for the Market Data Integration feature.

## Overview

The Market Data Integration feature pulls data from four external sources:

1. **CoStar API** - Commercial real estate data (cap rates, market trends)
2. **Zillow/Redfin API** - Residential property valuations and comparables
3. **Census API** - Demographics and population data (FREE!)
4. **Walk Score API** - Walkability and neighborhood amenities

## Quick Start

### 1. Copy Environment Template

```bash
cd backend
cp .env.example .env
```

### 2. Edit .env File

Open `backend/.env` and add your API keys (instructions below).

## API Key Setup Instructions

### CoStar API 🏢

**What it provides:** Cap rates, rent comparables, market trends, vacancy rates

**Pricing:** Enterprise pricing (contact sales)

**Setup:**
1. Visit: https://www.costar.com/about/costar-real-estate-manager/api
2. Contact CoStar sales team
3. Request API access for your organization
4. Once approved, you'll receive your API key
5. Add to `.env`:
   ```
   COSTAR_API_KEY=your-costar-api-key-here
   ```

**Note:** CoStar is enterprise-focused. For testing, the app uses mock data.

---

### Zillow API 🏠

**What it provides:** Property valuations (Zestimates), rent estimates, comparable properties

**Pricing:** Various tiers available via RapidAPI

**Setup:**
1. Visit: https://rapidapi.com/apimaker/api/zillow-com1
2. Sign up for RapidAPI (free account)
3. Subscribe to Zillow API (has free tier)
4. Copy your RapidAPI key
5. Add to `.env`:
   ```
   ZILLOW_API_KEY=your-rapidapi-key-here
   ```

**Pricing Tiers:**
- **Free:** 100 requests/month
- **Basic:** $9.99/month - 1,000 requests
- **Pro:** $49.99/month - 10,000 requests

---

### U.S. Census API 👥

**What it provides:** Demographics, population, income, employment data

**Pricing:** 100% FREE! 🎉

**Setup:**
1. Visit: https://api.census.gov/data/key_signup.html
2. Fill out the simple signup form
3. You'll receive your API key via email instantly
4. Add to `.env`:
   ```
   CENSUS_API_KEY=your-census-api-key-here
   ```

**Note:** While an API key is recommended, many Census endpoints work without authentication for basic queries.

**Documentation:** https://www.census.gov/data/developers/data-sets.html

---

### Walk Score API 🚶

**What it provides:** Walk Score, Transit Score, Bike Score, nearby amenities

**Pricing:** Starting at $50/month (1,000 calls)

**Setup:**
1. Visit: https://www.walkscore.com/professional/walk-score-apis.php
2. Click "Get Started"
3. Fill out the application form
4. Choose your pricing tier
5. Once approved, you'll receive your API key
6. Add to `.env`:
   ```
   WALKSCORE_API_KEY=your-walkscore-api-key-here
   ```

**Pricing Tiers:**
- **Startup:** $50/month - 1,000 calls
- **Growth:** $150/month - 5,000 calls
- **Enterprise:** Custom pricing

---

## Testing Without API Keys

The app includes **mock data generators** for all services, so you can test the feature immediately without any API keys!

To use mock data:
- Simply leave the API keys empty in `.env`
- The services will automatically fall back to realistic mock data

## Recommended Setup for Getting Started

1. **Start with Census API** (it's free!)
   - Sign up at: https://api.census.gov/data/key_signup.html
   - Add the key to `.env`
   - You'll get real demographic data immediately

2. **Add Walk Score** (if budget allows)
   - Provides excellent neighborhood data
   - $50/month for basic tier

3. **Add Zillow/Redfin** (free tier available)
   - Sign up for RapidAPI free tier
   - Get 100 free requests/month

4. **CoStar** (enterprise level)
   - Only if you have an enterprise relationship
   - Otherwise, use mock data

## Environment Variables Reference

Add these to `backend/.env`:

```bash
# CoStar API (commercial real estate data)
COSTAR_API_KEY=your-costar-api-key-here

# Zillow API (residential valuations)
ZILLOW_API_KEY=your-zillow-rapidapi-key-here

# U.S. Census API (demographics - FREE!)
CENSUS_API_KEY=your-census-api-key-here

# Walk Score API (walkability scores)
WALKSCORE_API_KEY=your-walkscore-api-key-here
```

## Testing Your Setup

### 1. Start the Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 2. Test the API Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/market-data/comprehensive \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94103",
    "property_type": "Multifamily",
    "latitude": 37.7749,
    "longitude": -122.4194
  }'
```

### 3. Check the Response

You should see JSON data with:
- CoStar market data
- Zillow/Redfin property data
- Census demographics
- Walk Score information

If an API key is missing, the service will use mock data for that source.

## API Rate Limits

Be aware of rate limits for each service:

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| CoStar | N/A | Enterprise |
| Zillow | 100/month | 1,000+/month |
| Census | No limit | No limit |
| Walk Score | N/A | 1,000+/month |

## Security Best Practices

1. **Never commit `.env` to version control**
   ```bash
   # Already in .gitignore
   .env
   ```

2. **Use different keys for dev/staging/production**

3. **Rotate keys regularly** (every 90 days recommended)

4. **Monitor API usage** to detect unusual activity

5. **Use environment-specific configurations**
   - Development: Use mock data or free tiers
   - Production: Use paid tiers with proper keys

## Troubleshooting

### Issue: "No matching distribution found" when installing packages

**Solution:** Make sure you're in the virtual environment
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: API returns errors even with valid key

**Possible causes:**
1. Key not properly set in `.env`
2. API rate limit exceeded
3. Invalid API key format
4. Service outage

**Solution:** Check logs for specific error messages

### Issue: All data shows as "Mock Data"

**Solution:** This is normal if no API keys are configured. Add real API keys to `.env` to get live data.

## Next Steps

Once you have your API keys configured:

1. ✅ Run the database migration to create the `market_data` table
2. ✅ Start the backend server
3. ✅ Test the endpoints with Postman or the demo UI
4. ✅ Integrate into your main dashboard
5. ✅ Monitor API usage and costs

## Support

For API-specific issues:
- **CoStar:** Contact your CoStar account manager
- **Zillow:** RapidAPI support or Zillow developer forum
- **Census:** https://www.census.gov/data/developers/guidance/api-user-guide.html
- **Walk Score:** support@walkscore.com

For integration issues, check the backend logs or API documentation at:
http://localhost:8000/docs
