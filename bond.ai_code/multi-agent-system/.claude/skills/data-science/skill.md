# Data Science & Analytics Expert

This skill provides comprehensive guidance for professional data analysis, statistical modeling, and insight generation for real estate financial analytics, with emphasis on actionable intelligence and data-driven decision making.

## Overview

You are a data science expert specializing in real estate analytics and financial modeling. Your role is to:
- Analyze complex real estate and financial datasets
- Apply statistical and machine learning techniques
- Generate actionable insights from data
- Create predictive models for investment decisions
- Visualize data to tell compelling stories
- Identify trends, patterns, and anomalies
- Provide evidence-based recommendations
- Quantify risk and opportunity

## Core Philosophy

**Data-Driven Decision Making:**
- Start with business questions, not just data
- Focus on actionable insights, not just numbers
- Validate assumptions with statistical rigor
- Communicate findings clearly to stakeholders
- Balance sophistication with interpretability
- Always consider real-world context

**Professional Standards:**
- Institutional-grade analytics for investment decisions
- Reproducible analysis with clear methodology
- Transparent assumptions and limitations
- Appropriate statistical significance testing
- Proper handling of outliers and missing data
- Regular model validation and monitoring

## Current Project Context

**Tech Stack:**

*Backend (Python):*
- NumPy 1.26.2 & Pandas 2.1.4 (data processing)
- SciPy 1.11.4 (scientific computing)
- Scikit-learn 1.3.2 (machine learning)
- XGBoost 2.0.3 (gradient boosting)
- Statsmodels 0.14.1 (time series & forecasting)
- NumPy Financial 1.0.0 (financial calculations)
- Matplotlib 3.8.2 (visualization)
- YFinance 0.2.66 (market data)

*Frontend (TypeScript/JavaScript):*
- Recharts 2.15.2 (primary charting)
- Chart.js 4.5.1 (alternative charting)
- date-fns 4.1.0 (date utilities)

**Domain Focus:**
- Real estate property analysis
- Portfolio performance analytics
- Investment return modeling (IRR, MOIC, Cash-on-Cash)
- Risk assessment (concentration, leverage, market)
- Market intelligence and trends
- Property valuation and comps analysis
- Cash flow forecasting
- Fund performance tracking

## Data Analysis Methodologies

### 1. Real Estate Financial Metrics

**Internal Rate of Return (IRR):**
```python
import numpy as np
from numpy_financial import irr

def calculate_portfolio_irr(cash_flows: list, dates: list) -> float:
    """
    Calculate IRR from time-series cash flows.

    Args:
        cash_flows: List of cash flows (negative for investments, positive for returns)
        dates: List of corresponding dates

    Returns:
        Annualized IRR as percentage
    """
    # Sort by date
    sorted_flows = sorted(zip(dates, cash_flows), key=lambda x: x[0])
    dates_sorted = [d for d, _ in sorted_flows]
    flows_sorted = [f for _, f in sorted_flows]

    # Calculate IRR using numpy_financial
    periodic_irr = irr(flows_sorted)

    # Annualize based on period
    if len(dates_sorted) > 1:
        days_total = (dates_sorted[-1] - dates_sorted[0]).days
        periods_per_year = 365 / max(days_total / len(flows_sorted), 1)
        annual_irr = ((1 + periodic_irr) ** periods_per_year - 1) * 100
        return round(annual_irr, 2)

    return None


def calculate_xirr(cash_flows: list, dates: list) -> float:
    """
    Calculate XIRR (Extended IRR) for irregular cash flows.

    More accurate than IRR for real-world scenarios with irregular timing.
    """
    from scipy.optimize import newton

    def xirr_func(rate, cash_flows, dates):
        """NPV function for XIRR calculation."""
        return sum(
            cf / ((1 + rate) ** ((date - dates[0]).days / 365.0))
            for cf, date in zip(cash_flows, dates)
        )

    try:
        # Use Newton's method to find the rate where NPV = 0
        result = newton(lambda r: xirr_func(r, cash_flows, dates), 0.1)
        return round(result * 100, 2)  # Convert to percentage
    except:
        return None


# Example usage
cash_flows = [-1000000, 50000, 60000, 70000, 1200000]  # Initial investment + returns
dates = [
    datetime(2020, 1, 1),
    datetime(2020, 12, 31),
    datetime(2021, 12, 31),
    datetime(2022, 12, 31),
    datetime(2023, 12, 31),
]

irr_value = calculate_xirr(cash_flows, dates)
print(f"Portfolio IRR: {irr_value}%")
```

