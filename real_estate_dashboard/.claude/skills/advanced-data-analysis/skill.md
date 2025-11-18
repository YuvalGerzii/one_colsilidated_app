---
name: Advanced Data Analysis Expert
description: Provides sophisticated data analysis techniques, statistical insights, and actionable recommendations for real estate business intelligence
---

# Advanced Data Analysis Expert

## Overview

This skill enables Claude to perform advanced data analysis on real estate data, uncovering deep insights, patterns, and actionable intelligence. It combines statistical rigor with business acumen to transform raw data into strategic recommendations.

## When to Use This Skill

Invoke this skill when:
- Analyzing complex datasets to identify trends, patterns, or anomalies
- Performing statistical analysis and hypothesis testing
- Creating executive-level insights and recommendations
- Conducting comparative analysis across properties, markets, or time periods
- Identifying correlations and causal relationships in real estate data
- Building data-driven narratives for decision-making
- Validating assumptions or testing business hypotheses
- Segmenting data for targeted analysis (cohort analysis, market segmentation)

## Core Analysis Capabilities

### 1. Exploratory Data Analysis (EDA)

**Key Techniques:**
- Descriptive statistics (mean, median, mode, standard deviation, quartiles)
- Distribution analysis (normal, skewed, bimodal distributions)
- Outlier detection (IQR method, Z-score, isolation forest)
- Missing data analysis and imputation strategies
- Data quality assessment and validation

**Real Estate Applications:**
```python
# Property price distribution analysis
def analyze_price_distribution(properties):
    """
    Analyze property price distribution with statistical measures
    """
    return {
        'mean': np.mean(properties.price),
        'median': np.median(properties.price),
        'std_dev': np.std(properties.price),
        'quartiles': np.percentile(properties.price, [25, 50, 75]),
        'skewness': stats.skew(properties.price),
        'kurtosis': stats.kurtosis(properties.price),
        'outliers': detect_outliers_iqr(properties.price)
    }
```

### 2. Comparative Analysis

**Techniques:**
- Year-over-year (YoY) analysis
- Period-over-period comparisons
- Benchmark analysis against market standards
- Portfolio performance comparison
- Market segmentation analysis

**Example Metrics:**
```typescript
interface ComparativeMetrics {
  yoyGrowth: number;           // Year-over-year growth %
  marketShare: number;          // Share of total market
  relativePerformance: number;  // vs. benchmark (1.0 = at par)
  percentileRank: number;       // Position in distribution
  zScore: number;               // Standard deviations from mean
}
```

### 3. Trend Analysis

**Methods:**
- Moving averages (simple, weighted, exponential)
- Trend line fitting (linear, polynomial, exponential)
- Seasonality detection and decomposition
- Growth rate calculations (CAGR, compounding)
- Momentum indicators

**Key Formulas:**
```
CAGR = (Ending Value / Beginning Value)^(1/years) - 1

Moving Average (n-period) = Σ(values) / n

Exponential MA = (Value_today × K) + (EMA_yesterday × (1-K))
where K = 2/(n+1)
```

### 4. Correlation and Causation Analysis

**Statistical Tests:**
- Pearson correlation coefficient (linear relationships)
- Spearman rank correlation (monotonic relationships)
- Regression analysis (simple, multiple, polynomial)
- Multicollinearity detection (VIF - Variance Inflation Factor)
- Granger causality tests

**Real Estate Example:**
```python
# Analyze factors affecting property NOI
def analyze_noi_drivers(df):
    """
    Identify key drivers of Net Operating Income
    """
    features = ['occupancy_rate', 'rental_rate', 'operating_expenses',
                'property_age', 'units', 'market_rent_growth']

    # Correlation matrix
    correlation_matrix = df[features + ['noi']].corr()

    # Multiple regression
    from sklearn.linear_model import LinearRegression
    X = df[features]
    y = df['noi']
    model = LinearRegression().fit(X, y)

    return {
        'correlations': correlation_matrix['noi'].sort_values(ascending=False),
        'feature_importance': dict(zip(features, model.coef_)),
        'r_squared': model.score(X, y)
    }
```

