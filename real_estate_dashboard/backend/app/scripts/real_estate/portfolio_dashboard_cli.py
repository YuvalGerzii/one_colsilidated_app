"""
Multi-Property Portfolio Dashboard
Comprehensive portfolio analytics, diversification analysis, and performance tracking
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
import json
from collections import defaultdict

DEFAULT_INPUTS: Dict[str, Any] = {
    "portfolio_name": "Sample Real Estate Portfolio",
    "owner": "Portfolio Manager",
    "analysis_date": "2025-01-01",

    # Portfolio Properties
    "properties": [
        {
            "id": "prop_1",
            "name": "Sunset Apartments",
            "type": "Multifamily",
            "location": "Miami, FL",
            "market": "Miami Metro",
            "acquisition_date": "2020-06-15",
            "purchase_price": 2500000,
            "current_value": 3000000,
            "debt_balance": 1800000,
            "annual_noi": 225000,
            "annual_debt_service": 135000,
            "cap_rate": 0.075,
            "occupancy_rate": 0.95,
            "lease_expiration_date": "2026-12-31",
            "interest_rate": 0.045,
            "rate_reset_date": "2027-06-15",
        },
        {
            "id": "prop_2",
            "name": "Downtown Office Tower",
            "type": "Commercial Office",
            "location": "Atlanta, GA",
            "market": "Atlanta CBD",
            "acquisition_date": "2019-03-20",
            "purchase_price": 5000000,
            "current_value": 5500000,
            "debt_balance": 3500000,
            "annual_noi": 440000,
            "annual_debt_service": 250000,
            "cap_rate": 0.080,
            "occupancy_rate": 0.88,
            "lease_expiration_date": "2025-06-30",
            "interest_rate": 0.050,
            "rate_reset_date": "2025-03-20",
        },
        {
            "id": "prop_3",
            "name": "Retail Plaza",
            "type": "Retail",
            "location": "Austin, TX",
            "market": "Austin Metro",
            "acquisition_date": "2021-09-10",
            "purchase_price": 3500000,
            "current_value": 4000000,
            "debt_balance": 2400000,
            "annual_noi": 320000,
            "annual_debt_service": 170000,
            "cap_rate": 0.080,
            "occupancy_rate": 0.92,
            "lease_expiration_date": "2027-09-30",
            "interest_rate": 0.048,
            "rate_reset_date": "2026-09-10",
        },
    ],

    # Portfolio Settings
    "target_cash_reserves": 500000,
    "rebalance_threshold": 0.10,  # Trigger rebalancing if allocation drifts >10%
    "min_property_allocation": 0.15,  # Min 15% per property
    "max_property_allocation": 0.40,  # Max 40% per property
    "alert_days_before_expiration": 90,
    "alert_days_before_rate_reset": 180,
}

FORM_FIELDS: List[Dict[str, Any]] = [
    # Portfolio Profile
    {
        "name": "portfolio_name",
        "label": "Portfolio Name",
        "type": "text",
        "section": "Portfolio Profile",
        "help": "Name for this portfolio"
    },
    {
        "name": "owner",
        "label": "Portfolio Owner/Manager",
        "type": "text",
        "section": "Portfolio Profile",
        "help": "Owner or manager name"
    },
    {
        "name": "analysis_date",
        "label": "Analysis Date",
        "type": "date",
        "section": "Portfolio Profile",
        "help": "Date of analysis (YYYY-MM-DD)"
    },

    # Portfolio Settings
    {
        "name": "target_cash_reserves",
        "label": "Target Cash Reserves ($)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Target cash reserves for the portfolio"
    },
    {
        "name": "rebalance_threshold",
        "label": "Rebalancing Threshold (%)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Trigger rebalancing if allocation drifts beyond this percentage"
    },
    {
        "name": "min_property_allocation",
        "label": "Min Property Allocation (%)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Minimum allocation per property"
    },
    {
        "name": "max_property_allocation",
        "label": "Max Property Allocation (%)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Maximum allocation per property"
    },
    {
        "name": "alert_days_before_expiration",
        "label": "Lease Expiration Alert (Days)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Alert this many days before lease expiration"
    },
    {
        "name": "alert_days_before_rate_reset",
        "label": "Rate Reset Alert (Days)",
        "type": "number",
        "section": "Portfolio Settings",
        "help": "Alert this many days before rate reset"
    },
]


def prepare_inputs(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare and validate inputs for portfolio calculations.
    """
    inputs = raw.copy()

    # Ensure percentages are decimals
    percentage_fields = [
        "rebalance_threshold", "min_property_allocation", "max_property_allocation"
    ]

    for field in percentage_fields:
        if field in inputs and inputs[field] > 1:
            inputs[field] = inputs[field] / 100.0

    # Parse analysis date
    if "analysis_date" in inputs and isinstance(inputs["analysis_date"], str):
        inputs["analysis_date"] = datetime.strptime(inputs["analysis_date"], "%Y-%m-%d")

    # Parse property dates
    if "properties" in inputs:
        for prop in inputs["properties"]:
            date_fields = ["acquisition_date", "lease_expiration_date", "rate_reset_date"]
            for field in date_fields:
                if field in prop and isinstance(prop[field], str):
                    prop[field] = datetime.strptime(prop[field], "%Y-%m-%d")

    return inputs


