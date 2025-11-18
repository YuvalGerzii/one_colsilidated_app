"""
Advanced Time Series Forecasting Module
=======================================

Comprehensive time series forecasting using ARIMA, SARIMA, Prophet,
LSTM, and other advanced algorithms.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class TimeSeriesForecaster:
    """
    Advanced time series forecasting with multiple algorithms.
    Supports ARIMA, SARIMA, Prophet, LSTM, and XGBoost.
    """

    def __init__(self):
        self.models = {}
        self.forecasts = {}
        self.metrics = {}
        self.fitted = False

    def fit_arima(
        self,
        series: pd.Series,
        order: Tuple[int, int, int] = None,
        seasonal_order: Tuple[int, int, int, int] = None,
        auto_order: bool = True
    ) -> Dict:
        """
        Fit ARIMA/SARIMA model.

        Args:
            series: Time series data
            order: ARIMA order (p, d, q)
            seasonal_order: Seasonal order (P, D, Q, s)
            auto_order: Automatically find best order

        Returns:
            Model fit results
        """
        try:
            from statsmodels.tsa.arima.model import ARIMA
            from statsmodels.tsa.statespace.sarimax import SARIMAX
            from statsmodels.tsa.stattools import adfuller
        except ImportError:
            return {"error": "statsmodels not installed"}

        # Check stationarity
        adf_result = adfuller(series.dropna())
        is_stationary = adf_result[1] < 0.05

        if auto_order:
            # Auto-detect order using AIC
            best_aic = np.inf
            best_order = (1, 1, 1)

            for p in range(3):
                for d in range(2):
                    for q in range(3):
                        try:
                            model = ARIMA(series, order=(p, d, q))
                            fitted = model.fit()
                            if fitted.aic < best_aic:
                                best_aic = fitted.aic
                                best_order = (p, d, q)
                        except:
                            continue

            order = best_order

        # Fit model
        if seasonal_order:
            model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
        else:
            model = ARIMA(series, order=order)

        fitted_model = model.fit()
        self.models['arima'] = fitted_model

        return {
            'model_type': 'SARIMA' if seasonal_order else 'ARIMA',
            'order': order,
            'seasonal_order': seasonal_order,
            'aic': round(fitted_model.aic, 2),
            'bic': round(fitted_model.bic, 2),
            'is_stationary': is_stationary
        }

    def fit_prophet(
        self,
        df: pd.DataFrame,
        date_column: str = 'ds',
        value_column: str = 'y',
        yearly_seasonality: bool = True,
        weekly_seasonality: bool = True,
        daily_seasonality: bool = False,
        holidays: pd.DataFrame = None,
        changepoint_prior_scale: float = 0.05,
        seasonality_prior_scale: float = 10.0
    ) -> Dict:
        """
        Fit Facebook Prophet model.

        Args:
            df: DataFrame with date and value columns
            date_column: Name of date column
            value_column: Name of value column
            yearly_seasonality: Include yearly seasonality
            weekly_seasonality: Include weekly seasonality
            daily_seasonality: Include daily seasonality
            holidays: Holiday DataFrame
            changepoint_prior_scale: Flexibility of trend
            seasonality_prior_scale: Flexibility of seasonality

        Returns:
            Model fit results
        """
        try:
            from prophet import Prophet
        except ImportError:
            return {"error": "prophet not installed. Install with: pip install prophet"}

        # Prepare data
        prophet_df = df[[date_column, value_column]].copy()
        prophet_df.columns = ['ds', 'y']
        prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

        # Initialize model
        model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
            changepoint_prior_scale=changepoint_prior_scale,
            seasonality_prior_scale=seasonality_prior_scale
        )

        # Add holidays if provided
        if holidays is not None:
            model.add_country_holidays(country_name='US')

        # Fit model
        model.fit(prophet_df)
        self.models['prophet'] = model

        return {
            'model_type': 'Prophet',
            'changepoints': len(model.changepoints),
            'yearly_seasonality': yearly_seasonality,
            'weekly_seasonality': weekly_seasonality,
            'daily_seasonality': daily_seasonality
        }

    def fit_lstm(
        self,
        series: np.ndarray,
        sequence_length: int = 30,
        n_features: int = 1,
        lstm_units: List[int] = [50, 30],
        dropout: float = 0.2,
        epochs: int = 100,
        batch_size: int = 32,
        validation_split: float = 0.1
    ) -> Dict:
        """
        Fit LSTM neural network model.

        Args:
            series: Time series array
            sequence_length: Input sequence length
            n_features: Number of features
            lstm_units: Units in LSTM layers
            dropout: Dropout rate
            epochs: Training epochs
            batch_size: Batch size
            validation_split: Validation split ratio

        Returns:
            Model fit results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense, Dropout
            from tensorflow.keras.callbacks import EarlyStopping
            from sklearn.preprocessing import MinMaxScaler
        except ImportError:
            return {"error": "tensorflow not installed. Install with: pip install tensorflow"}

        # Scale data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(series.reshape(-1, 1))

        # Create sequences
        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i, 0])
            y.append(scaled_data[i, 0])

        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], n_features))

        # Build model
        model = Sequential()
        model.add(LSTM(lstm_units[0], return_sequences=len(lstm_units) > 1, input_shape=(sequence_length, n_features)))
        model.add(Dropout(dropout))

        for i, units in enumerate(lstm_units[1:]):
            return_seq = i < len(lstm_units) - 2
            model.add(LSTM(units, return_sequences=return_seq))
            model.add(Dropout(dropout))

        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Early stopping
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        # Fit model
        history = model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stop],
            verbose=0
        )

        self.models['lstm'] = {
            'model': model,
            'scaler': scaler,
            'sequence_length': sequence_length
        }

        return {
            'model_type': 'LSTM',
            'layers': len(lstm_units),
            'total_params': model.count_params(),
            'final_loss': round(history.history['loss'][-1], 6),
            'final_val_loss': round(history.history['val_loss'][-1], 6),
            'epochs_trained': len(history.history['loss'])
        }

    def fit_xgboost(
        self,
        X: np.ndarray,
        y: np.ndarray,
        params: Dict = None
    ) -> Dict:
        """
        Fit XGBoost model for time series.

        Args:
            X: Features (lagged values, etc.)
            y: Target values
            params: XGBoost parameters

        Returns:
            Model fit results
        """
        try:
            import xgboost as xgb
        except ImportError:
            return {"error": "xgboost not installed. Install with: pip install xgboost"}

        default_params = {
            'objective': 'reg:squarederror',
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }

        if params:
            default_params.update(params)

        model = xgb.XGBRegressor(**default_params)
        model.fit(X, y)
        self.models['xgboost'] = model

        return {
            'model_type': 'XGBoost',
            'n_estimators': default_params['n_estimators'],
            'max_depth': default_params['max_depth'],
            'learning_rate': default_params['learning_rate'],
            'feature_importance': dict(zip(range(X.shape[1]), model.feature_importances_.round(4)))
        }

    def fit_exponential_smoothing(
        self,
        series: pd.Series,
        trend: str = 'add',
        seasonal: str = 'add',
        seasonal_periods: int = 12
    ) -> Dict:
        """
        Fit Exponential Smoothing (Holt-Winters) model.

        Args:
            series: Time series data
            trend: Trend type ('add', 'mul', None)
            seasonal: Seasonal type ('add', 'mul', None)
            seasonal_periods: Number of periods in season

        Returns:
            Model fit results
        """
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
        except ImportError:
            return {"error": "statsmodels not installed"}

        model = ExponentialSmoothing(
            series,
            trend=trend,
            seasonal=seasonal,
            seasonal_periods=seasonal_periods
        )

        fitted_model = model.fit()
        self.models['exp_smoothing'] = fitted_model

        return {
            'model_type': 'Exponential Smoothing',
            'trend': trend,
            'seasonal': seasonal,
            'seasonal_periods': seasonal_periods,
            'aic': round(fitted_model.aic, 2),
            'bic': round(fitted_model.bic, 2)
        }

    def forecast(
        self,
        model_name: str,
        periods: int,
        X_future: np.ndarray = None,
        return_conf_int: bool = True
    ) -> Dict:
        """
        Generate forecasts from fitted model.

        Args:
            model_name: Name of fitted model
            periods: Forecast horizon
            X_future: Future features for ML models
            return_conf_int: Return confidence intervals

        Returns:
            Forecast results
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not fitted")

        model = self.models[model_name]
        result = {}

        if model_name == 'arima':
            forecast = model.get_forecast(periods)
            result['forecast'] = forecast.predicted_mean.values
            if return_conf_int:
                conf_int = forecast.conf_int()
                result['lower'] = conf_int.iloc[:, 0].values
                result['upper'] = conf_int.iloc[:, 1].values

        elif model_name == 'prophet':
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            result['forecast'] = forecast['yhat'].tail(periods).values
            if return_conf_int:
                result['lower'] = forecast['yhat_lower'].tail(periods).values
                result['upper'] = forecast['yhat_upper'].tail(periods).values
            result['trend'] = forecast['trend'].tail(periods).values

        elif model_name == 'lstm':
            lstm_model = model['model']
            scaler = model['scaler']
            seq_len = model['sequence_length']

            # This would need the last sequence of data
            # For now, return placeholder
            result['forecast'] = np.zeros(periods)
            result['note'] = 'LSTM forecasting requires sequential prediction'

        elif model_name == 'xgboost':
            if X_future is None:
                raise ValueError("XGBoost requires X_future for forecasting")
            result['forecast'] = model.predict(X_future)

        elif model_name == 'exp_smoothing':
            result['forecast'] = model.forecast(periods).values

        self.forecasts[model_name] = result
        return result

    def forecast_lstm_iterative(
        self,
        series: np.ndarray,
        periods: int
    ) -> np.ndarray:
        """
        Iterative LSTM forecasting.

        Args:
            series: Historical series
            periods: Forecast horizon

        Returns:
            Forecast array
        """
        if 'lstm' not in self.models:
            raise ValueError("LSTM model not fitted")

        model = self.models['lstm']['model']
        scaler = self.models['lstm']['scaler']
        seq_len = self.models['lstm']['sequence_length']

        # Scale the input
        scaled = scaler.transform(series.reshape(-1, 1))

        # Get last sequence
        current_seq = scaled[-seq_len:].reshape(1, seq_len, 1)

        predictions = []
        for _ in range(periods):
            # Predict next value
            pred = model.predict(current_seq, verbose=0)[0, 0]
            predictions.append(pred)

            # Update sequence
            current_seq = np.roll(current_seq, -1, axis=1)
            current_seq[0, -1, 0] = pred

        # Inverse transform
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()

    def evaluate_model(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str
    ) -> Dict[str, float]:
        """
        Evaluate forecast accuracy.

        Args:
            y_true: Actual values
            y_pred: Predicted values
            model_name: Model name for storing metrics

        Returns:
            Dictionary of metrics
        """
        mae = np.mean(np.abs(y_true - y_pred))
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)

        # MAPE
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

        # SMAPE
        smape = np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-10)) * 100

        # Direction accuracy
        if len(y_true) > 1:
            actual_direction = np.diff(y_true) > 0
            pred_direction = np.diff(y_pred) > 0
            direction_accuracy = np.mean(actual_direction == pred_direction) * 100
        else:
            direction_accuracy = 0

        metrics = {
            'MAE': round(mae, 4),
            'MSE': round(mse, 4),
            'RMSE': round(rmse, 4),
            'MAPE': round(mape, 2),
            'SMAPE': round(smape, 2),
            'Direction_Accuracy': round(direction_accuracy, 2)
        }

        self.metrics[model_name] = metrics
        return metrics

    def decompose_series(
        self,
        series: pd.Series,
        model: str = 'additive',
        period: int = None
    ) -> Dict:
        """
        Decompose time series into trend, seasonal, and residual.

        Args:
            series: Time series data
            model: 'additive' or 'multiplicative'
            period: Seasonal period

        Returns:
            Decomposition components
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
        except ImportError:
            return {"error": "statsmodels not installed"}

        if period is None:
            period = min(12, len(series) // 2)

        decomposition = seasonal_decompose(series, model=model, period=period)

        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'observed': decomposition.observed
        }

    def get_best_model(self) -> str:
        """
        Get the best performing model based on metrics.

        Returns:
            Name of best model
        """
        if not self.metrics:
            raise ValueError("No models evaluated yet")

        # Compare by RMSE
        best_model = min(self.metrics.items(), key=lambda x: x[1]['RMSE'])
        return best_model[0]

    def get_all_metrics(self) -> Dict:
        """Get metrics for all evaluated models."""
        return self.metrics.copy()

    def walk_forward_validation(
        self,
        series: pd.Series,
        model_name: str,
        initial_train_size: int,
        forecast_horizon: int = 1,
        step: int = 1
    ) -> Dict:
        """
        Walk-forward validation for time series.

        Args:
            series: Time series data
            model_name: Model to use
            initial_train_size: Initial training size
            forecast_horizon: Forecast steps ahead
            step: Step size for rolling window

        Returns:
            Validation results
        """
        predictions = []
        actuals = []

        for i in range(initial_train_size, len(series) - forecast_horizon + 1, step):
            train = series[:i]
            test = series[i:i + forecast_horizon]

            # Fit model on training data
            if model_name == 'arima':
                self.fit_arima(train)
                forecast = self.forecast('arima', forecast_horizon)['forecast']
            elif model_name == 'exp_smoothing':
                self.fit_exponential_smoothing(train)
                forecast = self.forecast('exp_smoothing', forecast_horizon)['forecast']
            else:
                continue

            predictions.extend(forecast)
            actuals.extend(test.values)

        predictions = np.array(predictions)
        actuals = np.array(actuals)

        return self.evaluate_model(actuals, predictions, f'{model_name}_walkforward')
