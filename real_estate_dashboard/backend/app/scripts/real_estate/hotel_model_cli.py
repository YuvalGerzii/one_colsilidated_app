"""Interactive CLI for the hotel financial model."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import numpy_financial as npf
from rich.panel import Panel

from app.models.real_estate import HotelFinancialModel

from .base import (
    annuity_payment,
    console,
    ensure_database,
    ensure_report_dir,
    format_currency,
    format_percentage,
    prompt_choice,
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
    "project_name": "Harbor View Hotel",
    "hotel_type": "Upscale",
    "location": "Miami, FL",
    "brand_affiliation": "Independent",
    "analyst": "",
    "rooms": 180,
    "adr": 210.0,
    "year1_occupancy": 0.55,
    "stabilized_occupancy": 0.7,
    "adr_growth_rate": 0.03,
    "fnb_growth_rate": 0.03,
    "other_income_growth_rate": 0.02,
    "fnb_outlet_per_room_day": 35.0,
    "banquet_rev_per_group_room": 90.0,
    "group_room_pct": 0.3,
    "meeting_rev_per_room": 1000.0,
    "parking_rev_per_room": 800.0,
    "spa_rev_per_room": 300.0,
    "other_operated_rev_per_room": 500.0,
    "rooms_dept_pct": 0.28,
    "fnb_dept_pct": 0.65,
    "other_dept_pct": 0.35,
    "admin_per_room": 8000.0,
    "maintenance_per_room": 3200.0,
    "utilities_per_room": 2600.0,
    "insurance_pct": 0.015,
    "property_tax_pct": 0.035,
    "expense_growth_rate": 0.03,
    "total_project_cost": 45_000_000.0,
    "loan_to_cost": 0.6,
    "interest_rate": 0.065,
    "amort_years": 25,
    "hold_period_years": 5,
    "exit_cap_rate": 0.075,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text", "section": "Property Overview"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Overview"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Overview"},
    {
        "name": "brand_affiliation",
        "label": "Brand Affiliation",
        "type": "text",
        "section": "Property Overview",
    },
    {"name": "project_name", "label": "Project Name", "type": "text"},
    {"name": "location", "label": "Market / Location", "type": "text"},
    {
        "name": "hotel_type",
        "label": "Hotel Segment",
        "type": "text",
        "options": ["Luxury", "Upper Upscale", "Upscale", "Midscale", "Economy"],
        "section": "Property Overview",
    },
    {"name": "rooms", "label": "Room Count", "type": "number", "step": 1, "min": 20, "section": "Room & Demand"},
    {"name": "adr", "label": "Year 1 ADR ($)", "type": "number", "step": 5, "min": 50, "section": "Room & Demand"},
    {
        "name": "year1_occupancy",
        "label": "Year 1 Occupancy (%)",
        "type": "number",
        "step": 0.5,
        "min": 20,
        "max": 90,
        "format": "percentage",
        "section": "Room & Demand",
    },
    {
        "name": "stabilized_occupancy",
        "label": "Stabilized Occupancy (%)",
        "type": "number",
        "step": 0.5,
        "min": 30,
        "max": 95,
        "format": "percentage",
        "section": "Room & Demand",
    },
    {
        "name": "adr_growth_rate",
        "label": "ADR Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Room & Demand",
    },
    {
        "name": "fnb_growth_rate",
        "label": "F&B Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Room & Demand",
    },
    {
        "name": "other_income_growth_rate",
        "label": "Other Income Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Room & Demand",
    },
    {
        "name": "fnb_outlet_per_room_day",
        "label": "F&B Outlet Rev / Room-Night ($)",
        "type": "number",
        "step": 5,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "banquet_rev_per_group_room",
        "label": "Banquet Rev / Group Room ($)",
        "type": "number",
        "step": 5,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "group_room_pct",
        "label": "Group Room Mix (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 80,
        "format": "percentage",
        "section": "Ancillary Revenue",
    },
    {
        "name": "meeting_rev_per_room",
        "label": "Meeting & Events Rev / Room ($)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "parking_rev_per_room",
        "label": "Parking Rev / Room ($)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "spa_rev_per_room",
        "label": "Spa Rev / Room ($)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "other_operated_rev_per_room",
        "label": "Other Operated Rev / Room ($)",
        "type": "number",
        "step": 10,
        "min": 0,
        "section": "Ancillary Revenue",
    },
    {
        "name": "rooms_dept_pct",
        "label": "Rooms Dept. Margin (%)",
        "type": "number",
        "step": 1,
        "min": 10,
        "max": 80,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "fnb_dept_pct",
        "label": "F&B Dept. Margin (%)",
        "type": "number",
        "step": 1,
        "min": 20,
        "max": 90,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "other_dept_pct",
        "label": "Other Operated Margin (%)",
        "type": "number",
        "step": 1,
        "min": 10,
        "max": 80,
        "format": "percentage",
        "section": "Operating Expenses",
    },
    {
        "name": "admin_per_room",
        "label": "Admin & GM / Room ($)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "maintenance_per_room",
        "label": "Maintenance / Room ($)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "utilities_per_room",
        "label": "Utilities / Room ($)",
        "type": "number",
        "step": 25,
        "min": 0,
        "section": "Operating Expenses",
    },
    {
        "name": "insurance_pct",
        "label": "Insurance (% of Rev)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Fixed Charges & Escalators",
    },
    {
        "name": "property_tax_pct",
        "label": "Property Tax (% of Rev)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Fixed Charges & Escalators",
    },
    {
        "name": "expense_growth_rate",
        "label": "Expense Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 12,
        "format": "percentage",
        "section": "Fixed Charges & Escalators",
    },
    {
        "name": "total_project_cost",
        "label": "Total Project Cost ($)",
        "type": "number",
        "step": 100000,
        "min": 1_000_000,
        "section": "Financing & Exit",
    },
    {
        "name": "loan_to_cost",
        "label": "Loan-to-Cost (%)",
        "type": "number",
        "step": 1,
        "min": 30,
        "max": 85,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {
        "name": "interest_rate",
        "label": "Interest Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 2,
        "max": 15,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {
        "name": "amort_years",
        "label": "Amortization (years)",
        "type": "number",
        "step": 1,
        "min": 5,
        "max": 40,
        "section": "Financing & Exit",
    },
    {
        "name": "hold_period_years",
        "label": "Hold Period (years)",
        "type": "number",
        "step": 1,
        "min": 3,
        "max": 15,
        "section": "Financing & Exit",
    },
    {
        "name": "exit_cap_rate",
        "label": "Exit Cap Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 5,
        "max": 15,
        "format": "percentage",
        "section": "Financing & Exit",
    },
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults and compute financing fields."""

    merged = DEFAULT_INPUTS.copy()
    merged.update(overrides)
    loan_amount = merged["total_project_cost"] * merged["loan_to_cost"]
    equity = merged["total_project_cost"] - loan_amount
    annual_debt_service = annuity_payment(loan_amount, merged["interest_rate"], merged["amort_years"]) * 12
    merged.update(
        {
            "loan_amount": loan_amount,
            "equity": equity,
            "annual_debt_service": annual_debt_service,
        }
    )
    return merged


