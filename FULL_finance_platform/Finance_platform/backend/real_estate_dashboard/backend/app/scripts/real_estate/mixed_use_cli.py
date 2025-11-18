"""Mixed-use development financial model derived from the Excel workbook."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np

from .base import annuity_payment, format_currency, format_percentage, remaining_balance


COMPONENTS = ["Multifamily", "Office", "Retail", "Hotel", "Restaurant"]


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Metropolitan Mixed-Use Tower",
    "location": "Chicago, IL",
    "total_building_sf": 500_000.0,
    "analysis_years": 10,
    "multifamily_allocation": 0.4,
    "office_allocation": 0.25,
    "retail_allocation": 0.15,
    "hotel_allocation": 0.15,
    "restaurant_allocation": 0.05,
    "mf_avg_unit_sf": 850.0,
    "mf_avg_rent": 3500.0,
    "mf_occupancy": 0.96,
    "mf_rent_growth": 0.035,
    "mf_other_income_per_unit": 150.0,
    "mf_operating_expense_per_unit": 650.0,
    "office_load_factor": 1.2,
    "office_rent_per_sf": 45.0,
    "office_occupancy": 0.95,
    "office_rent_growth": 0.03,
    "office_expense_per_sf": 15.0,
    "office_expense_recovery": 0.98,
    "retail_rent_per_sf": 55.0,
    "retail_occupancy": 0.92,
    "retail_rent_growth": 0.04,
    "retail_percentage_rent_pct": 0.08,
    "retail_sales_per_sf": 500.0,
    "retail_cam_per_sf": 12.0,
    "retail_expense_per_sf": 18.0,
    "hotel_avg_room_sf": 500.0,
    "hotel_adr": 285.0,
    "hotel_occupancy": 0.75,
    "hotel_revpar_growth": 0.04,
    "hotel_fnb_per_room": 45.0,
    "hotel_other_per_room": 15.0,
    "hotel_operating_expense_pct": 0.65,
    "hotel_management_fee_pct": 0.03,
    "restaurant_rent_per_sf": 60.0,
    "restaurant_percentage_rent_pct": 0.1,
    "restaurant_sales_per_sf": 800.0,
    "restaurant_occupancy": 0.9,
    "restaurant_rent_growth": 0.035,
    "restaurant_expense_per_sf": 20.0,
    "land_cost": 75_000_000.0,
    "hard_cost_per_sf": 425.0,
    "soft_cost_pct": 0.18,
    "mf_ffe_per_unit": 8_000.0,
    "hotel_ffe_per_room": 15_000.0,
    "restaurant_ffe_per_sf": 125.0,
    "developer_fee_pct": 0.03,
    "contingency_pct": 0.05,
    "ltc": 0.65,
    "interest_rate": 0.065,
    "loan_term_years": 30,
    "interest_only_years": 0,
    "loan_fees_pct": 0.015,
    "hold_period_years": 10,
    "mf_exit_cap": 0.048,
    "office_exit_cap": 0.065,
    "retail_exit_cap": 0.06,
    "hotel_exit_cap": 0.07,
    "restaurant_exit_cap": 0.065,
    "selling_cost_pct": 0.025,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text"},
    {"name": "location", "label": "Location", "type": "text"},
    {"name": "total_building_sf", "label": "Gross Building SF", "type": "number", "step": 1000, "min": 100000},
    {"name": "analysis_years", "label": "Analysis Years", "type": "number", "step": 1, "min": 5, "max": 15},
    {"name": "multifamily_allocation", "label": "Multifamily Allocation", "type": "number", "step": 0.01, "min": 0.0, "max": 0.8},
    {"name": "office_allocation", "label": "Office Allocation", "type": "number", "step": 0.01, "min": 0.0, "max": 0.8},
    {"name": "retail_allocation", "label": "Retail Allocation", "type": "number", "step": 0.01, "min": 0.0, "max": 0.6},
    {"name": "hotel_allocation", "label": "Hotel Allocation", "type": "number", "step": 0.01, "min": 0.0, "max": 0.6},
    {"name": "restaurant_allocation", "label": "Restaurant Allocation", "type": "number", "step": 0.005, "min": 0.0, "max": 0.3},
    {"name": "mf_avg_rent", "label": "MF Rent ($/unit/mo)", "type": "number", "step": 50, "min": 1500},
    {"name": "mf_rent_growth", "label": "MF Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.07},
    {"name": "office_rent_per_sf", "label": "Office Rent ($/SF/yr)", "type": "number", "step": 1, "min": 20},
    {"name": "office_rent_growth", "label": "Office Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.06},
    {"name": "retail_rent_per_sf", "label": "Retail Rent ($/SF/yr)", "type": "number", "step": 1, "min": 30},
    {"name": "retail_rent_growth", "label": "Retail Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.08},
    {"name": "hotel_adr", "label": "Hotel ADR ($)", "type": "number", "step": 5, "min": 80},
    {"name": "hotel_revpar_growth", "label": "Hotel RevPAR Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.08},
    {"name": "restaurant_rent_per_sf", "label": "Restaurant Rent ($/SF/yr)", "type": "number", "step": 1, "min": 20},
    {"name": "restaurant_rent_growth", "label": "Restaurant Rent Growth", "type": "number", "step": 0.005, "min": 0.0, "max": 0.06},
    {"name": "hard_cost_per_sf", "label": "Hard Cost ($/SF)", "type": "number", "step": 10, "min": 200},
    {"name": "ltc", "label": "Loan-to-Cost", "type": "number", "step": 0.01, "min": 0.4, "max": 0.8},
    {"name": "interest_rate", "label": "Interest Rate", "type": "number", "step": 0.005, "min": 0.03, "max": 0.12},
    {"name": "hold_period_years", "label": "Hold Period", "type": "number", "step": 1, "min": 5, "max": 12},
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults."""

    data = DEFAULT_INPUTS.copy()
    data.update(overrides)
    return data


