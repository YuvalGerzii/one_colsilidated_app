"""Cross-method valuation comparison workspace."""

from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List

from .dcf_model import (
    build_chart_specs as dcf_chart_specs,
    build_projection as dcf_build_projection,
    build_report_tables as dcf_tables,
    compute_valuation as dcf_compute_valuation,
    prepare_inputs as dcf_prepare_inputs,
)
from .lbo_model import (
    build_chart_specs as lbo_chart_specs,
    build_projection as lbo_build_projection,
    build_report_tables as lbo_tables,
    compute_valuation as lbo_compute_valuation,
    prepare_inputs as lbo_prepare_inputs,
)


DEFAULT_INPUTS: Dict[str, Any] = {
    "company_name": "SampleCo Holdings",
    "analyst": "Finance Team",
    "base_year": 2023,
    "dcf_revenue": 180_000_000.0,
    "dcf_revenue_growth_rate": 0.08,
    "dcf_ebitda_margin": 0.24,
    "dcf_depreciation_pct": 0.03,
    "dcf_capex_pct": 0.04,
    "dcf_nwc_pct_of_revenue": 0.02,
    "dcf_tax_rate": 0.25,
    "dcf_discount_rate": 0.095,
    "dcf_terminal_growth_rate": 0.025,
    "dcf_projection_years": 5,
    "dcf_net_debt": 45_000_000.0,
    "dcf_shares_outstanding": 26_000_000.0,
    "lbo_revenue_growth_rate": 0.07,
    "lbo_ebitda_margin": 0.23,
    "lbo_depreciation_pct": 0.03,
    "lbo_capex_pct": 0.035,
    "lbo_nwc_pct_of_revenue": 0.02,
    "lbo_tax_rate": 0.25,
    "lbo_entry_multiple": 10.0,
    "lbo_exit_multiple": 11.0,
    "lbo_debt_percentage": 0.55,
    "lbo_interest_rate": 0.07,
    "lbo_amortization_years": 5,
    "lbo_purchase_fees_pct": 0.02,
    "lbo_exit_fees_pct": 0.01,
    "company_revenue": 180_000_000.0,
    "company_ebitda": 41_000_000.0,
    "company_earnings": 21_500_000.0,
    "net_debt": 45_000_000.0,
    "shares_outstanding": 26_000_000.0,
    "peer1_name": "Peer A",
    "peer1_ev_ebitda": 9.5,
    "peer1_ev_sales": 2.3,
    "peer2_name": "Peer B",
    "peer2_ev_ebitda": 10.2,
    "peer2_ev_sales": 2.6,
    "peer3_name": "Peer C",
    "peer3_ev_ebitda": 9.8,
    "peer3_ev_sales": 2.4,
    "precedent_ev_ebitda": 11.5,
    "precedent_ev_sales": 2.9,
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
        "name": "company_revenue",
        "label": "Latest Revenue ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "Company Metrics",
    },
    {
        "name": "company_ebitda",
        "label": "Latest EBITDA ($)",
        "type": "number",
        "step": 500_000,
        "section": "Company Metrics",
    },
    {
        "name": "company_earnings",
        "label": "Net Income ($)",
        "type": "number",
        "step": 500_000,
        "section": "Company Metrics",
    },
    {
        "name": "net_debt",
        "label": "Net Debt ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "Company Metrics",
    },
    {
        "name": "shares_outstanding",
        "label": "Diluted Shares",
        "type": "number",
        "step": 100_000,
        "section": "Company Metrics",
    },
    # DCF Fields
    {
        "name": "dcf_revenue",
        "label": "Base Revenue for DCF ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_revenue_growth_rate",
        "label": "Revenue Growth",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_ebitda_margin",
        "label": "EBITDA Margin",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_depreciation_pct",
        "label": "Depreciation (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_capex_pct",
        "label": "Capex (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_nwc_pct_of_revenue",
        "label": "NWC (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_tax_rate",
        "label": "Tax Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_discount_rate",
        "label": "Discount Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_terminal_growth_rate",
        "label": "Terminal Growth",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_projection_years",
        "label": "Projection Years",
        "type": "number",
        "step": 1,
        "min": 3,
        "max": 10,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_net_debt",
        "label": "Net Debt for DCF ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "DCF Inputs",
    },
    {
        "name": "dcf_shares_outstanding",
        "label": "Shares for DCF",
        "type": "number",
        "step": 100_000,
        "section": "DCF Inputs",
    },
    # LBO Fields
    {
        "name": "lbo_revenue_growth_rate",
        "label": "Revenue Growth",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_ebitda_margin",
        "label": "EBITDA Margin",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_depreciation_pct",
        "label": "Depreciation (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_capex_pct",
        "label": "Capex (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_nwc_pct_of_revenue",
        "label": "NWC (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_tax_rate",
        "label": "Tax Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_entry_multiple",
        "label": "Entry EV/EBITDA",
        "type": "number",
        "step": 0.25,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_exit_multiple",
        "label": "Exit EV/EBITDA",
        "type": "number",
        "step": 0.25,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_debt_percentage",
        "label": "Debt (% of EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_interest_rate",
        "label": "Interest Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_amortization_years",
        "label": "Amortization (years)",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 7,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_purchase_fees_pct",
        "label": "Purchase Fees (% of EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "LBO Inputs",
    },
    {
        "name": "lbo_exit_fees_pct",
        "label": "Exit Fees (% of EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "LBO Inputs",
    },
    # Comparables
    {
        "name": "peer1_name",
        "label": "Peer 1 Name",
        "type": "text",
        "section": "Trading Comps",
    },
    {
        "name": "peer1_ev_ebitda",
        "label": "Peer 1 EV/EBITDA",
        "type": "number",
        "step": 0.1,
        "section": "Trading Comps",
    },
    {
        "name": "peer1_ev_sales",
        "label": "Peer 1 EV/Sales",
        "type": "number",
        "step": 0.05,
        "section": "Trading Comps",
    },
    {
        "name": "peer2_name",
        "label": "Peer 2 Name",
        "type": "text",
        "section": "Trading Comps",
    },
    {
        "name": "peer2_ev_ebitda",
        "label": "Peer 2 EV/EBITDA",
        "type": "number",
        "step": 0.1,
        "section": "Trading Comps",
    },
    {
        "name": "peer2_ev_sales",
        "label": "Peer 2 EV/Sales",
        "type": "number",
        "step": 0.05,
        "section": "Trading Comps",
    },
    {
        "name": "peer3_name",
        "label": "Peer 3 Name",
        "type": "text",
        "section": "Trading Comps",
    },
    {
        "name": "peer3_ev_ebitda",
        "label": "Peer 3 EV/EBITDA",
        "type": "number",
        "step": 0.1,
        "section": "Trading Comps",
    },
    {
        "name": "peer3_ev_sales",
        "label": "Peer 3 EV/Sales",
        "type": "number",
        "step": 0.05,
        "section": "Trading Comps",
    },
    {
        "name": "precedent_ev_ebitda",
        "label": "Precedent EV/EBITDA",
        "type": "number",
        "step": 0.1,
        "section": "Trading Comps",
    },
    {
        "name": "precedent_ev_sales",
        "label": "Precedent EV/Sales",
        "type": "number",
        "step": 0.05,
        "section": "Trading Comps",
    },
]


