"""Interactive endpoints for real estate financial models."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.real_estate import (
    FixAndFlipModel,
    SingleFamilyRentalModel,
    SmallMultifamilyModel,
    SmallMultifamilyAcquisitionModel,
    HighRiseMultifamilyModel,
    HotelFinancialModel,
    MixedUseDevelopmentModel,
    LeaseAnalyzerModel,
    RenovationBudgetModel,
    SubdivisionModel,
    TaxStrategyModel,
    PortfolioModel,
)
from app.scripts.real_estate.fix_and_flip_cli import (
    DEFAULT_INPUTS as FIX_DEFAULTS,
    FORM_FIELDS as FIX_FIELDS,
    analyze_flip,
    build_chart_specs as fix_chart_specs,
    build_report_tables as fix_tables,
    prepare_inputs as fix_prepare_inputs,
)
from app.scripts.real_estate.hotel_model_cli import (
    DEFAULT_INPUTS as HOTEL_DEFAULTS,
    FORM_FIELDS as HOTEL_FIELDS,
    build_chart_specs as hotel_chart_specs,
    build_projection as hotel_build_projection,
    build_report_tables as hotel_tables,
    prepare_inputs as hotel_prepare_inputs,
)
from app.scripts.real_estate.mixed_use_cli import (
    DEFAULT_INPUTS as MIXED_USE_DEFAULTS,
    FORM_FIELDS as MIXED_USE_FIELDS,
    build_chart_specs as mixed_use_chart_specs,
    build_projection as mixed_use_build_projection,
    build_report_tables as mixed_use_tables,
    prepare_inputs as mixed_use_prepare_inputs,
)
from app.scripts.real_estate.single_family_rental_cli import (
    DEFAULT_INPUTS as SFR_DEFAULTS,
    FORM_FIELDS as SFR_FIELDS,
    build_chart_specs as sfr_chart_specs,
    build_projection as sfr_build_projection,
    build_report_tables as sfr_tables,
    compute_exit_comparison,
    prepare_inputs as sfr_prepare_inputs,
)
from app.scripts.real_estate.small_multifamily_cli import (
    DEFAULT_INPUTS as MULTI_DEFAULTS,
    FORM_FIELDS as MULTI_FIELDS,
    build_chart_specs as multi_chart_specs,
    build_projection as multi_build_projection,
    build_report_tables as multi_tables,
    prepare_inputs as multi_prepare_inputs,
)
from app.scripts.real_estate.small_multifamily_acquisition_cli import (
    DEFAULT_INPUTS as ACQ_DEFAULTS,
    FORM_FIELDS as ACQ_FIELDS,
    build_projection as acq_build_projection,
    build_report_tables as acq_tables,
    prepare_inputs as acq_prepare_inputs,
)
from app.scripts.real_estate.extended_multifamily_cli import (
    DEFAULT_INPUTS as EXT_MULTI_DEFAULTS,
    FORM_FIELDS as EXT_MULTI_FIELDS,
    build_chart_specs as ext_multi_chart_specs,
    build_projection as ext_multi_build_projection,
    build_report_tables as ext_multi_tables,
    prepare_inputs as ext_multi_prepare_inputs,
)
from app.scripts.real_estate.lease_analyzer_cli import (
    DEFAULT_INPUTS as LEASE_DEFAULTS,
    FORM_FIELDS as LEASE_FIELDS,
    build_chart_specs as lease_chart_specs,
    build_projection as lease_build_projection,
    build_report_tables as lease_tables,
    prepare_inputs as lease_prepare_inputs,
)
from app.scripts.real_estate.renovation_budget_cli import (
    DEFAULT_INPUTS as RENO_DEFAULTS,
    FORM_FIELDS as RENO_FIELDS,
    build_chart_specs as reno_chart_specs,
    build_projection as reno_build_projection,
    build_report_tables as reno_tables,
    prepare_inputs as reno_prepare_inputs,
)
from app.scripts.real_estate.subdivision_cli import (
    DEFAULT_INPUTS as SUBDIVISION_DEFAULTS,
    FORM_FIELDS as SUBDIVISION_FIELDS,
    build_chart_specs as subdivision_chart_specs,
    build_projection as subdivision_build_projection,
    build_report_tables as subdivision_tables,
    prepare_inputs as subdivision_prepare_inputs,
)
from app.scripts.real_estate.tax_strategy_cli import (
    DEFAULT_INPUTS as TAX_DEFAULTS,
    FORM_FIELDS as TAX_FIELDS,
    build_chart_specs as tax_chart_specs,
    build_report_tables as tax_tables,
    calculate_tax_strategy,
    prepare_inputs as tax_prepare_inputs,
)
from app.scripts.real_estate.portfolio_dashboard_cli import (
    DEFAULT_INPUTS as PORTFOLIO_DEFAULTS,
    FORM_FIELDS as PORTFOLIO_FIELDS,
    build_chart_specs as portfolio_chart_specs,
    build_report_tables as portfolio_tables,
    calculate_portfolio_dashboard,
    prepare_inputs as portfolio_prepare_inputs,
)

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[3] / "templates"))


class RunModelRequest(BaseModel):
    model: str
    values: Dict[str, Any]
    save_to_db: Optional[bool] = True


def _coerce_inputs(defaults: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for key, default_value in defaults.items():
        merged[key] = default_value
    for key, raw in overrides.items():
        if key not in defaults:
            continue
        if raw in ("", None):
            continue
        default_value = defaults[key]
        try:
            if isinstance(default_value, bool):
                merged[key] = str(raw).lower() in {"true", "1", "yes", "on"}
            elif isinstance(default_value, int) and not isinstance(default_value, bool):
                merged[key] = int(float(raw))
            elif isinstance(default_value, float):
                merged[key] = float(raw)
            else:
                merged[key] = raw
        except (TypeError, ValueError):
            merged[key] = default_value
    return merged


MODEL_REGISTRY = {
    "fix_and_flip": {
        "label": "Fix & Flip",
        "description": "Analyze short-term renovation projects with comprehensive financial modeling. This model calculates the Maximum Allowable Offer (MAO), tracks renovation costs, holding expenses, and exit strategies using the 70% rule and market-speed adjustments.",
        "explanation": "**What it does:** Evaluates fix-and-flip opportunities by calculating profit potential, required capital, and ROI based on purchase price, renovation costs, holding period, and after-repair value (ARV).\n\n**Inputs needed:** Property details (location, size, beds/baths), purchase price, ARV, renovation budget, holding costs, financing terms (LTV, interest rate, points), and market speed (Hot/Moderate/Slow). The model uses market speed to adjust the MAO calculation.",
        "use_case": "Best for short-term residential renovation projects (3-12 months) where the strategy is to buy, renovate, and quickly sell for profit.",
        "defaults": FIX_DEFAULTS,
        "fields": FIX_FIELDS,
        "prepare": fix_prepare_inputs,
        "db_model": FixAndFlipModel,
    },
    "single_family_rental": {
        "label": "Single-Family Rental",
        "description": "Model long-term buy-and-hold strategies including BRRRR (Buy, Rehab, Rent, Refinance, Repeat), traditional rental, and refinance scenarios with 30-year cash flow projections.",
        "explanation": "**What it does:** Projects rental income, operating expenses, loan amortization, equity buildup, and cash-on-cash returns over a 10-30 year hold period. Includes refinance analysis and multiple exit scenarios.\n\n**Inputs needed:** Purchase price, renovation costs, monthly rent, operating expenses (taxes, insurance, management, maintenance), financing terms, rent growth rate, appreciation rate, vacancy rate, and refinance assumptions. The model generates year-by-year projections of NOI, cash flow, and equity.",
        "use_case": "Ideal for single-family residential buy-and-hold investments, BRRRR strategies, and long-term wealth building through rental properties.",
        "defaults": SFR_DEFAULTS,
        "fields": SFR_FIELDS,
        "prepare": sfr_prepare_inputs,
        "db_model": SingleFamilyRentalModel,
    },
    "small_multifamily": {
        "label": "Small Multifamily (2-6 units)",
        "description": "Evaluate small multifamily properties with unit-by-unit analysis, value-add strategies, and disposition planning for 2-6 unit buildings.",
        "explanation": "**What it does:** Analyzes multifamily properties by modeling individual units, calculating NOI, debt service coverage ratios (DSCR), cap rates, and IRR. Tracks rent growth, vacancy, and exit values based on stabilized NOI.\n\n**Inputs needed:** Number of units, rent per unit, purchase price, renovation costs per unit, operating expenses, financing terms, rent growth, exit cap rate, and hold period. Input detailed assumptions for each unit type.",
        "use_case": "Perfect for duplex, triplex, and small apartment building investments (2-6 units) with value-add renovation opportunities.",
        "defaults": MULTI_DEFAULTS,
        "fields": MULTI_FIELDS,
        "prepare": multi_prepare_inputs,
        "db_model": SmallMultifamilyModel,
    },
    "small_multifamily_acquisition": {
        "label": "Small Multifamily Acquisition",
        "description": "Detailed acquisition analysis for small multifamily properties (2-20 units) including unit-by-unit renovation strategies and comprehensive exit analysis.",
        "explanation": "**What it does:** Provides comprehensive acquisition modeling for small multifamily properties with detailed financial analysis including purchase price allocation, renovation budgets, debt service calculations, NOI projections, and exit value assessment. Calculates cash-on-cash returns, IRR, cap rates, and DSCR.\n\n**Inputs needed:** Property details (type, units, building SF, lot size, year built, zoning), acquisition costs (purchase price, closing costs, renovation budget), holding costs (insurance, utilities, property tax), financing terms (LTV, interest rate, loan term), and exit assumptions (cap rate, selling costs).",
        "use_case": "Ideal for analyzing duplex, triplex, quadplex, and small multifamily acquisitions (2-20 units) with detailed hold-period analysis and exit value projections.",
        "defaults": ACQ_DEFAULTS,
        "fields": ACQ_FIELDS,
        "prepare": acq_prepare_inputs,
        "db_model": SmallMultifamilyAcquisitionModel,
    },
    "hotel": {
        "label": "Hotel",
        "description": "Comprehensive hotel financial modeling covering rooms revenue, F&B operations, meeting/event spaces, and ancillary outlets with stabilized P&L projections.",
        "explanation": "**What it does:** Projects hotel performance using occupancy rates, ADR (Average Daily Rate), RevPAR, and revenue from multiple departments (rooms, F&B, spa, parking). Calculates GOP (Gross Operating Profit), NOI, and exit valuations.\n\n**Inputs needed:** Number of rooms, ADR, occupancy %, F&B revenue assumptions, operating expense ratios, management fees, FF&E reserves, purchase/development cost, financing structure, and exit cap rate. Model generates detailed P&L by department.",
        "use_case": "Designed for hotel acquisitions, developments, and repositioning strategies across all hotel segments (economy to luxury).",
        "defaults": HOTEL_DEFAULTS,
        "fields": HOTEL_FIELDS,
        "prepare": hotel_prepare_inputs,
        "db_model": HotelFinancialModel,
    },
    "extended_multifamily": {
        "label": "High-Rise Multifamily (7+ units)",
        "description": "Extended multifamily analysis for larger apartment buildings and high-rise developments with 7+ units, including detailed unit mix, lease-up schedules, and institutional-grade reporting.",
        "explanation": "**What it does:** Models large multifamily properties with sophisticated lease-up assumptions, unit mix optimization, operating expense analysis, and value-add business plans. Calculates equity multiples, IRR, and cash-on-cash returns.\n\n**Inputs needed:** Total units, unit mix breakdown, average rent by unit type, T12 operating expenses, CapEx budgets, financing structure, rent growth, expense growth, stabilization timeline, and exit assumptions. Produces 10-year cash flow projections.",
        "use_case": "Ideal for institutional multifamily investments, large apartment complexes, and high-rise residential developments (7+ units).",
        "defaults": EXT_MULTI_DEFAULTS,
        "fields": EXT_MULTI_FIELDS,
        "prepare": ext_multi_prepare_inputs,
        "db_model": HighRiseMultifamilyModel,
    },
    "mixed_use": {
        "label": "Mixed-Use Tower",
        "description": "Complex mixed-use development modeling combining residential, retail, office, and hotel components with integrated cash flow analysis and component-level financial tracking.",
        "explanation": "**What it does:** Analyzes mixed-use projects by modeling each component separately (residential condos/apartments, retail, office, hotel) and aggregating to project-level returns. Calculates weighted average cap rates, blended yields, and total project IRR.\n\n**Inputs needed:** Square footage and revenue assumptions for each component, component mix %, construction/development costs, phasing schedule, financing for each component, absorption rates, and exit strategies by component. Each component uses its respective industry assumptions.",
        "use_case": "Best for urban mixed-use towers combining multiple asset classes (residential + retail + office + hotel) in a single development.",
        "defaults": MIXED_USE_DEFAULTS,
        "fields": MIXED_USE_FIELDS,
        "prepare": mixed_use_prepare_inputs,
        "db_model": MixedUseDevelopmentModel,
    },
    "lease_analyzer": {
        "label": "Lease Analyzer",
        "description": "Comprehensive commercial lease analysis tool for evaluating lease rollover schedules, tenant improvements, leasing commissions, and property cash flows.",
        "explanation": "**What it does:** Analyzes commercial property leases by modeling lease expiry schedules, renewal probabilities, market rent assumptions, tenant improvement costs, and leasing commissions. Calculates NOI projections, cash flow impacts, and property valuation based on lease rollover.\n\n**Inputs needed:** Total square footage, number of tenants, weighted average rent, vacancy rate, operating expense ratio, weighted average lease term (WALT), lease expiry schedule by year, renewal probability, market rent, TI allowances, leasing commissions, and cap rate.",
        "use_case": "Ideal for analyzing office, retail, and industrial properties with complex lease structures and rollover schedules. Useful for acquisition underwriting and lease renewal strategy planning.",
        "defaults": LEASE_DEFAULTS,
        "fields": LEASE_FIELDS,
        "prepare": lease_prepare_inputs,
        "db_model": LeaseAnalyzerModel,
    },
    "renovation_budget": {
        "label": "Renovation Budget",
        "description": "Detailed renovation budget calculator for value-add multifamily and commercial properties with unit-by-unit cost tracking and ROI analysis.",
        "explanation": "**What it does:** Builds comprehensive renovation budgets by tracking interior improvements (kitchen, bathroom, flooring, paint, appliances, fixtures, HVAC, electrical, plumbing), exterior work, common areas, and major capital items. Calculates all-in costs including contingency, soft costs, financing, and holding costs. Projects revenue impact and renovation ROI.\n\n**Inputs needed:** Number of units, renovation costs per unit by category (kitchen, bathroom, flooring, etc.), common area costs, exterior improvements, contingency percentage, soft costs, current vs. post-renovation rents, occupancy assumptions, project timeline, and financing terms.",
        "use_case": "Perfect for value-add multifamily renovations, adaptive reuse projects, and repositioning strategies. Helps determine optimal renovation scope and budget to maximize returns.",
        "defaults": RENO_DEFAULTS,
        "fields": RENO_FIELDS,
        "prepare": reno_prepare_inputs,
        "db_model": RenovationBudgetModel,
    },
    "subdivision": {
        "label": "Subdivision / Condo Conversion",
        "description": "Analyze multi-unit subdivision and condo conversion opportunities with comprehensive exit strategy comparison including subdivide & sell, sell as-is, BRRRR, and hybrid approaches.",
        "explanation": "**What it does:** Evaluates the financial viability of purchasing multi-unit properties (duplex to 10-plex) and converting them to individual condominiums or subdividing them for separate sales. Compares multiple exit strategies: (1) Subdivide & Sell individually for maximum profit, (2) Sell As-Is to investors, (3) BRRRR (refinance and hold), (4) Hybrid (sell some, keep some). Tracks conversion costs (legal fees, surveys, HOA formation, title work), renovation budgets, cash flow timelines, and ROI for each strategy.\n\n**Inputs needed:** Property details (units, square footage, beds/baths), purchase price, financing terms, renovation costs per unit (kitchen, bathroom, flooring, etc.), conversion/subdivision costs (survey, legal, HOA, permits), individual condo sale prices, as-is multi-unit value, stabilized rental income, project timeline (acquisition, renovation, conversion approval, marketing), and operating expenses.",
        "use_case": "Ideal for duplex, triplex, and small multifamily investors looking to maximize returns through condo conversion, legal subdivision, or townhome creation. Analyzes whether the conversion premium (15-40% typical) justifies the additional time, cost, and complexity compared to selling as-is or holding as a rental.",
        "defaults": SUBDIVISION_DEFAULTS,
        "fields": SUBDIVISION_FIELDS,
        "prepare": subdivision_prepare_inputs,
        "db_model": SubdivisionModel,
    },
    "tax_strategy": {
        "label": "Tax Strategy Integration",
        "description": "Comprehensive tax planning and optimization toolkit including 1031 Exchange modeling, Cost Segregation analysis, Opportunity Zone benefits, Entity Structure comparison, Capital Gains calculations, and Depreciation Recapture analysis.",
        "explanation": "**What it does:** Analyzes multiple tax strategies to minimize tax liability and maximize after-tax returns. Includes: (1) 1031 Exchange - timeline tracking and replacement property requirements, (2) Cost Segregation - accelerated depreciation calculations, (3) Opportunity Zone - tax deferral and elimination modeling, (4) Entity Structure - LLC vs S-Corp vs Partnership comparison, (5) Capital Gains - long-term vs short-term with state taxes, (6) Depreciation Recapture - automatic calculation on exit.\n\n**Inputs needed:** Property value, purchase price and date, property type, accumulated depreciation, holding period, sale date, replacement property details, cost segregation percentages, OZ investment amounts and dates, current entity type, annual income, federal/state tax rates, and financial assumptions (appreciation, discount rate).",
        "use_case": "Essential for sophisticated real estate investors looking to optimize tax efficiency across their portfolio. Ideal for analyzing disposition strategies, entity restructuring, and evaluating tax-deferred exchange opportunities.",
        "defaults": TAX_DEFAULTS,
        "fields": TAX_FIELDS,
        "prepare": tax_prepare_inputs,
        "db_model": TaxStrategyModel,
    },
    "portfolio_dashboard": {
        "label": "Multi-Property Portfolio Dashboard",
        "description": "Comprehensive portfolio analytics dashboard featuring consolidated performance metrics, property comparison matrix, diversification analysis, rebalancing recommendations, and automated alerts for lease expirations and rate resets.",
        "explanation": "**What it does:** Provides institutional-grade portfolio management tools including: (1) Consolidated Performance Metrics - total portfolio value, aggregate cash flow, weighted average cap rate, combined equity & debt positions, portfolio-wide IRR; (2) Property Comparison Matrix - side-by-side analysis of all properties with key metrics; (3) Correlation Analysis - diversification scoring by asset type, geography, and concentration risk (HHI); (4) Rebalancing Recommendations - automated alerts when allocations drift beyond thresholds; (5) Alerts - proactive notifications for lease expirations and interest rate resets.\n\n**Inputs needed:** Portfolio properties with details (name, type, location, market, acquisition date, current value, debt balance, NOI, debt service, cap rate, occupancy, lease expiration, rate reset date), portfolio settings (target cash reserves, rebalancing thresholds, min/max allocations), and alert preferences (days before expiration/reset).",
        "use_case": "Perfect for real estate investors managing multiple properties who need comprehensive portfolio oversight, diversification tracking, risk management, and proactive alerts. Ideal for portfolios with 2+ properties across different markets or asset classes.",
        "defaults": PORTFOLIO_DEFAULTS,
        "fields": PORTFOLIO_FIELDS,
        "prepare": portfolio_prepare_inputs,
        "db_model": PortfolioModel,
    },
}


def _group_fields(fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Organize form fields into ordered sections for layout."""

    sections: List[Dict[str, Any]] = []
    for field in fields:
        section_label = field.get("section", "Inputs")
        if sections and sections[-1]["label"] == section_label:
            sections[-1]["fields"].append(field)
        else:
            sections.append({"label": section_label, "fields": [field]})
    return sections


