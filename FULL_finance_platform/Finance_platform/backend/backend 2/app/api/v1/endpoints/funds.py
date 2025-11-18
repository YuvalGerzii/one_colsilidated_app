"""Fund API endpoints."""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import fund_crud
from app.schemas.fund import FundCreate, FundUpdate, FundResponse

router = APIRouter()


@router.get("/", response_model=List[FundResponse])
def list_funds(
    skip: int = 0,
    limit: int = 100,
    vintage_year: int = None,
    db: Session = Depends(get_db)
):
    """List all funds."""
    if vintage_year:
        funds = fund_crud.get_by_vintage_year(db, vintage_year)
    else:
        funds = fund_crud.get_multi(db, skip=skip, limit=limit)
    return funds


@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
def create_fund(
    fund: FundCreate,
    db: Session = Depends(get_db)
):
    """Create a new fund."""
    return fund_crud.create(db, fund)


@router.get("/{fund_id}", response_model=FundResponse)
def get_fund(
    fund_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific fund by ID."""
    fund = fund_crud.get(db, fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund


@router.put("/{fund_id}", response_model=FundResponse)
def update_fund(
    fund_id: UUID,
    fund_update: FundUpdate,
    db: Session = Depends(get_db)
):
    """Update a fund."""
    fund = fund_crud.get(db, fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund_crud.update(db, fund, fund_update)


@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fund(
    fund_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a fund."""
    success = fund_crud.delete(db, fund_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fund not found")
