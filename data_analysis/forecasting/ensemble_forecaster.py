"""
Ensemble Forecasting Module
============================

Advanced ensemble methods combining multiple forecasting models
for improved prediction accuracy and robustness.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from scipy.optimize import minimize
import warnings

warnings.filterwarnings('ignore')


class EnsembleForecaster:
    """
    Ensemble forecasting combining multiple models using
    various weighting strategies.
    """

    def __init__(self):
        self.models = {}
        self.weights = {}
        self.forecasts = {}
        self.ensemble_forecast = None
        self.metrics = {}

    def add_forecast(
        self,
        name: str,
        forecast: np.ndarray,
        confidence_lower: np.ndarray = None,
        confidence_upper: np.ndarray = None
    ) -> None:
        """
        Add a model forecast to the ensemble.

        Args:
            name: Model name
            forecast: Forecast values
            confidence_lower: Lower confidence bound
            confidence_upper: Upper confidence bound
        """
        self.forecasts[name] = {
            'forecast': np.array(forecast),
            'lower': np.array(confidence_lower) if confidence_lower is not None else None,
            'upper': np.array(confidence_upper) if confidence_upper is not None else None
        }

    def simple_average(self) -> np.ndarray:
        """
        Simple average ensemble.

        Returns:
            Averaged forecast
        """
        forecasts = np.array([f['forecast'] for f in self.forecasts.values()])
        self.ensemble_forecast = np.mean(forecasts, axis=0)

        # Set equal weights
        n_models = len(self.forecasts)
        self.weights = {name: 1/n_models for name in self.forecasts.keys()}

        return self.ensemble_forecast

    def weighted_average(
        self,
        weights: Dict[str, float]
    ) -> np.ndarray:
        """
        Weighted average ensemble.

        Args:
            weights: Dictionary of model weights

        Returns:
            Weighted average forecast
        """
        # Normalize weights
        total = sum(weights.values())
        normalized_weights = {k: v/total for k, v in weights.items()}

        forecast = np.zeros_like(list(self.forecasts.values())[0]['forecast'])

        for name, weight in normalized_weights.items():
            if name in self.forecasts:
                forecast += weight * self.forecasts[name]['forecast']

        self.ensemble_forecast = forecast
        self.weights = normalized_weights

        return self.ensemble_forecast

    def inverse_error_weighting(
        self,
        validation_errors: Dict[str, float]
    ) -> np.ndarray:
        """
        Weight models inversely proportional to their errors.

        Args:
            validation_errors: Dictionary of model validation errors

        Returns:
            Weighted forecast
        """
        # Calculate inverse error weights
        inverse_errors = {name: 1 / (error + 1e-10)
                        for name, error in validation_errors.items()
                        if name in self.forecasts}

        total = sum(inverse_errors.values())
        weights = {name: inv / total for name, inv in inverse_errors.items()}

        return self.weighted_average(weights)

    def optimal_weights(
        self,
        y_true: np.ndarray,
        forecasts_dict: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """
        Find optimal weights by minimizing forecast error.

        Args:
            y_true: Actual values
            forecasts_dict: Dictionary of model forecasts

        Returns:
            Optimally weighted forecast
        """
        model_names = list(forecasts_dict.keys())
        forecasts_matrix = np.array([forecasts_dict[name] for name in model_names])

        # Objective function: minimize MSE
        def objective(weights):
            weighted_forecast = np.sum(weights.reshape(-1, 1) * forecasts_matrix, axis=0)
            return np.mean((y_true - weighted_forecast) ** 2)

        # Constraints: weights sum to 1
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

        # Bounds: weights between 0 and 1
        bounds = [(0, 1) for _ in model_names]

        # Initial guess: equal weights
        initial_weights = np.ones(len(model_names)) / len(model_names)

        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        optimal_weights = {name: round(w, 4)
                         for name, w in zip(model_names, result.x)}

        # Apply weights to stored forecasts
        self.weights = optimal_weights

        if self.forecasts:
            return self.weighted_average(optimal_weights)
        else:
            # Return weighted forecast from input
            return np.sum(result.x.reshape(-1, 1) * forecasts_matrix, axis=0)

    def median_ensemble(self) -> np.ndarray:
        """
        Median ensemble (robust to outliers).

        Returns:
            Median forecast
        """
        forecasts = np.array([f['forecast'] for f in self.forecasts.values()])
        self.ensemble_forecast = np.median(forecasts, axis=0)

        return self.ensemble_forecast

    def trimmed_mean_ensemble(
        self,
        trim_proportion: float = 0.1
    ) -> np.ndarray:
        """
        Trimmed mean ensemble (removes extreme forecasts).

        Args:
            trim_proportion: Proportion to trim from each end

        Returns:
            Trimmed mean forecast
        """
        forecasts = np.array([f['forecast'] for f in self.forecasts.values()])
        self.ensemble_forecast = stats.trim_mean(forecasts, trim_proportion, axis=0)

        return self.ensemble_forecast

    def stacking_ensemble(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_pred: np.ndarray,
        meta_model: str = 'ridge'
    ) -> np.ndarray:
        """
        Stacking ensemble using meta-learner.

        Args:
            X_train: Training forecasts (n_samples, n_models)
            y_train: Actual training values
            X_pred: Prediction forecasts
            meta_model: Meta-learner type

        Returns:
            Stacked ensemble forecast
        """
        from sklearn.linear_model import Ridge, LinearRegression
        from sklearn.ensemble import GradientBoostingRegressor

        if meta_model == 'ridge':
            meta = Ridge(alpha=1.0)
        elif meta_model == 'linear':
            meta = LinearRegression()
        elif meta_model == 'gbm':
            meta = GradientBoostingRegressor(n_estimators=50)
        else:
            meta = Ridge(alpha=1.0)

        meta.fit(X_train, y_train)
        self.models['meta'] = meta

        self.ensemble_forecast = meta.predict(X_pred)

        # Store meta-model coefficients as weights
        if hasattr(meta, 'coef_'):
            coef = meta.coef_
            self.weights = {f'model_{i}': round(c, 4) for i, c in enumerate(coef)}

        return self.ensemble_forecast

    def bayesian_model_averaging(
        self,
        y_true: np.ndarray,
        forecasts_dict: Dict[str, np.ndarray],
        prior: str = 'uniform'
    ) -> np.ndarray:
        """
        Bayesian Model Averaging.

        Args:
            y_true: Actual values
            forecasts_dict: Dictionary of model forecasts
            prior: Prior distribution type

        Returns:
            BMA forecast
        """
        model_names = list(forecasts_dict.keys())
        n_models = len(model_names)

        # Calculate likelihoods (assuming Gaussian errors)
        likelihoods = {}
        for name, forecast in forecasts_dict.items():
            residuals = y_true - forecast
            sigma = np.std(residuals)
            # Log-likelihood
            ll = -0.5 * np.sum((residuals / sigma) ** 2) - len(y_true) * np.log(sigma)
            likelihoods[name] = ll

        # Convert to probabilities
        max_ll = max(likelihoods.values())
        exp_ll = {name: np.exp(ll - max_ll) for name, ll in likelihoods.items()}
        total = sum(exp_ll.values())

        # Posterior weights
        weights = {name: exp / total for name, exp in exp_ll.items()}

        self.weights = weights

        # Apply to stored forecasts
        if self.forecasts:
            return self.weighted_average(weights)
        else:
            forecast = np.zeros_like(list(forecasts_dict.values())[0])
            for name, weight in weights.items():
                forecast += weight * forecasts_dict[name]
            return forecast

    def dynamic_weighting(
        self,
        y_history: np.ndarray,
        forecasts_history: Dict[str, np.ndarray],
        window: int = 10
    ) -> Dict[str, float]:
        """
        Calculate dynamic weights based on recent performance.

        Args:
            y_history: Historical actual values
            forecasts_history: Historical forecasts per model
            window: Rolling window size

        Returns:
            Dynamic weights
        """
        recent_errors = {}

        for name, forecast in forecasts_history.items():
            # Calculate recent RMSE
            recent_y = y_history[-window:]
            recent_f = forecast[-window:]
            rmse = np.sqrt(np.mean((recent_y - recent_f) ** 2))
            recent_errors[name] = rmse

        return self.inverse_error_weighting(recent_errors)

    def confidence_interval_ensemble(
        self,
        confidence_level: float = 0.95
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate ensemble confidence intervals.

        Args:
            confidence_level: Confidence level (0-1)

        Returns:
            Tuple of (forecast, lower, upper)
        """
        forecasts = np.array([f['forecast'] for f in self.forecasts.values()])

        # Point forecast
        mean_forecast = np.mean(forecasts, axis=0)

        # Calculate intervals using forecast variance
        std_forecast = np.std(forecasts, axis=0)
        z_score = stats.norm.ppf((1 + confidence_level) / 2)

        lower = mean_forecast - z_score * std_forecast
        upper = mean_forecast + z_score * std_forecast

        self.ensemble_forecast = mean_forecast

        return mean_forecast, lower, upper

    def evaluate_ensemble(
        self,
        y_true: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate ensemble forecast accuracy.

        Args:
            y_true: Actual values

        Returns:
            Dictionary of metrics
        """
        if self.ensemble_forecast is None:
            raise ValueError("No ensemble forecast generated yet")

        y_pred = self.ensemble_forecast
        y_true = np.array(y_true)

        mae = np.mean(np.abs(y_true - y_pred))
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)

        # MAPE
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

        # Skill score vs baseline (simple average)
        if len(self.forecasts) > 1:
            simple_avg = self.simple_average()
            baseline_mse = np.mean((y_true - simple_avg) ** 2)
            skill_score = 1 - (mse / baseline_mse) if baseline_mse > 0 else 0
        else:
            skill_score = 0

        self.metrics = {
            'MAE': round(mae, 4),
            'MSE': round(mse, 4),
            'RMSE': round(rmse, 4),
            'MAPE': round(mape, 2),
            'Skill_Score': round(skill_score, 4)
        }

        return self.metrics

    def compare_models(
        self,
        y_true: np.ndarray
    ) -> pd.DataFrame:
        """
        Compare individual model performance.

        Args:
            y_true: Actual values

        Returns:
            DataFrame with model comparison
        """
        results = []

        for name, forecast_data in self.forecasts.items():
            forecast = forecast_data['forecast']

            mae = np.mean(np.abs(y_true - forecast))
            mse = np.mean((y_true - forecast) ** 2)
            rmse = np.sqrt(mse)

            mask = y_true != 0
            mape = np.mean(np.abs((y_true[mask] - forecast[mask]) / y_true[mask])) * 100

            results.append({
                'Model': name,
                'MAE': round(mae, 4),
                'MSE': round(mse, 4),
                'RMSE': round(rmse, 4),
                'MAPE': round(mape, 2),
                'Weight': round(self.weights.get(name, 0), 4)
            })

        return pd.DataFrame(results).sort_values('RMSE')

    def get_weights(self) -> Dict[str, float]:
        """Get current model weights."""
        return self.weights.copy()

    def get_ensemble_forecast(self) -> np.ndarray:
        """Get current ensemble forecast."""
        return self.ensemble_forecast.copy() if self.ensemble_forecast is not None else None

    def forecast_with_uncertainty(
        self,
        n_bootstrap: int = 1000,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Generate forecast with uncertainty using bootstrap.

        Args:
            n_bootstrap: Number of bootstrap samples
            confidence_level: Confidence level

        Returns:
            Dictionary with forecast and intervals
        """
        forecasts = np.array([f['forecast'] for f in self.forecasts.values()])
        n_models, n_periods = forecasts.shape

        # Bootstrap resampling
        bootstrap_forecasts = []
        for _ in range(n_bootstrap):
            # Random weights
            weights = np.random.dirichlet(np.ones(n_models))
            bootstrap_forecast = np.sum(weights.reshape(-1, 1) * forecasts, axis=0)
            bootstrap_forecasts.append(bootstrap_forecast)

        bootstrap_forecasts = np.array(bootstrap_forecasts)

        # Calculate percentiles
        alpha = (1 - confidence_level) / 2
        lower = np.percentile(bootstrap_forecasts, alpha * 100, axis=0)
        upper = np.percentile(bootstrap_forecasts, (1 - alpha) * 100, axis=0)
        mean = np.mean(bootstrap_forecasts, axis=0)

        return {
            'forecast': mean,
            'lower': lower,
            'upper': upper,
            'std': np.std(bootstrap_forecasts, axis=0)
        }
