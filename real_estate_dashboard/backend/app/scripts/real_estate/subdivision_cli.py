"""Interactive CLI and shared utilities for multi-unit subdivision analysis."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import (
    format_currency,
    format_percentage,
)


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Sample Subdivision Deal",
    "location": "Miami Beach, FL",
    "analyst": "",
    "property_type": "Duplex",
    "num_units": 2,
    "total_sqft": 1778,
    "sqft_per_unit": 889,
    "bedrooms_per_unit": 2,
    "bathrooms_per_unit": 1.0,
    "year_built": 1967,

    # Acquisition
    "purchase_price": 735000.0,
    "down_payment_pct": 0.03,
    "closing_costs": 20000.0,
    "interest_rate": 0.08,
    "loan_points": 0.02,

    # Current Income
    "current_monthly_rent": 4475.0,
    "market_monthly_rent": 5000.0,

    # Renovation Costs (per unit)
    "kitchen_cost_per_unit": 8000.0,
    "bathroom_cost_per_unit": 5000.0,
    "flooring_cost_per_unit": 4000.0,
    "paint_interior_per_unit": 2500.0,
    "paint_exterior_total": 3000.0,
    "appliances_per_unit": 3000.0,
    "plumbing_per_unit": 1500.0,
    "electrical_per_unit": 2000.0,
    "other_per_unit": 1000.0,
    "renovation_contingency_pct": 0.10,

    # Conversion/Subdivision Costs
    "survey_cost": 5000.0,
    "legal_fees": 12000.0,
    "hoa_formation": 4000.0,
    "title_work_per_unit": 1500.0,
    "permits_fees": 3500.0,
    "utility_separation": 0.0,
    "conversion_contingency_pct": 0.10,

    # Exit Strategy: Subdivide & Sell
    "individual_unit_sale_price": 450000.0,
    "commission_pct": 0.06,
    "selling_closing_pct": 0.015,

    # Exit Strategy: Sell As-Is
    "duplex_sale_price": 850000.0,

    # Exit Strategy: BRRRR
    "stabilized_value": 850000.0,
    "refinance_ltv": 0.75,
    "annual_noi": 55440.0,

    # Timeline (months)
    "acquisition_months": 2,
    "renovation_months": 3,
    "conversion_months": 6,
    "marketing_months": 3,

    # Operating Expenses (monthly)
    "property_tax_monthly": 800.0,
    "insurance_monthly": 300.0,
    "utilities_monthly": 200.0,
    "maintenance_monthly": 400.0,
    "hoa_fees_monthly": 0.0,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    # Property Profile
    {"name": "project_name", "label": "Project Name", "type": "text", "section": "Property Profile"},
    {"name": "location", "label": "Location", "type": "text", "section": "Property Profile"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Profile"},
    {
        "name": "property_type",
        "label": "Property Type",
        "type": "text",
        "options": ["Duplex", "Triplex", "Quadplex", "5-6 Units", "7-10 Units"],
        "section": "Property Profile",
    },
    {"name": "num_units", "label": "Number of Units", "type": "number", "step": 1, "min": 2, "max": 10, "section": "Property Profile"},
    {"name": "total_sqft", "label": "Total Square Footage", "type": "number", "step": 50, "min": 800, "section": "Property Profile"},
    {"name": "sqft_per_unit", "label": "SF per Unit (avg)", "type": "number", "step": 50, "min": 400, "section": "Property Profile"},
    {"name": "bedrooms_per_unit", "label": "Bedrooms per Unit (avg)", "type": "number", "step": 1, "min": 1, "section": "Property Profile"},
    {"name": "bathrooms_per_unit", "label": "Bathrooms per Unit (avg)", "type": "number", "step": 0.5, "min": 1, "section": "Property Profile"},
    {"name": "year_built", "label": "Year Built", "type": "number", "step": 1, "min": 1900, "section": "Property Profile"},

    # Acquisition & Financing
    {"name": "purchase_price", "label": "Purchase Price ($)", "type": "number", "step": 5000, "min": 100000, "section": "Acquisition & Financing"},
    {"name": "down_payment_pct", "label": "Down Payment (%)", "type": "number", "step": 1, "min": 3, "max": 25, "format": "percentage", "section": "Acquisition & Financing"},
    {"name": "closing_costs", "label": "Closing Costs ($)", "type": "number", "step": 1000, "min": 0, "section": "Acquisition & Financing"},
    {"name": "interest_rate", "label": "Interest Rate (%)", "type": "number", "step": 0.25, "min": 3, "max": 15, "format": "percentage", "section": "Acquisition & Financing"},
    {"name": "loan_points", "label": "Loan Points (%)", "type": "number", "step": 0.25, "min": 0, "max": 5, "format": "percentage", "section": "Acquisition & Financing"},

    # Current Income
    {"name": "current_monthly_rent", "label": "Current Monthly Rent ($)", "type": "number", "step": 100, "min": 0, "section": "Current Income"},
    {"name": "market_monthly_rent", "label": "Market Monthly Rent ($)", "type": "number", "step": 100, "min": 0, "section": "Current Income"},

    # Renovation Costs
    {"name": "kitchen_cost_per_unit", "label": "Kitchen (per unit) ($)", "type": "number", "step": 500, "min": 0, "section": "Renovation Costs"},
    {"name": "bathroom_cost_per_unit", "label": "Bathroom (per unit) ($)", "type": "number", "step": 500, "min": 0, "section": "Renovation Costs"},
    {"name": "flooring_cost_per_unit", "label": "Flooring (per unit) ($)", "type": "number", "step": 500, "min": 0, "section": "Renovation Costs"},
    {"name": "paint_interior_per_unit", "label": "Interior Paint (per unit) ($)", "type": "number", "step": 250, "min": 0, "section": "Renovation Costs"},
    {"name": "paint_exterior_total", "label": "Exterior Paint (total) ($)", "type": "number", "step": 500, "min": 0, "section": "Renovation Costs"},
    {"name": "appliances_per_unit", "label": "Appliances (per unit) ($)", "type": "number", "step": 500, "min": 0, "section": "Renovation Costs"},
    {"name": "plumbing_per_unit", "label": "Plumbing (per unit) ($)", "type": "number", "step": 250, "min": 0, "section": "Renovation Costs"},
    {"name": "electrical_per_unit", "label": "Electrical (per unit) ($)", "type": "number", "step": 250, "min": 0, "section": "Renovation Costs"},
    {"name": "other_per_unit", "label": "Other (per unit) ($)", "type": "number", "step": 250, "min": 0, "section": "Renovation Costs"},
    {"name": "renovation_contingency_pct", "label": "Renovation Contingency (%)", "type": "number", "step": 1, "min": 0, "max": 25, "format": "percentage", "section": "Renovation Costs"},

    # Conversion/Subdivision Costs
    {"name": "survey_cost", "label": "Survey & Engineering ($)", "type": "number", "step": 500, "min": 0, "section": "Conversion Costs"},
    {"name": "legal_fees", "label": "Legal Fees ($)", "type": "number", "step": 1000, "min": 0, "section": "Conversion Costs"},
    {"name": "hoa_formation", "label": "HOA Formation ($)", "type": "number", "step": 500, "min": 0, "section": "Conversion Costs"},
    {"name": "title_work_per_unit", "label": "Title Work (per unit) ($)", "type": "number", "step": 250, "min": 0, "section": "Conversion Costs"},
    {"name": "permits_fees", "label": "Permits & Fees ($)", "type": "number", "step": 500, "min": 0, "section": "Conversion Costs"},
    {"name": "utility_separation", "label": "Utility Separation ($)", "type": "number", "step": 500, "min": 0, "section": "Conversion Costs"},
    {"name": "conversion_contingency_pct", "label": "Conversion Contingency (%)", "type": "number", "step": 1, "min": 0, "max": 25, "format": "percentage", "section": "Conversion Costs"},

    # Exit Strategy: Subdivide
    {"name": "individual_unit_sale_price", "label": "Individual Unit Sale Price ($)", "type": "number", "step": 5000, "min": 100000, "section": "Exit: Subdivide & Sell"},
    {"name": "commission_pct", "label": "Sales Commission (%)", "type": "number", "step": 0.5, "min": 0, "max": 10, "format": "percentage", "section": "Exit: Subdivide & Sell"},
    {"name": "selling_closing_pct", "label": "Selling Closing Costs (%)", "type": "number", "step": 0.25, "min": 0, "max": 5, "format": "percentage", "section": "Exit: Subdivide & Sell"},

    # Exit Strategy: Sell As-Is
    {"name": "duplex_sale_price", "label": "As-Is Sale Price ($)", "type": "number", "step": 5000, "min": 100000, "section": "Exit: Sell As-Is"},

    # Exit Strategy: BRRRR
    {"name": "stabilized_value", "label": "Stabilized Value ($)", "type": "number", "step": 5000, "min": 100000, "section": "Exit: BRRRR"},
    {"name": "refinance_ltv", "label": "Refinance LTV (%)", "type": "number", "step": 1, "min": 50, "max": 80, "format": "percentage", "section": "Exit: BRRRR"},
    {"name": "annual_noi", "label": "Annual NOI ($)", "type": "number", "step": 1000, "min": 0, "section": "Exit: BRRRR"},

    # Timeline
    {"name": "acquisition_months", "label": "Acquisition (months)", "type": "number", "step": 1, "min": 1, "max": 6, "section": "Timeline"},
    {"name": "renovation_months", "label": "Renovation (months)", "type": "number", "step": 1, "min": 1, "max": 12, "section": "Timeline"},
    {"name": "conversion_months", "label": "Conversion Approval (months)", "type": "number", "step": 1, "min": 3, "max": 18, "section": "Timeline"},
    {"name": "marketing_months", "label": "Marketing & Sale (months)", "type": "number", "step": 1, "min": 1, "max": 12, "section": "Timeline"},

    # Operating Expenses
    {"name": "property_tax_monthly", "label": "Property Tax (monthly) ($)", "type": "number", "step": 50, "min": 0, "section": "Operating Expenses"},
    {"name": "insurance_monthly", "label": "Insurance (monthly) ($)", "type": "number", "step": 25, "min": 0, "section": "Operating Expenses"},
    {"name": "utilities_monthly", "label": "Utilities (monthly) ($)", "type": "number", "step": 25, "min": 0, "section": "Operating Expenses"},
    {"name": "maintenance_monthly", "label": "Maintenance (monthly) ($)", "type": "number", "step": 50, "min": 0, "section": "Operating Expenses"},
    {"name": "hoa_fees_monthly", "label": "HOA Fees (monthly) ($)", "type": "number", "step": 25, "min": 0, "section": "Operating Expenses"},
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Combine overrides with defaults for downstream processing."""
    merged = DEFAULT_INPUTS.copy()
    merged.update(overrides)
    return merged


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate all exit strategies and financial metrics for subdivision analysis."""

    num_units = inputs["num_units"]
    purchase_price = inputs["purchase_price"]
    down_payment_pct = inputs["down_payment_pct"]
    closing_costs = inputs["closing_costs"]
    interest_rate = inputs["interest_rate"]
    loan_points = inputs["loan_points"]

    # Calculate financing
    down_payment = purchase_price * down_payment_pct
    loan_amount = purchase_price - down_payment
    points_cost = loan_amount * loan_points

    # Calculate renovation costs
    per_unit_costs = (
        inputs["kitchen_cost_per_unit"] +
        inputs["bathroom_cost_per_unit"] +
        inputs["flooring_cost_per_unit"] +
        inputs["paint_interior_per_unit"] +
        inputs["appliances_per_unit"] +
        inputs["plumbing_per_unit"] +
        inputs["electrical_per_unit"] +
        inputs["other_per_unit"]
    )
    total_unit_costs = per_unit_costs * num_units
    exterior_costs = inputs["paint_exterior_total"]
    renovation_subtotal = total_unit_costs + exterior_costs
    renovation_contingency = renovation_subtotal * inputs["renovation_contingency_pct"]
    total_renovation = renovation_subtotal + renovation_contingency

    # Calculate conversion costs
    conversion_subtotal = (
        inputs["survey_cost"] +
        inputs["legal_fees"] +
        inputs["hoa_formation"] +
        (inputs["title_work_per_unit"] * num_units) +
        inputs["permits_fees"] +
        inputs["utility_separation"]
    )
    conversion_contingency = conversion_subtotal * inputs["conversion_contingency_pct"]
    total_conversion = conversion_subtotal + conversion_contingency

    # Calculate timeline and holding costs
    total_months = (
        inputs["acquisition_months"] +
        inputs["renovation_months"] +
        inputs["conversion_months"] +
        inputs["marketing_months"]
    )
    monthly_operating = (
        inputs["property_tax_monthly"] +
        inputs["insurance_monthly"] +
        inputs["utilities_monthly"] +
        inputs["maintenance_monthly"] +
        inputs["hoa_fees_monthly"]
    )
    monthly_debt_service = (loan_amount * interest_rate / 12) if loan_amount > 0 else 0
    total_monthly_costs = monthly_operating + monthly_debt_service
    total_holding_costs = total_monthly_costs * total_months

    # Calculate cash invested
    cash_at_closing = down_payment + closing_costs + points_cost
    total_cash_invested = cash_at_closing + total_renovation + total_conversion + total_holding_costs

    # STRATEGY 1: Subdivide & Sell Individual Units
    individual_sale_price = inputs["individual_unit_sale_price"]
    total_gross_proceeds = individual_sale_price * num_units
    commission = total_gross_proceeds * inputs["commission_pct"]
    selling_closing = total_gross_proceeds * inputs["selling_closing_pct"]
    net_proceeds_subdivide = total_gross_proceeds - commission - selling_closing

    total_cost_subdivide = (
        loan_amount +
        total_renovation +
        total_conversion +
        total_holding_costs +
        commission +
        selling_closing
    )

    profit_subdivide = net_proceeds_subdivide - total_cost_subdivide
    roi_subdivide = (profit_subdivide / total_cash_invested) if total_cash_invested > 0 else 0

    # STRATEGY 2: Sell As-Is (Multi-Unit)
    duplex_price = inputs["duplex_sale_price"]
    commission_duplex = duplex_price * inputs["commission_pct"]
    closing_duplex = duplex_price * inputs["selling_closing_pct"]
    net_proceeds_duplex = duplex_price - commission_duplex - closing_duplex

    # For as-is, we still do light renovation but no conversion
    cash_invested_duplex = cash_at_closing + (total_renovation * 0.3) + (total_holding_costs * 0.5)  # Lighter touch
    total_cost_duplex = loan_amount + (total_renovation * 0.3) + commission_duplex + closing_duplex + (total_holding_costs * 0.5)

    profit_duplex = net_proceeds_duplex - total_cost_duplex
    roi_duplex = (profit_duplex / cash_invested_duplex) if cash_invested_duplex > 0 else 0

    # STRATEGY 3: BRRRR (Buy, Renovate, Rent, Refinance, Repeat)
    stabilized_value = inputs["stabilized_value"]
    refinance_amount = stabilized_value * inputs["refinance_ltv"]
    cash_out = refinance_amount - loan_amount

    annual_noi = inputs["annual_noi"]
    monthly_cashflow = (annual_noi / 12) - monthly_debt_service if annual_noi > 0 else 0

    cash_invested_brrrr = cash_at_closing + total_renovation + total_holding_costs
    roi_brrrr = (monthly_cashflow * 12 / cash_invested_brrrr) if cash_invested_brrrr > 0 else 0

    # Build projections array (monthly cash flow for first 18 months)
    projections = []
    for month in range(1, 19):
        if month <= inputs["acquisition_months"]:
            phase = "Acquisition"
            cash_flow = -monthly_operating
        elif month <= inputs["acquisition_months"] + inputs["renovation_months"]:
            phase = "Renovation"
            cash_flow = -monthly_operating - (total_renovation / inputs["renovation_months"])
        elif month <= inputs["acquisition_months"] + inputs["renovation_months"] + inputs["conversion_months"]:
            phase = "Conversion"
            cash_flow = inputs["current_monthly_rent"] - monthly_operating - monthly_debt_service
        else:
            phase = "Marketing"
            cash_flow = inputs["current_monthly_rent"] - monthly_operating - monthly_debt_service

        projections.append({
            "month": month,
            "phase": phase,
            "cash_flow": cash_flow,
            "cumulative_cash_flow": sum(p["cash_flow"] for p in projections) + cash_flow if projections else cash_flow,
        })

    # Compile metrics
    metrics = {
        "total_cash_invested": total_cash_invested,
        "cash_at_closing": cash_at_closing,
        "total_renovation": total_renovation,
        "total_conversion": total_conversion,
        "total_holding_costs": total_holding_costs,
        "total_months": total_months,

        # Strategy 1: Subdivide
        "subdivide_gross_proceeds": total_gross_proceeds,
        "subdivide_net_proceeds": net_proceeds_subdivide,
        "subdivide_profit": profit_subdivide,
        "subdivide_roi": roi_subdivide,

        # Strategy 2: Sell As-Is
        "duplex_gross_proceeds": duplex_price,
        "duplex_net_proceeds": net_proceeds_duplex,
        "duplex_profit": profit_duplex,
        "duplex_roi": roi_duplex,

        # Strategy 3: BRRRR
        "brrrr_refinance_amount": refinance_amount,
        "brrrr_cash_out": cash_out,
        "brrrr_annual_cashflow": monthly_cashflow * 12,
        "brrrr_monthly_cashflow": monthly_cashflow,
        "brrrr_roi": roi_brrrr,

        # Conversion Premium
        "conversion_premium_dollars": total_gross_proceeds - duplex_price,
        "conversion_premium_pct": ((total_gross_proceeds - duplex_price) / duplex_price) if duplex_price > 0 else 0,
    }

    return {
        "projections": projections,
        "metrics": metrics,
    }


def build_report_tables(
    inputs: Dict[str, Any],
    projections: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Return table definitions for web UI rendering."""

    tables = []

    # Property Overview Table
    tables.append({
        "title": "Property Overview",
        "headers": ["Field", "Value"],
        "rows": [
            {"Field": "Project", "Value": inputs["project_name"]},
            {"Field": "Location", "Value": inputs["location"]},
            {"Field": "Property Type", "Value": inputs["property_type"]},
            {"Field": "Units", "Value": str(inputs["num_units"])},
            {"Field": "Total SF", "Value": f"{inputs['total_sqft']:,} sf"},
            {"Field": "SF per Unit", "Value": f"{inputs['sqft_per_unit']:,} sf"},
            {"Field": "Beds/Baths", "Value": f"{inputs['bedrooms_per_unit']}/{inputs['bathrooms_per_unit']}"},
            {"Field": "Year Built", "Value": str(inputs["year_built"])},
        ],
    })

    # Acquisition Summary
    down_payment = inputs["purchase_price"] * inputs["down_payment_pct"]
    loan_amount = inputs["purchase_price"] - down_payment

    tables.append({
        "title": "Acquisition Summary",
        "headers": ["Item", "Amount"],
        "rows": [
            {"Item": "Purchase Price", "Amount": format_currency(inputs["purchase_price"])},
            {"Item": f"Down Payment ({format_percentage(inputs['down_payment_pct'])})", "Amount": format_currency(down_payment)},
            {"Item": "Loan Amount", "Amount": format_currency(loan_amount)},
            {"Item": "Closing Costs", "Amount": format_currency(inputs["closing_costs"])},
            {"Item": "Cash at Closing", "Amount": format_currency(metrics["cash_at_closing"])},
        ],
    })

    # Renovation Breakdown
    tables.append({
        "title": "Renovation Budget",
        "headers": ["Category", "Cost"],
        "rows": [
            {"Category": f"Kitchen ({inputs['num_units']} units)", "Cost": format_currency(inputs["kitchen_cost_per_unit"] * inputs["num_units"])},
            {"Category": f"Bathroom ({inputs['num_units']} units)", "Cost": format_currency(inputs["bathroom_cost_per_unit"] * inputs["num_units"])},
            {"Category": f"Flooring ({inputs['num_units']} units)", "Cost": format_currency(inputs["flooring_cost_per_unit"] * inputs["num_units"])},
            {"Category": f"Interior Paint ({inputs['num_units']} units)", "Cost": format_currency(inputs["paint_interior_per_unit"] * inputs["num_units"])},
            {"Category": "Exterior Paint", "Cost": format_currency(inputs["paint_exterior_total"])},
            {"Category": f"Appliances ({inputs['num_units']} units)", "Cost": format_currency(inputs["appliances_per_unit"] * inputs["num_units"])},
            {"Category": f"Plumbing ({inputs['num_units']} units)", "Cost": format_currency(inputs["plumbing_per_unit"] * inputs["num_units"])},
            {"Category": f"Electrical ({inputs['num_units']} units)", "Cost": format_currency(inputs["electrical_per_unit"] * inputs["num_units"])},
            {"Category": f"Other ({inputs['num_units']} units)", "Cost": format_currency(inputs["other_per_unit"] * inputs["num_units"])},
            {"Category": f"Contingency ({format_percentage(inputs['renovation_contingency_pct'])})", "Cost": format_currency(metrics["total_renovation"] - (metrics["total_renovation"] / (1 + inputs["renovation_contingency_pct"])))},
            {"Category": "**Total Renovation**", "Cost": format_currency(metrics["total_renovation"])},
        ],
    })

    # Conversion Costs
    tables.append({
        "title": "Conversion/Subdivision Costs",
        "headers": ["Item", "Cost"],
        "rows": [
            {"Item": "Survey & Engineering", "Cost": format_currency(inputs["survey_cost"])},
            {"Item": "Legal Fees (Condo Docs)", "Cost": format_currency(inputs["legal_fees"])},
            {"Item": "HOA Formation", "Cost": format_currency(inputs["hoa_formation"])},
            {"Item": f"Title Work ({inputs['num_units']} units)", "Cost": format_currency(inputs["title_work_per_unit"] * inputs["num_units"])},
            {"Item": "Permits & Fees", "Cost": format_currency(inputs["permits_fees"])},
            {"Item": "Utility Separation", "Cost": format_currency(inputs["utility_separation"])},
            {"Item": f"Contingency ({format_percentage(inputs['conversion_contingency_pct'])})", "Cost": format_currency(metrics["total_conversion"] - (metrics["total_conversion"] / (1 + inputs["conversion_contingency_pct"])))},
            {"Item": "**Total Conversion**", "Cost": format_currency(metrics["total_conversion"])},
        ],
    })

    # Exit Strategy Comparison
    tables.append({
        "title": "Exit Strategy Comparison",
        "headers": ["Strategy", "Gross Proceeds", "Net Proceeds", "Profit", "ROI"],
        "rows": [
            {
                "Strategy": "Subdivide & Sell",
                "Gross Proceeds": format_currency(metrics["subdivide_gross_proceeds"]),
                "Net Proceeds": format_currency(metrics["subdivide_net_proceeds"]),
                "Profit": format_currency(metrics["subdivide_profit"]),
                "ROI": format_percentage(metrics["subdivide_roi"]),
            },
            {
                "Strategy": "Sell As-Is (Multi-Unit)",
                "Gross Proceeds": format_currency(metrics["duplex_gross_proceeds"]),
                "Net Proceeds": format_currency(metrics["duplex_net_proceeds"]),
                "Profit": format_currency(metrics["duplex_profit"]),
                "ROI": format_percentage(metrics["duplex_roi"]),
            },
            {
                "Strategy": "BRRRR (Hold & Refinance)",
                "Gross Proceeds": format_currency(metrics["brrrr_refinance_amount"]),
                "Net Proceeds": format_currency(metrics["brrrr_cash_out"]),
                "Profit": format_currency(metrics["brrrr_annual_cashflow"]) + " /year",
                "ROI": format_percentage(metrics["brrrr_roi"]) + " annual",
            },
        ],
    })

    # Key Metrics
    tables.append({
        "title": "Key Investment Metrics",
        "headers": ["Metric", "Value"],
        "rows": [
            {"Metric": "Total Cash Invested", "Value": format_currency(metrics["total_cash_invested"])},
            {"Metric": "Total Project Timeline", "Value": f"{metrics['total_months']} months"},
            {"Metric": "Conversion Premium", "Value": format_currency(metrics["conversion_premium_dollars"]) + f" ({format_percentage(metrics['conversion_premium_pct'])})"},
            {"Metric": "Best Strategy", "Value": "Subdivide & Sell" if metrics["subdivide_roi"] > metrics["duplex_roi"] else "Sell As-Is"},
            {"Metric": "Best ROI", "Value": format_percentage(max(metrics["subdivide_roi"], metrics["duplex_roi"]))},
        ],
    })

    return tables