def _normalized_allocations(inputs: Dict[str, Any]) -> Dict[str, float]:
    raw = {
        "Multifamily": inputs.get("multifamily_allocation", 0.0),
        "Office": inputs.get("office_allocation", 0.0),
        "Retail": inputs.get("retail_allocation", 0.0),
        "Hotel": inputs.get("hotel_allocation", 0.0),
        "Restaurant": inputs.get("restaurant_allocation", 0.0),
    }
    total = sum(raw.values())
    if total == 0:
        return {component: 0.0 for component in COMPONENTS}
    return {component: value / total for component, value in raw.items()}


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Create a consolidated 10-year projection for the mixed-use development."""

    prepared = inputs.copy()
    allocations = _normalized_allocations(prepared)
    total_sf = prepared["total_building_sf"]

    component_sf = {component: total_sf * allocations[component] for component in COMPONENTS}
    mf_units = max(int(round(component_sf["Multifamily"] / prepared["mf_avg_unit_sf"])), 1)
    hotel_rooms = max(int(round(component_sf["Hotel"] / prepared["hotel_avg_room_sf"])), 0)

    # Development budget
    hard_costs = total_sf * prepared["hard_cost_per_sf"]
    soft_costs = hard_costs * prepared["soft_cost_pct"]
    mf_ffe = mf_units * prepared["mf_ffe_per_unit"]
    hotel_ffe = hotel_rooms * prepared["hotel_ffe_per_room"]
    restaurant_ffe = component_sf["Restaurant"] * prepared["restaurant_ffe_per_sf"]
    subtotal = prepared["land_cost"] + hard_costs + soft_costs + mf_ffe + hotel_ffe + restaurant_ffe
    developer_fee = subtotal * prepared["developer_fee_pct"]
    contingency = (hard_costs + soft_costs) * prepared["contingency_pct"]
    total_development_cost = subtotal + developer_fee + contingency
    loan_amount = total_development_cost * prepared["ltc"]
    loan_fees = loan_amount * prepared["loan_fees_pct"]
    total_project_cost = total_development_cost + loan_fees
    equity = total_project_cost - loan_amount

    # Revenue baselines
    mf_gpr_year1 = mf_units * prepared["mf_avg_rent"] * 12
    mf_other_income_year1 = mf_units * prepared["mf_other_income_per_unit"] * 12
    mf_operating_expense_year1 = mf_units * prepared["mf_operating_expense_per_unit"] * 12

    office_rsf = component_sf["Office"] * prepared["office_load_factor"]
    office_gross_rent_year1 = office_rsf * prepared["office_rent_per_sf"]
    office_net_expense_per_sf = prepared["office_expense_per_sf"] * (1 - prepared["office_expense_recovery"])

    retail_base_rent_year1 = component_sf["Retail"] * prepared["retail_rent_per_sf"] * prepared["retail_occupancy"]
    retail_percentage_rent_year1 = (
        component_sf["Retail"]
        * prepared["retail_sales_per_sf"]
        * prepared["retail_percentage_rent_pct"]
    )
    retail_cam_year1 = component_sf["Retail"] * prepared["retail_cam_per_sf"]
    retail_expenses_year1 = component_sf["Retail"] * prepared["retail_expense_per_sf"]

    hotel_room_revenue_year1 = hotel_rooms * prepared["hotel_adr"] * prepared["hotel_occupancy"] * 365
    hotel_fnb_year1 = hotel_rooms * prepared["hotel_fnb_per_room"] * 365
    hotel_other_year1 = hotel_rooms * prepared["hotel_other_per_room"] * 365

    restaurant_base_rent_year1 = (
        component_sf["Restaurant"]
        * prepared["restaurant_rent_per_sf"]
        * prepared["restaurant_occupancy"]
    )
    restaurant_percentage_rent_year1 = (
        component_sf["Restaurant"]
        * prepared["restaurant_sales_per_sf"]
        * prepared["restaurant_percentage_rent_pct"]
    )
    restaurant_expenses_year1 = component_sf["Restaurant"] * prepared["restaurant_expense_per_sf"]

    analysis_years = min(max(int(prepared["analysis_years"]), 1), 20)
    hold_period = min(max(int(prepared["hold_period_years"]), 1), analysis_years)

    debt_service_schedule: List[float] = []
    io_years = min(prepared.get("interest_only_years", 0), prepared["loan_term_years"])
    amort_years = max(prepared["loan_term_years"] - io_years, 0)
    amort_payment = (
        annuity_payment(loan_amount, prepared["interest_rate"], amort_years) * 12
        if amort_years > 0
        else loan_amount * prepared["interest_rate"]
    )
    for year in range(1, analysis_years + 1):
        if year <= io_years:
            debt_service_schedule.append(loan_amount * prepared["interest_rate"])
        else:
            debt_service_schedule.append(amort_payment)

    projections: List[Dict[str, Any]] = []
    component_details: List[Dict[str, float]] = []
    cumulative_cash_flow = 0.0

    for year in range(1, analysis_years + 1):
        mf_gpr = mf_gpr_year1 * ((1 + prepared["mf_rent_growth"]) ** (year - 1))
        mf_effective_income = mf_gpr * prepared["mf_occupancy"] + (
            mf_other_income_year1 * ((1 + prepared["mf_rent_growth"]) ** (year - 1))
        )
        mf_expenses = mf_operating_expense_year1 * ((1 + prepared["mf_rent_growth"]) ** (year - 1))
        mf_noi = mf_effective_income - mf_expenses

        office_income = office_gross_rent_year1 * ((1 + prepared["office_rent_growth"]) ** (year - 1))
        office_effective_income = office_income * prepared["office_occupancy"]
        office_expenses = office_rsf * office_net_expense_per_sf * ((1 + prepared["office_rent_growth"]) ** (year - 1))
        office_noi = office_effective_income - office_expenses

        retail_income = (
            retail_base_rent_year1 * ((1 + prepared["retail_rent_growth"]) ** (year - 1))
            + retail_percentage_rent_year1 * ((1 + prepared["retail_rent_growth"]) ** (year - 1))
            + retail_cam_year1 * ((1 + prepared["retail_rent_growth"]) ** (year - 1))
        )
        retail_noi = retail_income - retail_expenses_year1 * ((1 + prepared["retail_rent_growth"]) ** (year - 1))

        hotel_total_revenue = (
            hotel_room_revenue_year1 * ((1 + prepared["hotel_revpar_growth"]) ** (year - 1))
            + hotel_fnb_year1 * ((1 + prepared["hotel_revpar_growth"]) ** (year - 1))
            + hotel_other_year1 * ((1 + prepared["hotel_revpar_growth"]) ** (year - 1))
        )
        hotel_operating_expense = hotel_total_revenue * prepared["hotel_operating_expense_pct"]
        hotel_management_fee = hotel_total_revenue * prepared["hotel_management_fee_pct"]
        hotel_noi = hotel_total_revenue - hotel_operating_expense - hotel_management_fee

        restaurant_income = (
            restaurant_base_rent_year1 * ((1 + prepared["restaurant_rent_growth"]) ** (year - 1))
            + restaurant_percentage_rent_year1 * ((1 + prepared["restaurant_rent_growth"]) ** (year - 1))
        )
        restaurant_noi = restaurant_income - restaurant_expenses_year1 * ((1 + prepared["restaurant_rent_growth"]) ** (year - 1))

        component_nois = {
            "Multifamily": mf_noi,
            "Office": office_noi,
            "Retail": retail_noi,
            "Hotel": hotel_noi,
            "Restaurant": restaurant_noi,
        }

        total_noi = sum(component_nois.values())
        total_income = (
            mf_effective_income
            + office_effective_income
            + retail_income
            + hotel_total_revenue
            + restaurant_income
        )

        debt_service = debt_service_schedule[year - 1]
        cash_flow = total_noi - debt_service
        cumulative_cash_flow += cash_flow

        projections.append(
            {
                "year": year,
                "total_income": total_income,
                "total_noi": total_noi,
                "debt_service": debt_service,
                "cash_flow": cash_flow,
                "cumulative_cash_flow": cumulative_cash_flow,
            }
        )
        component_details.append(component_nois)

    exit_year = hold_period
    exit_nois = component_details[exit_year - 1]
    exit_values = {
        "Multifamily": exit_nois["Multifamily"] / prepared["mf_exit_cap"] if prepared["mf_exit_cap"] else 0.0,
        "Office": exit_nois["Office"] / prepared["office_exit_cap"] if prepared["office_exit_cap"] else 0.0,
        "Retail": exit_nois["Retail"] / prepared["retail_exit_cap"] if prepared["retail_exit_cap"] else 0.0,
        "Hotel": exit_nois["Hotel"] / prepared["hotel_exit_cap"] if prepared["hotel_exit_cap"] else 0.0,
        "Restaurant": exit_nois["Restaurant"] / prepared["restaurant_exit_cap"] if prepared["restaurant_exit_cap"] else 0.0,
    }
    total_exit_value = sum(exit_values.values())
    weighted_exit_cap = sum(exit_nois.values()) / total_exit_value if total_exit_value else 0.0
    selling_costs = total_exit_value * prepared["selling_cost_pct"]

    if exit_year <= io_years or amort_years == 0:
        loan_balance_exit = loan_amount
    else:
        payments_made = (exit_year - io_years) * 12
        loan_balance_exit = remaining_balance(loan_amount, prepared["interest_rate"], amort_years, payments_made)

    net_sale = total_exit_value - selling_costs - loan_balance_exit

    cash_flows = [-equity]
    for year, projection in enumerate(projections, start=1):
        cf = projection["cash_flow"]
        if year == exit_year:
            cf += net_sale
        cash_flows.append(cf)

    irr_value = float(np.irr(cash_flows)) if any(cash_flows[1:]) else 0.0
    if np.isnan(irr_value):
        irr_value = 0.0
    equity_multiple = sum(cash_flows[1:]) / equity if equity else 0.0
    cash_on_cash = projections[0]["cash_flow"] / equity if equity else 0.0

    metrics = {
        "component_sf": component_sf,
        "mf_units": mf_units,
        "hotel_rooms": hotel_rooms,
        "hard_costs": hard_costs,
        "soft_costs": soft_costs,
        "mf_ffe": mf_ffe,
        "hotel_ffe": hotel_ffe,
        "restaurant_ffe": restaurant_ffe,
        "developer_fee": developer_fee,
        "contingency": contingency,
        "total_development_cost": total_development_cost,
        "loan_amount": loan_amount,
        "loan_fees": loan_fees,
        "total_project_cost": total_project_cost,
        "equity": equity,
        "component_noi_year1": component_details[0],
        "component_noi_exit": exit_nois,
        "exit_values": exit_values,
        "total_exit_value": total_exit_value,
        "weighted_exit_cap": weighted_exit_cap,
        "selling_costs": selling_costs,
        "loan_balance_exit": loan_balance_exit,
        "net_sale": net_sale,
        "irr": irr_value,
        "equity_multiple": equity_multiple,
        "cash_on_cash": cash_on_cash,
        "cash_flows": cash_flows,
        "cumulative_cash_flows": [row["cumulative_cash_flow"] for row in projections],
        "exit_year": exit_year,
    }

    return {
        "projections": projections,
        "component_details": component_details,
        "metrics": metrics,
    }


def build_report_tables(
    inputs: Dict[str, Any],
    projections: List[Dict[str, Any]],
    component_details: List[Dict[str, float]],
    metrics: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Assemble presentation tables for the interactive UI."""

    allocation_rows = [
        {
            "Component": component,
            "Allocation": format_percentage(metrics["component_sf"][component] / inputs["total_building_sf"] if inputs["total_building_sf"] else 0.0),
            "Square Feet": f"{metrics['component_sf'][component]:,.0f}",
        }
        for component in COMPONENTS
    ]

    development_rows = [
        {"Component": "Land Acquisition", "Amount": format_currency(inputs["land_cost"])},
        {"Component": "Hard Costs", "Amount": format_currency(metrics["hard_costs"])},
        {"Component": "Soft Costs", "Amount": format_currency(metrics["soft_costs"])},
        {"Component": "MF FF&E", "Amount": format_currency(metrics["mf_ffe"])},
        {"Component": "Hotel FF&E", "Amount": format_currency(metrics["hotel_ffe"])},
        {"Component": "Restaurant FF&E", "Amount": format_currency(metrics["restaurant_ffe"])},
        {"Component": "Developer Fee", "Amount": format_currency(metrics["developer_fee"])},
        {"Component": "Contingency", "Amount": format_currency(metrics["contingency"])},
        {"Component": "Loan Fees", "Amount": format_currency(metrics["loan_fees"])},
        {"Component": "Total Project Cost", "Amount": format_currency(metrics["total_project_cost"])},
    ]

    component_year1_rows = [
        {
            "Component": component,
            "Year 1 NOI": format_currency(metrics["component_noi_year1"][component]),
            "Exit NOI": format_currency(metrics["component_noi_exit"][component]),
            "Exit Value": format_currency(metrics["exit_values"][component]),
        }
        for component in COMPONENTS
    ]

    projection_rows = [
        {
            "Year": str(row["year"]),
            "Total Income": format_currency(row["total_income"]),
            "Total NOI": format_currency(row["total_noi"]),
            "Debt Service": format_currency(row["debt_service"]),
            "Cash Flow": format_currency(row["cash_flow"]),
            "Cumulative CF": format_currency(row["cumulative_cash_flow"]),
        }
        for row in projections
    ]

    financing_metrics = {
        "Loan Amount": format_currency(metrics["loan_amount"]),
        "Equity": format_currency(metrics["equity"]),
        "Cash-on-Cash (Y1)": format_percentage(metrics["cash_on_cash"]),
        "Project IRR": format_percentage(metrics["irr"]),
        "Equity Multiple": f"{metrics['equity_multiple']:.2f}x",
        "Weighted Exit Cap": format_percentage(metrics["weighted_exit_cap"]),
        "Net Sale": format_currency(metrics["net_sale"]),
    }

    return [
        {
            "kind": "metrics",
            "title": "Property Overview",
            "metrics": {
                "Building Size": f"{inputs['total_building_sf']:,.0f} SF",
                "Multifamily Units": f"{metrics['mf_units']:,}",
                "Hotel Keys": f"{metrics['hotel_rooms']:,}",
                "Total Project Cost": format_currency(metrics["total_project_cost"]),
                "Loan-to-Cost": format_percentage(inputs["ltc"]),
            },
        },
        {"kind": "table", "title": "Space Allocation", "columns": ["Component", "Allocation", "Square Feet"], "rows": allocation_rows},
        {"kind": "table", "title": "Development Budget", "columns": ["Component", "Amount"], "rows": development_rows},
        {"kind": "table", "title": "Component Performance", "columns": ["Component", "Year 1 NOI", "Exit NOI", "Exit Value"], "rows": component_year1_rows},
        {"kind": "metrics", "title": "Financing & Returns", "metrics": financing_metrics},
        {
            "kind": "table",
            "title": "Consolidated Projection",
            "columns": ["Year", "Total Income", "Total NOI", "Debt Service", "Cash Flow", "Cumulative CF"],
            "rows": projection_rows,
        },
    ]


