"""Interactive CLI and shared utilities for the small multifamily model."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from rich.panel import Panel

from app.models.real_estate import SmallMultifamilyModel

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
    "project_name": "Oak Ridge Apartments",
    "location": "Denver, CO",
    "analyst": "",
    "asset_class": "Value-Add",
    "units": 24,
    "purchase_price": 3_900_000.0,
    "closing_costs": 60_000.0,
    "renovation_capex": 300_000.0,
    "current_avg_rent": 1_800.0,
    "target_avg_rent": 2_200.0,
    "vacancy_rate": 0.05,
    "other_income_per_unit": 150.0,
    "property_tax_annual": 130_000.0,
    "insurance_annual": 20_000.0,
    "utilities_per_unit": 1_800.0,
    "repairs_per_unit": 1_200.0,
    "payroll_per_unit": 1_000.0,
    "admin_misc_per_unit": 600.0,
    "capex_reserve_per_unit": 500.0,
    "management_pct": 0.04,
    "rent_growth_rate": 0.03,
    "other_income_growth": 0.02,
    "expense_growth_rate": 0.025,
    "stabilization_years": 3,
    "hold_period_years": 5,
    "exit_cap_rate": 0.055,
    "loan_ltv": 0.65,
    "interest_rate": 0.06,
    "amort_years": 30,
    "location_score": 8,
    "condition_score": 7,
    "financial_score": 6,
    "rent_upside_score": 8,
    "structure_score": 7,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Property Name", "type": "text", "section": "Property Overview"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Overview"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Overview"},
    {"name": "asset_class", "label": "Asset Strategy", "type": "text", "section": "Property Overview"},
    {"name": "units", "label": "Unit Count", "type": "number", "step": 1, "min": 4, "section": "Property Overview"},
    {
        "name": "purchase_price",
        "label": "Purchase Price ($)",
        "type": "number",
        "step": 10000,
        "min": 500000,
        "section": "Acquisition & Capex",
    },
    {
        "name": "closing_costs",
        "label": "Closing Costs ($)",
        "type": "number",
        "step": 5000,
        "min": 0,
        "section": "Acquisition & Capex",
    },
    {
        "name": "renovation_capex",
        "label": "Renovation Budget ($)",
        "type": "number",
        "step": 5000,
        "min": 0,
        "section": "Acquisition & Capex",
    },
    {
        "name": "current_avg_rent",
        "label": "In-place Rent ($)",
        "type": "number",
        "step": 25,
        "min": 400,
        "section": "Revenue Assumptions",
    },
    {
        "name": "target_avg_rent",
        "label": "Target Rent ($)",
        "type": "number",
        "step": 25,
        "min": 400,
        "section": "Revenue Assumptions",
    },
    {
        "name": "vacancy_rate",
        "label": "Vacancy (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 30,
        "format": "percentage",
        "section": "Revenue Assumptions",
    },
    {
        "name": "other_income_per_unit",
        "label": "Other Income / Unit ($)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Revenue Assumptions",
    },
    {
        "name": "rent_growth_rate",
        "label": "Rent Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Revenue Assumptions",
    },
    {
        "name": "other_income_growth",
        "label": "Other Income Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Revenue Assumptions",
    },
    {
        "name": "property_tax_annual",
        "label": "Property Taxes ($ / year)",
        "type": "number",
        "step": 5000,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "insurance_annual",
        "label": "Insurance ($ / year)",
        "type": "number",
        "step": 1000,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "utilities_per_unit",
        "label": "Utilities / Unit ($ / year)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "repairs_per_unit",
        "label": "Repairs & Maintenance / Unit ($ / year)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "payroll_per_unit",
        "label": "Payroll / Unit ($ / year)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "admin_misc_per_unit",
        "label": "Admin & Misc / Unit ($ / year)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "capex_reserve_per_unit",
        "label": "CapEx Reserve / Unit ($ / year)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "management_pct",
        "label": "Management Fee (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 15,
        "format": "percentage",
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
        "name": "stabilization_years",
        "label": "Stabilization Period (years)",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 5,
        "section": "Hold & Exit",
    },
    {
        "name": "hold_period_years",
        "label": "Hold Period (years)",
        "type": "number",
        "step": 1,
        "min": 3,
        "max": 15,
        "section": "Hold & Exit",
    },
    {
        "name": "exit_cap_rate",
        "label": "Exit Cap Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 3,
        "max": 12,
        "format": "percentage",
        "section": "Hold & Exit",
    },
    {
        "name": "loan_ltv",
        "label": "Loan-to-Value (%)",
        "type": "number",
        "step": 1,
        "min": 40,
        "max": 85,
        "format": "percentage",
        "section": "Financing",
    },
    {
        "name": "interest_rate",
        "label": "Interest Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 2,
        "max": 15,
        "format": "percentage",
        "section": "Financing",
    },
    {
        "name": "amort_years",
        "label": "Amortization (years)",
        "type": "number",
        "step": 1,
        "min": 10,
        "max": 40,
        "section": "Financing",
    },
    {
        "name": "location_score",
        "label": "Location Score",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 10,
        "section": "Investment Thesis",
    },
    {
        "name": "condition_score",
        "label": "Condition Score",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 10,
        "section": "Investment Thesis",
    },
    {
        "name": "financial_score",
        "label": "Financial Profile Score",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 10,
        "section": "Investment Thesis",
    },
    {
        "name": "rent_upside_score",
        "label": "Rent Upside Score",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 10,
        "section": "Investment Thesis",
    },
    {
        "name": "structure_score",
        "label": "Deal Structure Score",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 10,
        "section": "Investment Thesis",
    },
    {"name": "project_name", "label": "Property Name", "type": "text"},
    {"name": "location", "label": "Market / Location", "type": "text"},
    {"name": "units", "label": "Unit Count", "type": "number", "step": 1, "min": 5},
    {"name": "purchase_price", "label": "Purchase Price ($)", "type": "number", "step": 10000, "min": 500000},
    {"name": "renovation_capex", "label": "Renovation Budget ($)", "type": "number", "step": 5000, "min": 0},
    {"name": "current_avg_rent", "label": "In-place Rent ($)", "type": "number", "step": 50, "min": 500},
    {"name": "target_avg_rent", "label": "Target Rent ($)", "type": "number", "step": 50, "min": 500},
    {"name": "vacancy_rate", "label": "Vacancy", "type": "number", "step": 0.01, "min": 0.02, "max": 0.15},
    {"name": "rent_growth_rate", "label": "Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.06},
    {"name": "expense_growth_rate", "label": "Expense Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.05},
    {"name": "loan_ltv", "label": "Loan-to-Value", "type": "number", "step": 0.01, "min": 0.5, "max": 0.8},
    {"name": "interest_rate", "label": "Interest Rate", "type": "number", "step": 0.005, "min": 0.03, "max": 0.1},
    {"name": "hold_period_years", "label": "Hold Period (years)", "type": "number", "step": 1, "min": 3, "max": 10},
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults for consistent processing."""

    data = DEFAULT_INPUTS.copy()
    data.update(overrides)
    return data


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Create multi-year operating projections."""

    units = inputs["units"]
    vacancy = inputs["vacancy_rate"]
    rent_growth = inputs["rent_growth_rate"]
    other_income_growth = inputs["other_income_growth"]
    expense_growth = inputs["expense_growth_rate"]
    stabilization_years = inputs["stabilization_years"]
    hold_years = inputs["hold_period_years"]

    loan_amount = inputs["purchase_price"] * inputs["loan_ltv"]
    equity = inputs["purchase_price"] + inputs["closing_costs"] + inputs["renovation_capex"] - loan_amount
    annual_debt_service = annuity_payment(loan_amount, inputs["interest_rate"], inputs["amort_years"]) * 12

    projections: List[Dict[str, Any]] = []
    cumulative_cash_flow = 0.0

    for year in range(1, hold_years + 1):
        if year <= stabilization_years:
            progress = year / stabilization_years
            avg_rent = inputs["current_avg_rent"] + progress * (
                inputs["target_avg_rent"] - inputs["current_avg_rent"]
            )
        else:
            avg_rent = inputs["target_avg_rent"] * ((1 + rent_growth) ** (year - stabilization_years))

        gross_potential = avg_rent * 12 * units
        vacancy_loss = gross_potential * vacancy
        other_income = inputs["other_income_per_unit"] * 12 * units * ((1 + other_income_growth) ** (year - 1))
        effective_gross_income = gross_potential - vacancy_loss + other_income

        property_tax = inputs["property_tax_annual"] * ((1 + expense_growth) ** (year - 1))
        insurance = inputs["insurance_annual"] * ((1 + expense_growth) ** (year - 1))
        utilities = inputs["utilities_per_unit"] * units * ((1 + expense_growth) ** (year - 1))
        repairs = inputs["repairs_per_unit"] * units * ((1 + expense_growth) ** (year - 1))
        payroll = inputs["payroll_per_unit"] * units * ((1 + expense_growth) ** (year - 1))
        admin_misc = inputs["admin_misc_per_unit"] * units * ((1 + expense_growth) ** (year - 1))
        reserves = inputs["capex_reserve_per_unit"] * units * ((1 + expense_growth) ** (year - 1))
        management_fee = effective_gross_income * inputs["management_pct"]

        operating_expenses = (
            property_tax
            + insurance
            + utilities
            + repairs
            + payroll
            + admin_misc
            + reserves
            + management_fee
        )

        noi = effective_gross_income - operating_expenses
        cash_flow = noi - annual_debt_service

        cumulative_cash_flow += cash_flow

        projections.append(
            {
                "year": year,
                "average_rent": avg_rent,
                "gpr": gross_potential,
                "vacancy_loss": vacancy_loss,
                "other_income": other_income,
                "effective_gross_income": effective_gross_income,
                "operating_expenses": operating_expenses,
                "noi": noi,
                "debt_service": annual_debt_service,
                "cash_flow": cash_flow,
                "cumulative_cash_flow": cumulative_cash_flow,
            }
        )

    exit_noi = projections[hold_years - 1]["noi"]
    exit_value = exit_noi / inputs["exit_cap_rate"] if inputs["exit_cap_rate"] else 0.0
    loan_balance_exit = remaining_balance(loan_amount, inputs["interest_rate"], inputs["amort_years"], hold_years * 12)
    net_sale = exit_value - loan_balance_exit

    cash_flows = [-equity]
    for year, projection in enumerate(projections, start=1):
        cf = projection["cash_flow"]
        if year == hold_years:
            cf += net_sale
        cash_flows.append(cf)

    irr_value = float(np.irr(cash_flows)) if any(cash_flows[1:]) else 0.0
    if np.isnan(irr_value):
        irr_value = 0.0
    equity_multiple = sum(cash_flows[1:]) / equity if equity else 0.0
    dscr = projections[0]["noi"] / annual_debt_service if annual_debt_service else 0.0
    cap_rate = projections[0]["noi"] / inputs["purchase_price"] if inputs["purchase_price"] else 0.0
    cash_on_cash = projections[0]["cash_flow"] / equity if equity else 0.0

    opportunity_score = (
        inputs["location_score"]
        + inputs["condition_score"]
        + inputs["financial_score"]
        + inputs["rent_upside_score"]
        + inputs["structure_score"]
    ) / 5

    risk_flags = []
    if cap_rate < 0.05:
        risk_flags.append("Low entry cap rate")
    if dscr < 1.2:
        risk_flags.append("DSCR below 1.20x")
    if projections[0]["cash_flow"] < 0:
        risk_flags.append("Negative year-one cash flow")

    metrics = {
        "equity": equity,
        "loan_amount": loan_amount,
        "annual_debt_service": annual_debt_service,
        "exit_value": exit_value,
        "loan_balance_exit": loan_balance_exit,
        "net_sale": net_sale,
        "irr": irr_value,
        "equity_multiple": equity_multiple,
        "dscr": dscr,
        "cap_rate": cap_rate,
        "cash_on_cash": cash_on_cash,
        "opportunity_score": opportunity_score,
        "risk_flags": risk_flags,
        "cash_flows": cash_flows,
        "cumulative_cash_flows": [p["cumulative_cash_flow"] for p in projections],
    }

    return {"projections": projections, "metrics": metrics}


def build_report_tables(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Show analysis tables."""

    year1 = projections[0]
    hold_years = inputs["hold_period_years"]
    hold_projection = projections[hold_years - 1]

    property_rows = [
        {"Field": "Property", "Value": inputs["project_name"]},
        {"Field": "Location", "Value": inputs["location"]},
        {"Field": "Asset Class", "Value": inputs["asset_class"]},
        {"Field": "Units", "Value": f"{inputs['units']:,}"},
        {"Field": "Analyst", "Value": inputs.get("analyst") or "N/A"},
    ]

    acquisition_metrics = {
        "Purchase Price": format_currency(inputs["purchase_price"]),
        "Closing + CapEx": format_currency(inputs["closing_costs"] + inputs["renovation_capex"]),
        "Loan Amount": format_currency(metrics["loan_amount"]),
        "Equity": format_currency(metrics["equity"]),
        "Opportunity Score": f"{metrics['opportunity_score']:.1f} / 10",
    }

    year_one_metrics = {
        "Average Rent": format_currency(year1["average_rent"]),
        "NOI": format_currency(year1["noi"]),
        "Cap Rate": format_percentage(metrics["cap_rate"]),
        "Cash Flow": format_currency(year1["cash_flow"]),
        "Cash-on-Cash": format_percentage(metrics["cash_on_cash"]),
        "DSCR": f"{metrics['dscr']:.2f}",
    }

    exit_metrics = {
        "Hold Years": hold_years,
        "Stabilized NOI": format_currency(hold_projection["noi"]),
        "Exit Value": format_currency(metrics["exit_value"]),
        "Loan Balance at Exit": format_currency(metrics["loan_balance_exit"]),
        "Net Sale": format_currency(metrics["net_sale"]),
        "Project IRR": format_percentage(metrics["irr"]),
        "Equity Multiple": f"{metrics['equity_multiple']:.2f}x",
    }

    projection_rows = [
        {
            "Year": str(projection["year"]),
            "Avg Rent": format_currency(projection["average_rent"]),
            "GPR": format_currency(projection["gpr"]),
            "Vacancy": format_currency(projection["vacancy_loss"]),
            "Other Income": format_currency(projection["other_income"]),
            "EGI": format_currency(projection["effective_gross_income"]),
            "Expenses": format_currency(projection["operating_expenses"]),
            "NOI": format_currency(projection["noi"]),
            "Debt Service": format_currency(projection["debt_service"]),
            "Cash Flow": format_currency(projection["cash_flow"]),
            "Cumulative CF": format_currency(projection["cumulative_cash_flow"]),
        }
        for projection in projections
    ]

    return [
        {"kind": "table", "title": "Property Overview", "columns": ["Field", "Value"], "rows": property_rows},
        {"kind": "metrics", "title": "Acquisition Overview", "metrics": acquisition_metrics},
        {"kind": "metrics", "title": "Year 1 Performance", "metrics": year_one_metrics},
        {"kind": "metrics", "title": "Exit Summary", "metrics": exit_metrics},
        {
            "kind": "table",
            "title": "Hold Period Projection",
            "columns": [
                "Year",
                "Avg Rent",
                "GPR",
                "Vacancy",
                "Other Income",
                "EGI",
                "Expenses",
                "NOI",
                "Debt Service",
                "Cash Flow",
                "Cumulative CF",
            ],
            "rows": projection_rows,
        },
    ]