**Multiple on Invested Capital (MOIC):**
```python
from decimal import Decimal

def calculate_moic(
    initial_investment: Decimal,
    current_value: Decimal,
    total_distributions: Decimal = Decimal(0)
) -> float:
    """
    Calculate MOIC (Multiple on Invested Capital).

    MOIC = (Current Value + Total Distributions) / Initial Investment

    Example:
        Investment: $1M
        Current Value: $2M
        Distributions: $500K
        MOIC = ($2M + $500K) / $1M = 2.5x
    """
    if initial_investment <= 0:
        return None

    total_return = current_value + total_distributions
    moic = float(total_return) / float(initial_investment)

    return round(moic, 2)


def calculate_cash_on_cash(
    annual_cash_flow: Decimal,
    initial_cash_invested: Decimal
) -> float:
    """
    Calculate Cash-on-Cash Return.

    CoC = Annual Pre-Tax Cash Flow / Total Cash Invested
    """
    if initial_cash_invested <= 0:
        return None

    coc = (float(annual_cash_flow) / float(initial_cash_invested)) * 100
    return round(coc, 2)
```

**Cap Rate Analysis:**
```python
def calculate_cap_rate(noi: Decimal, property_value: Decimal) -> float:
    """
    Calculate Capitalization Rate.

    Cap Rate = NOI / Property Value
    """
    if property_value <= 0:
        return None

    cap_rate = (float(noi) / float(property_value)) * 100
    return round(cap_rate, 2)


def calculate_going_in_cap_rate(
    year_1_noi: Decimal,
    purchase_price: Decimal,
    closing_costs: Decimal = Decimal(0)
) -> float:
    """
    Calculate Going-In Cap Rate (Year 1).

    Includes closing costs in the denominator.
    """
    total_cost = purchase_price + closing_costs
    return calculate_cap_rate(year_1_noi, total_cost)


def stabilized_cap_rate(
    stabilized_noi: Decimal,
    property_value: Decimal
) -> float:
    """
    Calculate Stabilized Cap Rate (at full occupancy).
    """
    return calculate_cap_rate(stabilized_noi, property_value)
```

**Debt Service Coverage Ratio (DSCR):**
```python
def calculate_dscr(noi: Decimal, annual_debt_service: Decimal) -> float:
    """
    Calculate Debt Service Coverage Ratio.

    DSCR = NOI / Annual Debt Service

    Typical lending requirements:
    - DSCR > 1.25 for most commercial loans
    - DSCR > 1.35 for agency loans
    """
    if annual_debt_service <= 0:
        return None

    dscr = float(noi) / float(annual_debt_service)
    return round(dscr, 2)


def calculate_ltv(loan_amount: Decimal, property_value: Decimal) -> float:
    """
    Calculate Loan-to-Value Ratio.

    LTV = Loan Amount / Property Value
    """
    if property_value <= 0:
        return None

    ltv = (float(loan_amount) / float(property_value)) * 100
    return round(ltv, 2)
```

### 2. Statistical Analysis Techniques

**Descriptive Statistics:**
```python
import pandas as pd
import numpy as np
from scipy import stats

def comprehensive_statistics(data: pd.Series, metric_name: str) -> dict:
    """
    Calculate comprehensive descriptive statistics.

    Returns full statistical summary for a metric.
    """
    return {
        'metric': metric_name,
        'count': int(data.count()),
        'mean': float(data.mean()),
        'median': float(data.median()),
        'std_dev': float(data.std()),
        'variance': float(data.var()),
        'min': float(data.min()),
        'max': float(data.max()),
        'q1': float(data.quantile(0.25)),
        'q3': float(data.quantile(0.75)),
        'iqr': float(data.quantile(0.75) - data.quantile(0.25)),
        'skewness': float(stats.skew(data.dropna())),
        'kurtosis': float(stats.kurtosis(data.dropna())),
        'cv': float(data.std() / data.mean()) if data.mean() != 0 else None,  # Coefficient of variation
    }


def detect_outliers_iqr(data: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method.

    Args:
        data: Series of values
        multiplier: IQR multiplier (typically 1.5 or 3.0)

    Returns:
        Boolean series indicating outliers
    """
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    return (data < lower_bound) | (data > upper_bound)


def detect_outliers_zscore(data: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using Z-score method.

    Args:
        data: Series of values
        threshold: Z-score threshold (typically 2.5 or 3.0)

    Returns:
        Boolean series indicating outliers
    """
    z_scores = np.abs(stats.zscore(data.dropna()))
    return pd.Series(z_scores > threshold, index=data.index)
```

**Correlation Analysis:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

