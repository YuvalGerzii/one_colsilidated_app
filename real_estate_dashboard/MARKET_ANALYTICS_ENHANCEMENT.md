# Market Intelligence Analytics Enhancement

## Overview

This document describes the enhanced analytics capabilities added to the market intelligence system for deeper data analysis, trend tracking, correlation discovery, and insight generation.

## New Database Models

### 1. MarketTrend
**Purpose**: Track time-series trends and technical indicators

**Key Fields**:
- Moving Averages (5, 10, 20, 50, 200-day)
- Percentage Changes (1d, 5d, 1m, 3m, 6m, 1y, YTD)
- Volatility measures (daily, weekly, monthly)
- RSI (Relative Strength Index)
- Momentum Score (-100 to +100)
- Trend Direction (bullish, bearish, neutral, choppy)
- Z-Score (standard deviations from mean)
- Percentile Rank (0-100)
- Anomaly Detection (flags unusual movements)

**Use Cases**:
- Identify entry/exit points for REIT investments
- Spot trend reversals in interest rates
- Track momentum across real estate sector
- Flag abnormal market movements
- Historical trend analysis

### 2. MarketCorrelation
**Purpose**: Track relationships between market indicators

**Key Fields**:
- Pearson, Spearman, Kendall correlation coefficients
- Statistical significance (p-value, confidence level)
- Correlation strength (strong, moderate, weak, none)
- Optimal lag analysis (which indicator leads)
- Trading signal classification (leading, lagging, coincident)

**Use Cases**:
- Understand REIT sensitivity to interest rate changes
- Find leading indicators for property price trends
- Identify diversification opportunities
- Build predictive models
- Risk management

### 3. MarketInsight
**Purpose**: Store AI-generated and rule-based actionable insights

**Key Fields**:
- Insight type (trend, anomaly, opportunity, risk, alert)
- Severity (critical, high, medium, low, info)
- Title, summary, detailed analysis
- Related indicators
- Suggested actions
- Confidence score (0-100)
- Expiration date

**Use Cases**:
- Daily market briefings
- Investment opportunity alerts
- Risk warnings
- Automated reporting
- Decision support

### 4. DataQualityMetric
**Purpose**: Monitor data quality and reliability over time

**Key Fields**:
- Completeness percentage
- Accuracy, timeliness, consistency scores
- Overall quality score
- Fetch duration and API response time
- Error rates
- Uptime percentage

**Use Cases**:
- API health monitoring
- Data source reliability tracking
- SLA compliance
- Troubleshooting data issues
- Vendor evaluation

### 5. MarketAnalyticsCache
**Purpose**: Pre-calculated analytics for fast query performance

**Key Fields**:
- Cache key and category
- Analysis type and time period
- Cached results (JSON)
- Freshness tracking
- Calculation duration

**Use Cases**:
- Dashboard performance optimization
- Reduce computation overhead
- Consistent metrics across views
- Historical snapshots

### 6. MarketScenarioAnalysis
**Purpose**: Store what-if projections and stress tests

**Key Fields**:
- Scenario type (base, optimistic, pessimistic, stress)
- Key assumptions (rates, GDP, inflation, unemployment)
- Projected outcomes (prices, rents, REIT performance, cap rates)
- Monthly projections with confidence intervals
- Risk assessment

**Use Cases**:
- Investment planning
- Risk assessment
- Sensitivity analysis
- Portfolio stress testing
- Client presentations

### 7. MarketComparison
**Purpose**: Comparative analyses between markets, periods, or metrics

**Key Fields**:
- Comparison type (market vs market, period vs period, etc.)
- Entities being compared
- Difference metrics (absolute, percentage, relative)
- Statistical comparisons (correlation, beta, alpha)
- Rankings

**Use Cases**:
- Market selection
- Performance benchmarking
- Time-series comparison
- Competitive analysis

### 8. MarketAlert
**Purpose**: Automated alerts for significant market events

**Key Fields**:
- Alert type and severity
- Triggering condition and threshold
- Current vs threshold values
- Alert status (active, acknowledged, resolved, dismissed)
- Notification channels
- Recommended actions

**Use Cases**:
- Real-time monitoring
- Threshold breach notifications
- Risk alerts
- Opportunity detection
- Compliance monitoring

## Analytics Service Features

### Data Validation & Enrichment

