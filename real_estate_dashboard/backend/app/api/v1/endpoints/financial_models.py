"""
Financial Models API Endpoints

This module provides REST API endpoints for DCF and LBO financial models.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel as PydanticBase, Field

from app.api.deps import get_db
from app.core.auth import get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.financial_models import DCFModel, LBOModel, ComparableCompany


router = APIRouter()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class DCFModelCreate(PydanticBase):
    """Schema for creating a DCF model"""
    name: str
    company_name: Optional[str] = None
    ticker: Optional[str] = None
    description: Optional[str] = None
    current_stock_price: Optional[float] = None
    shares_outstanding: Optional[float] = None
    revenue_projections: Optional[dict] = None
    ebitda_margins: Optional[dict] = None
    capex_assumptions: Optional[dict] = None
    nwc_assumptions: Optional[dict] = None
    dna_assumptions: Optional[dict] = None
    risk_free_rate: Optional[float] = None
    beta: Optional[float] = None
    market_risk_premium: Optional[float] = None
    cost_of_debt: Optional[float] = None
    tax_rate: Optional[float] = None
    debt_to_equity: Optional[float] = None
    terminal_growth_rate: Optional[float] = None
    exit_multiple: Optional[float] = None
    terminal_method: Optional[str] = None
    cash: Optional[float] = None
    total_debt: Optional[float] = None
    preferred_stock: Optional[float] = None
    minority_interest: Optional[float] = None
    results: Optional[dict] = None
    sensitivity_analysis: Optional[dict] = None
    scenario_analysis: Optional[dict] = None
    trading_comps: Optional[dict] = None
    historical_financials: Optional[dict] = None


class DCFModelUpdate(PydanticBase):
    """Schema for updating a DCF model"""
    name: Optional[str] = None
    company_name: Optional[str] = None
    ticker: Optional[str] = None
    description: Optional[str] = None
    current_stock_price: Optional[float] = None
    shares_outstanding: Optional[float] = None
    revenue_projections: Optional[dict] = None
    ebitda_margins: Optional[dict] = None
    capex_assumptions: Optional[dict] = None
    nwc_assumptions: Optional[dict] = None
    dna_assumptions: Optional[dict] = None
    risk_free_rate: Optional[float] = None
    beta: Optional[float] = None
    market_risk_premium: Optional[float] = None
    cost_of_debt: Optional[float] = None
    tax_rate: Optional[float] = None
    debt_to_equity: Optional[float] = None
    terminal_growth_rate: Optional[float] = None
    exit_multiple: Optional[float] = None
    terminal_method: Optional[str] = None
    cash: Optional[float] = None
    total_debt: Optional[float] = None
    preferred_stock: Optional[float] = None
    minority_interest: Optional[float] = None
    results: Optional[dict] = None
    sensitivity_analysis: Optional[dict] = None
    scenario_analysis: Optional[dict] = None
    trading_comps: Optional[dict] = None
    historical_financials: Optional[dict] = None


class LBOModelCreate(PydanticBase):
    """Schema for creating an LBO model"""
    name: str
    company_name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    transaction_date: Optional[str] = None
    holding_period: Optional[int] = None
    ltm_revenue: Optional[float] = None
    ltm_ebitda: Optional[float] = None
    entry_ev_revenue_multiple: Optional[float] = None
    entry_ev_ebitda_multiple: Optional[float] = None
    purchase_price: Optional[float] = None
    total_leverage: Optional[float] = None
    senior_leverage: Optional[float] = None
    sources: Optional[dict] = None
    uses: Optional[dict] = None
    ma_fees_pct: Optional[float] = None
    legal_fees: Optional[float] = None
    financing_fees_pct: Optional[float] = None
    debt_schedule: Optional[dict] = None
    revenue_projections: Optional[dict] = None
    ebitda_margins: Optional[dict] = None
    capex_assumptions: Optional[dict] = None
    nwc_assumptions: Optional[dict] = None
    dna_expense: Optional[dict] = None
    exit_ev_ebitda_multiple: Optional[float] = None
    preferred_return: Optional[float] = None
    gp_catchup_pct: Optional[float] = None
    carried_interest_pct: Optional[float] = None
    results: Optional[dict] = None
    credit_metrics: Optional[dict] = None
    sensitivity_analysis: Optional[dict] = None
    distribution_waterfall: Optional[dict] = None


class LBOModelUpdate(PydanticBase):
    """Schema for updating an LBO model"""
    name: Optional[str] = None
    company_name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    transaction_date: Optional[str] = None
    holding_period: Optional[int] = None
    ltm_revenue: Optional[float] = None
    ltm_ebitda: Optional[float] = None
    entry_ev_revenue_multiple: Optional[float] = None
    entry_ev_ebitda_multiple: Optional[float] = None
    purchase_price: Optional[float] = None
    total_leverage: Optional[float] = None
    senior_leverage: Optional[float] = None
    sources: Optional[dict] = None
    uses: Optional[dict] = None
    ma_fees_pct: Optional[float] = None
    legal_fees: Optional[float] = None
    financing_fees_pct: Optional[float] = None
    debt_schedule: Optional[dict] = None
    revenue_projections: Optional[dict] = None
    ebitda_margins: Optional[dict] = None
    capex_assumptions: Optional[dict] = None
    nwc_assumptions: Optional[dict] = None
    dna_expense: Optional[dict] = None
    exit_ev_ebitda_multiple: Optional[float] = None
    preferred_return: Optional[float] = None
    gp_catchup_pct: Optional[float] = None
    carried_interest_pct: Optional[float] = None
    results: Optional[dict] = None
    credit_metrics: Optional[dict] = None
    sensitivity_analysis: Optional[dict] = None
    distribution_waterfall: Optional[dict] = None


# ============================================================================
# DCF Model Endpoints
# ============================================================================

@router.post("/dcf", status_code=status.HTTP_201_CREATED)
def create_dcf_model(
    model_data: DCFModelCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new DCF model"""
    current_user, company = user_company

    model = DCFModel(
        **model_data.dict(),
        company_id=company.id if company else None
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model.to_dict()


@router.get("/dcf")
def list_dcf_models(
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """List all DCF models"""
    current_user, company = user_company

    query = db.query(DCFModel).filter(
        DCFModel.deleted_at.is_(None)
    )

    # Filter by company_id if user has a company
    if company:
        query = query.filter(DCFModel.company_id == company.id)

    models = query.offset(skip).limit(limit).all()
    return [model.to_dict() for model in models]


@router.get("/dcf/{model_id}")
def get_dcf_model(
    model_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get a specific DCF model by ID"""
    current_user, company = user_company

    filters = [
        DCFModel.id == model_id,
        DCFModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(DCFModel.company_id == company.id)

    model = db.query(DCFModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DCF model not found"
        )

    return model.to_dict()


@router.put("/dcf/{model_id}")
def update_dcf_model(
    model_id: UUID,
    model_data: DCFModelUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Update a DCF model"""
    current_user, company = user_company

    filters = [
        DCFModel.id == model_id,
        DCFModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(DCFModel.company_id == company.id)

    model = db.query(DCFModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DCF model not found"
        )

    # Update only provided fields
    update_data = model_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)

    db.commit()
    db.refresh(model)
    return model.to_dict()


@router.delete("/dcf/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dcf_model(
    model_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Soft delete a DCF model"""
    current_user, company = user_company

    filters = [
        DCFModel.id == model_id,
        DCFModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(DCFModel.company_id == company.id)

    model = db.query(DCFModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DCF model not found"
        )

    model.soft_delete()
    db.commit()
    return None


# ============================================================================
# LBO Model Endpoints
# ============================================================================

@router.post("/lbo", status_code=status.HTTP_201_CREATED)
def create_lbo_model(
    model_data: LBOModelCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new LBO model"""
    current_user, company = user_company

    model = LBOModel(
        **model_data.dict(),
        company_id=company.id if company else None
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model.to_dict()


@router.get("/lbo")
def list_lbo_models(
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """List all LBO models"""
    current_user, company = user_company

    query = db.query(LBOModel).filter(
        LBOModel.deleted_at.is_(None)
    )

    # Filter by company_id if user has a company
    if company:
        query = query.filter(LBOModel.company_id == company.id)

    models = query.offset(skip).limit(limit).all()
    return [model.to_dict() for model in models]


@router.get("/lbo/{model_id}")
def get_lbo_model(
    model_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get a specific LBO model by ID"""
    current_user, company = user_company

    filters = [
        LBOModel.id == model_id,
        LBOModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(LBOModel.company_id == company.id)

    model = db.query(LBOModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LBO model not found"
        )

    return model.to_dict()


@router.put("/lbo/{model_id}")
def update_lbo_model(
    model_id: UUID,
    model_data: LBOModelUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Update an LBO model"""
    current_user, company = user_company

    filters = [
        LBOModel.id == model_id,
        LBOModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(LBOModel.company_id == company.id)

    model = db.query(LBOModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LBO model not found"
        )

    # Update only provided fields
    update_data = model_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)

    db.commit()
    db.refresh(model)
    return model.to_dict()


@router.delete("/lbo/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lbo_model(
    model_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Soft delete an LBO model"""
    current_user, company = user_company

    filters = [
        LBOModel.id == model_id,
        LBOModel.deleted_at.is_(None)
    ]

    if company:
        filters.append(LBOModel.company_id == company.id)

    model = db.query(LBOModel).filter(*filters).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LBO model not found"
        )

    model.soft_delete()
    db.commit()
    return None