def correlation_analysis(df: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """
    Perform correlation analysis between variables.

    Args:
        df: DataFrame with numeric columns
        method: 'pearson', 'spearman', or 'kendall'

    Returns:
        Correlation matrix
    """
    corr_matrix = df.corr(method=method)
    return corr_matrix


def find_strong_correlations(
    df: pd.DataFrame,
    threshold: float = 0.7,
    method: str = 'pearson'
) -> list:
    """
    Find pairs of variables with strong correlations.

    Returns list of tuples: (var1, var2, correlation)
    """
    corr_matrix = df.corr(method=method)

    strong_correlations = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) >= threshold:
                strong_correlations.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    round(corr_value, 3)
                ))

    return sorted(strong_correlations, key=lambda x: abs(x[2]), reverse=True)


# Example: Analyze property metrics correlations
property_metrics = df[['cap_rate', 'occupancy_rate', 'noi', 'property_value', 'age']]
correlations = find_strong_correlations(property_metrics, threshold=0.6)

for var1, var2, corr in correlations:
    print(f"{var1} <-> {var2}: {corr}")
```

**Hypothesis Testing:**
```python
from scipy.stats import ttest_ind, mannwhitneyu, chi2_contingency

def compare_two_groups(
    group1: pd.Series,
    group2: pd.Series,
    test_type: str = 'auto'
) -> dict:
    """
    Compare two groups using appropriate statistical test.

    Args:
        group1, group2: Data for each group
        test_type: 'ttest', 'mannwhitney', or 'auto'

    Returns:
        Dictionary with test results
    """
    # Remove NaN values
    group1_clean = group1.dropna()
    group2_clean = group2.dropna()

    # Check normality (Shapiro-Wilk test)
    _, p_norm1 = stats.shapiro(group1_clean) if len(group1_clean) < 5000 else (None, 0.05)
    _, p_norm2 = stats.shapiro(group2_clean) if len(group2_clean) < 5000 else (None, 0.05)

    is_normal = (p_norm1 > 0.05) and (p_norm2 > 0.05)

    # Choose test
    if test_type == 'auto':
        test_type = 'ttest' if is_normal else 'mannwhitney'

    # Perform test
    if test_type == 'ttest':
        statistic, p_value = ttest_ind(group1_clean, group2_clean)
        test_name = "Independent t-test"
    else:
        statistic, p_value = mannwhitneyu(group1_clean, group2_clean)
        test_name = "Mann-Whitney U test"

    return {
        'test': test_name,
        'statistic': float(statistic),
        'p_value': float(p_value),
        'significant': p_value < 0.05,
        'group1_mean': float(group1_clean.mean()),
        'group2_mean': float(group2_clean.mean()),
        'difference': float(group1_clean.mean() - group2_clean.mean()),
        'effect_size': float(abs(group1_clean.mean() - group2_clean.mean()) /
                           np.sqrt((group1_clean.std()**2 + group2_clean.std()**2) / 2))
    }


# Example: Compare performance of two markets
market_a_returns = df[df['market'] == 'Market A']['annual_return']
market_b_returns = df[df['market'] == 'Market B']['annual_return']

result = compare_two_groups(market_a_returns, market_b_returns)
print(f"P-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")
```

### 3. Time Series Analysis & Forecasting

**Trend Analysis:**
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def decompose_time_series(
    data: pd.Series,
    period: int = 12,
    model: str = 'additive'
) -> dict:
    """
    Decompose time series into trend, seasonal, and residual components.

    Args:
        data: Time series data with datetime index
        period: Seasonal period (12 for monthly data with yearly seasonality)
        model: 'additive' or 'multiplicative'

    Returns:
        Dictionary with decomposition components
    """
    decomposition = seasonal_decompose(data, model=model, period=period)

    return {
        'trend': decomposition.trend,
        'seasonal': decomposition.seasonal,
        'residual': decomposition.resid,
        'original': data
    }


def forecast_exponential_smoothing(
    data: pd.Series,
    periods: int = 12,
    seasonal_periods: int = 12,
    trend: str = 'add',
    seasonal: str = 'add'
) -> dict:
    """
    Forecast using Exponential Smoothing (Holt-Winters).

    Good for data with trend and seasonality.
    """
    model = ExponentialSmoothing(
        data,
        seasonal_periods=seasonal_periods,
        trend=trend,
        seasonal=seasonal seasonal
    )

    fitted_model = model.fit()
    forecast = fitted_model.forecast(periods)

    # Calculate confidence intervals (simplified)
    std_err = np.std(fitted_model.resid)

    return {
        'forecast': forecast,
        'lower_bound': forecast - 1.96 * std_err,
        'upper_bound': forecast + 1.96 * std_err,
        'fitted_values': fitted_model.fittedvalues,
        'model': fitted_model
    }


# Example: Forecast NOI for next 12 months
monthly_noi = df.set_index('date')['noi']
forecast_result = forecast_exponential_smoothing(monthly_noi, periods=12)

print("12-Month NOI Forecast:")
for date, value in forecast_result['forecast'].items():
    print(f"{date}: ${value:,.0f}")
```

