"""
Advanced Trend Detection Module
================================

Comprehensive trend detection including change point detection,
structural breaks, and trend analysis algorithms.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from scipy.signal import find_peaks, savgol_filter
import warnings

warnings.filterwarnings('ignore')


class TrendDetector:
    """
    Advanced trend detection and change point analysis.
    """

    def __init__(self):
        self.trends = {}
        self.change_points = []
        self.patterns = {}

    def detect_linear_trend(
        self,
        series: pd.Series,
        significance_level: float = 0.05
    ) -> Dict:
        """
        Detect linear trend using regression.

        Args:
            series: Time series data
            significance_level: P-value threshold

        Returns:
            Dictionary with trend analysis
        """
        x = np.arange(len(series))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, series.values)

        # Determine trend direction
        if p_value < significance_level:
            if slope > 0:
                trend = 'increasing'
            else:
                trend = 'decreasing'
        else:
            trend = 'no_significant_trend'

        # Calculate trend strength
        trend_strength = abs(r_value)

        return {
            'trend': trend,
            'slope': round(slope, 6),
            'intercept': round(intercept, 4),
            'r_squared': round(r_value ** 2, 4),
            'p_value': round(p_value, 4),
            'std_err': round(std_err, 6),
            'trend_strength': round(trend_strength, 4),
            'is_significant': p_value < significance_level
        }

    def mann_kendall_test(
        self,
        series: pd.Series
    ) -> Dict:
        """
        Mann-Kendall trend test for monotonic trends.

        Args:
            series: Time series data

        Returns:
            Dictionary with test results
        """
        n = len(series)
        s = 0

        # Calculate S statistic
        for i in range(n - 1):
            for j in range(i + 1, n):
                diff = series.iloc[j] - series.iloc[i]
                s += np.sign(diff)

        # Calculate variance
        # Adjust for ties
        unique, counts = np.unique(series.values, return_counts=True)
        tie_correction = sum(t * (t - 1) * (2 * t + 5) for t in counts if t > 1)

        var_s = (n * (n - 1) * (2 * n + 5) - tie_correction) / 18

        # Calculate Z statistic
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0

        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

        # Determine trend
        if z > 0:
            trend = 'increasing'
        elif z < 0:
            trend = 'decreasing'
        else:
            trend = 'no_trend'

        # Sen's slope estimator
        slopes = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                if j - i > 0:
                    slope = (series.iloc[j] - series.iloc[i]) / (j - i)
                    slopes.append(slope)
        sen_slope = np.median(slopes) if slopes else 0

        return {
            'trend': trend,
            's_statistic': int(s),
            'z_statistic': round(z, 4),
            'p_value': round(p_value, 4),
            'sen_slope': round(sen_slope, 6),
            'is_significant': p_value < 0.05
        }

    def detect_change_points_cusum(
        self,
        series: pd.Series,
        threshold: float = None
    ) -> List[int]:
        """
        Detect change points using CUSUM algorithm.

        Args:
            series: Time series data
            threshold: Detection threshold

        Returns:
            List of change point indices
        """
        values = series.values
        mean = np.mean(values)
        std = np.std(values)

        if threshold is None:
            threshold = 4 * std

        # Calculate cumulative sum
        cusum_pos = np.zeros(len(values))
        cusum_neg = np.zeros(len(values))

        change_points = []

        for i in range(1, len(values)):
            cusum_pos[i] = max(0, cusum_pos[i-1] + (values[i] - mean - 0.5 * std))
            cusum_neg[i] = max(0, cusum_neg[i-1] - (values[i] - mean + 0.5 * std))

            if cusum_pos[i] > threshold or cusum_neg[i] > threshold:
                change_points.append(i)
                # Reset CUSUM
                cusum_pos[i] = 0
                cusum_neg[i] = 0

        self.change_points = change_points
        return change_points

    def detect_change_points_pelt(
        self,
        series: pd.Series,
        penalty: str = 'bic',
        min_size: int = 2
    ) -> List[int]:
        """
        Detect change points using PELT algorithm (requires ruptures).

        Args:
            series: Time series data
            penalty: Penalty method ('bic', 'aic', or numeric)
            min_size: Minimum segment size

        Returns:
            List of change point indices
        """
        try:
            import ruptures as rpt
        except ImportError:
            # Fallback to binary segmentation
            return self.detect_change_points_binary_segmentation(series)

        values = series.values

        # Fit PELT algorithm
        model = rpt.Pelt(model="rbf", min_size=min_size).fit(values)

        # Detect change points
        if penalty == 'bic':
            pen = np.log(len(values)) * np.var(values)
        elif penalty == 'aic':
            pen = 2 * np.var(values)
        else:
            pen = float(penalty)

        change_points = model.predict(pen=pen)

        # Remove last point (end of series)
        if change_points and change_points[-1] == len(values):
            change_points = change_points[:-1]

        self.change_points = change_points
        return change_points

    def detect_change_points_binary_segmentation(
        self,
        series: pd.Series,
        n_bkps: int = 5,
        min_size: int = 5
    ) -> List[int]:
        """
        Detect change points using binary segmentation.

        Args:
            series: Time series data
            n_bkps: Number of breakpoints to detect
            min_size: Minimum segment size

        Returns:
            List of change point indices
        """
        values = series.values
        n = len(values)

        def cost(start, end):
            """Calculate cost of segment."""
            segment = values[start:end]
            if len(segment) < 2:
                return 0
            return len(segment) * np.var(segment)

        def find_best_split(start, end):
            """Find best split point in segment."""
            if end - start < 2 * min_size:
                return None, np.inf

            best_split = None
            best_cost = np.inf

            for i in range(start + min_size, end - min_size + 1):
                total_cost = cost(start, i) + cost(i, end)
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_split = i

            return best_split, best_cost

        # Binary segmentation
        segments = [(0, n)]
        change_points = []

        while len(change_points) < n_bkps and segments:
            # Find best split among all segments
            best_segment = None
            best_split = None
            best_gain = -np.inf

            for start, end in segments:
                split, split_cost = find_best_split(start, end)
                if split is not None:
                    current_cost = cost(start, end)
                    gain = current_cost - split_cost
                    if gain > best_gain:
                        best_gain = gain
                        best_split = split
                        best_segment = (start, end)

            if best_segment is None or best_gain <= 0:
                break

            # Add change point and update segments
            change_points.append(best_split)
            segments.remove(best_segment)
            segments.append((best_segment[0], best_split))
            segments.append((best_split, best_segment[1]))

        self.change_points = sorted(change_points)
        return self.change_points

    def detect_structural_breaks(
        self,
        series: pd.Series,
        exog: pd.DataFrame = None,
        max_breaks: int = 5
    ) -> Dict:
        """
        Detect structural breaks (Chow test style).

        Args:
            series: Time series data
            exog: Exogenous variables
            max_breaks: Maximum number of breaks

        Returns:
            Dictionary with break analysis
        """
        n = len(series)
        values = series.values

        breaks = []
        f_stats = []

        # Test each potential break point
        for i in range(int(n * 0.15), int(n * 0.85)):
            # Split data
            y1, y2 = values[:i], values[i:]

            if len(y1) < 5 or len(y2) < 5:
                continue

            # Calculate SSR
            ssr_total = np.sum((values - np.mean(values)) ** 2)
            ssr1 = np.sum((y1 - np.mean(y1)) ** 2)
            ssr2 = np.sum((y2 - np.mean(y2)) ** 2)

            # F-statistic
            k = 2  # number of parameters
            numerator = (ssr_total - (ssr1 + ssr2)) / k
            denominator = (ssr1 + ssr2) / (n - 2 * k)

            if denominator > 0:
                f_stat = numerator / denominator
                f_stats.append((i, f_stat))

        # Find significant breaks
        if f_stats:
            f_stats.sort(key=lambda x: x[1], reverse=True)
            breaks = [f[0] for f in f_stats[:max_breaks] if f[1] > 3.84]  # chi2(1, 0.95)

        return {
            'breaks': sorted(breaks),
            'n_breaks': len(breaks),
            'top_f_stats': [(idx, round(f, 2)) for idx, f in f_stats[:5]]
        }

    def detect_seasonality(
        self,
        series: pd.Series,
        max_lag: int = None
    ) -> Dict:
        """
        Detect seasonality using autocorrelation.

        Args:
            series: Time series data
            max_lag: Maximum lag to check

        Returns:
            Dictionary with seasonality analysis
        """
        n = len(series)
        if max_lag is None:
            max_lag = min(365, n // 2)

        # Calculate autocorrelation
        autocorr = []
        for lag in range(1, max_lag):
            if lag < n:
                corr = series.autocorr(lag=lag)
                autocorr.append(corr)
            else:
                autocorr.append(0)

        autocorr = np.array(autocorr)

        # Find peaks (seasonal periods)
        peaks, properties = find_peaks(autocorr, height=0.1, distance=3)

        # Get top seasonal periods
        if len(peaks) > 0:
            peak_values = autocorr[peaks]
            sorted_idx = np.argsort(peak_values)[::-1]
            top_peaks = peaks[sorted_idx][:5] + 1  # Convert to 1-based

            seasonal_periods = top_peaks.tolist()
            seasonal_strengths = [round(autocorr[p-1], 4) for p in seasonal_periods]
        else:
            seasonal_periods = []
            seasonal_strengths = []

        # Determine primary seasonality
        if seasonal_periods:
            primary_period = seasonal_periods[0]
            if primary_period == 7:
                seasonality_type = 'weekly'
            elif primary_period in [30, 31]:
                seasonality_type = 'monthly'
            elif primary_period in [90, 91, 92]:
                seasonality_type = 'quarterly'
            elif primary_period in [365, 366]:
                seasonality_type = 'yearly'
            else:
                seasonality_type = f'{primary_period}-period'
        else:
            seasonality_type = 'none'

        return {
            'has_seasonality': len(seasonal_periods) > 0,
            'seasonality_type': seasonality_type,
            'seasonal_periods': seasonal_periods,
            'seasonal_strengths': seasonal_strengths
        }

    def smooth_trend(
        self,
        series: pd.Series,
        method: str = 'savgol',
        window: int = 11,
        poly_order: int = 3
    ) -> pd.Series:
        """
        Smooth series to extract trend.

        Args:
            series: Time series data
            method: Smoothing method
            window: Window size
            poly_order: Polynomial order for savgol

        Returns:
            Smoothed series
        """
        if method == 'savgol':
            # Ensure window is odd
            if window % 2 == 0:
                window += 1
            smoothed = savgol_filter(series.values, window, poly_order)
        elif method == 'rolling':
            smoothed = series.rolling(window=window, center=True).mean().values
        elif method == 'ewma':
            smoothed = series.ewm(span=window).mean().values
        else:
            smoothed = series.values

        return pd.Series(smoothed, index=series.index)

    def decompose_trend_seasonality(
        self,
        series: pd.Series,
        period: int = None,
        model: str = 'additive'
    ) -> Dict:
        """
        Decompose series into trend, seasonal, and residual.

        Args:
            series: Time series data
            period: Seasonal period
            model: 'additive' or 'multiplicative'

        Returns:
            Dictionary with decomposition components
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
        except ImportError:
            return {"error": "statsmodels not installed"}

        if period is None:
            # Auto-detect period
            seasonality = self.detect_seasonality(series)
            if seasonality['seasonal_periods']:
                period = seasonality['seasonal_periods'][0]
            else:
                period = min(12, len(series) // 2)

        decomposition = seasonal_decompose(
            series,
            model=model,
            period=period,
            extrapolate_trend='freq'
        )

        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'observed': decomposition.observed,
            'period': period,
            'model': model
        }

    def calculate_trend_momentum(
        self,
        series: pd.Series,
        periods: List[int] = [7, 14, 30]
    ) -> Dict:
        """
        Calculate trend momentum indicators.

        Args:
            series: Time series data
            periods: Periods for momentum calculation

        Returns:
            Dictionary with momentum indicators
        """
        result = {}

        for period in periods:
            if len(series) > period:
                # Rate of change
                roc = ((series.iloc[-1] - series.iloc[-period-1]) /
                       series.iloc[-period-1] * 100)

                # Moving average
                ma = series.rolling(period).mean().iloc[-1]

                # Trend direction
                if series.iloc[-1] > ma:
                    direction = 'above_ma'
                else:
                    direction = 'below_ma'

                result[f'{period}d'] = {
                    'roc': round(roc, 2),
                    'ma': round(ma, 4),
                    'direction': direction,
                    'current_vs_ma': round((series.iloc[-1] - ma) / ma * 100, 2)
                }

        return result

    def identify_patterns(
        self,
        series: pd.Series,
        pattern_types: List[str] = None
    ) -> Dict:
        """
        Identify common patterns in time series.

        Args:
            series: Time series data
            pattern_types: Patterns to look for

        Returns:
            Dictionary with identified patterns
        """
        if pattern_types is None:
            pattern_types = ['double_top', 'double_bottom', 'head_shoulders']

        patterns = {}
        values = series.values
        n = len(values)

        # Find local maxima and minima
        peaks, _ = find_peaks(values, distance=n // 20)
        valleys, _ = find_peaks(-values, distance=n // 20)

        # Double top pattern
        if 'double_top' in pattern_types and len(peaks) >= 2:
            # Check for two similar peaks
            for i in range(len(peaks) - 1):
                peak1_val = values[peaks[i]]
                peak2_val = values[peaks[i + 1]]

                # Peaks within 5% of each other
                if abs(peak1_val - peak2_val) / peak1_val < 0.05:
                    patterns['double_top'] = {
                        'detected': True,
                        'peaks': [int(peaks[i]), int(peaks[i + 1])],
                        'values': [round(peak1_val, 4), round(peak2_val, 4)]
                    }
                    break
            else:
                patterns['double_top'] = {'detected': False}

        # Double bottom pattern
        if 'double_bottom' in pattern_types and len(valleys) >= 2:
            for i in range(len(valleys) - 1):
                valley1_val = values[valleys[i]]
                valley2_val = values[valleys[i + 1]]

                if abs(valley1_val - valley2_val) / valley1_val < 0.05:
                    patterns['double_bottom'] = {
                        'detected': True,
                        'valleys': [int(valleys[i]), int(valleys[i + 1])],
                        'values': [round(valley1_val, 4), round(valley2_val, 4)]
                    }
                    break
            else:
                patterns['double_bottom'] = {'detected': False}

        self.patterns = patterns
        return patterns

    def get_trend_summary(
        self,
        series: pd.Series
    ) -> Dict:
        """
        Get comprehensive trend summary.

        Args:
            series: Time series data

        Returns:
            Dictionary with trend summary
        """
        return {
            'linear_trend': self.detect_linear_trend(series),
            'mann_kendall': self.mann_kendall_test(series),
            'seasonality': self.detect_seasonality(series),
            'momentum': self.calculate_trend_momentum(series)
        }
