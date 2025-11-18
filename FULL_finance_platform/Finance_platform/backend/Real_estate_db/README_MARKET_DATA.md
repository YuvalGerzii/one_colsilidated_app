# Real Estate Market Data Import Package
## NYC & Miami Market Intelligence for Portfolio Dashboard

---

## 📦 Package Contents

This package provides **structured real estate market data** for NYC and Miami, ready for PostgreSQL import:

### 1. **Database Schema** (`real_estate_market_data_schema.sql`)
- 3 core tables for real estate market intelligence
- Indexes for query performance
- Views for common analysis patterns
- Helper functions for market analysis

### 2. **Market Data CSV Files**
- `market_data.csv` (119 records) - Cap rates, rents, operating metrics
- `comp_transactions.csv` (38 records) - Major property transactions
- `economic_indicators.csv` (95 records) - Population, employment, economic data

### 3. **Import Script** (`import_market_data.py`)
- Automated Python script for database import
- Handles data validation and error checking
- Provides import verification

### 4. **This Documentation** (`README_MARKET_DATA.md`)

---

## 🎯 What This Data Provides

### **Market Data Table** (119 records)
**NYC Markets:**
- Cap rates by borough (Manhattan, Brooklyn, Queens, Bronx) and class (A, B, C)
- Rental rates (Studio, 1BR, 2BR, 3BR) by submarket
- Vacancy rates by borough
- Operating expenses as % of EGI
- Property taxes, insurance, management fees
- Construction costs by building type
- Office metrics (Midtown, Downtown, Hudson Yards)
- Supply pipeline (units under construction, deliveries)

**Miami Markets:**
- Cap rates by submarket (Brickell, Miami Beach, Coral Gables, Fort Lauderdale, West Palm)
- Rental rates and vacancy by county
- Operating expenses including hurricane insurance premiums
- Transaction volumes and pricing
- Construction pipeline and absorption

**Time Coverage:** Q1 2023 - Q4 2024

### **Comp Transactions Table** (38 records)
**Major Deals:**
- NYC: $425M (1 West End Ave), $395M (555 Tenth Ave), $383M (303 East 33rd St)
- Miami: $190M (The Hamilton), $139M (The Point at Lakeside), $134M (Palmera)
- Office transactions including 245 Park Ave ($1.2B), 1111 Brickell ($311M)
- Development sites: 98 Flatbush Ave, 739 Ocean Dr, Gateway at Wynwood
- Distressed deals: Foreclosures and bankruptcy sales
- Portfolio transactions: Multi-property deals

**Transaction Types:** Arms length sales, development sites, distressed assets, portfolios

### **Economic Indicators Table** (95 records)
**NYC Metro:**
- Population: 8.48M (+87K YoY)
- Employment: 4.8M (all-time high)
- Job growth by sector (tech +23.7K, financial services +10.5K)
- Median household income: $82,700
- Construction costs and labor rates
- Financing rates (Fannie Mae, Freddie Mac, CMBS)

**Miami Metro:**
- Population: 6.34M (+6.5% 5-year growth)
- Strong in-migration (+61K net domestic)
- Employment: 3.18M (3.2% job growth)
- Median household income: $67,300
- Hurricane insurance costs (up 253% over 10 years)
- Construction costs and material pricing

**Macro Indicators:**
- SOFR: 5.32%
- 10-Year Treasury: 4.36%
- Agency lending rates: 5.17-5.86%

---

## 🚀 Quick Start (10 Minutes)

### Step 1: Apply Database Schema

```bash
# Connect to your Portfolio Dashboard database
psql -U postgres -d portfolio_dashboard

# Apply the real estate market data schema
\i real_estate_market_data_schema.sql

# Verify tables created
\dt
```

You should see:
- `market_data`
- `comp_transactions`
- `economic_indicators`

### Step 2: Install Python Dependencies

```bash
pip install psycopg2-binary pandas --break-system-packages
```

