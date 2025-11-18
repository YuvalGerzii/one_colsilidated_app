"""
Fund Metrics Calculation Service

This service provides calculation methods for PE/VC fund metrics including:
- IRR (Internal Rate of Return)
- MOIC (Multiple on Invested Capital)
- DPI (Distributions to Paid-In)
- RVPI (Residual Value to Paid-In)
- TVPI (Total Value to Paid-In)
- Distribution Waterfall Calculator
- Management Fee Calculator
- Carried Interest Calculator
"""

from decimal import Decimal
from datetime import date, timedelta
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from scipy.optimize import newton
import logging

logger = logging.getLogger(__name__)


class FundMetricsService:
    """
    Service for calculating fund-level metrics
    """

    @staticmethod
    def calculate_irr(cash_flows: List[Tuple[date, Decimal]]) -> Optional[Decimal]:
        """
        Calculate Internal Rate of Return (IRR) using Newton-Raphson method

        Args:
            cash_flows: List of (date, amount) tuples
                       Negative for investments, positive for distributions

        Returns:
            IRR as a decimal (e.g., 0.25 for 25%) or None if cannot calculate
        """
        if not cash_flows or len(cash_flows) < 2:
            return None

        try:
            # Sort cash flows by date
            cash_flows = sorted(cash_flows, key=lambda x: x[0])

            # Convert to numpy arrays
            base_date = cash_flows[0][0]
            days = np.array([(cf[0] - base_date).days for cf in cash_flows])
            amounts = np.array([float(cf[1]) for cf in cash_flows])

            # Define NPV function and its derivative
            def npv(rate):
                return np.sum(amounts * np.power(1 + rate, -days / 365.0))

            def npv_derivative(rate):
                return np.sum(-amounts * (days / 365.0) * np.power(1 + rate, -(days / 365.0) - 1))

            # Use Newton-Raphson to find IRR
            irr = newton(npv, 0.1, fprime=npv_derivative, maxiter=100)

            return Decimal(str(round(irr, 6)))
        except Exception as e:
            logger.warning(f"Failed to calculate IRR: {e}")
            return None

    @staticmethod
    def calculate_moic(total_invested: Decimal, total_value: Decimal) -> Optional[Decimal]:
        """
        Calculate Multiple on Invested Capital (MOIC)

        Args:
            total_invested: Total capital invested
            total_value: Total value (distributions + NAV)

        Returns:
            MOIC as a decimal (e.g., 2.5 for 2.5x)
        """
        if total_invested <= 0:
            return None

        moic = total_value / total_invested
        return Decimal(str(round(moic, 4)))

    @staticmethod
    def calculate_dpi(total_distributions: Decimal, total_called: Decimal) -> Optional[Decimal]:
        """
        Calculate Distributions to Paid-In (DPI)

        Args:
            total_distributions: Total distributions to LPs
            total_called: Total capital called from LPs

        Returns:
            DPI as a decimal
        """
        if total_called <= 0:
            return None

        dpi = total_distributions / total_called
        return Decimal(str(round(dpi, 4)))

    @staticmethod
    def calculate_rvpi(nav: Decimal, total_called: Decimal) -> Optional[Decimal]:
        """
        Calculate Residual Value to Paid-In (RVPI)

        Args:
            nav: Net Asset Value (fair value of remaining investments)
            total_called: Total capital called from LPs

        Returns:
            RVPI as a decimal
        """
        if total_called <= 0:
            return None

        rvpi = nav / total_called
        return Decimal(str(round(rvpi, 4)))

    @staticmethod
    def calculate_tvpi(dpi: Optional[Decimal], rvpi: Optional[Decimal]) -> Optional[Decimal]:
        """
        Calculate Total Value to Paid-In (TVPI)

        Args:
            dpi: Distributions to Paid-In
            rvpi: Residual Value to Paid-In

        Returns:
            TVPI as a decimal (TVPI = DPI + RVPI)
        """
        if dpi is None or rvpi is None:
            return None

        tvpi = dpi + rvpi
        return Decimal(str(round(tvpi, 4)))

    @staticmethod
    def calculate_management_fee(
        committed_capital: Decimal,
        invested_capital: Decimal,
        nav: Decimal,
        management_fee_rate: Decimal,
        fee_basis: str,
        period_days: int = 365
    ) -> Decimal:
        """
        Calculate management fee for a period

        Args:
            committed_capital: Total committed capital
            invested_capital: Total invested capital
            nav: Current Net Asset Value
            management_fee_rate: Annual management fee rate (e.g., 0.02 for 2%)
            fee_basis: Basis for fee calculation ('committed_capital', 'invested_capital', 'nav')
            period_days: Number of days in the period (default 365)

        Returns:
            Management fee amount
        """
        basis_map = {
            'committed_capital': committed_capital,
            'invested_capital': invested_capital,
            'nav': nav
        }

        basis_amount = basis_map.get(fee_basis, committed_capital)
        annual_fee = basis_amount * management_fee_rate
        period_fee = annual_fee * Decimal(period_days) / Decimal(365)

        return Decimal(str(round(period_fee, 2)))


