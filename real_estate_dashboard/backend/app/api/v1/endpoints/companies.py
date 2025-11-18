"""
Company Management API Endpoints

This module provides REST API endpoints for managing companies in the multi-tenant
property management system. Each company represents an isolated workspace.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.company import Company


router = APIRouter()


# Pydantic Schemas

class CompanyBase(BaseModel):
    """Base company schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Company name (must be unique)")
    details: Optional[str] = Field(None, description="Company description and details")
    region: Optional[str] = Field(None, max_length=100, description="Primary region/location")
    contact_info: Optional[str] = Field(None, description="Contact information (email, phone, address)")
    logo_url: Optional[str] = Field(None, max_length=500, description="URL to company logo")


class CompanyCreate(CompanyBase):
    """Schema for creating a new company"""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating an existing company"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    details: Optional[str] = None
    region: Optional[str] = Field(None, max_length=100)
    contact_info: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=500)


class CompanyResponse(CompanyBase):
    """Schema for company response with additional metadata"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    property_count: int = Field(0, description="Number of active properties")

    class Config:
        from_attributes = True


class CompanySummary(BaseModel):
    """Lightweight company summary for dropdown/list views"""
    id: UUID
    name: str
    region: Optional[str]

    class Config:
        from_attributes = True


# API Endpoints

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new company workspace.

    - **name**: Company name (required, must be unique)
    - **details**: Additional company information
    - **region**: Primary operating region
    - **contact_info**: Contact details
    - **logo_url**: URL to company logo
    """
    # Check if company name already exists
    existing = db.query(Company).filter(
        Company.name == company_data.name,
        Company.deleted_at.is_(None)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Company with name '{company_data.name}' already exists"
        )

    # Create new company
    company = Company(**company_data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)

    return company


@router.get("/", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    region: Optional[str] = Query(None, description="Filter by region"),
    search: Optional[str] = Query(None, description="Search in company name"),
    db: Session = Depends(get_db),
):
    """
    List all active companies with optional filtering.

    - **skip**: Pagination offset
    - **limit**: Maximum number of results (max 500)
    - **region**: Filter by specific region
    - **search**: Search companies by name
    """
    query = db.query(Company).filter(Company.deleted_at.is_(None))

    if region:
        query = query.filter(Company.region == region)

    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))

    companies = query.order_by(Company.name).offset(skip).limit(limit).all()

    return companies


@router.get("/summary", response_model=List[CompanySummary])
async def list_companies_summary(
    db: Session = Depends(get_db),
):
    """
    Get lightweight list of all companies for dropdown/selector UI.

    Returns only id, name, and region for optimal performance.
    """
    companies = db.query(Company).filter(
        Company.deleted_at.is_(None)
    ).order_by(Company.name).all()

    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get a specific company by ID.

    - **company_id**: UUID of the company to retrieve
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )

    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing company.

    - **company_id**: UUID of the company to update
    - Only provided fields will be updated
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )

    # Check if new name conflicts with existing company
    update_data = company_data.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing = db.query(Company).filter(
            Company.name == update_data["name"],
            Company.id != company_id,
            Company.deleted_at.is_(None)
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Company with name '{update_data['name']}' already exists"
            )

    # Update company fields
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)

    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    hard_delete: bool = Query(False, description="Permanently delete (true) or soft delete (false)"),
    db: Session = Depends(get_db),
):
    """
    Delete a company (soft delete by default).

    - **company_id**: UUID of the company to delete
    - **hard_delete**: If true, permanently delete; if false (default), soft delete

    WARNING: Deleting a company will cascade delete all associated properties!
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None) if not hard_delete else True
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )

    # Check if company has properties
    if company.property_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete company with {company.property_count} active properties. "
                   "Delete or reassign properties first."
        )

    if hard_delete:
        db.delete(company)
    else:
        company.soft_delete()

    db.commit()

    return None


@router.post("/{company_id}/restore", response_model=CompanyResponse)
async def restore_company(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Restore a soft-deleted company.

    - **company_id**: UUID of the company to restore
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_not(None)
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deleted company with id {company_id} not found"
        )

    company.restore()
    db.commit()
    db.refresh(company)

    return company


@router.get("/{company_id}/data-stats", response_model=dict)
async def get_company_data_stats(
    company_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get data statistics for a company to verify data isolation.

    Returns counts of all company-specific records to ensure new companies
    start with zero data and existing companies have proper data isolation.

    This endpoint is useful for:
    - Verifying new companies have no pre-populated data
    - Debugging data isolation issues
    - Getting an overview of company data

    - **company_id**: UUID of the company to check
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )

    # Import models for counting
    from app.models.property_management import Property
    from app.models.deal import Deal
    from app.models.legal_services import LegalDocument, ComplianceItem
    from app.models.crm import Broker
    from app.models.accounting import AccountingProfile

    # Count company-specific records
    stats = {
        "company_id": str(company_id),
        "company_name": company.name,
        "company_specific_data": {
            "properties": db.query(Property).filter(
                Property.company_id == company_id,
                Property.deleted_at.is_(None)
            ).count(),
            "deals": db.query(Deal).filter(
                Deal.company_id == company_id
            ).count(),
            "legal_documents": db.query(LegalDocument).filter(
                LegalDocument.company_id == company_id
            ).count(),
            "compliance_items": db.query(ComplianceItem).filter(
                ComplianceItem.company_id == company_id
            ).count(),
            "brokers": db.query(Broker).filter(
                Broker.company_id == company_id
            ).count(),
            "accounting_profiles": db.query(AccountingProfile).filter(
                AccountingProfile.company_id == company_id
            ).count(),
        },
        "is_empty": True,  # Will be updated based on counts
        "message": ""
    }

    # Calculate if company is empty (all counts are 0)
    total_records = sum(stats["company_specific_data"].values())
    stats["is_empty"] = (total_records == 0)

    if stats["is_empty"]:
        stats["message"] = "✅ Company has zero data - ready for use!"
    else:
        stats["message"] = f"Company has {total_records} records across various tables"

    # Add note about global/shared data
    stats["note"] = (
        "Market intelligence data (economic indicators, market data, etc.) "
        "is intentionally shared across all companies and not included in these counts."
    )

    return stats
