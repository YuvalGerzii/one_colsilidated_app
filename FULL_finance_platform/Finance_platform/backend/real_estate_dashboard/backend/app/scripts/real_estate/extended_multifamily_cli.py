"""High-rise multifamily financial model extracted from the Excel workbook."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

from .base import (
    annuity_payment,
    format_currency,
    format_percentage,
    remaining_balance,
)


UNIT_TYPES: Tuple[str, ...] = ("Studio", "1 Bedroom", "2 Bedroom", "3 Bedroom", "Penthouse")


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Skyline Residences",
    "location": "Downtown Austin, TX",
    "analyst": "",
    "total_units": 250,
    "analysis_years": 10,
    "total_floors": 25,
    "unit_mix_studio_pct": 0.1,
    "unit_mix_one_bed_pct": 0.34,
    "unit_mix_two_bed_pct": 0.44,
    "unit_mix_three_bed_pct": 0.12,
    "unit_mix_penthouse_pct": 0.0,
    "studio_avg_sf": 550.0,
    "one_bed_avg_sf": 750.0,
    "two_bed_avg_sf": 1100.0,
    "three_bed_avg_sf": 1400.0,
    "penthouse_avg_sf": 2500.0,
    "studio_rent": 2200.0,
    "one_bed_rent": 2800.0,
    "two_bed_rent": 3800.0,
    "three_bed_rent": 5200.0,
    "penthouse_rent": 8500.0,
    "physical_occupancy": 0.96,
    "economic_occupancy": 0.95,
    "rent_growth": 0.035,
    "concession_rate": 0.02,
    "bad_debt_rate": 0.005,
    "other_income_per_unit": 150.0,
    "other_income_growth": 0.025,
    "property_management_per_unit": 240.0,
    "staff_per_unit": 180.0,
    "repairs_per_unit": 120.0,
    "utilities_per_unit": 85.0,
    "marketing_per_unit": 45.0,
    "insurance_per_unit": 950.0,
    "taxes_per_unit": 4500.0,
    "reserves_per_unit": 300.0,
    "expense_growth": 0.03,
    "land_cost": 15_000_000.0,
    "hard_cost_per_sf": 325.0,
    "soft_cost_pct": 0.18,
    "ffe_per_unit": 8000.0,
    "developer_fee_pct": 0.03,
    "contingency_pct": 0.05,
    "closing_cost_pct": 0.025,
    "ltc": 0.65,
    "interest_rate": 0.065,
    "loan_term_years": 30,
    "interest_only_years": 2,
    "loan_fees_pct": 0.015,
    "exit_year": 10,
    "exit_cap_rate": 0.05,
    "selling_cost_pct": 0.025,
    "condo_sale_pct": 0.5,
    "condo_premium_pct": 0.25,
    "condo_conversion_cost": 15_000.0,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text"},
    {"name": "location", "label": "Location", "type": "text"},
    {"name": "total_units", "label": "Total Units", "type": "number", "step": 1, "min": 50},
    {"name": "analysis_years", "label": "Analysis Years", "type": "number", "step": 1, "min": 5, "max": 15},
    {"name": "unit_mix_studio_pct", "label": "Studios (% of units)", "type": "number", "step": 0.01, "min": 0.0, "max": 0.5},
    {"name": "unit_mix_one_bed_pct", "label": "1BR (% of units)", "type": "number", "step": 0.01, "min": 0.1, "max": 0.6},
    {"name": "unit_mix_two_bed_pct", "label": "2BR (% of units)", "type": "number", "step": 0.01, "min": 0.1, "max": 0.7},
    {"name": "unit_mix_three_bed_pct", "label": "3BR (% of units)", "type": "number", "step": 0.01, "min": 0.0, "max": 0.3},
    {"name": "unit_mix_penthouse_pct", "label": "Penthouse (% of units)", "type": "number", "step": 0.01, "min": 0.0, "max": 0.15},
    {"name": "studio_rent", "label": "Studio Rent ($/mo)", "type": "number", "step": 50, "min": 1200},
    {"name": "one_bed_rent", "label": "1BR Rent ($/mo)", "type": "number", "step": 50, "min": 1500},
    {"name": "two_bed_rent", "label": "2BR Rent ($/mo)", "type": "number", "step": 50, "min": 1800},
    {"name": "three_bed_rent", "label": "3BR Rent ($/mo)", "type": "number", "step": 50, "min": 2200},
    {"name": "penthouse_rent", "label": "Penthouse Rent ($/mo)", "type": "number", "step": 100, "min": 5000},
    {"name": "rent_growth", "label": "Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.07},
    {"name": "economic_occupancy", "label": "Economic Occupancy", "type": "number", "step": 0.005, "min": 0.8, "max": 1.0},
    {"name": "other_income_per_unit", "label": "Other Income ($/unit/mo)", "type": "number", "step": 10, "min": 0},
    {"name": "expense_growth", "label": "Expense Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.06},
    {"name": "land_cost", "label": "Land Cost ($)", "type": "number", "step": 100000, "min": 0},
    {"name": "hard_cost_per_sf", "label": "Hard Cost ($/SF)", "type": "number", "step": 5, "min": 150},
    {"name": "soft_cost_pct", "label": "Soft Costs (% of hard)", "type": "number", "step": 0.01, "min": 0.05, "max": 0.35},
    {"name": "ltc", "label": "Loan-to-Cost", "type": "number", "step": 0.01, "min": 0.4, "max": 0.8},
    {"name": "interest_rate", "label": "Interest Rate", "type": "number", "step": 0.005, "min": 0.03, "max": 0.12},
    {"name": "exit_cap_rate", "label": "Exit Cap Rate", "type": "number", "step": 0.0025, "min": 0.035, "max": 0.08},
    {"name": "exit_year", "label": "Exit Year", "type": "number", "step": 1, "min": 3, "max": 10},
]


@dataclass
class UnitMixResult:
    counts: Dict[str, int]
    average_rent: float
    average_sf: float
    rentable_sf: float
    gross_potential_rent: float


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults and normalize numeric inputs."""

    data = DEFAULT_INPUTS.copy()
    data.update(overrides)
    return data