**Validates**:
- Price ranges (negative prices, zero prices)
- Volume sanity checks
- 52-week high/low comparisons
- Economic indicator ranges

**Enriches With**:
- Large move flags (>5% daily change)
- Movement classification (strong_up, up, flat, down, strong_down)
- 52-week high/low flags
- Data completeness percentage
- Validation timestamps and issues

### Trend Analysis

**Calculates**:
- Simple Moving Averages (SMA 5, 10, 20, 50, 200)
- Percentage changes across multiple timeframes
- Daily, weekly, monthly volatility
- Relative Strength Index (RSI)
- Momentum scores based on MA crossovers
- Trend direction classification

**Identifies**:
- Bullish/bearish trends
- Golden/death crosses (MA20 crosses MA50)
- Choppy/neutral markets
- Anomalies (>2.5 standard deviations from mean)

**Applications**:
- Technical analysis
- Entry/exit timing
- Risk management
- Portfolio rebalancing

### Correlation Analysis

**Methods**:
- Pearson correlation (linear relationships)
- Spearman correlation (monotonic relationships)
- Kendall Tau (rank correlation)
- Lag analysis (finds leading indicators)

**Tracks**:
- REITs vs Interest Rates
- REITs vs Market Indices (S&P 500)
- Interest Rate Spreads (10Y vs 30Y)
- REIT sector correlations
- Economic indicators vs property prices

**Insights**:
- Correlation strength classification
- Statistical significance testing
- Leading/lagging/coincident relationships
- Optimal lag periods

### Insight Generation

**Rule-Based Insights**:
- Large REIT movements (>3% daily)
- Interest rate trend changes
- Economic indicator anomalies
- Correlation breakdowns

**Future ML-Based Insights**:
- Pattern recognition
- Predictive signals
- Regime change detection
- Sentiment analysis

**Insight Categories**:
- Trends (directional movements)
- Anomalies (unusual patterns)
- Opportunities (buy signals)
- Risks (warning signs)
- Alerts (threshold breaches)

## Enhanced Daily Update Process

### Phase 1-3: Data Collection (Existing)
1. Fetch YFinance data (REITs, indices, rates)
2. Fetch Economics API data
3. Create daily snapshot

### Phase 4: Calculate Trends (NEW)
- Analyzes all indicators fetched in Phase 1-2
- Calculates moving averages, momentum, volatility
- Stores trends in `MarketTrend` table
- Flags anomalies automatically

**Metrics**: Typically calculates 20-30 trends daily

### Phase 5: Calculate Correlations (NEW)
- Tracks key correlation pairs:
  - VNQ vs 10Y Treasury
  - IYR vs 30Y Treasury
  - VNQ vs S&P 500
  - XLRE vs S&P 500
  - 10Y vs 30Y spread
  - VNQ vs IYR
- Stores in `MarketCorrelation` table
- Updates every 90 days

**Metrics**: Calculates 6 correlation pairs daily

### Phase 6: Generate Insights (NEW)
- Analyzes trends for significant movements
- Checks for threshold breaches
- Identifies opportunities and risks
- Stores in `MarketInsight` table

**Metrics**: Generates 5-15 insights daily

### Phase 7: Cleanup (Existing)
- Removes old data (90-180 days)
- Maintains database performance

## Analytics Queries

### Get Latest Trends
```sql
SELECT * FROM market_trends
WHERE analysis_date = CURRENT_DATE
ORDER BY momentum_score DESC;
```

### Find Strong Correlations
```sql
SELECT * FROM market_correlations
WHERE ABS(pearson_correlation) > 0.7
AND is_significant = true
ORDER BY ABS(pearson_correlation) DESC;
```

### Get Active Insights
```sql
SELECT * FROM market_insights
WHERE is_active = true
AND severity IN ('critical', 'high')
ORDER BY insight_date DESC, severity;
```

### Track Data Quality
```sql
SELECT
  data_source,
  AVG(overall_quality_score) as avg_quality,
  AVG(completeness_pct) as avg_completeness,
  AVG(error_rate_pct) as avg_error_rate
FROM data_quality_metrics
WHERE measurement_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY data_source
ORDER BY avg_quality DESC;
```

### Find Anomalies
```sql
SELECT * FROM market_trends
WHERE is_anomaly = true
AND analysis_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY anomaly_score DESC;
```

## API Endpoints (To Be Created)