class WaterfallCalculator:
    """
    Distribution Waterfall Calculator

    Implements the European/American waterfall structures for PE/VC distributions
    """

    @staticmethod
    def calculate_american_waterfall(
        distribution_amount: Decimal,
        total_invested: Decimal,
        total_distributed_to_date: Decimal,
        preferred_return_rate: Decimal,
        carried_interest_rate: Decimal,
        lp_share: Decimal,
        catch_up_rate: Optional[Decimal] = Decimal("1.0")
    ) -> Dict[str, Decimal]:
        """
        Calculate American (deal-by-deal) waterfall distribution

        Args:
            distribution_amount: Amount to distribute
            total_invested: Total capital invested
            total_distributed_to_date: Total distributions made so far
            preferred_return_rate: Preferred return rate (e.g., 0.08 for 8%)
            carried_interest_rate: GP carry rate (e.g., 0.20 for 20%)
            lp_share: LP share after carry (typically 1 - carried_interest_rate)
            catch_up_rate: GP catch-up rate (typically 1.0 for 100%)

        Returns:
            Dictionary with waterfall breakdown:
            {
                'lp_return_of_capital': amount,
                'lp_preferred_return': amount,
                'gp_catch_up': amount,
                'lp_remaining_profit': amount,
                'gp_carried_interest': amount,
                'lp_total': amount,
                'gp_total': amount
            }
        """
        remaining = distribution_amount
        result = {
            'lp_return_of_capital': Decimal("0"),
            'lp_preferred_return': Decimal("0"),
            'gp_catch_up': Decimal("0"),
            'lp_remaining_profit': Decimal("0"),
            'gp_carried_interest': Decimal("0"),
            'lp_total': Decimal("0"),
            'gp_total': Decimal("0")
        }

        # Track what has been returned
        returned_capital = min(total_distributed_to_date, total_invested)
        unreturned_capital = total_invested - returned_capital

        # 1. Return of Capital to LPs
        if remaining > 0 and unreturned_capital > 0:
            return_of_capital = min(remaining, unreturned_capital)
            result['lp_return_of_capital'] = return_of_capital
            remaining -= return_of_capital
            returned_capital += return_of_capital

        # 2. Preferred Return to LPs
        if remaining > 0:
            # Calculate total preferred return owed on returned capital
            # Simplified: assuming pref return on capital * rate
            total_pref_owed = total_invested * preferred_return_rate

            # Calculate how much pref has been paid
            pref_already_paid = max(Decimal("0"), total_distributed_to_date - returned_capital)
            pref_still_owed = max(Decimal("0"), total_pref_owed - pref_already_paid)

            preferred_return_amount = min(remaining, pref_still_owed)
            result['lp_preferred_return'] = preferred_return_amount
            remaining -= preferred_return_amount

        # 3. GP Catch-up
        if remaining > 0 and catch_up_rate:
            # GP catches up until they have their carried interest percentage of total profits
            # Total profit so far = total distributed - capital - pref return
            total_profit_distributed = (
                total_distributed_to_date + distribution_amount - total_invested
            )

            # GP should have: total_profit * carry_rate
            gp_target = total_profit_distributed * carried_interest_rate

            # How much has GP gotten so far (just from catch-up in prior distributions)
            # Simplified calculation
            catch_up_amount = min(remaining, gp_target * catch_up_rate)
            result['gp_catch_up'] = catch_up_amount
            remaining -= catch_up_amount

        # 4. Remaining profits split between LP and GP
        if remaining > 0:
            lp_split = remaining * lp_share
            gp_split = remaining * carried_interest_rate

            result['lp_remaining_profit'] = lp_split
            result['gp_carried_interest'] = gp_split
            remaining = Decimal("0")

        # Calculate totals
        result['lp_total'] = (
            result['lp_return_of_capital'] +
            result['lp_preferred_return'] +
            result['lp_remaining_profit']
        )
        result['gp_total'] = (
            result['gp_catch_up'] +
            result['gp_carried_interest']
        )

        return result

    @staticmethod
    def calculate_european_waterfall(
        distribution_amount: Decimal,
        total_invested: Decimal,
        total_distributed_to_date: Decimal,
        preferred_return_rate: Decimal,
        carried_interest_rate: Decimal
    ) -> Dict[str, Decimal]:
        """
        Calculate European (whole fund) waterfall distribution

        European waterfall only pays carry after all capital is returned + preferred return
        across the entire fund.

        Args:
            distribution_amount: Amount to distribute
            total_invested: Total capital invested across all deals
            total_distributed_to_date: Total distributions made so far
            preferred_return_rate: Preferred return rate
            carried_interest_rate: GP carry rate

        Returns:
            Dictionary with waterfall breakdown
        """
        remaining = distribution_amount
        result = {
            'lp_return_of_capital': Decimal("0"),
            'lp_preferred_return': Decimal("0"),
            'lp_profit': Decimal("0"),
            'gp_carried_interest': Decimal("0"),
            'lp_total': Decimal("0"),
            'gp_total': Decimal("0")
        }

        # 1. Return of Capital
        capital_returned = min(total_distributed_to_date, total_invested)
        capital_to_return = total_invested - capital_returned

        if remaining > 0 and capital_to_return > 0:
            return_of_capital = min(remaining, capital_to_return)
            result['lp_return_of_capital'] = return_of_capital
            remaining -= return_of_capital
            capital_returned += return_of_capital

        # 2. Preferred Return
        if remaining > 0 and capital_returned >= total_invested:
            total_pref_owed = total_invested * preferred_return_rate
            pref_paid = max(Decimal("0"), total_distributed_to_date - total_invested)
            pref_to_pay = max(Decimal("0"), total_pref_owed - pref_paid)

            preferred_return = min(remaining, pref_to_pay)
            result['lp_preferred_return'] = preferred_return
            remaining -= preferred_return

        # 3. Split remaining between LP and GP based on carried interest
        if remaining > 0:
            lp_share = Decimal("1") - carried_interest_rate
            result['lp_profit'] = remaining * lp_share
            result['gp_carried_interest'] = remaining * carried_interest_rate

        # Calculate totals
        result['lp_total'] = (
            result['lp_return_of_capital'] +
            result['lp_preferred_return'] +
            result['lp_profit']
        )
        result['gp_total'] = result['gp_carried_interest']

        return result

    @staticmethod
    def allocate_distribution_to_lps(
        total_lp_distribution: Decimal,
        lp_commitments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Allocate distribution amount to LPs based on their pro-rata share

        Args:
            total_lp_distribution: Total amount to distribute to LPs
            lp_commitments: List of LP commitment dictionaries with 'commitment_amount'

        Returns:
            List of LP allocations with distribution amounts
        """
        total_commitments = sum(
            Decimal(str(lp['commitment_amount']))
            for lp in lp_commitments
        )

        if total_commitments == 0:
            return []

        allocations = []
        for lp in lp_commitments:
            commitment = Decimal(str(lp['commitment_amount']))
            pro_rata_share = commitment / total_commitments
            distribution = total_lp_distribution * pro_rata_share

            allocations.append({
                **lp,
                'pro_rata_share': float(pro_rata_share),
                'distribution_amount': float(distribution)
            })

        return allocations


class FundPerformanceTracker:
    """
    Tracks and updates fund performance metrics
    """

    @staticmethod
    def update_fund_metrics(fund_data: Dict[str, Any]) -> Dict[str, Decimal]:
        """
        Calculate and update all fund metrics

        Args:
            fund_data: Dictionary containing fund information including:
                - total_called: Total capital called
                - total_distributed: Total distributions
                - nav: Net Asset Value
                - cash_flows: List of (date, amount) tuples for IRR

        Returns:
            Dictionary of calculated metrics
        """
        total_called = Decimal(str(fund_data.get('total_called', 0)))
        total_distributed = Decimal(str(fund_data.get('total_distributed', 0)))
        nav = Decimal(str(fund_data.get('nav', 0)))
        cash_flows = fund_data.get('cash_flows', [])

        metrics = {}

        # Calculate DPI
        metrics['dpi'] = FundMetricsService.calculate_dpi(
            total_distributed,
            total_called
        )

        # Calculate RVPI
        metrics['rvpi'] = FundMetricsService.calculate_rvpi(
            nav,
            total_called
        )

        # Calculate TVPI
        metrics['tvpi'] = FundMetricsService.calculate_tvpi(
            metrics['dpi'],
            metrics['rvpi']
        )

        # Calculate MOIC
        total_value = total_distributed + nav
        metrics['moic'] = FundMetricsService.calculate_moic(
            total_called,
            total_value
        )

        # Calculate IRR
        if cash_flows:
            metrics['irr'] = FundMetricsService.calculate_irr(cash_flows)
        else:
            metrics['irr'] = None

        return metrics


# Singleton instances
fund_metrics_service = FundMetricsService()
waterfall_calculator = WaterfallCalculator()
performance_tracker = FundPerformanceTracker()
