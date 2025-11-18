"""Interactive CLI and shared helpers for the lease analyzer model."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
from rich.panel import Panel

from app.models.real_estate import LeaseAnalyzerModel

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
    "project_name": "Office Lease Analysis",
    "location": "Downtown District",
    "analyst": "",
    "tags": "",
    "purpose": "",
    "references": "",
    "notes": "",
    "property_type": "Office",
    "total_square_footage": 50000,
    "num_tenants": 5,
    "weighted_avg_rent_psf": 28.50,
    "total_annual_rent": 1425000.0,
    "vacancy_rate": 0.10,
    "operating_expense_ratio": 0.35,
    "annual_rent_growth": 0.025,
    "weighted_avg_lease_term": 5.0,
    "tenant_improvement_psf": 25.0,
    "leasing_commission_pct": 0.05,
    "lease_expiry_year_1": 0.15,
    "lease_expiry_year_2": 0.20,
    "lease_expiry_year_3": 0.25,
    "lease_expiry_year_4": 0.20,
    "lease_expiry_year_5": 0.20,
    "renewal_probability": 0.70,
    "market_rent_psf": 30.00,
    "free_rent_months": 2,
    "cap_rate": 0.07,
    "projection_years": 10,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Property Name", "type": "text", "section": "Property Profile"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Profile"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Profile"},
    {"name": "property_type", "label": "Property Type", "type": "text", "section": "Property Profile"},
    {
        "name": "total_square_footage",
        "label": "Total Square Footage",
        "type": "number",
        "step": 1000,
        "min": 100,
        "section": "Property Profile",
    },
    {
        "name": "num_tenants",
        "label": "Number of Tenants",
        "type": "number",
        "step": 1,
        "min": 1,
        "section": "Property Profile",
    },
    {
        "name": "weighted_avg_rent_psf",
        "label": "Weighted Avg Rent ($/SF/year)",
        "type": "number",
        "step": 0.50,
        "min": 1,
        "section": "Lease Economics",
    },
    {
        "name": "total_annual_rent",
        "label": "Total Annual Rent ($)",
        "type": "number",
        "step": 10000,
        "min": 1000,
        "section": "Lease Economics",
    },
    {
        "name": "vacancy_rate",
        "label": "Vacancy Rate (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 50,
        "format": "percentage",
        "section": "Lease Economics",
    },
    {
        "name": "operating_expense_ratio",
        "label": "Operating Expense Ratio (%)",
        "type": "number",
        "step": 1,
        "min": 10,
        "max": 80,
        "format": "percentage",
        "section": "Lease Economics",
    },
    {
        "name": "annual_rent_growth",
        "label": "Annual Rent Growth (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Lease Economics",
    },
    {
        "name": "weighted_avg_lease_term",
        "label": "Weighted Avg Lease Term (years)",
        "type": "number",
        "step": 0.5,
        "min": 1,
        "max": 20,
        "section": "Lease Economics",
    },
    {
        "name": "tenant_improvement_psf",
        "label": "Tenant Improvements ($/SF)",
        "type": "number",
        "step": 1,
        "min": 0,
        "section": "Leasing Costs",
    },
    {
        "name": "leasing_commission_pct",
        "label": "Leasing Commission (%)",
        "type": "number",
        "step": 0.5,
        "min": 0,
        "max": 10,
        "format": "percentage",
        "section": "Leasing Costs",
    },
    {
        "name": "lease_expiry_year_1",
        "label": "Lease Expiry Year 1 (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Lease Rollover Schedule",
    },
    {
        "name": "lease_expiry_year_2",
        "label": "Lease Expiry Year 2 (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Lease Rollover Schedule",
    },
    {
        "name": "lease_expiry_year_3",
        "label": "Lease Expiry Year 3 (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Lease Rollover Schedule",
    },
    {
        "name": "lease_expiry_year_4",
        "label": "Lease Expiry Year 4 (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Lease Rollover Schedule",
    },
    {
        "name": "lease_expiry_year_5",
        "label": "Lease Expiry Year 5 (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Lease Rollover Schedule",
    },
    {
        "name": "renewal_probability",
        "label": "Renewal Probability (%)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 100,
        "format": "percentage",
        "section": "Market Assumptions",
    },
    {
        "name": "market_rent_psf",
        "label": "Market Rent ($/SF/year)",
        "type": "number",
        "step": 0.50,
        "min": 1,
        "section": "Market Assumptions",
    },
    {
        "name": "free_rent_months",
        "label": "Free Rent Period (months)",
        "type": "number",
        "step": 1,
        "min": 0,
        "max": 12,
        "section": "Market Assumptions",
    },
    {
        "name": "cap_rate",
        "label": "Cap Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 3,
        "max": 12,
        "format": "percentage",
        "section": "Valuation",
    },
    {
        "name": "projection_years",
        "label": "Projection Period (years)",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 20,
        "section": "Valuation",
    },
    {"name": "tags", "label": "Tags (comma-separated)", "type": "text", "section": "Metadata"},
    {"name": "purpose", "label": "Analysis Purpose", "type": "text", "section": "Metadata"},
    {"name": "references", "label": "References / Links", "type": "text", "section": "Metadata"},
    {"name": "notes", "label": "Additional Notes", "type": "textarea", "section": "Metadata"},
]


def prepare_inputs(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert percentages to decimals."""
    out = raw.copy()
    for key in [
        "vacancy_rate",
        "operating_expense_ratio",
        "annual_rent_growth",
        "leasing_commission_pct",
        "lease_expiry_year_1",
        "lease_expiry_year_2",
        "lease_expiry_year_3",
        "lease_expiry_year_4",
        "lease_expiry_year_5",
        "renewal_probability",
        "cap_rate",
    ]:
        if key in out and out[key] > 1:
            out[key] = out[key] / 100.0
    return out


