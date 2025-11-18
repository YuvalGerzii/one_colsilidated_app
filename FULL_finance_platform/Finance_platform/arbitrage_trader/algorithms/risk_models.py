"""
Advanced risk models including VaR, CVaR, and stress testing.
"""
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
from scipy import stats


class RiskCalculator:
    """Advanced risk calculations."""

    def __init__(self, config: dict = None):
        """
        Initialize risk calculator.

        Args:
            config: Configuration parameters
        """
        self.config = config or {}
        self.confidence_level = self.config.get("confidence_level", 0.95)

    def calculate_var(
        self,
        returns: List[Decimal],
        confidence_level: float = None,
        method: str = "historical"
    ) -> Decimal:
        """
        Calculate Value at Risk (VaR).

        Args:
            returns: Historical returns
            confidence_level: Confidence level (default 0.95)
            method: Calculation method (historical, parametric, monte_carlo)

        Returns:
            VaR value
        """
        if not returns:
            return Decimal(0)

        confidence_level = confidence_level or self.confidence_level
        returns_array = np.array([float(r) for r in returns])

        if method == "historical":
            # Historical VaR
            var = np.percentile(returns_array, (1 - confidence_level) * 100)

        elif method == "parametric":
            # Parametric VaR (assumes normal distribution)
            mean = np.mean(returns_array)
            std = np.std(returns_array)
            z_score = stats.norm.ppf(1 - confidence_level)
            var = mean + z_score * std

        elif method == "monte_carlo":
            # Monte Carlo VaR
            mean = np.mean(returns_array)
            std = np.std(returns_array)
            simulated = np.random.normal(mean, std, 10000)
            var = np.percentile(simulated, (1 - confidence_level) * 100)

        else:
            raise ValueError(f"Unknown method: {method}")

        return Decimal(str(var))

    def calculate_cvar(
        self,
        returns: List[Decimal],
        confidence_level: float = None
    ) -> Decimal:
        """
        Calculate Conditional Value at Risk (CVaR/Expected Shortfall).

        CVaR is the expected loss given that the loss exceeds VaR.

        Args:
            returns: Historical returns
            confidence_level: Confidence level

        Returns:
            CVaR value
        """
        if not returns:
            return Decimal(0)

        confidence_level = confidence_level or self.confidence_level
        returns_array = np.array([float(r) for r in returns])

        # Calculate VaR first
        var = float(self.calculate_var(returns, confidence_level))

        # CVaR is the average of returns below VaR
        tail_returns = returns_array[returns_array <= var]

        if len(tail_returns) == 0:
            return Decimal(str(var))

        cvar = np.mean(tail_returns)

        return Decimal(str(cvar))

    def calculate_portfolio_var(
        self,
        positions: Dict[str, Decimal],
        returns_history: Dict[str, List[Decimal]],
        correlation_matrix: np.ndarray = None,
        confidence_level: float = None
    ) -> Decimal:
        """
        Calculate portfolio VaR using variance-covariance method.

        Args:
            positions: Dictionary of asset -> position value
            returns_history: Historical returns for each asset
            correlation_matrix: Correlation matrix (optional)
            confidence_level: Confidence level

        Returns:
            Portfolio VaR
        """
        if not positions or not returns_history:
            return Decimal(0)

        confidence_level = confidence_level or self.confidence_level
        assets = list(positions.keys())

        # Build returns matrix
        returns_matrix = []
        position_values = []

        for asset in assets:
            if asset in returns_history:
                returns_array = [float(r) for r in returns_history[asset]]
                returns_matrix.append(returns_array)
                position_values.append(float(positions[asset]))

        if not returns_matrix:
            return Decimal(0)

        returns_matrix = np.array(returns_matrix)
        position_values = np.array(position_values)

        # Calculate portfolio returns
        portfolio_returns = np.dot(position_values, returns_matrix) / np.sum(position_values)

        # Calculate portfolio VaR
        portfolio_var = self.calculate_var(
            [Decimal(str(r)) for r in portfolio_returns],
            confidence_level
        )

        return portfolio_var

    def stress_test(
        self,
        portfolio_value: Decimal,
        scenarios: List[Dict]
    ) -> Dict:
        """
        Perform stress testing on portfolio.

        Args:
            portfolio_value: Current portfolio value
            scenarios: List of stress scenarios with shocks

        Returns:
            Stress test results
        """
        results = []

        for scenario in scenarios:
            scenario_name = scenario.get("name", "Unknown")
            shocks = scenario.get("shocks", {})

            # Calculate impact
            total_impact = Decimal(0)
            asset_impacts = {}

            for asset, shock in shocks.items():
                impact = portfolio_value * Decimal(str(shock))
                total_impact += impact
                asset_impacts[asset] = float(impact)

            final_value = portfolio_value + total_impact
            loss_percentage = (total_impact / portfolio_value * 100) if portfolio_value > 0 else Decimal(0)

            results.append({
                "scenario": scenario_name,
                "portfolio_value": float(portfolio_value),
                "total_impact": float(total_impact),
                "final_value": float(final_value),
                "loss_percentage": float(loss_percentage),
                "asset_impacts": asset_impacts
            })

        return {
            "stress_test_date": datetime.now().isoformat(),
            "scenarios": results,
            "worst_case": min(results, key=lambda x: x["final_value"]) if results else None
        }

    def calculate_maximum_drawdown(
        self,
        equity_curve: List[Decimal]
    ) -> Dict:
        """
        Calculate maximum drawdown.

        Args:
            equity_curve: Portfolio values over time

        Returns:
            Maximum drawdown information
        """
        if len(equity_curve) < 2:
            return {
                "max_drawdown": 0,
                "max_drawdown_pct": 0,
                "peak_value": 0,
                "trough_value": 0,
                "recovery_date": None
            }

        equity_array = np.array([float(v) for v in equity_curve])

        # Find running maximum
        running_max = np.maximum.accumulate(equity_array)

        # Calculate drawdown
        drawdown = equity_array - running_max
        drawdown_pct = drawdown / running_max * 100

        # Find maximum drawdown
        max_dd_idx = np.argmin(drawdown)
        max_dd = drawdown[max_dd_idx]
        max_dd_pct = drawdown_pct[max_dd_idx]

        # Find peak before max drawdown
        peak_idx = np.argmax(running_max[:max_dd_idx+1])
        peak_value = running_max[peak_idx]
        trough_value = equity_array[max_dd_idx]

        # Find recovery (if any)
        recovery_idx = None
        for i in range(max_dd_idx, len(equity_array)):
            if equity_array[i] >= peak_value:
                recovery_idx = i
                break

        return {
            "max_drawdown": float(max_dd),
            "max_drawdown_pct": float(max_dd_pct),
            "peak_value": float(peak_value),
            "peak_index": int(peak_idx),
            "trough_value": float(trough_value),
            "trough_index": int(max_dd_idx),
            "recovery_index": int(recovery_idx) if recovery_idx else None,
            "drawdown_duration": int(max_dd_idx - peak_idx),
            "recovery_duration": int(recovery_idx - max_dd_idx) if recovery_idx else None
        }

    def calculate_expected_shortfall(
        self,
        returns: List[Decimal],
        confidence_level: float = None
    ) -> Decimal:
        """
        Calculate Expected Shortfall (ES) / CVaR.

        Alias for calculate_cvar.
        """
        return self.calculate_cvar(returns, confidence_level)

    def calculate_downside_deviation(
        self,
        returns: List[Decimal],
        target_return: Decimal = Decimal(0)
    ) -> Decimal:
        """
        Calculate downside deviation.

        Only considers returns below target return.

        Args:
            returns: Returns series
            target_return: Target return threshold

        Returns:
            Downside deviation
        """
        if not returns:
            return Decimal(0)

        returns_array = np.array([float(r) for r in returns])
        target = float(target_return)

        # Only consider returns below target
        downside_returns = returns_array[returns_array < target]

        if len(downside_returns) == 0:
            return Decimal(0)

        # Calculate squared deviations
        squared_deviations = (downside_returns - target) ** 2
        downside_variance = np.mean(squared_deviations)
        downside_dev = np.sqrt(downside_variance)

        return Decimal(str(downside_dev))

    def calculate_sortino_ratio(
        self,
        returns: List[Decimal],
        risk_free_rate: Decimal = Decimal(0),
        target_return: Decimal = Decimal(0)
    ) -> Decimal:
        """
        Calculate Sortino ratio.

        Similar to Sharpe but uses downside deviation.

        Args:
            returns: Returns series
            risk_free_rate: Risk-free rate
            target_return: Target return

        Returns:
            Sortino ratio
        """
        if not returns:
            return Decimal(0)

        returns_array = np.array([float(r) for r in returns])
        mean_return = Decimal(str(np.mean(returns_array)))

        downside_dev = self.calculate_downside_deviation(returns, target_return)

        if downside_dev == 0:
            return Decimal(0)

        sortino = (mean_return - risk_free_rate) / downside_dev

        # Annualize
        sortino_annualized = sortino * Decimal(str(np.sqrt(252)))

        return sortino_annualized

    def calculate_calmar_ratio(
        self,
        returns: List[Decimal],
        equity_curve: List[Decimal]
    ) -> Decimal:
        """
        Calculate Calmar ratio.

        Annualized return / Maximum drawdown.

        Args:
            returns: Returns series
            equity_curve: Equity curve

        Returns:
            Calmar ratio
        """
        if not returns or not equity_curve:
            return Decimal(0)

        # Annualized return
        returns_array = np.array([float(r) for r in returns])
        mean_return = np.mean(returns_array)
        annualized_return = Decimal(str(mean_return * 252))

        # Maximum drawdown
        max_dd_info = self.calculate_maximum_drawdown(equity_curve)
        max_dd = abs(Decimal(str(max_dd_info["max_drawdown_pct"])))

        if max_dd == 0:
            return Decimal(0)

        calmar = annualized_return / max_dd

        return calmar

    def calculate_tail_risk(
        self,
        returns: List[Decimal],
        threshold_percentile: float = 5
    ) -> Dict:
        """
        Calculate tail risk metrics.

        Args:
            returns: Returns series
            threshold_percentile: Percentile for tail definition

        Returns:
            Tail risk metrics
        """
        if not returns:
            return {}

        returns_array = np.array([float(r) for r in returns])

        # Left tail (losses)
        left_threshold = np.percentile(returns_array, threshold_percentile)
        left_tail = returns_array[returns_array <= left_threshold]

        # Right tail (gains)
        right_threshold = np.percentile(returns_array, 100 - threshold_percentile)
        right_tail = returns_array[returns_array >= right_threshold]

        return {
            "left_tail_threshold": float(left_threshold),
            "left_tail_mean": float(np.mean(left_tail)) if len(left_tail) > 0 else 0,
            "left_tail_std": float(np.std(left_tail)) if len(left_tail) > 0 else 0,
            "left_tail_count": int(len(left_tail)),
            "right_tail_threshold": float(right_threshold),
            "right_tail_mean": float(np.mean(right_tail)) if len(right_tail) > 0 else 0,
            "right_tail_std": float(np.std(right_tail)) if len(right_tail) > 0 else 0,
            "right_tail_count": int(len(right_tail)),
            "tail_ratio": float(np.abs(np.mean(right_tail) / np.mean(left_tail)))
                if len(left_tail) > 0 and len(right_tail) > 0 and np.mean(left_tail) != 0 else 0
        }

    def monte_carlo_simulation(
        self,
        initial_value: Decimal,
        expected_return: Decimal,
        volatility: Decimal,
        time_horizon_days: int = 252,
        num_simulations: int = 10000
    ) -> Dict:
        """
        Run Monte Carlo simulation for portfolio.

        Args:
            initial_value: Starting portfolio value
            expected_return: Expected annual return
            volatility: Annual volatility
            time_horizon_days: Simulation horizon in days
            num_simulations: Number of simulations

        Returns:
            Simulation results
        """
        dt = 1 / 252  # Daily time step
        initial = float(initial_value)
        mu = float(expected_return)
        sigma = float(volatility)

        # Generate simulations
        simulations = np.zeros((num_simulations, time_horizon_days + 1))
        simulations[:, 0] = initial

        for t in range(1, time_horizon_days + 1):
            random_returns = np.random.normal(mu * dt, sigma * np.sqrt(dt), num_simulations)
            simulations[:, t] = simulations[:, t-1] * (1 + random_returns)

        # Calculate statistics
        final_values = simulations[:, -1]

        return {
            "initial_value": initial,
            "expected_return": mu,
            "volatility": sigma,
            "time_horizon_days": time_horizon_days,
            "num_simulations": num_simulations,
            "mean_final_value": float(np.mean(final_values)),
            "median_final_value": float(np.median(final_values)),
            "std_final_value": float(np.std(final_values)),
            "min_final_value": float(np.min(final_values)),
            "max_final_value": float(np.max(final_values)),
            "percentiles": {
                "5th": float(np.percentile(final_values, 5)),
                "25th": float(np.percentile(final_values, 25)),
                "50th": float(np.percentile(final_values, 50)),
                "75th": float(np.percentile(final_values, 75)),
                "95th": float(np.percentile(final_values, 95))
            },
            "probability_of_loss": float(np.sum(final_values < initial) / num_simulations * 100),
            "expected_profit": float(np.mean(final_values) - initial)
        }

    def calculate_risk_adjusted_return(
        self,
        returns: List[Decimal],
        risk_free_rate: Decimal = Decimal(0),
        method: str = "sharpe"
    ) -> Decimal:
        """
        Calculate risk-adjusted return.

        Args:
            returns: Returns series
            risk_free_rate: Risk-free rate
            method: Method (sharpe, sortino, calmar)

        Returns:
            Risk-adjusted return metric
        """
        if not returns:
            return Decimal(0)

        returns_array = np.array([float(r) for r in returns])
        mean_return = Decimal(str(np.mean(returns_array)))
        std_return = Decimal(str(np.std(returns_array)))

        if method == "sharpe":
            if std_return == 0:
                return Decimal(0)
            sharpe = (mean_return - risk_free_rate) / std_return
            return sharpe * Decimal(str(np.sqrt(252)))  # Annualized

        elif method == "sortino":
            return self.calculate_sortino_ratio(returns, risk_free_rate)

        elif method == "calmar":
            # Would need equity curve for calmar
            return Decimal(0)

        else:
            raise ValueError(f"Unknown method: {method}")
