# Economic Analysis Tools - Quick Start

## 🚀 Quick Start Guide

### Installation

All analysis tools are already installed. No additional dependencies needed!

### Basic Usage

```bash
cd /home/user/real_estate_dashboard/backend

# 1. Analyze a country's economy
python3 analyze_economics.py analyze united-states

# 2. Compare countries
python3 analyze_economics.py compare united-states china japan \
  --indicator "GDP Growth Rate"

# 3. Housing market deep-dive
python3 analyze_economics.py housing united-states

# 4. Trend analysis
python3 analyze_economics.py trends united-states "House Prices"

# 5. Find correlations
python3 analyze_economics.py correlate united-states \
  "House Prices" "Mortgage Rate"
```

---

## 📊 Available Analysis Tools

### 1. Economic Analyzer
**What it does:** Comprehensive single-country economic health assessment

**Features:**
- Classifies indicators as Leading/Coincident/Lagging
- Calculates economic health score (0-100)
- Identifies positive/negative signals
- Provides interpretation for each indicator

**Use when:** You want to understand overall economic health

```bash
python3 analyze_economics.py analyze united-states
```

---

### 2. Country Comparator
**What it does:** Compare economic metrics across multiple countries

**Features:**
- Side-by-side indicator comparison
- Rankings and statistics
- PPP-adjusted GDP per capita
- Housing affordability comparison
- Country scoring system

**Use when:** Comparing markets or investment locations

```bash
python3 analyze_economics.py compare united-states china germany \
  --indicator "Unemployment Rate" --category labour
```

---

### 3. Trend Analyzer
**What it does:** Analyze historical trends and forecast future values

**Features:**
- Growth rate calculations (PoP, YoY, CAGR)
- Trend strength and direction
- Volatility analysis
- Momentum indicators
- Simple forecasting

**Use when:** Understanding price/indicator trends over time

```bash
python3 analyze_economics.py trends united-states "GDP Growth Rate"
```

---

### 4. Correlation Analyzer
**What it does:** Find relationships between economic indicators

