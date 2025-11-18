"""
Debt Calculations Service

This service provides calculation methods for debt management including:
- Debt Service Coverage Ratio (DSCR)
- Amortization schedules
- Refinancing analysis
- Loan comparison
- Interest rate sensitivity analysis
"""

from decimal import Decimal
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class DebtCalculationsService:
    """
    Service for debt-related financial calculations
    """

    @staticmethod
    def calculate_monthly_payment(
        loan_amount: Decimal,
        annual_rate: Decimal,
        term_months: int,
        interest_only_months: int = 0
    ) -> Decimal:
        """
        Calculate monthly payment for a loan

        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate (e.g., 0.05 for 5%)
            term_months: Total loan term in months
            interest_only_months: Number of interest-only months

        Returns:
            Monthly payment amount
        """
        if loan_amount <= 0 or term_months <= 0:
            return Decimal("0")

        monthly_rate = annual_rate / Decimal("12")

        if monthly_rate == 0:
            return loan_amount / Decimal(term_months)

        # Calculate fully amortizing payment for remaining term
        amortizing_months = term_months - interest_only_months

        if amortizing_months <= 0:
            # Interest-only for entire term
            return loan_amount * monthly_rate

        # PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
        numerator = monthly_rate * (1 + monthly_rate) ** amortizing_months
        denominator = (1 + monthly_rate) ** amortizing_months - 1

        if denominator == 0:
            return Decimal("0")

        return loan_amount * (numerator / denominator)

    @staticmethod
    def calculate_dscr(
        net_operating_income: Decimal,
        annual_debt_service: Decimal
    ) -> Optional[Decimal]:
        """
        Calculate Debt Service Coverage Ratio

        Args:
            net_operating_income: Annual NOI
            annual_debt_service: Annual debt service (principal + interest)

        Returns:
            DSCR ratio or None if cannot calculate
        """
        if annual_debt_service <= 0:
            return None

        dscr = net_operating_income / annual_debt_service
        return Decimal(str(round(dscr, 4)))

    @staticmethod
    def calculate_debt_yield(
        net_operating_income: Decimal,
        loan_amount: Decimal
    ) -> Optional[Decimal]:
        """
        Calculate Debt Yield

        Args:
            net_operating_income: Annual NOI
            loan_amount: Total loan amount

        Returns:
            Debt yield percentage or None if cannot calculate
        """
        if loan_amount <= 0:
            return None

        debt_yield = (net_operating_income / loan_amount) * Decimal("100")
        return Decimal(str(round(debt_yield, 4)))

    @staticmethod
    def calculate_ltv(
        loan_amount: Decimal,
        property_value: Decimal
    ) -> Optional[Decimal]:
        """
        Calculate Loan to Value ratio

        Args:
            loan_amount: Total loan amount
            property_value: Property value

        Returns:
            LTV ratio (as decimal, e.g., 0.75 for 75%) or None
        """
        if property_value <= 0:
            return None

        ltv = loan_amount / property_value
        return Decimal(str(round(ltv, 6)))

    @staticmethod
    def generate_amortization_schedule(
        loan_amount: Decimal,
        annual_rate: Decimal,
        term_months: int,
        start_date: date,
        interest_only_months: int = 0,
        balloon_months: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate complete amortization schedule

        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate
            term_months: Total loan term in months
            start_date: Loan start date
            interest_only_months: Number of interest-only months
            balloon_months: If balloon payment, number of months until balloon

        Returns:
            List of payment schedule entries
        """
        schedule = []
        balance = loan_amount
        monthly_rate = annual_rate / Decimal("12")
        cumulative_principal = Decimal("0")
        cumulative_interest = Decimal("0")

        # Calculate payment amounts
        interest_only_payment = loan_amount * monthly_rate if monthly_rate > 0 else Decimal("0")

        amortizing_months = term_months - interest_only_months
        if balloon_months:
            amortizing_months = min(balloon_months - interest_only_months, amortizing_months)

        amortizing_payment = DebtCalculationsService.calculate_monthly_payment(
            loan_amount, annual_rate, term_months, interest_only_months
        )

        for month in range(1, term_months + 1):
            payment_date = start_date + relativedelta(months=month)

            # Interest for this period
            interest_payment = balance * monthly_rate

            # Determine payment amount and principal
            if month <= interest_only_months:
                # Interest-only period
                payment = interest_only_payment
                principal_payment = Decimal("0")
            elif balloon_months and month == balloon_months:
                # Balloon payment
                principal_payment = balance
                payment = principal_payment + interest_payment
            else:
                # Regular amortizing payment
                payment = amortizing_payment
                principal_payment = payment - interest_payment

            # Ensure principal doesn't exceed remaining balance
            principal_payment = min(principal_payment, balance)

            # Update balances
            balance -= principal_payment
            cumulative_principal += principal_payment
            cumulative_interest += interest_payment

            schedule.append({
                "payment_number": month,
                "payment_date": payment_date.isoformat(),
                "beginning_balance": float(balance + principal_payment),
                "payment_amount": float(payment),
                "principal_payment": float(principal_payment),
                "interest_payment": float(interest_payment),
                "ending_balance": float(balance),
                "cumulative_principal": float(cumulative_principal),
                "cumulative_interest": float(cumulative_interest)
            })

            # Break if fully paid off
            if balance <= Decimal("0.01"):
                break

        return schedule

    @staticmethod
    def calculate_refinancing_analysis(
        current_loan: Dict[str, Any],
        proposed_loan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze refinancing opportunity

        Args:
            current_loan: Current loan details
            proposed_loan: Proposed new loan details

        Returns:
            Refinancing analysis with savings/costs
        """
        # Extract current loan details
        current_balance = Decimal(str(current_loan.get("balance", 0)))
        current_rate = Decimal(str(current_loan.get("rate", 0)))
        current_term_remaining = int(current_loan.get("term_remaining_months", 0))
        current_payment = Decimal(str(current_loan.get("monthly_payment", 0)))

        # Extract proposed loan details
        new_rate = Decimal(str(proposed_loan.get("rate", 0)))
        new_term = int(proposed_loan.get("term_months", current_term_remaining))
        new_closing_costs = Decimal(str(proposed_loan.get("closing_costs", 0)))
        cash_out = Decimal(str(proposed_loan.get("cash_out", 0)))

        # Calculate new loan amount
        new_loan_amount = current_balance + cash_out + new_closing_costs

        # Calculate new payment
        new_payment = DebtCalculationsService.calculate_monthly_payment(
            new_loan_amount, new_rate, new_term
        )

        # Calculate monthly savings
        monthly_savings = current_payment - new_payment

        # Calculate break-even months
        break_even_months = None
        if monthly_savings > 0:
            break_even_months = int(new_closing_costs / monthly_savings) + 1

        # Calculate total interest for current loan
        current_total_interest = (current_payment * Decimal(current_term_remaining)) - current_balance

        # Calculate total interest for new loan
        new_total_interest = (new_payment * Decimal(new_term)) - new_loan_amount

        # Calculate lifetime savings
        lifetime_savings = current_total_interest - new_total_interest - new_closing_costs

        return {
            "current_loan": {
                "balance": float(current_balance),
                "rate": float(current_rate),
                "monthly_payment": float(current_payment),
                "remaining_months": current_term_remaining,
                "total_interest": float(current_total_interest),
                "total_payments": float(current_payment * Decimal(current_term_remaining))
            },
            "proposed_loan": {
                "loan_amount": float(new_loan_amount),
                "rate": float(new_rate),
                "monthly_payment": float(new_payment),
                "term_months": new_term,
                "closing_costs": float(new_closing_costs),
                "total_interest": float(new_total_interest),
                "total_payments": float(new_payment * Decimal(new_term))
            },
            "savings_analysis": {
                "monthly_savings": float(monthly_savings),
                "annual_savings": float(monthly_savings * Decimal("12")),
                "lifetime_savings": float(lifetime_savings),
                "break_even_months": break_even_months,
                "rate_reduction": float(current_rate - new_rate),
                "recommended": monthly_savings > 0 and (break_even_months is None or break_even_months < 36)
            }
        }

    @staticmethod
    def calculate_interest_rate_sensitivity(
        loan_amount: Decimal,
        base_rate: Decimal,
        term_months: int,
        rate_variations: List[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Calculate interest rate sensitivity analysis

        Args:
            loan_amount: Loan amount
            base_rate: Base interest rate
            term_months: Loan term in months
            rate_variations: List of rate changes to analyze (e.g., [-0.01, -0.005, 0, 0.005, 0.01])

        Returns:
            Sensitivity analysis results
        """
        if rate_variations is None:
            rate_variations = [
                Decimal("-0.02"),  # -2%
                Decimal("-0.01"),  # -1%
                Decimal("-0.005"),  # -0.5%
                Decimal("0"),      # Base
                Decimal("0.005"),  # +0.5%
                Decimal("0.01"),   # +1%
                Decimal("0.02")    # +2%
            ]

        base_payment = DebtCalculationsService.calculate_monthly_payment(
            loan_amount, base_rate, term_months
        )

        scenarios = []

        for rate_change in rate_variations:
            adjusted_rate = base_rate + rate_change
            adjusted_payment = DebtCalculationsService.calculate_monthly_payment(
                loan_amount, adjusted_rate, term_months
            )

            payment_difference = adjusted_payment - base_payment
            total_interest = (adjusted_payment * Decimal(term_months)) - loan_amount

            scenarios.append({
                "rate_change": float(rate_change),
                "adjusted_rate": float(adjusted_rate),
                "monthly_payment": float(adjusted_payment),
                "payment_difference": float(payment_difference),
                "annual_difference": float(payment_difference * Decimal("12")),
                "total_interest": float(total_interest),
                "total_cost": float(adjusted_payment * Decimal(term_months))
            })

        return {
            "base_scenario": {
                "rate": float(base_rate),
                "monthly_payment": float(base_payment),
                "loan_amount": float(loan_amount),
                "term_months": term_months
            },
            "scenarios": scenarios
        }

    @staticmethod
    def compare_loans(
        loan_scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare multiple loan scenarios

        Args:
            loan_scenarios: List of loan scenario dictionaries

        Returns:
            Comparison analysis with best options
        """
        comparisons = []

        for i, scenario in enumerate(loan_scenarios):
            loan_amount = Decimal(str(scenario.get("loan_amount", 0)))
            rate = Decimal(str(scenario.get("rate", 0)))
            term = int(scenario.get("term_months", 360))
            closing_costs = Decimal(str(scenario.get("closing_costs", 0)))
            points = Decimal(str(scenario.get("points", 0)))

            # Calculate monthly payment
            monthly_payment = DebtCalculationsService.calculate_monthly_payment(
                loan_amount, rate, term
            )

            # Calculate total interest
            total_payments = monthly_payment * Decimal(term)
            total_interest = total_payments - loan_amount

            # Calculate effective cost including closing costs and points
            total_cost = total_payments + closing_costs + (loan_amount * points / Decimal("100"))

            # Calculate APR (simplified)
            total_financing_cost = closing_costs + (loan_amount * points / Decimal("100"))
            net_loan_amount = loan_amount - total_financing_cost
            apr = rate  # Simplified; true APR calculation is more complex

            comparisons.append({
                "scenario_name": scenario.get("name", f"Scenario {i+1}"),
                "lender": scenario.get("lender", "Unknown"),
                "loan_amount": float(loan_amount),
                "rate": float(rate),
                "term_months": term,
                "monthly_payment": float(monthly_payment),
                "total_payments": float(total_payments),
                "total_interest": float(total_interest),
                "closing_costs": float(closing_costs),
                "points": float(points),
                "total_cost": float(total_cost),
                "apr": float(apr)
            })

        # Find best options
        if comparisons:
            lowest_payment = min(comparisons, key=lambda x: x["monthly_payment"])
            lowest_total_cost = min(comparisons, key=lambda x: x["total_cost"])
            lowest_rate = min(comparisons, key=lambda x: x["rate"])

            return {
                "comparisons": comparisons,
                "best_options": {
                    "lowest_monthly_payment": lowest_payment["scenario_name"],
                    "lowest_total_cost": lowest_total_cost["scenario_name"],
                    "lowest_rate": lowest_rate["scenario_name"]
                }
            }

        return {"comparisons": [], "best_options": {}}


# Singleton instance
debt_calculations_service = DebtCalculationsService()