def build_projection(inputs: Dict[str, float]) -> Dict[str, Any]:
    """Generate multi-year projections and return summary metrics."""

    rooms = inputs["rooms"]
    projection_years = max(5, inputs["hold_period_years"])
    debt_service = inputs["annual_debt_service"]
    expense_growth = inputs["expense_growth_rate"]
    fnb_growth = inputs["fnb_growth_rate"]
    other_growth = inputs["other_income_growth_rate"]
    adr_growth = inputs["adr_growth_rate"]
    stabilized_occupancy = inputs["stabilized_occupancy"]
    year1_occupancy = inputs["year1_occupancy"]

    projections: List[Dict[str, float]] = []
    adr = inputs["adr"]
    fnb_outlet = inputs["fnb_outlet_per_room_day"]
    banquet = inputs["banquet_rev_per_group_room"]
    group_pct = inputs["group_room_pct"]
    other_components = (
        inputs["meeting_rev_per_room"]
        + inputs["parking_rev_per_room"]
        + inputs["spa_rev_per_room"]
        + inputs["other_operated_rev_per_room"]
    )

    departmental_pcts = {
        "rooms": inputs["rooms_dept_pct"],
        "fnb": inputs["fnb_dept_pct"],
        "other": inputs["other_dept_pct"],
    }

    per_room_costs = {
        "admin": inputs["admin_per_room"],
        "maintenance": inputs["maintenance_per_room"],
        "utilities": inputs["utilities_per_room"],
    }

    cumulative_cash_flow = 0.0

    for year in range(1, projection_years + 1):
        occupancy = year1_occupancy if year == 1 else stabilized_occupancy
        adr_year = adr * ((1 + adr_growth) ** (year - 1))
        rooms_sold = rooms * 365 * occupancy
        rooms_revenue = rooms_sold * adr_year

        fnb_multiplier = (1 + fnb_growth) ** (year - 1)
        restaurant_revenue = fnb_outlet * rooms * 365 * fnb_multiplier
        banquet_revenue = banquet * rooms_sold * group_pct * fnb_multiplier
        fnb_revenue = restaurant_revenue + banquet_revenue

        other_revenue = rooms * other_components * ((1 + other_growth) ** (year - 1))
        total_revenue = rooms_revenue + fnb_revenue + other_revenue

        rooms_expense = rooms_revenue * departmental_pcts["rooms"]
        fnb_expense = fnb_revenue * departmental_pcts["fnb"]
        other_expense = other_revenue * departmental_pcts["other"]
        departmental_expenses = rooms_expense + fnb_expense + other_expense

        undistributed = sum(
            rooms * cost * ((1 + expense_growth) ** (year - 1))
            for cost in per_room_costs.values()
        )
        insurance = total_revenue * inputs["insurance_pct"]
        property_tax = total_revenue * inputs["property_tax_pct"]
        total_expenses = departmental_expenses + undistributed + insurance + property_tax

        gop = total_revenue - departmental_expenses
        noi = total_revenue - total_expenses
        cash_flow = noi - debt_service
        cumulative_cash_flow += cash_flow
        revpar = adr_year * occupancy

        projections.append(
            {
                "year": year,
                "occupancy": occupancy,
                "adr": adr_year,
                "revpar": revpar,
                "rooms_revenue": rooms_revenue,
                "fnb_revenue": fnb_revenue,
                "other_revenue": other_revenue,
                "total_revenue": total_revenue,
                "departmental_expenses": departmental_expenses,
                "undistributed": undistributed,
                "insurance": insurance,
                "property_tax": property_tax,
                "total_expenses": total_expenses,
                "gop": gop,
                "gop_margin": gop / total_revenue if total_revenue else 0.0,
                "noi": noi,
                "noi_margin": noi / total_revenue if total_revenue else 0.0,
                "cash_flow": cash_flow,
                "cumulative_cash_flow": cumulative_cash_flow,
            }
        )

    hold_years = inputs["hold_period_years"]
    exit_cap_rate = inputs["exit_cap_rate"]
    loan_amount = inputs["loan_amount"]
    annual_rate = inputs["interest_rate"]
    amort_years = inputs["amort_years"]

    loan_balance_exit = remaining_balance(
        loan_amount,
        annual_rate,
        amort_years,
        hold_years * 12,
    )
    noi_exit = projections[hold_years - 1]["noi"]
    exit_value = noi_exit / exit_cap_rate if exit_cap_rate else 0.0
    net_sale = exit_value - loan_balance_exit

    equity = inputs["equity"]
    cash_flows = [-equity]
    for year, projection in enumerate(projections, start=1):
        cf = projection["cash_flow"]
        if year == hold_years:
            cf += net_sale
        cash_flows.append(cf)

    irr_value = float(npf.irr(cash_flows)) if any(cash_flows[1:]) else 0.0
    if np.isnan(irr_value):
        irr_value = 0.0
    irr = irr_value
    equity_multiple = sum(cash_flows[1:]) / equity if equity else 0.0
    dscr = projections[0]["noi"] / debt_service if debt_service else 0.0

    summary = {
        "cash_flows": cash_flows,
        "equity_multiple": equity_multiple,
        "irr": irr,
        "dscr": dscr,
        "exit_value": exit_value,
        "net_sale_proceeds": net_sale,
        "loan_balance_exit": loan_balance_exit,
        "projections": projections,
        "cumulative_cash_flows": [p["cumulative_cash_flow"] for p in projections],
    }

    return summary


