"""Small multifamily acquisition financial model for detailed unit-by-unit analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence
import numpy as np
import numpy_financial as npf


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Miami Quadplex Acquisition",
    "location": "Miami, FL",
    "analyst": "",
    "address": "123 Ocean Drive, Miami, FL 33139",
    "property_type": "quadplex",
    "number_of_units": 4,
    "total_building_sf": 4800,
    "lot_size_acres": 0.25,
    "year_built": 1985,
    "zoning": "R-4 Multi-Family",
    "purchase_price": 650000,
    "closing_costs": 19500,
    "total_renovation_budget": 80000,
    "holding_period_months": 24,
    "monthly_insurance": 500,
    "monthly_utilities": 300,
    "monthly_property_tax": 2000,
    "loan_ltv": 0.75,
    "interest_rate": 0.065,
    "loan_term_years": 30,
    "exit_cap_rate": 0.06,
    "selling_cost_pct": 0.06,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text"},
    {"name": "location", "label": "Location", "type": "text"},
    {"name": "property_type", "label": "Property Type", "type": "select",
     "options": ["duplex", "triplex", "quadplex", "small_multifamily"]},
    {"name": "number_of_units", "label": "Number of Units", "type": "number", "step": 1, "min": 2, "max": 20},
    {"name": "purchase_price", "label": "Purchase Price ($)", "type": "number", "step": 1000, "min": 100000},
    {"name": "closing_costs", "label": "Closing Costs ($)", "type": "number", "step": 500, "min": 0},
    {"name": "total_renovation_budget", "label": "Total Renovation Budget ($)", "type": "number", "step": 1000, "min": 0},
    {"name": "loan_ltv", "label": "Loan-to-Value", "type": "number", "step": 0.01, "min": 0.5, "max": 0.9},
    {"name": "interest_rate", "label": "Interest Rate", "type": "number", "step": 0.005, "min": 0.02, "max": 0.15},
    {"name": "loan_term_years", "label": "Loan Term (years)", "type": "number", "step": 1, "min": 10, "max": 30},
    {"name": "exit_cap_rate", "label": "Exit Cap Rate", "type": "number", "step": 0.0025, "min": 0.04, "max": 0.10},
]


def annuity_payment(principal: float, annual_rate: float, years: int) -> float:
    """Calculate monthly payment for an annuity."""
    if annual_rate == 0:
        return principal / (years * 12)
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    return (principal * (monthly_rate * (1 + monthly_rate) ** num_payments)) / ((1 + monthly_rate) ** num_payments - 1)


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults."""
    data = DEFAULT_INPUTS.copy()
    data.update(overrides)
    return data


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Generate acquisition analysis and investment metrics."""

    prepared = inputs.copy()

    # Extract key inputs
    purchase_price = prepared["purchase_price"]
    closing_costs = prepared.get("closing_costs", purchase_price * 0.03)
    total_renovation = prepared.get("total_renovation_budget", 0)
    number_of_units = prepared.get("number_of_units", 4)

    # Financing
    loan_ltv = prepared.get("loan_ltv", 0.75)
    interest_rate = prepared.get("interest_rate", 0.065)
    loan_term_years = prepared.get("loan_term_years", 30)

    total_acquisition_cost = purchase_price + closing_costs
    loan_amount = purchase_price * loan_ltv
    down_payment = purchase_price - loan_amount
    total_project_cost = total_acquisition_cost + total_renovation
    equity_required = down_payment + closing_costs + total_renovation

    # Monthly debt service
    monthly_payment = annuity_payment(loan_amount, interest_rate, loan_term_years)
    annual_debt_service = monthly_payment * 12

    # Revenue assumptions (from frontend default)
    # Assuming average market rent of $1,800/mo per unit
    avg_market_rent_per_unit = 1800
    annual_gross_rent = avg_market_rent_per_unit * 12 * number_of_units
    vacancy_rate = 0.05
    effective_gross_income = annual_gross_rent * (1 - vacancy_rate)

    # Operating expenses
    monthly_insurance = prepared.get("monthly_insurance", 500)
    monthly_utilities = prepared.get("monthly_utilities", 300)
    monthly_property_tax = prepared.get("monthly_property_tax", 2000)

    annual_insurance = monthly_insurance * 12
    annual_utilities = monthly_utilities * 12
    annual_property_tax = monthly_property_tax * 12
    management_fee = effective_gross_income * 0.08
    maintenance = effective_gross_income * 0.05

    total_operating_expenses = (
        annual_insurance +
        annual_utilities +
        annual_property_tax +
        management_fee +
        maintenance
    )

    # NOI and cash flow
    noi = effective_gross_income - total_operating_expenses
    annual_cash_flow = noi - annual_debt_service

    # Exit analysis
    exit_cap_rate = prepared.get("exit_cap_rate", 0.06)
    exit_value = noi / exit_cap_rate if exit_cap_rate > 0 else 0
    selling_cost_pct = prepared.get("selling_cost_pct", 0.06)
    selling_costs = exit_value * selling_cost_pct

    # Calculate loan balance at exit (assuming 5-year hold)
    hold_years = 5
    payments_made = hold_years * 12
    monthly_rate = interest_rate / 12
    total_payments = loan_term_years * 12

    if interest_rate > 0:
        remaining_balance = loan_amount * (
            ((1 + monthly_rate) ** total_payments - (1 + monthly_rate) ** payments_made) /
            ((1 + monthly_rate) ** total_payments - 1)
        )
    else:
        remaining_balance = loan_amount * (total_payments - payments_made) / total_payments

    net_proceeds = exit_value - selling_costs - remaining_balance
    total_cash_flow = annual_cash_flow * hold_years
    total_return = net_proceeds + total_cash_flow

    # ROI calculations
    cash_on_cash = annual_cash_flow / equity_required if equity_required > 0 else 0
    total_roi = total_return / equity_required if equity_required > 0 else 0

    # IRR calculation
    cash_flows = [-equity_required]
    for year in range(1, hold_years):
        cash_flows.append(annual_cash_flow)
    cash_flows.append(annual_cash_flow + net_proceeds)

    try:
        irr = float(npf.irr(cash_flows))
        if np.isnan(irr):
            irr = 0.0
    except:
        irr = 0.0

    metrics = {
        "purchase_price": purchase_price,
        "closing_costs": closing_costs,
        "total_renovation": total_renovation,
        "total_acquisition_cost": total_acquisition_cost,
        "total_project_cost": total_project_cost,
        "loan_amount": loan_amount,
        "down_payment": down_payment,
        "equity_required": equity_required,
        "number_of_units": number_of_units,
        "price_per_unit": purchase_price / number_of_units if number_of_units > 0 else 0,
        "annual_gross_rent": annual_gross_rent,
        "vacancy_loss": annual_gross_rent * vacancy_rate,
        "effective_gross_income": effective_gross_income,
        "operating_expenses": total_operating_expenses,
        "noi": noi,
        "annual_debt_service": annual_debt_service,
        "annual_cash_flow": annual_cash_flow,
        "monthly_cash_flow": annual_cash_flow / 12,
        "cash_on_cash": cash_on_cash,
        "exit_value": exit_value,
        "selling_costs": selling_costs,
        "remaining_loan_balance": remaining_balance,
        "net_sale_proceeds": net_proceeds,
        "total_return": total_return,
        "total_roi": total_roi,
        "irr": irr,
        "cap_rate": noi / total_project_cost if total_project_cost > 0 else 0,
        "debt_service_coverage": noi / annual_debt_service if annual_debt_service > 0 else 0,
    }

    return {"metrics": metrics, "inputs": prepared}


def format_currency(value: float) -> str:
    """Format a number as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format a number as percentage."""
    return f"{value * 100:.2f}%"


def build_report_tables(inputs: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build structured tables for the interactive UI."""

    acquisition_rows = [
        {"Item": "Purchase Price", "Amount": format_currency(metrics["purchase_price"])},
        {"Item": "Closing Costs", "Amount": format_currency(metrics["closing_costs"])},
        {"Item": "Renovation Budget", "Amount": format_currency(metrics["total_renovation"])},
        {"Item": "Total Project Cost", "Amount": format_currency(metrics["total_project_cost"])},
    ]

    financing_rows = [
        {"Item": "Down Payment", "Amount": format_currency(metrics["down_payment"])},
        {"Item": "Loan Amount", "Amount": format_currency(metrics["loan_amount"])},
        {"Item": "Equity Required", "Amount": format_currency(metrics["equity_required"])},
        {"Item": "Annual Debt Service", "Amount": format_currency(metrics["annual_debt_service"])},
    ]

    returns_metrics = {
        "Cash-on-Cash": format_percentage(metrics["cash_on_cash"]),
        "IRR": format_percentage(metrics["irr"]),
        "Total ROI": format_percentage(metrics["total_roi"]),
        "Cap Rate": format_percentage(metrics["cap_rate"]),
        "DSCR": f"{metrics['debt_service_coverage']:.2f}x",
    }

    return [
        {"kind": "table", "title": "Acquisition Costs", "columns": ["Item", "Amount"], "rows": acquisition_rows},
        {"kind": "table", "title": "Financing", "columns": ["Item", "Amount"], "rows": financing_rows},
        {"kind": "metrics", "title": "Investment Returns", "metrics": returns_metrics},
    ]