### Step 3: Run Import Script

```bash
# Basic usage
python import_market_data.py --db-name portfolio_dashboard --user postgres

# With password
python import_market_data.py --db-name portfolio_dashboard --user postgres --password yourpassword

# Custom host
python import_market_data.py --db-name portfolio_dashboard --user postgres --host myserver.com
```

The script will:
- ✅ Connect to your database
- ✅ Import all 3 CSV files
- ✅ Handle duplicates gracefully
- ✅ Verify record counts
- ✅ Provide sample queries

### Step 4: Verify Import

```sql
-- Check record counts
SELECT 
    'market_data' as table_name, COUNT(*) as records FROM market_data
UNION ALL
SELECT 
    'comp_transactions', COUNT(*) FROM comp_transactions
UNION ALL
SELECT 
    'economic_indicators', COUNT(*) FROM economic_indicators;
```

Expected output:
- market_data: 119 records
- comp_transactions: 38 records
- economic_indicators: 95 records

---

## 📊 Sample Queries

### 1. Latest Cap Rates by Market

```sql
SELECT * FROM v_latest_cap_rates 
WHERE market_name = 'NYC' 
  AND property_type = 'multifamily'
ORDER BY submarket_name, property_class;
```

### 2. Recent Manhattan Transactions

```sql
SELECT 
    address,
    sale_date,
    sale_price,
    price_per_unit,
    cap_rate,
    units,
    buyer
FROM v_recent_comp_transactions
WHERE city = 'Manhattan'
  AND property_type = 'multifamily'
ORDER BY sale_date DESC
LIMIT 10;
```

### 3. Miami Economic Indicators

```sql
SELECT 
    indicator_name,
    indicator_value,
    indicator_unit,
    as_of_date
FROM v_latest_economic_indicators
WHERE geography = 'Miami Metro'
  AND indicator_name IN ('population', 'employment', 'median_household_income')
ORDER BY indicator_name;
```

### 4. Compare NYC vs Miami Cap Rates

```sql
SELECT 
    market_name,
    property_type,
    property_class,
    AVG(metric_value) as avg_cap_rate,
    COUNT(*) as data_points
FROM market_data
WHERE metric_name = 'cap_rate'
  AND property_type = 'multifamily'
  AND period >= '2024-01-01'
GROUP BY market_name, property_type, property_class
ORDER BY market_name, property_class;
```

### 5. Rent Growth Analysis

```sql
WITH rent_data AS (
    SELECT 
        market_name,
        submarket_name,
        metric_value as rent,
        period,
        ROW_NUMBER() OVER (
            PARTITION BY market_name, submarket_name 
            ORDER BY period DESC
        ) as rn
    FROM market_data
    WHERE metric_name LIKE 'rent_per_month%'
      AND property_class = 'A'
)
SELECT 
    market_name,
    submarket_name,
    rent as current_rent,
    period as as_of_date
FROM rent_data
WHERE rn = 1
ORDER BY market_name, submarket_name;
```

### 6. Construction Cost Comparison

```sql
SELECT 
    market_name,
    metric_name,
    metric_value as cost_psf,
    data_source
FROM market_data
WHERE metric_name LIKE '%construction_cost_psf%'
  AND property_type = 'multifamily'
ORDER BY market_name, 
         CASE 
             WHEN metric_name LIKE '%_low' THEN 1
             WHEN metric_name LIKE '%_mid' THEN 2
             WHEN metric_name LIKE '%_high' THEN 3
             WHEN metric_name LIKE '%_luxury' THEN 4
         END;
```

### 7. Transaction Heat Map (Last 6 Months)

```sql
SELECT 
    city,
    property_type,
    COUNT(*) as transaction_count,
    AVG(sale_price) as avg_sale_price,
    AVG(price_per_sf) as avg_price_psf,
    AVG(cap_rate) as avg_cap_rate
FROM comp_transactions
WHERE sale_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY city, property_type
ORDER BY city, property_type;
```