def _unit_mix(inputs: Dict[str, Any]) -> UnitMixResult:
    """Translate allocation percentages into discrete unit counts."""

    total_units = int(round(inputs["total_units"]))
    percentages = [
        inputs.get("unit_mix_studio_pct", 0.0),
        inputs.get("unit_mix_one_bed_pct", 0.0),
        inputs.get("unit_mix_two_bed_pct", 0.0),
        inputs.get("unit_mix_three_bed_pct", 0.0),
        inputs.get("unit_mix_penthouse_pct", 0.0),
    ]

    total_pct = sum(percentages)
    if not total_pct:
        percentages = [0.1, 0.34, 0.44, 0.12, 0.0]
        total_pct = 1.0

    normalized = [pct / total_pct for pct in percentages]
    counts: List[int] = []
    remaining = total_units
    for idx, pct in enumerate(normalized):
        if idx == len(normalized) - 1:
            count = max(0, remaining)
        else:
            count = max(0, int(round(total_units * pct)))
            remaining -= count
        counts.append(count)

    rents = [
        inputs["studio_rent"],
        inputs["one_bed_rent"],
        inputs["two_bed_rent"],
        inputs["three_bed_rent"],
        inputs["penthouse_rent"],
    ]
    average_rent = sum(r * c for r, c in zip(rents, counts)) / max(sum(counts), 1)

    sfs = [
        inputs["studio_avg_sf"],
        inputs["one_bed_avg_sf"],
        inputs["two_bed_avg_sf"],
        inputs["three_bed_avg_sf"],
        inputs["penthouse_avg_sf"],
    ]
    rentable_sf = sum(sf * c for sf, c in zip(sfs, counts))
    average_sf = rentable_sf / max(sum(counts), 1)

    gross_potential_rent = sum(rent * count * 12 for rent, count in zip(rents, counts))

    mix_counts = {unit_type: counts[idx] for idx, unit_type in enumerate(UNIT_TYPES)}
    return UnitMixResult(mix_counts, average_rent, average_sf, rentable_sf, gross_potential_rent)


