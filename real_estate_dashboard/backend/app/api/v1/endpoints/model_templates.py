"""
Model Templates & Presets API Endpoints

Endpoints for:
- Template library management
- One-click model duplication
- Side-by-side model comparison
- Industry-standard presets
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.model_templates import (
    ModelTemplate, TemplateCategory, TemplateType, TemplateScope,
    TemplateUsageLog, ModelComparison, PresetAssumptionSet, ModelClone
)

router = APIRouter()


# ================================
# PYDANTIC SCHEMAS
# ================================

class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: TemplateCategory
    template_type: TemplateType
    scope: TemplateScope = TemplateScope.USER
    assumptions: dict
    configuration: Optional[dict] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    industry_sector: Optional[str] = None
    tags: Optional[List[str]] = None
    version: Optional[str] = None
    is_published: bool = False


class TemplateCreate(TemplateBase):
    company_id: Optional[UUID] = None
    is_default: bool = False


class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    assumptions: Optional[dict] = None
    configuration: Optional[dict] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    industry_sector: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None


class TemplateResponse(TemplateBase):
    id: UUID
    company_id: Optional[UUID]
    user_id: Optional[UUID]
    is_default: bool
    usage_count: int
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    id: UUID
    name: str
    category: TemplateCategory
    template_type: TemplateType
    scope: TemplateScope
    property_type: Optional[str]
    market: Optional[str]
    is_default: bool
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PresetAssumptionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: TemplateCategory
    property_type: Optional[str] = None
    market: Optional[str] = None
    industry: Optional[str] = None
    assumptions: dict
    source: Optional[str] = None
    source_date: Optional[date] = None
    confidence_level: Optional[str] = None
    version: Optional[str] = None


class PresetAssumptionResponse(PresetAssumptionBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ModelCloneRequest(BaseModel):
    source_model_id: str
    source_model_type: str
    clone_type: str = "full_copy"
    modifications: Optional[dict] = None
    new_name: Optional[str] = None


class ModelCloneResponse(BaseModel):
    id: UUID
    source_model_id: str
    cloned_model_id: str
    clone_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class ModelComparisonCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    model_type: str
    model_ids: List[str] = Field(..., min_items=2, max_items=10)
    comparison_metrics: Optional[dict] = None
    display_settings: Optional[dict] = None
    is_shared: bool = False
    shared_with_users: Optional[List[UUID]] = None


class ModelComparisonResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    model_type: str
    model_ids: List[str]
    comparison_metrics: Optional[dict]
    display_settings: Optional[dict]
    is_shared: bool
    user_id: UUID
    company_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


# ================================
# TEMPLATE ENDPOINTS
# ================================

@router.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: TemplateCreate,
    user_id: UUID = Query(..., description="Current user ID"),
    db: Session = Depends(get_db)
):
    """
    Create a new model template.

    Templates can be:
    - User-specific (scope=USER)
    - Company-wide (scope=COMPANY)
    - System defaults (scope=SYSTEM - admin only)
    """
    template = ModelTemplate(
        **template_data.model_dump(exclude={'company_id'}),
        user_id=user_id,
        company_id=template_data.company_id
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return template


@router.get("/templates", response_model=List[TemplateListResponse])
async def list_templates(
    category: Optional[TemplateCategory] = Query(None),
    template_type: Optional[TemplateType] = Query(None),
    scope: Optional[TemplateScope] = Query(None),
    property_type: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    user_id: Optional[UUID] = Query(None),
    company_id: Optional[UUID] = Query(None),
    include_defaults_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """
    List available templates with optional filters.

    Returns templates visible to the user:
    - System templates (always visible)
    - Company templates (if company_id provided)
    - User templates (if user_id provided)
    - Public templates
    """
    query = db.query(ModelTemplate).filter(ModelTemplate.deleted_at.is_(None))

    # Apply filters
    if category:
        query = query.filter(ModelTemplate.category == category)

    if template_type:
        query = query.filter(ModelTemplate.template_type == template_type)

    if scope:
        query = query.filter(ModelTemplate.scope == scope)
    else:
        # Default: show system, company, user, and public templates
        visibility_filter = or_(
            ModelTemplate.scope == TemplateScope.SYSTEM,
            ModelTemplate.scope == TemplateScope.PUBLIC
        )
        if company_id:
            visibility_filter = or_(
                visibility_filter,
                and_(ModelTemplate.scope == TemplateScope.COMPANY, ModelTemplate.company_id == company_id)
            )
        if user_id:
            visibility_filter = or_(
                visibility_filter,
                and_(ModelTemplate.scope == TemplateScope.USER, ModelTemplate.user_id == user_id)
            )
        query = query.filter(visibility_filter)

    if property_type:
        query = query.filter(ModelTemplate.property_type == property_type)

    if market:
        query = query.filter(ModelTemplate.market == market)

    if include_defaults_only:
        query = query.filter(ModelTemplate.is_default == True)

    # Order by usage and date
    query = query.order_by(desc(ModelTemplate.is_default), desc(ModelTemplate.usage_count), desc(ModelTemplate.created_at))

    templates = query.all()
    return templates


@router.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID with full details."""
    template = db.query(ModelTemplate).filter(
        ModelTemplate.id == template_id,
        ModelTemplate.deleted_at.is_(None)
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    return template


@router.patch("/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: UUID,
    template_data: TemplateUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing template."""
    template = db.query(ModelTemplate).filter(
        ModelTemplate.id == template_id,
        ModelTemplate.deleted_at.is_(None)
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    # Update fields
    update_data = template_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    db.commit()
    db.refresh(template)

    return template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Soft delete a template."""
    template = db.query(ModelTemplate).filter(
        ModelTemplate.id == template_id,
        ModelTemplate.deleted_at.is_(None)
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    template.deleted_at = datetime.utcnow()
    db.commit()


@router.post("/templates/{template_id}/apply")
async def apply_template(
    template_id: UUID,
    model_type: str = Query(..., description="Type of model to create"),
    user_id: UUID = Query(...),
    company_id: Optional[UUID] = Query(None),
    overrides: Optional[dict] = Body(None, description="Override specific assumptions"),
    db: Session = Depends(get_db)
):
    """
    Apply a template to create a new model instance.

    This endpoint returns the template data that should be used to initialize
    a new model of the specified type.
    """
    template = db.query(ModelTemplate).filter(
        ModelTemplate.id == template_id,
        ModelTemplate.deleted_at.is_(None)
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    # Increment usage counter
    template.usage_count += 1
    template.last_used_at = datetime.utcnow()

    # Log usage
    usage_log = TemplateUsageLog(
        template_id=template_id,
        user_id=user_id,
        company_id=company_id,
        model_type=model_type,
        action="applied"
    )
    db.add(usage_log)

    db.commit()

    # Merge template assumptions with overrides
    final_assumptions = {**template.assumptions}
    if overrides:
        final_assumptions.update(overrides)

    return {
        "template_id": template_id,
        "model_type": model_type,
        "assumptions": final_assumptions,
        "configuration": template.configuration,
        "metadata": {
            "template_name": template.name,
            "property_type": template.property_type,
            "market": template.market
        }
    }


# ================================
# MODEL CLONING ENDPOINTS
# ================================

@router.post("/models/clone", response_model=ModelCloneResponse)
async def clone_model(
    clone_request: ModelCloneRequest,
    user_id: UUID = Query(...),
    company_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Clone/duplicate an existing model.

    This creates a lineage record but returns the data needed to create
    the duplicate. The actual model creation happens client-side or through
    the specific model's API.
    """
    # Create clone record for lineage tracking
    clone_record = ModelClone(
        source_model_type=clone_request.source_model_type,
        source_model_id=clone_request.source_model_id,
        cloned_model_type=clone_request.source_model_type,  # Usually same type
        cloned_model_id=f"pending_{datetime.utcnow().timestamp()}",  # Temporary ID
        user_id=user_id,
        company_id=company_id,
        clone_type=clone_request.clone_type,
        modifications=clone_request.modifications
    )

    db.add(clone_record)
    db.commit()
    db.refresh(clone_record)

    return clone_record


@router.get("/models/clones", response_model=List[ModelCloneResponse])
async def list_model_clones(
    source_model_id: Optional[str] = Query(None),
    cloned_model_id: Optional[str] = Query(None),
    model_type: Optional[str] = Query(None),
    user_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """List model cloning history."""
    query = db.query(ModelClone)

    if source_model_id:
        query = query.filter(ModelClone.source_model_id == source_model_id)

    if cloned_model_id:
        query = query.filter(ModelClone.cloned_model_id == cloned_model_id)

    if model_type:
        query = query.filter(ModelClone.source_model_type == model_type)

    if user_id:
        query = query.filter(ModelClone.user_id == user_id)

    query = query.order_by(desc(ModelClone.created_at))

    return query.all()


# ================================
# MODEL COMPARISON ENDPOINTS
# ================================

@router.post("/comparisons", response_model=ModelComparisonResponse, status_code=status.HTTP_201_CREATED)
async def create_comparison(
    comparison_data: ModelComparisonCreate,
    user_id: UUID = Query(...),
    company_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Create a new model comparison configuration for side-by-side analysis.
    """
    comparison = ModelComparison(
        **comparison_data.model_dump(),
        user_id=user_id,
        company_id=company_id
    )

    db.add(comparison)
    db.commit()
    db.refresh(comparison)

    return comparison


@router.get("/comparisons", response_model=List[ModelComparisonResponse])
async def list_comparisons(
    user_id: Optional[UUID] = Query(None),
    company_id: Optional[UUID] = Query(None),
    model_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List saved model comparisons."""
    query = db.query(ModelComparison).filter(ModelComparison.deleted_at.is_(None))

    if user_id:
        # Show user's comparisons or shared comparisons
        query = query.filter(
            or_(
                ModelComparison.user_id == user_id,
                ModelComparison.is_shared == True
            )
        )

    if company_id:
        query = query.filter(ModelComparison.company_id == company_id)

    if model_type:
        query = query.filter(ModelComparison.model_type == model_type)

    query = query.order_by(desc(ModelComparison.created_at))

    return query.all()


@router.get("/comparisons/{comparison_id}", response_model=ModelComparisonResponse)
async def get_comparison(
    comparison_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific comparison configuration."""
    comparison = db.query(ModelComparison).filter(
        ModelComparison.id == comparison_id,
        ModelComparison.deleted_at.is_(None)
    ).first()

    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )

    return comparison


@router.delete("/comparisons/{comparison_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comparison(
    comparison_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a comparison configuration."""
    comparison = db.query(ModelComparison).filter(
        ModelComparison.id == comparison_id,
        ModelComparison.deleted_at.is_(None)
    ).first()

    if not comparison:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparison not found"
        )

    comparison.deleted_at = datetime.utcnow()
    db.commit()


# ================================
# PRESET ASSUMPTIONS ENDPOINTS
# ================================

@router.get("/presets", response_model=List[PresetAssumptionResponse])
async def list_preset_assumptions(
    category: Optional[TemplateCategory] = Query(None),
    property_type: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List industry-standard preset assumption sets.

    These are curated assumptions based on industry data sources like:
    - NCREIF property indices
    - CoStar market reports
    - Industry benchmarks
    """
    query = db.query(PresetAssumptionSet).filter(PresetAssumptionSet.is_active == True)

    if category:
        query = query.filter(PresetAssumptionSet.category == category)

    if property_type:
        query = query.filter(PresetAssumptionSet.property_type == property_type)

    if market:
        query = query.filter(PresetAssumptionSet.market == market)

    if industry:
        query = query.filter(PresetAssumptionSet.industry == industry)

    query = query.order_by(desc(PresetAssumptionSet.source_date))

    return query.all()


@router.get("/presets/{preset_id}", response_model=PresetAssumptionResponse)
async def get_preset_assumption(
    preset_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific preset assumption set."""
    preset = db.query(PresetAssumptionSet).filter(
        PresetAssumptionSet.id == preset_id,
        PresetAssumptionSet.is_active == True
    ).first()

    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preset not found"
        )

    return preset


# ================================
# UTILITY ENDPOINTS
# ================================

@router.get("/templates/recommend")
async def recommend_templates(
    model_type: str = Query(...),
    property_type: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    company_id: Optional[UUID] = Query(None),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get recommended templates based on context.

    Recommendations are based on:
    - Model type match
    - Property type match
    - Market similarity
    - Usage popularity
    - Default templates
    """
    query = db.query(ModelTemplate).filter(
        ModelTemplate.deleted_at.is_(None),
        ModelTemplate.template_type.in_([TemplateType(model_type)])  # Match model type
    )

    # Prioritize matching criteria
    if property_type:
        query = query.filter(ModelTemplate.property_type == property_type)

    if market:
        query = query.filter(ModelTemplate.market == market)

    # Order by relevance
    query = query.order_by(
        desc(ModelTemplate.is_default),
        desc(ModelTemplate.usage_count),
        desc(ModelTemplate.created_at)
    ).limit(limit)

    templates = query.all()

    return {
        "recommendations": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "usage_count": t.usage_count,
                "is_default": t.is_default,
                "match_score": calculate_match_score(t, model_type, property_type, market)
            }
            for t in templates
        ]
    }


def calculate_match_score(template, model_type: str, property_type: Optional[str], market: Optional[str]) -> float:
    """Calculate relevance score for template recommendation."""
    score = 0.0

    # Base score for being a default
    if template.is_default:
        score += 50.0

    # Usage popularity (log scale)
    import math
    if template.usage_count > 0:
        score += min(math.log(template.usage_count + 1) * 10, 30.0)

    # Exact matches
    if property_type and template.property_type == property_type:
        score += 15.0

    if market and template.market == market:
        score += 10.0

    # Recency bonus
    days_old = (datetime.utcnow() - template.created_at).days
    if days_old < 90:
        score += 5.0

    return round(score, 2)


__all__ = ["router"]
