"""Deterministic discounted cash flow model for corporate finance workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


DEFAULT_INPUTS: Dict[str, Any] = {
    "company_name": "SampleCo Holdings",
    "analyst": "Finance Team",
    "base_year": 2023,
    "revenue": 180_000_000.0,
    "revenue_growth_rate": 0.08,
    "ebitda_margin": 0.24,
    "depreciation_pct": 0.03,
    "capex_pct": 0.04,
    "nwc_pct_of_revenue": 0.02,
    "tax_rate": 0.25,
    "discount_rate": 0.095,
    "terminal_growth_rate": 0.025,
    "net_debt": 45_000_000.0,
    "shares_outstanding": 26_000_000.0,
    "projection_years": 5,
}


FORM_FIELDS: List[Dict[str, Any]] = [
    {"name": "company_name", "label": "Company", "type": "text", "section": "Overview"},
    {"name": "analyst", "label": "Analyst", "type": "text", "section": "Overview"},
    {
        "name": "base_year",
        "label": "Base Year",
        "type": "number",
        "step": 1,
        "min": 2000,
        "section": "Overview",
    },
    {
        "name": "projection_years",
        "label": "Projection Horizon (years)",
        "type": "number",
        "min": 3,
        "max": 10,
        "step": 1,
        "section": "Overview",
    },
    {
        "name": "revenue",
        "label": "Base Year Revenue ($)",
        "type": "number",
        "step": 1000000,
        "min": 1_000_000,
        "section": "Operating Assumptions",
    },
    {
        "name": "revenue_growth_rate",
        "label": "Annual Revenue Growth",
        "type": "number",
        "step": 0.1,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "ebitda_margin",
        "label": "EBITDA Margin",
        "type": "number",
        "step": 0.1,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "depreciation_pct",
        "label": "Depreciation (% of Revenue)",
        "type": "number",
        "step": 0.05,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "capex_pct",
        "label": "Capex (% of Revenue)",
        "type": "number",
        "step": 0.05,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "nwc_pct_of_revenue",
        "label": "Net Working Capital (% of Revenue)",
        "type": "number",
        "step": 0.05,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "tax_rate",
        "label": "Cash Tax Rate",
        "type": "number",
        "step": 0.1,
        "format": "percentage",
        "section": "Operating Assumptions",
    },
    {
        "name": "discount_rate",
        "label": "WACC / Discount Rate",
        "type": "number",
        "step": 0.1,
        "format": "percentage",
        "section": "Valuation Assumptions",
    },
    {
        "name": "terminal_growth_rate",
        "label": "Terminal Growth",
        "type": "number",
        "step": 0.05,
        "format": "percentage",
        "section": "Valuation Assumptions",
    },
    {
        "name": "net_debt",
        "label": "Net Debt ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "Capital Structure",
    },
    {
        "name": "shares_outstanding",
        "label": "Diluted Shares Outstanding",
        "type": "number",
        "step": 100_000,
        "min": 1,
        "section": "Capital Structure",
    },
]


@dataclass
class ProjectionYear:
    year: int
    revenue: float
    ebitda: float
    depreciation: float
    ebit: float
    taxes: float
    nopat: float
    capex: float
    change_in_nwc: float
    free_cash_flow: float


def prepare_inputs(values: Dict[str, Any]) -> Dict[str, Any]:
    """Merge overrides with defaults and ensure numeric types."""

    data: Dict[str, Any] = {**DEFAULT_INPUTS}
    for key, value in values.items():
        if key not in data:
            continue
        default_value = data[key]
        if isinstance(default_value, (int, float)):
            try:
                data[key] = float(value)
            except (TypeError, ValueError):
                continue
        else:
            data[key] = value
    data["projection_years"] = int(max(1, round(data.get("projection_years", 5))))
    return data


def build_projection(inputs: Dict[str, Any]) -> List[ProjectionYear]:
    """Project unlevered free cash flows over the model horizon."""

    years: List[ProjectionYear] = []
    revenue = float(inputs["revenue"])
    growth = float(inputs["revenue_growth_rate"])
    ebitda_margin = float(inputs["ebitda_margin"])
    depreciation_pct = float(inputs["depreciation_pct"])
    capex_pct = float(inputs["capex_pct"])
    nwc_pct = float(inputs["nwc_pct_of_revenue"])
    tax_rate = float(inputs["tax_rate"])
    projection_years = int(inputs["projection_years"])

    prior_nwc = revenue * nwc_pct

    for i in range(1, projection_years + 1):
        revenue = revenue * (1 + growth)
        ebitda = revenue * ebitda_margin
        depreciation = revenue * depreciation_pct
        ebit = ebitda - depreciation
        taxes = max(0.0, ebit) * tax_rate
        nopat = ebit - taxes
        capex = revenue * capex_pct
        nwc = revenue * nwc_pct
        change_in_nwc = nwc - prior_nwc
        fcf = nopat + depreciation - capex - change_in_nwc

        years.append(
            ProjectionYear(
                year=int(inputs["base_year"]) + i,
                revenue=revenue,
                ebitda=ebitda,
                depreciation=depreciation,
                ebit=ebit,
                taxes=taxes,
                nopat=nopat,
                capex=capex,
                change_in_nwc=change_in_nwc,
                free_cash_flow=fcf,
            )
        )

        prior_nwc = nwc

    return years


def compute_valuation(inputs: Dict[str, Any], projection: List[ProjectionYear]) -> Dict[str, Any]:
    """Discount projected cash flows and compute equity value."""

    discount_rate = float(inputs["discount_rate"])
    terminal_growth = float(inputs["terminal_growth_rate"])
    net_debt = float(inputs["net_debt"])
    shares = max(1.0, float(inputs["shares_outstanding"]))

    pv_cash_flows: List[float] = []
    present_value = 0.0

    for idx, year in enumerate(projection, start=1):
        discount_factor = (1 + discount_rate) ** idx
        pv = year.free_cash_flow / discount_factor
        pv_cash_flows.append(pv)
        present_value += pv

    terminal_fcf = projection[-1].free_cash_flow * (1 + terminal_growth)
    terminal_value = terminal_fcf / max(discount_rate - terminal_growth, 1e-6)
    pv_terminal = terminal_value / ((1 + discount_rate) ** len(projection))

    enterprise_value = present_value + pv_terminal
    equity_value = enterprise_value - net_debt
    share_price = equity_value / shares

    return {
        "pv_cash_flows": pv_cash_flows,
        "present_value_flows": present_value,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "share_price": share_price,
        "implied_ev_ebitda": enterprise_value / max(projection[-1].ebitda, 1e-6),
    }


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _format_currency_m(value: float) -> str:
    return f"${value/1_000_000:,.2f}M"


def _format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def build_report_tables(
    inputs: Dict[str, Any], projection: List[ProjectionYear], valuation: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Construct tables mirroring the Excel workbook outputs."""

    overview_rows = [
        {"Field": "Company", "Value": inputs["company_name"]},
        {"Field": "Analyst", "Value": inputs.get("analyst", "")},
        {"Field": "Base Year", "Value": int(inputs["base_year"])},
        {"Field": "Projection Horizon", "Value": f"{int(inputs['projection_years'])} years"},
    ]

    valuation_metrics = {
        "Enterprise Value": _format_currency(valuation["enterprise_value"]),
        "Equity Value": _format_currency(valuation["equity_value"]),
        "Implied Share Price": _format_currency(valuation["share_price"]),
        "PV of FCF": _format_currency(valuation["present_value_flows"]),
        "PV of Terminal Value": _format_currency(valuation["pv_terminal_value"]),
        "Terminal Value": _format_currency(valuation["terminal_value"]),
        "Implied EV/EBITDA": f"{valuation['implied_ev_ebitda']:.2f}x",
    }

    projection_rows = [
        {
            "Year": year.year,
            "Revenue": _format_currency(year.revenue),
            "EBITDA": _format_currency(year.ebitda),
            "EBIT": _format_currency(year.ebit),
            "NOPAT": _format_currency(year.nopat),
            "Free Cash Flow": _format_currency(year.free_cash_flow),
        }
        for year in projection
    ]

    discount_rows = []
    for idx, (year, pv) in enumerate(zip(projection, valuation["pv_cash_flows"]), start=1):
        discount_factor = (1 + inputs["discount_rate"]) ** idx
        discount_rows.append(
            {
                "Year": year.year,
                "Discount Factor": f"{1/discount_factor:.4f}",
                "FCF": _format_currency(year.free_cash_flow),
                "Present Value": _format_currency(pv),
            }
        )

    return [
        {"kind": "table", "title": "Company Overview", "columns": ["Field", "Value"], "rows": overview_rows},
        {"kind": "metrics", "title": "Valuation Summary", "metrics": valuation_metrics},
        {
            "kind": "table",
            "title": "Projected Free Cash Flows",
            "columns": ["Year", "Revenue", "EBITDA", "EBIT", "NOPAT", "Free Cash Flow"],
            "rows": projection_rows,
        },
        {
            "kind": "table",
            "title": "Discounting Detail",
            "columns": ["Year", "Discount Factor", "FCF", "Present Value"],
            "rows": discount_rows,
        },
    ]


