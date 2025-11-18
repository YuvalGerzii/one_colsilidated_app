"""Leveraged buyout model used by the corporate finance workspace."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


DEFAULT_INPUTS: Dict[str, Any] = {
    "company_name": "SampleCo Holdings",
    "analyst": "Finance Team",
    "base_year": 2023,
    "revenue": 180_000_000.0,
    "revenue_growth_rate": 0.07,
    "ebitda_margin": 0.23,
    "depreciation_pct": 0.03,
    "capex_pct": 0.035,
    "nwc_pct_of_revenue": 0.02,
    "tax_rate": 0.25,
    "entry_multiple": 10.0,
    "exit_multiple": 11.0,
    "debt_percentage": 0.55,
    "interest_rate": 0.07,
    "amortization_years": 5,
    "purchase_fees_pct": 0.02,
    "exit_fees_pct": 0.01,
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
        "name": "revenue",
        "label": "Base Revenue ($)",
        "type": "number",
        "step": 1_000_000,
        "section": "Operating Assumptions",
    },
    {
        "name": "revenue_growth_rate",
        "label": "Revenue Growth",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "Operating Assumptions",
    },
    {
        "name": "ebitda_margin",
        "label": "EBITDA Margin",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "Operating Assumptions",
    },
    {
        "name": "depreciation_pct",
        "label": "Depreciation (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "Operating Assumptions",
    },
    {
        "name": "capex_pct",
        "label": "Capex (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "Operating Assumptions",
    },
    {
        "name": "nwc_pct_of_revenue",
        "label": "Net Working Capital (% of Revenue)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "Operating Assumptions",
    },
    {
        "name": "tax_rate",
        "label": "Tax Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "Operating Assumptions",
    },
    {
        "name": "entry_multiple",
        "label": "Entry EV/EBITDA",
        "type": "number",
        "step": 0.25,
        "min": 1,
        "section": "Valuation Assumptions",
    },
    {
        "name": "exit_multiple",
        "label": "Exit EV/EBITDA",
        "type": "number",
        "step": 0.25,
        "min": 1,
        "section": "Valuation Assumptions",
    },
    {
        "name": "debt_percentage",
        "label": "Debt Financing (% of EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "Capital Structure",
    },
    {
        "name": "interest_rate",
        "label": "Cash Interest Rate",
        "type": "number",
        "format": "percentage",
        "step": 0.1,
        "section": "Capital Structure",
    },
    {
        "name": "amortization_years",
        "label": "Debt Amortization (years)",
        "type": "number",
        "step": 1,
        "min": 1,
        "max": 7,
        "section": "Capital Structure",
    },
    {
        "name": "purchase_fees_pct",
        "label": "Acquisition Fees (% of EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "Fees & Leakage",
    },
    {
        "name": "exit_fees_pct",
        "label": "Exit Fees (% of Exit EV)",
        "type": "number",
        "format": "percentage",
        "step": 0.05,
        "section": "Fees & Leakage",
    },
]


@dataclass
class LBOYear:
    year: int
    revenue: float
    ebitda: float
    depreciation: float
    ebit: float
    taxes: float
    capex: float
    change_in_nwc: float
    free_cash_flow: float
    interest: float
    principal_payment: float
    ending_debt: float
    cash_to_equity: float


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
    data["amortization_years"] = int(max(1, round(data.get("amortization_years", 5))))
    return data


def build_projection(inputs: Dict[str, Any]) -> List[LBOYear]:
    revenue = float(inputs["revenue"])
    growth = float(inputs["revenue_growth_rate"])
    ebitda_margin = float(inputs["ebitda_margin"])
    depreciation_pct = float(inputs["depreciation_pct"])
    capex_pct = float(inputs["capex_pct"])
    nwc_pct = float(inputs["nwc_pct_of_revenue"])
    tax_rate = float(inputs["tax_rate"])
    entry_multiple = float(inputs["entry_multiple"])
    debt_pct = float(inputs["debt_percentage"])
    interest_rate = float(inputs["interest_rate"])
    amort_years = int(inputs["amortization_years"])
    purchase_fees_pct = float(inputs["purchase_fees_pct"])

    base_ebitda = revenue * ebitda_margin
    enterprise_value = base_ebitda * entry_multiple
    debt = enterprise_value * debt_pct
    equity = enterprise_value - debt
    fees = enterprise_value * purchase_fees_pct
    initial_equity = equity + fees

    nwc_prior = revenue * nwc_pct

    schedule: List[LBOYear] = []
    remaining_debt = debt
    for i in range(1, 6):
        revenue = revenue * (1 + growth)
        ebitda = revenue * ebitda_margin
        depreciation = revenue * depreciation_pct
        ebit = ebitda - depreciation
        taxes = max(0.0, ebit) * tax_rate
        capex = revenue * capex_pct
        nwc = revenue * nwc_pct
        change_in_nwc = nwc - nwc_prior
        fcf = ebitda - taxes - capex - change_in_nwc

        interest = remaining_debt * interest_rate
        scheduled_principal = debt / amort_years
        principal_payment = min(remaining_debt, scheduled_principal)
        cash_to_equity = fcf - interest - principal_payment
        remaining_debt = max(0.0, remaining_debt - principal_payment)

        schedule.append(
            LBOYear(
                year=int(inputs["base_year"]) + i,
                revenue=revenue,
                ebitda=ebitda,
                depreciation=depreciation,
                ebit=ebit,
                taxes=taxes,
                capex=capex,
                change_in_nwc=change_in_nwc,
                free_cash_flow=fcf,
                interest=interest,
                principal_payment=principal_payment,
                ending_debt=remaining_debt,
                cash_to_equity=cash_to_equity,
            )
        )

        nwc_prior = nwc

    return schedule


def _irr(cash_flows: List[float], guess: float = 0.15) -> float:
    rate = guess
    for _ in range(100):
        npv = 0.0
        d_npv = 0.0
        for t, cash in enumerate(cash_flows):
            denom = (1 + rate) ** t
            npv += cash / denom
            if t > 0:
                d_npv -= t * cash / ((1 + rate) ** (t + 1))
        if abs(d_npv) < 1e-9:
            break
        new_rate = rate - npv / d_npv
        if abs(new_rate - rate) < 1e-7:
            return max(-0.9999, new_rate)
        rate = new_rate
    return max(-0.9999, rate)


def compute_valuation(inputs: Dict[str, Any], schedule: List[LBOYear]) -> Dict[str, Any]:
    entry_multiple = float(inputs["entry_multiple"])
    exit_multiple = float(inputs["exit_multiple"])
    exit_fees_pct = float(inputs["exit_fees_pct"])
    debt_pct = float(inputs["debt_percentage"])
    purchase_fees_pct = float(inputs["purchase_fees_pct"])

    base_ebitda = float(inputs["revenue"]) * float(inputs["ebitda_margin"])
    entry_ev = base_ebitda * entry_multiple
    initial_debt = entry_ev * debt_pct
    equity = entry_ev - initial_debt
    fees = entry_ev * purchase_fees_pct
    initial_equity_outlay = equity + fees

    final_year = schedule[-1]
    exit_ev = final_year.ebitda * exit_multiple
    exit_fees = exit_ev * exit_fees_pct
    equity_value_at_exit = exit_ev - final_year.ending_debt - exit_fees

    cash_flows = [-initial_equity_outlay]
    cumulative_cash = -initial_equity_outlay
    for year in schedule:
        cash_flows.append(year.cash_to_equity)
        cumulative_cash += year.cash_to_equity
    cash_flows[-1] += equity_value_at_exit
    cumulative_cash += equity_value_at_exit

    irr = _irr(cash_flows)
    total_distributions = sum(cash_flows[1:])
    moic = total_distributions / max(initial_equity_outlay, 1.0)

    return {
        "entry_ev": entry_ev,
        "initial_debt": initial_debt,
        "initial_equity": initial_equity_outlay,
        "exit_ev": exit_ev,
        "exit_equity_value": equity_value_at_exit,
        "cash_flows": cash_flows,
        "irr": irr,
        "moic": moic,
    }


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _format_percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def build_report_tables(inputs: Dict[str, Any], schedule: List[LBOYear], valuation: Dict[str, Any]) -> List[Dict[str, Any]]:
    overview_rows = [
        {"Field": "Company", "Value": inputs["company_name"]},
        {"Field": "Analyst", "Value": inputs.get("analyst", "")},
        {"Field": "Entry EV/EBITDA", "Value": f"{inputs['entry_multiple']:.2f}x"},
        {"Field": "Exit EV/EBITDA", "Value": f"{inputs['exit_multiple']:.2f}x"},
        {"Field": "Leverage", "Value": _format_percentage(inputs["debt_percentage"])},
    ]

    valuation_metrics = {
        "Entry Enterprise Value": _format_currency(valuation["entry_ev"]),
        "Equity Contribution": _format_currency(valuation["initial_equity"]),
        "Debt Financing": _format_currency(valuation["initial_debt"]),
        "Exit Enterprise Value": _format_currency(valuation["exit_ev"]),
        "Equity Value at Exit": _format_currency(valuation["exit_equity_value"]),
        "Gross IRR": _format_percentage(valuation["irr"]),
        "Equity MOIC": f"{valuation['moic']:.2f}x",
    }

    schedule_rows = [
        {
            "Year": year.year,
            "Revenue": _format_currency(year.revenue),
            "EBITDA": _format_currency(year.ebitda),
            "Interest": _format_currency(year.interest),
            "Principal": _format_currency(year.principal_payment),
            "Ending Debt": _format_currency(year.ending_debt),
            "Cash to Equity": _format_currency(year.cash_to_equity),
        }
        for year in schedule
    ]

    cash_flow_rows = []
    running_cf = -valuation["initial_equity"]
    cash_flow_rows.append(
        {
            "Period": "Close",
            "Cash Flow": _format_currency(-valuation["initial_equity"]),
            "Cumulative": _format_currency(running_cf),
        }
    )
    for year in schedule:
        running_cf += year.cash_to_equity
        cash_flow_rows.append(
            {
                "Period": year.year,
                "Cash Flow": _format_currency(year.cash_to_equity),
                "Cumulative": _format_currency(running_cf),
            }
        )
    running_cf += valuation["exit_equity_value"]
    cash_flow_rows.append(
        {
            "Period": "Exit",
            "Cash Flow": _format_currency(valuation["exit_equity_value"]),
            "Cumulative": _format_currency(running_cf),
        }
    )

    return [
        {"kind": "table", "title": "Deal Overview", "columns": ["Field", "Value"], "rows": overview_rows},
        {"kind": "metrics", "title": "Equity Returns", "metrics": valuation_metrics},
        {
            "kind": "table",
            "title": "Operating & Debt Schedule",
            "columns": ["Year", "Revenue", "EBITDA", "Interest", "Principal", "Ending Debt", "Cash to Equity"],
            "rows": schedule_rows,
        },
        {
            "kind": "table",
            "title": "Equity Cash Flow Bridge",
            "columns": ["Period", "Cash Flow", "Cumulative"],
            "rows": cash_flow_rows,
        },
    ]


def build_chart_specs(inputs: Dict[str, Any], schedule: List[LBOYear], valuation: Dict[str, Any]) -> List[Dict[str, Any]]:
    years = [str(year.year) for year in schedule]
    debt_balance = [round(year.ending_debt / 1_000_000, 2) for year in schedule]
    ebitda = [round(year.ebitda / 1_000_000, 2) for year in schedule]
    cash_equity = [round(year.cash_to_equity / 1_000_000, 2) for year in schedule]

    irr = valuation["irr"]
    moic = valuation["moic"]

    return [
        {
            "key": "debt_vs_ebitda",
            "title": "Debt Paydown vs EBITDA",
            "type": "line",
            "labels": years,
            "datasets": {
                "Ending Debt ($MM)": debt_balance,
                "EBITDA ($MM)": ebitda,
            },
            "y_label": "Millions of USD",
        },
        {
            "key": "equity_cashflows",
            "title": "Annual Cash Flows to Equity",
            "type": "bar",
            "labels": years,
            "datasets": [
                {
                    "label": "Cash to Equity ($MM)",
                    "data": cash_equity,
                }
            ],
            "y_label": "Millions of USD",
        },
        {
            "key": "returns_summary",
            "title": "Equity Returns Snapshot",
            "type": "bar",
            "labels": ["Gross IRR", "Equity MOIC"],
            "datasets": [
                {
                    "label": "Performance",
                    "data": [round(irr * 100, 2), round(moic, 2)],
                }
            ],
            "y_label": "% / Multiple",
        },
    ]
