#!/usr/bin/env python3
"""
Complete Data Analysis Example
===============================

Demonstrates all capabilities of the data analysis package.
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_analysis.core.data_preprocessor import DataPreprocessor
from data_analysis.core.feature_engineering import FeatureEngineer
from data_analysis.core.utils import DataAnalysisUtils
from data_analysis.forecasting.time_series_forecaster import TimeSeriesForecaster
from data_analysis.forecasting.ensemble_forecaster import EnsembleForecaster
from data_analysis.trends.trend_detector import TrendDetector
from data_analysis.trends.anomaly_detector import AnomalyDetector
from data_analysis.predictive.ml_predictor import MLPredictor
from data_analysis.projections.scenario_analyzer import ScenarioAnalyzer
from data_analysis.projections.monte_carlo import MonteCarloSimulator


def generate_sample_data(n_samples: int = 500) -> pd.DataFrame:
    """Generate sample financial time series data."""
    np.random.seed(42)

    dates = pd.date_range('2022-01-01', periods=n_samples, freq='D')

    # Generate price with trend and seasonality
    trend = np.linspace(100, 150, n_samples)
    seasonality = 10 * np.sin(2 * np.pi * np.arange(n_samples) / 365)
    noise = np.random.randn(n_samples) * 3

    price = trend + seasonality + noise

    # Add some anomalies
    anomaly_indices = [50, 150, 300, 400]
    for idx in anomaly_indices:
        price[idx] += np.random.choice([-20, 20])

    # Generate related features
    volume = np.random.randint(10000, 100000, n_samples)
    volatility = np.abs(np.random.randn(n_samples)) * 0.02

    return pd.DataFrame({
        'date': dates,
        'price': price,
        'volume': volume,
        'volatility': volatility
    })


def example_preprocessing():
    """Example: Data Preprocessing."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: DATA PREPROCESSING")
    print("=" * 60)

    # Generate data
    df = generate_sample_data()
    df.loc[10:20, 'price'] = np.nan  # Add missing values

    # Initialize preprocessor
    preprocessor = DataPreprocessor()

    # Analyze data quality
    quality = preprocessor.analyze_data_quality(df)
    print(f"\nData Quality Report:")
    print(f"  - Total rows: {quality['total_rows']}")
    print(f"  - Missing values in 'price': {quality['columns']['price']['missing_count']}")

    # Handle missing values
    df_clean = preprocessor.handle_missing_values(df, strategy='auto')
    print(f"\nAfter handling missing values:")
    print(f"  - Missing in 'price': {df_clean['price'].isna().sum()}")

    # Create time features
    df_features = preprocessor.create_time_features(df_clean, 'date')
    print(f"\nAdded time features: {[c for c in df_features.columns if c not in df.columns]}")

    return df_features


def example_feature_engineering():
    """Example: Feature Engineering."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: FEATURE ENGINEERING")
    print("=" * 60)

    df = generate_sample_data()
    engineer = FeatureEngineer()

    # Create lag features
    df = engineer.create_lag_features(df, ['price'], lags=[1, 7, 30])
    print(f"\nCreated lag features: {len([c for c in df.columns if 'lag' in c])}")

    # Create rolling features
    df = engineer.create_rolling_features(
        df, ['price'],
        windows=[7, 30],
        functions=['mean', 'std']
    )
    print(f"Created rolling features: {len([c for c in df.columns if 'rolling' in c])}")

    # Create diff features
    df = engineer.create_diff_features(df, ['price'], periods=[1, 7])
    print(f"Created diff features: {len([c for c in df.columns if 'diff' in c])}")

    print(f"\nTotal features created: {len(engineer.get_created_features())}")

    return df


def example_forecasting():
    """Example: Time Series Forecasting."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: TIME SERIES FORECASTING")
    print("=" * 60)

    df = generate_sample_data()
    series = pd.Series(df['price'].values, index=df['date'])

    forecaster = TimeSeriesForecaster()
    ensemble = EnsembleForecaster()

    # Fit ARIMA
    print("\nFitting ARIMA model...")
    arima_result = forecaster.fit_arima(series, auto_order=True)
    if 'error' not in arima_result:
        print(f"  - Order: {arima_result['order']}")
        print(f"  - AIC: {arima_result['aic']}")

        # Generate forecast
        forecast = forecaster.forecast('arima', 30)
        ensemble.add_forecast('arima', forecast['forecast'])
        print(f"  - Forecast mean: {np.mean(forecast['forecast']):.2f}")

    # Fit Exponential Smoothing
    print("\nFitting Exponential Smoothing...")
    es_result = forecaster.fit_exponential_smoothing(series)
    if 'error' not in es_result:
        print(f"  - AIC: {es_result['aic']}")

        forecast = forecaster.forecast('exp_smoothing', 30)
        ensemble.add_forecast('exp_smoothing', forecast['forecast'])

    # Ensemble forecast
    print("\nCreating ensemble forecast...")
    ensemble_forecast = ensemble.simple_average()
    print(f"  - Ensemble mean: {np.mean(ensemble_forecast):.2f}")
    print(f"  - Model weights: {ensemble.get_weights()}")

    return ensemble_forecast


