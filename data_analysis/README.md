# Advanced Data Analysis Package

A comprehensive suite of tools for data analysis, forecasting, trend identification, predictive modeling, and visualization.

## Features

### Core Components

- **Data Preprocessing**: Cleaning, transformation, missing value handling, outlier detection
- **Feature Engineering**: Lag features, rolling statistics, interactions, target encoding

### Forecasting

- **Time Series Models**: ARIMA, SARIMA, Prophet, LSTM, Exponential Smoothing
- **Ensemble Methods**: Simple averaging, weighted averaging, optimal weights, stacking

### Trend Analysis

- **Trend Detection**: Linear regression, Mann-Kendall test, Sen's slope
- **Change Point Detection**: CUSUM, PELT, Binary Segmentation
- **Seasonality Detection**: Autocorrelation analysis, decomposition

### Anomaly Detection

- **Statistical Methods**: Z-score, IQR, MAD
- **Machine Learning**: Isolation Forest, LOF, DBSCAN, One-Class SVM
- **Deep Learning**: Autoencoder-based detection

### Predictive Modeling

- **ML Models**: XGBoost, Random Forest, Gradient Boosting, LightGBM, CatBoost
- **Neural Networks**: MLP, LSTM, GRU, CNN, Transformer
- **Model Comparison**: Automated evaluation and ranking

### Projections

- **Scenario Analysis**: Baseline, optimistic, pessimistic scenarios
- **Monte Carlo Simulation**: GBM, mean-reverting, jump-diffusion processes
- **Risk Metrics**: VaR, CVaR, percentiles

### Visualization

- **Advanced Charts**: Time series, forecasts, anomalies, feature importance
- **Dashboard Generation**: HTML reports with key metrics and insights

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from data_analysis.main import run_quick_analysis
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Run comprehensive analysis
results = run_quick_analysis(df, target_column='value', date_column='date')
```

## Module Usage

### Forecasting

```python
from data_analysis.forecasting import TimeSeriesForecaster

forecaster = TimeSeriesForecaster()
forecaster.fit_arima(series, auto_order=True)
forecast = forecaster.forecast('arima', periods=30)
```

### Anomaly Detection

```python
from data_analysis.trends import AnomalyDetector

detector = AnomalyDetector()
result = detector.detect_isolation_forest(data, contamination=0.05)
anomalies = result['anomaly_indices']
```

### ML Prediction

```python
from data_analysis.predictive import MLPredictor

predictor = MLPredictor()
predictor.train_xgboost(X_train, y_train)
comparison = predictor.compare_models(X_test, y_test)
```

### Monte Carlo Simulation

```python
from data_analysis.projections import MonteCarloSimulator

mc = MonteCarloSimulator(n_simulations=10000)
risk_analysis = mc.run_risk_analysis(
    initial_value=100,
    drift=0.001,
    volatility=0.02,
    periods=30
)
```

## Run Complete Example

```bash
python -m data_analysis.examples.complete_example
```

## Structure

```
data_analysis/
├── core/
│   ├── data_preprocessor.py
│   ├── feature_engineering.py
│   └── utils.py
├── forecasting/
│   ├── time_series_forecaster.py
│   └── ensemble_forecaster.py
├── trends/
│   ├── trend_detector.py
│   └── anomaly_detector.py
├── predictive/
│   ├── ml_predictor.py
│   └── neural_predictor.py
├── visualization/
│   ├── advanced_charts.py
│   └── dashboard_generator.py
├── projections/
│   ├── scenario_analyzer.py
│   └── monte_carlo.py
├── examples/
│   └── complete_example.py
├── main.py
└── requirements.txt
```

## License

MIT License
