"""Interactive CLI and shared helpers for the renovation budget model."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from rich.panel import Panel

from app.models.real_estate import RenovationBudgetModel

from .base import (
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
    save_bar_chart,
    save_line_chart,
    session_scope,
)


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Oakwood Apartments Renovation",
    "location": "Phoenix, AZ",
    "analyst": "",
    "tags": "",
    "purpose": "",
    "references": "",
    "notes": "",
    "property_type": "Multifamily",
    "total_units": 24,
    "square_footage_per_unit": 850,
    "total_square_footage": 20400,
    "kitchen_renovation_per_unit": 12000.0,
    "bathroom_renovation_per_unit": 8000.0,
    "flooring_per_unit": 3500.0,
    "paint_per_unit": 1200.0,
    "appliances_per_unit": 2500.0,
    "fixtures_per_unit": 1500.0,
    "hvac_per_unit": 4000.0,
    "electrical_per_unit": 2000.0,
    "plumbing_per_unit": 2500.0,
    "other_per_unit": 1000.0,
    "common_area_renovation": 50000.0,
    "exterior_improvements": 75000.0,
    "landscaping": 20000.0,
    "parking_lot_repaving": 30000.0,
    "roof_replacement": 0.0,
    "structural_repairs": 0.0,
    "contingency_pct": 0.10,
    "soft_costs_pct": 0.08,
    "current_avg_rent": 1200.0,
    "post_reno_avg_rent": 1500.0,
    "current_occupancy": 0.75,
    "stabilized_occupancy": 0.95,
    "months_to_complete": 8,
    "units_renovated_per_month": 3,
    "financing_cost_pct": 0.06,
    "holding_costs_monthly": 5000.0,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text", "section": "Property Profile"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Profile"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Profile"},
    {"name": "property_type", "label": "Property Type", "type": "text", "section": "Property Profile"},
    {
        "name": "total_units",
        "label": "Total Units",
        "type": "number",
        "step": 1,
        "min": 1,
        "section": "Property Profile",
    },
    {
        "name": "square_footage_per_unit",
        "label": "Square Footage Per Unit",
        "type": "number",
        "step": 50,
        "min": 100,
        "section": "Property Profile",
    },
    {
        "name": "total_square_footage",
        "label": "Total Square Footage",
        "type": "number",
        "step": 100,
        "min": 100,
        "section": "Property Profile",
    },
    {
        "name": "kitchen_renovation_per_unit",
        "label": "Kitchen Renovation ($/unit)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "bathroom_renovation_per_unit",
        "label": "Bathroom Renovation ($/unit)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "flooring_per_unit",
        "label": "Flooring ($/unit)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "paint_per_unit",
        "label": "Paint ($/unit)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "appliances_per_unit",
        "label": "Appliances ($/unit)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "fixtures_per_unit",
        "label": "Fixtures & Hardware ($/unit)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Interior Renovation Costs",
    },
    {
        "name": "hvac_per_unit",
        "label": "HVAC ($/unit)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Systems & Mechanical",
    },
    {
        "name": "electrical_per_unit",
        "label": "Electrical ($/unit)",
        "type": "number",
        "step": 200,
        "min": 0,
        "section": "Systems & Mechanical",
    },
    {
        "name": "plumbing_per_unit",
        "label": "Plumbing ($/unit)",
        "type": "number",
        "step": 200,
        "min": 0,
        "section": "Systems & Mechanical",
    },
    {
        "name": "other_per_unit",
        "label": "Other Interior Costs ($/unit)",
        "type": "number",
        "step": 100,
        "min": 0,
        "section": "Systems & Mechanical",
    },
    {
        "name": "common_area_renovation",
        "label": "Common Area Renovation ($)",
        "type": "number",
        "step": 1000,
        "min": 0,
        "section": "Exterior & Common Areas",
    },
    {
        "name": "exterior_improvements",
        "label": "Exterior Improvements ($)",
        "type": "number",
        "step": 1000,
        "min": 0,
        "section": "Exterior & Common Areas",
    },
    {
        "name": "landscaping",
        "label": "Landscaping ($)",
        "type": "number",
        "step": 1000,
        "min": 0,
        "section": "Exterior & Common Areas",
    },
    {
        "name": "parking_lot_repaving",
        "label": "Parking Lot ($)",
        "type": "number",
        "step": 1000,
        "min": 0,
        "section": "Exterior & Common Areas",
    },
    {
        "name": "roof_replacement",
        "label": "Roof Replacement ($)",
        "type": "number",
        "step": 5000,
        "min": 0,
        "section": "Major Capital Items",
    },
    {
        "name": "structural_repairs",
        "label": "Structural Repairs ($)",
        "type": "number",
        "step": 5000,
        "min": 0,
        "section": "Major Capital Items",
    },
    {
        "name": "contingency_pct",
        "label": "Contingency (%)",
        "type": "number",
        "step": 1,
        "min": 5,
        "max": 25,
        "format": "percentage",
        "section": "Budget Adjustments",
    },
    {
        "name": "soft_costs_pct",
        "label": "Soft Costs (%)",
        "type": "number",
        "step": 1,
        "min": 3,
        "max": 15,
        "format": "percentage",
        "section": "Budget Adjustments",
    },
    {
        "name": "current_avg_rent",
        "label": "Current Avg Rent ($/month)",
        "type": "number",
        "step": 50,
        "min": 100,
        "section": "Revenue Impact",
    },
    {
        "name": "post_reno_avg_rent",
        "label": "Post-Renovation Avg Rent ($/month)",
        "type": "number",
        "step": 50,
        "min": 100,
        "section": "Revenue Impact",
    },
    {
        "name": "current_occupancy",
        "label": "Current Occupancy (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Revenue Impact",
    },
    {
        "name": "stabilized_occupancy",
        "label": "Stabilized Occupancy (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Revenue Impact",
    },
    {
        "name": "months_to_complete",
        "label": "Project Duration (months)",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 36,
        "section": "Timeline & Financing",
    },
    {
        "name": "units_renovated_per_month",
        "label": "Units Renovated Per Month",
        "type": "number",
        "step": 1,
        "min": 1,
        "section": "Timeline & Financing",
    },
    {
        "name": "financing_cost_pct",
        "label": "Financing Interest Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 15,
        "format": "percentage",
        "section": "Timeline & Financing",
    },
    {
        "name": "holding_costs_monthly",
        "label": "Monthly Holding Costs ($)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Timeline & Financing",
    },
    {"name": "tags", "label": "Tags (comma-separated)", "type": "text", "section": "Metadata"},
    {"name": "purpose", "label": "Analysis Purpose", "type": "text", "section": "Metadata"},
    {"name": "references", "label": "References / Links", "type": "text", "section": "Metadata"},
    {"name": "notes", "label": "Additional Notes", "type": "textarea", "section": "Metadata"},
]


def prepare_inputs(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert percentages to decimals."""
    out = raw.copy()
    for key in ["contingency_pct", "soft_costs_pct", "current_occupancy", "stabilized_occupancy", "financing_cost_pct"]:
        if key in out and out[key] > 1:
            out[key] = out[key] / 100.0
    return out


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Build renovation budget breakdown and ROI analysis."""

    total_units = inputs["total_units"]

    # Calculate per-unit interior costs
    interior_per_unit = (
        inputs["kitchen_renovation_per_unit"]
        + inputs["bathroom_renovation_per_unit"]
        + inputs["flooring_per_unit"]
        + inputs["paint_per_unit"]
        + inputs["appliances_per_unit"]
        + inputs["fixtures_per_unit"]
        + inputs["hvac_per_unit"]
        + inputs["electrical_per_unit"]
        + inputs["plumbing_per_unit"]
        + inputs["other_per_unit"]
    )

    total_interior_costs = interior_per_unit * total_units

    # Exterior and common area costs
    exterior_costs = (
        inputs["common_area_renovation"]
        + inputs["exterior_improvements"]
        + inputs["landscaping"]
        + inputs["parking_lot_repaving"]
    )

    # Major capital items
    major_capital = inputs["roof_replacement"] + inputs["structural_repairs"]

    # Hard costs subtotal
    hard_costs = total_interior_costs + exterior_costs + major_capital

    # Contingency and soft costs
    contingency = hard_costs * inputs["contingency_pct"]
    soft_costs = hard_costs * inputs["soft_costs_pct"]

    # Total renovation budget
    total_budget = hard_costs + contingency + soft_costs

    # Financing costs
    months = inputs["months_to_complete"]
    financing_rate = inputs["financing_cost_pct"]
    avg_outstanding_balance = total_budget / 2  # Assume linear drawdown
    financing_costs = (avg_outstanding_balance * financing_rate * months) / 12

    # Holding costs
    total_holding_costs = inputs["holding_costs_monthly"] * months

    # All-in cost
    all_in_cost = total_budget + financing_costs + total_holding_costs

    # Revenue impact analysis
    current_monthly_revenue = inputs["current_avg_rent"] * total_units * inputs["current_occupancy"]
    stabilized_monthly_revenue = inputs["post_reno_avg_rent"] * total_units * inputs["stabilized_occupancy"]
    monthly_revenue_increase = stabilized_monthly_revenue - current_monthly_revenue
    annual_revenue_increase = monthly_revenue_increase * 12

    # ROI calculations
    if all_in_cost > 0:
        renovation_yield = annual_revenue_increase / all_in_cost
        payback_years = all_in_cost / annual_revenue_increase if annual_revenue_increase > 0 else 999
    else:
        renovation_yield = 0
        payback_years = 999

    # Cost per unit and per SF
    cost_per_unit = total_budget / total_units
    cost_per_sf = total_budget / inputs["total_square_footage"] if inputs["total_square_footage"] > 0 else 0

    # Breakdown by category
    breakdown = {
        "Interior Renovations": {
            "Kitchen": inputs["kitchen_renovation_per_unit"] * total_units,
            "Bathroom": inputs["bathroom_renovation_per_unit"] * total_units,
            "Flooring": inputs["flooring_per_unit"] * total_units,
            "Paint": inputs["paint_per_unit"] * total_units,
            "Appliances": inputs["appliances_per_unit"] * total_units,
            "Fixtures": inputs["fixtures_per_unit"] * total_units,
            "HVAC": inputs["hvac_per_unit"] * total_units,
            "Electrical": inputs["electrical_per_unit"] * total_units,
            "Plumbing": inputs["plumbing_per_unit"] * total_units,
            "Other": inputs["other_per_unit"] * total_units,
        },
        "Exterior & Common": {
            "Common Areas": inputs["common_area_renovation"],
            "Exterior": inputs["exterior_improvements"],
            "Landscaping": inputs["landscaping"],
            "Parking": inputs["parking_lot_repaving"],
        },
        "Major Capital": {
            "Roof": inputs["roof_replacement"],
            "Structural": inputs["structural_repairs"],
        },
    }

    metrics = {
        "total_units": total_units,
        "interior_per_unit": interior_per_unit,
        "total_interior_costs": total_interior_costs,
        "exterior_costs": exterior_costs,
        "major_capital": major_capital,
        "hard_costs": hard_costs,
        "contingency": contingency,
        "soft_costs": soft_costs,
        "total_budget": total_budget,
        "financing_costs": financing_costs,
        "total_holding_costs": total_holding_costs,
        "all_in_cost": all_in_cost,
        "cost_per_unit": cost_per_unit,
        "cost_per_sf": cost_per_sf,
        "current_monthly_revenue": current_monthly_revenue,
        "stabilized_monthly_revenue": stabilized_monthly_revenue,
        "monthly_revenue_increase": monthly_revenue_increase,
        "annual_revenue_increase": annual_revenue_increase,
        "renovation_yield": renovation_yield,
        "payback_years": payback_years,
    }

    return {"breakdown": breakdown, "metrics": metrics}


def build_report_tables(inputs: Dict[str, Any], breakdown: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build table specifications for the frontend."""

    # Budget summary table
    summary_table = {
        "title": "Renovation Budget Summary",
        "headers": ["Item", "Amount"],
        "rows": [
            ["Total Units", f"{metrics['total_units']:,}"],
            ["Hard Costs", format_currency(metrics['hard_costs'])],
            ["Contingency", format_currency(metrics['contingency'])],
            ["Soft Costs", format_currency(metrics['soft_costs'])],
            ["Total Renovation Budget", format_currency(metrics['total_budget'])],
            ["Financing Costs", format_currency(metrics['financing_costs'])],
            ["Holding Costs", format_currency(metrics['total_holding_costs'])],
            ["All-In Cost", format_currency(metrics['all_in_cost'])],
            ["Cost Per Unit", format_currency(metrics['cost_per_unit'])],
            ["Cost Per SF", f"${metrics['cost_per_sf']:.2f}"],
        ],
    }

    # ROI analysis table
    roi_table = {
        "title": "Return on Investment Analysis",
        "headers": ["Metric", "Value"],
        "rows": [
            ["Current Monthly Revenue", format_currency(metrics['current_monthly_revenue'])],
            ["Stabilized Monthly Revenue", format_currency(metrics['stabilized_monthly_revenue'])],
            ["Monthly Revenue Increase", format_currency(metrics['monthly_revenue_increase'])],
            ["Annual Revenue Increase", format_currency(metrics['annual_revenue_increase'])],
            ["Renovation Yield", format_percentage(metrics['renovation_yield'])],
            ["Payback Period", f"{metrics['payback_years']:.1f} years"],
        ],
    }

    # Interior costs breakdown
    interior_rows = []
    for category, amount in breakdown["Interior Renovations"].items():
        if amount > 0:
            interior_rows.append([category, format_currency(amount)])
    interior_rows.append(["Total Interior", format_currency(metrics['total_interior_costs'])])

    interior_table = {
        "title": "Interior Renovation Costs",
        "headers": ["Category", "Amount"],
        "rows": interior_rows,
    }

    # Exterior & capital breakdown
    exterior_rows = []
    for category, amount in breakdown["Exterior & Common"].items():
        if amount > 0:
            exterior_rows.append([category, format_currency(amount)])
    for category, amount in breakdown["Major Capital"].items():
        if amount > 0:
            exterior_rows.append([category, format_currency(amount)])
    exterior_rows.append(["Total Exterior & Capital", format_currency(metrics['exterior_costs'] + metrics['major_capital'])])

    exterior_table = {
        "title": "Exterior & Capital Costs",
        "headers": ["Category", "Amount"],
        "rows": exterior_rows,
    }

    return [summary_table, roi_table, interior_table, exterior_table]