def build_chart_specs(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Persist charts similar to the Excel visualization tabs."""

    years = [projection["year"] for projection in projections]

    return [
        {
            "key": "performance",
            "type": "line",
            "title": "NOI, Cash Flow, and Debt Service",
            "filename": "noi_cashflow_debt.png",
            "labels": years,
            "datasets": {
                "NOI": [projection["noi"] for projection in projections],
                "Cash Flow": [projection["cash_flow"] for projection in projections],
                "Debt Service": [projection["debt_service"] for projection in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "income_vs_expense",
            "type": "line",
            "title": "Effective Gross Income vs Operating Expenses",
            "filename": "income_vs_expenses.png",
            "labels": years,
            "datasets": {
                "Effective Gross Income": [projection["effective_gross_income"] for projection in projections],
                "Operating Expenses": [projection["operating_expenses"] for projection in projections],
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
            "key": "opportunity_scores",
            "type": "bar",
            "title": "Opportunity Score Components",
            "filename": "opportunity_scores.png",
            "labels": ["Location", "Condition", "Financial", "Rent Upside", "Structure"],
            "datasets": [
                {
                    "label": "Score",
                    "data": [
                        inputs["location_score"],
                        inputs["condition_score"],
                        inputs["financial_score"],
                        inputs["rent_upside_score"],
                        inputs["structure_score"],
                    ],
                }
            ],
            "x_label": "Category",
            "y_label": "Score",
        },
    ]


def display_results(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> None:
    """CLI entry point for displaying results."""

    for table in build_report_tables(inputs, projections, metrics):
        if table["kind"] == "metrics":
            render_metrics_table(table["title"], table["metrics"])
        else:
            render_projection_table(table["title"], table["columns"], table["rows"])

    if metrics["risk_flags"]:
        console.print(Panel("\n".join(metrics["risk_flags"]), title="Risk Flags", style="bold yellow"))


def generate_visualizations(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> Dict[str, str]:
    """Persist charts similar to the Excel visualization tabs."""

    report_dir = ensure_report_dir("small_multifamily", inputs["project_name"])
    chart_paths: Dict[str, str] = {}

    for spec in build_chart_specs(inputs, projections, metrics):
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
    """Collect property, income, and expense assumptions."""

    defaults = DEFAULT_INPUTS

    project_name = prompt_text("Property name", default=defaults["project_name"])
    location = prompt_text("Market / Location", default=defaults["location"])
    analyst = prompt_text("Analyst name", allow_blank=True) or None
    asset_class = prompt_text("Asset class (Core, Value-Add, etc.)", default=defaults["asset_class"])

    units = prompt_int("Number of units", minimum=5, maximum=100, default=defaults["units"])
    purchase_price = prompt_float("Purchase price", minimum=500000.0, default=defaults["purchase_price"])
    closing_costs = prompt_float("Closing costs", default=defaults["closing_costs"])
    renovation_capex = prompt_float("Renovation / CapEx budget", default=defaults["renovation_capex"])
    current_avg_rent = prompt_float("In-place average rent (monthly)", default=defaults["current_avg_rent"])
    target_avg_rent = prompt_float("Target market rent (monthly)", default=defaults["target_avg_rent"])
    vacancy_rate = prompt_percentage("Stabilized vacancy", default=defaults["vacancy_rate"], maximum=0.15)
    other_income_per_unit = prompt_float("Other income per unit (monthly)", default=defaults["other_income_per_unit"])

    property_tax_annual = prompt_float("Annual property taxes", default=defaults["property_tax_annual"])
    insurance_annual = prompt_float("Annual insurance", default=defaults["insurance_annual"])
    utilities_per_unit = prompt_float("Utilities per unit (annual)", default=defaults["utilities_per_unit"])
    repairs_per_unit = prompt_float("Repairs & maintenance per unit (annual)", default=defaults["repairs_per_unit"])
    payroll_per_unit = prompt_float("Payroll / onsite staff per unit (annual)", default=defaults["payroll_per_unit"])
    admin_misc_per_unit = prompt_float("Admin & misc per unit (annual)", default=defaults["admin_misc_per_unit"])
    capex_reserve_per_unit = prompt_float("Replacement reserve per unit (annual)", default=defaults["capex_reserve_per_unit"])
    management_pct = prompt_percentage("Management fee (% of EGI)", default=defaults["management_pct"])

    rent_growth_rate = prompt_percentage("Rent growth after stabilization", default=defaults["rent_growth_rate"])
    other_income_growth = prompt_percentage("Other income growth", default=defaults["other_income_growth"])
    expense_growth_rate = prompt_percentage("Operating expense growth", default=defaults["expense_growth_rate"])
    stabilization_years = prompt_int("Years to reach market rent", default=defaults["stabilization_years"], minimum=1, maximum=5)
    hold_period_years = prompt_int("Hold period (years)", default=defaults["hold_period_years"], minimum=3, maximum=10)
    exit_cap_rate = prompt_percentage("Exit cap rate", default=defaults["exit_cap_rate"])

    loan_ltv = prompt_percentage("Acquisition LTV", default=defaults["loan_ltv"], maximum=0.8)
    interest_rate = prompt_percentage("Loan interest rate", default=defaults["interest_rate"])
    amort_years = prompt_int("Amortization period (years)", default=defaults["amort_years"], minimum=20, maximum=35)

    location_score = prompt_int("Location score (1-10)", default=defaults["location_score"], minimum=1, maximum=10)
    condition_score = prompt_int("Physical condition score (1-10)", default=defaults["condition_score"], minimum=1, maximum=10)
    financial_score = prompt_int("Financial performance score (1-10)", default=defaults["financial_score"], minimum=1, maximum=10)
    rent_upside_score = prompt_int("Rent upside score (1-10)", default=defaults["rent_upside_score"], minimum=1, maximum=10)
    structure_score = prompt_int("Deal structure score (1-10)", default=defaults["structure_score"], minimum=1, maximum=10)

    return prepare_inputs(
        {
            "project_name": project_name,
            "location": location,
            "analyst": analyst,
            "asset_class": asset_class,
            "units": units,
            "purchase_price": purchase_price,
            "closing_costs": closing_costs,
            "renovation_capex": renovation_capex,
            "current_avg_rent": current_avg_rent,
            "target_avg_rent": target_avg_rent,
            "vacancy_rate": vacancy_rate,
            "other_income_per_unit": other_income_per_unit,
            "property_tax_annual": property_tax_annual,
            "insurance_annual": insurance_annual,
            "utilities_per_unit": utilities_per_unit,
            "repairs_per_unit": repairs_per_unit,
            "payroll_per_unit": payroll_per_unit,
            "admin_misc_per_unit": admin_misc_per_unit,
            "capex_reserve_per_unit": capex_reserve_per_unit,
            "management_pct": management_pct,
            "rent_growth_rate": rent_growth_rate,
            "other_income_growth": other_income_growth,
            "expense_growth_rate": expense_growth_rate,
            "stabilization_years": stabilization_years,
            "hold_period_years": hold_period_years,
            "exit_cap_rate": exit_cap_rate,
            "loan_ltv": loan_ltv,
            "interest_rate": interest_rate,
            "amort_years": amort_years,
            "location_score": location_score,
            "condition_score": condition_score,
            "financial_score": financial_score,
            "rent_upside_score": rent_upside_score,
            "structure_score": structure_score,
        }
    )


def main() -> None:
    """CLI entry point."""

    ensure_database()
    console.print(Panel("Small Multifamily Acquisition Analyzer", style="bold white on blue"))
    inputs = gather_inputs()
    output = build_projection(inputs)
    projections = output["projections"]
    metrics = output["metrics"]
    display_results(inputs, projections, metrics)
    chart_paths = generate_visualizations(inputs, projections, metrics)

    with session_scope() as session:
        record = SmallMultifamilyModel(
            name=inputs["project_name"],
            location=inputs["location"],
            analyst=inputs.get("analyst"),
            asset_class=inputs.get("asset_class"),
            inputs=inputs,
            results={
                "projections": projections,
                "metrics": metrics,
                "charts": chart_paths,
            },
        )
        session.add(record)
        session.flush()
        console.print(
            Panel(
                f"Small multifamily model saved with ID [bold]{record.id}[/bold]",
                style="green",
            )
        )


if __name__ == "__main__":
    main()