@router.get("/tools", response_class=HTMLResponse)
async def render_tools_page(request: Request) -> HTMLResponse:
    """Render the model selection landing page."""

    context = {
        "request": request,
        "models": [
            {
                "slug": slug,
                "label": config["label"],
                "description": config.get("description", ""),
            }
            for slug, config in MODEL_REGISTRY.items()
        ],
    }
    return templates.TemplateResponse("real_estate/tools_index.html", context)


@router.get("/tools/{model_slug}", response_class=HTMLResponse)
async def render_model_page(request: Request, model_slug: str) -> HTMLResponse:
    """Render the fully interactive page for a specific model."""

    try:
        if model_slug not in MODEL_REGISTRY:
            raise HTTPException(status_code=404, detail="Unknown model")

        config = MODEL_REGISTRY[model_slug]

        context = {
            "request": request,
            "model_slug": model_slug,
            "model": {
                "slug": model_slug,
                "label": config["label"],
                "description": config.get("description", ""),
                "defaults": config["defaults"],
                "fields": config["fields"],
                "sections": _group_fields(config["fields"]),
            },
            "other_models": [
                {"slug": slug, "label": cfg["label"]}
                for slug, cfg in MODEL_REGISTRY.items()
                if slug != model_slug
            ],
        }

        return templates.TemplateResponse("real_estate/model_detail.html", context)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error rendering model page for {model_slug}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to render calculator: {str(e)}")