def build_chart_specs(inputs: Dict[str, Any], breakdown: Dict[str, Any], metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build chart specifications for the frontend."""

    # Budget breakdown pie chart
    budget_chart = {
        "title": "Budget Breakdown",
        "type": "pie",
        "data": {
            "labels": ["Interior Renovations", "Exterior & Common", "Major Capital", "Contingency", "Soft Costs"],
            "datasets": [{
                "data": [
                    metrics['total_interior_costs'],
                    metrics['exterior_costs'],
                    metrics['major_capital'],
                    metrics['contingency'],
                    metrics['soft_costs'],
                ],
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.6)",
                    "rgba(54, 162, 235, 0.6)",
                    "rgba(255, 206, 86, 0.6)",
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(153, 102, 255, 0.6)",
                ],
            }],
        },
    }

    # Interior costs breakdown
    interior_categories = []
    interior_amounts = []
    for category, amount in breakdown["Interior Renovations"].items():
        if amount > 0:
            interior_categories.append(category)
            interior_amounts.append(amount)

    interior_chart = {
        "title": "Interior Renovation Costs by Category",
        "type": "bar",
        "data": {
            "labels": interior_categories,
            "datasets": [{
                "label": "Cost ($)",
                "data": interior_amounts,
                "backgroundColor": "rgba(75, 192, 192, 0.6)",
            }],
        },
    }

    # Revenue comparison
    revenue_chart = {
        "title": "Revenue Impact",
        "type": "bar",
        "data": {
            "labels": ["Current Monthly Revenue", "Stabilized Monthly Revenue"],
            "datasets": [{
                "label": "Monthly Revenue ($)",
                "data": [metrics['current_monthly_revenue'], metrics['stabilized_monthly_revenue']],
                "backgroundColor": ["rgba(255, 99, 132, 0.6)", "rgba(54, 162, 235, 0.6)"],
            }],
        },
    }

    return [budget_chart, interior_chart, revenue_chart]


def interactive_cli():
    """Run the interactive CLI for renovation budget analysis."""
    console.print(Panel.fit("🔨 Renovation Budget Analyzer", style="bold cyan"))

    # Gather inputs
    project_name = prompt_text("Project Name", DEFAULT_INPUTS["project_name"])
    location = prompt_text("Location", DEFAULT_INPUTS["location"])
    analyst = prompt_text("Analyst", DEFAULT_INPUTS["analyst"])

    total_units = prompt_int("Total Units", DEFAULT_INPUTS["total_units"])
    kitchen_cost = prompt_float("Kitchen Renovation Per Unit", DEFAULT_INPUTS["kitchen_renovation_per_unit"])
    bathroom_cost = prompt_float("Bathroom Renovation Per Unit", DEFAULT_INPUTS["bathroom_renovation_per_unit"])

    inputs = {
        **DEFAULT_INPUTS,
        "project_name": project_name,
        "location": location,
        "analyst": analyst,
        "total_units": total_units,
        "kitchen_renovation_per_unit": kitchen_cost,
        "bathroom_renovation_per_unit": bathroom_cost,
    }

    # Prepare and run
    prepared = prepare_inputs(inputs)
    output = build_projection(prepared)

    # Display results
    console.print("\n" + "=" * 80)
    console.print("[bold green]RENOVATION BUDGET ANALYSIS[/bold green]")
    console.print("=" * 80 + "\n")

    metrics_data = [
        ["Total Budget", format_currency(output['metrics']['total_budget'])],
        ["All-In Cost", format_currency(output['metrics']['all_in_cost'])],
        ["Cost Per Unit", format_currency(output['metrics']['cost_per_unit'])],
        ["Renovation Yield", format_percentage(output['metrics']['renovation_yield'])],
    ]
    render_metrics_table("Budget Summary", metrics_data)

    # Save to database
    console.print("\n[cyan]Saving to database...[/cyan]")
    ensure_database()
    with session_scope() as session:
        record = RenovationBudgetModel(
            name=project_name,
            location=location,
            analyst=analyst,
            property_type=inputs["property_type"],
            total_units=total_units,
            inputs=prepared,
            results=output,
        )
        session.add(record)

    console.print("[bold green]✓ Analysis complete![/bold green]\n")


if __name__ == "__main__":
    interactive_cli()
