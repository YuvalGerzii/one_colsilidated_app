"""
Sensitivity Analysis Service

Provides comprehensive sensitivity analysis for real estate financial models:
- One-way sensitivity (tornado charts)
- Two-way sensitivity (heat maps)
- Monte Carlo simulations
- Scenario analysis
- Break-even calculations

All calculations use FREE data sources - no API keys required.
"""

import logging
from typing import Dict, List, Any, Callable, Optional, Tuple
import random
import statistics
import math

logger = logging.getLogger(__name__)


class SensitivityAnalysisService:
    """Perform sensitivity analysis on financial models"""

    @staticmethod
    def one_way_sensitivity(
        base_inputs: Dict[str, float],
        calculate_metric: Callable[[Dict[str, float]], float],
        variables: List[Dict[str, Any]],
        metric_name: str = "Output"
    ) -> Dict[str, Any]:
        """
        Perform one-way sensitivity analysis (tornado chart data)

        Args:
            base_inputs: Base case input values
            calculate_metric: Function that calculates the output metric
            variables: List of variables to analyze, each with:
                - name: Variable name
                - label: Display label
                - min: Minimum value to test
                - max: Maximum value to test
            metric_name: Name of the output metric

        Returns:
            Dict with sensitivity results for tornado chart
        """
        base_metric = calculate_metric(base_inputs.copy())

        results = []

        for var in variables:
            var_name = var["name"]

            # Calculate metric with min value
            min_inputs = base_inputs.copy()
            min_inputs[var_name] = var["min"]
            min_metric = calculate_metric(min_inputs)

            # Calculate metric with max value
            max_inputs = base_inputs.copy()
            max_inputs[var_name] = var["max"]
            max_metric = calculate_metric(max_inputs)

            # Calculate range and impact
            metric_range = abs(max_metric - min_metric)
            impact_percentage = (metric_range / base_metric * 100) if base_metric != 0 else 0

            results.append({
                "variable": var_name,
                "label": var.get("label", var_name),
                "base_value": base_inputs.get(var_name, var.get("base_value", 0)),
                "min_value": var["min"],
                "max_value": var["max"],
                "metric_at_min": round(min_metric, 2),
                "metric_at_max": round(max_metric, 2),
                "metric_range": round(metric_range, 2),
                "impact_percentage": round(impact_percentage, 2),
                "sensitivity_rank": 0  # Will be ranked below
            })

        # Sort by impact (highest impact first - most sensitive variables)
        results.sort(key=lambda x: x["impact_percentage"], reverse=True)

        # Add sensitivity ranks
        for i, result in enumerate(results):
            result["sensitivity_rank"] = i + 1

        return {
            "base_metric": round(base_metric, 2),
            "metric_name": metric_name,
            "variables_analyzed": len(variables),
            "sensitivities": results,
            "most_sensitive": results[0]["variable"] if results else None,
            "least_sensitive": results[-1]["variable"] if results else None
        }

    @staticmethod
    def two_way_sensitivity(
        base_inputs: Dict[str, float],
        calculate_metric: Callable[[Dict[str, float]], float],
        x_variable: Dict[str, Any],
        y_variable: Dict[str, Any],
        steps: int = 7
    ) -> Dict[str, Any]:
        """
        Perform two-way sensitivity analysis (heat map data)

        Args:
            base_inputs: Base case input values
            calculate_metric: Function that calculates the output metric
            x_variable: Variable for X-axis (dict with name, min, max, label)
            y_variable: Variable for Y-axis (dict with name, min, max, label)
            steps: Number of steps for each variable (default 7 for 7x7 grid)

        Returns:
            Dict with heat map data
        """
        x_name = x_variable["name"]
        y_name = y_variable["name"]

        # Generate value ranges
        x_values = [
            x_variable["min"] + (x_variable["max"] - x_variable["min"]) * i / (steps - 1)
            for i in range(steps)
        ]

        y_values = [
            y_variable["min"] + (y_variable["max"] - y_variable["min"]) * i / (steps - 1)
            for i in range(steps)
        ]

        # Calculate metrics for all combinations
        heat_map_data = []
        all_metrics = []

        for y_val in y_values:
            row = []
            for x_val in x_values:
                inputs = base_inputs.copy()
                inputs[x_name] = x_val
                inputs[y_name] = y_val

                metric = calculate_metric(inputs)
                row.append(round(metric, 2))
                all_metrics.append(metric)

            heat_map_data.append(row)

        # Calculate statistics
        min_metric = min(all_metrics)
        max_metric = max(all_metrics)
        avg_metric = statistics.mean(all_metrics)

        return {
            "x_variable": {
                "name": x_name,
                "label": x_variable.get("label", x_name),
                "values": [round(v, 2) for v in x_values]
            },
            "y_variable": {
                "name": y_name,
                "label": y_variable.get("label", y_name),
                "values": [round(v, 2) for v in y_values]
            },
            "heat_map_data": heat_map_data,
            "statistics": {
                "min": round(min_metric, 2),
                "max": round(max_metric, 2),
                "average": round(avg_metric, 2),
                "range": round(max_metric - min_metric, 2)
            }
        }

    @staticmethod
    def monte_carlo_simulation(
        base_inputs: Dict[str, float],
        calculate_metric: Callable[[Dict[str, float]], float],
        variables: List[Dict[str, Any]],
        iterations: int = 10000,
        distribution: str = "normal"  # normal, uniform, triangular
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation

        Args:
            base_inputs: Base case input values
            calculate_metric: Function that calculates the output metric
            variables: List of variables with statistical distributions
            iterations: Number of simulation runs
            distribution: Type of distribution (normal, uniform, triangular)

        Returns:
            Dict with simulation results and statistics
        """
        results = []

        # Limit iterations for performance
        iterations = min(iterations, 100000)

        for _ in range(iterations):
            simulated_inputs = base_inputs.copy()

            for var in variables:
                var_name = var["name"]

                if distribution == "normal":
                    # Normal distribution: mean = base_value, std_dev based on range
                    mean = var.get("base_value", base_inputs.get(var_name, 0))
                    # Assume min/max are ~2 std deviations from mean
                    std_dev = (var["max"] - var["min"]) / 4
                    value = random.gauss(mean, std_dev)
                    # Clip to min/max
                    value = max(var["min"], min(var["max"], value))

                elif distribution == "uniform":
                    # Uniform distribution between min and max
                    value = random.uniform(var["min"], var["max"])

                elif distribution == "triangular":
                    # Triangular distribution (min, mode, max)
                    mode = var.get("base_value", base_inputs.get(var_name, 0))
                    value = random.triangular(var["min"], var["max"], mode)

                simulated_inputs[var_name] = value

            metric = calculate_metric(simulated_inputs)
            results.append(metric)

        # Calculate statistics
        results.sort()
        mean = statistics.mean(results)
        median = statistics.median(results)
        std_dev = statistics.stdev(results) if len(results) > 1 else 0

        # Percentiles
        p5 = results[int(len(results) * 0.05)]
        p25 = results[int(len(results) * 0.25)]
        p75 = results[int(len(results) * 0.75)]
        p95 = results[int(len(results) * 0.95)]

        # Create histogram data (20 bins)
        num_bins = 20
        min_val = min(results)
        max_val = max(results)
        bin_width = (max_val - min_val) / num_bins

        histogram = []
        for i in range(num_bins):
            bin_start = min_val + i * bin_width
            bin_end = bin_start + bin_width
            count = sum(1 for r in results if bin_start <= r < bin_end)
            histogram.append({
                "bin_start": round(bin_start, 2),
                "bin_end": round(bin_end, 2),
                "count": count,
                "frequency": round(count / iterations, 4)
            })

        return {
            "iterations": iterations,
            "distribution_type": distribution,
            "statistics": {
                "mean": round(mean, 2),
                "median": round(median, 2),
                "std_dev": round(std_dev, 2),
                "min": round(min(results), 2),
                "max": round(max(results), 2),
                "range": round(max(results) - min(results), 2),
                "coefficient_of_variation": round(std_dev / mean * 100, 2) if mean != 0 else 0
            },
            "percentiles": {
                "p5": round(p5, 2),
                "p25": round(p25, 2),
                "p50_median": round(median, 2),
                "p75": round(p75, 2),
                "p95": round(p95, 2)
            },
            "histogram": histogram,
            "risk_metrics": {
                "probability_of_loss": round(sum(1 for r in results if r < 0) / iterations * 100, 2),
                "value_at_risk_95": round(p5, 2),  # 95% VaR (5th percentile)
                "expected_shortfall": round(statistics.mean([r for r in results if r <= p5]), 2) if p5 < 0 else 0
            }
        }

    @staticmethod
    def scenario_analysis(
        base_inputs: Dict[str, float],
        calculate_metric: Callable[[Dict[str, float]], float],
        scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze predefined scenarios

        Args:
            base_inputs: Base case input values
            calculate_metric: Function that calculates the output metric
            scenarios: List of scenarios, each with:
                - name: Scenario name
                - description: Description
                - adjustments: Dict of variable adjustments (e.g., {"rent_growth": 1.05})

        Returns:
            Dict with scenario comparison results
        """
        results = []

        # Always include base case
        base_metric = calculate_metric(base_inputs.copy())
        results.append({
            "name": "Base Case",
            "description": "Current assumptions",
            "metric": round(base_metric, 2),
            "vs_base_amount": 0,
            "vs_base_percentage": 0
        })

        # Calculate each scenario
        for scenario in scenarios:
            scenario_inputs = base_inputs.copy()

            # Apply adjustments
            adjustments = scenario.get("adjustments", {})
            for var_name, adjustment in adjustments.items():
                if var_name in scenario_inputs:
                    # Adjustment can be absolute value or multiplier
                    if isinstance(adjustment, dict):
                        if "multiply_by" in adjustment:
                            scenario_inputs[var_name] *= adjustment["multiply_by"]
                        elif "add" in adjustment:
                            scenario_inputs[var_name] += adjustment["add"]
                        elif "value" in adjustment:
                            scenario_inputs[var_name] = adjustment["value"]
                    else:
                        # Assume it's an absolute value
                        scenario_inputs[var_name] = adjustment

            metric = calculate_metric(scenario_inputs)

            results.append({
                "name": scenario["name"],
                "description": scenario.get("description", ""),
                "metric": round(metric, 2),
                "vs_base_amount": round(metric - base_metric, 2),
                "vs_base_percentage": round((metric - base_metric) / base_metric * 100, 2) if base_metric != 0 else 0,
                "adjustments_applied": adjustments
            })

        return {
            "base_metric": round(base_metric, 2),
            "scenarios": results,
            "best_case": max(results, key=lambda x: x["metric"]),
            "worst_case": min(results, key=lambda x: x["metric"]),
            "range": round(max(r["metric"] for r in results) - min(r["metric"] for r in results), 2)
        }

    @staticmethod
    def break_even_analysis(
        base_inputs: Dict[str, float],
        calculate_metric: Callable[[Dict[str, float]], float],
        variables: List[Dict[str, Any]],
        target_metric: float = 0
    ) -> Dict[str, Any]:
        """
        Calculate break-even values for each variable

        Args:
            base_inputs: Base case input values
            calculate_metric: Function that calculates the output metric
            variables: List of variables to analyze
            target_metric: Target metric value (default 0 for break-even)

        Returns:
            Dict with break-even values for each variable
        """
        results = []

        for var in variables:
            var_name = var["name"]
            base_value = base_inputs.get(var_name, var.get("base_value", 0))

            # Use binary search to find break-even value
            min_val = var["min"]
            max_val = var["max"]

            # Check if break-even is possible within range
            min_inputs = base_inputs.copy()
            min_inputs[var_name] = min_val
            min_metric = calculate_metric(min_inputs)

            max_inputs = base_inputs.copy()
            max_inputs[var_name] = max_val
            max_metric = calculate_metric(max_inputs)

            # Binary search for break-even
            tolerance = 0.01
            max_iterations = 100
            break_even_value = None

            if (min_metric - target_metric) * (max_metric - target_metric) < 0:
                # Break-even exists within range
                for _ in range(max_iterations):
                    mid_val = (min_val + max_val) / 2

                    mid_inputs = base_inputs.copy()
                    mid_inputs[var_name] = mid_val
                    mid_metric = calculate_metric(mid_inputs)

                    if abs(mid_metric - target_metric) < tolerance:
                        break_even_value = mid_val
                        break

                    if (min_metric - target_metric) * (mid_metric - target_metric) < 0:
                        max_val = mid_val
                        max_metric = mid_metric
                    else:
                        min_val = mid_val
                        min_metric = mid_metric

            if break_even_value is not None:
                change_amount = break_even_value - base_value
                change_percentage = (change_amount / base_value * 100) if base_value != 0 else 0

                # Classify difficulty
                abs_change_pct = abs(change_percentage)
                if abs_change_pct < 10:
                    difficulty = "easy"
                    emoji = "🟢"
                elif abs_change_pct < 25:
                    difficulty = "moderate"
                    emoji = "🟡"
                elif abs_change_pct < 50:
                    difficulty = "challenging"
                    emoji = "🟠"
                else:
                    difficulty = "difficult"
                    emoji = "🔴"

                results.append({
                    "variable": var_name,
                    "label": var.get("label", var_name),
                    "base_value": round(base_value, 2),
                    "break_even_value": round(break_even_value, 2),
                    "change_amount": round(change_amount, 2),
                    "change_percentage": round(change_percentage, 2),
                    "difficulty": difficulty,
                    "emoji": emoji,
                    "achievable": True
                })
            else:
                results.append({
                    "variable": var_name,
                    "label": var.get("label", var_name),
                    "base_value": round(base_value, 2),
                    "break_even_value": None,
                    "change_amount": None,
                    "change_percentage": None,
                    "difficulty": "impossible",
                    "emoji": "❌",
                    "achievable": False,
                    "note": "Break-even not achievable within reasonable range"
                })

        # Sort by difficulty (easiest first)
        difficulty_order = {"easy": 0, "moderate": 1, "challenging": 2, "difficult": 3, "impossible": 4}
        results.sort(key=lambda x: difficulty_order.get(x["difficulty"], 4))

        return {
            "target_metric": target_metric,
            "break_even_analysis": results,
            "easiest_path": results[0] if results else None,
            "achievable_variables": [r["variable"] for r in results if r["achievable"]]
        }


# Example usage and helper functions for common real estate calculations

def calculate_cash_on_cash_return(inputs: Dict[str, float]) -> float:
    """Calculate cash-on-cash return for real estate investment"""
    annual_noi = inputs.get("annual_noi", 0)
    total_cash_invested = inputs.get("total_cash_invested", 1)

    return (annual_noi / total_cash_invested) * 100 if total_cash_invested > 0 else 0


def calculate_cap_rate(inputs: Dict[str, float]) -> float:
    """Calculate capitalization rate"""
    annual_noi = inputs.get("annual_noi", 0)
    property_value = inputs.get("property_value", 1)

    return (annual_noi / property_value) * 100 if property_value > 0 else 0


def calculate_dscr(inputs: Dict[str, float]) -> float:
    """Calculate debt service coverage ratio"""
    annual_noi = inputs.get("annual_noi", 0)
    annual_debt_service = inputs.get("annual_debt_service", 1)

    return annual_noi / annual_debt_service if annual_debt_service > 0 else 0


def calculate_irr_simple(inputs: Dict[str, float]) -> float:
    """Simplified IRR calculation for quick estimates"""
    # This is a simplified version - for production use numpy.irr or similar
    total_cash_flow = inputs.get("total_cash_flow", 0)
    initial_investment = inputs.get("initial_investment", 1)
    years = inputs.get("years", 1)

    if initial_investment > 0 and years > 0:
        # Simple approximation
        return ((total_cash_flow / initial_investment) ** (1 / years) - 1) * 100
    return 0