def calculate_consolidated_metrics(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate consolidated portfolio performance metrics.
    """
    properties = inputs.get("properties", [])

    # Aggregate values
    total_portfolio_value = sum(p["current_value"] for p in properties)
    total_debt = sum(p["debt_balance"] for p in properties)
    total_equity = total_portfolio_value - total_debt
    total_noi = sum(p["annual_noi"] for p in properties)
    total_debt_service = sum(p["annual_debt_service"] for p in properties)
    aggregate_cash_flow = total_noi - total_debt_service

    # Weighted average cap rate
    weighted_cap_rate = sum(
        p["cap_rate"] * (p["current_value"] / total_portfolio_value)
        for p in properties
    ) if total_portfolio_value > 0 else 0

    # Portfolio-wide IRR (simplified - based on cash flow and equity appreciation)
    total_purchase_price = sum(p["purchase_price"] for p in properties)
    total_appreciation = total_portfolio_value - total_purchase_price
    total_equity_invested = sum(p["purchase_price"] - p["debt_balance"] for p in properties)

    # Calculate holding period weighted average
    analysis_date = inputs.get("analysis_date", datetime.now())
    if isinstance(analysis_date, str):
        analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")

    total_years = 0
    for prop in properties:
        acq_date = prop.get("acquisition_date")
        if isinstance(acq_date, str):
            acq_date = datetime.strptime(acq_date, "%Y-%m-%d")
        years_held = (analysis_date - acq_date).days / 365.25
        total_years += years_held

    avg_years_held = total_years / len(properties) if properties else 1

    # Simple IRR approximation
    annual_return = aggregate_cash_flow + (total_appreciation / avg_years_held)
    portfolio_irr = annual_return / total_equity_invested if total_equity_invested > 0 else 0

    # Leverage metrics
    ltv_ratio = total_debt / total_portfolio_value if total_portfolio_value > 0 else 0
    debt_service_coverage = total_noi / total_debt_service if total_debt_service > 0 else 0

    # Occupancy metrics
    weighted_occupancy = sum(
        p["occupancy_rate"] * (p["current_value"] / total_portfolio_value)
        for p in properties
    ) if total_portfolio_value > 0 else 0

    return {
        "total_portfolio_value": total_portfolio_value,
        "total_debt": total_debt,
        "total_equity": total_equity,
        "total_noi": total_noi,
        "total_debt_service": total_debt_service,
        "aggregate_cash_flow": aggregate_cash_flow,
        "weighted_cap_rate": weighted_cap_rate,
        "portfolio_irr": portfolio_irr,
        "ltv_ratio": ltv_ratio,
        "debt_service_coverage": debt_service_coverage,
        "weighted_occupancy": weighted_occupancy,
        "num_properties": len(properties),
        "avg_years_held": avg_years_held,
    }


def calculate_property_comparison(inputs: Dict[str, Any], consolidated: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create property comparison matrix.
    """
    properties = inputs.get("properties", [])
    total_value = consolidated["total_portfolio_value"]

    comparison_matrix = []

    for prop in properties:
        equity = prop["current_value"] - prop["debt_balance"]
        cash_flow = prop["annual_noi"] - prop["annual_debt_service"]
        coc_return = cash_flow / equity if equity > 0 else 0
        appreciation = prop["current_value"] - prop["purchase_price"]
        appreciation_pct = appreciation / prop["purchase_price"] if prop["purchase_price"] > 0 else 0
        allocation = prop["current_value"] / total_value if total_value > 0 else 0

        # Calculate holding period
        acq_date = prop.get("acquisition_date")
        analysis_date = inputs.get("analysis_date", datetime.now())
        if isinstance(acq_date, str):
            acq_date = datetime.strptime(acq_date, "%Y-%m-%d")
        if isinstance(analysis_date, str):
            analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")
        years_held = (analysis_date - acq_date).days / 365.25

        comparison_matrix.append({
            "id": prop["id"],
            "name": prop["name"],
            "type": prop["type"],
            "location": prop["location"],
            "market": prop["market"],
            "current_value": prop["current_value"],
            "equity": equity,
            "debt_balance": prop["debt_balance"],
            "ltv": prop["debt_balance"] / prop["current_value"] if prop["current_value"] > 0 else 0,
            "annual_noi": prop["annual_noi"],
            "annual_cash_flow": cash_flow,
            "cap_rate": prop["cap_rate"],
            "coc_return": coc_return,
            "appreciation": appreciation,
            "appreciation_pct": appreciation_pct,
            "allocation": allocation,
            "occupancy_rate": prop["occupancy_rate"],
            "years_held": years_held,
        })

    return comparison_matrix


def calculate_correlation_analysis(inputs: Dict[str, Any], comparison: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze portfolio diversification and correlations.
    """
    properties = inputs.get("properties", [])

    # Diversification by property type
    type_allocation = defaultdict(float)
    for comp in comparison:
        type_allocation[comp["type"]] += comp["allocation"]

    # Diversification by market
    market_allocation = defaultdict(float)
    for comp in comparison:
        market_allocation[comp["market"]] += comp["allocation"]

    # Calculate concentration risk (Herfindahl-Hirschman Index)
    hhi_property = sum(comp["allocation"] ** 2 for comp in comparison)
    hhi_type = sum(alloc ** 2 for alloc in type_allocation.values())
    hhi_market = sum(alloc ** 2 for alloc in market_allocation.values())

    # Diversification score (0-100, higher is better)
    # HHI ranges from 1/n (perfectly diversified) to 1 (concentrated)
    n_properties = len(properties)
    min_hhi = 1 / n_properties if n_properties > 0 else 1
    diversification_score = (1 - ((hhi_property - min_hhi) / (1 - min_hhi))) * 100 if n_properties > 1 else 100

    # Risk assessment
    if hhi_property > 0.25:
        concentration_risk = "High"
    elif hhi_property > 0.15:
        concentration_risk = "Medium"
    else:
        concentration_risk = "Low"

    # Geographic diversification
    num_markets = len(market_allocation)
    geographic_diversity = "High" if num_markets >= 3 else ("Medium" if num_markets == 2 else "Low")

    # Asset type diversification
    num_types = len(type_allocation)
    asset_diversity = "High" if num_types >= 3 else ("Medium" if num_types == 2 else "Low")

    return {
        "type_allocation": dict(type_allocation),
        "market_allocation": dict(market_allocation),
        "hhi_property": hhi_property,
        "hhi_type": hhi_type,
        "hhi_market": hhi_market,
        "diversification_score": diversification_score,
        "concentration_risk": concentration_risk,
        "geographic_diversity": geographic_diversity,
        "asset_diversity": asset_diversity,
        "num_markets": num_markets,
        "num_property_types": num_types,
    }


def calculate_rebalancing_recommendations(inputs: Dict[str, Any], comparison: List[Dict[str, Any]], correlation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate portfolio rebalancing recommendations.
    """
    rebalance_threshold = inputs.get("rebalance_threshold", 0.10)
    min_allocation = inputs.get("min_property_allocation", 0.15)
    max_allocation = inputs.get("max_property_allocation", 0.40)

    # Ideal allocation (equal weight or based on strategy)
    num_properties = len(comparison)
    target_allocation = 1.0 / num_properties if num_properties > 0 else 0

    rebalancing_needed = False
    recommendations = []

    for comp in comparison:
        current_allocation = comp["allocation"]
        allocation_drift = abs(current_allocation - target_allocation)

        # Check if rebalancing is needed
        if allocation_drift > rebalance_threshold:
            rebalancing_needed = True
            action = "Reduce" if current_allocation > target_allocation else "Increase"
            target_change = (target_allocation - current_allocation) * comparison[0].get("current_value", 0)

            recommendations.append({
                "property_id": comp["id"],
                "property_name": comp["name"],
                "current_allocation": current_allocation,
                "target_allocation": target_allocation,
                "allocation_drift": allocation_drift,
                "action": action,
                "recommended_change": target_change,
                "priority": "High" if allocation_drift > rebalance_threshold * 2 else "Medium",
            })

        # Check allocation limits
        if current_allocation < min_allocation:
            recommendations.append({
                "property_id": comp["id"],
                "property_name": comp["name"],
                "current_allocation": current_allocation,
                "target_allocation": min_allocation,
                "allocation_drift": min_allocation - current_allocation,
                "action": "Increase",
                "recommended_change": (min_allocation - current_allocation) * comp["current_value"],
                "priority": "High",
                "reason": "Below minimum allocation threshold",
            })
            rebalancing_needed = True

        if current_allocation > max_allocation:
            recommendations.append({
                "property_id": comp["id"],
                "property_name": comp["name"],
                "current_allocation": current_allocation,
                "target_allocation": max_allocation,
                "allocation_drift": current_allocation - max_allocation,
                "action": "Reduce",
                "recommended_change": (current_allocation - max_allocation) * comp["current_value"],
                "priority": "High",
                "reason": "Exceeds maximum allocation threshold",
            })
            rebalancing_needed = True

    # Sort recommendations by priority and drift
    recommendations.sort(key=lambda x: (x.get("priority", "Low") == "Low", -x.get("allocation_drift", 0)))

    return {
        "rebalancing_needed": rebalancing_needed,
        "recommendations": recommendations,
        "num_recommendations": len(recommendations),
        "target_allocation": target_allocation,
    }


def calculate_alerts(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate alerts for lease expirations and rate resets.
    """
    properties = inputs.get("properties", [])
    analysis_date = inputs.get("analysis_date", datetime.now())
    if isinstance(analysis_date, str):
        analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")

    alert_days_expiration = inputs.get("alert_days_before_expiration", 90)
    alert_days_rate_reset = inputs.get("alert_days_before_rate_reset", 180)

    lease_alerts = []
    rate_reset_alerts = []

    for prop in properties:
        # Lease expiration alerts
        lease_exp = prop.get("lease_expiration_date")
        if isinstance(lease_exp, str):
            lease_exp = datetime.strptime(lease_exp, "%Y-%m-%d")

        if lease_exp:
            days_until_expiration = (lease_exp - analysis_date).days
            if 0 <= days_until_expiration <= alert_days_expiration:
                severity = "Critical" if days_until_expiration <= 30 else ("High" if days_until_expiration <= 60 else "Medium")
                lease_alerts.append({
                    "property_id": prop["id"],
                    "property_name": prop["name"],
                    "alert_type": "Lease Expiration",
                    "expiration_date": lease_exp.strftime("%Y-%m-%d"),
                    "days_until": days_until_expiration,
                    "severity": severity,
                    "action_required": f"Renew or find new tenant for {prop['name']}",
                })

        # Rate reset alerts
        rate_reset = prop.get("rate_reset_date")
        if isinstance(rate_reset, str):
            rate_reset = datetime.strptime(rate_reset, "%Y-%m-%d")

        if rate_reset:
            days_until_reset = (rate_reset - analysis_date).days
            if 0 <= days_until_reset <= alert_days_rate_reset:
                severity = "Critical" if days_until_reset <= 60 else ("High" if days_until_reset <= 120 else "Medium")
                rate_reset_alerts.append({
                    "property_id": prop["id"],
                    "property_name": prop["name"],
                    "alert_type": "Rate Reset",
                    "reset_date": rate_reset.strftime("%Y-%m-%d"),
                    "days_until": days_until_reset,
                    "current_rate": prop.get("interest_rate", 0),
                    "severity": severity,
                    "action_required": f"Review financing options for {prop['name']}",
                })

    # Combine all alerts
    all_alerts = lease_alerts + rate_reset_alerts
    all_alerts.sort(key=lambda x: x["days_until"])

    return {
        "lease_alerts": lease_alerts,
        "rate_reset_alerts": rate_reset_alerts,
        "all_alerts": all_alerts,
        "total_alerts": len(all_alerts),
        "critical_alerts": len([a for a in all_alerts if a["severity"] == "Critical"]),
        "high_alerts": len([a for a in all_alerts if a["severity"] == "High"]),
        "medium_alerts": len([a for a in all_alerts if a["severity"] == "Medium"]),
    }


def calculate_portfolio_dashboard(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main calculation function that orchestrates all portfolio dashboard calculations.
    """
    results = {
        "portfolio_name": inputs["portfolio_name"],
        "owner": inputs["owner"],
        "analysis_date": inputs.get("analysis_date", datetime.now()).strftime("%Y-%m-%d") if isinstance(inputs.get("analysis_date"), datetime) else inputs.get("analysis_date"),
    }

    # Consolidated Performance Metrics
    results["consolidated_metrics"] = calculate_consolidated_metrics(inputs)

    # Property Comparison Matrix
    results["property_comparison"] = calculate_property_comparison(inputs, results["consolidated_metrics"])

    # Correlation Analysis
    results["correlation_analysis"] = calculate_correlation_analysis(inputs, results["property_comparison"])

    # Rebalancing Recommendations
    results["rebalancing"] = calculate_rebalancing_recommendations(inputs, results["property_comparison"], results["correlation_analysis"])

    # Alerts
    results["alerts"] = calculate_alerts(inputs)

    return results


def build_report_tables(inputs: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build formatted tables for display.
    """
    tables = []

    # Portfolio Summary Table
    cm = results["consolidated_metrics"]
    summary_rows = [
        {"Metric": "Total Portfolio Value", "Value": f"${cm['total_portfolio_value']:,.0f}"},
        {"Metric": "Total Equity", "Value": f"${cm['total_equity']:,.0f}"},
        {"Metric": "Total Debt", "Value": f"${cm['total_debt']:,.0f}"},
        {"Metric": "LTV Ratio", "Value": f"{cm['ltv_ratio']:.1%}"},
        {"Metric": "Number of Properties", "Value": str(cm['num_properties'])},
        {"Metric": "Aggregate Annual NOI", "Value": f"${cm['total_noi']:,.0f}"},
        {"Metric": "Aggregate Annual Cash Flow", "Value": f"${cm['aggregate_cash_flow']:,.0f}"},
        {"Metric": "Weighted Avg Cap Rate", "Value": f"{cm['weighted_cap_rate']:.2%}"},
        {"Metric": "Portfolio IRR", "Value": f"{cm['portfolio_irr']:.2%}"},
        {"Metric": "Debt Service Coverage", "Value": f"{cm['debt_service_coverage']:.2f}x"},
        {"Metric": "Weighted Occupancy", "Value": f"{cm['weighted_occupancy']:.1%}"},
    ]
    tables.append({
        "title": "Portfolio Performance Summary",
        "rows": summary_rows,
        "columns": ["Metric", "Value"]
    })

    # Property Comparison Table
    comp_rows = []
    for prop in results["property_comparison"]:
        comp_rows.append({
            "Property": prop["name"],
            "Type": prop["type"],
            "Value": f"${prop['current_value']:,.0f}",
            "Allocation": f"{prop['allocation']:.1%}",
            "NOI": f"${prop['annual_noi']:,.0f}",
            "Cash Flow": f"${prop['annual_cash_flow']:,.0f}",
            "Cap Rate": f"{prop['cap_rate']:.2%}",
            "CoC Return": f"{prop['coc_return']:.2%}",
            "Occupancy": f"{prop['occupancy_rate']:.0%}",
        })
    tables.append({
        "title": "Property Comparison Matrix",
        "rows": comp_rows,
        "columns": ["Property", "Type", "Value", "Allocation", "NOI", "Cash Flow", "Cap Rate", "CoC Return", "Occupancy"]
    })

    # Diversification Analysis Table
    corr = results["correlation_analysis"]
    div_rows = [
        {"Metric": "Diversification Score", "Value": f"{corr['diversification_score']:.1f}/100"},
        {"Metric": "Concentration Risk", "Value": corr['concentration_risk']},
        {"Metric": "Geographic Diversity", "Value": corr['geographic_diversity']},
        {"Metric": "Asset Type Diversity", "Value": corr['asset_diversity']},
        {"Metric": "Number of Markets", "Value": str(corr['num_markets'])},
        {"Metric": "Number of Property Types", "Value": str(corr['num_property_types'])},
        {"Metric": "HHI (Property)", "Value": f"{corr['hhi_property']:.3f}"},
    ]
    tables.append({
        "title": "Diversification Analysis",
        "rows": div_rows,
        "columns": ["Metric", "Value"]
    })

    # Asset Type Allocation
    type_rows = []
    for asset_type, allocation in corr["type_allocation"].items():
        type_rows.append({
            "Asset Type": asset_type,
            "Allocation": f"{allocation:.1%}",
        })
    tables.append({
        "title": "Asset Type Allocation",
        "rows": type_rows,
        "columns": ["Asset Type", "Allocation"]
    })

    # Geographic Allocation
    market_rows = []
    for market, allocation in corr["market_allocation"].items():
        market_rows.append({
            "Market": market,
            "Allocation": f"{allocation:.1%}",
        })
    tables.append({
        "title": "Geographic Allocation",
        "rows": market_rows,
        "columns": ["Market", "Allocation"]
    })

    # Rebalancing Recommendations
    if results["rebalancing"]["rebalancing_needed"]:
        rebal_rows = []
        for rec in results["rebalancing"]["recommendations"]:
            rebal_rows.append({
                "Property": rec["property_name"],
                "Current": f"{rec['current_allocation']:.1%}",
                "Target": f"{rec['target_allocation']:.1%}",
                "Drift": f"{rec['allocation_drift']:.1%}",
                "Action": rec["action"],
                "Priority": rec["priority"],
            })
        tables.append({
            "title": "Rebalancing Recommendations",
            "rows": rebal_rows,
            "columns": ["Property", "Current", "Target", "Drift", "Action", "Priority"]
        })

    # Alerts Table
    if results["alerts"]["total_alerts"] > 0:
        alert_rows = []
        for alert in results["alerts"]["all_alerts"]:
            alert_rows.append({
                "Property": alert["property_name"],
                "Alert Type": alert["alert_type"],
                "Date": alert.get("expiration_date") or alert.get("reset_date"),
                "Days Until": str(alert["days_until"]),
                "Severity": alert["severity"],
                "Action": alert["action_required"],
            })
        tables.append({
            "title": "Active Alerts",
            "rows": alert_rows,
            "columns": ["Property", "Alert Type", "Date", "Days Until", "Severity", "Action"]
        })

    return tables


def build_chart_specs(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build chart specifications for visualizations.
    """
    charts = []

    # Portfolio Value Breakdown
    value_data = []
    for prop in results["property_comparison"]:
        value_data.append({
            "Property": prop["name"],
            "Value": prop["current_value"],
            "Equity": prop["equity"],
            "Debt": prop["debt_balance"],
        })
    charts.append({
        "title": "Portfolio Value by Property",
        "type": "bar",
        "data": value_data,
        "xKey": "Property",
        "yKeys": ["Value"],
        "colors": ["#10b981"]
    })

    # Asset Type Allocation Pie Chart
    type_data = []
    corr = results["correlation_analysis"]
    for asset_type, allocation in corr["type_allocation"].items():
        type_data.append({
            "Type": asset_type,
            "Allocation": allocation * 100,
        })
    charts.append({
        "title": "Asset Type Allocation",
        "type": "pie",
        "data": type_data,
        "dataKey": "Allocation",
        "nameKey": "Type",
        "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    })

    # Geographic Allocation Pie Chart
    market_data = []
    for market, allocation in corr["market_allocation"].items():
        market_data.append({
            "Market": market,
            "Allocation": allocation * 100,
        })
    charts.append({
        "title": "Geographic Allocation",
        "type": "pie",
        "data": market_data,
        "dataKey": "Allocation",
        "nameKey": "Market",
        "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    })

    # Cash Flow Comparison
    cashflow_data = []
    for prop in results["property_comparison"]:
        cashflow_data.append({
            "Property": prop["name"],
            "NOI": prop["annual_noi"],
            "Cash Flow": prop["annual_cash_flow"],
        })
    charts.append({
        "title": "Annual Cash Flow by Property",
        "type": "bar",
        "data": cashflow_data,
        "xKey": "Property",
        "yKeys": ["Cash Flow"],
        "colors": ["#10b981"]
    })

    # Performance Metrics Comparison
    performance_data = []
    for prop in results["property_comparison"]:
        performance_data.append({
            "Property": prop["name"],
            "Cap Rate": prop["cap_rate"] * 100,
            "CoC Return": prop["coc_return"] * 100,
        })
    charts.append({
        "title": "Performance Metrics by Property",
        "type": "bar",
        "data": performance_data,
        "xKey": "Property",
        "yKeys": ["Cap Rate", "CoC Return"],
        "colors": ["#3b82f6", "#10b981"]
    })

    return charts


if __name__ == "__main__":
    # CLI interface for testing
    import sys

    inputs = prepare_inputs(DEFAULT_INPUTS)
    results = calculate_portfolio_dashboard(inputs)
    tables = build_report_tables(inputs, results)

    print("\n" + "="*80)
    print("MULTI-PROPERTY PORTFOLIO DASHBOARD REPORT")
    print("="*80 + "\n")

    for table in tables:
        print(f"\n{table['title']}")
        print("-" * 80)
        for row in table['rows']:
            print(f"{list(row.values())[0]:<40} {list(row.values())[1]:>20}")

    print("\n" + "="*80)