### 5. Segmentation and Cohort Analysis

**Approaches:**
- Market segmentation (geographic, demographic, behavioral)
- Property clustering (by performance, characteristics)
- Tenant cohort analysis
- Investment vintage analysis
- Risk-based segmentation

**Example Segments:**
```typescript
interface PropertySegment {
  segmentName: string;
  criteria: {
    priceRange?: [number, number];
    capRateRange?: [number, number];
    occupancyRate?: number;
    location?: string[];
    propertyType?: string[];
  };
  metrics: {
    count: number;
    avgPerformance: number;
    growthRate: number;
    riskScore: number;
  };
}
```

### 6. Anomaly Detection

**Techniques:**
- Statistical outliers (Z-score, modified Z-score)
- IQR-based detection
- Time series anomalies
- Contextual anomalies (unusual combinations)
- Change point detection

**Alert Thresholds:**
```python
# Define anomaly detection rules
ANOMALY_RULES = {
    'price_zscore': 3.0,        # 3 std deviations from mean
    'vacancy_spike': 0.15,      # 15% increase in vacancy
    'expense_ratio': 0.60,      # Operating expenses > 60% of revenue
    'rent_decline': -0.10,      # 10% decline in rental rates
}
```

### 7. Predictive Indicators

**Leading Indicators:**
- Rental inquiry volume trends
- Days-on-market velocity changes
- Permit and construction activity
- Economic indicators (employment, GDP growth)
- Interest rate trends

**Lagging Indicators:**
- Historical occupancy rates
- Realized returns
- Completed transactions
- Actual rent growth

## Best Practices

### ✅ DO:

1. **Start with Questions**
   - Define clear analytical questions before diving into data
   - Align analysis with business objectives
   - Identify key decisions the analysis should inform

2. **Validate Data Quality**
   - Check for missing, duplicate, or inconsistent data
   - Verify data sources and collection methods
   - Document data quality issues and handling approaches

3. **Use Appropriate Statistical Methods**
   - Choose tests appropriate for data distribution
   - Check assumptions (normality, independence, homoscedasticity)
   - Report confidence intervals and p-values where relevant

4. **Provide Context**
   - Compare against benchmarks and historical performance
   - Consider external factors (market conditions, seasonality)
   - Explain statistical findings in business terms

5. **Visualize Effectively**
   - Use appropriate chart types for the data
   - Highlight key insights with annotations
   - Keep visualizations clean and focused

6. **Document Methodology**
   - Explain analytical approach and assumptions
   - Provide reproducible code/formulas
   - Note limitations of the analysis

### ❌ DON'T:

1. **Confuse Correlation with Causation**
   - Don't assume relationships are causal without evidence
   - Consider confounding variables
   - Use causal inference methods when appropriate

2. **Cherry-Pick Data**
   - Don't selectively report only favorable findings
   - Present complete picture including limitations
   - Avoid survivorship bias

3. **Ignore Statistical Significance**
   - Don't report findings without statistical validation
   - Check sample sizes are adequate
   - Consider Type I and Type II errors

4. **Over-Complicate**
   - Don't use complex methods when simple ones suffice
   - Avoid jargon in executive summaries
   - Focus on actionable insights

## Analysis Frameworks

### STAR Analysis Framework
- **S**ituation: Current state and context
- **T**rend: Historical patterns and trajectories
- **A**nomaly: Deviations and outliers
- **R**ecommendation: Data-driven next steps

### Five Whys + Data
Use iterative questioning to dig deeper:
1. Why is occupancy declining? → Data shows 15% drop in Q4
2. Why in Q4? → Seasonal analysis shows it's unusual for this market
3. Why is this market different? → Competitor analysis reveals 3 new properties
4. Why did competitors enter? → Market rent growth was 8% annually
5. Why didn't we see this coming? → Leading indicators were not monitored

## Sample Analysis Workflow