def _base_operating_expense(inputs: Dict[str, Any]) -> float:
    """Calculate year-one operating expenses based on per-unit assumptions."""

    units = inputs["total_units"]
    monthly_per_unit = (
        inputs["property_management_per_unit"]
        + inputs["staff_per_unit"]
        + inputs["repairs_per_unit"]
        + inputs["utilities_per_unit"]
        + inputs["marketing_per_unit"]
    )
    annual_per_unit = (
        inputs["insurance_per_unit"]
        + inputs["taxes_per_unit"]
        + inputs["reserves_per_unit"]
    )
    return units * (monthly_per_unit * 12 + annual_per_unit)


def _debt_service_schedule(inputs: Dict[str, Any], years: int) -> Sequence[float]:
    """Return annual debt service for each projection year."""

    loan_amount = inputs["loan_amount"]
    interest_rate = inputs["interest_rate"]
    io_years = min(inputs.get("interest_only_years", 0), inputs["loan_term_years"])
    amort_years = max(inputs["loan_term_years"] - io_years, 0)

    schedule: List[float] = []
    amort_payment = (
        annuity_payment(loan_amount, interest_rate, amort_years) * 12
        if amort_years > 0
        else loan_amount * interest_rate
    )

    for year in range(1, years + 1):
        if year <= io_years:
            schedule.append(loan_amount * interest_rate)
        else:
            schedule.append(amort_payment)
    return schedule


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a 10-year operating projection and investment metrics."""

    prepared = inputs.copy()
    mix = _unit_mix(prepared)
    prepared["unit_mix"] = mix.counts
    prepared["average_unit_rent"] = mix.average_rent
    prepared["average_unit_sf"] = mix.average_sf
    prepared["rentable_sf"] = mix.rentable_sf
    prepared["gross_potential_rent_year1"] = mix.gross_potential_rent

    other_income_year1 = prepared["other_income_per_unit"] * 12 * prepared["total_units"]
    prepared["other_income_year1"] = other_income_year1

    operating_expense_year1 = _base_operating_expense(prepared)
    prepared["operating_expense_year1"] = operating_expense_year1

    hard_costs = prepared["rentable_sf"] * prepared["hard_cost_per_sf"]
    soft_costs = hard_costs * prepared["soft_cost_pct"]
    ffe_total = prepared["total_units"] * prepared["ffe_per_unit"]
    subtotal = prepared["land_cost"] + hard_costs + soft_costs + ffe_total
    developer_fee = subtotal * prepared["developer_fee_pct"]
    contingency = (hard_costs + soft_costs) * prepared["contingency_pct"]
    closing_costs = prepared["land_cost"] * prepared["closing_cost_pct"]
    total_development_cost = subtotal + developer_fee + contingency + closing_costs
    loan_amount = total_development_cost * prepared["ltc"]
    loan_fees = loan_amount * prepared["loan_fees_pct"]
    total_project_cost = total_development_cost + loan_fees
    equity_requirement = total_project_cost - loan_amount

    prepared.update(
        {
            "hard_costs": hard_costs,
            "soft_costs": soft_costs,
            "ffe_total": ffe_total,
            "developer_fee": developer_fee,
            "contingency": contingency,
            "closing_costs": closing_costs,
            "total_development_cost": total_development_cost,
            "loan_amount": loan_amount,
            "loan_fees": loan_fees,
            "total_project_cost": total_project_cost,
            "equity_requirement": equity_requirement,
        }
    )

    analysis_years = min(max(int(prepared["analysis_years"]), 1), 20)
    rent_growth = prepared["rent_growth"]
    other_income_growth = prepared["other_income_growth"]
    expense_growth = prepared["expense_growth"]
    egr = prepared["economic_occupancy"]
    concession = prepared["concession_rate"]
    bad_debt = prepared["bad_debt_rate"]

    gpr_year1 = mix.gross_potential_rent
    debt_service_schedule = _debt_service_schedule(prepared, analysis_years)

    projections: List[Dict[str, Any]] = []
    cumulative_cash_flow = 0.0

    for year in range(1, analysis_years + 1):
        rent_multiplier = (1 + rent_growth) ** (year - 1)
        gpr = gpr_year1 * rent_multiplier
        vacancy_loss = gpr * (1 - egr)
        concession_loss = gpr * concession
        bad_debt_loss = gpr * bad_debt
        other_income = other_income_year1 * ((1 + other_income_growth) ** (year - 1))
        effective_gross_income = gpr - vacancy_loss - concession_loss - bad_debt_loss + other_income

        operating_expenses = operating_expense_year1 * ((1 + expense_growth) ** (year - 1))
        noi = effective_gross_income - operating_expenses
        debt_service = debt_service_schedule[year - 1]
        cash_flow = noi - debt_service
        cumulative_cash_flow += cash_flow

        projections.append(
            {
                "year": year,
                "gross_potential_rent": gpr,
                "vacancy_loss": vacancy_loss,
                "concession_loss": concession_loss,
                "bad_debt_loss": bad_debt_loss,
                "other_income": other_income,
                "effective_gross_income": effective_gross_income,
                "operating_expenses": operating_expenses,
                "noi": noi,
                "noi_margin": noi / effective_gross_income if effective_gross_income else 0.0,
                "debt_service": debt_service,
                "cash_flow": cash_flow,
                "cumulative_cash_flow": cumulative_cash_flow,
            }
        )

    exit_year = min(max(int(prepared["exit_year"]), 1), analysis_years)
    exit_projection = projections[exit_year - 1]
    exit_noi = exit_projection["noi"]
    exit_value = exit_noi / prepared["exit_cap_rate"] if prepared["exit_cap_rate"] else 0.0
    io_years = min(prepared.get("interest_only_years", 0), prepared["loan_term_years"])
    amort_years = max(prepared["loan_term_years"] - io_years, 0)
    if exit_year <= io_years or amort_years == 0:
        loan_balance_exit = loan_amount
    else:
        payments_made = (exit_year - io_years) * 12
        loan_balance_exit = remaining_balance(loan_amount, prepared["interest_rate"], amort_years, payments_made)
    selling_costs = exit_value * prepared["selling_cost_pct"]
    net_sale_proceeds = exit_value - selling_costs - loan_balance_exit

    condo_units = sum(mix.counts.values()) * prepared["condo_sale_pct"]
    condo_value_per_unit = (
        (exit_noi / max(sum(mix.counts.values()), 1)) / prepared["exit_cap_rate"]
        if prepared["exit_cap_rate"]
        else 0.0
    )
    condo_sale_value = condo_units * condo_value_per_unit * (1 + prepared["condo_premium_pct"])
    condo_conversion_costs = condo_units * prepared["condo_conversion_cost"]
    condo_net_value = condo_sale_value - condo_conversion_costs

    cash_flows = [-equity_requirement]
    for year, projection in enumerate(projections, start=1):
        cf = projection["cash_flow"]
        if year == exit_year:
            cf += net_sale_proceeds
        cash_flows.append(cf)

    irr_value = float(np.irr(cash_flows)) if any(cash_flows[1:]) else 0.0
    if np.isnan(irr_value):
        irr_value = 0.0
    equity_multiple = sum(cash_flows[1:]) / equity_requirement if equity_requirement else 0.0
    year1 = projections[0]
    stabilized_cap_rate = year1["noi"] / total_project_cost if total_project_cost else 0.0
    cash_on_cash = year1["cash_flow"] / equity_requirement if equity_requirement else 0.0

    metrics = {
        "unit_mix": mix.counts,
        "average_unit_rent": mix.average_rent,
        "average_unit_sf": mix.average_sf,
        "rentable_sf": mix.rentable_sf,
        "gross_potential_rent_year1": gpr_year1,
        "other_income_year1": other_income_year1,
        "operating_expense_year1": operating_expense_year1,
        "hard_costs": hard_costs,
        "soft_costs": soft_costs,
        "ffe_total": ffe_total,
        "developer_fee": developer_fee,
        "contingency": contingency,
        "closing_costs": closing_costs,
        "total_development_cost": total_development_cost,
        "loan_amount": loan_amount,
        "loan_fees": loan_fees,
        "total_project_cost": total_project_cost,
        "equity_requirement": equity_requirement,
        "exit_noi": exit_noi,
        "exit_value": exit_value,
        "selling_costs": selling_costs,
        "loan_balance_exit": loan_balance_exit,
        "net_sale_proceeds": net_sale_proceeds,
        "condo_sale_value": condo_sale_value,
        "condo_conversion_costs": condo_conversion_costs,
        "condo_net_value": condo_net_value,
        "irr": irr_value,
        "equity_multiple": equity_multiple,
        "cash_on_cash": cash_on_cash,
        "stabilized_cap_rate": stabilized_cap_rate,
        "noi_margin_year1": year1["noi_margin"],
        "cash_flows": cash_flows,
        "cumulative_cash_flows": [p["cumulative_cash_flow"] for p in projections],
        "exit_year": exit_year,
    }

    return {"projections": projections, "metrics": metrics}


def build_report_tables(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build structured tables for the interactive UI."""

    unit_mix_rows = [
        {
            "Unit Type": unit_type,
            "Count": f"{metrics['unit_mix'][unit_type]:,}",
            "Avg SF": f"{inputs[f'{label}_avg_sf']:.0f}",
            "Rent": format_currency(inputs[f"{label}_rent"]),
        }
        for unit_type, label in zip(UNIT_TYPES, ["studio", "one_bed", "two_bed", "three_bed", "penthouse"])
    ]

    development_rows = [
        {"Component": "Land Acquisition", "Amount": format_currency(inputs["land_cost"])},
        {"Component": "Hard Costs", "Amount": format_currency(metrics["hard_costs"])},
        {"Component": "Soft Costs", "Amount": format_currency(metrics["soft_costs"])},
        {"Component": "FF&E", "Amount": format_currency(metrics["ffe_total"])},
        {"Component": "Developer Fee", "Amount": format_currency(metrics["developer_fee"])},
        {"Component": "Contingency", "Amount": format_currency(metrics["contingency"])},
        {"Component": "Closing Costs", "Amount": format_currency(metrics["closing_costs"])},
        {"Component": "Loan Fees", "Amount": format_currency(metrics["loan_fees"])},
        {"Component": "Total Project Cost", "Amount": format_currency(metrics["total_project_cost"])},
    ]

    financing_metrics = {
        "Loan Amount": format_currency(metrics["loan_amount"]),
        "Equity Requirement": format_currency(metrics["equity_requirement"]),
        "Stabilized Cap Rate": format_percentage(metrics["stabilized_cap_rate"]),
        "Cash-on-Cash (Y1)": format_percentage(metrics["cash_on_cash"]),
        "NOI Margin (Y1)": format_percentage(metrics["noi_margin_year1"]),
        "Project IRR": format_percentage(metrics["irr"]),
        "Equity Multiple": f"{metrics['equity_multiple']:.2f}x",
    }

    exit_metrics = {
        "Exit Year": metrics["exit_year"],
        "Exit NOI": format_currency(metrics["exit_noi"]),
        "Exit Value": format_currency(metrics["exit_value"]),
        "Selling Costs": format_currency(metrics["selling_costs"]),
        "Loan Balance": format_currency(metrics["loan_balance_exit"]),
        "Net Sale Proceeds": format_currency(metrics["net_sale_proceeds"]),
        "Condo Net Value": format_currency(metrics["condo_net_value"]),
    }

    projection_rows = [
        {
            "Year": str(row["year"]),
            "GPR": format_currency(row["gross_potential_rent"]),
            "Vacancy": format_currency(row["vacancy_loss"]),
            "Concessions": format_currency(row["concession_loss"]),
            "Bad Debt": format_currency(row["bad_debt_loss"]),
            "Other Income": format_currency(row["other_income"]),
            "EGI": format_currency(row["effective_gross_income"]),
            "OpEx": format_currency(row["operating_expenses"]),
            "NOI": format_currency(row["noi"]),
            "NOI Margin": format_percentage(row["noi_margin"]),
            "Debt Service": format_currency(row["debt_service"]),
            "Cash Flow": format_currency(row["cash_flow"]),
            "Cumulative CF": format_currency(row["cumulative_cash_flow"]),
        }
        for row in projections
    ]

    return [
        {"kind": "table", "title": "Unit Mix", "columns": ["Unit Type", "Count", "Avg SF", "Rent"], "rows": unit_mix_rows},
        {
            "kind": "metrics",
            "title": "Key Metrics",
            "metrics": {
                "Average Unit Rent": format_currency(metrics["average_unit_rent"]),
                "Average Unit Size": f"{metrics['average_unit_sf']:.0f} SF",
                "Total Rentable SF": f"{metrics['rentable_sf']:,.0f} SF",
                "Year 1 GPR": format_currency(metrics["gross_potential_rent_year1"]),
                "Year 1 Other Income": format_currency(metrics["other_income_year1"]),
                "Year 1 Operating Expenses": format_currency(metrics["operating_expense_year1"]),
            },
        },
        {"kind": "table", "title": "Development Budget", "columns": ["Component", "Amount"], "rows": development_rows},
        {"kind": "metrics", "title": "Financing & Returns", "metrics": financing_metrics},
        {"kind": "metrics", "title": "Exit Scenario", "metrics": exit_metrics},
        {
            "kind": "table",
            "title": "10-Year Projection",
            "columns": [
                "Year",
                "GPR",
                "Vacancy",
                "Concessions",
                "Bad Debt",
                "Other Income",
                "EGI",
                "OpEx",
                "NOI",
                "NOI Margin",
                "Debt Service",
                "Cash Flow",
                "Cumulative CF",
            ],
            "rows": projection_rows,
        },
    ]