### Trend Endpoints
- `GET /market-intelligence/trends/{ticker}` - Get trend analysis
- `GET /market-intelligence/trends/anomalies` - Get recent anomalies
- `GET /market-intelligence/trends/momentum` - Get top momentum indicators

### Correlation Endpoints
- `GET /market-intelligence/correlations` - Get all correlations
- `GET /market-intelligence/correlations/{symbol1}/{symbol2}` - Specific pair
- `GET /market-intelligence/correlations/strongest` - Highest correlations

### Insight Endpoints
- `GET /market-intelligence/insights` - Get all active insights
- `GET /market-intelligence/insights/critical` - Critical insights only
- `GET /market-intelligence/insights/{id}/acknowledge` - Acknowledge insight

### Quality Endpoints
- `GET /market-intelligence/quality/summary` - Data quality overview
- `GET /market-intelligence/quality/{source}` - Source-specific quality

### Alert Endpoints
- `GET /market-intelligence/alerts/active` - Active alerts
- `POST /market-intelligence/alerts/{id}/acknowledge` - Acknowledge alert

## Performance Considerations

### Indexing
- All date fields indexed for time-series queries
- Symbol/ticker fields indexed for lookups
- Composite indexes on frequently joined columns
- Covering indexes for common aggregations

### Caching
- Trend calculations cached for 15 minutes
- Correlation results cached for 1 hour
- Insights cached until new day
- Analytics cache table for expensive queries

### Optimization
- Batch processing where possible
- Parallel trend calculations
- Incremental correlation updates
- Async insight generation

## Data Retention

### Short-term (90 days)
- YFinance market data
- Economic indicators
- Data quality metrics

### Medium-term (180 days)
- Market snapshots
- Trends
- Correlations

### Long-term (365+ days)
- Insights (historical reference)
- Scenario analyses
- Major alerts

## Monitoring & Alerting

### Key Metrics to Monitor
- Trend calculation success rate (target: >95%)
- Correlation calculation completions (target: 100%)
- Insight generation count (expected: 5-15/day)
- Data quality scores (target: >90/100)
- Analytics processing time (target: <5 minutes)

### Alert Thresholds
- Critical: Data quality < 70/100
- High: >10% trend calculation failures
- Medium: No insights generated in 24 hours
- Low: Analytics processing > 10 minutes

## Future Enhancements

### Machine Learning Integration
- LSTM for time-series forecasting
- Random Forest for pattern recognition
- Clustering for market regime detection
- Neural networks for sentiment analysis

### Advanced Analytics
- Multi-factor models
- Principal Component Analysis (PCA)
- Causal inference
- Bayesian networks

### User Features
- Custom alert configuration
- Personalized insights
- Interactive scenario builder
- Automated reporting

### Data Sources
- Alternative data integration
- Sentiment data (news, social media)
- Property listing data
- Transaction data

## Best Practices

### Data Validation
- Always validate before storing
- Flag suspicious data
- Maintain audit trail
- Document data quality issues

### Trend Analysis
- Use appropriate time windows
- Consider market regime
- Account for seasonality
- Validate technical indicators

### Correlation Tracking
- Check statistical significance
- Consider lag relationships
- Monitor correlation stability
- Beware of spurious correlations

### Insight Generation
- Set appropriate confidence thresholds
- Include context and rationale
- Provide actionable recommendations
- Track insight accuracy over time

## Troubleshooting

### Trends Not Calculating
- Check for sufficient historical data (need 200+ days for MA200)
- Verify data quality in source tables
- Check for NaN/null values
- Review error logs for exceptions

### Correlations Missing
- Ensure both indicators have overlapping dates
- Verify minimum data points (need 10+)
- Check indicator types match expected
- Review correlation pair definitions

### No Insights Generated
- Verify trend calculations completed
- Check insight generation rules
- Review threshold settings
- Ensure anomaly detection working

### Performance Issues
- Check index usage (EXPLAIN queries)
- Review cache hit rates
- Monitor concurrent calculations
- Consider data archival

## Summary

The enhanced analytics system provides:
- ✅ Comprehensive trend analysis with technical indicators
- ✅ Statistical correlation tracking
- ✅ Automated insight generation
- ✅ Data quality monitoring
- ✅ Analytical caching for performance
- ✅ Scenario analysis capabilities
- ✅ Real-time alerting
- ✅ Historical comparison tools

These enhancements enable deeper analysis, better decision-making, and automated intelligence for real estate investment strategies.
