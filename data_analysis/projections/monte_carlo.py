"""
Monte Carlo Simulation Module
==============================

Advanced Monte Carlo simulations for risk analysis
and probabilistic forecasting.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Callable
from scipy import stats
import warnings

warnings.filterwarnings('ignore')


class MonteCarloSimulator:
    """
    Monte Carlo simulation for risk analysis and forecasting.
    """

    def __init__(self, n_simulations: int = 10000, random_seed: int = 42):
        """
        Initialize simulator.

        Args:
            n_simulations: Number of simulations
            random_seed: Random seed for reproducibility
        """
        self.n_simulations = n_simulations
        self.random_seed = random_seed
        self.simulations = None
        self.results = {}
        np.random.seed(random_seed)

    def simulate_geometric_brownian_motion(
        self,
        initial_value: float,
        drift: float,
        volatility: float,
        periods: int,
        dt: float = 1/252
    ) -> np.ndarray:
        """
        Simulate paths using Geometric Brownian Motion.

        Args:
            initial_value: Starting value
            drift: Drift (expected return)
            volatility: Volatility (standard deviation)
            periods: Number of periods
            dt: Time step

        Returns:
            Array of simulated paths (n_simulations x periods)
        """
        # Generate random shocks
        Z = np.random.standard_normal((self.n_simulations, periods))

        # GBM formula
        paths = np.zeros((self.n_simulations, periods + 1))
        paths[:, 0] = initial_value

        for t in range(1, periods + 1):
            paths[:, t] = paths[:, t-1] * np.exp(
                (drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * Z[:, t-1]
            )

        self.simulations = paths[:, 1:]
        return self.simulations

    def simulate_mean_reverting(
        self,
        initial_value: float,
        mean: float,
        speed: float,
        volatility: float,
        periods: int
    ) -> np.ndarray:
        """
        Simulate mean-reverting process (Ornstein-Uhlenbeck).

        Args:
            initial_value: Starting value
            mean: Long-term mean
            speed: Speed of mean reversion
            volatility: Volatility
            periods: Number of periods

        Returns:
            Array of simulated paths
        """
        dt = 1

        paths = np.zeros((self.n_simulations, periods + 1))
        paths[:, 0] = initial_value

        for t in range(1, periods + 1):
            dW = np.random.standard_normal(self.n_simulations) * np.sqrt(dt)
            paths[:, t] = paths[:, t-1] + speed * (mean - paths[:, t-1]) * dt + volatility * dW

        self.simulations = paths[:, 1:]
        return self.simulations

    def simulate_jump_diffusion(
        self,
        initial_value: float,
        drift: float,
        volatility: float,
        jump_intensity: float,
        jump_mean: float,
        jump_std: float,
        periods: int
    ) -> np.ndarray:
        """
        Simulate Merton's jump-diffusion process.

        Args:
            initial_value: Starting value
            drift: Drift rate
            volatility: Diffusion volatility
            jump_intensity: Average number of jumps per period
            jump_mean: Mean jump size
            jump_std: Jump size standard deviation
            periods: Number of periods

        Returns:
            Array of simulated paths
        """
        dt = 1

        paths = np.zeros((self.n_simulations, periods + 1))
        paths[:, 0] = initial_value

        for t in range(1, periods + 1):
            # Diffusion component
            dW = np.random.standard_normal(self.n_simulations) * np.sqrt(dt)
            diffusion = (drift - 0.5 * volatility**2) * dt + volatility * dW

            # Jump component
            n_jumps = np.random.poisson(jump_intensity * dt, self.n_simulations)
            jumps = np.zeros(self.n_simulations)
            for i in range(self.n_simulations):
                if n_jumps[i] > 0:
                    jumps[i] = np.sum(np.random.normal(jump_mean, jump_std, n_jumps[i]))

            paths[:, t] = paths[:, t-1] * np.exp(diffusion + jumps)

        self.simulations = paths[:, 1:]
        return self.simulations

    def simulate_bootstrap(
        self,
        historical_returns: np.ndarray,
        initial_value: float,
        periods: int,
        block_size: int = 1
    ) -> np.ndarray:
        """
        Bootstrap simulation from historical returns.

        Args:
            historical_returns: Historical return series
            initial_value: Starting value
            periods: Number of periods
            block_size: Block size for block bootstrap

        Returns:
            Array of simulated paths
        """
        n_returns = len(historical_returns)

        if block_size == 1:
            # Simple bootstrap
            indices = np.random.randint(0, n_returns, (self.n_simulations, periods))
            sampled_returns = historical_returns[indices]
        else:
            # Block bootstrap
            n_blocks = int(np.ceil(periods / block_size))
            sampled_returns = np.zeros((self.n_simulations, periods))

            for sim in range(self.n_simulations):
                returns = []
                for _ in range(n_blocks):
                    start = np.random.randint(0, n_returns - block_size + 1)
                    returns.extend(historical_returns[start:start + block_size])
                sampled_returns[sim] = returns[:periods]

        # Convert returns to prices
        paths = np.zeros((self.n_simulations, periods + 1))
        paths[:, 0] = initial_value
        for t in range(1, periods + 1):
            paths[:, t] = paths[:, t-1] * (1 + sampled_returns[:, t-1])

        self.simulations = paths[:, 1:]
        return self.simulations

    def calculate_var(
        self,
        confidence_level: float = 0.95,
        horizon: int = -1
    ) -> float:
        """
        Calculate Value at Risk.

        Args:
            confidence_level: Confidence level (e.g., 0.95)
            horizon: Time horizon (default: final period)

        Returns:
            VaR value
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        final_values = self.simulations[:, horizon]
        initial_value = self.simulations[:, 0].mean() if horizon != 0 else self.simulations[:, 0].mean()

        returns = (final_values - initial_value) / initial_value
        var = np.percentile(returns, (1 - confidence_level) * 100)

        self.results['var'] = {
            'confidence': confidence_level,
            'value': round(var, 4),
            'dollar_value': round(initial_value * var, 2)
        }

        return var

    def calculate_cvar(
        self,
        confidence_level: float = 0.95,
        horizon: int = -1
    ) -> float:
        """
        Calculate Conditional Value at Risk (Expected Shortfall).

        Args:
            confidence_level: Confidence level
            horizon: Time horizon

        Returns:
            CVaR value
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        final_values = self.simulations[:, horizon]
        initial_value = self.simulations[:, 0].mean() if horizon != 0 else self.simulations[:, 0].mean()

        returns = (final_values - initial_value) / initial_value
        var = np.percentile(returns, (1 - confidence_level) * 100)
        cvar = returns[returns <= var].mean()

        self.results['cvar'] = {
            'confidence': confidence_level,
            'value': round(cvar, 4),
            'dollar_value': round(initial_value * cvar, 2)
        }

        return cvar

    def get_percentiles(
        self,
        percentiles: List[float] = [5, 25, 50, 75, 95],
        horizon: int = -1
    ) -> Dict[int, float]:
        """
        Get percentile values at specified horizon.

        Args:
            percentiles: List of percentiles
            horizon: Time horizon

        Returns:
            Dictionary of percentile values
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        final_values = self.simulations[:, horizon]

        result = {}
        for p in percentiles:
            result[p] = round(np.percentile(final_values, p), 2)

        self.results['percentiles'] = result
        return result

    def get_probability_of_target(
        self,
        target: float,
        comparison: str = 'above',
        horizon: int = -1
    ) -> float:
        """
        Calculate probability of reaching target.

        Args:
            target: Target value
            comparison: 'above' or 'below'
            horizon: Time horizon

        Returns:
            Probability
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        final_values = self.simulations[:, horizon]

        if comparison == 'above':
            prob = np.mean(final_values >= target)
        else:
            prob = np.mean(final_values <= target)

        self.results['target_probability'] = {
            'target': target,
            'comparison': comparison,
            'probability': round(prob, 4)
        }

        return prob

    def get_confidence_intervals(
        self,
        confidence_level: float = 0.95
    ) -> pd.DataFrame:
        """
        Get confidence intervals for all periods.

        Args:
            confidence_level: Confidence level

        Returns:
            DataFrame with confidence intervals
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        alpha = (1 - confidence_level) / 2
        lower_pct = alpha * 100
        upper_pct = (1 - alpha) * 100

        mean = np.mean(self.simulations, axis=0)
        median = np.median(self.simulations, axis=0)
        lower = np.percentile(self.simulations, lower_pct, axis=0)
        upper = np.percentile(self.simulations, upper_pct, axis=0)

        return pd.DataFrame({
            'Period': range(1, self.simulations.shape[1] + 1),
            'Mean': mean.round(2),
            'Median': median.round(2),
            f'Lower_{int(confidence_level*100)}%': lower.round(2),
            f'Upper_{int(confidence_level*100)}%': upper.round(2)
        })

    def get_statistics(
        self,
        horizon: int = -1
    ) -> Dict:
        """
        Get comprehensive statistics.

        Args:
            horizon: Time horizon

        Returns:
            Dictionary of statistics
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        final_values = self.simulations[:, horizon]

        return {
            'mean': round(np.mean(final_values), 2),
            'median': round(np.median(final_values), 2),
            'std': round(np.std(final_values), 2),
            'min': round(np.min(final_values), 2),
            'max': round(np.max(final_values), 2),
            'skewness': round(stats.skew(final_values), 4),
            'kurtosis': round(stats.kurtosis(final_values), 4),
            'n_simulations': self.n_simulations
        }

    def run_risk_analysis(
        self,
        initial_value: float,
        drift: float,
        volatility: float,
        periods: int,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Run comprehensive risk analysis.

        Args:
            initial_value: Starting value
            drift: Expected return
            volatility: Volatility
            periods: Number of periods
            confidence_level: Confidence level

        Returns:
            Comprehensive risk analysis results
        """
        # Run simulation
        self.simulate_geometric_brownian_motion(
            initial_value, drift, volatility, periods
        )

        # Calculate risk metrics
        var = self.calculate_var(confidence_level)
        cvar = self.calculate_cvar(confidence_level)
        percentiles = self.get_percentiles()
        stats_dict = self.get_statistics()

        # Probability analysis
        prob_profit = self.get_probability_of_target(initial_value, 'above')
        prob_20pct_loss = self.get_probability_of_target(initial_value * 0.8, 'below')

        return {
            'input_parameters': {
                'initial_value': initial_value,
                'drift': drift,
                'volatility': volatility,
                'periods': periods
            },
            'statistics': stats_dict,
            'percentiles': percentiles,
            'var': {
                'confidence': confidence_level,
                'value': round(var * initial_value, 2),
                'percentage': round(var * 100, 2)
            },
            'cvar': {
                'confidence': confidence_level,
                'value': round(cvar * initial_value, 2),
                'percentage': round(cvar * 100, 2)
            },
            'probabilities': {
                'profit': round(prob_profit, 4),
                'loss_20pct': round(prob_20pct_loss, 4)
            }
        }

    def sensitivity_to_parameters(
        self,
        base_initial: float,
        base_drift: float,
        base_volatility: float,
        periods: int,
        param_ranges: Dict[str, Tuple[float, float, int]] = None
    ) -> Dict:
        """
        Analyze sensitivity to input parameters.

        Args:
            base_initial: Base initial value
            base_drift: Base drift
            base_volatility: Base volatility
            periods: Number of periods
            param_ranges: Dict of (min, max, n_points) for each parameter

        Returns:
            Sensitivity analysis results
        """
        if param_ranges is None:
            param_ranges = {
                'drift': (base_drift * 0.5, base_drift * 1.5, 5),
                'volatility': (base_volatility * 0.5, base_volatility * 1.5, 5)
            }

        results = {}

        for param, (min_val, max_val, n_points) in param_ranges.items():
            values = np.linspace(min_val, max_val, n_points)
            means = []
            stds = []

            for val in values:
                if param == 'drift':
                    self.simulate_geometric_brownian_motion(
                        base_initial, val, base_volatility, periods
                    )
                elif param == 'volatility':
                    self.simulate_geometric_brownian_motion(
                        base_initial, base_drift, val, periods
                    )

                final_values = self.simulations[:, -1]
                means.append(np.mean(final_values))
                stds.append(np.std(final_values))

            results[param] = {
                'values': values.round(4).tolist(),
                'mean_outcomes': np.array(means).round(2).tolist(),
                'std_outcomes': np.array(stds).round(2).tolist()
            }

        return results

    def get_simulation_paths(
        self,
        n_paths: int = 100
    ) -> np.ndarray:
        """
        Get sample paths for visualization.

        Args:
            n_paths: Number of paths to return

        Returns:
            Array of sample paths
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        indices = np.random.choice(self.n_simulations, min(n_paths, self.n_simulations), replace=False)
        return self.simulations[indices]

    def get_fan_chart_data(
        self,
        percentiles: List[int] = [5, 10, 25, 50, 75, 90, 95]
    ) -> pd.DataFrame:
        """
        Get data for fan chart visualization.

        Args:
            percentiles: Percentiles for fan bands

        Returns:
            DataFrame with percentile data
        """
        if self.simulations is None:
            raise ValueError("Run simulation first")

        data = {'Period': range(1, self.simulations.shape[1] + 1)}

        for p in percentiles:
            data[f'P{p}'] = np.percentile(self.simulations, p, axis=0).round(2)

        return pd.DataFrame(data)