def prepare_inputs(values: Dict[str, Any]) -> Dict[str, Any]:
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
    return data


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def _format_multiple(value: float) -> str:
    return f"{value:.2f}x"


def _parse_currency(value: Any) -> float:
    try:
        return float(str(value).replace("$", "").replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def _safe_mean(values: List[float]) -> float:
    filtered = [value for value in values if value not in (None, 0, 0.0)]
    if not filtered:
        return 0.0
    return mean(filtered)


def run_comparison(values: Dict[str, Any]) -> Dict[str, Any]:
    inputs = prepare_inputs(values)

    dcf_inputs = dcf_prepare_inputs(
        {
            "company_name": inputs["company_name"],
            "analyst": inputs.get("analyst", ""),
            "base_year": inputs["base_year"],
            "revenue": inputs["dcf_revenue"],
            "revenue_growth_rate": inputs["dcf_revenue_growth_rate"],
            "ebitda_margin": inputs["dcf_ebitda_margin"],
            "depreciation_pct": inputs["dcf_depreciation_pct"],
            "capex_pct": inputs["dcf_capex_pct"],
            "nwc_pct_of_revenue": inputs["dcf_nwc_pct_of_revenue"],
            "tax_rate": inputs["dcf_tax_rate"],
            "discount_rate": inputs["dcf_discount_rate"],
            "terminal_growth_rate": inputs["dcf_terminal_growth_rate"],
            "projection_years": inputs["dcf_projection_years"],
            "net_debt": inputs["dcf_net_debt"],
            "shares_outstanding": inputs["dcf_shares_outstanding"],
        }
    )
    dcf_projection = dcf_build_projection(dcf_inputs)
    dcf_valuation = dcf_compute_valuation(dcf_inputs, dcf_projection)

    lbo_inputs = lbo_prepare_inputs(
        {
            "company_name": inputs["company_name"],
            "analyst": inputs.get("analyst", ""),
            "base_year": inputs["base_year"],
            "revenue": inputs["company_revenue"],
            "revenue_growth_rate": inputs["lbo_revenue_growth_rate"],
            "ebitda_margin": inputs["lbo_ebitda_margin"],
            "depreciation_pct": inputs["lbo_depreciation_pct"],
            "capex_pct": inputs["lbo_capex_pct"],
            "nwc_pct_of_revenue": inputs["lbo_nwc_pct_of_revenue"],
            "tax_rate": inputs["lbo_tax_rate"],
            "entry_multiple": inputs["lbo_entry_multiple"],
            "exit_multiple": inputs["lbo_exit_multiple"],
            "debt_percentage": inputs["lbo_debt_percentage"],
            "interest_rate": inputs["lbo_interest_rate"],
            "amortization_years": inputs["lbo_amortization_years"],
            "purchase_fees_pct": inputs["lbo_purchase_fees_pct"],
            "exit_fees_pct": inputs["lbo_exit_fees_pct"],
        }
    )
    lbo_schedule = lbo_build_projection(lbo_inputs)
    lbo_valuation = lbo_compute_valuation(lbo_inputs, lbo_schedule)

    peers = [
        {
            "name": inputs.get("peer1_name", "Peer 1"),
            "ev_ebitda": inputs.get("peer1_ev_ebitda", 0.0),
            "ev_sales": inputs.get("peer1_ev_sales", 0.0),
        },
        {
            "name": inputs.get("peer2_name", "Peer 2"),
            "ev_ebitda": inputs.get("peer2_ev_ebitda", 0.0),
            "ev_sales": inputs.get("peer2_ev_sales", 0.0),
        },
        {
            "name": inputs.get("peer3_name", "Peer 3"),
            "ev_ebitda": inputs.get("peer3_ev_ebitda", 0.0),
            "ev_sales": inputs.get("peer3_ev_sales", 0.0),
        },
    ]

    avg_ev_ebitda = _safe_mean([peer["ev_ebitda"] for peer in peers])
    avg_ev_sales = _safe_mean([peer["ev_sales"] for peer in peers])

    trading_ev_from_ebitda = avg_ev_ebitda * inputs["company_ebitda"]
    trading_ev_from_sales = avg_ev_sales * inputs["company_revenue"]
    trading_ev = _safe_mean([trading_ev_from_ebitda, trading_ev_from_sales])
    trading_equity = trading_ev - inputs["net_debt"]
    trading_share_price = trading_equity / max(inputs["shares_outstanding"], 1.0)

    precedent_ev_from_ebitda = inputs["precedent_ev_ebitda"] * inputs["company_ebitda"]
    precedent_ev_from_sales = inputs["precedent_ev_sales"] * inputs["company_revenue"]
    precedent_ev = _safe_mean([precedent_ev_from_ebitda, precedent_ev_from_sales])
    precedent_equity = precedent_ev - inputs["net_debt"]
    precedent_share_price = precedent_equity / max(inputs["shares_outstanding"], 1.0)

    valuation_summary = [
        {
            "Method": "Discounted Cash Flow",
            "Enterprise Value": _format_currency(dcf_valuation["enterprise_value"]),
            "Equity Value": _format_currency(dcf_valuation["equity_value"]),
            "Share Price": _format_currency(dcf_valuation["share_price"]),
        },
        {
            "Method": "Leveraged Buyout",
            "Enterprise Value": _format_currency(lbo_valuation["exit_ev"]),
            "Equity Value": _format_currency(lbo_valuation["exit_equity_value"]),
            "Share Price": _format_currency(
                lbo_valuation["exit_equity_value"] / max(inputs["shares_outstanding"], 1.0)
            ),
        },
        {
            "Method": "Trading Comps",
            "Enterprise Value": _format_currency(trading_ev),
            "Equity Value": _format_currency(trading_equity),
            "Share Price": _format_currency(trading_share_price),
        },
        {
            "Method": "Precedent Transactions",
            "Enterprise Value": _format_currency(precedent_ev),
            "Equity Value": _format_currency(precedent_equity),
            "Share Price": _format_currency(precedent_share_price),
        },
    ]

    peer_rows = [
        {
            "Company": peer["name"],
            "EV/EBITDA": _format_multiple(peer["ev_ebitda"]),
            "EV/Sales": _format_multiple(peer["ev_sales"]),
        }
        for peer in peers
    ]
    peer_rows.append(
        {
            "Company": "Average",
            "EV/EBITDA": _format_multiple(avg_ev_ebitda),
            "EV/Sales": _format_multiple(avg_ev_sales),
        }
    )

    summary_metrics = {
        "DCF Share Price": _format_currency(dcf_valuation["share_price"]),
        "LBO Equity IRR": _format_percentage(lbo_valuation["irr"]),
        "Trading Share Price": _format_currency(trading_share_price),
        "Precedent Share Price": _format_currency(precedent_share_price),
        "DCF EV/EBITDA": _format_multiple(dcf_valuation["implied_ev_ebitda"]),
        "Exit Equity Value": _format_currency(lbo_valuation["exit_equity_value"]),
    }

    tables = [
        {
            "kind": "table",
            "title": "Company Overview",
            "columns": ["Field", "Value"],
            "rows": [
                {"Field": "Company", "Value": inputs["company_name"]},
                {"Field": "Analyst", "Value": inputs.get("analyst", "")},
                {"Field": "Revenue", "Value": _format_currency(inputs["company_revenue"])},
                {"Field": "EBITDA", "Value": _format_currency(inputs["company_ebitda"])},
                {"Field": "Net Income", "Value": _format_currency(inputs["company_earnings"])},
                {"Field": "Shares", "Value": f"{inputs['shares_outstanding']:,}"},
            ],
        },
        {"kind": "metrics", "title": "Valuation Highlights", "metrics": summary_metrics},
        {
            "kind": "table",
            "title": "Valuation Summary",
            "columns": ["Method", "Enterprise Value", "Equity Value", "Share Price"],
            "rows": valuation_summary,
        },
        {
            "kind": "table",
            "title": "Trading Comparables",
            "columns": ["Company", "EV/EBITDA", "EV/Sales"],
            "rows": peer_rows,
        },
    ]

    share_price_chart = {
        "key": "share_price_methods",
        "title": "Share Price by Valuation Method",
        "type": "bar",
        "labels": [row["Method"] for row in valuation_summary],
        "datasets": [
            {
                "label": "Share Price ($)",
                "data": [round(_parse_currency(row["Share Price"]), 2) for row in valuation_summary],
            }
        ],
        "y_label": "USD per Share",
    }

    enterprise_value_chart = {
        "key": "enterprise_value_methods",
        "title": "Enterprise Value Comparison",
        "type": "bar",
        "labels": [row["Method"] for row in valuation_summary],
        "datasets": [
            {
                "label": "Enterprise Value ($MM)",
                "data": [round(_parse_currency(row["Enterprise Value"]) / 1_000_000, 2) for row in valuation_summary],
            }
        ],
        "y_label": "Millions",
    }

    charts = [share_price_chart, enterprise_value_chart]

    return {
        "tables": tables,
        "charts": charts,
        "dcf": {
            "tables": dcf_tables(dcf_inputs, dcf_projection, dcf_valuation),
            "charts": dcf_chart_specs(dcf_inputs, dcf_projection, dcf_valuation),
        },
        "lbo": {
            "tables": lbo_tables(lbo_inputs, lbo_schedule, lbo_valuation),
            "charts": lbo_chart_specs(lbo_inputs, lbo_schedule, lbo_valuation),
        },
    }


def build_report_tables(values: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = run_comparison(values)
    return result["tables"]


def build_chart_specs(values: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = run_comparison(values)
    return result["charts"]
