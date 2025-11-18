"""
Advanced Forecasting Algorithms
================================

State-of-the-art forecasting methods including Theta, TBATS,
and hybrid approaches.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from scipy.optimize import minimize
import warnings

warnings.filterwarnings('ignore')


class AdvancedForecaster:
    """
    Advanced forecasting algorithms beyond standard methods.
    """

    def __init__(self):
        self.models = {}
        self.forecasts = {}

    def theta_method(
        self,
        series: pd.Series,
        periods: int,
        theta: float = 2.0
    ) -> Dict:
        """
        Theta method - decomposes series into theta lines.

        Simple yet powerful method that won M3 competition.

        Args:
            series: Time series data
            periods: Forecast horizon
            theta: Theta parameter (default 2.0)

        Returns:
            Forecast results
        """
        n = len(series)
        y = series.values

        # Calculate trend using linear regression
        x = np.arange(n)
        slope, intercept, _, _, _ = stats.linregress(x, y)

        # Create theta lines
        # Theta=0 line (linear regression)
        theta0 = intercept + slope * x

        # Theta=2 line (amplified curvature)
        theta2 = theta * y - (theta - 1) * theta0

        # Forecast theta=0 (extrapolate linear trend)
        x_future = np.arange(n, n + periods)
        theta0_forecast = intercept + slope * x_future

        # Forecast theta=2 using Simple Exponential Smoothing
        alpha = self._optimize_ses_alpha(theta2)
        ses_level = theta2[-1]
        theta2_forecast = np.full(periods, ses_level)

        # Combine forecasts (average of theta lines)
        forecast = (theta0_forecast + theta2_forecast) / 2

        self.forecasts['theta'] = forecast
        return {
            'forecast': forecast,
            'theta': theta,
            'alpha': round(alpha, 4),
            'slope': round(slope, 6)
        }

    def _optimize_ses_alpha(self, series: np.ndarray) -> float:
        """Optimize SES alpha parameter."""
        def ses_sse(alpha):
            n = len(series)
            level = series[0]
            sse = 0
            for i in range(1, n):
                forecast = level
                error = series[i] - forecast
                sse += error ** 2
                level = alpha * series[i] + (1 - alpha) * level
            return sse

        result = minimize(ses_sse, 0.5, bounds=[(0.01, 0.99)])
        return result.x[0]

    def damped_trend(
        self,
        series: pd.Series,
        periods: int,
        alpha: float = None,
        beta: float = None,
        phi: float = 0.98
    ) -> Dict:
        """
        Damped trend exponential smoothing.

        Args:
            series: Time series
            periods: Forecast horizon
            alpha: Level smoothing
            beta: Trend smoothing
            phi: Damping parameter

        Returns:
            Forecast results
        """
        y = series.values
        n = len(y)

        # Optimize parameters if not provided
        if alpha is None or beta is None:
            alpha, beta = self._optimize_holt_params(y, phi)

        # Initialize
        level = y[0]
        trend = y[1] - y[0] if n > 1 else 0

        # Fit model
        fitted = np.zeros(n)
        for i in range(n):
            fitted[i] = level + phi * trend
            if i < n - 1:
                level_new = alpha * y[i] + (1 - alpha) * (level + phi * trend)
                trend = beta * (level_new - level) + (1 - beta) * phi * trend
                level = level_new

        # Forecast
        forecast = np.zeros(periods)
        for h in range(1, periods + 1):
            phi_sum = sum(phi ** i for i in range(1, h + 1))
            forecast[h - 1] = level + phi_sum * trend

        self.forecasts['damped_trend'] = forecast
        return {
            'forecast': forecast,
            'alpha': round(alpha, 4),
            'beta': round(beta, 4),
            'phi': phi,
            'final_level': round(level, 4),
            'final_trend': round(trend, 6)
        }

    def _optimize_holt_params(self, series: np.ndarray, phi: float) -> Tuple[float, float]:
        """Optimize Holt's method parameters."""
        def holt_sse(params):
            alpha, beta = params
            n = len(series)
            level = series[0]
            trend = series[1] - series[0] if n > 1 else 0
            sse = 0

            for i in range(n):
                forecast = level + phi * trend
                error = series[i] - forecast
                sse += error ** 2
                if i < n - 1:
                    level_new = alpha * series[i] + (1 - alpha) * (level + phi * trend)
                    trend = beta * (level_new - level) + (1 - beta) * phi * trend
                    level = level_new
            return sse

        result = minimize(holt_sse, [0.5, 0.1], bounds=[(0.01, 0.99), (0.01, 0.99)])
        return result.x[0], result.x[1]

    def croston_method(
        self,
        series: pd.Series,
        periods: int,
        alpha: float = 0.1
    ) -> Dict:
        """
        Croston's method for intermittent demand forecasting.

        Args:
            series: Time series with zeros
            periods: Forecast horizon
            alpha: Smoothing parameter

        Returns:
            Forecast results
        """
        y = series.values
        n = len(y)

        # Separate demand sizes and intervals
        demands = []
        intervals = []
        last_demand_idx = -1

        for i in range(n):
            if y[i] > 0:
                demands.append(y[i])
                if last_demand_idx >= 0:
                    intervals.append(i - last_demand_idx)
                last_demand_idx = i

        if len(demands) == 0:
            forecast = np.zeros(periods)
        else:
            # Initialize
            z = demands[0]  # demand level
            p = intervals[0] if intervals else 1  # interval level

            # Update with SES
            for i in range(1, len(demands)):
                z = alpha * demands[i] + (1 - alpha) * z
                if i < len(intervals):
                    p = alpha * intervals[i] + (1 - alpha) * p

            # Forecast = demand / interval
            forecast_value = z / p if p > 0 else z
            forecast = np.full(periods, forecast_value)

        self.forecasts['croston'] = forecast
        return {
            'forecast': forecast,
            'alpha': alpha,
            'demand_level': round(z, 4) if len(demands) > 0 else 0,
            'interval_level': round(p, 4) if len(demands) > 0 else 0
        }

    def double_seasonal_holt_winters(
        self,
        series: pd.Series,
        periods: int,
        period1: int = 24,
        period2: int = 168,
        alpha: float = 0.1,
        beta: float = 0.01,
        gamma1: float = 0.1,
        gamma2: float = 0.01
    ) -> Dict:
        """
        Double seasonal Holt-Winters for multiple seasonalities.

        Useful for hourly data with daily and weekly patterns.

        Args:
            series: Time series
            periods: Forecast horizon
            period1: First seasonal period
            period2: Second seasonal period
            alpha, beta, gamma1, gamma2: Smoothing parameters

        Returns:
            Forecast results
        """
        y = series.values
        n = len(y)

        # Initialize components
        level = np.mean(y[:period2])
        trend = (np.mean(y[period2:2*period2]) - np.mean(y[:period2])) / period2 if n >= 2*period2 else 0

        # Initialize seasonal components
        seasonal1 = np.zeros(period1)
        seasonal2 = np.zeros(period2)

        for i in range(period1):
            seasonal1[i] = np.mean([y[j] for j in range(i, min(n, period2), period1)]) - level

        for i in range(period2):
            seasonal2[i] = np.mean([y[j] for j in range(i, n, period2)]) - level - seasonal1[i % period1]

        # Fit model
        fitted = np.zeros(n)
        for t in range(n):
            s1_idx = t % period1
            s2_idx = t % period2
            fitted[t] = level + trend + seasonal1[s1_idx] + seasonal2[s2_idx]

            # Update
            level_new = alpha * (y[t] - seasonal1[s1_idx] - seasonal2[s2_idx]) + (1 - alpha) * (level + trend)
            trend = beta * (level_new - level) + (1 - beta) * trend
            seasonal1[s1_idx] = gamma1 * (y[t] - level_new - seasonal2[s2_idx]) + (1 - gamma1) * seasonal1[s1_idx]
            seasonal2[s2_idx] = gamma2 * (y[t] - level_new - seasonal1[s1_idx]) + (1 - gamma2) * seasonal2[s2_idx]
            level = level_new

        # Forecast
        forecast = np.zeros(periods)
        for h in range(periods):
            t = n + h
            s1_idx = t % period1
            s2_idx = t % period2
            forecast[h] = level + (h + 1) * trend + seasonal1[s1_idx] + seasonal2[s2_idx]

        self.forecasts['double_seasonal'] = forecast
        return {
            'forecast': forecast,
            'period1': period1,
            'period2': period2,
            'final_level': round(level, 4),
            'final_trend': round(trend, 6)
        }

    def ets_auto(
        self,
        series: pd.Series,
        periods: int
    ) -> Dict:
        """
        Automatic ETS model selection.

        Args:
            series: Time series
            periods: Forecast horizon

        Returns:
            Best model forecast
        """
        y = series.values
        n = len(y)

        best_aic = np.inf
        best_model = None
        best_forecast = None

        # Try different model configurations
        models = [
            ('SES', {'trend': None, 'seasonal': None}),
            ('Holt', {'trend': 'add', 'seasonal': None}),
            ('Damped', {'trend': 'add', 'seasonal': None, 'damped': True})
        ]

        for name, config in models:
            try:
                if name == 'SES':
                    alpha = self._optimize_ses_alpha(y)
                    level = y[0]
                    fitted = np.zeros(n)
                    for i in range(n):
                        fitted[i] = level
                        level = alpha * y[i] + (1 - alpha) * level
                    forecast = np.full(periods, level)
                    residuals = y - fitted
                    k = 1

                elif name == 'Holt':
                    result = self.damped_trend(series, periods, phi=1.0)
                    forecast = result['forecast']
                    k = 2

                elif name == 'Damped':
                    result = self.damped_trend(series, periods, phi=0.98)
                    forecast = result['forecast']
                    k = 3

                # Calculate AIC
                if name == 'SES':
                    sse = np.sum(residuals ** 2)
                else:
                    sse = np.sum((y[1:] - np.roll(y, 1)[1:]) ** 2)  # Simplified

                aic = n * np.log(sse / n) + 2 * k

                if aic < best_aic:
                    best_aic = aic
                    best_model = name
                    best_forecast = forecast

            except:
                continue

        self.forecasts['ets_auto'] = best_forecast
        return {
            'forecast': best_forecast,
            'model': best_model,
            'aic': round(best_aic, 2)
        }

    def weighted_ensemble(
        self,
        series: pd.Series,
        periods: int,
        methods: List[str] = None
    ) -> Dict:
        """
        Smart weighted ensemble of multiple methods.

        Args:
            series: Time series
            periods: Forecast horizon
            methods: Methods to include

        Returns:
            Ensemble forecast
        """
        if methods is None:
            methods = ['theta', 'damped_trend', 'ets_auto']

        forecasts = {}
        weights = {}

        # Generate forecasts from each method
        for method in methods:
            try:
                if method == 'theta':
                    result = self.theta_method(series, periods)
                elif method == 'damped_trend':
                    result = self.damped_trend(series, periods)
                elif method == 'ets_auto':
                    result = self.ets_auto(series, periods)
                elif method == 'croston':
                    result = self.croston_method(series, periods)

                forecasts[method] = result['forecast']

                # Calculate weights based on in-sample fit
                y = series.values
                n = len(y)
                holdout = max(10, n // 5)
                train = pd.Series(y[:-holdout])

                if method == 'theta':
                    val_result = self.theta_method(train, holdout)
                elif method == 'damped_trend':
                    val_result = self.damped_trend(train, holdout)
                elif method == 'ets_auto':
                    val_result = self.ets_auto(train, holdout)
                else:
                    val_result = {'forecast': np.full(holdout, np.mean(train))}

                val_forecast = val_result['forecast']
                actual = y[-holdout:]
                mse = np.mean((actual - val_forecast) ** 2)
                weights[method] = 1 / (mse + 1e-10)

            except:
                continue

        # Normalize weights
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

        # Weighted average
        ensemble = np.zeros(periods)
        for method, forecast in forecasts.items():
            ensemble += weights[method] * forecast

        self.forecasts['ensemble'] = ensemble
        return {
            'forecast': ensemble,
            'weights': {k: round(v, 4) for k, v in weights.items()},
            'methods': list(forecasts.keys())
        }

    def forecast_with_regressors(
        self,
        y: pd.Series,
        X: pd.DataFrame,
        X_future: pd.DataFrame,
        method: str = 'ridge'
    ) -> Dict:
        """
        Forecast with external regressors.

        Args:
            y: Target series
            X: Historical regressors
            X_future: Future regressors
            method: Regression method

        Returns:
            Forecast results
        """
        from sklearn.linear_model import Ridge, Lasso
        from sklearn.ensemble import GradientBoostingRegressor

        if method == 'ridge':
            model = Ridge(alpha=1.0)
        elif method == 'lasso':
            model = Lasso(alpha=0.1)
        elif method == 'gbm':
            model = GradientBoostingRegressor(n_estimators=100, max_depth=3)

        model.fit(X, y)
        forecast = model.predict(X_future)

        self.forecasts['regression'] = forecast
        return {
            'forecast': forecast,
            'method': method,
            'n_regressors': X.shape[1]
        }

    def get_all_forecasts(self) -> Dict[str, np.ndarray]:
        """Get all generated forecasts."""
        return self.forecasts.copy()