```python
# Complete analysis workflow example
def comprehensive_property_analysis(property_data):
    """
    End-to-end analysis of property portfolio
    """

    # 1. Data Quality Check
    quality_report = assess_data_quality(property_data)

    # 2. Descriptive Statistics
    descriptive_stats = calculate_descriptive_stats(property_data)

    # 3. Trend Analysis
    trends = analyze_trends(property_data, periods=['monthly', 'quarterly', 'yearly'])

    # 4. Comparative Analysis
    benchmarks = compare_to_benchmarks(property_data, market_data)

    # 5. Correlation Analysis
    correlations = analyze_correlations(property_data)

    # 6. Segmentation
    segments = segment_properties(property_data, criteria=['performance', 'location', 'type'])

    # 7. Anomaly Detection
    anomalies = detect_anomalies(property_data)

    # 8. Insights Generation
    insights = generate_insights({
        'stats': descriptive_stats,
        'trends': trends,
        'benchmarks': benchmarks,
        'correlations': correlations,
        'segments': segments,
        'anomalies': anomalies
    })

    # 9. Recommendations
    recommendations = generate_recommendations(insights)

    return {
        'executive_summary': create_executive_summary(insights, recommendations),
        'detailed_findings': insights,
        'recommendations': recommendations,
        'supporting_data': {
            'quality_report': quality_report,
            'stats': descriptive_stats,
            'visualizations': generate_visualizations(property_data, insights)
        }
    }
```

## Key Performance Indicators (KPIs) to Analyze

### Financial KPIs
- Net Operating Income (NOI) and trends
- Cash-on-Cash Return
- IRR (Internal Rate of Return)
- Cap Rate compression/expansion
- Debt Service Coverage Ratio (DSCR)

### Operational KPIs
- Occupancy rate and velocity
- Tenant turnover rate
- Average lease term
- Rent collection rate
- Maintenance cost per unit

### Market KPIs
- Rent growth rate (actual vs. market)
- Market absorption rate
- Competitive position (price, amenities)
- Market share by segment

## Statistical Significance Guidelines

- **p-value < 0.05**: Statistically significant (95% confidence)
- **p-value < 0.01**: Highly significant (99% confidence)
- **Effect size**: Report practical significance, not just statistical
- **Sample size**: Minimum 30 observations for parametric tests
- **Confidence intervals**: Report 95% CI for estimates

## Execution Instructions

When this skill is invoked:

1. **Understand the Question**
   - Clarify the business question or decision to be informed
   - Identify relevant metrics and data sources
   - Define success criteria for the analysis

2. **Explore the Data**
   - Assess data quality and completeness
   - Calculate descriptive statistics
   - Identify distributions, outliers, and patterns

3. **Apply Appropriate Methods**
   - Select statistical techniques suited to the question
   - Validate assumptions
   - Perform rigorous analysis

4. **Generate Insights**
   - Interpret findings in business context
   - Identify patterns, trends, and anomalies
   - Quantify relationships and impacts

5. **Create Recommendations**
   - Translate insights into actionable recommendations
   - Prioritize by impact and feasibility
   - Quantify expected outcomes where possible

6. **Communicate Clearly**
   - Provide executive summary for decision-makers
   - Support with detailed analysis for stakeholders
   - Use visualizations to enhance understanding
   - Document methodology for reproducibility

## Integration with Other Skills

- **Data Science**: Use for predictive modeling and machine learning
- **Finance**: Apply to financial analysis and valuation
- **Manager/CEO**: Frame insights for strategic decision-making
- **Marketing**: Segment customers and analyze campaign effectiveness

## Deliverable Checklist

Before completing analysis:
- [ ] Business question is clearly defined
- [ ] Data quality has been assessed and documented
- [ ] Appropriate statistical methods have been applied
- [ ] Assumptions have been validated
- [ ] Statistical significance has been tested
- [ ] Results are interpreted in business context
- [ ] Visualizations effectively communicate findings
- [ ] Actionable recommendations are provided
- [ ] Limitations and caveats are documented
- [ ] Analysis is reproducible (code/formulas provided)