def build_projection(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Build lease rollover and cash flow projections."""
    years = inputs["projection_years"]
    total_sf = inputs["total_square_footage"]
    base_rent_psf = inputs["weighted_avg_rent_psf"]
    vacancy = inputs["vacancy_rate"]
    opex_ratio = inputs["operating_expense_ratio"]
    rent_growth = inputs["annual_rent_growth"]
    ti_psf = inputs["tenant_improvement_psf"]
    commission_pct = inputs["leasing_commission_pct"]
    market_rent = inputs["market_rent_psf"]
    renewal_prob = inputs["renewal_probability"]
    free_months = inputs["free_rent_months"]
    cap_rate = inputs["cap_rate"]

    # Lease expiry schedule
    expiry_schedule = [
        inputs.get("lease_expiry_year_1", 0),
        inputs.get("lease_expiry_year_2", 0),
        inputs.get("lease_expiry_year_3", 0),
        inputs.get("lease_expiry_year_4", 0),
        inputs.get("lease_expiry_year_5", 0),
    ]

    projections = []
    occupied_sf = total_sf * (1 - vacancy)

    for year in range(1, years + 1):
        # Calculate rent per SF for this year
        current_rent_psf = base_rent_psf * ((1 + rent_growth) ** (year - 1))

        # Determine lease rollover
        expiry_idx = min(year - 1, len(expiry_schedule) - 1)
        rollover_pct = expiry_schedule[expiry_idx] if year <= 5 else 0.20
        rollover_sf = occupied_sf * rollover_pct

        # Calculate leasing costs
        renewed_sf = rollover_sf * renewal_prob
        new_tenant_sf = rollover_sf * (1 - renewal_prob)

        # TI and commissions
        ti_cost = new_tenant_sf * ti_psf
        commission = (renewed_sf + new_tenant_sf) * market_rent * commission_pct
        total_leasing_costs = ti_cost + commission

        # Calculate revenue
        gross_rent = occupied_sf * current_rent_psf
        free_rent_loss = (free_months / 12) * (new_tenant_sf * market_rent)
        effective_gross_income = gross_rent - free_rent_loss

        # Operating expenses
        operating_expenses = effective_gross_income * opex_ratio

        # NOI
        noi = effective_gross_income - operating_expenses

        # Cash flow after leasing costs
        cash_flow = noi - total_leasing_costs

        # Property value
        property_value = noi / cap_rate if cap_rate > 0 else 0

        projections.append({
            "year": year,
            "occupied_sf": occupied_sf,
            "rollover_sf": rollover_sf,
            "renewed_sf": renewed_sf,
            "new_tenant_sf": new_tenant_sf,
            "rent_psf": current_rent_psf,
            "gross_rent": gross_rent,
            "free_rent_loss": free_rent_loss,
            "effective_gross_income": effective_gross_income,
            "operating_expenses": operating_expenses,
            "noi": noi,
            "ti_cost": ti_cost,
            "commission": commission,
            "total_leasing_costs": total_leasing_costs,
            "cash_flow": cash_flow,
            "property_value": property_value,
        })

    # Calculate summary metrics
    total_noi = sum(p["noi"] for p in projections)
    avg_noi = total_noi / len(projections)
    total_leasing_costs = sum(p["total_leasing_costs"] for p in projections)
    avg_cash_flow = sum(p["cash_flow"] for p in projections) / len(projections)
    stabilized_value = avg_noi / cap_rate if cap_rate > 0 else 0

    metrics = {
        "total_sf": total_sf,
        "occupied_sf": occupied_sf,
        "walt": inputs["weighted_avg_lease_term"],
        "avg_rent_psf": base_rent_psf,
        "market_rent_psf": market_rent,
        "avg_annual_noi": avg_noi,
        "avg_annual_cash_flow": avg_cash_flow,
        "total_leasing_costs": total_leasing_costs,
        "stabilized_value": stabilized_value,
        "cap_rate": cap_rate,
    }

    return {"projections": projections, "metrics": metrics}


def build_report_tables(
    inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Build table specifications for the frontend."""

    # Summary metrics table
    summary_table = {
        "title": "Lease Analysis Summary",
        "headers": ["Metric", "Value"],
        "rows": [
            ["Total Square Footage", f"{metrics['total_sf']:,.0f} SF"],
            ["Occupied Square Footage", f"{metrics['occupied_sf']:,.0f} SF"],
            ["Weighted Average Lease Term", f"{metrics['walt']:.1f} years"],
            ["Average Rent ($/SF)", f"${metrics['avg_rent_psf']:.2f}"],
            ["Market Rent ($/SF)", f"${metrics['market_rent_psf']:.2f}"],
            ["Average Annual NOI", format_currency(metrics['avg_annual_noi'])],
            ["Average Annual Cash Flow", format_currency(metrics['avg_annual_cash_flow'])],
            ["Total Leasing Costs (All Years)", format_currency(metrics['total_leasing_costs'])],
            ["Stabilized Property Value", format_currency(metrics['stabilized_value'])],
            ["Cap Rate", format_percentage(metrics['cap_rate'])],
        ],
    }

    # Projections table
    projection_rows = []
    for p in projections:
        projection_rows.append([
            f"Year {p['year']}",
            format_currency(p['noi']),
            format_currency(p['cash_flow']),
            f"{p['rollover_sf']:,.0f} SF",
            format_currency(p['total_leasing_costs']),
            format_currency(p['property_value']),
        ])

    projection_table = {
        "title": "Year-by-Year Projections",
        "headers": ["Year", "NOI", "Cash Flow", "Lease Rollover", "Leasing Costs", "Property Value"],
        "rows": projection_rows,
    }

    # Lease rollover table
    rollover_rows = []
    for p in projections[:min(10, len(projections))]:
        rollover_rows.append([
            f"Year {p['year']}",
            f"{p['rollover_sf']:,.0f} SF",
            f"{p['renewed_sf']:,.0f} SF",
            f"{p['new_tenant_sf']:,.0f} SF",
            format_currency(p['ti_cost']),
            format_currency(p['commission']),
        ])

    rollover_table = {
        "title": "Lease Rollover Analysis",
        "headers": ["Year", "Expiring SF", "Renewed SF", "New Tenant SF", "TI Costs", "Commissions"],
        "rows": rollover_rows,
    }

    return [summary_table, projection_table, rollover_table]


def build_chart_specs(
    inputs: Dict[str, Any], projections: List[Dict[str, Any]], metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Build chart specifications for the frontend."""

    years = [p["year"] for p in projections]

    # NOI and Cash Flow chart
    noi_cashflow_chart = {
        "title": "NOI vs Cash Flow Over Time",
        "type": "line",
        "data": {
            "labels": [f"Year {y}" for y in years],
            "datasets": [
                {
                    "label": "NOI",
                    "data": [p["noi"] for p in projections],
                    "borderColor": "rgb(75, 192, 192)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                },
                {
                    "label": "Cash Flow",
                    "data": [p["cash_flow"] for p in projections],
                    "borderColor": "rgb(255, 99, 132)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                },
            ],
        },
    }

    # Lease rollover chart
    rollover_chart = {
        "title": "Lease Rollover Schedule",
        "type": "bar",
        "data": {
            "labels": [f"Year {y}" for y in years],
            "datasets": [
                {
                    "label": "Renewed Leases (SF)",
                    "data": [p["renewed_sf"] for p in projections],
                    "backgroundColor": "rgba(54, 162, 235, 0.6)",
                },
                {
                    "label": "New Tenant Leases (SF)",
                    "data": [p["new_tenant_sf"] for p in projections],
                    "backgroundColor": "rgba(255, 206, 86, 0.6)",
                },
            ],
        },
    }

    # Leasing costs chart
    leasing_costs_chart = {
        "title": "Annual Leasing Costs",
        "type": "bar",
        "data": {
            "labels": [f"Year {y}" for y in years],
            "datasets": [
                {
                    "label": "TI Costs",
                    "data": [p["ti_cost"] for p in projections],
                    "backgroundColor": "rgba(153, 102, 255, 0.6)",
                },
                {
                    "label": "Commissions",
                    "data": [p["commission"] for p in projections],
                    "backgroundColor": "rgba(255, 159, 64, 0.6)",
                },
            ],
        },
    }

    return [noi_cashflow_chart, rollover_chart, leasing_costs_chart]


def interactive_cli():
    """Run the interactive CLI for lease analysis."""
    console.print(Panel.fit("🏢 Lease Analyzer", style="bold cyan"))

    # Gather inputs
    project_name = prompt_text("Property Name", DEFAULT_INPUTS["project_name"])
    location = prompt_text("Location", DEFAULT_INPUTS["location"])
    analyst = prompt_text("Analyst", DEFAULT_INPUTS["analyst"])

    total_sf = prompt_float("Total Square Footage", DEFAULT_INPUTS["total_square_footage"])
    num_tenants = prompt_int("Number of Tenants", DEFAULT_INPUTS["num_tenants"])
    avg_rent = prompt_float("Weighted Avg Rent ($/SF/year)", DEFAULT_INPUTS["weighted_avg_rent_psf"])
    vacancy = prompt_percentage("Vacancy Rate", DEFAULT_INPUTS["vacancy_rate"])
    walt = prompt_float("Weighted Avg Lease Term (years)", DEFAULT_INPUTS["weighted_avg_lease_term"])

    inputs = {
        **DEFAULT_INPUTS,
        "project_name": project_name,
        "location": location,
        "analyst": analyst,
        "total_square_footage": total_sf,
        "num_tenants": num_tenants,
        "weighted_avg_rent_psf": avg_rent,
        "vacancy_rate": vacancy / 100,
        "weighted_avg_lease_term": walt,
    }

    # Prepare and run
    prepared = prepare_inputs(inputs)
    output = build_projection(prepared)

    # Display results
    console.print("\n" + "=" * 80)
    console.print("[bold green]LEASE ANALYSIS RESULTS[/bold green]")
    console.print("=" * 80 + "\n")

    metrics_data = [
        ["Total SF", f"{output['metrics']['total_sf']:,.0f}"],
        ["Avg Annual NOI", format_currency(output['metrics']['avg_annual_noi'])],
        ["Avg Annual Cash Flow", format_currency(output['metrics']['avg_annual_cash_flow'])],
        ["Stabilized Value", format_currency(output['metrics']['stabilized_value'])],
    ]
    render_metrics_table("Summary Metrics", metrics_data)

    # Save to database
    console.print("\n[cyan]Saving to database...[/cyan]")
    ensure_database()
    with session_scope() as session:
        record = LeaseAnalyzerModel(
            name=project_name,
            location=location,
            analyst=analyst,
            property_type=inputs["property_type"],
            inputs=prepared,
            results=output,
        )
        session.add(record)

    console.print("[bold green]✓ Analysis complete![/bold green]\n")


if __name__ == "__main__":
    interactive_cli()
