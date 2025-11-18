"""Interactive endpoints for real estate financial models."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

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
from app.scripts.real_estate.extended_multifamily_cli import (
    DEFAULT_INPUTS as EXT_MULTI_DEFAULTS,
    FORM_FIELDS as EXT_MULTI_FIELDS,
    build_chart_specs as ext_multi_chart_specs,
    build_projection as ext_multi_build_projection,
    build_report_tables as ext_multi_tables,
    prepare_inputs as ext_multi_prepare_inputs,
)

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[3] / "templates"))


class RunModelRequest(BaseModel):
    model: str
    values: Dict[str, Any]


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
        "description": "Analyze renovation projects with lender-style underwriting, 70% rule checks, and exit sensitivities.",
        "defaults": FIX_DEFAULTS,
        "fields": FIX_FIELDS,
        "prepare": fix_prepare_inputs,
    },
    "single_family_rental": {
        "label": "Single-Family Rental",
        "description": "Model BRRRR, refinance, and long-term hold strategies with full operating statements and exit pathways.",
        "defaults": SFR_DEFAULTS,
        "fields": SFR_FIELDS,
        "prepare": sfr_prepare_inputs,
    },
    "small_multifamily": {
        "label": "Small Multifamily",
        "description": "Evaluate value-add multifamily opportunities with unit-by-unit assumptions, financing, and disposition metrics.",
        "defaults": MULTI_DEFAULTS,
        "fields": MULTI_FIELDS,
        "prepare": multi_prepare_inputs,
    },
    "hotel": {
        "label": "Hotel",
        "description": "Project hotel P&Ls across rooms and ancillary outlets with stabilized performance and exit capitalization analysis.",
        "defaults": HOTEL_DEFAULTS,
        "fields": HOTEL_FIELDS,
        "prepare": hotel_prepare_inputs,
    },
    "extended_multifamily": {
        "label": "High-Rise Multifamily",
        "defaults": EXT_MULTI_DEFAULTS,
        "fields": EXT_MULTI_FIELDS,
        "prepare": ext_multi_prepare_inputs,
    },
    "mixed_use": {
        "label": "Mixed-Use Tower",
        "defaults": MIXED_USE_DEFAULTS,
        "fields": MIXED_USE_FIELDS,
        "prepare": mixed_use_prepare_inputs,
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
@router.get("/tools", response_class=HTMLResponse)
async def render_tools_page(request: Request) -> HTMLResponse:
    """Serve the interactive playground UI."""

    context = {
        "request": request,
        "model_configs": {
            slug: {
                "label": config["label"],
                "fields": config["fields"],
                "defaults": config["defaults"],
            }
            for slug, config in MODEL_REGISTRY.items()
        },
        "active_model": next(iter(MODEL_REGISTRY.keys())),
    }
    return templates.TemplateResponse("real_estate/tools.html", context)


@router.post("/tools/run")
async def run_model(payload: RunModelRequest) -> Dict[str, Any]:
    """Execute a model run and return table/chart specifications."""

    if payload.model not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail="Unknown model")

    config = MODEL_REGISTRY[payload.model]
    coerced = _coerce_inputs(config["defaults"], payload.values)
    prepared = config["prepare"](coerced)

    if payload.model == "fix_and_flip":
        results = analyze_flip(prepared)
        tables = fix_tables(prepared, results)
        charts = fix_chart_specs(results)
        response = {"tables": tables, "charts": charts}
    elif payload.model == "single_family_rental":
        sfr_output = sfr_build_projection(prepared)
        exit_metrics = compute_exit_comparison(prepared, sfr_output["metrics"], sfr_output["projections"])
        tables = sfr_tables(prepared, sfr_output["projections"], sfr_output["metrics"], exit_metrics)
        charts = sfr_chart_specs(prepared, sfr_output["projections"], sfr_output["metrics"], exit_metrics)
        response = {"tables": tables, "charts": charts}
    elif payload.model == "small_multifamily":
        multi_output = multi_build_projection(prepared)
        tables = multi_tables(prepared, multi_output["projections"], multi_output["metrics"])
        charts = multi_chart_specs(prepared, multi_output["projections"], multi_output["metrics"])
        response = {"tables": tables, "charts": charts}
    elif payload.model == "extended_multifamily":
        ext_output = ext_multi_build_projection(prepared)
        tables = ext_multi_tables(prepared, ext_output["projections"], ext_output["metrics"])
        charts = ext_multi_chart_specs(prepared, ext_output["projections"], ext_output["metrics"])
        response = {"tables": tables, "charts": charts}
    elif payload.model == "mixed_use":
        mixed_output = mixed_use_build_projection(prepared)
        tables = mixed_use_tables(
            prepared,
            mixed_output["projections"],
            mixed_output["component_details"],
            mixed_output["metrics"],
        )
        charts = mixed_use_chart_specs(
            prepared,
            mixed_output["projections"],
            mixed_output["component_details"],
            mixed_output["metrics"],
        )
        response = {"tables": tables, "charts": charts}
    else:
        hotel_summary = hotel_build_projection(prepared)
        tables = hotel_tables(prepared, hotel_summary)
        charts = hotel_chart_specs(prepared, hotel_summary)
        response = {"tables": tables, "charts": charts}

    return response
