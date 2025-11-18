"""Interactive CLI and shared helpers for the single-family rental model."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from rich.panel import Panel

from app.models.real_estate import SingleFamilyRentalModel

from .base import (
    annuity_payment,
    console,
    ensure_database,
    ensure_report_dir,
    format_currency,
    format_percentage,
    prompt_float,
    prompt_int,
    prompt_percentage,
    prompt_text,
    render_metrics_table,
    render_projection_table,
    remaining_balance,
    save_bar_chart,
    save_line_chart,
    session_scope,
)


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Maple Street Rental",
    "location": "Charlotte, NC",
    "analyst": "",
    "property_type": "Single-Family Residence",
    "square_footage": 1600,
    "bedrooms": 3,
    "bathrooms": 2.0,
    "year_built": 1990,
    "purchase_price": 280_000.0,
    "closing_costs": 5_000.0,
    "renovation_costs": 30_000.0,
    "arv": 340_000.0,
    "monthly_rent": 2_200.0,
    "other_income_monthly": 0.0,
    "rent_growth_rate": 0.03,
    "vacancy_rate": 0.05,
    "appreciation_rate": 0.03,
    "management_pct": 0.08,
    "maintenance_pct": 0.08,
    "property_tax_annual": 3_500.0,
    "insurance_annual": 1_500.0,
    "utilities_monthly": 150.0,
    "hoa_monthly": 0.0,
    "other_expenses_monthly": 50.0,
    "capex_reserve_monthly": 150.0,
    "expense_growth_rate": 0.025,
    "down_payment_pct": 0.25,
    "interest_rate": 0.065,
    "loan_term_years": 30,
    "selling_cost_pct": 0.07,
    "hold_period_years": 10,
    "refinance_ltv": 0.75,
    "refinance_rate": 0.06,
    "refinance_term_years": 30,
    "refinance_year": 0,
    "refinance_cost_pct": 0.03,
    "holding_costs_monthly": 600.0,
    "holding_period_months": 6,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Property Name", "type": "text", "section": "Property Profile"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Profile"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Profile"},
    {"name": "property_type", "label": "Property Type", "type": "text", "section": "Property Profile"},
    {
        "name": "square_footage",
        "label": "Square Footage",
        "type": "number",
        "step": 50,
        "min": 400,
        "section": "Property Profile",
    },
    {"name": "bedrooms", "label": "Bedrooms", "type": "number", "step": 1, "min": 0, "section": "Property Profile"},
    {
        "name": "bathrooms",
        "label": "Bathrooms",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "section": "Property Profile",
    },
    {"name": "year_built", "label": "Year Built", "type": "number", "step": 1, "min": 1900, "section": "Property Profile"},
    {
        "name": "purchase_price",
        "label": "Purchase Price ($)",
        "type": "number",
        "step": 1000,
        "min": 50000,
        "section": "Acquisition & Rehab",
    },
    {
        "name": "closing_costs",
        "label": "Closing Costs ($)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Acquisition & Rehab",
    },
    {
        "name": "renovation_costs",
        "label": "Renovation Budget ($)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Acquisition & Rehab",
    },
    {"name": "arv", "label": "After Repair Value ($)", "type": "number", "step": 1000, "min": 50000, "section": "Acquisition & Rehab"},
    {
        "name": "holding_costs_monthly",
        "label": "Monthly Holding Costs ($)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Acquisition & Rehab",
    },
    {
        "name": "holding_period_months",
        "label": "Holding Period (months)",
        "type": "number",
        "step": 1,
        "min": 1,
        "section": "Acquisition & Rehab",
    },
    {
        "name": "monthly_rent",
        "label": "Monthly Rent ($)",
        "type": "number",
        "step": 50,
        "min": 500,
        "section": "Income & Growth",
    },
    {
        "name": "other_income_monthly",
        "label": "Other Monthly Income ($)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Income & Growth",
    },
    {
        "name": "rent_growth_rate",
        "label": "Rent Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Income & Growth",
    },
    {
        "name": "vacancy_rate",
        "label": "Vacancy Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 25,
        "format": "percentage",
        "section": "Income & Growth",
    },
    {
        "name": "appreciation_rate",
        "label": "Appreciation (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Income & Growth",
    },
    {
        "name": "management_pct",
        "label": "Management Fee (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 20,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "maintenance_pct",
        "label": "Maintenance Allowance (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 25,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "property_tax_annual",
        "label": "Property Taxes ($ / year)",
        "type": "number",
        "step": 250,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "insurance_annual",
        "label": "Insurance ($ / year)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "utilities_monthly",
        "label": "Utilities ($ / month)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "hoa_monthly",
        "label": "HOA Dues ($ / month)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "other_expenses_monthly",
        "label": "Other Expenses ($ / month)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "capex_reserve_monthly",
        "label": "CapEx Reserve ($ / month)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "expense_growth_rate",
        "label": "Expense Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "down_payment_pct",
        "label": "Down Payment (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 60,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "interest_rate",
        "label": "Loan Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 2,
        "max": 15,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "loan_term_years",
        "label": "Loan Term (years)",
        "type": "number",
        "step": 1,
        "min": 5,
        "max": 40,
        "section": "Financing & Disposition",
    },
    {
        "name": "refinance_ltv",
        "label": "Refinance LTV (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 85,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "refinance_rate",
        "label": "Refinance Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 2,
        "max": 12,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "refinance_term_years",
        "label": "Refinance Term (years)",
        "type": "number",
        "step": 1,
        "min": 5,
        "max": 40,
        "section": "Financing & Disposition",
    },
    {
        "name": "refinance_year",
        "label": "Refinance Year (0 = no refi)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 10,
        "section": "Financing & Disposition",
    },
    {
        "name": "refinance_cost_pct",
        "label": "Refinance Costs (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "selling_cost_pct",
        "label": "Selling Costs (%)",
        "type": "number",
        "step": 0.25,
        "min": 3,
        "max": 12,
        "format": "percentage",
        "section": "Financing & Disposition",
    },
    {
        "name": "hold_period_years",
        "label": "Hold Period (years)",
        "type": "number",
        "step": 1,
        "min": 5,
        "max": 20,
        "section": "Holding Strategy",
    },
    {"name": "project_name", "label": "Property Name", "type": "text"},
    {"name": "location", "label": "Market / Location", "type": "text"},
    {"name": "purchase_price", "label": "Purchase Price ($)", "type": "number", "step": 1000, "min": 50000},
    {"name": "renovation_costs", "label": "Renovation Budget ($)", "type": "number", "step": 500, "min": 0},
    {"name": "monthly_rent", "label": "Monthly Rent ($)", "type": "number", "step": 50, "min": 500},
    {"name": "vacancy_rate", "label": "Vacancy Rate", "type": "number", "step": 0.01, "min": 0.0, "max": 0.2},
    {"name": "management_pct", "label": "Management Fee", "type": "number", "step": 0.01, "min": 0.0, "max": 0.15},
    {"name": "maintenance_pct", "label": "Maintenance Allowance", "type": "number", "step": 0.01, "min": 0.0, "max": 0.2},
    {"name": "interest_rate", "label": "Loan Rate", "type": "number", "step": 0.005, "min": 0.03, "max": 0.12},
    {"name": "down_payment_pct", "label": "Down Payment", "type": "number", "step": 0.01, "min": 0.1, "max": 0.4},
    {"name": "hold_period_years", "label": "Hold Period (years)", "type": "number", "step": 1, "min": 5, "max": 15},
    {"name": "refinance_year", "label": "Refinance Year (0 for none)", "type": "number", "step": 1, "min": 0, "max": 5},
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults and compute derived finance fields."""

    data = DEFAULT_INPUTS.copy()
    data.update(overrides)
    down_payment = data["purchase_price"] * data["down_payment_pct"]
    loan_amount = data["purchase_price"] - down_payment
    equity_invested = down_payment + data["closing_costs"] + data["renovation_costs"]
    total_project_cost = data["purchase_price"] + data["closing_costs"] + data["renovation_costs"]
    annual_debt_service = annuity_payment(loan_amount, data["interest_rate"], data["loan_term_years"]) * 12
    data.update(
        {
            "down_payment": down_payment,
            "loan_amount": loan_amount,
            "equity_invested": equity_invested,
            "total_project_cost": total_project_cost,
            "annual_debt_service": annual_debt_service,
        }
    )
    return data


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute ten-year projections and key metrics."""

    years = 10
    rent_growth = inputs["rent_growth_rate"]
    expense_growth = inputs["expense_growth_rate"]
    appreciation = inputs["appreciation_rate"]
    refinance_year = inputs["refinance_year"]
    perform_refi = inputs["refinance_ltv"] > 0 and refinance_year > 0

    monthly_rent = inputs["monthly_rent"]
    other_income_monthly = inputs["other_income_monthly"]
    vacancy_rate = inputs["vacancy_rate"]
    management_pct = inputs["management_pct"]
    maintenance_pct = inputs["maintenance_pct"]
    property_tax = inputs["property_tax_annual"]
    insurance = inputs["insurance_annual"]
    utilities_monthly = inputs["utilities_monthly"]
    hoa_monthly = inputs["hoa_monthly"]
    other_expenses_monthly = inputs["other_expenses_monthly"]
    capex_monthly = inputs["capex_reserve_monthly"]

    loan_amount = inputs["loan_amount"]
    interest_rate = inputs["interest_rate"]
    loan_term = inputs["loan_term_years"]
    arv = inputs["arv"]

    debt_services: List[float] = []
    loan_balances: List[float] = []
    cash_out_refi = 0.0

    current_principal = loan_amount
    current_rate = interest_rate
    current_term = loan_term
    payments_made = 0
    refi_executed = False

    for year in range(1, years + 1):
        annual_payment = annuity_payment(current_principal, current_rate, current_term) * 12
        debt_services.append(annual_payment)
        payments_made += 12
        balance_end = remaining_balance(current_principal, current_rate, current_term, payments_made)

        if perform_refi and not refi_executed and year == refinance_year:
            property_value = arv * ((1 + appreciation) ** year)
            new_principal = property_value * inputs["refinance_ltv"]
            refinance_costs = new_principal * inputs["refinance_cost_pct"]
            cash_out_refi = new_principal - balance_end - refinance_costs
            current_principal = new_principal
            current_rate = inputs["refinance_rate"]
            current_term = inputs["refinance_term_years"]
            payments_made = 0
            refi_executed = True
            balance_end = current_principal

        loan_balances.append(balance_end)

    projections: List[Dict[str, Any]] = []
    equity = inputs["equity_invested"]
    cash_flows: List[float] = [-equity]

    cumulative_cash_flow = 0.0

    for year in range(1, years + 1):
        rent_annual = monthly_rent * (1 + rent_growth) ** (year - 1) * 12
        other_income = other_income_monthly * (1 + rent_growth) ** (year - 1) * 12
        vacancy_loss = rent_annual * vacancy_rate
        effective_gross_income = rent_annual - vacancy_loss + other_income

        mgmt_expense = rent_annual * management_pct
        maintenance_expense = rent_annual * maintenance_pct
        property_tax_annual = property_tax * ((1 + expense_growth) ** (year - 1))
        insurance_annual = insurance * ((1 + expense_growth) ** (year - 1))
        utilities = utilities_monthly * ((1 + expense_growth) ** (year - 1)) * 12
        hoa = hoa_monthly * ((1 + expense_growth) ** (year - 1)) * 12
        other_expense = other_expenses_monthly * ((1 + expense_growth) ** (year - 1)) * 12
        capex = capex_monthly * ((1 + expense_growth) ** (year - 1)) * 12

        operating_expenses = (
            mgmt_expense
            + maintenance_expense
            + property_tax_annual
            + insurance_annual
            + utilities
            + hoa
            + other_expense
            + capex
        )

        noi = effective_gross_income - operating_expenses
        debt_service = debt_services[year - 1]

        annual_cash_flow = noi - debt_service
        if perform_refi and year == refinance_year:
            annual_cash_flow += cash_out_refi

        property_value = arv * ((1 + appreciation) ** year)
        loan_balance = loan_balances[year - 1]
        equity_position = property_value - loan_balance

        cumulative_cash_flow += annual_cash_flow

        projections.append(
            {
                "year": year,
                "gross_rent": rent_annual,
                "vacancy": vacancy_loss,
                "other_income": other_income,
                "effective_gross_income": effective_gross_income,
                "operating_expenses": operating_expenses,
                "noi": noi,
                "debt_service": debt_service,
                "cash_flow": annual_cash_flow,
                "loan_balance": loan_balance,
                "property_value": property_value,
                "equity": equity_position,
                "cumulative_cash_flow": cumulative_cash_flow,
            }
        )

        cash_flows.append(annual_cash_flow)

    hold_years = inputs["hold_period_years"]
    exit_value = arv * ((1 + appreciation) ** hold_years)
    selling_costs = exit_value * inputs["selling_cost_pct"]
    loan_balance_exit = loan_balances[hold_years - 1]
    net_sale_proceeds = exit_value - selling_costs - loan_balance_exit
    cash_flows[hold_years] += net_sale_proceeds

    irr_value = float(np.irr(cash_flows)) if any(cash_flows[1:]) else 0.0
    if np.isnan(irr_value):
        irr_value = 0.0
    equity_multiple = sum(cash_flows[1:]) / equity if equity else 0.0

    metrics = {
        "cash_flows": cash_flows,
        "equity_multiple": equity_multiple,
        "irr": irr_value,
        "cash_out_refi": cash_out_refi,
        "loan_balances": loan_balances,
        "exit_value": exit_value,
        "net_sale_proceeds": net_sale_proceeds,
        "loan_balance_exit": loan_balance_exit,
        "cumulative_cash_flows": [p["cumulative_cash_flow"] for p in projections],
    }

    return {"projections": projections, "metrics": metrics}


def compute_exit_comparison(
    inputs: Dict[str, Any], metrics: Dict[str, Any], projections: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Calculate exit strategy comparisons (flip, BRRRR, hold)."""

    selling_cost_pct = inputs["selling_cost_pct"]
    holding_costs = inputs["holding_costs_monthly"] * inputs["holding_period_months"]
    all_in_cost = inputs["purchase_price"] + inputs["closing_costs"] + inputs["renovation_costs"] + holding_costs
    selling_costs_flip = inputs["arv"] * selling_cost_pct
    gross_profit = inputs["arv"] - selling_costs_flip - all_in_cost
    equity_invested = inputs["equity_invested"]
    roi = gross_profit / equity_invested if equity_invested else 0.0
    profit_margin = gross_profit / inputs["arv"] if inputs["arv"] else 0.0

    brrrr_cash_out = metrics["cash_out_refi"]
    brrrr_cash_flow = projections[min(len(projections), 2) - 1]["cash_flow"]

    hold_cash_flow = projections[-1]["cash_flow"]
    hold_monthly_cash_flow = hold_cash_flow / 12

    return {
        "flip": {
            "gross_profit": gross_profit,
            "roi": roi,
            "profit_margin": profit_margin,
        },
        "brrrr": {
            "cash_out": brrrr_cash_out,
            "year_two_cash_flow": brrrr_cash_flow,
        },
        "hold": {
            "year_ten_cash_flow": hold_cash_flow,
            "monthly_cash_flow": hold_monthly_cash_flow,
            "irr": metrics["irr"],
        },
    }