def _transform_chart_for_frontend(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Transform backend chart spec to frontend-compatible format."""

    # If chart already has nested 'data' structure, return as-is
    if "data" in chart and "labels" in chart.get("data", {}):
        return chart

    # Extract labels and datasets from root level
    labels = chart.get("labels", [])
    datasets = chart.get("datasets", [])

    # Handle both dict and list datasets
    if isinstance(datasets, dict):
        # Convert dict format to array format
        datasets = [
            {"label": label, "data": data}
            for label, data in datasets.items()
        ]
    elif not isinstance(datasets, list):
        datasets = []

    # Return transformed chart with nested data structure
    return {
        "title": chart.get("title", ""),
        "type": chart.get("type", "bar"),
        "key": chart.get("key", ""),
        "data": {
            "labels": labels,
            "datasets": datasets
        }
    }


@router.post("/tools/run")
async def run_model(payload: RunModelRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Execute a model run and return table/chart specifications."""

    try:
        if payload.model not in MODEL_REGISTRY:
            raise HTTPException(status_code=404, detail="Unknown model")

        config = MODEL_REGISTRY[payload.model]

        try:
            coerced = _coerce_inputs(config["defaults"], payload.values)
            prepared = config["prepare"](coerced)
        except Exception as e:
            print(f"Error preparing inputs for {payload.model}: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")

        # Run the model and get results
        try:
            if payload.model == "fix_and_flip":
                results = analyze_flip(prepared)
                tables = fix_tables(prepared, results)
                charts = [_transform_chart_for_frontend(c) for c in fix_chart_specs(results)]
                response = {"tables": tables, "charts": charts}
                full_results = results
            elif payload.model == "single_family_rental":
                sfr_output = sfr_build_projection(prepared)
                exit_metrics = compute_exit_comparison(prepared, sfr_output["metrics"], sfr_output["projections"])
                tables = sfr_tables(prepared, sfr_output["projections"], sfr_output["metrics"], exit_metrics)
                charts = [_transform_chart_for_frontend(c) for c in sfr_chart_specs(prepared, sfr_output["projections"], sfr_output["metrics"], exit_metrics)]
                response = {"tables": tables, "charts": charts}
                full_results = {**sfr_output, "exit_metrics": exit_metrics}
            elif payload.model == "small_multifamily":
                multi_output = multi_build_projection(prepared)
                tables = multi_tables(prepared, multi_output["projections"], multi_output["metrics"])
                charts = [_transform_chart_for_frontend(c) for c in multi_chart_specs(prepared, multi_output["projections"], multi_output["metrics"])]
                response = {"tables": tables, "charts": charts}
                full_results = multi_output
            elif payload.model == "small_multifamily_acquisition":
                acq_output = acq_build_projection(prepared)
                tables = acq_tables(prepared, acq_output["metrics"])
                response = {"tables": tables, "charts": []}
                full_results = acq_output
            elif payload.model == "extended_multifamily":
                ext_output = ext_multi_build_projection(prepared)
                tables = ext_multi_tables(prepared, ext_output["projections"], ext_output["metrics"])
                charts = [_transform_chart_for_frontend(c) for c in ext_multi_chart_specs(prepared, ext_output["projections"], ext_output["metrics"])]
                response = {"tables": tables, "charts": charts}
                full_results = ext_output
            elif payload.model == "mixed_use":
                mixed_output = mixed_use_build_projection(prepared)
                tables = mixed_use_tables(
                    prepared,
                    mixed_output["projections"],
                    mixed_output["component_details"],
                    mixed_output["metrics"],
                )
                charts = [_transform_chart_for_frontend(c) for c in mixed_use_chart_specs(
                    prepared,
                    mixed_output["projections"],
                    mixed_output["component_details"],
                    mixed_output["metrics"],
                )]
                response = {"tables": tables, "charts": charts}
                full_results = mixed_output
            elif payload.model == "lease_analyzer":
                lease_output = lease_build_projection(prepared)
                tables = lease_tables(prepared, lease_output["projections"], lease_output["metrics"])
                charts = [_transform_chart_for_frontend(c) for c in lease_chart_specs(prepared, lease_output["projections"], lease_output["metrics"])]
                response = {"tables": tables, "charts": charts}
                full_results = lease_output
            elif payload.model == "renovation_budget":
                reno_output = reno_build_projection(prepared)
                tables = reno_tables(prepared, reno_output["breakdown"], reno_output["metrics"])
                charts = [_transform_chart_for_frontend(c) for c in reno_chart_specs(prepared, reno_output["breakdown"], reno_output["metrics"])]
                response = {"tables": tables, "charts": charts}
                full_results = reno_output
            elif payload.model == "subdivision":
                subdivision_output = subdivision_build_projection(prepared)
                tables = subdivision_tables(prepared, subdivision_output["projections"], subdivision_output["metrics"])
                charts = [_transform_chart_for_frontend(c) for c in subdivision_chart_specs(prepared, subdivision_output["projections"], subdivision_output["metrics"])]
                response = {"tables": tables, "charts": charts}
                full_results = subdivision_output
            elif payload.model == "tax_strategy":
                tax_output = calculate_tax_strategy(prepared)
                tables = tax_tables(prepared, tax_output)
                charts = [_transform_chart_for_frontend(c) for c in tax_chart_specs(tax_output)]
                response = {"tables": tables, "charts": charts}
                full_results = tax_output
            elif payload.model == "portfolio_dashboard":
                portfolio_output = calculate_portfolio_dashboard(prepared)
                tables = portfolio_tables(prepared, portfolio_output)
                charts = [_transform_chart_for_frontend(c) for c in portfolio_chart_specs(portfolio_output)]
                response = {"tables": tables, "charts": charts}
                full_results = portfolio_output
            else:  # hotel
                hotel_summary = hotel_build_projection(prepared)
                tables = hotel_tables(prepared, hotel_summary)
                charts = [_transform_chart_for_frontend(c) for c in hotel_chart_specs(prepared, hotel_summary)]
                response = {"tables": tables, "charts": charts}
                full_results = hotel_summary
        except Exception as e:
            print(f"Error executing {payload.model} model: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Model execution failed: {str(e)}")

        # Save to database if requested
        if payload.save_to_db:
            try:
                db_model_class = config["db_model"]

                # Extract common fields from prepared inputs
                name = prepared.get("project_name") or prepared.get("name", "Untitled Project")
                location = prepared.get("location", "")
                analyst = prepared.get("analyst", "")
                notes = prepared.get("notes", "")

                # Create model-specific fields
                model_specific_fields = {}
                if payload.model == "fix_and_flip":
                    model_specific_fields["market_type"] = prepared.get("market_type", "Moderate")
                elif payload.model == "single_family_rental":
                    model_specific_fields["strategy"] = "buy_and_hold"
                elif payload.model == "small_multifamily":
                    model_specific_fields["asset_class"] = prepared.get("asset_class", "Value-Add")
                elif payload.model == "small_multifamily_acquisition":
                    model_specific_fields["property_type"] = prepared.get("property_type", "quadplex")
                    model_specific_fields["number_of_units"] = prepared.get("number_of_units", 4)
                elif payload.model == "extended_multifamily":
                    model_specific_fields["total_units"] = prepared.get("total_units", 0)
                elif payload.model == "hotel":
                    model_specific_fields["hotel_type"] = prepared.get("hotel_type", "Full-Service")
                elif payload.model == "mixed_use":
                    model_specific_fields["primary_mix"] = prepared.get("primary_mix", "Mixed")
                elif payload.model == "lease_analyzer":
                    model_specific_fields["property_type"] = prepared.get("property_type", "Office")
                elif payload.model == "renovation_budget":
                    model_specific_fields["property_type"] = prepared.get("property_type", "Multifamily")
                    model_specific_fields["total_units"] = prepared.get("total_units", 0)
                elif payload.model == "subdivision":
                    model_specific_fields["property_type"] = prepared.get("property_type", "Duplex")
                    model_specific_fields["num_units"] = prepared.get("num_units", 2)
                    # Determine best exit strategy based on ROI
                    metrics = full_results.get("metrics", {})
                    subdivide_roi = metrics.get("subdivide_roi", 0)
                    duplex_roi = metrics.get("duplex_roi", 0)
                    brrrr_roi = metrics.get("brrrr_roi", 0)
                    if subdivide_roi >= duplex_roi and subdivide_roi >= brrrr_roi:
                        model_specific_fields["exit_strategy"] = "Subdivide"
                    elif duplex_roi >= subdivide_roi and duplex_roi >= brrrr_roi:
                        model_specific_fields["exit_strategy"] = "As-Is"
                    else:
                        model_specific_fields["exit_strategy"] = "BRRRR"
                elif payload.model == "tax_strategy":
                    model_specific_fields["property_type"] = prepared.get("property_type", "Multifamily")
                    model_specific_fields["current_entity_type"] = prepared.get("current_entity_type", "LLC")
                    summary = full_results.get("summary", {})
                    model_specific_fields["total_tax_savings"] = int(summary.get("total_tax_savings", 0))
                elif payload.model == "portfolio_dashboard":
                    consolidated = full_results.get("consolidated_metrics", {})
                    correlation = full_results.get("correlation_analysis", {})
                    model_specific_fields["num_properties"] = consolidated.get("num_properties", 0)
                    model_specific_fields["total_portfolio_value"] = int(consolidated.get("total_portfolio_value", 0))
                    model_specific_fields["diversification_score"] = int(correlation.get("diversification_score", 0))

                # Create database record
                db_record = db_model_class(
                    name=name,
                    location=location,
                    analyst=analyst,
                    notes=notes,
                    model_version="1.0",
                    inputs=prepared,
                    results=full_results,
                    **model_specific_fields
                )

                db.add(db_record)
                db.commit()
                db.refresh(db_record)

                # Add the saved record ID to the response
                response["saved_id"] = str(db_record.id)
                response["saved_at"] = db_record.created_at.isoformat() if hasattr(db_record, 'created_at') else None
            except Exception as e:
                # Log error but don't fail the request
                print(f"Error saving to database: {e}")
                response["db_save_error"] = str(e)

        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in run_model: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")