### 8. Financing Rates Comparison

```sql
SELECT 
    indicator_name,
    indicator_value as rate,
    period
FROM economic_indicators
WHERE geography = 'NYC Metro'
  AND indicator_name LIKE '%_rate%'
  AND indicator_name IN (
      'fannie_mae_rate_10yr',
      'freddie_mac_rate_10yr',
      'cmbs_rate_10yr',
      'sofr_rate'
  )
ORDER BY indicator_name;
```

---

## 🔗 Integration with Portfolio Dashboard

### Use Case 1: Real Estate Portfolio Company Benchmarking

```sql
-- Compare your multifamily portfolio company to market
SELECT 
    pc.company_name,
    pc.headquarters_city as location,
    -- Your company metrics
    fm.revenue,
    fm.ebitda,
    fm.ebitda_margin,
    -- Market cap rates
    md.metric_value as market_cap_rate,
    md.submarket_name
FROM portfolio_companies pc
JOIN financial_metrics fm ON pc.company_id = fm.company_id
LEFT JOIN market_data md ON 
    (CASE 
        WHEN pc.headquarters_city LIKE '%New York%' THEN 'NYC'
        WHEN pc.headquarters_city LIKE '%Miami%' THEN 'Miami'
    END) = md.market_name
    AND md.property_type = 'multifamily'
    AND md.metric_name = 'cap_rate'
    AND md.property_class = 'A'
WHERE pc.sector = 'Real Estate'
  AND fm.period_type = 'quarterly'
  AND fm.period_end_date = (
      SELECT MAX(period_end_date) 
      FROM financial_metrics 
      WHERE company_id = pc.company_id
  );
```

### Use Case 2: Market Entry Analysis

```sql
-- Analyze market opportunity for new investment
WITH market_summary AS (
    SELECT 
        market_name,
        AVG(CASE WHEN metric_name = 'cap_rate' THEN metric_value END) as avg_cap_rate,
        AVG(CASE WHEN metric_name = 'rent_growth_yoy' THEN metric_value END) as rent_growth,
        AVG(CASE WHEN metric_name = 'vacancy_rate' THEN metric_value END) as vacancy_rate
    FROM market_data
    WHERE property_type = 'multifamily'
      AND period >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY market_name
),
econ_summary AS (
    SELECT 
        CASE 
            WHEN geography = 'NYC Metro' THEN 'NYC'
            WHEN geography = 'Miami Metro' THEN 'Miami'
        END as market_name,
        MAX(CASE WHEN indicator_name = 'population' THEN indicator_value END) as population,
        MAX(CASE WHEN indicator_name = 'employment' THEN indicator_value END) as employment,
        MAX(CASE WHEN indicator_name = 'median_household_income' THEN indicator_value END) as median_income
    FROM economic_indicators
    WHERE geography IN ('NYC Metro', 'Miami Metro')
    GROUP BY 
        CASE 
            WHEN geography = 'NYC Metro' THEN 'NYC'
            WHEN geography = 'Miami Metro' THEN 'Miami'
        END
)
SELECT 
    ms.market_name,
    ms.avg_cap_rate,
    ms.rent_growth,
    ms.vacancy_rate,
    es.population,
    es.employment,
    es.median_income
FROM market_summary ms
JOIN econ_summary es ON ms.market_name = es.market_name
ORDER BY ms.avg_cap_rate DESC;
```

### Use Case 3: Valuation Validation

