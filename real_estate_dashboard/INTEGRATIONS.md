# Third-Party Integrations

This document describes the third-party integrations available in the Real Estate Dashboard.

## Overview

The dashboard supports integrations with various external services to enhance functionality:

- **Market Data**: Economic indicators, demographics, housing data
- **Property Data**: Property listings, valuations, comps
- **Banking & Payments**: Bank account linking, payment processing
- **Tools & Automation**: Notifications, file storage, workflows

## Quick Start

### 1. Configure API Keys

Copy the integration environment template:

```bash
cd backend
cp .env.integrations.example .env.integrations
```

Edit `.env.integrations` and add your API keys. Then source it in your main `.env`:

```bash
# In backend/.env
source .env.integrations  # Or manually copy the variables
```

### 2. Enable Integrations

Set feature flags in `.env`:

```bash
ENABLE_INTEGRATIONS=True
ENABLE_CENSUS_INTEGRATION=True
ENABLE_BLS_INTEGRATION=True
ENABLE_FRED_INTEGRATION=True
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Start the Server

```bash
uvicorn app.main:app --reload
```

### 5. Test Integrations

Visit the Integrations page in the UI or use the API:

```bash
curl http://localhost:8000/api/v1/integrations/status
curl http://localhost:8000/api/v1/integrations/test/census
```

## Available Integrations

### 🆓 Free Integrations

#### Census Bureau (No API key required)
- **Cost**: Free
- **API Key**: Optional (increases rate limits)
- **Get Key**: https://api.census.gov/data/key_signup.html
- **Features**:
  - Population demographics
  - Housing statistics
  - Income data
  - Property characteristics by ZIP code

**Example Usage**:
```bash
curl "http://localhost:8000/api/v1/integrations/market-data/census/demographics?zip_code=10001"
```

#### Bureau of Labor Statistics (No API key required)
- **Cost**: Free
- **API Key**: Optional (500 queries/day vs 25 without)
- **Get Key**: https://data.bls.gov/registrationEngine/
- **Features**:
  - Unemployment rates
  - Employment statistics
  - Consumer Price Index (CPI)
  - Wage data

**Example Usage**:
```bash
curl "http://localhost:8000/api/v1/integrations/market-data/bls/unemployment"
curl "http://localhost:8000/api/v1/integrations/market-data/bls/employment"
```

#### FRED - Federal Reserve Economic Data (Free API key required)
- **Cost**: Free
- **API Key**: Required
- **Get Key**: https://fred.stlouisfed.org/docs/api/api_key.html
- **Features**:
  - Mortgage rates (30-year, 15-year)
  - Interest rates
  - Housing market indicators
  - GDP and economic metrics

**Example Usage**:
```bash
curl "http://localhost:8000/api/v1/integrations/market-data/fred/mortgage-rates?rate_type=30Y"
curl "http://localhost:8000/api/v1/integrations/market-data/fred/housing-indicators"
```

#### Slack (Free)
- **Cost**: Free
- **API Key**: Bot token (free to create)
- **Get Token**: https://api.slack.com/apps
- **Features**:
  - Send notifications to channels
  - Deal updates
  - Financial report alerts
  - Portfolio change notifications

**Example Usage**:
```bash
curl -X POST "http://localhost:8000/api/v1/integrations/notifications/slack/send" \
  -H "Content-Type: application/json" \
  -d '{"channel": "#deals", "message": "New property acquired!"}'
```

#### Google Drive (Free 15GB)
- **Cost**: Free (15GB storage)
- **API Key**: OAuth2 access token
- **Setup**: https://console.cloud.google.com/
- **Features**:
  - Document storage
  - File sharing
  - Folder organization
  - Version history

#### Plaid (Free sandbox)
- **Cost**: Free sandbox, paid for production
- **API Key**: Client ID + Secret
- **Get Credentials**: https://dashboard.plaid.com/
- **Features**:
  - Bank account linking
  - Balance checking
  - Transaction history
  - Identity verification

#### Stripe (Free test mode)
- **Cost**: Free test mode
- **API Key**: Test API key (sk_test_...)
- **Get Key**: https://dashboard.stripe.com/apikeys
- **Features**:
  - Payment processing
  - Subscription management
  - Invoice generation
  - Customer management

### 💰 Paid/Limited Integrations

#### ATTOM Data Solutions
- **Cost**: Free trial, then $49+/month
- **API Key**: Required
- **Get Key**: https://api.developer.attomdata.com/
- **Features**:
  - Property details
  - Automated valuations (AVM)
  - Sales comps
  - Tax assessor data

#### Realtor.com (via RapidAPI)
- **Cost**: 500 requests/month free
- **API Key**: RapidAPI key
- **Get Key**: https://rapidapi.com/apidojo/api/realtor/
- **Features**:
  - Property listings
  - Sold properties
  - Market trends
  - Property details

## Integration Categories

### Market Data
Get economic indicators and market trends to inform investment decisions.

**Endpoints**:
- `GET /api/v1/integrations/market-data/census/demographics`
- `GET /api/v1/integrations/market-data/bls/unemployment`
- `GET /api/v1/integrations/market-data/bls/employment`
- `GET /api/v1/integrations/market-data/fred/mortgage-rates`
- `GET /api/v1/integrations/market-data/fred/housing-indicators`
- `GET /api/v1/integrations/market-data/fred/interest-rates`

### Property Data
Access property listings, valuations, and comparable sales.

**Endpoints**:
- `GET /api/v1/integrations/property-data/attom/details`
- `GET /api/v1/integrations/property-data/realtor/search`

### Notifications
Send alerts and updates to team communication channels.

**Endpoints**:
- `POST /api/v1/integrations/notifications/slack/send`
- `POST /api/v1/integrations/notifications/slack/deal`

### Management Endpoints
Monitor and test integration status.

**Endpoints**:
- `GET /api/v1/integrations/status` - View all integrations
- `GET /api/v1/integrations/test/{integration_key}` - Test specific integration
- `GET /api/v1/integrations/test-all` - Test all integrations
- `GET /api/v1/integrations/metadata/{integration_key}` - Get integration details

## Architecture

### Backend Structure

```
backend/app/integrations/
├── __init__.py
├── base.py              # Base integration classes
├── manager.py           # Integration manager
├── loader.py            # Integration initialization
├── market_data/
│   ├── census.py
│   ├── bls.py
│   └── fred.py
├── property_data/
│   ├── attom.py
│   └── realtor.py
├── banking/
│   ├── plaid.py
│   └── stripe.py
└── tools/
    ├── slack.py
    └── google_drive.py