def build_chart_specs(
    inputs: Dict[str, Any], projection: List[ProjectionYear], valuation: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Return chart configurations for the client UI."""

    years = [str(year.year) for year in projection]
    revenue = [round(year.revenue / 1_000_000, 2) for year in projection]
    ebitda = [round(year.ebitda / 1_000_000, 2) for year in projection]
    fcf = [round(year.free_cash_flow / 1_000_000, 2) for year in projection]

    pv_series = [round(pv / 1_000_000, 2) for pv in valuation["pv_cash_flows"]]
    pv_series[-1] += round(valuation["pv_terminal_value"] / 1_000_000, 2)

    return [
        {
            "key": "revenue_stack",
            "title": "Revenue, EBITDA & Free Cash Flow",
            "type": "line",
            "labels": years,
            "datasets": {
                "Revenue ($MM)": revenue,
                "EBITDA ($MM)": ebitda,
                "FCF ($MM)": fcf,
            },
            "y_label": "Millions of USD",
        },
        {
            "key": "discount_curve",
            "title": "Present Value of Cash Flows",
            "type": "bar",
            "labels": years,
            "datasets": [
                {
                    "label": "PV of Cash Flow ($MM)",
                    "data": pv_series,
                }
            ],
            "y_label": "Millions of USD",
        },
    ]
