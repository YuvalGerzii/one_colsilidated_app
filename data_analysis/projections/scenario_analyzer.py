"""
Scenario Analysis Module
=========================

Advanced scenario analysis for projections and what-if analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union, Callable
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class ScenarioAnalyzer:
    """
    Scenario analysis for projections and sensitivity analysis.
    """

    def __init__(self):
        self.scenarios = {}
        self.projections = {}
        self.sensitivity_results = {}

    def define_scenario(
        self,
        name: str,
        parameters: Dict[str, float],
        description: str = ''
    ) -> None:
        """
        Define a scenario with parameters.

        Args:
            name: Scenario name
            parameters: Dictionary of parameter values
            description: Scenario description
        """
        self.scenarios[name] = {
            'parameters': parameters,
            'description': description,
            'created_at': datetime.now().isoformat()
        }

    def create_baseline_scenario(
        self,
        historical_data: pd.Series,
        growth_rate: float = None
    ) -> Dict:
        """
        Create baseline scenario from historical data.

        Args:
            historical_data: Historical time series
            growth_rate: Manual growth rate (auto-calculated if None)

        Returns:
            Baseline scenario parameters
        """
        if growth_rate is None:
            # Calculate historical growth rate
            returns = historical_data.pct_change().dropna()
            growth_rate = returns.mean()

        volatility = historical_data.pct_change().std()
        last_value = historical_data.iloc[-1]

        parameters = {
            'growth_rate': round(growth_rate, 6),
            'volatility': round(volatility, 6),
            'base_value': round(last_value, 4),
            'mean': round(historical_data.mean(), 4),
            'std': round(historical_data.std(), 4)
        }

        self.define_scenario('baseline', parameters, 'Baseline scenario based on historical data')
        return parameters

    def create_scenario_variants(
        self,
        baseline: str = 'baseline',
        variants: List[str] = None
    ) -> Dict[str, Dict]:
        """
        Create scenario variants (optimistic, pessimistic, etc.).

        Args:
            baseline: Name of baseline scenario
            variants: List of variants to create

        Returns:
            Dictionary of variant scenarios
        """
        if baseline not in self.scenarios:
            raise ValueError(f"Baseline scenario '{baseline}' not found")

        if variants is None:
            variants = ['optimistic', 'pessimistic', 'conservative']

        base_params = self.scenarios[baseline]['parameters']
        variant_scenarios = {}

        if 'optimistic' in variants:
            opt_params = base_params.copy()
            opt_params['growth_rate'] = base_params['growth_rate'] * 1.5
            opt_params['volatility'] = base_params['volatility'] * 0.8
            self.define_scenario('optimistic', opt_params, 'Optimistic growth scenario')
            variant_scenarios['optimistic'] = opt_params

        if 'pessimistic' in variants:
            pess_params = base_params.copy()
            pess_params['growth_rate'] = base_params['growth_rate'] * 0.5
            pess_params['volatility'] = base_params['volatility'] * 1.3
            self.define_scenario('pessimistic', pess_params, 'Pessimistic growth scenario')
            variant_scenarios['pessimistic'] = pess_params

        if 'conservative' in variants:
            cons_params = base_params.copy()
            cons_params['growth_rate'] = base_params['growth_rate'] * 0.8
            cons_params['volatility'] = base_params['volatility']
            self.define_scenario('conservative', cons_params, 'Conservative growth scenario')
            variant_scenarios['conservative'] = cons_params

        if 'aggressive' in variants:
            agg_params = base_params.copy()
            agg_params['growth_rate'] = base_params['growth_rate'] * 2.0
            agg_params['volatility'] = base_params['volatility'] * 1.2
            self.define_scenario('aggressive', agg_params, 'Aggressive growth scenario')
            variant_scenarios['aggressive'] = agg_params

        return variant_scenarios

    def project_scenario(
        self,
        scenario_name: str,
        periods: int,
        method: str = 'compound'
    ) -> np.ndarray:
        """
        Project values for a scenario.

        Args:
            scenario_name: Name of scenario
            periods: Projection periods
            method: 'compound', 'linear', or 'random_walk'

        Returns:
            Projected values
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        params = self.scenarios[scenario_name]['parameters']
        base_value = params['base_value']
        growth_rate = params['growth_rate']

        if method == 'compound':
            # Compound growth
            projections = base_value * (1 + growth_rate) ** np.arange(1, periods + 1)

        elif method == 'linear':
            # Linear growth
            projections = base_value + base_value * growth_rate * np.arange(1, periods + 1)

        elif method == 'random_walk':
            # Random walk with drift
            volatility = params.get('volatility', growth_rate * 0.5)
            np.random.seed(42)
            shocks = np.random.normal(growth_rate, volatility, periods)
            projections = base_value * np.cumprod(1 + shocks)

        self.projections[scenario_name] = projections
        return projections

    def project_all_scenarios(
        self,
        periods: int,
        method: str = 'compound'
    ) -> pd.DataFrame:
        """
        Project all defined scenarios.

        Args:
            periods: Projection periods
            method: Projection method

        Returns:
            DataFrame with all projections
        """
        results = {}

        for name in self.scenarios.keys():
            results[name] = self.project_scenario(name, periods, method)

        return pd.DataFrame(results)

    def sensitivity_analysis(
        self,
        scenario_name: str,
        parameter: str,
        range_pct: float = 0.5,
        n_points: int = 21,
        periods: int = 12
    ) -> Dict:
        """
        Perform sensitivity analysis on a parameter.

        Args:
            scenario_name: Scenario to analyze
            parameter: Parameter to vary
            range_pct: Range as percentage of base value
            n_points: Number of points to evaluate
            periods: Projection periods

        Returns:
            Sensitivity analysis results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        base_params = self.scenarios[scenario_name]['parameters']
        base_value = base_params[parameter]

        # Create parameter range
        min_val = base_value * (1 - range_pct)
        max_val = base_value * (1 + range_pct)
        param_values = np.linspace(min_val, max_val, n_points)

        # Calculate projections for each parameter value
        final_values = []
        for val in param_values:
            temp_params = base_params.copy()
            temp_params[parameter] = val

            # Simple compound projection
            growth = temp_params.get('growth_rate', 0)
            base = temp_params.get('base_value', 100)
            final = base * (1 + growth) ** periods
            final_values.append(final)

        # Calculate sensitivity metrics
        base_final = base_params['base_value'] * (1 + base_params.get('growth_rate', 0)) ** periods
        elasticity = np.gradient(final_values, param_values)

        results = {
            'parameter': parameter,
            'param_values': param_values,
            'final_values': np.array(final_values),
            'base_final': base_final,
            'elasticity': elasticity,
            'sensitivity': (max(final_values) - min(final_values)) / base_final * 100
        }

        self.sensitivity_results[parameter] = results
        return results

    def tornado_analysis(
        self,
        scenario_name: str,
        parameters: List[str],
        periods: int = 12,
        swing_pct: float = 0.2
    ) -> pd.DataFrame:
        """
        Perform tornado analysis for multiple parameters.

        Args:
            scenario_name: Scenario to analyze
            parameters: Parameters to analyze
            periods: Projection periods
            swing_pct: Parameter swing percentage

        Returns:
            DataFrame with tornado analysis results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        base_params = self.scenarios[scenario_name]['parameters']

        # Calculate base case
        base_final = base_params['base_value'] * (1 + base_params.get('growth_rate', 0)) ** periods

        results = []

        for param in parameters:
            if param not in base_params:
                continue

            base_val = base_params[param]

            # Low case
            low_params = base_params.copy()
            low_params[param] = base_val * (1 - swing_pct)
            if param == 'growth_rate':
                low_final = base_params['base_value'] * (1 + low_params[param]) ** periods
            else:
                low_final = low_params.get('base_value', 100) * (1 + base_params.get('growth_rate', 0)) ** periods

            # High case
            high_params = base_params.copy()
            high_params[param] = base_val * (1 + swing_pct)
            if param == 'growth_rate':
                high_final = base_params['base_value'] * (1 + high_params[param]) ** periods
            else:
                high_final = high_params.get('base_value', 100) * (1 + base_params.get('growth_rate', 0)) ** periods

            results.append({
                'Parameter': param,
                'Low_Value': round(base_val * (1 - swing_pct), 6),
                'Base_Value': round(base_val, 6),
                'High_Value': round(base_val * (1 + swing_pct), 6),
                'Low_Result': round(low_final, 2),
                'Base_Result': round(base_final, 2),
                'High_Result': round(high_final, 2),
                'Swing': round(high_final - low_final, 2)
            })

        df = pd.DataFrame(results)
        df = df.sort_values('Swing', ascending=False)
        return df

    def what_if_analysis(
        self,
        scenario_name: str,
        changes: Dict[str, float],
        periods: int = 12
    ) -> Dict:
        """
        Perform what-if analysis with specific parameter changes.

        Args:
            scenario_name: Base scenario
            changes: Dictionary of parameter changes (multipliers)
            periods: Projection periods

        Returns:
            What-if analysis results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        base_params = self.scenarios[scenario_name]['parameters']
        modified_params = base_params.copy()

        # Apply changes
        for param, multiplier in changes.items():
            if param in modified_params:
                modified_params[param] = base_params[param] * multiplier

        # Calculate projections
        base_proj = base_params['base_value'] * (1 + base_params.get('growth_rate', 0)) ** np.arange(1, periods + 1)
        mod_proj = modified_params['base_value'] * (1 + modified_params.get('growth_rate', 0)) ** np.arange(1, periods + 1)

        # Calculate impact
        impact = (mod_proj[-1] - base_proj[-1]) / base_proj[-1] * 100

        return {
            'base_params': base_params,
            'modified_params': modified_params,
            'base_projection': base_proj,
            'modified_projection': mod_proj,
            'final_impact_pct': round(impact, 2),
            'changes_applied': changes
        }

    def breakeven_analysis(
        self,
        scenario_name: str,
        target_value: float,
        parameter: str,
        periods: int = 12,
        tolerance: float = 0.01
    ) -> Dict:
        """
        Find parameter value needed to reach target.

        Args:
            scenario_name: Scenario to analyze
            target_value: Target final value
            parameter: Parameter to adjust
            periods: Projection periods
            tolerance: Convergence tolerance

        Returns:
            Breakeven analysis results
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        base_params = self.scenarios[scenario_name]['parameters']

        # Binary search for breakeven value
        if parameter == 'growth_rate':
            low, high = -0.5, 1.0
        else:
            base_val = base_params[parameter]
            low, high = base_val * 0.1, base_val * 3.0

        for _ in range(100):
            mid = (low + high) / 2
            test_params = base_params.copy()
            test_params[parameter] = mid

            # Calculate final value
            if parameter == 'growth_rate':
                final = base_params['base_value'] * (1 + mid) ** periods
            else:
                final = test_params.get('base_value', 100) * (1 + base_params.get('growth_rate', 0)) ** periods

            if abs(final - target_value) / target_value < tolerance:
                break
            elif final < target_value:
                low = mid
            else:
                high = mid

        return {
            'parameter': parameter,
            'breakeven_value': round(mid, 6),
            'base_value': base_params[parameter],
            'target': target_value,
            'achieved_value': round(final, 2),
            'change_required': round((mid - base_params[parameter]) / base_params[parameter] * 100, 2)
        }

    def compare_scenarios(
        self,
        periods: int = 12
    ) -> pd.DataFrame:
        """
        Compare all scenarios.

        Args:
            periods: Projection periods

        Returns:
            Comparison DataFrame
        """
        projections = self.project_all_scenarios(periods)

        comparison = []
        for scenario in projections.columns:
            proj = projections[scenario]
            params = self.scenarios[scenario]['parameters']

            comparison.append({
                'Scenario': scenario,
                'Growth_Rate': round(params.get('growth_rate', 0) * 100, 2),
                'Initial_Value': round(params.get('base_value', 0), 2),
                'Final_Value': round(proj.iloc[-1], 2),
                'Total_Growth_Pct': round((proj.iloc[-1] / params.get('base_value', 1) - 1) * 100, 2),
                'Min_Value': round(proj.min(), 2),
                'Max_Value': round(proj.max(), 2)
            })

        return pd.DataFrame(comparison)

    def generate_probability_weighted_forecast(
        self,
        scenario_weights: Dict[str, float],
        periods: int = 12
    ) -> Dict:
        """
        Generate probability-weighted forecast from scenarios.

        Args:
            scenario_weights: Dictionary of scenario probabilities
            periods: Projection periods

        Returns:
            Weighted forecast results
        """
        # Normalize weights
        total_weight = sum(scenario_weights.values())
        normalized = {k: v / total_weight for k, v in scenario_weights.items()}

        # Project all scenarios
        projections = self.project_all_scenarios(periods)

        # Calculate weighted average
        weighted_forecast = np.zeros(periods)
        for scenario, weight in normalized.items():
            if scenario in projections.columns:
                weighted_forecast += weight * projections[scenario].values

        # Calculate variance across scenarios
        variance = np.zeros(periods)
        for scenario, weight in normalized.items():
            if scenario in projections.columns:
                variance += weight * (projections[scenario].values - weighted_forecast) ** 2

        return {
            'weighted_forecast': weighted_forecast,
            'std_dev': np.sqrt(variance),
            'weights': normalized,
            'projections': projections
        }

    def get_scenario_summary(self) -> pd.DataFrame:
        """
        Get summary of all defined scenarios.

        Returns:
            Summary DataFrame
        """
        summary = []
        for name, data in self.scenarios.items():
            params = data['parameters']
            summary.append({
                'Scenario': name,
                'Description': data.get('description', ''),
                'Base_Value': params.get('base_value', 0),
                'Growth_Rate': params.get('growth_rate', 0),
                'Volatility': params.get('volatility', 0)
            })

        return pd.DataFrame(summary)