**Moving Averages & Momentum:**
```python
def calculate_moving_averages(data: pd.Series, windows: list = [3, 6, 12]) -> pd.DataFrame:
    """
    Calculate multiple moving averages.

    Useful for identifying trends in property values, rents, etc.
    """
    df = pd.DataFrame({'value': data})

    for window in windows:
        df[f'ma_{window}'] = data.rolling(window=window).mean()
        df[f'ema_{window}'] = data.ewm(span=window, adjust=False).mean()

    return df


def calculate_momentum_indicators(data: pd.Series, periods: int = 12) -> pd.DataFrame:
    """
    Calculate momentum and rate of change indicators.
    """
    df = pd.DataFrame({'value': data})

    # Rate of change
    df['roc'] = data.pct_change(periods=periods) * 100

    # Momentum (absolute change)
    df['momentum'] = data.diff(periods=periods)

    # Relative strength
    gains = data.diff().clip(lower=0)
    losses = -data.diff().clip(upper=0)

    avg_gains = gains.rolling(window=periods).mean()
    avg_losses = losses.rolling(window=periods).mean()

    rs = avg_gains / avg_losses
    df['rsi'] = 100 - (100 / (1 + rs))

    return df


# Example: Analyze property value trends
property_values = df.set_index('date')['property_value']
ma_df = calculate_moving_averages(property_values)

# Identify trend
if ma_df['ma_3'].iloc[-1] > ma_df['ma_12'].iloc[-1]:
    print("Short-term upward trend detected")
```

**Seasonality Detection:**
```python
from statsmodels.tsa.stattools import adfuller

def test_stationarity(data: pd.Series) -> dict:
    """
    Test if time series is stationary using Augmented Dickey-Fuller test.

    Stationary = mean and variance constant over time
    """
    result = adfuller(data.dropna())

    return {
        'adf_statistic': float(result[0]),
        'p_value': float(result[1]),
        'is_stationary': result[1] < 0.05,
        'critical_values': result[4]
    }


def detect_seasonality(data: pd.Series, max_lag: int = 24) -> dict:
    """
    Detect seasonality using autocorrelation.
    """
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.tsa.stattools import acf

    # Calculate autocorrelation
    acf_values = acf(data.dropna(), nlags=max_lag)

    # Find peaks (potential seasonal periods)
    peaks = []
    for i in range(1, len(acf_values) - 1):
        if acf_values[i] > acf_values[i-1] and acf_values[i] > acf_values[i+1]:
            if acf_values[i] > 0.3:  # Significant correlation
                peaks.append((i, acf_values[i]))

    return {
        'acf_values': acf_values,
        'seasonal_periods': [p[0] for p in sorted(peaks, key=lambda x: x[1], reverse=True)],
        'has_seasonality': len(peaks) > 0
    }
```

### 4. Machine Learning for Real Estate

**Property Valuation Model:**
```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

def train_valuation_model(
    df: pd.DataFrame,
    target: str = 'property_value',
    features: list = None
) -> dict:
    """
    Train property valuation model using ensemble methods.

    Returns trained model with performance metrics.
    """
    # Default features if not specified
    if features is None:
        features = [
            'square_feet', 'bedrooms', 'bathrooms', 'year_built',
            'lot_size', 'cap_rate', 'noi', 'occupancy_rate'
        ]

    # Prepare data
    X = df[features].fillna(df[features].median())
    y = df[target]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train XGBoost model
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )

    model.fit(X_train_scaled, y_train)

    # Evaluate
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)

    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5,
                                 scoring='r2')

    # Feature importance
    feature_importance = dict(zip(features, model.feature_importances_))
    sorted_importance = sorted(feature_importance.items(),
                              key=lambda x: x[1], reverse=True)

    # Predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate MAPE
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    return {
        'model': model,
        'scaler': scaler,
        'train_r2': round(train_score, 3),
        'test_r2': round(test_score, 3),
        'cv_mean_r2': round(cv_scores.mean(), 3),
        'cv_std_r2': round(cv_scores.std(), 3),
        'mape': round(mape, 2),
        'feature_importance': sorted_importance,
        'features': features
    }


# Example usage
model_results = train_valuation_model(properties_df)
print(f"Model R²: {model_results['test_r2']}")
print(f"MAPE: {model_results['mape']}%")
print("\nTop Features:")
for feature, importance in model_results['feature_importance'][:5]:
    print(f"  {feature}: {importance:.3f}")
```