def build_report_tables(inputs: Dict[str, Any], summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return table definitions shared by the CLI and interactive UI."""

    projections = summary["projections"]
    year1 = projections[0]
    hold_years = inputs["hold_period_years"]
    hold_projection = projections[hold_years - 1]

    property_rows = [
        {"Field": "Property", "Value": inputs["project_name"]},
        {"Field": "Location", "Value": inputs["location"]},
        {"Field": "Hotel Type", "Value": inputs["hotel_type"]},
        {"Field": "Brand", "Value": inputs.get("brand_affiliation", "Independent")},
        {"Field": "Room Count", "Value": f"{inputs['rooms']:,}"},
        {"Field": "Analyst", "Value": inputs.get("analyst") or "N/A"},
    ]

    year_one_metrics = {
        "Occupancy": format_percentage(year1["occupancy"]),
        "ADR": format_currency(year1["adr"]),
        "RevPAR": format_currency(year1["revpar"]),
        "Total Revenue": format_currency(year1["total_revenue"]),
        "Departmental Expenses": format_currency(year1["departmental_expenses"]),
        "NOI": format_currency(year1["noi"]),
        "NOI Margin": format_percentage(year1["noi_margin"]),
        "Cash Flow": format_currency(year1["cash_flow"]),
        "DSCR": f"{summary['dscr']:.2f}",
    }

    investment_metrics = {
        "Total Project Cost": format_currency(inputs["total_project_cost"]),
        "Equity Invested": format_currency(inputs["equity"]),
        "Annual Debt Service": format_currency(inputs["annual_debt_service"]),
        "Equity Multiple": f"{summary['equity_multiple']:.2f}x",
        "Project IRR": format_percentage(summary["irr"]),
    }

    hold_metrics = {
        "Hold Years": hold_years,
        "Stabilized NOI": format_currency(hold_projection["noi"]),
        "Exit Value": format_currency(summary["exit_value"]),
        "Net Sale Proceeds": format_currency(summary["net_sale_proceeds"]),
        "Loan Balance at Exit": format_currency(summary["loan_balance_exit"]),
    }

    revenue_mix_rows = [
        {
            "Stream": "Rooms",
            "Year 1": format_currency(year1["rooms_revenue"]),
            "Share": format_percentage(year1["rooms_revenue"] / year1["total_revenue"] if year1["total_revenue"] else 0.0),
        },
        {
            "Stream": "Food & Beverage",
            "Year 1": format_currency(year1["fnb_revenue"]),
            "Share": format_percentage(year1["fnb_revenue"] / year1["total_revenue"] if year1["total_revenue"] else 0.0),
        },
        {
            "Stream": "Other",
            "Year 1": format_currency(year1["other_revenue"]),
            "Share": format_percentage(year1["other_revenue"] / year1["total_revenue"] if year1["total_revenue"] else 0.0),
        },
    ]

    pro_forma_rows = [
        {
            "Year": str(projection["year"]),
            "Occ %": f"{projection['occupancy']*100:.1f}%",
            "ADR": format_currency(projection["adr"]),
            "RevPAR": format_currency(projection["revpar"]),
            "Rooms Rev": format_currency(projection["rooms_revenue"]),
            "F&B Rev": format_currency(projection["fnb_revenue"]),
            "Other Rev": format_currency(projection["other_revenue"]),
            "Total Rev": format_currency(projection["total_revenue"]),
            "Dept Exp": format_currency(projection["departmental_expenses"]),
            "Total Exp": format_currency(projection["total_expenses"]),
            "NOI": format_currency(projection["noi"]),
            "Cash Flow": format_currency(projection["cash_flow"]),
            "Cumulative CF": format_currency(projection["cumulative_cash_flow"]),
        }
        for projection in projections
    ]

    return [
        {"kind": "table", "title": "Property Overview", "columns": ["Field", "Value"], "rows": property_rows},
        {"kind": "metrics", "title": "Year 1 Performance", "metrics": year_one_metrics},
        {"kind": "metrics", "title": "Investment Returns", "metrics": investment_metrics},
        {"kind": "metrics", "title": "Hold Period Summary", "metrics": hold_metrics},
        {
            "kind": "table",
            "title": "Revenue Mix",
            "columns": ["Stream", "Year 1", "Share"],
            "rows": revenue_mix_rows,
        },
        {
            "kind": "table",
            "title": "Hotel Pro Forma",
            "columns": [
                "Year",
                "Occ %",
                "ADR",
                "RevPAR",
                "Rooms Rev",
                "F&B Rev",
                "Other Rev",
                "Total Rev",
                "Dept Exp",
                "Total Exp",
                "NOI",
                "Cash Flow",
                "Cumulative CF",
            ],
            "rows": pro_forma_rows,
        },
    ]


def build_chart_specs(inputs: Dict[str, Any], summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return chart definitions for the hotel model."""

    projections = summary["projections"]
    years = [projection["year"] for projection in projections]
    revenue_mix = projections[0]

    # Calculate RevPAR and GOP margin trends
    revpar_values = [projection["revpar"] for projection in projections]
    gop_margin_values = [projection["gop_margin"] * 100 for projection in projections]
    noi_margin_values = [projection["noi_margin"] * 100 for projection in projections]

    return [
        {
            "key": "revenue_expenses",
            "type": "line",
            "title": "Revenue vs Total Expenses vs NOI",
            "filename": "revenue_expense_trends.png",
            "labels": years,
            "datasets": [
                {
                    "label": "Total Revenue ($)",
                    "data": [projection["total_revenue"] for projection in projections],
                    "borderColor": "#4ECDC4",
                    "backgroundColor": "rgba(78, 205, 196, 0.1)",
                    "fill": True,
                },
                {
                    "label": "Total Expenses ($)",
                    "data": [projection["total_expenses"] for projection in projections],
                    "borderColor": "#FF6B6B",
                    "backgroundColor": "rgba(255, 107, 107, 0.1)",
                    "fill": True,
                },
                {
                    "label": "NOI ($)",
                    "data": [projection["noi"] for projection in projections],
                    "borderColor": "#95E1D3",
                    "backgroundColor": "rgba(149, 225, 211, 0.1)",
                    "fill": True,
                },
            ],
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "cash_flow",
            "type": "line",
            "title": "Cash Flow and Cumulative Cash Flow",
            "filename": "cash_flow_trends.png",
            "labels": years,
            "datasets": [
                {
                    "label": "Annual Cash Flow ($)",
                    "data": [projection["cash_flow"] for projection in projections],
                    "borderColor": "#36A2EB",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "fill": True,
                },
                {
                    "label": "Cumulative Cash Flow ($)",
                    "data": summary["cumulative_cash_flows"],
                    "borderColor": "#4BC0C0",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "fill": True,
                },
            ],
            "x_label": "Year",
            "y_label": "Amount ($)",
        },
        {
            "key": "occupancy_adr",
            "type": "line",
            "title": "Occupancy and ADR Trends",
            "filename": "occupancy_adr.png",
            "labels": years,
            "datasets": [
                {
                    "label": "Occupancy (%)",
                    "data": [projection["occupancy"] * 100 for projection in projections],
                    "borderColor": "#4ECDC4",
                    "backgroundColor": "rgba(78, 205, 196, 0.2)",
                    "fill": True,
                    "yAxisID": "y",
                },
                {
                    "label": "ADR ($)",
                    "data": [projection["adr"] for projection in projections],
                    "borderColor": "#FF6B6B",
                    "backgroundColor": "rgba(255, 107, 107, 0.2)",
                    "fill": True,
                    "yAxisID": "y1",
                },
            ],
            "x_label": "Year",
            "y_label": "Value",
        },
        {
            "key": "revenue_mix",
            "type": "bar",
            "title": "Year 1 Revenue Mix",
            "filename": "revenue_mix_year1.png",
            "labels": ["Rooms", "Food & Beverage", "Other"],
            "datasets": [
                {
                    "label": "Revenue ($)",
                    "data": [
                        revenue_mix["rooms_revenue"],
                        revenue_mix["fnb_revenue"],
                        revenue_mix["other_revenue"],
                    ],
                    "backgroundColor": ["#4ECDC4", "#FF6B6B", "#FFD93D"],
                }
            ],
            "x_label": "Revenue Stream",
            "y_label": "Amount ($)",
        },
        {
            "key": "revpar_trend",
            "type": "line",
            "title": "RevPAR Growth Over Time",
            "filename": "revpar_trend.png",
            "labels": years,
            "datasets": [
                {
                    "label": "RevPAR ($)",
                    "data": revpar_values,
                    "borderColor": "#36A2EB",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "fill": True,
                }
            ],
            "x_label": "Year",
            "y_label": "RevPAR ($)",
        },
        {
            "key": "margin_analysis",
            "type": "line",
            "title": "Profitability Margins",
            "filename": "margin_analysis.png",
            "labels": years,
            "datasets": [
                {
                    "label": "GOP Margin (%)",
                    "data": gop_margin_values,
                    "borderColor": "#4ECDC4",
                    "backgroundColor": "rgba(78, 205, 196, 0.2)",
                    "fill": True,
                },
                {
                    "label": "NOI Margin (%)",
                    "data": noi_margin_values,
                    "borderColor": "#95E1D3",
                    "backgroundColor": "rgba(149, 225, 211, 0.2)",
                    "fill": True,
                },
            ],
            "x_label": "Year",
            "y_label": "Margin (%)",
        },
        {
            "key": "revenue_streams",
            "type": "line",
            "title": "Revenue Streams Over Time",
            "filename": "revenue_streams.png",
            "labels": years,
            "datasets": [
                {
                    "label": "Rooms Revenue ($)",
                    "data": [projection["rooms_revenue"] for projection in projections],
                    "borderColor": "#4ECDC4",
                    "backgroundColor": "rgba(78, 205, 196, 0.1)",
                    "fill": True,
                },
                {
                    "label": "F&B Revenue ($)",
                    "data": [projection["fnb_revenue"] for projection in projections],
                    "borderColor": "#FF6B6B",
                    "backgroundColor": "rgba(255, 107, 107, 0.1)",
                    "fill": True,
                },
                {
                    "label": "Other Revenue ($)",
                    "data": [projection["other_revenue"] for projection in projections],
                    "borderColor": "#FFD93D",
                    "backgroundColor": "rgba(255, 217, 61, 0.1)",
                    "fill": True,
                },
            ],
            "x_label": "Year",
            "y_label": "Revenue ($)",
        },
        {
            "key": "gop_trend",
            "type": "bar",
            "title": "Gross Operating Profit by Year",
            "filename": "gop_trend.png",
            "labels": years,
            "datasets": [
                {
                    "label": "GOP ($)",
                    "data": [projection["gop"] for projection in projections],
                    "backgroundColor": "#4ECDC4",
                }
            ],
            "x_label": "Year",
            "y_label": "GOP ($)",
        },
    ]


def display_results(inputs: Dict[str, Any], summary: Dict[str, Any]) -> None:
    """Render summary tables in the console."""

    for table in build_report_tables(inputs, summary):
        if table["kind"] == "metrics":
            render_metrics_table(table["title"], table["metrics"])
        else:
            render_projection_table(table["title"], table["columns"], table["rows"])


def generate_visualizations(inputs: Dict[str, Any], summary: Dict[str, Any]) -> Dict[str, str]:
    """Save charts for the hotel analysis."""

    report_dir = ensure_report_dir("hotel", inputs["project_name"])
    chart_paths: Dict[str, str] = {}

    for spec in build_chart_specs(inputs, summary):
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
    """Collect inputs for the hotel model."""

    defaults = DEFAULT_INPUTS

    project_name = prompt_text("Project name", default=defaults["project_name"])
    hotel_type = prompt_choice(
        "Hotel segment",
        ["Luxury", "Upper Upscale", "Upscale", "Midscale", "Economy"],
        default=defaults["hotel_type"],
    )
    location = prompt_text("Market / Location", default=defaults["location"])
    brand_affiliation = prompt_text("Brand affiliation", default=defaults["brand_affiliation"])
    analyst = prompt_text("Analyst name", allow_blank=True) or None

    rooms = prompt_int("Number of rooms", minimum=10, default=defaults["rooms"])
    adr = prompt_float("Year 1 ADR", minimum=40.0, default=defaults["adr"])
    year1_occupancy = prompt_percentage("Year 1 occupancy", default=defaults["year1_occupancy"])
    stabilized_occupancy = prompt_percentage("Stabilized occupancy", default=defaults["stabilized_occupancy"])
    adr_growth_rate = prompt_percentage("Annual ADR growth", default=defaults["adr_growth_rate"], maximum=0.08)
    fnb_growth_rate = prompt_percentage("Annual F&B growth", default=defaults["fnb_growth_rate"], maximum=0.1)
    other_income_growth_rate = prompt_percentage(
        "Other income growth",
        default=defaults["other_income_growth_rate"],
        maximum=0.08,
    )

    fnb_outlet_per_room_day = prompt_float(
        "Restaurant revenue per room per day", default=defaults["fnb_outlet_per_room_day"], minimum=0.0
    )
    banquet_rev_per_group_room = prompt_float(
        "Banquet revenue per group room night", default=defaults["banquet_rev_per_group_room"], minimum=0.0
    )
    group_room_pct = prompt_percentage("Group room mix", default=defaults["group_room_pct"])

    meeting_rev_per_room = prompt_float("Meeting revenue per room per year", default=defaults["meeting_rev_per_room"])
    parking_rev_per_room = prompt_float("Parking revenue per room per year", default=defaults["parking_rev_per_room"])
    spa_rev_per_room = prompt_float("Spa/Fitness revenue per room per year", default=defaults["spa_rev_per_room"])
    other_operated_rev_per_room = prompt_float(
        "Other operated revenue per room per year", default=defaults["other_operated_rev_per_room"]
    )

    rooms_dept_pct = prompt_percentage("Rooms department expense (% of revenue)", default=defaults["rooms_dept_pct"])
    fnb_dept_pct = prompt_percentage("F&B department expense (% of revenue)", default=defaults["fnb_dept_pct"])
    other_dept_pct = prompt_percentage(
        "Other department expense (% of revenue)", default=defaults["other_dept_pct"]
    )

    admin_per_room = prompt_float("Admin & general per room per year", default=defaults["admin_per_room"])
    maintenance_per_room = prompt_float("Property operations & maintenance per room", default=defaults["maintenance_per_room"])
    utilities_per_room = prompt_float("Utilities per room", default=defaults["utilities_per_room"])
    insurance_pct = prompt_percentage("Insurance (% of revenue)", default=defaults["insurance_pct"], maximum=0.05)
    property_tax_pct = prompt_percentage(
        "Property tax (% of revenue)", default=defaults["property_tax_pct"], maximum=0.07
    )
    expense_growth_rate = prompt_percentage("Annual expense growth", default=defaults["expense_growth_rate"])

    total_project_cost = prompt_float("Total project cost", minimum=1_000_000.0, default=defaults["total_project_cost"])
    loan_to_cost = prompt_percentage("Loan-to-cost", default=defaults["loan_to_cost"], maximum=0.85)
    interest_rate = prompt_percentage("Interest rate", default=defaults["interest_rate"], maximum=0.12)
    amort_years = prompt_int("Amortization period (years)", default=defaults["amort_years"], minimum=5, maximum=35)
    hold_period_years = prompt_int("Hold period (years)", default=defaults["hold_period_years"], minimum=3, maximum=15)
    exit_cap_rate = prompt_percentage("Exit cap rate", default=defaults["exit_cap_rate"], maximum=0.12)

    loan_amount = total_project_cost * loan_to_cost
    equity = total_project_cost - loan_amount
    annual_debt_service = annuity_payment(loan_amount, interest_rate, amort_years) * 12

    return prepare_inputs(
        {
            "project_name": project_name,
            "hotel_type": hotel_type,
            "location": location,
            "brand_affiliation": brand_affiliation,
            "analyst": analyst,
            "rooms": rooms,
            "adr": adr,
            "year1_occupancy": year1_occupancy,
            "stabilized_occupancy": stabilized_occupancy,
            "adr_growth_rate": adr_growth_rate,
            "fnb_growth_rate": fnb_growth_rate,
            "other_income_growth_rate": other_income_growth_rate,
            "fnb_outlet_per_room_day": fnb_outlet_per_room_day,
            "banquet_rev_per_group_room": banquet_rev_per_group_room,
            "group_room_pct": group_room_pct,
            "meeting_rev_per_room": meeting_rev_per_room,
            "parking_rev_per_room": parking_rev_per_room,
            "spa_rev_per_room": spa_rev_per_room,
            "other_operated_rev_per_room": other_operated_rev_per_room,
            "rooms_dept_pct": rooms_dept_pct,
            "fnb_dept_pct": fnb_dept_pct,
            "other_dept_pct": other_dept_pct,
            "admin_per_room": admin_per_room,
            "maintenance_per_room": maintenance_per_room,
            "utilities_per_room": utilities_per_room,
            "insurance_pct": insurance_pct,
            "property_tax_pct": property_tax_pct,
            "expense_growth_rate": expense_growth_rate,
            "total_project_cost": total_project_cost,
            "loan_to_cost": loan_to_cost,
            "interest_rate": interest_rate,
            "amort_years": amort_years,
            "hold_period_years": hold_period_years,
            "exit_cap_rate": exit_cap_rate,
        }
    )


def main() -> None:
    """Collect inputs, run the model, and persist the results."""

    ensure_database()
    console.print(Panel("Hotel Financial Model Builder", style="bold white on blue"))

    inputs = gather_inputs()
    summary = build_projection(inputs)
    display_results(inputs, summary)
    chart_paths = generate_visualizations(inputs, summary)

    with session_scope() as session:
        record = HotelFinancialModel(
            name=inputs["project_name"],
            hotel_type=inputs["hotel_type"],
            location=inputs["location"],
            analyst=inputs.get("analyst"),
            inputs=inputs,
            results={
                "projections": summary["projections"],
                "cash_flows": summary["cash_flows"],
                "equity_multiple": summary["equity_multiple"],
                "irr": summary["irr"],
                "dscr": summary["dscr"],
                "exit_value": summary["exit_value"],
                "net_sale_proceeds": summary["net_sale_proceeds"],
                "loan_balance_exit": summary["loan_balance_exit"],
                "charts": chart_paths,
            },
        )
        session.add(record)
        session.flush()
        console.print(
            Panel(
                f"Hotel model saved with ID [bold]{record.id}[/bold]",
                style="green",
            )
        )


if __name__ == "__main__":
    main()
