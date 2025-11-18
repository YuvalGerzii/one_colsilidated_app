"""Endpoints powering the corporate finance modeling workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.scripts.corporate_finance import (
    COMPARISON_DEFAULTS,
    COMPARISON_FIELDS,
    DCF_DEFAULTS,
    DCF_FIELDS,
    LBO_DEFAULTS,
    LBO_FIELDS,
    comparison_run,
    dcf_build_projection,
    dcf_chart_specs,
    dcf_compute_valuation,
    dcf_prepare_inputs,
    dcf_tables,
    lbo_build_projection,
    lbo_chart_specs,
    lbo_compute_valuation,
    lbo_prepare_inputs,
    lbo_tables,
)

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[3] / "templates"))


class RunFinanceModelRequest(BaseModel):
    model: str
    values: Dict[str, Any]


def _coerce_inputs(defaults: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {**defaults}
    for key, value in overrides.items():
        if key not in merged:
            continue
        default_value = merged[key]
        if isinstance(default_value, (int, float)):
            try:
                merged[key] = float(value)
            except (TypeError, ValueError):
                continue
        else:
            merged[key] = value
    return merged


MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "dcf": {
        "label": "Discounted Cash Flow",
        "description": "Project unlevered free cash flows and value the company using a traditional DCF methodology.",
        "defaults": DCF_DEFAULTS,
        "fields": DCF_FIELDS,
        "prepare": dcf_prepare_inputs,
    },
    "lbo": {
        "label": "Leveraged Buyout",
        "description": "Model a sponsor-style LBO with debt schedules, equity cash flows, and exit valuation metrics.",
        "defaults": LBO_DEFAULTS,
        "fields": LBO_FIELDS,
        "prepare": lbo_prepare_inputs,
    },
    "comparisons": {
        "label": "Valuation Comparisons",
        "description": "Compare valuation outputs across DCF, LBO, trading comps, and precedent transactions.",
        "defaults": COMPARISON_DEFAULTS,
        "fields": COMPARISON_FIELDS,
        "prepare": lambda values: values,  # coercion handled in run path
    },
}


def _group_fields(fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []
    for field in fields:
        section_label = field.get("section", "Inputs")
        if sections and sections[-1]["label"] == section_label:
            sections[-1]["fields"].append(field)
        else:
            sections.append({"label": section_label, "fields": [field]})
    return sections


@router.get("/models", response_class=HTMLResponse)
async def render_finance_models(request: Request) -> HTMLResponse:
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
    return templates.TemplateResponse("finance/tools_index.html", context)


@router.get("/models/{model_slug}", response_class=HTMLResponse)
async def render_finance_model(request: Request, model_slug: str) -> HTMLResponse:
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
    return templates.TemplateResponse("finance/model_detail.html", context)


@router.post("/models/run")
async def run_finance_model(payload: RunFinanceModelRequest) -> Dict[str, Any]:
    if payload.model not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail="Unknown model")

    config = MODEL_REGISTRY[payload.model]
    defaults = config["defaults"]
    coerced = _coerce_inputs(defaults, payload.values)

    if payload.model == "dcf":
        prepared = dcf_prepare_inputs(coerced)
        projection = dcf_build_projection(prepared)
        valuation = dcf_compute_valuation(prepared, projection)
        tables = dcf_tables(prepared, projection, valuation)
        charts = dcf_chart_specs(prepared, projection, valuation)
        return {"tables": tables, "charts": charts}
    if payload.model == "lbo":
        prepared = lbo_prepare_inputs(coerced)
        schedule = lbo_build_projection(prepared)
        valuation = lbo_compute_valuation(prepared, schedule)
        tables = lbo_tables(prepared, schedule, valuation)
        charts = lbo_chart_specs(prepared, schedule, valuation)
        return {"tables": tables, "charts": charts}

    # comparisons run their own coercion/validation
    comparison_result = comparison_run(coerced)
    return comparison_result
