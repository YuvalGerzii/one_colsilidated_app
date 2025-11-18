"""
Data Quality and Drift Monitoring
==================================

Monitor data quality, detect drift, and validate data.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
import warnings

warnings.filterwarnings('ignore')


class DataQualityMonitor:
    """
    Monitor data quality and detect issues.
    """

    def __init__(self):
        self.baseline_stats = {}
        self.quality_scores = {}
        self.issues = []

    def set_baseline(self, df: pd.DataFrame) -> Dict:
        """
        Set baseline statistics for monitoring.

        Args:
            df: Baseline DataFrame

        Returns:
            Baseline statistics
        """
        stats_dict = {}

        for col in df.columns:
            col_stats = {
                'dtype': str(df[col].dtype),
                'count': len(df[col]),
                'missing_pct': df[col].isna().sum() / len(df) * 100,
                'unique': df[col].nunique()
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                col_stats.update({
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'median': df[col].median(),
                    'q1': df[col].quantile(0.25),
                    'q3': df[col].quantile(0.75)
                })

            stats_dict[col] = col_stats

        self.baseline_stats = stats_dict
        return stats_dict

    def check_quality(self, df: pd.DataFrame) -> Dict:
        """
        Check data quality against baseline.

        Args:
            df: DataFrame to check

        Returns:
            Quality report
        """
        self.issues = []
        quality_report = {
            'overall_score': 100,
            'columns': {},
            'issues': []
        }

        score_deductions = 0

        for col in df.columns:
            col_issues = []

            # Check if column exists in baseline
            if col not in self.baseline_stats:
                col_issues.append(f"New column not in baseline")
                score_deductions += 5
                continue

            baseline = self.baseline_stats[col]

            # Check missing values
            missing_pct = df[col].isna().sum() / len(df) * 100
            if missing_pct > baseline.get('missing_pct', 0) + 5:
                col_issues.append(f"Missing values increased: {missing_pct:.1f}% vs {baseline['missing_pct']:.1f}%")
                score_deductions += 10

            # Check data types
            if str(df[col].dtype) != baseline['dtype']:
                col_issues.append(f"Data type changed: {df[col].dtype} vs {baseline['dtype']}")
                score_deductions += 15

            # Check numeric distributions
            if pd.api.types.is_numeric_dtype(df[col]):
                # Check for out-of-range values
                if df[col].min() < baseline['min'] * 0.5:
                    col_issues.append(f"Min value much lower: {df[col].min():.2f} vs {baseline['min']:.2f}")
                    score_deductions += 5

                if df[col].max() > baseline['max'] * 2:
                    col_issues.append(f"Max value much higher: {df[col].max():.2f} vs {baseline['max']:.2f}")
                    score_deductions += 5

                # Check mean shift
                mean_shift = abs(df[col].mean() - baseline['mean']) / (baseline['std'] + 1e-10)
                if mean_shift > 3:
                    col_issues.append(f"Mean shifted by {mean_shift:.1f} std")
                    score_deductions += 10

            quality_report['columns'][col] = {
                'issues': col_issues,
                'n_issues': len(col_issues)
            }

            self.issues.extend([f"{col}: {issue}" for issue in col_issues])

        quality_report['overall_score'] = max(0, 100 - score_deductions)
        quality_report['issues'] = self.issues

        return quality_report

    def detect_drift(
        self,
        reference: pd.DataFrame,
        current: pd.DataFrame,
        threshold: float = 0.05
    ) -> Dict:
        """
        Detect data drift using statistical tests.

        Args:
            reference: Reference (training) data
            current: Current (production) data
            threshold: P-value threshold

        Returns:
            Drift report
        """
        drift_report = {
            'drifted_features': [],
            'details': {}
        }

        for col in reference.columns:
            if col not in current.columns:
                continue

            if pd.api.types.is_numeric_dtype(reference[col]):
                # Kolmogorov-Smirnov test
                ref_values = reference[col].dropna().values
                cur_values = current[col].dropna().values

                if len(ref_values) > 0 and len(cur_values) > 0:
                    ks_stat, p_value = stats.ks_2samp(ref_values, cur_values)

                    drift_report['details'][col] = {
                        'test': 'KS',
                        'statistic': round(ks_stat, 4),
                        'p_value': round(p_value, 4),
                        'drifted': p_value < threshold
                    }

                    if p_value < threshold:
                        drift_report['drifted_features'].append(col)
            else:
                # Chi-square test for categorical
                ref_counts = reference[col].value_counts()
                cur_counts = current[col].value_counts()

                # Align categories
                all_cats = set(ref_counts.index) | set(cur_counts.index)
                ref_aligned = [ref_counts.get(cat, 0) for cat in all_cats]
                cur_aligned = [cur_counts.get(cat, 0) for cat in all_cats]

                # Normalize
                ref_freq = np.array(ref_aligned) / sum(ref_aligned)
                cur_freq = np.array(cur_aligned) / sum(cur_aligned)

                # Jensen-Shannon divergence
                m = (ref_freq + cur_freq) / 2
                js_div = 0.5 * (stats.entropy(ref_freq, m) + stats.entropy(cur_freq, m))

                drift_report['details'][col] = {
                    'test': 'JS_divergence',
                    'statistic': round(js_div, 4),
                    'drifted': js_div > 0.1
                }

                if js_div > 0.1:
                    drift_report['drifted_features'].append(col)

        drift_report['n_drifted'] = len(drift_report['drifted_features'])
        drift_report['pct_drifted'] = round(
            len(drift_report['drifted_features']) / len(reference.columns) * 100, 1
        )

        return drift_report

    def validate_schema(
        self,
        df: pd.DataFrame,
        schema: Dict
    ) -> Dict:
        """
        Validate DataFrame against schema.

        Args:
            df: DataFrame to validate
            schema: Schema definition

        Returns:
            Validation results
        """
        errors = []
        warnings_list = []

        # Check required columns
        if 'required_columns' in schema:
            missing = set(schema['required_columns']) - set(df.columns)
            if missing:
                errors.append(f"Missing required columns: {missing}")

        # Check column types
        if 'column_types' in schema:
            for col, expected_type in schema['column_types'].items():
                if col in df.columns:
                    actual_type = str(df[col].dtype)
                    if expected_type not in actual_type:
                        errors.append(f"{col}: expected {expected_type}, got {actual_type}")

        # Check value ranges
        if 'value_ranges' in schema:
            for col, (min_val, max_val) in schema['value_ranges'].items():
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    if df[col].min() < min_val:
                        errors.append(f"{col}: values below minimum {min_val}")
                    if df[col].max() > max_val:
                        errors.append(f"{col}: values above maximum {max_val}")

        # Check unique constraints
        if 'unique_columns' in schema:
            for col in schema['unique_columns']:
                if col in df.columns:
                    if df[col].duplicated().any():
                        warnings_list.append(f"{col}: contains duplicates")

        # Check not null
        if 'not_null_columns' in schema:
            for col in schema['not_null_columns']:
                if col in df.columns:
                    null_count = df[col].isna().sum()
                    if null_count > 0:
                        errors.append(f"{col}: contains {null_count} null values")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings_list
        }


class ConceptDriftDetector:
    """
    Detect concept drift in model predictions.
    """

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.error_history = []
        self.drift_points = []

    def add_prediction(
        self,
        y_true: float,
        y_pred: float
    ) -> Dict:
        """
        Add a prediction and check for drift.

        Args:
            y_true: Actual value
            y_pred: Predicted value

        Returns:
            Drift status
        """
        error = abs(y_true - y_pred)
        self.error_history.append(error)

        result = {
            'drift_detected': False,
            'current_error': round(error, 4)
        }

        if len(self.error_history) < 2 * self.window_size:
            return result

        # Compare recent errors to baseline
        baseline = np.mean(self.error_history[-2*self.window_size:-self.window_size])
        recent = np.mean(self.error_history[-self.window_size:])

        baseline_std = np.std(self.error_history[-2*self.window_size:-self.window_size])

        # Check for significant increase
        if recent > baseline + 2 * baseline_std:
            result['drift_detected'] = True
            result['baseline_error'] = round(baseline, 4)
            result['recent_error'] = round(recent, 4)
            self.drift_points.append(len(self.error_history))

        return result

    def get_drift_report(self) -> Dict:
        """Get comprehensive drift report."""
        if len(self.error_history) == 0:
            return {'n_predictions': 0}

        return {
            'n_predictions': len(self.error_history),
            'n_drift_points': len(self.drift_points),
            'mean_error': round(np.mean(self.error_history), 4),
            'error_trend': 'increasing' if len(self.error_history) > 100 and
                          np.mean(self.error_history[-50:]) > np.mean(self.error_history[:50])
                          else 'stable',
            'drift_points': self.drift_points
        }

    def reset(self):
        """Reset detector."""
        self.error_history = []
        self.drift_points = []


class StatisticalTests:
    """
    Statistical tests for data analysis.
    """

    @staticmethod
    def normality_test(series: pd.Series) -> Dict:
        """
        Test for normality using multiple methods.

        Args:
            series: Data series

        Returns:
            Test results
        """
        values = series.dropna().values

        # Shapiro-Wilk (for n < 5000)
        if len(values) < 5000:
            sw_stat, sw_p = stats.shapiro(values[:5000])
        else:
            sw_stat, sw_p = stats.shapiro(values[:5000])

        # D'Agostino-Pearson
        if len(values) >= 20:
            dp_stat, dp_p = stats.normaltest(values)
        else:
            dp_stat, dp_p = np.nan, np.nan

        # Skewness and kurtosis
        skew = stats.skew(values)
        kurtosis = stats.kurtosis(values)

        is_normal = sw_p > 0.05 and (np.isnan(dp_p) or dp_p > 0.05)

        return {
            'is_normal': is_normal,
            'shapiro_wilk': {'statistic': round(sw_stat, 4), 'p_value': round(sw_p, 4)},
            'dagostino': {'statistic': round(dp_stat, 4) if not np.isnan(dp_stat) else None,
                        'p_value': round(dp_p, 4) if not np.isnan(dp_p) else None},
            'skewness': round(skew, 4),
            'kurtosis': round(kurtosis, 4)
        }

    @staticmethod
    def stationarity_test(series: pd.Series) -> Dict:
        """
        Test for stationarity using ADF test.

        Args:
            series: Time series

        Returns:
            Test results
        """
        from statsmodels.tsa.stattools import adfuller

        values = series.dropna().values
        result = adfuller(values, autolag='AIC')

        return {
            'is_stationary': result[1] < 0.05,
            'adf_statistic': round(result[0], 4),
            'p_value': round(result[1], 4),
            'critical_values': {k: round(v, 4) for k, v in result[4].items()},
            'n_lags': result[2]
        }

    @staticmethod
    def granger_causality(
        y: pd.Series,
        x: pd.Series,
        max_lag: int = 5
    ) -> Dict:
        """
        Test Granger causality.

        Does x help predict y?

        Args:
            y: Target series
            x: Potential causal series
            max_lag: Maximum lag to test

        Returns:
            Test results
        """
        from statsmodels.tsa.stattools import grangercausalitytests

        data = pd.concat([y, x], axis=1).dropna()
        data.columns = ['y', 'x']

        try:
            result = grangercausalitytests(data, maxlag=max_lag, verbose=False)

            # Get best lag
            best_lag = 1
            best_p = 1

            for lag in range(1, max_lag + 1):
                p_value = result[lag][0]['ssr_ftest'][1]
                if p_value < best_p:
                    best_p = p_value
                    best_lag = lag

            return {
                'granger_causes': best_p < 0.05,
                'best_lag': best_lag,
                'p_value': round(best_p, 4)
            }
        except:
            return {
                'granger_causes': False,
                'error': 'Test failed'
            }

    @staticmethod
    def cointegration_test(
        series1: pd.Series,
        series2: pd.Series
    ) -> Dict:
        """
        Test for cointegration between two series.

        Args:
            series1: First series
            series2: Second series

        Returns:
            Test results
        """
        from statsmodels.tsa.stattools import coint

        values1 = series1.dropna().values
        values2 = series2.dropna().values

        # Align lengths
        min_len = min(len(values1), len(values2))
        values1 = values1[:min_len]
        values2 = values2[:min_len]

        try:
            coint_stat, p_value, crit_values = coint(values1, values2)

            return {
                'is_cointegrated': p_value < 0.05,
                'statistic': round(coint_stat, 4),
                'p_value': round(p_value, 4),
                'critical_values': {
                    '1%': round(crit_values[0], 4),
                    '5%': round(crit_values[1], 4),
                    '10%': round(crit_values[2], 4)
                }
            }
        except:
            return {
                'is_cointegrated': False,
                'error': 'Test failed'
            }