```

### Key Concepts

#### Base Integration Class
All integrations inherit from `BaseIntegration` which provides:
- Configuration validation
- Error handling
- Status management
- Graceful degradation when API keys are missing

#### Integration Manager
Central registry for all integrations:
- Register integrations at startup
- Query by category or status
- Test connections
- Get status summaries

#### Graceful Handling
Integrations without API keys are automatically skipped:
```python
if not integration.is_available:
    # Integration not configured - skip gracefully
    return {"error": "Integration not available"}
```

## Configuration

### Environment Variables

```bash
# Feature Flags
ENABLE_INTEGRATIONS=True
ENABLE_CENSUS_INTEGRATION=True
ENABLE_BLS_INTEGRATION=True
ENABLE_FRED_INTEGRATION=True

# API Keys
CENSUS_API_KEY=your_key_here          # Optional
BLS_API_KEY=your_key_here             # Optional
FRED_API_KEY=your_key_here            # Required for FRED

# Paid Services (optional)
ATTOM_API_KEY=your_key_here
REALTOR_RAPIDAPI_KEY=your_key_here

# Banking
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENVIRONMENT=sandbox

STRIPE_API_KEY=sk_test_...

# Tools
SLACK_BOT_TOKEN=xoxb-...
GOOGLE_DRIVE_ACCESS_TOKEN=ya29....
```

### Feature Flags

Control which integrations are enabled:

```python
ENABLE_CENSUS_INTEGRATION = True   # Enable Census Bureau
ENABLE_FRED_INTEGRATION = False    # Disable FRED
```

## Error Handling

All integrations use consistent error handling:

```json
{
  "success": false,
  "error": "Integration not available. Set FRED_API_KEY in environment.",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

When an integration is not configured, API endpoints return HTTP 503 with a helpful error message.

## Best Practices

### 1. Start with Free Integrations
Begin with Census Bureau, BLS, and FRED (free) before adding paid services.

### 2. Use Sandbox/Test Modes
For Plaid and Stripe, start with sandbox/test modes before production.

### 3. Monitor Rate Limits
- Census: No hard limit, but get API key for better performance
- BLS: 25 queries/day without key, 500 with key
- FRED: Generous limits with free API key

### 4. Cache Data
Market data doesn't change frequently - implement caching:
```python
# Cache mortgage rates for 1 hour
cache_duration = 3600
```

### 5. Handle Errors Gracefully
Always check integration availability before use:
```python
integration = integration_manager.get("fred")
if not integration or not integration.is_available:
    # Use fallback data or skip feature
    pass
```

## Testing

### Test All Integrations
```bash
curl http://localhost:8000/api/v1/integrations/test-all
```

### Test Specific Integration
```bash
curl http://localhost:8000/api/v1/integrations/test/census
curl http://localhost:8000/api/v1/integrations/test/fred
```

### Check Status
```bash
curl http://localhost:8000/api/v1/integrations/status
```

## Troubleshooting

### Integration Shows "not_configured"
- Check that the API key is set in `.env`
- Verify the feature flag is enabled (`ENABLE_*_INTEGRATION=True`)
- Restart the backend server

### Connection Test Fails
- Verify API key is correct
- Check internet connectivity
- Review API documentation for changes
- Check rate limits

### Integration Not Appearing
- Ensure integration is registered in `loader.py`
- Check for initialization errors in server logs
- Verify imports are correct

## Future Integrations

Potential integrations to add:
- ✅ Census Bureau
- ✅ BLS
- ✅ FRED
- ⏳ Zillow API (when/if available)
- ⏳ Redfin API (limited availability)
- ⏳ QuickBooks Online
- ⏳ Xero
- ⏳ AppFolio
- ⏳ DocuSign
- ⏳ Zapier webhooks

## Support

For integration issues:
1. Check the integration's official documentation
2. Review error messages in server logs
3. Verify API key permissions and quotas
4. Test with the integration's official tools/playground

## License

Each third-party integration is subject to its own terms of service and licensing. Review each service's documentation before use.