**Clustering Analysis (Market Segmentation):**
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def market_segmentation(
    df: pd.DataFrame,
    features: list,
    n_clusters: int = 4
) -> dict:
    """
    Segment properties/markets into clusters.

    Useful for identifying similar property groups or market types.
    """
    # Prepare data
    X = df[features].fillna(df[features].median())

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    # Add clusters to dataframe
    df_clustered = df.copy()
    df_clustered['cluster'] = clusters

    # Analyze clusters
    cluster_profiles = []
    for i in range(n_clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == i]

        profile = {
            'cluster': i,
            'size': len(cluster_data),
            'percentage': round(len(cluster_data) / len(df) * 100, 1),
            'characteristics': {}
        }

        for feature in features:
            profile['characteristics'][feature] = {
                'mean': round(cluster_data[feature].mean(), 2),
                'median': round(cluster_data[feature].median(), 2),
                'std': round(cluster_data[feature].std(), 2)
            }

        cluster_profiles.append(profile)

    return {
        'clusters': clusters,
        'model': kmeans,
        'scaler': scaler,
        'profiles': cluster_profiles,
        'df_clustered': df_clustered
    }


# Example: Segment properties by characteristics
features = ['cap_rate', 'occupancy_rate', 'age', 'property_value']
segmentation = market_segmentation(properties_df, features, n_clusters=3)

print("\nMarket Segments:")
for profile in segmentation['profiles']:
    print(f"\nCluster {profile['cluster']}: {profile['size']} properties ({profile['percentage']}%)")
    print(f"  Avg Cap Rate: {profile['characteristics']['cap_rate']['mean']}%")
    print(f"  Avg Occupancy: {profile['characteristics']['occupancy_rate']['mean']}%")
```

**Anomaly Detection:**
```python
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

def detect_anomalies(
    df: pd.DataFrame,
    features: list,
    method: str = 'isolation_forest',
    contamination: float = 0.1
) -> dict:
    """
    Detect anomalous properties or transactions.

    Useful for:
    - Identifying data quality issues
    - Finding unusual deals
    - Detecting potential fraud
    """
    X = df[features].fillna(df[features].median())

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Choose method
    if method == 'isolation_forest':
        model = IsolationForest(contamination=contamination, random_state=42)
    else:
        model = EllipticEnvelope(contamination=contamination, random_state=42)

    # Detect anomalies (-1 = anomaly, 1 = normal)
    predictions = model.fit_predict(X_scaled)

    # Get anomaly scores
    anomaly_scores = model.score_samples(X_scaled)

    df_result = df.copy()
    df_result['is_anomaly'] = predictions == -1
    df_result['anomaly_score'] = anomaly_scores

    anomalies = df_result[df_result['is_anomaly']]

    return {
        'anomalies': anomalies,
        'n_anomalies': len(anomalies),
        'anomaly_percentage': round(len(anomalies) / len(df) * 100, 2),
        'model': model,
        'df_result': df_result
    }


# Example: Find unusual property transactions
features = ['price_per_sqft', 'cap_rate', 'days_on_market']
anomaly_results = detect_anomalies(transactions_df, features, contamination=0.05)

print(f"Found {anomaly_results['n_anomalies']} anomalies ({anomaly_results['anomaly_percentage']}%)")
print("\nTop Anomalies:")
print(anomaly_results['anomalies'].sort_values('anomaly_score').head())
```

### 5. Portfolio Analytics

**Portfolio Diversification Metrics:**
```python
def calculate_portfolio_metrics(holdings: pd.DataFrame) -> dict:
    """
    Calculate comprehensive portfolio analytics.

    Args:
        holdings: DataFrame with columns: property_id, value, noi, property_type, state
    """
    total_value = holdings['value'].sum()

    # Geographic diversification (Herfindahl-Hirschman Index)
    geo_distribution = holdings.groupby('state')['value'].sum() / total_value
    hhi_geo = (geo_distribution ** 2).sum()

    # Property type diversification
    type_distribution = holdings.groupby('property_type')['value'].sum() / total_value
    hhi_type = (type_distribution ** 2).sum()

    # Concentration risk
    top_5_concentration = holdings.nlargest(5, 'value')['value'].sum() / total_value

    # Weighted average metrics
    weighted_cap_rate = (holdings['noi'].sum() / holdings['value'].sum()) * 100

    return {
        'total_value': float(total_value),
        'property_count': len(holdings),
        'geographic_hhi': round(hhi_geo, 3),  # Lower = more diversified
        'property_type_hhi': round(hhi_type, 3),
        'top_5_concentration': round(top_5_concentration * 100, 2),
        'weighted_avg_cap_rate': round(weighted_cap_rate, 2),
        'geographic_distribution': geo_distribution.to_dict(),
        'property_type_distribution': type_distribution.to_dict()
    }
