"""
Advanced Anomaly Detection Module
==================================

Comprehensive anomaly detection algorithms for time series
and multivariate data analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from scipy.signal import find_peaks
import warnings

warnings.filterwarnings('ignore')


class AnomalyDetector:
    """
    Advanced anomaly detection for time series and multivariate data.
    """

    def __init__(self):
        self.anomalies = []
        self.anomaly_scores = None
        self.threshold = None
        self.models = {}

    def detect_statistical_anomalies(
        self,
        series: pd.Series,
        method: str = 'zscore',
        threshold: float = 3.0
    ) -> Dict:
        """
        Detect anomalies using statistical methods.

        Args:
            series: Time series data
            method: 'zscore', 'iqr', or 'mad'
            threshold: Detection threshold

        Returns:
            Dictionary with anomaly detection results
        """
        values = series.values
        anomalies = []
        scores = np.zeros(len(values))

        if method == 'zscore':
            mean = np.mean(values)
            std = np.std(values)
            scores = np.abs((values - mean) / std)
            anomalies = np.where(scores > threshold)[0].tolist()

        elif method == 'iqr':
            Q1 = np.percentile(values, 25)
            Q3 = np.percentile(values, 75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            anomalies = np.where((values < lower) | (values > upper))[0].tolist()
            scores = np.where(values < lower, (lower - values) / IQR,
                            np.where(values > upper, (values - upper) / IQR, 0))

        elif method == 'mad':
            median = np.median(values)
            mad = np.median(np.abs(values - median))
            scores = np.abs(values - median) / (mad * 1.4826)
            anomalies = np.where(scores > threshold)[0].tolist()

        self.anomalies = anomalies
        self.anomaly_scores = scores

        return {
            'method': method,
            'threshold': threshold,
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies,
            'anomaly_values': [round(values[i], 4) for i in anomalies[:10]],
            'scores': scores
        }

    def detect_isolation_forest(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        contamination: float = 0.1,
        n_estimators: int = 100
    ) -> Dict:
        """
        Detect anomalies using Isolation Forest.

        Args:
            data: Input data (can be multivariate)
            contamination: Expected proportion of anomalies
            n_estimators: Number of trees

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            from sklearn.ensemble import IsolationForest
        except ImportError:
            return {"error": "scikit-learn not installed"}

        if isinstance(data, pd.DataFrame):
            X = data.values
        else:
            X = data.reshape(-1, 1) if data.ndim == 1 else data

        model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=42
        )

        predictions = model.fit_predict(X)
        scores = model.decision_function(X)

        anomalies = np.where(predictions == -1)[0].tolist()

        self.models['isolation_forest'] = model
        self.anomalies = anomalies
        self.anomaly_scores = -scores  # Convert to anomaly scores

        return {
            'method': 'Isolation Forest',
            'contamination': contamination,
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies,
            'scores': -scores
        }

    def detect_local_outlier_factor(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        n_neighbors: int = 20,
        contamination: float = 0.1
    ) -> Dict:
        """
        Detect anomalies using Local Outlier Factor.

        Args:
            data: Input data
            n_neighbors: Number of neighbors
            contamination: Expected proportion of anomalies

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            from sklearn.neighbors import LocalOutlierFactor
        except ImportError:
            return {"error": "scikit-learn not installed"}

        if isinstance(data, pd.DataFrame):
            X = data.values
        else:
            X = data.reshape(-1, 1) if data.ndim == 1 else data

        model = LocalOutlierFactor(
            n_neighbors=n_neighbors,
            contamination=contamination,
            novelty=False
        )

        predictions = model.fit_predict(X)
        scores = model.negative_outlier_factor_

        anomalies = np.where(predictions == -1)[0].tolist()

        self.anomalies = anomalies
        self.anomaly_scores = -scores

        return {
            'method': 'Local Outlier Factor',
            'n_neighbors': n_neighbors,
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies,
            'scores': -scores
        }

    def detect_dbscan(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        eps: float = 0.5,
        min_samples: int = 5
    ) -> Dict:
        """
        Detect anomalies using DBSCAN clustering.

        Args:
            data: Input data
            eps: Maximum distance between samples
            min_samples: Minimum samples in neighborhood

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            from sklearn.cluster import DBSCAN
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            return {"error": "scikit-learn not installed"}

        if isinstance(data, pd.DataFrame):
            X = data.values
        else:
            X = data.reshape(-1, 1) if data.ndim == 1 else data

        # Scale data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(X_scaled)

        # Anomalies are labeled as -1
        anomalies = np.where(labels == -1)[0].tolist()

        self.models['dbscan'] = model
        self.anomalies = anomalies

        return {
            'method': 'DBSCAN',
            'eps': eps,
            'min_samples': min_samples,
            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies
        }

    def detect_one_class_svm(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        nu: float = 0.1,
        kernel: str = 'rbf'
    ) -> Dict:
        """
        Detect anomalies using One-Class SVM.

        Args:
            data: Input data
            nu: Upper bound on training errors
            kernel: Kernel type

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            from sklearn.svm import OneClassSVM
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            return {"error": "scikit-learn not installed"}

        if isinstance(data, pd.DataFrame):
            X = data.values
        else:
            X = data.reshape(-1, 1) if data.ndim == 1 else data

        # Scale data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = OneClassSVM(nu=nu, kernel=kernel)
        predictions = model.fit_predict(X_scaled)
        scores = model.decision_function(X_scaled)

        anomalies = np.where(predictions == -1)[0].tolist()

        self.models['ocsvm'] = model
        self.anomalies = anomalies
        self.anomaly_scores = -scores

        return {
            'method': 'One-Class SVM',
            'nu': nu,
            'kernel': kernel,
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies,
            'scores': -scores
        }

    def detect_time_series_anomalies(
        self,
        series: pd.Series,
        window: int = 30,
        n_sigmas: float = 3.0
    ) -> Dict:
        """
        Detect anomalies in time series using rolling statistics.

        Args:
            series: Time series data
            window: Rolling window size
            n_sigmas: Number of standard deviations

        Returns:
            Dictionary with anomaly detection results
        """
        rolling_mean = series.rolling(window=window, center=True).mean()
        rolling_std = series.rolling(window=window, center=True).std()

        # Calculate upper and lower bounds
        upper_bound = rolling_mean + n_sigmas * rolling_std
        lower_bound = rolling_mean - n_sigmas * rolling_std

        # Identify anomalies
        anomalies = series[(series > upper_bound) | (series < lower_bound)]
        anomaly_indices = anomalies.index.tolist()

        # Calculate anomaly scores
        z_scores = (series - rolling_mean) / rolling_std
        scores = np.abs(z_scores.values)

        self.anomalies = [series.index.get_loc(idx) for idx in anomaly_indices if idx in series.index]
        self.anomaly_scores = scores

        return {
            'method': 'Rolling Statistics',
            'window': window,
            'n_sigmas': n_sigmas,
            'n_anomalies': len(anomalies),
            'anomaly_indices': self.anomalies,
            'anomaly_dates': anomaly_indices,
            'scores': scores,
            'bounds': {
                'upper': upper_bound,
                'lower': lower_bound
            }
        }

    def detect_seasonal_anomalies(
        self,
        series: pd.Series,
        period: int = 7,
        n_sigmas: float = 3.0
    ) -> Dict:
        """
        Detect anomalies accounting for seasonality.

        Args:
            series: Time series data
            period: Seasonal period
            n_sigmas: Number of standard deviations

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
        except ImportError:
            return {"error": "statsmodels not installed"}

        # Decompose series
        decomposition = seasonal_decompose(
            series,
            model='additive',
            period=period,
            extrapolate_trend='freq'
        )

        # Analyze residuals for anomalies
        residuals = decomposition.resid.dropna()
        mean_resid = residuals.mean()
        std_resid = residuals.std()

        # Identify anomalies in residuals
        threshold = n_sigmas * std_resid
        anomalies = residuals[np.abs(residuals - mean_resid) > threshold]

        return {
            'method': 'Seasonal Decomposition',
            'period': period,
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies.index.tolist(),
            'anomaly_values': anomalies.values.round(4).tolist()
        }

    def detect_collective_anomalies(
        self,
        series: pd.Series,
        window: int = 10,
        threshold: float = 2.0
    ) -> Dict:
        """
        Detect collective/contextual anomalies.

        Args:
            series: Time series data
            window: Window size for collective detection
            threshold: Detection threshold

        Returns:
            Dictionary with collective anomaly results
        """
        values = series.values
        n = len(values)

        # Calculate window statistics
        collective_anomalies = []

        for i in range(0, n - window + 1):
            window_data = values[i:i + window]

            # Compare window to overall distribution
            overall_mean = np.mean(values)
            overall_std = np.std(values)
            window_mean = np.mean(window_data)

            z_score = abs(window_mean - overall_mean) / overall_std

            if z_score > threshold:
                collective_anomalies.append({
                    'start': i,
                    'end': i + window,
                    'z_score': round(z_score, 4),
                    'window_mean': round(window_mean, 4)
                })

        return {
            'method': 'Collective Anomaly Detection',
            'window': window,
            'threshold': threshold,
            'n_collective_anomalies': len(collective_anomalies),
            'anomalies': collective_anomalies
        }

    def detect_autoencoder_anomalies(
        self,
        data: np.ndarray,
        encoding_dim: int = 8,
        threshold_percentile: float = 95,
        epochs: int = 50
    ) -> Dict:
        """
        Detect anomalies using autoencoder reconstruction error.

        Args:
            data: Input data
            encoding_dim: Encoding dimension
            threshold_percentile: Percentile for threshold
            epochs: Training epochs

        Returns:
            Dictionary with anomaly detection results
        """
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Model
            from tensorflow.keras.layers import Input, Dense
        except ImportError:
            return {"error": "tensorflow not installed"}

        if data.ndim == 1:
            data = data.reshape(-1, 1)

        input_dim = data.shape[1]

        # Build autoencoder
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(encoding_dim, activation='relu')(input_layer)
        decoded = Dense(input_dim, activation='linear')(encoded)

        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')

        # Train
        autoencoder.fit(data, data, epochs=epochs, batch_size=32, verbose=0)

        # Calculate reconstruction error
        reconstructed = autoencoder.predict(data)
        reconstruction_error = np.mean((data - reconstructed) ** 2, axis=1)

        # Determine threshold
        threshold = np.percentile(reconstruction_error, threshold_percentile)
        anomalies = np.where(reconstruction_error > threshold)[0].tolist()

        self.models['autoencoder'] = autoencoder
        self.anomalies = anomalies
        self.anomaly_scores = reconstruction_error

        return {
            'method': 'Autoencoder',
            'encoding_dim': encoding_dim,
            'threshold': round(threshold, 6),
            'n_anomalies': len(anomalies),
            'anomaly_indices': anomalies,
            'reconstruction_errors': reconstruction_error
        }

    def ensemble_detection(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        methods: List[str] = None,
        voting: str = 'majority'
    ) -> Dict:
        """
        Ensemble anomaly detection combining multiple methods.

        Args:
            data: Input data
            methods: List of methods to use
            voting: 'majority', 'unanimous', or 'any'

        Returns:
            Dictionary with ensemble results
        """
        if methods is None:
            methods = ['zscore', 'isolation_forest', 'lof']

        if isinstance(data, pd.DataFrame):
            series = data.iloc[:, 0] if len(data.columns) == 1 else None
            X = data.values
        else:
            series = pd.Series(data.flatten())
            X = data.reshape(-1, 1) if data.ndim == 1 else data

        all_anomalies = {}
        n_samples = len(data)

        # Run each method
        for method in methods:
            if method == 'zscore' and series is not None:
                result = self.detect_statistical_anomalies(series, method='zscore')
                all_anomalies['zscore'] = set(result['anomaly_indices'])

            elif method == 'iqr' and series is not None:
                result = self.detect_statistical_anomalies(series, method='iqr')
                all_anomalies['iqr'] = set(result['anomaly_indices'])

            elif method == 'isolation_forest':
                result = self.detect_isolation_forest(X)
                all_anomalies['isolation_forest'] = set(result['anomaly_indices'])

            elif method == 'lof':
                result = self.detect_local_outlier_factor(X)
                all_anomalies['lof'] = set(result['anomaly_indices'])

            elif method == 'dbscan':
                result = self.detect_dbscan(X)
                all_anomalies['dbscan'] = set(result['anomaly_indices'])

        # Combine results
        if voting == 'majority':
            # Anomaly if detected by majority of methods
            vote_counts = {}
            for idx in range(n_samples):
                vote_counts[idx] = sum(1 for method_anomalies in all_anomalies.values()
                                      if idx in method_anomalies)
            threshold = len(methods) / 2
            final_anomalies = [idx for idx, count in vote_counts.items()
                             if count > threshold]

        elif voting == 'unanimous':
            # Anomaly if detected by all methods
            if all_anomalies:
                final_anomalies = list(set.intersection(*all_anomalies.values()))
            else:
                final_anomalies = []

        else:  # 'any'
            # Anomaly if detected by any method
            if all_anomalies:
                final_anomalies = list(set.union(*all_anomalies.values()))
            else:
                final_anomalies = []

        self.anomalies = sorted(final_anomalies)

        return {
            'method': 'Ensemble',
            'voting': voting,
            'methods_used': list(all_anomalies.keys()),
            'n_anomalies': len(final_anomalies),
            'anomaly_indices': sorted(final_anomalies),
            'per_method_counts': {method: len(anomalies)
                                 for method, anomalies in all_anomalies.items()}
        }

    def get_anomaly_summary(
        self,
        series: pd.Series
    ) -> Dict:
        """
        Get comprehensive anomaly summary.

        Args:
            series: Time series data

        Returns:
            Dictionary with anomaly summary
        """
        # Run multiple detection methods
        zscore_result = self.detect_statistical_anomalies(series, 'zscore')
        iqr_result = self.detect_statistical_anomalies(series, 'iqr')
        rolling_result = self.detect_time_series_anomalies(series)

        # Combine results
        all_anomalies = set(zscore_result['anomaly_indices'] +
                          iqr_result['anomaly_indices'] +
                          rolling_result['anomaly_indices'])

        return {
            'total_anomalies': len(all_anomalies),
            'zscore': zscore_result['n_anomalies'],
            'iqr': iqr_result['n_anomalies'],
            'rolling': rolling_result['n_anomalies'],
            'combined_indices': sorted(list(all_anomalies))
        }
