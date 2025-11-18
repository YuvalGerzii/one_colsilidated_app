# 🚀 MCP Financial Data Integration Guide
## Portfolio Dashboard + Financial Datasets MCP Server

---

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Database Integration](#database-integration)
4. [Use Cases & Examples](#use-cases--examples)
5. [API Integration Patterns](#api-integration-patterns)
6. [Automated Workflows](#automated-workflows)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What This Integration Provides

The Financial Datasets MCP server enhances your Portfolio Dashboard with:

#### 1. **Automated Comparable Company Analysis**
- Pull public company financials directly into DCF models
- Calculate trading multiples automatically
- Update comps quarterly without manual data entry

#### 2. **Market Benchmark Validation**
- Validate portfolio company valuations against public markets
- Generate LP reports with current market context
- Track valuation trends over time

#### 3. **Exit Multiple Tracking**
- Monitor sector-specific exit multiples
- Identify optimal exit timing based on market conditions
- Support M&A negotiations with real-time comps

#### 4. **Real-Time Market Data**
- Current stock prices for public comparables
- Historical price trends for sector analysis
- News monitoring for market events

---

## Installation & Setup

### Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] PostgreSQL database running
- [ ] Claude Desktop installed
- [ ] Financial Datasets API key obtained

### Step 1: Install MCP Server

```bash
# Clone the repository
git clone https://github.com/financial-datasets/mcp-server
cd mcp-server

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv add "mcp[cli]" httpx

# Configure API key
cp .env.example .env
echo "FINANCIAL_DATASETS_API_KEY=your_api_key_here" > .env
```

### Step 2: Configure Claude Desktop

**macOS:**
```bash
# Create config directory
mkdir -p ~/Library/Application\ Support/Claude/

# Find uv path
which uv  # Copy this path

# Edit config
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
# Config location
%APPDATA%\Claude\claude_desktop_config.json
```

**Configuration JSON:**
```json
{
  "mcpServers": {
    "financial-datasets": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

### Step 3: Verify Installation

1. Restart Claude Desktop
2. Look for hammer icon (🔨) in bottom right
3. Test with: "Get Apple's latest income statement"

---

## Database Integration

### Apply Market Data Schema

```bash
# Connect to your PostgreSQL database
psql -U your_username -d portfolio_dashboard

# Apply the market data schema
\i market_data_schema.sql

# Verify tables created
\dt public_comparables
\dt market_financials
\dt valuation_multiples
```

### Populate Initial Comparables

```sql
-- Add your industry-specific comparables
INSERT INTO public_comparables (ticker, company_name, industry, sector) VALUES
('CRM', 'Salesforce', 'Enterprise Software', 'Technology'),
('WDAY', 'Workday', 'Enterprise Software', 'Technology'),
('NOW', 'ServiceNow', 'Enterprise Software', 'Technology'),
('SNOW', 'Snowflake', 'Data Infrastructure', 'Technology');

-- Map to portfolio companies
INSERT INTO company_comparable_mapping (company_id, comparable_id, is_primary, relevance_score)
SELECT 
    c.company_id,
    pc.comparable_id,
    TRUE,
    0.95
FROM companies c
CROSS JOIN public_comparables pc
WHERE c.company_name = 'Acme Corp'  -- Your portfolio company
    AND pc.ticker IN ('CRM', 'WDAY', 'NOW');
```

---

## Use Cases & Examples

### Use Case 1: Automated DCF Comparable Analysis

**Scenario:** You're building a DCF model for a SaaS portfolio company and need current public market comps.

**Workflow:**

1. **Identify Comparables** (one-time setup)
```sql
-- Add SaaS comparables to database
INSERT INTO public_comparables (ticker, company_name, industry, sector) VALUES
('DDOG', 'Datadog', 'Cloud Monitoring', 'Technology'),
('MDB', 'MongoDB', 'Database Software', 'Technology'),
('NET', 'Cloudflare', 'Web Infrastructure', 'Technology');
```

2. **Fetch Data via MCP** (via Claude Desktop)
```
Ask Claude: "Get the latest income statements and balance sheets for DDOG, MDB, and NET"
```

3. **Calculate Multiples** (Python script)
```python
from mcp_market_data_integration import MCPMarketDataIntegrator
import asyncio

async def get_saas_comps():
    integrator = MCPMarketDataIntegrator(api_key="your-key")
    
    # Get data
    tickers = ["DDOG", "MDB", "NET"]
    comp_data = await integrator.get_comparable_companies_data(tickers)
    
    # Calculate multiples
    multiples = integrator.calculate_trading_multiples(comp_data)
    
    # Get industry benchmarks
    benchmarks = integrator.get_industry_benchmarks(multiples)
    
    print(f"Median EV/Revenue: {benchmarks['ev_revenue']['median']}x")
    print(f"Median EV/EBITDA: {benchmarks['ev_ebitda']['median']}x")
    
    return benchmarks

# Run it
asyncio.run(get_saas_comps())
```

4. **Store in Database**
```python
# Store multiples for historical tracking
import psycopg2

conn = psycopg2.connect("dbname=portfolio_dashboard user=postgres")
cur = conn.cursor()

for ticker, data in multiples.items():
    cur.execute("""
        INSERT INTO valuation_multiples 
        (comparable_id, as_of_date, ev_revenue, ev_ebitda, pe_ratio, market_cap, enterprise_value)
        VALUES (
            (SELECT comparable_id FROM public_comparables WHERE ticker = %s),
            CURRENT_DATE,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (comparable_id, as_of_date) 
        DO UPDATE SET 
            ev_revenue = EXCLUDED.ev_revenue,
            ev_ebitda = EXCLUDED.ev_ebitda,
            pe_ratio = EXCLUDED.pe_ratio
    """, (ticker, data['ev_revenue'], data['ev_ebitda'], data['pe_ratio'], 
          data['market_cap'], data['enterprise_value']))

conn.commit()
```

### Use Case 2: Quarterly Valuation Validation

**Scenario:** Validate your portfolio company valuations against current market conditions for board reporting.

**Automated Script:**

```python
# quarterly_valuation_check.py
import asyncio
from datetime import datetime
from mcp_market_data_integration import MCPMarketDataIntegrator
import psycopg2
import json

async def quarterly_valuation_check():
    """
    Run quarterly validation of all portfolio companies
    """
    # Initialize
    integrator = MCPMarketDataIntegrator(api_key="your-key")
    conn = psycopg2.connect("dbname=portfolio_dashboard")
    cur = conn.cursor()
    
    # Get all active portfolio companies
    cur.execute("""
        SELECT 
            c.company_id,
            c.company_name,
            c.industry,
            f.revenue,
            f.ebitda,
            v.enterprise_value,
            ARRAY_AGG(pc.ticker) as comp_tickers
        FROM companies c
        JOIN financial_metrics f ON c.company_id = f.company_id
        JOIN valuations v ON c.company_id = v.company_id
        JOIN company_comparable_mapping ccm ON c.company_id = ccm.company_id
        JOIN public_comparables pc ON ccm.comparable_id = pc.comparable_id
        WHERE c.status = 'Active'
            AND f.period_end_date = (
                SELECT MAX(period_end_date) 
                FROM financial_metrics 
                WHERE company_id = c.company_id
            )
        GROUP BY c.company_id, c.company_name, c.industry, 
                 f.revenue, f.ebitda, v.enterprise_value
    """)
    
    companies = cur.fetchall()
    
    # Validate each company
    results = []
    for company_id, name, industry, revenue, ebitda, ev, tickers in companies:
        print(f"\nValidating {name}...")
        
        # Portfolio metrics
        portfolio_metrics = {
            "revenue": float(revenue),
            "ebitda": float(ebitda),
            "enterprise_value": float(ev)
        }
        
        # Get validation
        validation = await integrator.validate_portfolio_company_valuation(
            portfolio_metrics,
            tickers
        )
        
        # Store validation log
        assessment = validation['valuation_assessment']
        cur.execute("""
            INSERT INTO valuation_validation_log (
                company_id, valuation_date,
                portfolio_revenue, portfolio_ebitda, portfolio_enterprise_value,
                portfolio_ev_revenue, portfolio_ev_ebitda,
                market_ev_revenue_median, market_ev_ebitda_median,
                ev_revenue_vs_market_pct, ev_ebitda_vs_market_pct,
                valuation_flag, assessment_summary
            ) VALUES (%s, CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_id,
            portfolio_metrics['revenue'],
            portfolio_metrics['ebitda'],
            portfolio_metrics['enterprise_value'],
            validation['portfolio_company']['ev_revenue'],
            validation['portfolio_company']['ev_ebitda'],
            validation['market_benchmarks']['ev_revenue']['median'],
            validation['market_benchmarks']['ev_ebitda']['median'],
            assessment.get('ev_revenue_vs_median', {}).get('difference_pct'),
            assessment.get('ev_ebitda_vs_median', {}).get('difference_pct'),
            assessment['overall_assessment'].split('-')[0].strip(),
            assessment['overall_assessment']
        ))
        
        results.append({
            "company": name,
            "industry": industry,
            "assessment": assessment['overall_assessment'],
            "details": validation
        })
    
    conn.commit()
    
    # Generate summary report
    print("\n" + "="*60)
    print("QUARTERLY VALUATION VALIDATION SUMMARY")
    print("="*60)
    for r in results:
        print(f"\n{r['company']} ({r['industry']})")
        print(f"  Assessment: {r['assessment']}")
    
    return results

# Schedule this to run quarterly
if __name__ == "__main__":
    asyncio.run(quarterly_valuation_check())
```

### Use Case 3: Live LP Reporting Dashboard

**Scenario:** Create a live dashboard for LPs showing portfolio valuations vs. market benchmarks.

**FastAPI Endpoint:**

```python
# api_endpoints.py
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import asyncio
from mcp_market_data_integration import MCPMarketDataIntegrator
import psycopg2

app = FastAPI()

@app.get("/api/portfolio-valuation-summary")
async def get_portfolio_valuation_summary(fund_id: int):
    """
    Returns portfolio-wide valuation summary with market context
    """
    conn = psycopg2.connect("dbname=portfolio_dashboard")
    cur = conn.cursor()
    
    # Get fund's portfolio companies with latest metrics
    cur.execute("""
        SELECT 
            c.company_id,
            c.company_name,
            c.industry,
            v.enterprise_value,
            vvl.valuation_flag,
            vvl.ev_revenue_vs_market_pct,
            vvl.ev_ebitda_vs_market_pct
        FROM companies c
        JOIN valuations v ON c.company_id = v.company_id
        LEFT JOIN valuation_validation_log vvl ON c.company_id = vvl.company_id
            AND vvl.validation_date = (
                SELECT MAX(validation_date)
                FROM valuation_validation_log
                WHERE company_id = c.company_id
            )
        WHERE c.fund_id = %s AND c.status = 'Active'
    """, (fund_id,))
    
    companies = cur.fetchall()
    
    # Aggregate statistics
    total_ev = sum(float(row[3]) for row in companies)
    premium_count = sum(1 for row in companies if row[4] == 'Above Market')
    discount_count = sum(1 for row in companies if row[4] == 'Below Market')
    at_market_count = sum(1 for row in companies if row[4] == 'At Market')
    
    return {
        "fund_id": fund_id,
        "as_of_date": "2024-10-31",
        "total_portfolio_value": total_ev,
        "company_count": len(companies),
        "valuation_distribution": {
            "premium": premium_count,
            "at_market": at_market_count,
            "discount": discount_count
        },
        "companies": [
            {
                "name": row[1],
                "industry": row[2],
                "enterprise_value": float(row[3]),
                "valuation_flag": row[4],
                "ev_revenue_vs_market": float(row[5]) if row[5] else None,
                "ev_ebitda_vs_market": float(row[6]) if row[6] else None
            }
            for row in companies
        ]
    }

@app.get("/api/market-benchmarks/{industry}")
async def get_market_benchmarks(industry: str):
    """
    Returns current market benchmarks for an industry
    """
    conn = psycopg2.connect("dbname=portfolio_dashboard")
    cur = conn.cursor()
    
    cur.execute("""
        SELECT * FROM v_latest_industry_benchmarks
        WHERE industry = %s
    """, (industry,))
    
    result = cur.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Industry not found")
    
    return {
        "industry": result[0],
        "as_of_date": str(result[2]),
        "ev_revenue": {
            "median": float(result[3]),
            "mean": float(result[4])
        },
        "ev_ebitda": {
            "median": float(result[5]),
            "mean": float(result[6])
        },
        "pe_ratio": {
            "median": float(result[7]),
            "mean": float(result[8])
        },
        "ebitda_margin": {
            "median": float(result[9])
        },
        "sample_size": result[11]
    }
```

---

## API Integration Patterns

### Pattern 1: Batch Update (Recommended for Daily/Weekly)

```python
# batch_market_data_update.py
import asyncio
from mcp_market_data_integration import MCPMarketDataIntegrator
import psycopg2

async def batch_update_market_data():
    """
    Update all comparables in database with latest market data
    """
    integrator = MCPMarketDataIntegrator(api_key="your-key")
    conn = psycopg2.connect("dbname=portfolio_dashboard")
    cur = conn.cursor()
    
    # Get all active comparables
    cur.execute("SELECT ticker FROM public_comparables WHERE is_active = TRUE")
    tickers = [row[0] for row in cur.fetchall()]
    
    # Batch fetch (max 25 at a time to avoid rate limits)
    batch_size = 25
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        print(f"Fetching batch {i//batch_size + 1}: {batch}")
        
        comp_data = await integrator.get_comparable_companies_data(batch)
        multiples = integrator.calculate_trading_multiples(comp_data)
        
        # Store multiples
        for ticker, data in multiples.items():
            if 'error' in data:
                continue
            
            cur.execute("""
                INSERT INTO valuation_multiples 
                (comparable_id, as_of_date, market_cap, enterprise_value,
                 ev_revenue, ev_ebitda, pe_ratio)
                VALUES (
                    (SELECT comparable_id FROM public_comparables WHERE ticker = %s),
                    CURRENT_DATE, %s, %s, %s, %s, %s
                )
                ON CONFLICT (comparable_id, as_of_date)
                DO UPDATE SET
                    market_cap = EXCLUDED.market_cap,
                    enterprise_value = EXCLUDED.enterprise_value,
                    ev_revenue = EXCLUDED.ev_revenue,
                    ev_ebitda = EXCLUDED.ev_ebitda,
                    pe_ratio = EXCLUDED.pe_ratio
            """, (ticker, data['market_cap'], data['enterprise_value'],
                  data['ev_revenue'], data['ev_ebitda'], data['pe_ratio']))
        
        conn.commit()
        print(f"✓ Batch {i//batch_size + 1} completed")
        
        # Rate limiting (be nice to the API)
        await asyncio.sleep(2)
    
    print("\n✓ All market data updated successfully")

if __name__ == "__main__":
    asyncio.run(batch_update_market_data())
```

### Pattern 2: Real-Time On-Demand

```python
# realtime_market_data.py
from fastapi import FastAPI, BackgroundTasks
from mcp_market_data_integration import MCPMarketDataIntegrator

app = FastAPI()
integrator = MCPMarketDataIntegrator(api_key="your-key")

@app.get("/api/comparable/{ticker}/live")
async def get_live_comparable_data(ticker: str):
    """
    Fetch and return live market data for a comparable
    """
    comp_data = await integrator.get_comparable_companies_data([ticker])
    multiples = integrator.calculate_trading_multiples(comp_data)
    
    return {
        "ticker": ticker,
        "as_of": "live",
        "data": multiples.get(ticker, {"error": "Data not available"})
    }
```

---

## Automated Workflows

### Weekly Update Script (Cron Job)

```bash
# /etc/cron.d/portfolio-dashboard-market-update
0 6 * * 1 /path/to/python /path/to/batch_market_data_update.py >> /var/log/market_update.log 2>&1
```

### Pre-Board Meeting Script

```python
# pre_board_meeting_prep.py
"""
Run 24 hours before board meetings to ensure all data is current
"""
import asyncio

async def prepare_board_materials():
    # 1. Update all market data
    from batch_market_data_update import batch_update_market_data
    await batch_update_market_data()
    
    # 2. Run valuation validation
    from quarterly_valuation_check import quarterly_valuation_check
    results = await quarterly_valuation_check()
    
    # 3. Generate PDF reports
    # (implement your PDF generation logic)
    
    print("✓ Board materials ready")

if __name__ == "__main__":
    asyncio.run(prepare_board_materials())
```

---

## Best Practices

### 1. Rate Limiting
- Max 100 requests per minute to Financial Datasets API
- Implement exponential backoff for errors
- Cache results for 24 hours minimum

### 2. Error Handling
```python
async def safe_api_call(ticker):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await integrator.get_comparable_companies_data([ticker])
        except Exception as e:
            if attempt == max_retries - 1:
                # Log to database
                log_api_error(ticker, str(e))
                return None
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Data Validation
```python
def validate_multiple(value, multiple_type):
    """
    Validate multiples are within reasonable ranges
    """
    ranges = {
        'ev_revenue': (0.1, 50.0),
        'ev_ebitda': (1.0, 100.0),
        'pe_ratio': (1.0, 500.0)
    }
    
    if value is None:
        return False
    
    min_val, max_val = ranges.get(multiple_type, (0, float('inf')))
    return min_val <= value <= max_val
```

---

## Troubleshooting

### Issue: MCP Server Not Showing in Claude Desktop

**Solution:**
1. Verify config file location:
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
2. Check paths are absolute (not relative)
3. Restart Claude Desktop completely
4. Check uv is in PATH: `which uv`

### Issue: API Rate Limits

**Solution:**
- Implement caching layer
- Use batch operations
- Schedule updates during off-hours

### Issue: Stale Data in Database

**Solution:**
```sql
-- Find comparables not updated recently
SELECT ticker, MAX(as_of_date) as last_update
FROM public_comparables c
LEFT JOIN valuation_multiples vm ON c.comparable_id = vm.comparable_id
GROUP BY ticker
HAVING MAX(as_of_date) < CURRENT_DATE - INTERVAL '7 days'
OR MAX(as_of_date) IS NULL;
```

---

## Next Steps

1. ✅ Install MCP server and configure Claude Desktop
2. ✅ Apply database schema
3. ✅ Add your comparables to `public_comparables` table
4. ✅ Run test validation on one portfolio company
5. ✅ Set up automated batch update script
6. ✅ Create LP reporting dashboard endpoint
7. ✅ Schedule quarterly valuation validations

---

## Support Resources

- **Financial Datasets API Docs**: https://docs.financialdatasets.ai/
- **MCP Protocol Docs**: https://modelcontextprotocol.io/
- **Portfolio Dashboard Docs**: See `Portfolio_Dashboard_Implementation_Plan.md`

---

**Questions?** Check the project documentation or reach out to the development team.