def build_chart_specs(
    inputs: Dict[str, Any],
    projections: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Return chart specifications for web UI rendering."""

    charts = []

    # ROI Comparison Chart
    charts.append({
        "title": "Exit Strategy ROI Comparison",
        "type": "bar",
        "key": "roi_comparison",
        "labels": ["Subdivide & Sell", "Sell As-Is", "BRRRR (Annual)"],
        "datasets": [
            {
                "label": "Return on Investment",
                "data": [
                    metrics["subdivide_roi"] * 100,
                    metrics["duplex_roi"] * 100,
                    metrics["brrrr_roi"] * 100,
                ],
                "backgroundColor": ["#10b981", "#3b82f6", "#f59e0b"],
            }
        ],
    })

    # Profit Comparison
    charts.append({
        "title": "Profit Comparison by Strategy",
        "type": "bar",
        "key": "profit_comparison",
        "labels": ["Subdivide & Sell", "Sell As-Is"],
        "datasets": [
            {
                "label": "Net Profit ($)",
                "data": [
                    metrics["subdivide_profit"],
                    metrics["duplex_profit"],
                ],
                "backgroundColor": ["#10b981", "#3b82f6"],
            }
        ],
    })

    # Cash Flow Over Time
    charts.append({
        "title": "Monthly Cash Flow Projection",
        "type": "line",
        "key": "cash_flow_timeline",
        "labels": [f"Month {p['month']}" for p in projections],
        "datasets": [
            {
                "label": "Monthly Cash Flow",
                "data": [p["cash_flow"] for p in projections],
                "borderColor": "#3b82f6",
                "fill": False,
            },
            {
                "label": "Cumulative Cash Flow",
                "data": [p["cumulative_cash_flow"] for p in projections],
                "borderColor": "#10b981",
                "fill": True,
            },
        ],
    })

    # Cost Breakdown Pie Chart
    charts.append({
        "title": "Total Investment Breakdown",
        "type": "pie",
        "key": "cost_breakdown",
        "labels": ["Cash at Closing", "Renovation", "Conversion", "Holding Costs"],
        "datasets": [
            {
                "label": "Investment Allocation",
                "data": [
                    metrics["cash_at_closing"],
                    metrics["total_renovation"],
                    metrics["total_conversion"],
                    metrics["total_holding_costs"],
                ],
                "backgroundColor": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
            }
        ],
    })

    return charts
