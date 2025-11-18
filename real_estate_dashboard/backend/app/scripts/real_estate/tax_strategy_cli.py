"""
Tax Strategy Integration Calculator
Comprehensive tax planning and optimization for real estate investments
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
import json

DEFAULT_INPUTS: Dict[str, Any] = {
    "project_name": "Tax Strategy Analysis",
    "location": "California",
    "analyst": "Tax Advisor",

    # Property Information
    "property_value": 1000000.0,
    "purchase_price": 900000.0,
    "purchase_date": "2020-01-15",
    "property_type": "Multifamily",
    "land_value_pct": 0.20,

    # 1031 Exchange Settings
    "enable_1031": True,
    "sale_date": "2025-12-01",
    "replacement_property_value": 1200000.0,
    "identification_days": 45,
    "exchange_completion_days": 180,

    # Cost Segregation Settings
    "enable_cost_seg": True,
    "cost_seg_study_cost": 8000.0,
    "personal_property_pct": 0.15,
    "land_improvements_pct": 0.10,
    "building_pct": 0.55,

    # Opportunity Zone Settings
    "enable_opportunity_zone": False,
    "oz_investment_amount": 500000.0,
    "oz_investment_date": "2024-01-01",
    "oz_hold_period_years": 10,

    # Entity Structure
    "current_entity_type": "LLC",
    "compare_entities": True,
    "annual_income": 200000.0,
    "state_tax_rate": 0.093,

    # Capital Gains Settings
    "holding_period_months": 24,
    "federal_income_bracket": 0.24,
    "state_capital_gains_rate": 0.133,
    "net_investment_income_tax": 0.038,

    # Depreciation Settings
    "accumulated_depreciation": 100000.0,
    "bonus_depreciation_taken": 50000.0,
    "section_179_taken": 0.0,

    # Financial Assumptions
    "annual_appreciation": 0.03,
    "inflation_rate": 0.025,
    "discount_rate": 0.08,
}

FORM_FIELDS: List[Dict[str, Any]] = [
    # Property Profile Section
    {
        "name": "project_name",
        "label": "Project Name",
        "type": "text",
        "section": "Property Profile",
        "help": "Name for this tax strategy analysis"
    },
    {
        "name": "location",
        "label": "Location (State)",
        "type": "text",
        "section": "Property Profile",
        "help": "State for tax calculations"
    },
    {
        "name": "analyst",
        "label": "Analyst/Advisor",
        "type": "text",
        "section": "Property Profile",
        "help": "Name of tax advisor or analyst"
    },
    {
        "name": "property_value",
        "label": "Current Property Value ($)",
        "type": "number",
        "section": "Property Profile",
        "help": "Current fair market value"
    },
    {
        "name": "purchase_price",
        "label": "Original Purchase Price ($)",
        "type": "number",
        "section": "Property Profile",
        "help": "Original acquisition cost"
    },
    {
        "name": "purchase_date",
        "label": "Purchase Date",
        "type": "date",
        "section": "Property Profile",
        "help": "Original purchase date (YYYY-MM-DD)"
    },
    {
        "name": "property_type",
        "label": "Property Type",
        "type": "select",
        "options": ["Single Family", "Multifamily", "Commercial", "Mixed-Use", "Industrial"],
        "section": "Property Profile",
        "help": "Type of property for depreciation calculations"
    },
    {
        "name": "land_value_pct",
        "label": "Land Value %",
        "type": "number",
        "section": "Property Profile",
        "help": "Percentage of value allocated to land (non-depreciable)"
    },

    # 1031 Exchange Section
    {
        "name": "enable_1031",
        "label": "Enable 1031 Exchange Analysis",
        "type": "boolean",
        "section": "1031 Exchange",
        "help": "Analyze 1031 like-kind exchange benefits"
    },
    {
        "name": "sale_date",
        "label": "Planned Sale Date",
        "type": "date",
        "section": "1031 Exchange",
        "help": "Date of property sale (YYYY-MM-DD)"
    },
    {
        "name": "replacement_property_value",
        "label": "Replacement Property Value ($)",
        "type": "number",
        "section": "1031 Exchange",
        "help": "Target value of replacement property"
    },
    {
        "name": "identification_days",
        "label": "Identification Period (Days)",
        "type": "number",
        "section": "1031 Exchange",
        "help": "Days to identify replacement property (typically 45)"
    },
    {
        "name": "exchange_completion_days",
        "label": "Exchange Completion (Days)",
        "type": "number",
        "section": "1031 Exchange",
        "help": "Days to complete exchange (typically 180)"
    },

    # Cost Segregation Section
    {
        "name": "enable_cost_seg",
        "label": "Enable Cost Segregation",
        "type": "boolean",
        "section": "Cost Segregation",
        "help": "Analyze accelerated depreciation benefits"
    },
    {
        "name": "cost_seg_study_cost",
        "label": "Cost Seg Study Cost ($)",
        "type": "number",
        "section": "Cost Segregation",
        "help": "One-time cost for cost segregation study"
    },
    {
        "name": "personal_property_pct",
        "label": "Personal Property %",
        "type": "number",
        "section": "Cost Segregation",
        "help": "% allocated to 5-year personal property"
    },
    {
        "name": "land_improvements_pct",
        "label": "Land Improvements %",
        "type": "number",
        "section": "Cost Segregation",
        "help": "% allocated to 15-year land improvements"
    },
    {
        "name": "building_pct",
        "label": "Building %",
        "type": "number",
        "section": "Cost Segregation",
        "help": "% allocated to 27.5/39-year building"
    },

    # Opportunity Zone Section
    {
        "name": "enable_opportunity_zone",
        "label": "Enable Opportunity Zone Analysis",
        "type": "boolean",
        "section": "Opportunity Zone",
        "help": "Analyze Qualified Opportunity Zone benefits"
    },
    {
        "name": "oz_investment_amount",
        "label": "OZ Investment Amount ($)",
        "type": "number",
        "section": "Opportunity Zone",
        "help": "Amount invested in Opportunity Zone"
    },
    {
        "name": "oz_investment_date",
        "label": "OZ Investment Date",
        "type": "date",
        "section": "Opportunity Zone",
        "help": "Date of OZ investment (YYYY-MM-DD)"
    },
    {
        "name": "oz_hold_period_years",
        "label": "OZ Hold Period (Years)",
        "type": "number",
        "section": "Opportunity Zone",
        "help": "Planned holding period (10+ for full benefits)"
    },

    # Entity Structure Section
    {
        "name": "current_entity_type",
        "label": "Current Entity Type",
        "type": "select",
        "options": ["LLC", "S-Corp", "C-Corp", "Partnership", "Sole Proprietorship"],
        "section": "Entity Structure",
        "help": "Current entity structure"
    },
    {
        "name": "compare_entities",
        "label": "Compare Entity Structures",
        "type": "boolean",
        "section": "Entity Structure",
        "help": "Compare tax implications across entity types"
    },
    {
        "name": "annual_income",
        "label": "Annual Property Income ($)",
        "type": "number",
        "section": "Entity Structure",
        "help": "Annual net operating income"
    },
    {
        "name": "state_tax_rate",
        "label": "State Tax Rate",
        "type": "number",
        "section": "Entity Structure",
        "help": "State income tax rate (decimal)"
    },

    # Capital Gains Section
    {
        "name": "holding_period_months",
        "label": "Holding Period (Months)",
        "type": "number",
        "section": "Capital Gains",
        "help": "Months property has been held"
    },
    {
        "name": "federal_income_bracket",
        "label": "Federal Income Tax Bracket",
        "type": "number",
        "section": "Capital Gains",
        "help": "Marginal federal income tax rate (decimal)"
    },
    {
        "name": "state_capital_gains_rate",
        "label": "State Capital Gains Rate",
        "type": "number",
        "section": "Capital Gains",
        "help": "State capital gains tax rate (decimal)"
    },
    {
        "name": "net_investment_income_tax",
        "label": "Net Investment Income Tax",
        "type": "number",
        "section": "Capital Gains",
        "help": "NIIT rate (typically 3.8% for high earners)"
    },

    # Depreciation Section
    {
        "name": "accumulated_depreciation",
        "label": "Accumulated Depreciation ($)",
        "type": "number",
        "section": "Depreciation",
        "help": "Total depreciation taken to date"
    },
    {
        "name": "bonus_depreciation_taken",
        "label": "Bonus Depreciation Taken ($)",
        "type": "number",
        "section": "Depreciation",
        "help": "Amount of bonus depreciation claimed"
    },
    {
        "name": "section_179_taken",
        "label": "Section 179 Deduction ($)",
        "type": "number",
        "section": "Depreciation",
        "help": "Section 179 expense deduction taken"
    },

    # Financial Assumptions
    {
        "name": "annual_appreciation",
        "label": "Annual Appreciation Rate",
        "type": "number",
        "section": "Assumptions",
        "help": "Expected annual property appreciation (decimal)"
    },
    {
        "name": "inflation_rate",
        "label": "Inflation Rate",
        "type": "number",
        "section": "Assumptions",
        "help": "Expected annual inflation (decimal)"
    },
    {
        "name": "discount_rate",
        "label": "Discount Rate",
        "type": "number",
        "section": "Assumptions",
        "help": "Discount rate for NPV calculations (decimal)"
    },
]


def prepare_inputs(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare and validate inputs for tax strategy calculations.
    """
    inputs = raw.copy()

    # Ensure percentages are decimals
    percentage_fields = [
        "land_value_pct", "personal_property_pct", "land_improvements_pct",
        "building_pct", "state_tax_rate", "federal_income_bracket",
        "state_capital_gains_rate", "net_investment_income_tax",
        "annual_appreciation", "inflation_rate", "discount_rate"
    ]

    for field in percentage_fields:
        if field in inputs and inputs[field] > 1:
            inputs[field] = inputs[field] / 100.0

    # Parse dates
    date_fields = ["purchase_date", "sale_date", "oz_investment_date"]
    for field in date_fields:
        if field in inputs and isinstance(inputs[field], str):
            inputs[field] = datetime.strptime(inputs[field], "%Y-%m-%d")

    return inputs