```sql
-- Validate portfolio company valuation against comp transactions
CREATE OR REPLACE VIEW v_valuation_benchmarks AS
SELECT 
    pc.company_name,
    v.equity_value,
    v.valuation_date,
    -- Comparable transactions
    AVG(ct.price_per_unit) as market_avg_price_per_unit,
    AVG(ct.cap_rate) as market_avg_cap_rate,
    COUNT(ct.transaction_id) as comp_count
FROM portfolio_companies pc
JOIN valuations v ON pc.company_id = v.company_id
LEFT JOIN comp_transactions ct ON 
    ct.city = pc.headquarters_city
    AND ct.property_type = 'multifamily'
    AND ct.sale_date >= v.valuation_date - INTERVAL '12 months'
    AND ct.sale_date <= v.valuation_date
WHERE pc.sector = 'Real Estate'
  AND v.valuation_date = (
      SELECT MAX(valuation_date) 
      FROM valuations 
      WHERE company_id = pc.company_id
  )
GROUP BY pc.company_name, v.equity_value, v.valuation_date;
```

---

## 📈 Dashboard Ideas

### 1. Market Overview Dashboard
- Cap rate trends by market and class
- Rent growth heatmap
- Transaction volume trends
- Supply pipeline by submarket

### 2. Economic Indicators Dashboard
- Population and employment trends
- Income growth comparison
- Construction cost trends
- Financing rates timeline

### 3. Competitive Intelligence Dashboard
- Recent transactions by submarket
- Price per unit trends
- Development site activity
- Distressed deal opportunities

### 4. Portfolio Performance Dashboard
- Your companies vs market benchmarks
- Valuation multiples vs comps
- Operating metrics comparison
- Market positioning analysis

---

## 🔄 Data Update Strategy

### Quarterly Updates Recommended

**Data Sources to Monitor:**
- **Cap Rates**: CoStar, Real Capital Analytics, local brokerages
- **Rental Rates**: Zillow, Apartments.com, RentCafe, local MLS
- **Transactions**: CoStar, REIS, public records, brokerage reports
- **Economic Data**: U.S. Census, BLS, local planning departments
- **Construction Costs**: RSMeans, local estimators

**Update Process:**
1. Collect latest data from sources
2. Structure into CSV format (use existing files as templates)
3. Run import script with new data
4. Review data quality and outliers
5. Update dashboards and reports

**Automation Options:**
- Web scraping scripts for public data sources
- API integrations (CoStar, REIS, Census Bureau)
- PDF extraction for brokerage reports
- Scheduled quarterly runs

---

## 🛠️ Advanced Usage

### Custom Queries

```sql
-- Create custom metric view
CREATE VIEW v_market_health_score AS
SELECT 
    market_name,
    submarket_name,
    property_type,
    -- Calculate health score (0-100)
    (
        COALESCE(100 - (vacancy_rate * 10), 50) * 0.3 +
        COALESCE(rent_growth * 10, 50) * 0.3 +
        COALESCE(100 - ((cap_rate - 4) * 10), 50) * 0.4
    ) as health_score
FROM (
    SELECT 
        market_name,
        submarket_name,
        property_type,
        AVG(CASE WHEN metric_name = 'vacancy_rate' THEN metric_value END) as vacancy_rate,
        AVG(CASE WHEN metric_name = 'rent_growth_yoy' THEN metric_value END) as rent_growth,
        AVG(CASE WHEN metric_name = 'cap_rate' THEN metric_value END) as cap_rate
    FROM market_data
    WHERE period >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY market_name, submarket_name, property_type
) as metrics;
```

### Export for Analysis

```sql
-- Export NYC multifamily data for Excel analysis
COPY (
    SELECT * FROM market_data 
    WHERE market_name = 'NYC' 
      AND property_type = 'multifamily'
    ORDER BY period DESC
) TO '/tmp/nyc_multifamily_export.csv' 
CSV HEADER;
```

---

## 📚 Data Sources

All data extracted from the comprehensive **67-page NYC & Miami Real Estate Market Analysis (2024-2025)**