def example_trend_detection():
    """Example: Trend Detection."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: TREND DETECTION")
    print("=" * 60)

    df = generate_sample_data()
    series = pd.Series(df['price'].values, index=df['date'])

    detector = TrendDetector()

    # Linear trend
    linear = detector.detect_linear_trend(series)
    print(f"\nLinear Trend Analysis:")
    print(f"  - Direction: {linear['trend']}")
    print(f"  - Slope: {linear['slope']:.6f}")
    print(f"  - R²: {linear['r_squared']}")

    # Mann-Kendall test
    mk = detector.mann_kendall_test(series)
    print(f"\nMann-Kendall Test:")
    print(f"  - Trend: {mk['trend']}")
    print(f"  - Z-statistic: {mk['z_statistic']}")
    print(f"  - P-value: {mk['p_value']}")

    # Seasonality detection
    seasonality = detector.detect_seasonality(series)
    print(f"\nSeasonality Analysis:")
    print(f"  - Has seasonality: {seasonality['has_seasonality']}")
    print(f"  - Type: {seasonality['seasonality_type']}")
    if seasonality['seasonal_periods']:
        print(f"  - Periods: {seasonality['seasonal_periods']}")

    # Change point detection
    change_points = detector.detect_change_points_cusum(series)
    print(f"\nChange Points: {len(change_points)} detected")

    return detector.get_trend_summary(series)


def example_anomaly_detection():
    """Example: Anomaly Detection."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: ANOMALY DETECTION")
    print("=" * 60)

    df = generate_sample_data()
    series = pd.Series(df['price'].values, index=df['date'])

    detector = AnomalyDetector()

    # Z-score method
    zscore = detector.detect_statistical_anomalies(series, method='zscore', threshold=3.0)
    print(f"\nZ-Score Method:")
    print(f"  - Anomalies: {zscore['n_anomalies']}")

    # IQR method
    iqr = detector.detect_statistical_anomalies(series, method='iqr', threshold=1.5)
    print(f"\nIQR Method:")
    print(f"  - Anomalies: {iqr['n_anomalies']}")

    # Rolling statistics
    rolling = detector.detect_time_series_anomalies(series, window=30)
    print(f"\nRolling Statistics Method:")
    print(f"  - Anomalies: {rolling['n_anomalies']}")

    # Isolation Forest
    iso = detector.detect_isolation_forest(series.values, contamination=0.05)
    print(f"\nIsolation Forest:")
    print(f"  - Anomalies: {iso['n_anomalies']}")

    # Ensemble detection
    print("\nEnsemble Detection:")
    ensemble = detector.ensemble_detection(series.values, voting='majority')
    print(f"  - Combined anomalies: {ensemble['n_anomalies']}")
    print(f"  - Per method: {ensemble['per_method_counts']}")

    return detector.get_anomaly_summary(series)


