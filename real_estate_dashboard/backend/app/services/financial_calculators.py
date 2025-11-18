"""
Financial Calculators

Practical calculators for financial decision-making:
- Mortgage affordability calculator
- Mortgage payment calculator
- Rent vs Buy calculator
- Break-even analysis
- Down payment calculator
- Refinancing calculator
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import math

logger = logging.getLogger(__name__)


class FinancialCalculators:
    """Financial calculators for housing and investment decisions"""

    @staticmethod
    def calculate_mortgage_payment(
        loan_amount: float,
        annual_rate: float,
        years: int = 30,
        monthly_payment: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate monthly mortgage payment and amortization details

        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate (e.g., 6.5 for 6.5%)
            years: Loan term in years
            monthly_payment: Optional - if provided, calculates loan amount instead

        Returns:
            Dict with payment details and amortization summary
        """
        if annual_rate <= 0:
            return {"error": "Interest rate must be positive"}

        monthly_rate = annual_rate / 100 / 12
        n_payments = years * 12

        if monthly_payment is None:
            # Calculate payment from loan amount
            if loan_amount <= 0:
                return {"error": "Loan amount must be positive"}

            # Monthly payment formula: M = P[r(1+r)^n]/[(1+r)^n-1]
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** n_payments
            ) / ((1 + monthly_rate) ** n_payments - 1)

            total_paid = monthly_payment * n_payments
            total_interest = total_paid - loan_amount

        else:
            # Calculate loan amount from payment
            # P = M[(1+r)^n-1]/[r(1+r)^n]
            loan_amount = monthly_payment * (
                ((1 + monthly_rate) ** n_payments - 1) /
                (monthly_rate * (1 + monthly_rate) ** n_payments)
            )

            total_paid = monthly_payment * n_payments
            total_interest = total_paid - loan_amount

        # Generate amortization summary (first year and totals)
        amortization_summary = []
        remaining_balance = loan_amount
        total_principal_paid = 0
        total_interest_paid = 0

        for month in range(1, min(13, n_payments + 1)):  # First year
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

            total_principal_paid += principal_payment
            total_interest_paid += interest_payment

            amortization_summary.append({
                "month": month,
                "payment": round(monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "balance": round(remaining_balance, 2)
            })

        return {
            "loan_amount": round(loan_amount, 2),
            "annual_rate": annual_rate,
            "loan_term_years": years,
            "monthly_payment": round(monthly_payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2),
            "interest_as_percentage": round((total_interest / loan_amount) * 100, 1),
            "first_year_summary": {
                "principal_paid": round(sum(p["principal"] for p in amortization_summary), 2),
                "interest_paid": round(sum(p["interest"] for p in amortization_summary), 2)
            },
            "amortization_first_year": amortization_summary
        }

    @staticmethod
    def calculate_affordability(
        annual_income: float,
        monthly_debts: float = 0,
        down_payment: float = 0,
        interest_rate: float = 6.5,
        loan_term_years: int = 30,
        property_tax_rate: float = 1.2,
        insurance_annual: float = 1200,
        hoa_monthly: float = 0,
        front_end_ratio: float = 28,
        back_end_ratio: float = 36
    ) -> Dict[str, Any]:
        """
        Calculate how much house you can afford

        Uses standard lending ratios:
        - Front-end ratio (housing costs / income): typically 28%
        - Back-end ratio (all debts / income): typically 36%

        Args:
            annual_income: Gross annual income
            monthly_debts: Other monthly debt payments (car, student loans, etc.)
            down_payment: Available down payment
            interest_rate: Annual interest rate
            loan_term_years: Loan term
            property_tax_rate: Annual property tax as % of home value
            insurance_annual: Annual homeowners insurance
            hoa_monthly: Monthly HOA fees
            front_end_ratio: Max housing cost as % of income (default 28)
            back_end_ratio: Max total debt as % of income (default 36)

        Returns:
            Dict with affordability analysis
        """
        monthly_income = annual_income / 12

        # Maximum monthly housing payment (front-end ratio)
        max_housing_payment = monthly_income * (front_end_ratio / 100)

        # Maximum total debt payment (back-end ratio)
        max_total_debt = monthly_income * (back_end_ratio / 100)

        # Maximum mortgage payment (after subtracting existing debts)
        max_mortgage_payment_debt_ratio = max_total_debt - monthly_debts

        # The lower of the two limits
        max_mortgage_payment = min(max_housing_payment, max_mortgage_payment_debt_ratio)

        # Account for property tax, insurance, and HOA
        # These are estimated as part of monthly housing costs
        # We need to reverse-engineer the home price

        # Monthly payment = mortgage + tax + insurance + HOA
        # Mortgage payment = max_mortgage_payment - (tax + insurance + HOA)

        # Start with estimated home price, iterate to find actual
        estimated_price = 300000  # Starting estimate
        for _ in range(10):  # Iterate to converge
            monthly_tax = (estimated_price * (property_tax_rate / 100)) / 12
            monthly_insurance = insurance_annual / 12
            monthly_other = monthly_tax + monthly_insurance + hoa_monthly

            available_for_mortgage = max_mortgage_payment - monthly_other

            # Calculate loan amount from available payment
            monthly_rate = interest_rate / 100 / 12
            n_payments = loan_term_years * 12

            if monthly_rate > 0:
                loan_amount = available_for_mortgage * (
                    ((1 + monthly_rate) ** n_payments - 1) /
                    (monthly_rate * (1 + monthly_rate) ** n_payments)
                )
            else:
                loan_amount = available_for_mortgage * n_payments

            # Home price = loan amount + down payment
            estimated_price = loan_amount + down_payment

        max_home_price = estimated_price
        max_loan_amount = loan_amount

        # Calculate actual monthly costs
        monthly_tax = (max_home_price * (property_tax_rate / 100)) / 12
        monthly_insurance = insurance_annual / 12
        total_monthly_housing = available_for_mortgage + monthly_tax + monthly_insurance + hoa_monthly

        # Breakdown
        breakdown = {
            "mortgage_payment": round(available_for_mortgage, 2),
            "property_tax": round(monthly_tax, 2),
            "insurance": round(monthly_insurance, 2),
            "hoa": round(hoa_monthly, 2),
            "total_housing_payment": round(total_monthly_housing, 2)
        }

        # Calculate ratios
        actual_front_end = (total_monthly_housing / monthly_income) * 100
        actual_back_end = ((total_monthly_housing + monthly_debts) / monthly_income) * 100

        return {
            "annual_income": annual_income,
            "monthly_income": round(monthly_income, 2),
            "down_payment": down_payment,
            "max_home_price": round(max_home_price, 2),
            "max_loan_amount": round(max_loan_amount, 2),
            "loan_to_value": round((max_loan_amount / max_home_price) * 100, 1),
            "monthly_payment_breakdown": breakdown,
            "ratios": {
                "front_end_ratio": round(actual_front_end, 1),
                "front_end_limit": front_end_ratio,
                "back_end_ratio": round(actual_back_end, 1),
                "back_end_limit": back_end_ratio
            },
            "guidelines": {
                "front_end_ok": actual_front_end <= front_end_ratio,
                "back_end_ok": actual_back_end <= back_end_ratio
            },
            "interpretation": (
                f"Based on ${annual_income:,.0f} annual income, you can afford a home up to "
                f"${max_home_price:,.0f} with ${down_payment:,.0f} down payment. "
                f"Monthly housing costs: ${total_monthly_housing:,.0f} "
                f"({actual_front_end:.1f}% of income)."
            )
        }

    @staticmethod
    def calculate_rent_vs_buy(
        home_price: float,
        down_payment: float,
        interest_rate: float,
        monthly_rent: float,
        years: int = 10,
        annual_appreciation: float = 3.0,
        property_tax_rate: float = 1.2,
        insurance_annual: float = 1200,
        maintenance_rate: float = 1.0,
        closing_costs_rate: float = 3.0,
        rental_increase: float = 2.5
    ) -> Dict[str, Any]:
        """
        Compare renting vs buying over time

        Args:
            home_price: Purchase price
            down_payment: Down payment amount
            interest_rate: Mortgage rate
            monthly_rent: Current monthly rent
            years: Analysis period
            annual_appreciation: Expected home appreciation rate
            property_tax_rate: Annual property tax %
            insurance_annual: Annual insurance cost
            maintenance_rate: Annual maintenance as % of home value
            closing_costs_rate: Closing costs as % of home price
            rental_increase: Annual rent increase %

        Returns:
            Dict with rent vs buy comparison
        """
        loan_amount = home_price - down_payment

        # Calculate mortgage payment
        mortgage_calc = FinancialCalculators.calculate_mortgage_payment(
            loan_amount,
            interest_rate,
            30  # Assume 30-year mortgage
        )

        monthly_mortgage = mortgage_calc["monthly_payment"]

        # Initial costs
        closing_costs = home_price * (closing_costs_rate / 100)
        initial_investment_buy = down_payment + closing_costs

        # Yearly analysis
        buying_costs = []
        renting_costs = []

        cumulative_buying = initial_investment_buy
        cumulative_renting = 0

        current_rent = monthly_rent
        current_home_value = home_price
        remaining_balance = loan_amount

        for year in range(1, years + 1):
            # Buying costs
            annual_mortgage = monthly_mortgage * 12
            annual_tax = current_home_value * (property_tax_rate / 100)
            annual_insurance = insurance_annual
            annual_maintenance = current_home_value * (maintenance_rate / 100)

            total_buying_cost = annual_mortgage + annual_tax + annual_insurance + annual_maintenance
            cumulative_buying += total_buying_cost

            # Home appreciation
            current_home_value *= (1 + annual_appreciation / 100)

            # Mortgage principal reduction (simplified)
            monthly_rate = interest_rate / 100 / 12
            # Calculate how much principal is paid down
            interest_paid = 0
            principal_paid = 0
            for month in range(12):
                interest_payment = remaining_balance * monthly_rate
                principal_payment = monthly_mortgage - interest_payment
                remaining_balance -= principal_payment
                interest_paid += interest_payment
                principal_paid += principal_payment

            # Equity = down payment + principal paid + appreciation
            equity = down_payment + (loan_amount - remaining_balance)

            buying_costs.append({
                "year": year,
                "annual_cost": round(total_buying_cost, 2),
                "cumulative_cost": round(cumulative_buying, 2),
                "home_value": round(current_home_value, 2),
                "remaining_mortgage": round(remaining_balance, 2),
                "equity": round(equity, 2),
                "net_position": round(current_home_value - remaining_balance - cumulative_buying, 2)
            })

            # Renting costs
            annual_rent = current_rent * 12
            cumulative_renting += annual_rent

            renting_costs.append({
                "year": year,
                "monthly_rent": round(current_rent, 2),
                "annual_cost": round(annual_rent, 2),
                "cumulative_cost": round(cumulative_renting, 2)
            })

            # Increase rent for next year
            current_rent *= (1 + rental_increase / 100)

        # Final comparison
        final_home_value = buying_costs[-1]["home_value"]
        final_mortgage = buying_costs[-1]["remaining_mortgage"]
        final_equity = final_home_value - final_mortgage
        total_buying_costs = buying_costs[-1]["cumulative_cost"]
        total_renting_costs = renting_costs[-1]["cumulative_cost"]

        # Net benefit of buying = equity - cumulative costs + initial investment back
        # vs renting cumulative costs
        buying_net_position = final_equity - total_buying_costs
        renting_net_position = -total_renting_costs

        savings = buying_net_position - renting_net_position

        # Break-even year (when buying becomes cheaper than renting)
        break_even_year = None
        for i, (buy, rent) in enumerate(zip(buying_costs, renting_costs)):
            buy_net = buy["net_position"]
            rent_net = -rent["cumulative_cost"]

            if buy_net > rent_net and break_even_year is None:
                break_even_year = i + 1

        return {
            "analysis_period_years": years,
            "initial_costs": {
                "down_payment": down_payment,
                "closing_costs": closing_costs,
                "total_initial_investment": initial_investment_buy
            },
            "buying_summary": {
                "total_costs_paid": round(total_buying_costs, 2),
                "final_home_value": round(final_home_value, 2),
                "final_equity": round(final_equity, 2),
                "net_position": round(buying_net_position, 2)
            },
            "renting_summary": {
                "total_rent_paid": round(total_renting_costs, 2),
                "net_position": round(renting_net_position, 2)
            },
            "comparison": {
                "savings_from_buying": round(savings, 2),
                "break_even_year": break_even_year,
                "better_option": "buying" if savings > 0 else "renting"
            },
            "yearly_breakdown": {
                "buying": buying_costs[-5:],  # Last 5 years
                "renting": renting_costs[-5:]
            },
            "recommendation": (
                f"Over {years} years, {'buying' if savings > 0 else 'renting'} is better by "
                f"${abs(savings):,.0f}. "
                f"{'Break-even occurs in year ' + str(break_even_year) if break_even_year else 'Renting remains cheaper throughout.'}"
            )
        }

    @staticmethod
    def calculate_refinance_analysis(
        current_loan_balance: float,
        current_interest_rate: float,
        current_remaining_years: float,
        new_interest_rate: float,
        new_loan_term_years: int = 30,
        refinance_costs: float = 5000,
        cash_out_amount: float = 0
    ) -> Dict[str, Any]:
        """
        Analyze if refinancing makes sense

        Args:
            current_loan_balance: Remaining balance on current mortgage
            current_interest_rate: Current rate
            current_remaining_years: Years left on current mortgage
            new_interest_rate: New refinanced rate
            new_loan_term_years: New loan term
            refinance_costs: Closing costs for refinancing
            cash_out_amount: Additional cash to take out (cash-out refi)

        Returns:
            Dict with refinancing analysis
        """
        # Current mortgage payment
        current_payment_calc = FinancialCalculators.calculate_mortgage_payment(
            current_loan_balance,
            current_interest_rate,
            int(current_remaining_years)
        )
        current_monthly_payment = current_payment_calc["monthly_payment"]
        current_total_remaining = current_monthly_payment * current_remaining_years * 12

        # New mortgage (loan balance + cash out + costs if rolled in)
        new_loan_amount = current_loan_balance + cash_out_amount + refinance_costs

        # New mortgage payment
        new_payment_calc = FinancialCalculators.calculate_mortgage_payment(
            new_loan_amount,
            new_interest_rate,
            new_loan_term_years
        )
        new_monthly_payment = new_payment_calc["monthly_payment"]
        new_total_to_pay = new_monthly_payment * new_loan_term_years * 12

        # Monthly savings
        monthly_savings = current_monthly_payment - new_monthly_payment

        # Break-even point (months to recover refinance costs)
        if monthly_savings > 0:
            break_even_months = refinance_costs / monthly_savings
        else:
            break_even_months = float('inf')

        # Total interest comparison
        current_total_interest = current_total_remaining - current_loan_balance
        new_total_interest = new_total_to_pay - new_loan_amount

        interest_savings = current_total_interest - new_total_interest

        # Recommendation
        if monthly_savings > 0 and break_even_months < 36:
            recommendation = "✅ Refinancing is recommended"
            reason = f"You'll save ${monthly_savings:,.0f}/month and break even in {break_even_months:.1f} months"
        elif monthly_savings > 0:
            recommendation = "⚠️ Marginal benefit"
            reason = f"Savings of ${monthly_savings:,.0f}/month but long break-even ({break_even_months:.0f} months)"
        else:
            recommendation = "❌ Refinancing not recommended"
            reason = f"Monthly payment increases by ${abs(monthly_savings):,.0f}"

        return {
            "current_mortgage": {
                "balance": current_loan_balance,
                "rate": current_interest_rate,
                "remaining_years": current_remaining_years,
                "monthly_payment": round(current_monthly_payment, 2),
                "total_remaining_cost": round(current_total_remaining, 2),
                "total_interest_remaining": round(current_total_interest, 2)
            },
            "new_mortgage": {
                "loan_amount": new_loan_amount,
                "rate": new_interest_rate,
                "term_years": new_loan_term_years,
                "monthly_payment": round(new_monthly_payment, 2),
                "total_cost": round(new_total_to_pay, 2),
                "total_interest": round(new_total_interest, 2)
            },
            "analysis": {
                "monthly_savings": round(monthly_savings, 2),
                "annual_savings": round(monthly_savings * 12, 2),
                "interest_savings": round(interest_savings, 2),
                "refinance_costs": refinance_costs,
                "break_even_months": round(break_even_months, 1) if break_even_months != float('inf') else "N/A",
                "break_even_years": round(break_even_months / 12, 1) if break_even_months != float('inf') else "N/A"
            },
            "recommendation": recommendation,
            "reason": reason
        }

    @staticmethod
    def calculate_down_payment_scenarios(
        home_price: float,
        interest_rate: float,
        down_payment_percentages: List[float] = [5, 10, 15, 20, 25, 30]
    ) -> Dict[str, Any]:
        """
        Compare different down payment scenarios

        Args:
            home_price: Home purchase price
            interest_rate: Mortgage interest rate
            down_payment_percentages: List of down payment percentages to compare

        Returns:
            Dict with comparison of scenarios
        """
        scenarios = []

        for dp_pct in down_payment_percentages:
            down_payment = home_price * (dp_pct / 100)
            loan_amount = home_price - down_payment

            # PMI required if down payment < 20%
            requires_pmi = dp_pct < 20
            monthly_pmi = (loan_amount * 0.005 / 12) if requires_pmi else 0  # ~0.5% annually

            # Calculate mortgage payment
            mortgage_calc = FinancialCalculators.calculate_mortgage_payment(
                loan_amount,
                interest_rate,
                30
            )

            monthly_payment = mortgage_calc["monthly_payment"] + monthly_pmi
            total_paid = monthly_payment * 360
            total_interest = mortgage_calc["total_interest"]

            if requires_pmi:
                # PMI typically drops after reaching 20% equity
                months_until_pmi_drops = 0
                remaining_balance = loan_amount
                monthly_rate = interest_rate / 100 / 12

                for month in range(1, 361):
                    interest_payment = remaining_balance * monthly_rate
                    principal_payment = mortgage_calc["monthly_payment"] - interest_payment
                    remaining_balance -= principal_payment

                    equity_pct = ((home_price - remaining_balance) / home_price) * 100
                    if equity_pct >= 20:
                        months_until_pmi_drops = month
                        break

                total_pmi_paid = monthly_pmi * months_until_pmi_drops
            else:
                months_until_pmi_drops = 0
                total_pmi_paid = 0

            scenarios.append({
                "down_payment_percentage": dp_pct,
                "down_payment_amount": round(down_payment, 2),
                "loan_amount": round(loan_amount, 2),
                "requires_pmi": requires_pmi,
                "monthly_payment": round(monthly_payment, 2),
                "monthly_pmi": round(monthly_pmi, 2),
                "months_until_pmi_drops": months_until_pmi_drops,
                "total_pmi_paid": round(total_pmi_paid, 2),
                "total_interest": round(total_interest, 2),
                "total_paid": round(total_paid + total_pmi_paid, 2),
                "savings_vs_minimum": None  # Will calculate after
            })

        # Calculate savings vs 5% down
        baseline_total = scenarios[0]["total_paid"]
        for scenario in scenarios:
            scenario["savings_vs_minimum"] = round(baseline_total - scenario["total_paid"], 2)

        return {
            "home_price": home_price,
            "interest_rate": interest_rate,
            "scenarios": scenarios,
            "insights": [
                f"💰 Putting 20% down saves ${scenarios[0]['total_pmi_paid']:,.0f} in PMI costs",
                f"📊 Each 5% additional down payment reduces monthly payment by ~${scenarios[0]['monthly_payment'] - scenarios[1]['monthly_payment']:,.0f}",
                f"🎯 20% down (${home_price * 0.20:,.0f}) eliminates PMI and saves most long-term"
            ]
        }