def build_chart_specs(inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return chart definitions used by the UI for visualization."""

    years = [row["year"] for row in projections]

    return [
        {
            "key": "noi_vs_expenses",
            "type": "line",
            "title": "Effective Gross Income vs Operating Expenses",
            "labels": years,
            "datasets": {
                "Effective Gross Income": [row["effective_gross_income"] for row in projections],
                "Operating Expenses": [row["operating_expenses"] for row in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "noi_cashflow",
            "type": "line",
            "title": "NOI and Cash Flow",
            "labels": years,
            "datasets": {
                "NOI": [row["noi"] for row in projections],
                "Cash Flow": [row["cash_flow"] for row in projections],
                "Debt Service": [row["debt_service"] for row in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "cumulative_cf",
            "type": "line",
            "title": "Cumulative Cash Flow",
            "labels": years,
            "datasets": {"Cumulative Cash Flow": metrics["cumulative_cash_flows"]},
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "unit_mix",
            "type": "bar",
            "title": "Unit Mix Distribution",
            "labels": list(metrics["unit_mix"].keys()),
            "datasets": [
                {
                    "label": "Units",
                    "data": [metrics["unit_mix"][unit] for unit in metrics["unit_mix"]],
                }
            ],
            "x_label": "Unit Type",
            "y_label": "Count",
        },
    ]