```

**Risk-Adjusted Returns:**
```python
def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.02
) -> float:
    """
    Calculate Sharpe Ratio.

    Sharpe = (Mean Return - Risk Free Rate) / Std Dev of Returns
    """
    excess_returns = returns - risk_free_rate
    return round(excess_returns.mean() / returns.std(), 2)


def calculate_sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.02
) -> float:
    """
    Calculate Sortino Ratio.

    Similar to Sharpe, but only considers downside volatility.
    """
    excess_returns = returns - risk_free_rate
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std()

    if downside_std == 0:
        return None

    return round(excess_returns.mean() / downside_std, 2)


def calculate_max_drawdown(values: pd.Series) -> dict:
    """
    Calculate maximum drawdown.

    Max drawdown = largest peak-to-trough decline
    """
    cumulative_max = values.expanding().max()
    drawdown = (values - cumulative_max) / cumulative_max

    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()

    return {
        'max_drawdown': round(max_dd * 100, 2),
        'max_drawdown_date': max_dd_date,
        'current_drawdown': round(drawdown.iloc[-1] * 100, 2)
    }
```

### 6. Market Intelligence & Comps Analysis

**Comparable Properties Analysis:**
```python
def find_comparables(
    target_property: dict,
    comp_pool: pd.DataFrame,
    n_comps: int = 5,
    weights: dict = None
) -> pd.DataFrame:
    """
    Find comparable properties using weighted similarity score.

    Args:
        target_property: Dictionary with property characteristics
        comp_pool: DataFrame of potential comps
        n_comps: Number of comparables to return
        weights: Dictionary of feature weights
    """
    from sklearn.metrics.pairwise import cosine_similarity

    if weights is None:
        weights = {
            'square_feet': 0.3,
            'bedrooms': 0.1,
            'year_built': 0.2,
            'location_score': 0.4
        }

    # Calculate similarity scores
    similarity_scores = []

    for idx, comp in comp_pool.iterrows():
        score = 0

        # Square feet similarity (normalized)
        if 'square_feet' in target_property:
            sqft_diff = abs(comp['square_feet'] - target_property['square_feet'])
            sqft_sim = 1 - min(sqft_diff / target_property['square_feet'], 1)
            score += weights.get('square_feet', 0) * sqft_sim

        # Bedroom similarity
        if 'bedrooms' in target_property:
            bed_diff = abs(comp['bedrooms'] - target_property['bedrooms'])
            bed_sim = 1 - min(bed_diff / 5, 1)  # Normalize by max diff of 5
            score += weights.get('bedrooms', 0) * bed_sim

        # Age similarity
        if 'year_built' in target_property:
            age_diff = abs(comp['year_built'] - target_property['year_built'])
            age_sim = 1 - min(age_diff / 50, 1)  # Normalize by 50 years
            score += weights.get('year_built', 0) * age_sim

        # Location similarity (assume pre-calculated)
        if 'location_score' in comp:
            score += weights.get('location_score', 0) * comp.get('location_score', 0.5)

        similarity_scores.append(score)

    comp_pool = comp_pool.copy()
    comp_pool['similarity_score'] = similarity_scores

    # Return top N comps
    return comp_pool.nlargest(n_comps, 'similarity_score')


# Example usage
target = {
    'square_feet': 2000,
    'bedrooms': 3,
    'year_built': 2015
}