**Features:**
- Pearson correlation calculation
- Theory validation (e.g., Okun's Law)
- Leading indicator identification
- Multi-indicator correlation matrix

**Use when:** Understanding what drives specific indicators

```bash
python3 analyze_economics.py correlate united-states \
  "House Prices" "GDP Growth Rate"
```

---

### 5. Housing Market Analyzer
**What it does:** Specialized real estate market analysis

**Features:**
- Market cycle identification (Expansion/Peak/Contraction/Trough)
- Affordability analysis (price-to-income, payment burden)
- Market momentum assessment
- Health score calculation
- Buy/sell recommendations

**Use when:** Making real estate investment decisions

```bash
python3 analyze_economics.py housing united-states
```

---

## 🎯 Common Use Cases

### Use Case 1: "Should I buy a house now?"

```bash
# Step 1: Check housing market health
python3 analyze_economics.py housing united-states

# Look for:
# - Market Cycle: Is it Expansion (prices rising) or Contraction?
# - Affordability: Is price-to-income ratio reasonable (<5)?
# - Momentum: Are permits/starts increasing or decreasing?

# Step 2: Check mortgage rate trends
python3 analyze_economics.py trends united-states "Mortgage Rate 30Y"

# Look for:
# - Direction: Rising or falling?
# - Forecast: Expected to increase or decrease?

# Step 3: Check economic health
python3 analyze_economics.py analyze united-states

# Look for:
# - Health Score: >60 is good
# - Employment: Low unemployment = job security
# - GDP Growth: Positive = economic strength
```

**Decision Framework:**
- ✅ **Buy if:** Contraction/Trough cycle, falling rates, good health
- ⏸️ **Wait if:** Peak cycle, rising rates, weak health
- ❌ **Avoid if:** Peak + rising rates + weak health

---

### Use Case 2: "Which country has the best real estate opportunity?"

```bash
# Step 1: Compare housing affordability
python3 analyze_economics.py compare united-states canada australia germany \
  --indicator "House Price" --category housing

# Step 2: Check each country's housing market
python3 analyze_economics.py housing united-states
python3 analyze_economics.py housing canada
python3 analyze_economics.py housing australia
python3 analyze_economics.py housing germany

# Step 3: Compare economic health
python3 analyze_economics.py analyze united-states
python3 analyze_economics.py analyze canada
# ... etc

# Look for:
# - Lowest price-to-income ratio = best affordability
# - Expansion/Recovery cycle = growth potential
# - High health score = economic stability
```

---

### Use Case 3: "Is the economy heading for recession?"

```bash
# Step 1: Check leading indicators
python3 analyze_economics.py analyze united-states

# Look at:
# - Leading indicators section
# - Are Building Permits, Consumer Confidence declining?

# Step 2: Analyze GDP trend
python3 analyze_economics.py trends united-states "GDP Growth Rate"

# Look for:
# - Downward trend
# - Negative momentum
# - Slowing growth rates

# Step 3: Check unemployment correlation with GDP
python3 analyze_economics.py correlate united-states \
  "GDP Growth Rate" "Unemployment Rate"

# Should be negative correlation
# If positive (GDP down, unemployment up) = recession warning
```

**Recession Signals:**
- 📉 Leading indicators declining
- 📉 GDP growth slowing or negative
- 📈 Unemployment rising
- 📉 Consumer confidence falling
- 📉 PMI < 50

---

### Use Case 4: "What factors drive house prices?"

```bash
# Test multiple correlations
python3 analyze_economics.py correlate united-states \
  "House Prices" "GDP Growth Rate"

python3 analyze_economics.py correlate united-states \
  "House Prices" "Mortgage Rate 30Y"

python3 analyze_economics.py correlate united-states \
  "House Prices" "Unemployment Rate"

python3 analyze_economics.py correlate united-states \
  "House Prices" "Building Permits"

# Expected results:
# - GDP: Positive correlation (+0.3 to +0.5)
# - Mortgage Rate: Negative correlation (-0.4 to -0.6)
# - Unemployment: Negative correlation (-0.3 to -0.5)
# - Building Permits: Positive correlation (+0.5 to +0.7)
```

---

## 📚 Key Metrics Cheat Sheet

### Economic Health Score
- **80-100**: Excellent
- **60-79**: Good
- **40-59**: Mixed
- **20-39**: Weak
- **0-19**: Poor

### GDP Growth Rate
- **>4%**: Very strong
- **2-4%**: Healthy
- **0-2%**: Sluggish
- **<0%**: Recession

### Unemployment Rate
- **<3.5%**: Very tight
- **3.5-5%**: Healthy
- **5-7%**: Elevated
- **>7%**: High

### Inflation (CPI)
- **<1%**: Too low
- **1-3%**: Healthy
- **3-5%**: Elevated
- **>5%**: High

### Price-to-Income Ratio
- **<3**: Excellent affordability
- **3-4**: Good
- **4-5**: Moderate
- **5-6**: Poor
- **>6**: Very poor

### PMI
- **>50**: Expansion
- **=50**: Neutral
- **<50**: Contraction

### Correlation Coefficient
- **0.7-1.0**: Strong positive
- **0.3-0.7**: Moderate positive
- **-0.3 to 0.3**: Weak/none
- **-0.7 to -0.3**: Moderate negative
- **-1.0 to -0.7**: Strong negative

---

## 🔧 Python API Usage

### Example: Full Analysis Pipeline

```python
from app.database.country_database_manager import country_db_manager
from app.services.economics_db_service import EconomicsDBService
from app.services.economic_analyzer import EconomicAnalyzer
from app.services.housing_market_analyzer import HousingMarketAnalyzer
from app.services.country_comparator import CountryComparator

# Setup
db = country_db_manager.get_session("united-states")
db_service = EconomicsDBService(db)

# 1. Economic health check
analyzer = EconomicAnalyzer(db_service)
economic_health = analyzer.analyze_country("United States")
print(f"Health Score: {economic_health['summary']['health_score']}/100")

# 2. Housing market analysis
housing_analyzer = HousingMarketAnalyzer(db_service)
housing_analysis = housing_analyzer.analyze_housing_market("United States")
print(f"Market Cycle: {housing_analysis['market_cycle']['phase']}")
print(f"Affordability: {housing_analysis['affordability']['level']}")

# 3. Compare to other countries
comparator = CountryComparator()
comparison = comparator.compare_housing_affordability([
    "United States", "Canada", "Germany"
])

# Rankings
for rank in comparison['rankings']:
    print(f"#{rank['rank']} {rank['country']}: {rank['affordability']}")

# 4. Trend analysis
from app.services.trend_analyzer import TrendAnalyzer
trend_analyzer = TrendAnalyzer(db_service)

trend = trend_analyzer.analyze_trend(
    "United States",
    "House Prices",
    periods=12
)

print(f"Trend: {trend['trend']['direction']}")
print(f"Growth: {trend['growth_rates']['year_over_year']:.2f}%")
```

---

## 📖 Full Documentation

For complete details on all metrics, interpretations, and economic theory:

**See:** `ECONOMIC_ANALYSIS_GUIDE.md`

Topics covered:
- Economic indicator classifications (Leading/Lagging/Coincident)
- All metrics explained in detail
- Economic theory (Okun's Law, Phillips Curve, etc.)
- Real-world examples and interpretations
- Advanced analysis techniques

---

## 🎯 Next Steps

1. **Run your first analysis:**
   ```bash
   python3 analyze_economics.py analyze united-states
   ```

2. **Try housing market analysis:**
   ```bash
   python3 analyze_economics.py housing united-states
   ```

3. **Compare countries:**
   ```bash
   python3 analyze_economics.py compare united-states china japan \
     --indicator "GDP Growth Rate"
   ```

4. **Read full guide:**
   Open `ECONOMIC_ANALYSIS_GUIDE.md` for complete documentation

---

## 🆘 Troubleshooting

**Error: No data available**
```bash
# Ensure country database is initialized and data is fetched
python3 initialize_country_databases.py --country united-states
python3 country_scripts/update_united_states.py
```

**Error: Country not found**
```bash
# List available countries
python3 initialize_country_databases.py --list

# Use correct country slug (e.g., "united-states" not "usa")
```

**Need more help?**
- Check `ECONOMIC_ANALYSIS_GUIDE.md` for detailed explanations
- Review `COUNTRY_DATABASES_GUIDE.md` for database setup
- See `WEEKLY_UPDATE_SYSTEM.md` for data fetching

---

**🎉 You now have professional-grade economic analysis tools!**
