"""Financial metrics API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import financial_metric_crud
from app.schemas.financial_metric import (
    FinancialMetricCreate, 
    FinancialMetricUpdate, 
    FinancialMetricResponse
)

router = APIRouter()


@router.get("/", response_model=List[FinancialMetricResponse])
def list_financials(
    company_id: UUID,
    period_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List financial metrics for a company."""
    return financial_metric_crud.get_by_company(
        db, company_id, period_type, skip, limit
    )


@router.post("/", response_model=FinancialMetricResponse, status_code=status.HTTP_201_CREATED)
def create_financial(
    financial: FinancialMetricCreate,
    db: Session = Depends(get_db)
):
    """Create a new financial metric."""
    return financial_metric_crud.create(db, financial)


@router.get("/{financial_id}", response_model=FinancialMetricResponse)
def get_financial(
    financial_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific financial metric by ID."""
    financial = financial_metric_crud.get(db, financial_id)
    if not financial:
        raise HTTPException(status_code=404, detail="Financial metric not found")
    return financial


@router.put("/{financial_id}", response_model=FinancialMetricResponse)
def update_financial(
    financial_id: UUID,
    financial_update: FinancialMetricUpdate,
    db: Session = Depends(get_db)
):
    """Update a financial metric."""
    financial = financial_metric_crud.get(db, financial_id)
    if not financial:
        raise HTTPException(status_code=404, detail="Financial metric not found")
    return financial_metric_crud.update(db, financial, financial_update)


@router.delete("/{financial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_financial(
    financial_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a financial metric."""
    success = financial_metric_crud.delete(db, financial_id)
    if not success:
        raise HTTPException(status_code=404, detail="Financial metric not found")