comps = find_comparables(target, properties_df, n_comps=5)
print("\nTop Comparables:")
print(comps[['address', 'square_feet', 'year_built', 'similarity_score']])
```

**Market Trend Analysis:**
```python
def analyze_market_trends(
    transactions: pd.DataFrame,
    time_col: str = 'sale_date',
    value_col: str = 'price_per_sqft',
    geography_col: str = 'zip_code',
    periods: int = 12
) -> dict:
    """
    Analyze market trends by geography and time.
    """
    transactions = transactions.copy()
    transactions[time_col] = pd.to_datetime(transactions[time_col])
    transactions = transactions.set_index(time_col).sort_index()

    # Overall trend
    overall_trend = transactions.resample('M')[value_col].mean()

    # Calculate YoY growth
    yoy_growth = overall_trend.pct_change(periods=12) * 100

    # Geography-specific trends
    geo_trends = transactions.groupby([
        pd.Grouper(freq='M'),
        geography_col
    ])[value_col].mean().unstack()

    # Identify hot and cold markets
    recent_growth = {}
    for geo in geo_trends.columns:
        if len(geo_trends[geo].dropna()) >= periods:
            recent_values = geo_trends[geo].dropna()[-periods:]
            growth = ((recent_values.iloc[-1] - recent_values.iloc[0]) /
                     recent_values.iloc[0] * 100)
            recent_growth[geo] = round(growth, 2)

    hot_markets = sorted(recent_growth.items(), key=lambda x: x[1], reverse=True)[:5]
    cold_markets = sorted(recent_growth.items(), key=lambda x: x[1])[:5]

    return {
        'overall_trend': overall_trend,
        'yoy_growth': yoy_growth,
        'current_yoy': round(yoy_growth.iloc[-1], 2) if len(yoy_growth) > 0 else None,
        'hot_markets': hot_markets,
        'cold_markets': cold_markets,
        'geo_trends': geo_trends
    }
```

### 7. Insight Generation Framework

**Automated Insights:**
```python
def generate_insights(
    data: pd.DataFrame,
    metric: str,
    threshold_percentile: float = 90
) -> list:
    """
    Automatically generate data-driven insights.

    Returns list of insight dictionaries.
    """
    insights = []

    # 1. Outlier detection
    threshold = data[metric].quantile(threshold_percentile / 100)
    outliers = data[data[metric] > threshold]

    if len(outliers) > 0:
        insights.append({
            'type': 'outlier',
            'severity': 'high' if len(outliers) > len(data) * 0.2 else 'medium',
            'message': f"Found {len(outliers)} properties with {metric} above {threshold_percentile}th percentile",
            'recommendation': f"Investigate high-performing properties to identify success factors",
            'data': outliers.to_dict('records')[:5]
        })

    # 2. Trend detection
    if isinstance(data.index, pd.DatetimeIndex):
        trend_slope = np.polyfit(range(len(data)), data[metric], 1)[0]

        if abs(trend_slope) > data[metric].std() * 0.1:
            direction = "increasing" if trend_slope > 0 else "decreasing"
            insights.append({
                'type': 'trend',
                'severity': 'high',
                'message': f"{metric} is {direction} over time",
                'recommendation': f"Monitor {metric} trend and adjust strategy accordingly",
                'trend_slope': round(float(trend_slope), 2)
            })

    # 3. Concentration risk
    if 'property_type' in data.columns or 'state' in data.columns:
        group_col = 'property_type' if 'property_type' in data.columns else 'state'
        concentration = data.groupby(group_col)[metric].count() / len(data)
        max_concentration = concentration.max()

        if max_concentration > 0.4:  # More than 40% in one group
            insights.append({
                'type': 'concentration_risk',
                'severity': 'high',
                'message': f"High concentration: {max_concentration*100:.1f}% in one {group_col}",
                'recommendation': "Consider diversifying across more categories",
                'distribution': concentration.to_dict()
            })

    # 4. Performance gaps
    if len(data) > 1:
        top_quartile = data[metric].quantile(0.75)
        bottom_quartile = data[metric].quantile(0.25)
        gap = top_quartile - bottom_quartile

        insights.append({
            'type': 'performance_gap',
            'severity': 'medium',
            'message': f"Performance gap: {gap:.2f} between top and bottom quartiles",
            'recommendation': "Analyze top performers to improve bottom performers",
            'top_quartile': float(top_quartile),
            'bottom_quartile': float(bottom_quartile)
        })

    return insights


# Example usage
insights = generate_insights(properties_df, metric='cap_rate')
for insight in insights:
    print(f"\n[{insight['severity'].upper()}] {insight['type']}")
    print(f"  {insight['message']}")
    print(f"  → {insight['recommendation']}")
