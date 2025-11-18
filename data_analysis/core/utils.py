"""
Data Analysis Utilities
=======================

Common utility functions for data analysis operations.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import json
import pickle
from pathlib import Path


class DataAnalysisUtils:
    """Utility functions for data analysis operations."""

    @staticmethod
    def load_data(
        file_path: str,
        file_type: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from various file formats.

        Args:
            file_path: Path to data file
            file_type: File type (auto-detected if None)
            **kwargs: Additional arguments for pandas readers

        Returns:
            Loaded DataFrame
        """
        path = Path(file_path)
        file_type = file_type or path.suffix.lower().replace('.', '')

        loaders = {
            'csv': pd.read_csv,
            'xlsx': pd.read_excel,
            'xls': pd.read_excel,
            'json': pd.read_json,
            'parquet': pd.read_parquet,
            'feather': pd.read_feather,
            'pkl': pd.read_pickle,
            'pickle': pd.read_pickle
        }

        if file_type not in loaders:
            raise ValueError(f"Unsupported file type: {file_type}")

        return loaders[file_type](file_path, **kwargs)

    @staticmethod
    def save_data(
        df: pd.DataFrame,
        file_path: str,
        file_type: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Save DataFrame to various file formats.

        Args:
            df: DataFrame to save
            file_path: Output path
            file_type: File type
            **kwargs: Additional arguments for pandas writers
        """
        path = Path(file_path)
        file_type = file_type or path.suffix.lower().replace('.', '')

        savers = {
            'csv': df.to_csv,
            'xlsx': df.to_excel,
            'json': df.to_json,
            'parquet': df.to_parquet,
            'feather': df.to_feather,
            'pkl': df.to_pickle,
            'pickle': df.to_pickle
        }

        if file_type not in savers:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_type in ['csv', 'xlsx']:
            savers[file_type](file_path, index=kwargs.pop('index', False), **kwargs)
        else:
            savers[file_type](file_path, **kwargs)

    @staticmethod
    def train_test_split_time_series(
        df: pd.DataFrame,
        test_size: float = 0.2,
        date_column: Optional[str] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split time series data chronologically.

        Args:
            df: Input DataFrame
            test_size: Proportion for test set
            date_column: Date column for sorting

        Returns:
            Tuple of (train_df, test_df)
        """
        if date_column:
            df = df.sort_values(date_column)

        split_idx = int(len(df) * (1 - test_size))
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()

        return train_df, test_df

    @staticmethod
    def create_sequences(
        data: np.ndarray,
        sequence_length: int,
        target_length: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM/RNN models.

        Args:
            data: Input array
            sequence_length: Length of input sequences
            target_length: Length of target sequences

        Returns:
            Tuple of (X_sequences, y_sequences)
        """
        X, y = [], []

        for i in range(len(data) - sequence_length - target_length + 1):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length:i + sequence_length + target_length])

        return np.array(X), np.array(y)

    @staticmethod
    def calculate_metrics(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        task: str = 'regression'
    ) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.

        Args:
            y_true: True values
            y_pred: Predicted values
            task: 'regression' or 'classification'

        Returns:
            Dictionary of metrics
        """
        from sklearn.metrics import (
            mean_absolute_error, mean_squared_error, r2_score,
            mean_absolute_percentage_error,
            accuracy_score, precision_score, recall_score, f1_score
        )

        if task == 'regression':
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_true, y_pred)

            # MAPE (handle zeros)
            mask = y_true != 0
            if mask.sum() > 0:
                mape = mean_absolute_percentage_error(y_true[mask], y_pred[mask]) * 100
            else:
                mape = np.nan

            # Symmetric MAPE
            smape = np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-10)) * 100

            return {
                'MAE': round(mae, 4),
                'MSE': round(mse, 4),
                'RMSE': round(rmse, 4),
                'R2': round(r2, 4),
                'MAPE': round(mape, 2),
                'SMAPE': round(smape, 2)
            }
        else:
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

            return {
                'Accuracy': round(accuracy, 4),
                'Precision': round(precision, 4),
                'Recall': round(recall, 4),
                'F1': round(f1, 4)
            }

    @staticmethod
    def generate_date_range(
        start_date: Union[str, datetime],
        periods: int,
        freq: str = 'D'
    ) -> pd.DatetimeIndex:
        """
        Generate a date range.

        Args:
            start_date: Start date
            periods: Number of periods
            freq: Frequency ('D', 'W', 'M', 'Q', 'Y')

        Returns:
            DatetimeIndex
        """
        return pd.date_range(start=start_date, periods=periods, freq=freq)

    @staticmethod
    def detect_seasonality(
        series: pd.Series,
        max_lag: int = 365
    ) -> Dict[str, Union[bool, int, float]]:
        """
        Detect seasonality in time series.

        Args:
            series: Time series data
            max_lag: Maximum lag to check

        Returns:
            Dictionary with seasonality information
        """
        from scipy.signal import find_peaks

        # Calculate autocorrelation
        autocorr = [series.autocorr(lag=i) for i in range(1, min(max_lag, len(series) // 2))]

        # Find peaks in autocorrelation
        peaks, properties = find_peaks(autocorr, height=0.1, distance=5)

        result = {
            'has_seasonality': len(peaks) > 0,
            'seasonal_periods': [],
            'peak_correlations': []
        }

        if len(peaks) > 0:
            # Sort by correlation strength
            sorted_idx = np.argsort([autocorr[p] for p in peaks])[::-1]
            top_peaks = peaks[sorted_idx[:3]]  # Top 3 periods

            result['seasonal_periods'] = (top_peaks + 1).tolist()
            result['peak_correlations'] = [round(autocorr[p], 4) for p in top_peaks]

        return result

    @staticmethod
    def detect_trend(
        series: pd.Series
    ) -> Dict[str, Union[str, float]]:
        """
        Detect trend in time series.

        Args:
            series: Time series data

        Returns:
            Dictionary with trend information
        """
        from scipy import stats

        # Linear regression
        x = np.arange(len(series))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, series.values)

        # Mann-Kendall test for trend
        n = len(series)
        s = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                s += np.sign(series.iloc[j] - series.iloc[i])

        # Variance of S
        var_s = n * (n - 1) * (2 * n + 5) / 18

        # Z statistic
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0

        # Determine trend direction
        if slope > 0 and p_value < 0.05:
            trend = 'increasing'
        elif slope < 0 and p_value < 0.05:
            trend = 'decreasing'
        else:
            trend = 'no_trend'

        return {
            'trend': trend,
            'slope': round(slope, 6),
            'r_squared': round(r_value ** 2, 4),
            'p_value': round(p_value, 4),
            'mann_kendall_z': round(z, 4)
        }

    @staticmethod
    def calculate_growth_rate(
        series: pd.Series,
        periods: int = 1,
        method: str = 'simple'
    ) -> pd.Series:
        """
        Calculate growth rate.

        Args:
            series: Input series
            periods: Number of periods
            method: 'simple' or 'compound'

        Returns:
            Growth rate series
        """
        if method == 'simple':
            return series.pct_change(periods) * 100
        else:  # compound
            return ((series / series.shift(periods)) ** (1 / periods) - 1) * 100

    @staticmethod
    def save_model(model: object, file_path: str) -> None:
        """
        Save model to disk.

        Args:
            model: Model object to save
            file_path: Output path
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as f:
            pickle.dump(model, f)

    @staticmethod
    def load_model(file_path: str) -> object:
        """
        Load model from disk.

        Args:
            file_path: Path to model file

        Returns:
            Loaded model
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def generate_report(
        results: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate analysis report.

        Args:
            results: Dictionary of analysis results
            output_path: Optional path to save report

        Returns:
            Report string
        """
        report = "=" * 60 + "\n"
        report += "DATA ANALYSIS REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 60 + "\n\n"

        def format_dict(d, indent=0):
            output = ""
            for key, value in d.items():
                prefix = "  " * indent
                if isinstance(value, dict):
                    output += f"{prefix}{key}:\n"
                    output += format_dict(value, indent + 1)
                elif isinstance(value, list):
                    output += f"{prefix}{key}: {value}\n"
                else:
                    output += f"{prefix}{key}: {value}\n"
            return output

        report += format_dict(results)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)

        return report

    @staticmethod
    def cross_validate_time_series(
        model,
        X: np.ndarray,
        y: np.ndarray,
        n_splits: int = 5,
        test_size: int = None
    ) -> Dict[str, List[float]]:
        """
        Time series cross-validation with expanding window.

        Args:
            model: Model with fit and predict methods
            X: Features
            y: Target
            n_splits: Number of splits
            test_size: Test set size per fold

        Returns:
            Dictionary of metrics per fold
        """
        from sklearn.base import clone

        n = len(X)
        if test_size is None:
            test_size = n // (n_splits + 1)

        results = {'mae': [], 'rmse': [], 'r2': []}

        for i in range(n_splits):
            train_end = n - (n_splits - i) * test_size
            test_start = train_end
            test_end = test_start + test_size

            X_train, y_train = X[:train_end], y[:train_end]
            X_test, y_test = X[test_start:test_end], y[test_start:test_end]

            # Clone and fit model
            model_clone = clone(model)
            model_clone.fit(X_train, y_train)
            y_pred = model_clone.predict(X_test)

            # Calculate metrics
            mae = np.mean(np.abs(y_test - y_pred))
            rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
            ss_res = np.sum((y_test - y_pred) ** 2)
            ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

            results['mae'].append(round(mae, 4))
            results['rmse'].append(round(rmse, 4))
            results['r2'].append(round(r2, 4))

        return results
