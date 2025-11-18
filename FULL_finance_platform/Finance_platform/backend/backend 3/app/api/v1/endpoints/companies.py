"""Company API endpoints."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import company_crud
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse

router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
def list_companies(
    skip: int = 0,
    limit: int = 100,
    fund_id: Optional[UUID] = None,
    sector: Optional[str] = None,
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """List all portfolio companies."""
    if fund_id:
        companies = company_crud.get_by_fund(db, fund_id, skip, limit)
    elif sector:
        companies = company_crud.get_by_sector(db, sector, skip, limit)
    elif status == "Active":
        companies = company_crud.get_active(db, skip, limit)
    else:
        companies = company_crud.get_multi(db, skip=skip, limit=limit)
    return companies


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    """Create a new portfolio company."""
    return company_crud.create(db, company)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific company by ID."""
    company = company_crud.get(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: UUID,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """Update a company."""
    company = company_crud.get(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_crud.update(db, company, company_update)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db)
):
    """Soft delete a company."""
    success = company_crud.soft_delete(db, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