def build_report_tables(
    inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any], exit_metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Produce table definitions used by both CLI and interactive UI."""

    year1 = projections[0]
    hold_years = inputs["hold_period_years"]
    hold_projection = projections[hold_years - 1]
    annual_debt_service = year1["debt_service"]

    cap_rate = year1["noi"] / inputs["total_project_cost"] if inputs["total_project_cost"] else 0.0
    cash_on_cash = year1["cash_flow"] / inputs["equity_invested"] if inputs["equity_invested"] else 0.0
    dscr = year1["noi"] / annual_debt_service if annual_debt_service else 0.0

    property_rows = [
        {"Field": "Property Name", "Value": inputs["project_name"]},
        {"Field": "Location", "Value": inputs["location"]},
        {"Field": "Property Type", "Value": inputs.get("property_type", "Single-Family")},
        {
            "Field": "Square Footage",
            "Value": f"{inputs.get('square_footage', 0):,} sf"
            if inputs.get("square_footage")
            else "N/A",
        },
        {
            "Field": "Bedrooms / Bathrooms",
            "Value": f"{inputs.get('bedrooms', 0)} / {inputs.get('bathrooms', 0)}",
        },
        {"Field": "Year Built", "Value": inputs.get("year_built", "N/A")},
        {"Field": "Analyst", "Value": inputs.get("analyst") or "N/A"},
    ]

    acquisition_metrics = {
        "Purchase Price": format_currency(inputs["purchase_price"]),
        "Closing Costs": format_currency(inputs["closing_costs"]),
        "Renovation Budget": format_currency(inputs["renovation_costs"]),
        "All-In Cost": format_currency(inputs["total_project_cost"]),
        "Initial Loan": format_currency(inputs["loan_amount"]),
        "Equity Invested": format_currency(inputs["equity_invested"]),
        "1% Rule": f"{(inputs['monthly_rent'] / inputs['purchase_price']) * 100:.2f}%",
    }

    year_one_metrics = {
        "Gross Rent": format_currency(year1["gross_rent"]),
        "Vacancy Loss": format_currency(year1["vacancy"]),
        "Effective Income": format_currency(year1["effective_gross_income"]),
        "Operating Expenses": format_currency(year1["operating_expenses"]),
        "NOI": format_currency(year1["noi"]),
        "Cap Rate": format_percentage(cap_rate),
        "Cash Flow": format_currency(year1["cash_flow"]),
        "Cash-on-Cash": format_percentage(cash_on_cash),
        "DSCR": f"{dscr:.2f}",
    }

    hold_metrics = {
        "Hold Years": str(hold_years),
        "Equity at Exit": format_currency(hold_projection["equity"]),
        "Exit Value": format_currency(metrics["exit_value"]),
        "Net Sale Proceeds": format_currency(metrics["net_sale_proceeds"]),
        "Loan Balance at Exit": format_currency(metrics["loan_balance_exit"]),
        "Project IRR": format_percentage(metrics["irr"]),
        "Equity Multiple": f"{metrics['equity_multiple']:.2f}x",
        "BRRRR Cash Out": format_currency(metrics["cash_out_refi"]),
    }

    projection_rows = [
        {
            "Year": str(projection["year"]),
            "Gross Rent": format_currency(projection["gross_rent"]),
            "Vacancy Loss": format_currency(projection["vacancy"]),
            "Effective Income": format_currency(projection["effective_gross_income"]),
            "Operating Expenses": format_currency(projection["operating_expenses"]),
            "NOI": format_currency(projection["noi"]),
            "Debt Service": format_currency(projection["debt_service"]),
            "Cash Flow": format_currency(projection["cash_flow"]),
            "Cumulative CF": format_currency(projection["cumulative_cash_flow"]),
            "Equity": format_currency(projection["equity"]),
            "Property Value": format_currency(projection["property_value"]),
        }
        for projection in projections
    ]

    exit_rows = [
        {
            "Strategy": "Flip",
            "Metric": "Gross Profit",
            "Value": format_currency(exit_metrics["flip"]["gross_profit"]),
        },
        {
            "Strategy": "Flip",
            "Metric": "ROI",
            "Value": format_percentage(exit_metrics["flip"]["roi"]),
        },
        {
            "Strategy": "Flip",
            "Metric": "Profit Margin",
            "Value": format_percentage(exit_metrics["flip"]["profit_margin"]),
        },
        {
            "Strategy": "BRRRR",
            "Metric": "Cash Out at Refi",
            "Value": format_currency(exit_metrics["brrrr"]["cash_out"]),
        },
        {
            "Strategy": "BRRRR",
            "Metric": "Year 2 Cash Flow",
            "Value": format_currency(exit_metrics["brrrr"]["year_two_cash_flow"]),
        },
        {
            "Strategy": "Hold",
            "Metric": "Year 10 Cash Flow",
            "Value": format_currency(exit_metrics["hold"]["year_ten_cash_flow"]),
        },
        {
            "Strategy": "Hold",
            "Metric": "Monthly Cash Flow",
            "Value": format_currency(exit_metrics["hold"]["monthly_cash_flow"]),
        },
        {
            "Strategy": "Hold",
            "Metric": "IRR",
            "Value": format_percentage(exit_metrics["hold"]["irr"]),
        },
    ]

    return [
        {"kind": "table", "title": "Property Information", "columns": ["Field", "Value"], "rows": property_rows},
        {"kind": "metrics", "title": "Acquisition Summary", "metrics": acquisition_metrics},
        {"kind": "metrics", "title": "Year 1 Performance", "metrics": year_one_metrics},
        {"kind": "metrics", "title": "Hold Strategy", "metrics": hold_metrics},
        {
            "kind": "table",
            "title": "10-Year Cash Flow",
            "columns": [
                "Year",
                "Gross Rent",
                "Vacancy Loss",
                "Effective Income",
                "Operating Expenses",
                "NOI",
                "Debt Service",
                "Cash Flow",
                "Cumulative CF",
                "Equity",
                "Property Value",
            ],
            "rows": projection_rows,
        },
        {
            "kind": "table",
            "title": "Exit Strategy Comparison",
            "columns": ["Strategy", "Metric", "Value"],
            "rows": exit_rows,
        },
    ]


def build_chart_specs(
    inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any], exit_metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Chart definitions shared by CLI and UI."""

    years = [projection["year"] for projection in projections]

    return [
        {
            "key": "cash_flow",
            "type": "line",
            "title": "Cash Flow vs NOI vs Debt Service",
            "filename": "cash_flow_trends.png",
            "labels": years,
            "datasets": {
                "NOI": [projection["noi"] for projection in projections],
                "Debt Service": [projection["debt_service"] for projection in projections],
                "Cash Flow": [projection["cash_flow"] for projection in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "equity",
            "type": "line",
            "title": "Equity Growth and Property Value",
            "filename": "equity_build.png",
            "labels": years,
            "datasets": {
                "Equity": [projection["equity"] for projection in projections],
                "Property Value": [projection["property_value"] for projection in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "cumulative",
            "type": "line",
            "title": "Cumulative Cash Flow",
            "filename": "cumulative_cash_flow.png",
            "labels": years,
            "datasets": {"Cumulative Cash Flow": metrics["cumulative_cash_flows"]},
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "exit",
            "type": "bar",
            "title": "Exit Strategy Value Comparison",
            "filename": "exit_strategy_comparison.png",
            "labels": ["Flip Gross Profit", "BRRRR Cash Out", "Hold Net Sale"],
            "datasets": [
                {
                    "label": "Value",
                    "data": [
                        exit_metrics["flip"]["gross_profit"],
                        exit_metrics["brrrr"]["cash_out"],
                        metrics["net_sale_proceeds"],
                    ],
                }
            ],
            "x_label": "Strategy",
            "y_label": "Amount ($)",
        },
    ]


def display_results(
    inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any], exit_metrics: Dict[str, Any]
) -> None:
    """Render model outputs to the console."""

    for table in build_report_tables(inputs, projections, metrics, exit_metrics):
        if table["kind"] == "metrics":
            render_metrics_table(table["title"], table["metrics"])
        else:
            render_projection_table(table["title"], table["columns"], table["rows"])


def generate_visualizations(
    inputs: Dict[str, Any],
    projections: List[Dict[str, Any]],
    metrics: Dict[str, Any],
    exit_metrics: Dict[str, Any],
) -> Dict[str, str]:
    """Create charts mirroring the Excel dashboards and return their paths."""

    report_dir = ensure_report_dir("single_family_rental", inputs["project_name"])
    chart_paths: Dict[str, str] = {}

    for spec in build_chart_specs(inputs, projections, metrics, exit_metrics):
        if spec["type"] == "bar":
            path = save_bar_chart(
                report_dir,
                spec["filename"],
                spec["title"],
                spec["labels"],
                spec["datasets"],
                spec["x_label"],
                spec["y_label"],
            )
        else:
            path = save_line_chart(
                report_dir,
                spec["filename"],
                spec["title"],
                spec["labels"],
                spec["datasets"],
                spec["x_label"],
                spec["y_label"],
            )
        chart_paths[spec["key"]] = str(path)

    console.print(
        Panel(
            "Charts saved to: " + str(report_dir.resolve()),
            title="Visualization Output",
            style="cyan",
        )
    )

    return chart_paths


def gather_inputs() -> Dict[str, Any]:
    """Prompt the user for all model inputs."""

    defaults = DEFAULT_INPUTS

    project_name = prompt_text("Property name or address", default=defaults["project_name"])
    location = prompt_text("Market / Location", default=defaults["location"])
    property_type = prompt_text("Property type", default=defaults["property_type"])
    square_footage = prompt_int("Square footage", default=defaults["square_footage"], minimum=300)
    bedrooms = prompt_int("Bedrooms", default=defaults["bedrooms"], minimum=1, maximum=10)
    bathrooms = prompt_float("Bathrooms", default=defaults["bathrooms"], minimum=1.0, maximum=6.0)
    year_built = prompt_int("Year built", default=defaults["year_built"], minimum=1900, maximum=2025)
    analyst = prompt_text("Analyst name", allow_blank=True) or None

    purchase_price = prompt_float("Purchase price", minimum=50000.0, default=defaults["purchase_price"])
    closing_costs = prompt_float("Closing costs", default=defaults["closing_costs"], minimum=0.0)
    renovation_costs = prompt_float("Renovation budget", default=defaults["renovation_costs"], minimum=0.0)
    arv = prompt_float("After repair value (ARV)", minimum=purchase_price, default=defaults["arv"])
    monthly_rent = prompt_float("Monthly rent", minimum=500.0, default=defaults["monthly_rent"])
    other_income_monthly = prompt_float("Other monthly income (laundry, etc.)", default=defaults["other_income_monthly"])
    rent_growth_rate = prompt_percentage("Annual rent growth", default=defaults["rent_growth_rate"])
    vacancy_rate = prompt_percentage("Vacancy allowance", default=defaults["vacancy_rate"], maximum=0.2)
    appreciation_rate = prompt_percentage("Annual appreciation", default=defaults["appreciation_rate"])

    management_pct = prompt_percentage("Property management fee (% of rent)", default=defaults["management_pct"])
    maintenance_pct = prompt_percentage("Maintenance allowance (% of rent)", default=defaults["maintenance_pct"])
    property_tax_annual = prompt_float("Annual property taxes", default=defaults["property_tax_annual"])
    insurance_annual = prompt_float("Annual insurance", default=defaults["insurance_annual"])
    utilities_monthly = prompt_float("Utilities (monthly)", default=defaults["utilities_monthly"])
    hoa_monthly = prompt_float("HOA (monthly)", default=defaults["hoa_monthly"])
    other_expenses_monthly = prompt_float("Other monthly expenses", default=defaults["other_expenses_monthly"])
    capex_reserve_monthly = prompt_float("Capital reserve (monthly)", default=defaults["capex_reserve_monthly"])
    expense_growth_rate = prompt_percentage("Annual expense growth", default=defaults["expense_growth_rate"])

    down_payment_pct = prompt_percentage("Down payment (% of purchase price)", default=defaults["down_payment_pct"])
    interest_rate = prompt_percentage("Loan interest rate", default=defaults["interest_rate"])
    loan_term_years = prompt_int("Loan term (years)", default=defaults["loan_term_years"], minimum=10, maximum=40)

    selling_cost_pct = prompt_percentage("Selling costs (% of sale price)", default=defaults["selling_cost_pct"])
    hold_period_years = prompt_int("Hold period (years)", default=defaults["hold_period_years"], minimum=5, maximum=10)

    refinance_ltv = prompt_percentage("Refinance LTV", default=defaults["refinance_ltv"], maximum=0.8)
    refinance_rate = prompt_percentage("Refinance interest rate", default=defaults["refinance_rate"])
    refinance_term_years = prompt_int("Refinance term (years)", default=defaults["refinance_term_years"], minimum=10, maximum=40)
    refinance_year = prompt_int("Refinance year (0 for none)", default=defaults["refinance_year"], minimum=0, maximum=5)
    refinance_cost_pct = prompt_percentage("Refinance closing costs (% of new loan)", default=defaults["refinance_cost_pct"])

    holding_costs_monthly = prompt_float("Holding costs during flip (monthly)", default=defaults["holding_costs_monthly"])
    holding_period_months = prompt_int("Holding period for flip (months)", default=defaults["holding_period_months"], minimum=3, maximum=18)

    down_payment = purchase_price * down_payment_pct
    loan_amount = purchase_price - down_payment
    equity_invested = down_payment + closing_costs + renovation_costs
    total_project_cost = purchase_price + closing_costs + renovation_costs

    annual_debt_service = annuity_payment(loan_amount, interest_rate, loan_term_years) * 12

    return prepare_inputs(
        {
            "project_name": project_name,
            "location": location,
            "analyst": analyst,
            "property_type": property_type,
            "square_footage": square_footage,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "year_built": year_built,
            "purchase_price": purchase_price,
            "closing_costs": closing_costs,
            "renovation_costs": renovation_costs,
            "arv": arv,
            "monthly_rent": monthly_rent,
            "other_income_monthly": other_income_monthly,
            "rent_growth_rate": rent_growth_rate,
            "vacancy_rate": vacancy_rate,
            "appreciation_rate": appreciation_rate,
            "management_pct": management_pct,
            "maintenance_pct": maintenance_pct,
            "property_tax_annual": property_tax_annual,
            "insurance_annual": insurance_annual,
            "utilities_monthly": utilities_monthly,
            "hoa_monthly": hoa_monthly,
            "other_expenses_monthly": other_expenses_monthly,
            "capex_reserve_monthly": capex_reserve_monthly,
            "expense_growth_rate": expense_growth_rate,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "loan_term_years": loan_term_years,
            "selling_cost_pct": selling_cost_pct,
            "hold_period_years": hold_period_years,
            "refinance_ltv": refinance_ltv,
            "refinance_rate": refinance_rate,
            "refinance_term_years": refinance_term_years,
            "refinance_year": refinance_year,
            "refinance_cost_pct": refinance_cost_pct,
            "holding_costs_monthly": holding_costs_monthly,
            "holding_period_months": holding_period_months,
        }
    )


def main() -> None:
    """Entry point for the CLI."""

    ensure_database()
    console.print(Panel("Single-Family Rental Model Builder", style="bold white on blue"))
    inputs = gather_inputs()

    output = build_projection(inputs)
    projections = output["projections"]
    metrics = output["metrics"]

    exit_metrics = compute_exit_comparison(inputs, metrics, projections)
    display_results(inputs, projections, metrics, exit_metrics)
    chart_paths = generate_visualizations(inputs, projections, metrics, exit_metrics)

    with session_scope() as session:
        record = SingleFamilyRentalModel(
            name=inputs["project_name"],
            location=inputs["location"],
            analyst=inputs.get("analyst"),
            strategy="BRRRR" if inputs["refinance_year"] else "Buy and Hold",
            inputs=inputs,
            results={
                "projections": projections,
                "metrics": metrics,
                "exit_comparison": exit_metrics,
                "charts": chart_paths,
            },
        )
        session.add(record)
        session.flush()
        console.print(
            Panel(
                f"Single-family rental model saved with ID [bold]{record.id}[/bold]",
                style="green",
            )
        )


if __name__ == "__main__":
    main()