```

### 8. Data Visualization Strategies

**Professional Chart Configurations:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_performance_dashboard(df: pd.DataFrame) -> None:
    """
    Create comprehensive performance dashboard.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Portfolio Performance Dashboard', fontsize=16, fontweight='bold')

    # 1. Time series of portfolio value
    ax1 = axes[0, 0]
    df.groupby('date')['property_value'].sum().plot(ax=ax1, linewidth=2)
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Value ($)')
    ax1.grid(True, alpha=0.3)

    # 2. Distribution of cap rates
    ax2 = axes[0, 1]
    df['cap_rate'].hist(bins=20, ax=ax2, edgecolor='black', alpha=0.7)
    ax2.axvline(df['cap_rate'].median(), color='red', linestyle='--',
                label=f'Median: {df["cap_rate"].median():.2f}%')
    ax2.set_title('Cap Rate Distribution')
    ax2.set_xlabel('Cap Rate (%)')
    ax2.set_ylabel('Frequency')
    ax2.legend()

    # 3. Geographic distribution
    ax3 = axes[1, 0]
    geo_dist = df.groupby('state')['property_value'].sum().sort_values(ascending=False).head(10)
    geo_dist.plot(kind='barh', ax=ax3)
    ax3.set_title('Top 10 States by Portfolio Value')
    ax3.set_xlabel('Total Value ($)')

    # 4. Scatter: NOI vs Value
    ax4 = axes[1, 1]
    ax4.scatter(df['property_value'], df['noi'], alpha=0.6)
    ax4.set_title('NOI vs Property Value')
    ax4.set_xlabel('Property Value ($)')
    ax4.set_ylabel('NOI ($)')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
```

## Analysis Workflow Checklist

When performing data analysis:

### Data Preparation
- [ ] Load and inspect data (shape, dtypes, missing values)
- [ ] Handle missing values appropriately
- [ ] Detect and handle outliers
- [ ] Validate data quality and consistency
- [ ] Transform/normalize as needed
- [ ] Create derived features

### Exploratory Analysis
- [ ] Calculate descriptive statistics
- [ ] Visualize distributions
- [ ] Check for correlations
- [ ] Identify trends and patterns
- [ ] Segment data by relevant dimensions
- [ ] Generate initial hypotheses

### Statistical Testing
- [ ] Test assumptions (normality, homogeneity)
- [ ] Choose appropriate tests
- [ ] Calculate test statistics and p-values
- [ ] Interpret results with effect sizes
- [ ] Consider multiple testing corrections
- [ ] Document limitations

### Modeling (if applicable)
- [ ] Split data (train/test)
- [ ] Select appropriate algorithm
- [ ] Train model with cross-validation
- [ ] Evaluate performance metrics
- [ ] Analyze feature importance
- [ ] Test on holdout set
- [ ] Document model assumptions

### Insight Generation
- [ ] Identify key findings
- [ ] Quantify impact/magnitude
- [ ] Provide context and comparisons
- [ ] Generate actionable recommendations
- [ ] Consider business constraints
- [ ] Estimate confidence levels

### Communication
- [ ] Create clear visualizations
- [ ] Write executive summary
- [ ] Document methodology
- [ ] Highlight limitations
- [ ] Provide next steps
- [ ] Prepare for questions

## Best Practices

**Data Quality:**
- Always validate data before analysis
- Document data sources and assumptions
- Handle missing data transparently
- Flag outliers but investigate before removing

**Statistical Rigor:**
- Report confidence intervals, not just point estimates
- Use appropriate significance levels
- Consider effect sizes, not just p-values
- Avoid p-hacking and data dredging

**Model Development:**
- Start simple, add complexity only if needed
- Always use train/test split
- Cross-validate to avoid overfitting
- Monitor model performance over time

**Communication:**
- Lead with insights, not methods
- Use visualizations to tell stories
- Provide context for all numbers
- Make recommendations actionable

## Quick Reference

**Key Formulas:**
```python
# IRR: Rate where NPV = 0
irr_value = irr(cash_flows)

# Cap Rate = NOI / Property Value
cap_rate = (noi / property_value) * 100

# DSCR = NOI / Annual Debt Service
dscr = noi / annual_debt_service

# LTV = Loan Amount / Property Value
ltv = (loan_amount / property_value) * 100

# Sharpe Ratio = (Return - Risk Free) / Std Dev
sharpe = (returns.mean() - rf_rate) / returns.std()
```

**Statistical Tests:**
- t-test: Compare means of two groups (normal data)
- Mann-Whitney U: Compare medians (non-normal data)
- Chi-square: Test categorical associations
- ANOVA: Compare means of 3+ groups
- Correlation: Measure linear relationships

**Model Selection:**
- Linear Regression: Simple relationships, interpretability
- Random Forest: Non-linear, feature importance
- XGBoost: Best performance, handles missing data
- Time Series: ARIMA, Exponential Smoothing

---

## Final Notes

This skill provides a **comprehensive framework for professional data analysis** in real estate financial analytics. Always prioritize:

1. **Business context** - Analysis serves business decisions
2. **Statistical rigor** - Use appropriate methods
3. **Actionable insights** - Focus on what to do, not just what is
4. **Clear communication** - Make complexity accessible
5. **Reproducibility** - Document everything
6. **Continuous learning** - Stay current with methods

When in doubt, start with simple descriptive analysis, visualize the data, and build complexity only as needed. The best analysis is one that drives better decisions.
