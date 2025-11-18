"""Interactive CLI and shared utilities for fix-and-flip analysis."""

from __future__ import annotations

from typing import Any, Dict, List

from rich.panel import Panel

from app.models.real_estate import FixAndFlipModel

from .base import (
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
    save_bar_chart,
    save_line_chart,
    session_scope,
)


MARKET_RULES = {
    "Hot": 0.65,
    "Moderate": 0.70,
    "Slow": 0.75,
}


DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Sample Fix & Flip",
    "location": "Austin, TX",
    "analyst": "",
    "property_type": "Single Family Home",
    "square_footage": 1800,
    "bedrooms": 3,
    "bathrooms": 2.0,
    "year_built": 1985,
    "market_type": "Moderate",
    "arv": 325_000.0,
    "purchase_price": 215_000.0,
    "repair_costs": 45_000.0,
    "closing_costs": 6_000.0,
    "holding_period_months": 6,
    "holding_costs_monthly": 700.0,
    "acquisition_months": 1,
    "renovation_months": 3,
    "marketing_months": 2,
    "loan_ltv": 0.75,
    "loan_points": 0.02,
    "interest_rate": 0.095,
    "selling_cost_pct": 0.07,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "project_name", "label": "Project Name", "type": "text", "section": "Property Profile"},
    {"name": "location", "label": "Market / Location", "type": "text", "section": "Property Profile"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Property Profile"},
    {"name": "property_type", "label": "Property Type", "type": "text", "section": "Property Profile"},
    {"name": "project_name", "label": "Project Name", "type": "text"},
    {"name": "location", "label": "Market / Location", "type": "text"},
    {"name": "property_type", "label": "Property Type", "type": "text"},
    {
        "name": "market_type",
        "label": "Market Speed",
        "type": "text",
        "options": list(MARKET_RULES.keys()),
        "section": "Property Profile",
    },
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
    {"name": "arv", "label": "After Repair Value ($)", "type": "number", "step": 1000, "min": 50000, "section": "Acquisition & Costs"},
    {
        "name": "purchase_price",
        "label": "Purchase Price ($)",
        "type": "number",
        "step": 1000,
        "min": 50000,
        "section": "Acquisition & Costs",
    },
    {
        "name": "closing_costs",
        "label": "Closing Costs ($)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Acquisition & Costs",
    },
    {
        "name": "repair_costs",
        "label": "Renovation Budget ($)",
        "type": "number",
        "step": 500,
        "min": 0,
        "section": "Acquisition & Costs",
    },
    {
        "name": "holding_costs_monthly",
        "label": "Monthly Holding Costs ($)",
        "type": "number",
        "step": 50,
        "min": 0,
        "section": "Timeline & Holding",
    },
    {
        "name": "holding_period_months",
        "label": "Hold Period (months)",
        "type": "number",
        "step": 1,
        "min": 1,
        "section": "Timeline & Holding",
    },
    {
        "name": "acquisition_months",
        "label": "Acquisition Timeline (months)",
        "type": "number",
        "step": 1,
        "min": 0,
        "section": "Timeline & Holding",
    },
    {
        "name": "renovation_months",
        "label": "Renovation Timeline (months)",
        "type": "number",
        "step": 1,
        "min": 0,
        "section": "Timeline & Holding",
    },
    {
        "name": "marketing_months",
        "label": "Marketing Timeline (months)",
        "type": "number",
        "step": 1,
        "min": 0,
        "section": "Timeline & Holding",
    },
    {
        "name": "loan_ltv",
        "label": "Loan-to-Value (%)",
        "type": "number",
        "step": 1,
        "min": 50,
        "max": 90,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {
        "name": "loan_points",
        "label": "Origination Points (%)",
        "type": "number",
        "step": 0.25,
        "min": 0,
        "max": 5,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {
        "name": "interest_rate",
        "label": "Interest Rate (%)",
        "type": "number",
        "step": 0.25,
        "min": 2,
        "max": 25,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {
        "name": "selling_cost_pct",
        "label": "Selling Costs (%)",
        "type": "number",
        "step": 0.25,
        "min": 3,
        "max": 12,
        "format": "percentage",
        "section": "Financing & Exit",
    },
    {"name": "purchase_price", "label": "Purchase Price ($)", "type": "number", "step": 1000, "min": 50000},
    {"name": "repair_costs", "label": "Renovation Budget ($)", "type": "number", "step": 500, "min": 0},
    {"name": "holding_period_months", "label": "Hold Period (months)", "type": "number", "step": 1, "min": 3},
    {"name": "holding_costs_monthly", "label": "Monthly Holding Costs ($)", "type": "number", "step": 50, "min": 0},
    {"name": "loan_ltv", "label": "Loan-to-Value", "type": "number", "step": 0.01, "min": 0.5, "max": 0.9},
    {"name": "interest_rate", "label": "Interest Rate", "type": "number", "step": 0.005, "min": 0.02, "max": 0.2},
]


def prepare_inputs(overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Combine overrides with defaults for downstream processing."""

    merged = DEFAULT_INPUTS.copy()
    merged.update(overrides)
    return merged


def analyze_flip(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate profitability, funding, and sensitivity metrics."""

    arv = inputs["arv"]
    repair_costs = inputs["repair_costs"]
    purchase_price = inputs["purchase_price"]
    closing_costs = inputs["closing_costs"]
    holding_costs = inputs["holding_costs_monthly"] * inputs["holding_period_months"]
    loan_ltv = inputs["loan_ltv"]
    loan_points = inputs["loan_points"]
    interest_rate = inputs["interest_rate"]
    holding_period_months = inputs["holding_period_months"]
    selling_cost_pct = inputs["selling_cost_pct"]

    mao_ratio = MARKET_RULES.get(inputs["market_type"], 0.70)
    mao = (arv * mao_ratio) - repair_costs

    loan_amount = purchase_price * loan_ltv
    down_payment = purchase_price - loan_amount
    points_cost = loan_amount * loan_points
    monthly_interest = (interest_rate / 12) * loan_amount
    interest_cost = monthly_interest * holding_period_months
    financing_costs = points_cost + interest_cost

    total_cost = (
        purchase_price
        + closing_costs
        + repair_costs
        + holding_costs
        + financing_costs
    )
    selling_costs = arv * selling_cost_pct
    gross_profit = arv - selling_costs - total_cost

    cash_invested = down_payment + closing_costs + repair_costs + points_cost + holding_costs
    roi = gross_profit / cash_invested if cash_invested else 0.0
    profit_margin = gross_profit / arv if arv else 0.0
    return_on_cost = gross_profit / total_cost if total_cost else 0.0

    timeline_rows = [
        {
            "phase": "Acquisition",
            "months": inputs["acquisition_months"],
            "cost": closing_costs + down_payment,
        },
        {
            "phase": "Renovation",
            "months": inputs["renovation_months"],
            "cost": repair_costs,
        },
        {
            "phase": "Marketing",
            "months": inputs["marketing_months"],
            "cost": holding_costs,
        },
    ]

    scenario_rows: List[Dict[str, Any]] = []
    for label, multiplier in [
        ("Conservative (-5%)", 0.95),
        ("Base", 1.0),
        ("Upside (+5%)", 1.05),
    ]:
        sale_price = arv * multiplier
        sale_costs = sale_price * selling_cost_pct
        profit = sale_price - sale_costs - total_cost
        scenario_rows.append(
            {
                "label": label,
                "sale_price": sale_price,
                "profit": profit,
                "roi": profit / cash_invested if cash_invested else 0.0,
            }
        )

    if roi >= 0.35:
        deal_quality = "Excellent"
    elif roi >= 0.25:
        deal_quality = "Strong"
    elif roi >= 0.15:
        deal_quality = "Average"
    else:
        deal_quality = "Marginal"

    return {
        "mao": mao,
        "mao_ratio": mao_ratio,
        "loan_amount": loan_amount,
        "down_payment": down_payment,
        "points_cost": points_cost,
        "interest_cost": interest_cost,
        "financing_costs": financing_costs,
        "total_cost": total_cost,
        "gross_profit": gross_profit,
        "cash_invested": cash_invested,
        "roi": roi,
        "profit_margin": profit_margin,
        "return_on_cost": return_on_cost,
        "timeline": timeline_rows,
        "scenario_rows": scenario_rows,
        "passes_mao": purchase_price <= mao,
        "cost_breakdown": {
            "Purchase": purchase_price,
            "Renovation": repair_costs,
            "Closing": closing_costs,
            "Holding": holding_costs,
            "Financing": financing_costs,
        },
        "deal_quality": deal_quality,
    }


def build_report_tables(inputs: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return table definitions shared by CLI rendering and the web UI."""

    property_rows = [
        {"Field": "Project", "Value": inputs["project_name"]},
        {"Field": "Location", "Value": inputs["location"]},
        {"Field": "Property Type", "Value": inputs.get("property_type", "Single Family")},
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

    key_metrics = {
        "ARV": format_currency(inputs["arv"]),
        "Purchase Price": format_currency(inputs["purchase_price"]),
        "Renovation Budget": format_currency(inputs["repair_costs"]),
        "All-In Cost": format_currency(results["total_cost"]),
        "Gross Profit": format_currency(results["gross_profit"]),
        "ROI": format_percentage(results["roi"]),
        "Profit Margin": format_percentage(results["profit_margin"]),
        "70% Rule Target": format_currency(results["mao"]),
        "Offer Meets Rule": "PASS" if results["passes_mao"] else "CAUTION",
        "Deal Quality": results["deal_quality"],
    }

    financing_metrics = {
        "Loan Amount": format_currency(results["loan_amount"]),
        "Down Payment": format_currency(results["down_payment"]),
        "Points Cost": format_currency(results["points_cost"]),
        "Interest Cost": format_currency(results["interest_cost"]),
        "Financing Costs": format_currency(results["financing_costs"]),
        "Cash Invested": format_currency(results["cash_invested"]),
        "Return on Cost": format_percentage(results["return_on_cost"]),
    }

    timeline_rows = [
        {
            "Phase": item["phase"],
            "Duration": f"{item['months']} mo",
            "Cost": format_currency(item["cost"]),
        }
        for item in results["timeline"]
    ]
    total_months = sum(item["months"] for item in results["timeline"])
    total_cost = sum(item["cost"] for item in results["timeline"])
    timeline_rows.append(
        {
            "Phase": "Total Hold Period",
            "Duration": f"{total_months} mo",
            "Cost": format_currency(total_cost),
        }
    )

    scenario_rows = [
        {
            "Scenario": item["label"],
            "Sale Price": format_currency(item["sale_price"]),
            "Profit": format_currency(item["profit"]),
            "ROI": format_percentage(item["roi"]),
        }
        for item in results["scenario_rows"]
    ]

    return [
        {"kind": "table", "title": "Property Information", "columns": ["Field", "Value"], "rows": property_rows},
        {"kind": "metrics", "title": "Key Deal Metrics", "metrics": key_metrics},
        {"kind": "metrics", "title": "Financing Summary", "metrics": financing_metrics},
        {"kind": "table", "title": "Project Timeline", "columns": ["Phase", "Duration", "Cost"], "rows": timeline_rows},
        {
            "kind": "table",
            "title": "Exit Sensitivity",
            "columns": ["Scenario", "Sale Price", "Profit", "ROI"],
            "rows": scenario_rows,
        },
    ]


def build_chart_specs(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return chart definitions that mirror the Excel dashboards."""

    cumulative_months: List[int] = []
    cumulative_costs: List[float] = []
    running_months = 0
    running_cost = 0.0
    for stage in results["timeline"]:
        running_months += stage["months"]
        running_cost += stage["cost"]
        cumulative_months.append(running_months)
        cumulative_costs.append(running_cost)

    return [
        {
            "key": "cost_breakdown",
            "type": "bar",
            "title": "Project Cost Breakdown",
            "filename": "cost_breakdown.png",
            "labels": list(results["cost_breakdown"].keys()),
            "datasets": [
                {
                    "label": "Cost",
                    "data": list(results["cost_breakdown"].values()),
                }
            ],
            "x_label": "Category",
            "y_label": "Amount ($)",
        },
        {
            "key": "scenario_profit",
            "type": "bar",
            "title": "Exit Scenario Profit",
            "filename": "scenario_profit.png",
            "labels": [row["label"] for row in results["scenario_rows"]],
            "datasets": [
                {
                    "label": "Profit",
                    "data": [row["profit"] for row in results["scenario_rows"]],
                }
            ],
            "x_label": "Scenario",
            "y_label": "Profit ($)",
        },
        {
            "key": "timeline",
            "type": "line",
            "title": "Cumulative Project Spend",
            "filename": "timeline_cumulative_cost.png",
            "labels": cumulative_months,
            "datasets": {"Cumulative Cost": cumulative_costs},
            "x_label": "Months",
            "y_label": "Amount ($)",
        },
    ]


def display_results(inputs: Dict[str, Any], results: Dict[str, Any]) -> None:
    """Render the analysis to the console."""

    for table in build_report_tables(inputs, results):
        if table["kind"] == "metrics":
            render_metrics_table(table["title"], table["metrics"])
        else:
            render_projection_table(table["title"], table["columns"], table["rows"])


def generate_visualizations(inputs: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, str]:
    """Generate charts that mirror the Excel dashboards."""

    report_dir = ensure_report_dir("fix_and_flip", inputs["project_name"])
    chart_paths: Dict[str, str] = {}

    for spec in build_chart_specs(results):
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
    """Prompt the user for fix-and-flip assumptions."""

    defaults = DEFAULT_INPUTS

    project_name = prompt_text("Project name", default=defaults["project_name"])
    location = prompt_text("Market / Location", default=defaults["location"])
    property_type = prompt_text("Property type", default=defaults["property_type"])
    square_footage = prompt_int("Square footage", default=defaults["square_footage"], minimum=500)
    bedrooms = prompt_int("Bedrooms", default=defaults["bedrooms"], minimum=1, maximum=10)
    bathrooms = prompt_float("Bathrooms", default=defaults["bathrooms"], minimum=1.0, maximum=6.0)
    year_built = prompt_int("Year built", default=defaults["year_built"], minimum=1900, maximum=2025)
    analyst = prompt_text("Analyst name", allow_blank=True) or None

    market_type = prompt_choice("Market speed", MARKET_RULES.keys(), default=defaults["market_type"])
    arv = prompt_float("After repair value (ARV)", minimum=100000.0, default=defaults["arv"])
    purchase_price = prompt_float("Purchase price", minimum=50000.0, default=defaults["purchase_price"])
    repair_costs = prompt_float("Renovation budget", minimum=10000.0, default=defaults["repair_costs"])
    closing_costs = prompt_float("Closing costs", default=defaults["closing_costs"])
    holding_period_months = prompt_int(
        "Total hold period (months)",
        default=defaults["holding_period_months"],
        minimum=3,
        maximum=18,
    )
    holding_costs_monthly = prompt_float(
        "Holding costs per month",
        default=defaults["holding_costs_monthly"],
        minimum=0.0,
    )

    acquisition_months = prompt_int(
        "Acquisition months",
        default=defaults["acquisition_months"],
        minimum=1,
        maximum=3,
    )
    renovation_months = prompt_int(
        "Renovation months",
        default=defaults["renovation_months"],
        minimum=1,
        maximum=12,
    )
    marketing_months = prompt_int(
        "Marketing months",
        default=defaults["marketing_months"],
        minimum=1,
        maximum=6,
    )

    loan_ltv = prompt_percentage("Loan-to-value", default=defaults["loan_ltv"], maximum=0.9)
    loan_points = prompt_percentage("Origination points (% of loan)", default=defaults["loan_points"])
    interest_rate = prompt_percentage("Interest rate (annual)", default=defaults["interest_rate"], maximum=0.18)
    selling_cost_pct = prompt_percentage("Selling costs (% of ARV)", default=defaults["selling_cost_pct"], maximum=0.1)

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
            "market_type": market_type,
            "arv": arv,
            "purchase_price": purchase_price,
            "repair_costs": repair_costs,
            "closing_costs": closing_costs,
            "holding_period_months": holding_period_months,
            "holding_costs_monthly": holding_costs_monthly,
            "acquisition_months": acquisition_months,
            "renovation_months": renovation_months,
            "marketing_months": marketing_months,
            "loan_ltv": loan_ltv,
            "loan_points": loan_points,
            "interest_rate": interest_rate,
            "selling_cost_pct": selling_cost_pct,
        }
    )


def main() -> None:
    """CLI entry point."""

    ensure_database()
    console.print(Panel("Fix & Flip Deal Analyzer", style="bold white on blue"))
    inputs = gather_inputs()
    results = analyze_flip(inputs)
    display_results(inputs, results)
    chart_paths = generate_visualizations(inputs, results)

    with session_scope() as session:
        record = FixAndFlipModel(
            name=inputs["project_name"],
            location=inputs["location"],
            analyst=inputs.get("analyst"),
            market_type=inputs["market_type"],
            inputs=inputs,
            results={**results, "charts": chart_paths},
        )
        session.add(record)
        session.flush()
        console.print(
            Panel(
                f"Fix-and-flip model saved with ID [bold]{record.id}[/bold]",
                style="green",
            )
        )


if __name__ == "__main__":
    main()