def build_chart_specs(
    inputs: Dict[str, Any],
    projections: List[Dict[str, Any]],
    component_details: List[Dict[str, float]],
    metrics: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Create chart specifications for the mixed-use model."""

    years = [row["year"] for row in projections]

    component_datasets = {
        component: [detail[component] for detail in component_details]
        for component in COMPONENTS
    }

    return [
        {
            "key": "noi_components",
            "type": "line",
            "title": "Component NOI Progression",
            "labels": years,
            "datasets": component_datasets,
            "x_label": "Year",
            "y_label": "NOI ($)",
        },
        {
            "key": "cash_flow",
            "type": "line",
            "title": "Total NOI vs Cash Flow",
            "labels": years,
            "datasets": {
                "Total NOI": [row["total_noi"] for row in projections],
                "Cash Flow": [row["cash_flow"] for row in projections],
                "Debt Service": [row["debt_service"] for row in projections],
            },
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "cumulative",
            "type": "line",
            "title": "Cumulative Cash Flow",
            "labels": years,
            "datasets": {"Cumulative Cash Flow": metrics["cumulative_cash_flows"]},
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "allocation",
            "type": "bar",
            "title": "Space Allocation Mix",
            "labels": COMPONENTS,
            "datasets": [
                {
                    "label": "Square Feet",
                    "data": [metrics["component_sf"][component] for component in COMPONENTS],
                }
            ],
            "x_label": "Component",
            "y_label": "Square Feet",
        },
    ]

