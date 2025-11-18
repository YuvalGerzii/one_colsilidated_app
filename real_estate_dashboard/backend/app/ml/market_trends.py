"""
Market Trend Forecasting Module

Uses time series analysis and ML to forecast:
- Property price trends
- Market inventory levels
- Days on market predictions
- Market absorption rates
"""

import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)


class MarketTrendForecaster:
    """
    Forecast real estate market trends using time series analysis.

    Combines classical time series methods (ARIMA, Exponential Smoothing)
    with gradient boosting for robust predictions.
    """

    def __init__(self):
        """Initialize the market trend forecaster."""
        self.models = {}
        self.metrics = {}

    def prepare_time_series(
        self,
        data: List[Dict],
        date_column: str = 'date',
        value_column: str = 'median_price'
    ) -> pd.DataFrame:
        """
        Prepare time series data.

        Args:
            data: List of dictionaries with date and value columns
            date_column: Name of date column
            value_column: Name of value column to forecast

        Returns:
            DataFrame with datetime index
        """
        df = pd.DataFrame(data)
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.set_index(date_column)
        df = df.sort_index()

        # Handle missing values
        if df[value_column].isna().any():
            df[value_column] = df[value_column].interpolate(method='linear')

        return df[[value_column]]

    def forecast_with_arima(
        self,
        data: pd.Series,
        periods: int = 12,
        order: Tuple[int, int, int] = (1, 1, 1)
    ) -> Dict[str, any]:
        """
        Forecast using ARIMA model.

        Args:
            data: Time series data
            periods: Number of periods to forecast
            order: ARIMA order (p, d, q)

        Returns:
            Dictionary with forecasts and confidence intervals
        """
        try:
            model = ARIMA(data, order=order)
            fitted_model = model.fit()

            # Forecast
            forecast_result = fitted_model.forecast(steps=periods)
            conf_int = fitted_model.get_forecast(steps=periods).conf_int()

            return {
                'forecast': forecast_result.tolist(),
                'lower_bound': conf_int.iloc[:, 0].tolist(),
                'upper_bound': conf_int.iloc[:, 1].tolist(),
                'method': 'ARIMA',
                'aic': fitted_model.aic,
                'bic': fitted_model.bic
            }
        except Exception as e:
            logger.error(f"ARIMA forecast failed: {e}")
            return None

    def forecast_with_exponential_smoothing(
        self,
        data: pd.Series,
        periods: int = 12,
        seasonal_periods: int = 12
    ) -> Dict[str, any]:
        """
        Forecast using Exponential Smoothing (Holt-Winters).

        Args:
            data: Time series data
            periods: Number of periods to forecast
            seasonal_periods: Length of seasonal cycle

        Returns:
            Dictionary with forecasts
        """
        try:
            # Ensure we have enough data for seasonality
            if len(data) < 2 * seasonal_periods:
                seasonal_periods = None

            model = ExponentialSmoothing(
                data,
                seasonal_periods=seasonal_periods,
                trend='add',
                seasonal='add' if seasonal_periods else None
            )
            fitted_model = model.fit()

            # Forecast
            forecast = fitted_model.forecast(periods)

            return {
                'forecast': forecast.tolist(),
                'method': 'Exponential Smoothing',
                'seasonal_periods': seasonal_periods
            }
        except Exception as e:
            logger.error(f"Exponential Smoothing forecast failed: {e}")
            return None

    def forecast_with_gradient_boosting(
        self,
        data: pd.Series,
        periods: int = 12,
        lag_features: int = 12
    ) -> Dict[str, any]:
        """
        Forecast using Gradient Boosting with lag features.

        Args:
            data: Time series data
            periods: Number of periods to forecast
            lag_features: Number of lag features to use

        Returns:
            Dictionary with forecasts
        """
        try:
            # Create lag features
            df = pd.DataFrame({'value': data})

            for i in range(1, lag_features + 1):
                df[f'lag_{i}'] = df['value'].shift(i)

            # Add time-based features
            df['month'] = data.index.month
            df['quarter'] = data.index.quarter

            # Remove NaN rows
            df = df.dropna()

            # Prepare training data
            X = df.drop('value', axis=1)
            y = df['value']

            # Train model
            model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            model.fit(X, y)

            # Forecast
            forecasts = []
            last_values = data.tail(lag_features).tolist()

            for _ in range(periods):
                # Create feature vector
                features = last_values[-lag_features:]
                # Add time features (simplified)
                month = (data.index[-1].month + len(forecasts)) % 12 + 1
                quarter = (month - 1) // 3 + 1
                features.extend([month, quarter])

                # Predict
                pred = model.predict([features])[0]
                forecasts.append(pred)
                last_values.append(pred)

            return {
                'forecast': forecasts,
                'method': 'Gradient Boosting',
                'feature_importance': dict(zip(X.columns, model.feature_importances_.tolist()))
            }
        except Exception as e:
            logger.error(f"Gradient Boosting forecast failed: {e}")
            return None

    def forecast(
        self,
        data: List[Dict],
        periods: int = 12,
        date_column: str = 'date',
        value_column: str = 'median_price',
        methods: List[str] = ['arima', 'exponential_smoothing', 'gradient_boosting']
    ) -> Dict[str, any]:
        """
        Generate ensemble forecast using multiple methods.

        Args:
            data: Historical time series data
            periods: Number of periods to forecast
            date_column: Name of date column
            value_column: Name of value column
            methods: List of methods to use

        Returns:
            Dictionary with ensemble forecasts and individual method results
        """
        logger.info(f"Forecasting {periods} periods using {len(methods)} methods")

        # Prepare data
        ts_data = self.prepare_time_series(data, date_column, value_column)
        series = ts_data[value_column]

        results = {
            'historical': {
                'dates': ts_data.index.strftime('%Y-%m-%d').tolist(),
                'values': series.tolist()
            },
            'forecasts': {},
            'ensemble': None
        }

        # Generate forecast dates
        last_date = ts_data.index[-1]
        forecast_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=periods,
            freq='MS'
        )
        results['forecast_dates'] = forecast_dates.strftime('%Y-%m-%d').tolist()

        # Run each method
        all_forecasts = []

        if 'arima' in methods:
            arima_result = self.forecast_with_arima(series, periods)
            if arima_result:
                results['forecasts']['arima'] = arima_result
                all_forecasts.append(arima_result['forecast'])

        if 'exponential_smoothing' in methods:
            es_result = self.forecast_with_exponential_smoothing(series, periods)
            if es_result:
                results['forecasts']['exponential_smoothing'] = es_result
                all_forecasts.append(es_result['forecast'])

        if 'gradient_boosting' in methods:
            gb_result = self.forecast_with_gradient_boosting(series, periods)
            if gb_result:
                results['forecasts']['gradient_boosting'] = gb_result
                all_forecasts.append(gb_result['forecast'])

        # Create ensemble forecast (average of all methods)
        if all_forecasts:
            ensemble_forecast = np.mean(all_forecasts, axis=0)
            ensemble_std = np.std(all_forecasts, axis=0)

            results['ensemble'] = {
                'forecast': ensemble_forecast.tolist(),
                'lower_bound': (ensemble_forecast - 1.96 * ensemble_std).tolist(),
                'upper_bound': (ensemble_forecast + 1.96 * ensemble_std).tolist(),
                'std_dev': ensemble_std.tolist()
            }

        return results

    def analyze_trend(
        self,
        data: List[Dict],
        date_column: str = 'date',
        value_column: str = 'median_price'
    ) -> Dict[str, any]:
        """
        Analyze historical trends.

        Args:
            data: Historical time series data
            date_column: Name of date column
            value_column: Name of value column

        Returns:
            Dictionary with trend analysis
        """
        ts_data = self.prepare_time_series(data, date_column, value_column)
        series = ts_data[value_column]

        # Calculate statistics
        analysis = {
            'current_value': float(series.iloc[-1]),
            'mean': float(series.mean()),
            'median': float(series.median()),
            'std_dev': float(series.std()),
            'min': float(series.min()),
            'max': float(series.max()),
        }

        # Calculate growth rates
        analysis['growth_1m'] = float((series.iloc[-1] / series.iloc[-2] - 1) * 100) if len(series) > 1 else 0
        analysis['growth_3m'] = float((series.iloc[-1] / series.iloc[-4] - 1) * 100) if len(series) > 3 else 0
        analysis['growth_12m'] = float((series.iloc[-1] / series.iloc[-13] - 1) * 100) if len(series) > 12 else 0

        # Trend direction
        if len(series) >= 6:
            recent_trend = np.polyfit(range(6), series.tail(6).values, 1)[0]
            analysis['trend_direction'] = 'increasing' if recent_trend > 0 else 'decreasing'
            analysis['trend_strength'] = float(abs(recent_trend))
        else:
            analysis['trend_direction'] = 'insufficient_data'
            analysis['trend_strength'] = 0.0

        # Volatility
        returns = series.pct_change().dropna()
        analysis['volatility'] = float(returns.std() * np.sqrt(12))  # Annualized

        return analysis


def generate_sample_market_data(periods: int = 48) -> List[Dict]:
    """
    Generate synthetic market trend data for demonstration.

    Args:
        periods: Number of months of data to generate

    Returns:
        List of dictionaries with date and market metrics
    """
    np.random.seed(42)

    start_date = pd.Timestamp('2020-01-01')
    dates = pd.date_range(start=start_date, periods=periods, freq='MS')

    data = []
    base_price = 350000
    trend = 0

    for i, date in enumerate(dates):
        # Add trend, seasonality, and noise
        trend += np.random.normal(1000, 500)  # Upward trend with noise
        seasonal = 10000 * np.sin(2 * np.pi * i / 12)  # Annual seasonality
        noise = np.random.normal(0, 5000)

        price = base_price + trend + seasonal + noise

        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'median_price': max(price, 100000),  # Floor price
            'inventory': np.random.randint(1000, 5000),
            'days_on_market': np.random.randint(20, 80)
        })

    return data