**Primary Sources Include:**
- Ariel Property Advisors (NYC transactions)
- Alpha Realty (NYC quarterly reports)
- Corcoran (NYC rental market)
- NYC Rent Guidelines Board (vacancy survey)
- Lee Associates (South Florida markets)
- Miami Realtors Association (Miami data)
- RentCafe (Miami rentals)
- Partnership for NYC (employment data)
- U.S. Census Bureau (demographics)
- Federal Reserve (interest rates)
- Fannie Mae / Freddie Mac (lending rates)
- Construction cost estimators (both markets)
- Multiple institutional brokerage reports

**Data Quality:**
- High confidence: Direct from primary sources
- Medium confidence: Aggregated from multiple sources
- Low confidence: Estimates based on market trends

---

## 🐛 Troubleshooting

### Error: "psycopg2 module not found"
```bash
pip install psycopg2-binary --break-system-packages
```

### Error: "permission denied for table"
```sql
-- Grant permissions to your user
GRANT SELECT, INSERT, UPDATE ON market_data TO your_username;
GRANT SELECT, INSERT, UPDATE ON comp_transactions TO your_username;
GRANT SELECT, INSERT, UPDATE ON economic_indicators TO your_username;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO your_username;
```

### Error: "duplicate key value violates unique constraint"
- This is normal for duplicate records
- Script uses ON CONFLICT DO NOTHING to skip duplicates
- Check skipped count in import summary

### Data Looks Wrong
```sql
-- Verify sample data
SELECT * FROM market_data LIMIT 10;
SELECT * FROM comp_transactions LIMIT 5;
SELECT * FROM economic_indicators LIMIT 10;

-- Check for nulls
SELECT 
    COUNT(*) as total_records,
    COUNT(metric_value) as non_null_values,
    COUNT(*) - COUNT(metric_value) as null_values
FROM market_data;
```

---

## 📞 Next Steps

1. **Apply Schema**: Run `real_estate_market_data_schema.sql`
2. **Import Data**: Run `python import_market_data.py`
3. **Verify Import**: Run sample queries
4. **Build Dashboards**: Create visualizations
5. **Integrate Models**: Connect to your DCF/LBO models
6. **Schedule Updates**: Plan quarterly data refreshes
7. **Train Team**: Share query examples with analysts

---

## 🎯 Business Value

This market data enables:

**Investment Decisions:**
- Market entry/exit analysis
- Submarket selection
- Risk assessment
- Pricing strategies

**Valuation:**
- Comparable selection
- Cap rate benchmarking
- Market multiple validation
- Fair value estimation

**Portfolio Management:**
- Performance benchmarking
- Market positioning
- Competitive analysis
- Value creation opportunities

**LP Reporting:**
- Market context for returns
- External validation
- Industry trends
- Investment thesis support

**Due Diligence:**
- Market underwriting
- Rent comp analysis
- Operating expense validation
- Exit strategy planning

---

## 📄 Files Summary

| File | Records | Description |
|------|---------|-------------|
| `real_estate_market_data_schema.sql` | - | Database schema with 3 tables, views, functions |
| `market_data.csv` | 119 | Cap rates, rents, operating metrics, supply data |
| `comp_transactions.csv` | 38 | Major property sales in NYC and Miami |
| `economic_indicators.csv` | 95 | Population, employment, income, macro data |
| `import_market_data.py` | - | Automated import script with validation |
| `README_MARKET_DATA.md` | - | This comprehensive documentation |

**Total Dataset:** 252 data records covering NYC and Miami real estate markets (2023-2024)

---

## ✅ Import Checklist

- [ ] Database connection tested
- [ ] Schema file applied successfully
- [ ] market_data.csv imported (119 records)
- [ ] comp_transactions.csv imported (38 records)
- [ ] economic_indicators.csv imported (95 records)
- [ ] Sample queries return expected results
- [ ] Views are accessible (v_latest_cap_rates, etc.)
- [ ] Data integrated with portfolio companies
- [ ] Dashboards created
- [ ] Team trained on queries
- [ ] Update schedule established

---

**Ready to transform your market intelligence!** 🚀