def example_ml_prediction():
    """Example: ML Prediction."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: ML PREDICTION")
    print("=" * 60)

    # Prepare data
    df = generate_sample_data()
    engineer = FeatureEngineer()

    # Create features
    df = engineer.create_lag_features(df, ['price'], lags=[1, 7, 14])
    df = engineer.create_rolling_features(df, ['price'], windows=[7, 14], functions=['mean', 'std'])
    df = df.dropna()

    # Prepare X, y
    feature_cols = [c for c in df.columns if c not in ['date', 'price']]
    X = df[feature_cols].values
    y = df['price'].values

    # Train/test split
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    predictor = MLPredictor()

    # Train models
    print("\nTraining XGBoost...")
    xgb_result = predictor.train_xgboost(X_train, y_train)
    if 'error' not in xgb_result:
        print(f"  - Features: {xgb_result['n_features']}")

    print("Training Random Forest...")
    rf_result = predictor.train_random_forest(X_train, y_train)

    print("Training Gradient Boosting...")
    gb_result = predictor.train_gradient_boosting(X_train, y_train)

    # Compare models
    print("\nModel Comparison:")
    comparison = predictor.compare_models(X_test, y_test)
    print(comparison.to_string(index=False))

    # Best model
    best = predictor.get_best_model(X_test, y_test)
    print(f"\nBest model: {best}")

    return comparison


def example_scenario_analysis():
    """Example: Scenario Analysis."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: SCENARIO ANALYSIS")
    print("=" * 60)

    df = generate_sample_data()
    series = pd.Series(df['price'].values)

    analyzer = ScenarioAnalyzer()

    # Create baseline
    baseline = analyzer.create_baseline_scenario(series)
    print(f"\nBaseline Scenario:")
    print(f"  - Base value: {baseline['base_value']:.2f}")
    print(f"  - Growth rate: {baseline['growth_rate']*100:.2f}%")
    print(f"  - Volatility: {baseline['volatility']:.4f}")

    # Create variants
    variants = analyzer.create_scenario_variants()
    print(f"\nCreated {len(variants)} scenario variants")

    # Compare scenarios
    comparison = analyzer.compare_scenarios(periods=30)
    print("\nScenario Comparison:")
    print(comparison.to_string(index=False))

    # Sensitivity analysis
    sensitivity = analyzer.sensitivity_analysis('baseline', 'growth_rate', periods=30)
    print(f"\nSensitivity to growth_rate: {sensitivity['sensitivity']:.2f}%")

    return comparison


def example_monte_carlo():
    """Example: Monte Carlo Simulation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: MONTE CARLO SIMULATION")
    print("=" * 60)

    df = generate_sample_data()
    series = pd.Series(df['price'].values)

    # Calculate parameters
    returns = series.pct_change().dropna()
    drift = returns.mean()
    volatility = returns.std()
    initial = series.iloc[-1]

    simulator = MonteCarloSimulator(n_simulations=10000)

    # Run simulation
    print(f"\nRunning {simulator.n_simulations:,} simulations...")
    paths = simulator.simulate_geometric_brownian_motion(
        initial_value=initial,
        drift=drift,
        volatility=volatility,
        periods=30
    )

    # Get statistics
    stats = simulator.get_statistics()
    print(f"\nSimulation Statistics (30-day horizon):")
    print(f"  - Mean: {stats['mean']:.2f}")
    print(f"  - Std: {stats['std']:.2f}")
    print(f"  - Min: {stats['min']:.2f}")
    print(f"  - Max: {stats['max']:.2f}")

    # Risk metrics
    var = simulator.calculate_var(0.95)
    cvar = simulator.calculate_cvar(0.95)
    print(f"\nRisk Metrics:")
    print(f"  - VaR (95%): {var*100:.2f}%")
    print(f"  - CVaR (95%): {cvar*100:.2f}%")

    # Percentiles
    percentiles = simulator.get_percentiles([5, 25, 50, 75, 95])
    print(f"\nPercentiles:")
    for p, v in percentiles.items():
        print(f"  - P{p}: {v:.2f}")

    # Probability analysis
    prob_profit = simulator.get_probability_of_target(initial, 'above')
    print(f"\nProbability of profit: {prob_profit*100:.1f}%")

    return simulator.get_statistics()


def main():
    """Run all examples."""
    print("=" * 60)
    print("DATA ANALYSIS PACKAGE - COMPLETE EXAMPLES")
    print("=" * 60)

    # Run all examples
    example_preprocessing()
    example_feature_engineering()
    example_forecasting()
    example_trend_detection()
    example_anomaly_detection()
    example_ml_prediction()
    example_scenario_analysis()
    example_monte_carlo()

    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == '__main__':
    main()
