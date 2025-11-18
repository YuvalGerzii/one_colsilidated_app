"""
Extreme Value Theory (EVT) Model
Implements statistical methods for modeling extreme events and tail risks
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import stats


class ExtremeValueTheoryModel:
    """
    Implements Extreme Value Theory for tail risk estimation
    Uses both Peak Over Threshold (POT) and Block Maxima methods
    """

    def __init__(self, config: Dict):
        """
        Initialize EVT model

        Args:
            config: Configuration dictionary with EVT parameters
        """
        self.config = config
        self.threshold = None
        self.shape_param = None  # xi (tail index)
        self.scale_param = None  # sigma
        self.location_param = None  # mu

    def fit_generalized_pareto(self, data: np.ndarray, threshold_percentile: float = 0.95) -> Dict:
        """
        Fit Generalized Pareto Distribution (GPD) using Peak Over Threshold method

        Args:
            data: Historical loss data (positive values)
            threshold_percentile: Percentile to use as threshold (default 95%)

        Returns:
            Dictionary with fitted parameters
        """
        # Calculate threshold
        self.threshold = np.percentile(data, threshold_percentile * 100)

        # Extract exceedances (values above threshold)
        exceedances = data[data > self.threshold] - self.threshold

        if len(exceedances) < 10:
            raise ValueError(f"Insufficient exceedances ({len(exceedances)}). Lower threshold.")

        # Fit GPD to exceedances
        self.shape_param, self.location_param, self.scale_param = stats.genpareto.fit(exceedances)

        return {
            'threshold': self.threshold,
            'shape_xi': self.shape_param,
            'scale_sigma': self.scale_param,
            'location_mu': self.location_param,
            'num_exceedances': len(exceedances),
            'exceedance_rate': len(exceedances) / len(data)
        }

    def fit_generalized_extreme_value(self, data: np.ndarray, block_size: int = 20) -> Dict:
        """
        Fit Generalized Extreme Value (GEV) distribution using Block Maxima method

        Args:
            data: Historical data
            block_size: Size of blocks for extracting maxima

        Returns:
            Dictionary with fitted parameters
        """
        # Extract block maxima
        num_blocks = len(data) // block_size
        block_maxima = []

        for i in range(num_blocks):
            block = data[i * block_size:(i + 1) * block_size]
            block_maxima.append(np.max(np.abs(block)))

        block_maxima = np.array(block_maxima)

        # Fit GEV distribution
        self.shape_param, self.location_param, self.scale_param = stats.genextreme.fit(block_maxima)

        return {
            'shape_xi': self.shape_param,
            'location_mu': self.location_param,
            'scale_sigma': self.scale_param,
            'num_blocks': num_blocks,
            'block_size': block_size
        }

    def calculate_var(self, confidence_level: float, method: str = 'gpd') -> float:
        """
        Calculate Value at Risk (VaR) using EVT

        Args:
            confidence_level: Confidence level (e.g., 0.95, 0.99)
            method: 'gpd' for Generalized Pareto or 'gev' for GEV

        Returns:
            VaR estimate
        """
        if self.shape_param is None:
            raise ValueError("Model not fitted. Call fit_generalized_pareto or fit_generalized_extreme_value first.")

        if method == 'gpd':
            # VaR for GPD
            if self.shape_param != 0:
                var = self.threshold + (self.scale_param / self.shape_param) * \
                      ((1 - confidence_level) ** (-self.shape_param) - 1)
            else:
                var = self.threshold - self.scale_param * np.log(1 - confidence_level)

        elif method == 'gev':
            # VaR for GEV
            if self.shape_param != 0:
                var = self.location_param - (self.scale_param / self.shape_param) * \
                      (1 - (-np.log(confidence_level)) ** (-self.shape_param))
            else:
                var = self.location_param - self.scale_param * np.log(-np.log(confidence_level))

        else:
            raise ValueError(f"Unknown method: {method}")

        return float(var)

    def calculate_cvar(self, confidence_level: float, method: str = 'gpd') -> float:
        """
        Calculate Conditional Value at Risk (CVaR / Expected Shortfall)

        Args:
            confidence_level: Confidence level (e.g., 0.95, 0.99)
            method: 'gpd' or 'gev'

        Returns:
            CVaR estimate
        """
        var = self.calculate_var(confidence_level, method)

        if method == 'gpd':
            # CVaR for GPD
            if self.shape_param < 1 and self.shape_param != 0:
                cvar = var / (1 - self.shape_param) + \
                       (self.scale_param - self.shape_param * self.threshold) / (1 - self.shape_param)
            else:
                cvar = var + self.scale_param  # Approximation when xi >= 1

        elif method == 'gev':
            # CVaR for GEV (approximation)
            if self.shape_param < 1 and self.shape_param != 0:
                cvar = var + (self.scale_param + self.shape_param * (var - self.location_param)) / (1 - self.shape_param)
            else:
                cvar = var + self.scale_param

        else:
            raise ValueError(f"Unknown method: {method}")

        return float(cvar)

    def calculate_return_level(self, return_period: int, method: str = 'gpd') -> float:
        """
        Calculate return level (expected extreme value for given return period)

        Args:
            return_period: Return period in days (e.g., 100 for 100-day event)
            method: 'gpd' or 'gev'

        Returns:
            Return level estimate
        """
        probability = 1.0 / return_period

        if method == 'gpd':
            # Return level for GPD
            if self.shape_param != 0:
                return_level = self.threshold + (self.scale_param / self.shape_param) * \
                               (probability ** (-self.shape_param) - 1)
            else:
                return_level = self.threshold - self.scale_param * np.log(probability)

        elif method == 'gev':
            # Return level for GEV
            if self.shape_param != 0:
                return_level = self.location_param - (self.scale_param / self.shape_param) * \
                               (1 - (-np.log(1 - probability)) ** (-self.shape_param))
            else:
                return_level = self.location_param - self.scale_param * np.log(-np.log(1 - probability))

        else:
            raise ValueError(f"Unknown method: {method}")

        return float(return_level)

    def estimate_tail_index(self, data: np.ndarray) -> Dict:
        """
        Estimate tail index using Hill estimator
        Determines how heavy the tail is (higher = heavier tail)

        Args:
            data: Historical data

        Returns:
            Dictionary with tail index estimates
        """
        # Sort data in descending order
        sorted_data = np.sort(np.abs(data))[::-1]

        # Use top 5% for Hill estimator
        k = int(len(sorted_data) * 0.05)

        if k < 10:
            k = min(10, len(sorted_data) - 1)

        # Hill estimator
        hill_estimate = np.mean(np.log(sorted_data[:k])) - np.log(sorted_data[k])

        # Interpret tail index
        if hill_estimate > 0.5:
            tail_type = "Heavy tail (high extreme event risk)"
        elif hill_estimate > 0.25:
            tail_type = "Moderate tail"
        else:
            tail_type = "Light tail"

        return {
            'hill_estimator': hill_estimate,
            'tail_type': tail_type,
            'observations_used': k,
            'interpretation': f"α = 1/ξ = {1/hill_estimate:.2f}" if hill_estimate > 0 else "Normal-like tail"
        }

    def predict_extreme_event_probability(self, threshold: float, time_horizon_days: int) -> float:
        """
        Predict probability of extreme event exceeding threshold in time horizon

        Args:
            threshold: Loss threshold
            time_horizon_days: Time horizon in days

        Returns:
            Probability of exceedance
        """
        if self.shape_param is None:
            raise ValueError("Model not fitted.")

        # Probability of exceeding threshold in one period
        if threshold <= self.threshold:
            # Use empirical probability below threshold
            prob_one_period = 0.05  # Conservative estimate
        else:
            # Use GPD for exceedances above threshold
            exceedance = threshold - self.threshold
            if self.shape_param != 0:
                prob_one_period = (1 + self.shape_param * exceedance / self.scale_param) ** (-1 / self.shape_param)
            else:
                prob_one_period = np.exp(-exceedance / self.scale_param)

        # Probability over time horizon (assuming independence)
        prob_horizon = 1 - (1 - prob_one_period) ** time_horizon_days

        return float(prob_horizon)

    def generate_summary_report(self) -> Dict:
        """
        Generate comprehensive summary of EVT analysis

        Returns:
            Dictionary with summary statistics
        """
        if self.shape_param is None:
            return {'error': 'Model not fitted'}

        var_95 = self.calculate_var(0.95)
        var_99 = self.calculate_var(0.99)
        var_995 = self.calculate_var(0.995)

        cvar_95 = self.calculate_cvar(0.95)
        cvar_99 = self.calculate_cvar(0.99)

        return_100d = self.calculate_return_level(100)
        return_250d = self.calculate_return_level(250)

        return {
            'model_parameters': {
                'shape_xi': self.shape_param,
                'scale_sigma': self.scale_param,
                'location_mu': self.location_param,
                'threshold': self.threshold
            },
            'risk_metrics': {
                'var_95': var_95,
                'var_99': var_99,
                'var_995': var_995,
                'cvar_95': cvar_95,
                'cvar_99': cvar_99
            },
            'return_levels': {
                '100_day_event': return_100d,
                '250_day_event': return_250d
            },
            'interpretation': {
                'tail_behavior': 'Heavy tail' if self.shape_param > 0.5 else 'Moderate tail' if self.shape_param > 0 else 'Light tail',
                'extreme_risk': 'High' if self.shape_param > 0.3 else 'Moderate' if self.shape_param > 0 else 'Low'
            }
        }