def calculate_capital_gains(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate capital gains tax (long-term vs short-term).
    """
    property_value = inputs["property_value"]
    purchase_price = inputs["purchase_price"]
    holding_period_months = inputs["holding_period_months"]
    accumulated_depreciation = inputs["accumulated_depreciation"]

    # Calculate gain
    adjusted_basis = purchase_price - accumulated_depreciation
    total_gain = property_value - adjusted_basis
    capital_gain = property_value - purchase_price
    depreciation_recapture = accumulated_depreciation

    # Determine if long-term or short-term
    is_long_term = holding_period_months >= 12

    if is_long_term:
        # Long-term capital gains rates (0%, 15%, 20% based on income)
        federal_rate = inputs["federal_income_bracket"]
        if federal_rate <= 0.12:
            ltcg_rate = 0.0
        elif federal_rate <= 0.22:
            ltcg_rate = 0.15
        else:
            ltcg_rate = 0.20

        # Depreciation recapture taxed at 25%
        recapture_rate = 0.25

        federal_tax_on_gain = capital_gain * ltcg_rate
        federal_tax_on_recapture = depreciation_recapture * recapture_rate
        federal_tax_total = federal_tax_on_gain + federal_tax_on_recapture

    else:
        # Short-term: taxed as ordinary income
        ordinary_rate = inputs["federal_income_bracket"]
        federal_tax_total = total_gain * ordinary_rate
        federal_tax_on_gain = capital_gain * ordinary_rate
        federal_tax_on_recapture = depreciation_recapture * ordinary_rate

    # State taxes
    state_rate = inputs["state_capital_gains_rate"]
    state_tax = total_gain * state_rate

    # Net Investment Income Tax (3.8% for high earners)
    niit_rate = inputs["net_investment_income_tax"]
    niit_tax = total_gain * niit_rate

    # Total taxes
    total_tax = federal_tax_total + state_tax + niit_tax
    net_proceeds = property_value - total_tax
    effective_tax_rate = total_tax / total_gain if total_gain > 0 else 0

    return {
        "total_gain": total_gain,
        "capital_gain": capital_gain,
        "depreciation_recapture": depreciation_recapture,
        "adjusted_basis": adjusted_basis,
        "is_long_term": is_long_term,
        "federal_tax_on_gain": federal_tax_on_gain,
        "federal_tax_on_recapture": federal_tax_on_recapture,
        "federal_tax_total": federal_tax_total,
        "state_tax": state_tax,
        "niit_tax": niit_tax,
        "total_tax": total_tax,
        "net_proceeds": net_proceeds,
        "effective_tax_rate": effective_tax_rate,
    }


def calculate_1031_exchange(inputs: Dict[str, Any], capital_gains: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate 1031 exchange timeline and requirements.
    """
    sale_date = inputs["sale_date"]
    if isinstance(sale_date, str):
        sale_date = datetime.strptime(sale_date, "%Y-%m-%d")

    identification_deadline = sale_date + timedelta(days=inputs["identification_days"])
    exchange_deadline = sale_date + timedelta(days=inputs["exchange_completion_days"])

    # Calculate requirements
    relinquished_value = inputs["property_value"]
    replacement_value = inputs["replacement_property_value"]

    # Must be equal or greater value
    meets_value_requirement = replacement_value >= relinquished_value

    # Calculate tax deferral
    deferred_tax = capital_gains["total_tax"] if meets_value_requirement else 0
    boot = max(0, relinquished_value - replacement_value)
    taxable_boot = boot * capital_gains["effective_tax_rate"]

    # Calculate net benefit
    tax_savings = deferred_tax - taxable_boot

    return {
        "sale_date": sale_date.strftime("%Y-%m-%d"),
        "identification_deadline": identification_deadline.strftime("%Y-%m-%d"),
        "exchange_deadline": exchange_deadline.strftime("%Y-%m-%d"),
        "relinquished_value": relinquished_value,
        "replacement_value": replacement_value,
        "meets_value_requirement": meets_value_requirement,
        "deferred_tax": deferred_tax,
        "boot": boot,
        "taxable_boot": taxable_boot,
        "tax_savings": tax_savings,
        "days_to_identify": inputs["identification_days"],
        "days_to_complete": inputs["exchange_completion_days"],
    }


def calculate_cost_segregation(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate accelerated depreciation from cost segregation.
    """
    purchase_price = inputs["purchase_price"]
    land_value_pct = inputs["land_value_pct"]
    depreciable_basis = purchase_price * (1 - land_value_pct)

    # Allocate basis
    personal_property = depreciable_basis * inputs["personal_property_pct"]
    land_improvements = depreciable_basis * inputs["land_improvements_pct"]
    building = depreciable_basis * inputs["building_pct"]

    # Calculate depreciation schedules
    # Personal property: 5-year MACRS (200% declining balance)
    # Land improvements: 15-year MACRS
    # Building: 27.5 years (residential) or 39 years (commercial)

    property_type = inputs["property_type"]
    if property_type in ["Single Family", "Multifamily"]:
        building_life = 27.5
    else:
        building_life = 39

    # Year 1 depreciation
    personal_property_depr_yr1 = personal_property * 0.20  # 5-year MACRS
    land_improvements_depr_yr1 = land_improvements / 15
    building_depr_yr1 = building / building_life

    # Standard depreciation (no cost seg)
    standard_depr_yr1 = depreciable_basis / building_life

    # Cost seg benefit
    total_depr_yr1 = personal_property_depr_yr1 + land_improvements_depr_yr1 + building_depr_yr1
    accelerated_deduction = total_depr_yr1 - standard_depr_yr1

    # Tax savings (first year)
    tax_rate = inputs["federal_income_bracket"] + inputs["state_tax_rate"]
    tax_savings_yr1 = accelerated_deduction * tax_rate

    # NPV of cost seg study
    study_cost = inputs["cost_seg_study_cost"]
    roi = (tax_savings_yr1 - study_cost) / study_cost if study_cost > 0 else 0

    # 5-year cumulative benefit
    total_5yr_benefit = 0
    for year in range(1, 6):
        if year <= 5:
            pp_depr = personal_property * [0.20, 0.32, 0.192, 0.1152, 0.1152][year - 1]
        else:
            pp_depr = 0
        li_depr = land_improvements / 15
        bldg_depr = building / building_life
        total_depr = pp_depr + li_depr + bldg_depr
        standard_depr = depreciable_basis / building_life
        benefit = (total_depr - standard_depr) * tax_rate
        total_5yr_benefit += benefit / ((1 + inputs["discount_rate"]) ** year)

    return {
        "depreciable_basis": depreciable_basis,
        "personal_property": personal_property,
        "land_improvements": land_improvements,
        "building": building,
        "building_life": building_life,
        "personal_property_depr_yr1": personal_property_depr_yr1,
        "land_improvements_depr_yr1": land_improvements_depr_yr1,
        "building_depr_yr1": building_depr_yr1,
        "total_depr_yr1": total_depr_yr1,
        "standard_depr_yr1": standard_depr_yr1,
        "accelerated_deduction": accelerated_deduction,
        "tax_savings_yr1": tax_savings_yr1,
        "study_cost": study_cost,
        "net_benefit_yr1": tax_savings_yr1 - study_cost,
        "roi": roi,
        "total_5yr_benefit": total_5yr_benefit,
    }


def calculate_opportunity_zone(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate Opportunity Zone tax benefits.
    """
    investment = inputs["oz_investment_amount"]
    investment_date = inputs["oz_investment_date"]
    if isinstance(investment_date, str):
        investment_date = datetime.strptime(investment_date, "%Y-%m-%d")

    hold_years = inputs["oz_hold_period_years"]

    # Assumed appreciation
    appreciation_rate = inputs["annual_appreciation"]
    future_value = investment * ((1 + appreciation_rate) ** hold_years)
    gain = future_value - investment

    # OZ Benefits:
    # - Temporary deferral of capital gains (until 2026 or sale, whichever earlier)
    # - 10% step-up in basis if held 5+ years (before 2026)
    # - 15% step-up in basis if held 7+ years (before 2026)
    # - Permanent exclusion of OZ appreciation if held 10+ years

    # Assuming original capital gain invested
    original_gain = investment  # Assuming reinvested capital gain

    # Basis step-up
    if hold_years >= 7:
        basis_step_up_pct = 0.15
    elif hold_years >= 5:
        basis_step_up_pct = 0.10
    else:
        basis_step_up_pct = 0.0

    basis_step_up = original_gain * basis_step_up_pct
    deferred_gain_taxable = original_gain - basis_step_up

    # Tax on original gain (deferred until 2026 or sale)
    # Assuming 2026 is the trigger
    years_to_2026 = max(0, (datetime(2026, 12, 31) - investment_date).days / 365.25)

    tax_rate = inputs["federal_income_bracket"] + inputs["state_capital_gains_rate"]
    deferred_gain_tax = deferred_gain_taxable * tax_rate

    # Permanent exclusion if held 10+ years
    if hold_years >= 10:
        oz_gain_excluded = gain
        oz_gain_taxable = 0
    else:
        oz_gain_excluded = 0
        oz_gain_taxable = gain

    # Tax savings
    tax_on_oz_gain = oz_gain_taxable * tax_rate
    tax_without_oz = (original_gain + gain) * tax_rate
    total_tax_savings = tax_without_oz - (deferred_gain_tax + tax_on_oz_gain)

    return {
        "investment": investment,
        "hold_years": hold_years,
        "future_value": future_value,
        "gain": gain,
        "original_gain": original_gain,
        "basis_step_up_pct": basis_step_up_pct,
        "basis_step_up": basis_step_up,
        "deferred_gain_taxable": deferred_gain_taxable,
        "deferred_gain_tax": deferred_gain_tax,
        "oz_gain_excluded": oz_gain_excluded,
        "oz_gain_taxable": oz_gain_taxable,
        "tax_on_oz_gain": tax_on_oz_gain,
        "tax_without_oz": tax_without_oz,
        "total_tax_savings": total_tax_savings,
        "effective_tax_rate": (deferred_gain_tax + tax_on_oz_gain) / (original_gain + gain) if (original_gain + gain) > 0 else 0,
    }


def calculate_entity_comparison(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare tax implications across different entity structures.
    """
    annual_income = inputs["annual_income"]
    federal_rate = inputs["federal_income_bracket"]
    state_rate = inputs["state_tax_rate"]

    # LLC (Pass-through)
    llc_federal_tax = annual_income * federal_rate
    llc_state_tax = annual_income * state_rate
    llc_se_tax = annual_income * 0.153  # Self-employment tax (15.3%)
    llc_total_tax = llc_federal_tax + llc_state_tax + llc_se_tax
    llc_net_income = annual_income - llc_total_tax

    # S-Corp (Pass-through with reasonable salary)
    scorp_salary = min(annual_income * 0.4, annual_income)  # 40% reasonable salary
    scorp_distributions = annual_income - scorp_salary

    scorp_salary_se_tax = scorp_salary * 0.153
    scorp_salary_federal = scorp_salary * federal_rate
    scorp_salary_state = scorp_salary * state_rate
    scorp_dist_federal = scorp_distributions * federal_rate
    scorp_dist_state = scorp_distributions * state_rate
    scorp_total_tax = scorp_salary_se_tax + scorp_salary_federal + scorp_salary_state + scorp_dist_federal + scorp_dist_state
    scorp_net_income = annual_income - scorp_total_tax

    # C-Corp (Double taxation)
    ccorp_corporate_rate = 0.21  # Federal corporate tax rate
    ccorp_corporate_tax = annual_income * ccorp_corporate_rate
    ccorp_after_corp_tax = annual_income - ccorp_corporate_tax

    # Dividend tax (assuming all distributed)
    ccorp_dividend_rate = 0.20  # Qualified dividend rate
    ccorp_dividend_tax_federal = ccorp_after_corp_tax * ccorp_dividend_rate
    ccorp_dividend_tax_state = ccorp_after_corp_tax * state_rate
    ccorp_total_tax = ccorp_corporate_tax + ccorp_dividend_tax_federal + ccorp_dividend_tax_state
    ccorp_net_income = annual_income - ccorp_total_tax

    # Partnership (similar to LLC but may have different allocation)
    partnership_federal_tax = annual_income * federal_rate
    partnership_state_tax = annual_income * state_rate
    partnership_se_tax = annual_income * 0.153
    partnership_total_tax = partnership_federal_tax + partnership_state_tax + partnership_se_tax
    partnership_net_income = annual_income - partnership_total_tax

    # Sole Proprietorship (same as LLC for tax purposes)
    sole_prop_total_tax = llc_total_tax
    sole_prop_net_income = llc_net_income

    entities = {
        "LLC": {
            "federal_tax": llc_federal_tax,
            "state_tax": llc_state_tax,
            "se_tax": llc_se_tax,
            "total_tax": llc_total_tax,
            "net_income": llc_net_income,
            "effective_rate": llc_total_tax / annual_income,
        },
        "S-Corp": {
            "federal_tax": scorp_salary_federal + scorp_dist_federal,
            "state_tax": scorp_salary_state + scorp_dist_state,
            "se_tax": scorp_salary_se_tax,
            "total_tax": scorp_total_tax,
            "net_income": scorp_net_income,
            "effective_rate": scorp_total_tax / annual_income,
            "salary": scorp_salary,
            "distributions": scorp_distributions,
        },
        "C-Corp": {
            "corporate_tax": ccorp_corporate_tax,
            "dividend_tax_federal": ccorp_dividend_tax_federal,
            "dividend_tax_state": ccorp_dividend_tax_state,
            "total_tax": ccorp_total_tax,
            "net_income": ccorp_net_income,
            "effective_rate": ccorp_total_tax / annual_income,
        },
        "Partnership": {
            "federal_tax": partnership_federal_tax,
            "state_tax": partnership_state_tax,
            "se_tax": partnership_se_tax,
            "total_tax": partnership_total_tax,
            "net_income": partnership_net_income,
            "effective_rate": partnership_total_tax / annual_income,
        },
        "Sole Proprietorship": {
            "federal_tax": llc_federal_tax,
            "state_tax": llc_state_tax,
            "se_tax": llc_se_tax,
            "total_tax": sole_prop_total_tax,
            "net_income": sole_prop_net_income,
            "effective_rate": sole_prop_total_tax / annual_income,
        },
    }

    # Find best structure
    best_entity = min(entities.items(), key=lambda x: x[1]["total_tax"])

    return {
        "annual_income": annual_income,
        "entities": entities,
        "best_entity": best_entity[0],
        "best_entity_tax": best_entity[1]["total_tax"],
        "best_entity_net": best_entity[1]["net_income"],
        "current_entity": inputs["current_entity_type"],
        "current_entity_tax": entities[inputs["current_entity_type"]]["total_tax"],
        "potential_savings": entities[inputs["current_entity_type"]]["total_tax"] - best_entity[1]["total_tax"],
    }


def calculate_depreciation_recapture(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate depreciation recapture on property exit.
    """
    accumulated_depreciation = inputs["accumulated_depreciation"]
    bonus_depreciation = inputs["bonus_depreciation_taken"]
    section_179 = inputs["section_179_taken"]

    # Depreciation recapture is taxed at 25% (up to ordinary income rate)
    ordinary_rate = inputs["federal_income_bracket"]
    recapture_rate = min(0.25, ordinary_rate)

    # Calculate recapture tax
    total_recapture = accumulated_depreciation
    recapture_tax_federal = total_recapture * recapture_rate

    # State tax on recapture
    state_rate = inputs["state_tax_rate"]
    recapture_tax_state = total_recapture * state_rate

    # Total recapture tax
    total_recapture_tax = recapture_tax_federal + recapture_tax_state

    # Breakdown by type
    regular_depreciation = accumulated_depreciation - bonus_depreciation - section_179

    return {
        "accumulated_depreciation": accumulated_depreciation,
        "regular_depreciation": regular_depreciation,
        "bonus_depreciation": bonus_depreciation,
        "section_179": section_179,
        "recapture_rate_federal": recapture_rate,
        "recapture_tax_federal": recapture_tax_federal,
        "recapture_tax_state": recapture_tax_state,
        "total_recapture_tax": total_recapture_tax,
        "effective_recapture_rate": total_recapture_tax / total_recapture if total_recapture > 0 else 0,
    }


def calculate_tax_strategy(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main calculation function that orchestrates all tax strategy calculations.
    """
    results = {
        "project_name": inputs["project_name"],
        "location": inputs["location"],
        "analyst": inputs["analyst"],
        "property_value": inputs["property_value"],
        "purchase_price": inputs["purchase_price"],
    }

    # Capital Gains
    results["capital_gains"] = calculate_capital_gains(inputs)

    # 1031 Exchange
    if inputs.get("enable_1031", False):
        results["exchange_1031"] = calculate_1031_exchange(inputs, results["capital_gains"])

    # Cost Segregation
    if inputs.get("enable_cost_seg", False):
        results["cost_segregation"] = calculate_cost_segregation(inputs)

    # Opportunity Zone
    if inputs.get("enable_opportunity_zone", False):
        results["opportunity_zone"] = calculate_opportunity_zone(inputs)

    # Entity Comparison
    if inputs.get("compare_entities", False):
        results["entity_comparison"] = calculate_entity_comparison(inputs)

    # Depreciation Recapture
    results["depreciation_recapture"] = calculate_depreciation_recapture(inputs)

    # Summary metrics
    total_tax_savings = 0
    if "exchange_1031" in results:
        total_tax_savings += results["exchange_1031"]["tax_savings"]
    if "cost_segregation" in results:
        total_tax_savings += results["cost_segregation"]["total_5yr_benefit"]
    if "opportunity_zone" in results:
        total_tax_savings += results["opportunity_zone"]["total_tax_savings"]
    if "entity_comparison" in results:
        total_tax_savings += results["entity_comparison"]["potential_savings"]

    results["summary"] = {
        "total_tax_savings": total_tax_savings,
        "baseline_tax": results["capital_gains"]["total_tax"],
        "optimized_tax": results["capital_gains"]["total_tax"] - total_tax_savings,
        "tax_reduction_pct": total_tax_savings / results["capital_gains"]["total_tax"] if results["capital_gains"]["total_tax"] > 0 else 0,
    }

    return results


def build_report_tables(inputs: Dict[str, Any], results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build formatted tables for display.
    """
    tables = []

    # Summary Table
    summary_rows = [
        {"Metric": "Property Value", "Value": f"${results['property_value']:,.0f}"},
        {"Metric": "Purchase Price", "Value": f"${results['purchase_price']:,.0f}"},
        {"Metric": "Baseline Tax Liability", "Value": f"${results['summary']['baseline_tax']:,.0f}"},
        {"Metric": "Optimized Tax Liability", "Value": f"${results['summary']['optimized_tax']:,.0f}"},
        {"Metric": "Total Tax Savings", "Value": f"${results['summary']['total_tax_savings']:,.0f}"},
        {"Metric": "Tax Reduction", "Value": f"{results['summary']['tax_reduction_pct']:.1%}"},
    ]
    tables.append({
        "title": "Tax Strategy Summary",
        "rows": summary_rows,
        "columns": ["Metric", "Value"]
    })

    # Capital Gains Table
    cg = results["capital_gains"]
    cg_rows = [
        {"Item": "Total Gain", "Amount": f"${cg['total_gain']:,.0f}"},
        {"Item": "  Capital Gain", "Amount": f"${cg['capital_gain']:,.0f}"},
        {"Item": "  Depreciation Recapture", "Amount": f"${cg['depreciation_recapture']:,.0f}"},
        {"Item": "Holding Period", "Amount": "Long-term" if cg['is_long_term'] else "Short-term"},
        {"Item": "Federal Tax", "Amount": f"${cg['federal_tax_total']:,.0f}"},
        {"Item": "State Tax", "Amount": f"${cg['state_tax']:,.0f}"},
        {"Item": "NIIT", "Amount": f"${cg['niit_tax']:,.0f}"},
        {"Item": "Total Tax", "Amount": f"${cg['total_tax']:,.0f}"},
        {"Item": "Effective Rate", "Amount": f"{cg['effective_tax_rate']:.2%}"},
        {"Item": "Net Proceeds", "Amount": f"${cg['net_proceeds']:,.0f}"},
    ]
    tables.append({
        "title": "Capital Gains Analysis",
        "rows": cg_rows,
        "columns": ["Item", "Amount"]
    })

    # 1031 Exchange Table
    if "exchange_1031" in results:
        ex = results["exchange_1031"]
        ex_rows = [
            {"Item": "Sale Date", "Value": ex['sale_date']},
            {"Item": "Identification Deadline", "Value": ex['identification_deadline']},
            {"Item": "Exchange Deadline", "Value": ex['exchange_deadline']},
            {"Item": "Relinquished Property Value", "Value": f"${ex['relinquished_value']:,.0f}"},
            {"Item": "Replacement Property Value", "Value": f"${ex['replacement_value']:,.0f}"},
            {"Item": "Meets Value Requirement", "Value": "✓ Yes" if ex['meets_value_requirement'] else "✗ No"},
            {"Item": "Deferred Tax", "Value": f"${ex['deferred_tax']:,.0f}"},
            {"Item": "Boot (Taxable)", "Value": f"${ex['boot']:,.0f}"},
            {"Item": "Tax on Boot", "Value": f"${ex['taxable_boot']:,.0f}"},
            {"Item": "Net Tax Savings", "Value": f"${ex['tax_savings']:,.0f}"},
        ]
        tables.append({
            "title": "1031 Exchange Analysis",
            "rows": ex_rows,
            "columns": ["Item", "Value"]
        })

    # Cost Segregation Table
    if "cost_segregation" in results:
        cs = results["cost_segregation"]
        cs_rows = [
            {"Item": "Depreciable Basis", "Amount": f"${cs['depreciable_basis']:,.0f}"},
            {"Item": "  Personal Property (5-yr)", "Amount": f"${cs['personal_property']:,.0f}"},
            {"Item": "  Land Improvements (15-yr)", "Amount": f"${cs['land_improvements']:,.0f}"},
            {"Item": "  Building ({:.1f}-yr)".format(cs['building_life']), "Amount": f"${cs['building']:,.0f}"},
            {"Item": "Year 1 Depreciation (Cost Seg)", "Amount": f"${cs['total_depr_yr1']:,.0f}"},
            {"Item": "Year 1 Depreciation (Standard)", "Amount": f"${cs['standard_depr_yr1']:,.0f}"},
            {"Item": "Accelerated Deduction", "Amount": f"${cs['accelerated_deduction']:,.0f}"},
            {"Item": "Tax Savings (Year 1)", "Amount": f"${cs['tax_savings_yr1']:,.0f}"},
            {"Item": "Study Cost", "Amount": f"${cs['study_cost']:,.0f}"},
            {"Item": "Net Benefit (Year 1)", "Amount": f"${cs['net_benefit_yr1']:,.0f}"},
            {"Item": "ROI", "Amount": f"{cs['roi']:.1%}"},
            {"Item": "5-Year NPV Benefit", "Amount": f"${cs['total_5yr_benefit']:,.0f}"},
        ]
        tables.append({
            "title": "Cost Segregation Analysis",
            "rows": cs_rows,
            "columns": ["Item", "Amount"]
        })

    # Opportunity Zone Table
    if "opportunity_zone" in results:
        oz = results["opportunity_zone"]
        oz_rows = [
            {"Item": "Investment Amount", "Value": f"${oz['investment']:,.0f}"},
            {"Item": "Hold Period", "Value": f"{oz['hold_years']} years"},
            {"Item": "Future Value", "Value": f"${oz['future_value']:,.0f}"},
            {"Item": "OZ Gain", "Value": f"${oz['gain']:,.0f}"},
            {"Item": "Basis Step-Up", "Value": f"{oz['basis_step_up_pct']:.0%} (${oz['basis_step_up']:,.0f})"},
            {"Item": "Deferred Gain (Taxable)", "Value": f"${oz['deferred_gain_taxable']:,.0f}"},
            {"Item": "Tax on Deferred Gain", "Value": f"${oz['deferred_gain_tax']:,.0f}"},
            {"Item": "OZ Gain Excluded", "Value": f"${oz['oz_gain_excluded']:,.0f}"},
            {"Item": "OZ Gain Taxable", "Value": f"${oz['oz_gain_taxable']:,.0f}"},
            {"Item": "Total Tax Savings", "Value": f"${oz['total_tax_savings']:,.0f}"},
            {"Item": "Effective Tax Rate", "Value": f"{oz['effective_tax_rate']:.2%}"},
        ]
        tables.append({
            "title": "Opportunity Zone Benefits",
            "rows": oz_rows,
            "columns": ["Item", "Value"]
        })

    # Entity Comparison Table
    if "entity_comparison" in results:
        ec = results["entity_comparison"]
        ec_rows = []
        for entity_name, entity_data in ec["entities"].items():
            ec_rows.append({
                "Entity": entity_name,
                "Total Tax": f"${entity_data['total_tax']:,.0f}",
                "Net Income": f"${entity_data['net_income']:,.0f}",
                "Effective Rate": f"{entity_data['effective_rate']:.2%}",
            })
        tables.append({
            "title": "Entity Structure Comparison",
            "rows": ec_rows,
            "columns": ["Entity", "Total Tax", "Net Income", "Effective Rate"]
        })

        # Best entity recommendation
        rec_rows = [
            {"Item": "Current Entity", "Value": ec['current_entity']},
            {"Item": "Current Tax", "Value": f"${ec['current_entity_tax']:,.0f}"},
            {"Item": "Recommended Entity", "Value": ec['best_entity']},
            {"Item": "Recommended Tax", "Value": f"${ec['best_entity_tax']:,.0f}"},
            {"Item": "Potential Savings", "Value": f"${ec['potential_savings']:,.0f}"},
        ]
        tables.append({
            "title": "Entity Optimization Recommendation",
            "rows": rec_rows,
            "columns": ["Item", "Value"]
        })

    # Depreciation Recapture Table
    dr = results["depreciation_recapture"]
    dr_rows = [
        {"Item": "Total Accumulated Depreciation", "Amount": f"${dr['accumulated_depreciation']:,.0f}"},
        {"Item": "  Regular Depreciation", "Amount": f"${dr['regular_depreciation']:,.0f}"},
        {"Item": "  Bonus Depreciation", "Amount": f"${dr['bonus_depreciation']:,.0f}"},
        {"Item": "  Section 179", "Amount": f"${dr['section_179']:,.0f}"},
        {"Item": "Federal Recapture Rate", "Amount": f"{dr['recapture_rate_federal']:.2%}"},
        {"Item": "Federal Recapture Tax", "Amount": f"${dr['recapture_tax_federal']:,.0f}"},
        {"Item": "State Recapture Tax", "Amount": f"${dr['recapture_tax_state']:,.0f}"},
        {"Item": "Total Recapture Tax", "Amount": f"${dr['total_recapture_tax']:,.0f}"},
        {"Item": "Effective Recapture Rate", "Amount": f"{dr['effective_recapture_rate']:.2%}"},
    ]
    tables.append({
        "title": "Depreciation Recapture on Exit",
        "rows": dr_rows,
        "columns": ["Item", "Amount"]
    })

    return tables


def build_chart_specs(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build chart specifications for visualizations.
    """
    charts = []

    # Tax Savings Breakdown
    savings_data = []
    if "exchange_1031" in results:
        savings_data.append({
            "Strategy": "1031 Exchange",
            "Savings": results["exchange_1031"]["tax_savings"]
        })
    if "cost_segregation" in results:
        savings_data.append({
            "Strategy": "Cost Segregation",
            "Savings": results["cost_segregation"]["total_5yr_benefit"]
        })
    if "opportunity_zone" in results:
        savings_data.append({
            "Strategy": "Opportunity Zone",
            "Savings": results["opportunity_zone"]["total_tax_savings"]
        })
    if "entity_comparison" in results:
        savings_data.append({
            "Strategy": "Entity Optimization",
            "Savings": results["entity_comparison"]["potential_savings"]
        })

    if savings_data:
        charts.append({
            "title": "Tax Savings by Strategy",
            "type": "bar",
            "data": savings_data,
            "xKey": "Strategy",
            "yKeys": ["Savings"],
            "colors": ["#10b981"]
        })

    # Entity Comparison Chart
    if "entity_comparison" in results:
        entity_data = []
        for entity_name, entity_info in results["entity_comparison"]["entities"].items():
            entity_data.append({
                "Entity": entity_name,
                "Tax": entity_info["total_tax"],
                "Net": entity_info["net_income"]
            })
        charts.append({
            "title": "Entity Structure Tax Comparison",
            "type": "bar",
            "data": entity_data,
            "xKey": "Entity",
            "yKeys": ["Tax"],
            "colors": ["#ef4444"]
        })

    # Capital Gains Breakdown
    cg = results["capital_gains"]
    cg_data = [
        {"Component": "Federal Tax", "Amount": cg["federal_tax_total"]},
        {"Component": "State Tax", "Amount": cg["state_tax"]},
        {"Component": "NIIT", "Amount": cg["niit_tax"]},
    ]
    charts.append({
        "title": "Capital Gains Tax Breakdown",
        "type": "pie",
        "data": cg_data,
        "dataKey": "Amount",
        "nameKey": "Component",
        "colors": ["#3b82f6", "#8b5cf6", "#ec4899"]
    })

    return charts


if __name__ == "__main__":
    # CLI interface for testing
    import sys

    inputs = prepare_inputs(DEFAULT_INPUTS)
    results = calculate_tax_strategy(inputs)
    tables = build_report_tables(inputs, results)

    print("\n" + "="*80)
    print("TAX STRATEGY INTEGRATION REPORT")
    print("="*80 + "\n")

    for table in tables:
        print(f"\n{table['title']}")
        print("-" * 80)
        for row in table['rows']:
            print(f"{list(row.values())[0]:<40} {list(row.values())[1]:>20}")

    print("\n" + "="*80)
