"""
Advanced Data Analysis Package
==============================

A comprehensive suite of tools for data analysis, forecasting,
trend identification, predictive modeling, and visualization.

Modules:
    - core: Data preprocessing, feature engineering, utilities
    - forecasting: Time series forecasting (ARIMA, Prophet, LSTM, Ensemble)
    - trends: Trend detection, change point analysis, anomaly detection
    - predictive: Machine learning predictive models (XGBoost, RF, Neural Networks)
    - visualization: Advanced visualization and dashboards
    - projections: Scenario analysis, Monte Carlo simulations

Author: Data Science Team
Version: 1.0.0
"""

from .core import data_preprocessor, feature_engineering, utils
from .forecasting import time_series_forecaster, ensemble_forecaster
from .trends import trend_detector, anomaly_detector
from .predictive import ml_predictor, neural_predictor
from .visualization import advanced_charts, dashboard_generator
from .projections import scenario_analyzer, monte_carlo

__version__ = "1.0.0"
__all__ = [
    "data_preprocessor",
    "feature_engineering",
    "utils",
    "time_series_forecaster",
    "ensemble_forecaster",
    "trend_detector",
    "anomaly_detector",
    "ml_predictor",
    "neural_predictor",
    "advanced_charts",
    "dashboard_generator",
    "scenario_analyzer",
    "monte_carlo"
]
