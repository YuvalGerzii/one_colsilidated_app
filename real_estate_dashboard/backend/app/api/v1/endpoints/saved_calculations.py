"""
Saved Calculations API Endpoints

Handles saving, loading, versioning, and managing calculator results.
Replaces localStorage with database persistence.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import desc, and_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_active_user, get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.saved_calculation import SavedCalculation, CalculationType

router = APIRouter()


# ===== Request/Response Schemas =====

class CalculationSave(BaseModel):
    """Save a new calculation."""
    calculation_type: CalculationType
    property_name: str = Field(..., min_length=1, max_length=255)
    property_address: Optional[str] = None
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = False


class CalculationUpdate(BaseModel):
    """Update an existing calculation."""
    property_name: Optional[str] = None
    property_address: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None
    is_archived: Optional[bool] = None


class CalculationResponse(BaseModel):
    """Calculation response."""
    id: str
    calculation_type: str
    property_name: str
    property_address: Optional[str]
    version: int
    is_current_version: bool
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    notes: Optional[str]
    tags: Optional[List[str]]
    is_favorite: bool
    is_archived: bool
    created_at: str
    updated_at: str


# ===== Calculator Storage Endpoints =====

@router.post("/", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
async def save_calculation(
    calculation: CalculationSave,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Save a new calculation result.

    This replaces localStorage.setItem() for calculator results.
    """
    current_user, company = user_company

    new_calc = SavedCalculation(
        user_id=current_user.id,
        company_id=company.id if company else None,
        calculation_type=calculation.calculation_type.value,
        property_name=calculation.property_name,
        property_address=calculation.property_address,
        version=1,
        is_current_version=True,
        input_data=calculation.input_data,
        output_data=calculation.output_data,
        notes=calculation.notes,
        tags=calculation.tags,
        is_favorite=calculation.is_favorite or False,
    )

    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)

    return new_calc.to_dict()


@router.get("/", response_model=List[CalculationResponse])
async def list_calculations(
    calculation_type: Optional[CalculationType] = None,
    is_favorite: Optional[bool] = None,
    is_archived: Optional[bool] = None,
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    search: Optional[str] = Query(None, description="Search property name/address"),
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    List all saved calculations for the current user and company.

    Supports filtering by type, favorites, tags, and search.
    Replaces getting all calculator results from localStorage.
    """
    current_user, company = user_company

    query = db.query(SavedCalculation).filter(
        SavedCalculation.user_id == current_user.id,
        SavedCalculation.is_current_version == True  # Only show latest versions
    )

    # Filter by company_id if user has a company
    if company:
        query = query.filter(SavedCalculation.company_id == company.id)

    # Apply filters
    if calculation_type:
        query = query.filter(SavedCalculation.calculation_type == calculation_type.value)

    if is_favorite is not None:
        query = query.filter(SavedCalculation.is_favorite == is_favorite)

    if is_archived is not None:
        query = query.filter(SavedCalculation.is_archived == is_archived)
    else:
        # By default, exclude archived unless explicitly requested
        query = query.filter(SavedCalculation.is_archived == False)

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        # JSONB containment query
        query = query.filter(SavedCalculation.tags.contains(tag_list))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (SavedCalculation.property_name.ilike(search_pattern)) |
            (SavedCalculation.property_address.ilike(search_pattern))
        )

    # Order by updated_at descending (most recent first)
    calculations = query.order_by(desc(SavedCalculation.updated_at)).offset(skip).limit(limit).all()

    return [calc.to_dict() for calc in calculations]


@router.get("/{calculation_id}", response_model=CalculationResponse)
async def get_calculation(
    calculation_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Get a specific calculation by ID.

    Replaces localStorage.getItem() for a specific calculator result.
    """
    current_user, company = user_company

    filters = [
        SavedCalculation.id == calculation_id,
        SavedCalculation.user_id == current_user.id
    ]

    if company:
        filters.append(SavedCalculation.company_id == company.id)

    calculation = db.query(SavedCalculation).filter(*filters).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )

    return calculation.to_dict()


@router.put("/{calculation_id}", response_model=CalculationResponse)
async def update_calculation(
    calculation_id: UUID,
    update_data: CalculationUpdate,
    create_version: bool = Query(False, description="Create new version instead of updating"),
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Update an existing calculation.

    If create_version=true, creates a new version instead of updating in place.
    """
    current_user, company = user_company

    filters = [
        SavedCalculation.id == calculation_id,
        SavedCalculation.user_id == current_user.id
    ]

    if company:
        filters.append(SavedCalculation.company_id == company.id)

    calculation = db.query(SavedCalculation).filter(*filters).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )

    if create_version:
        # Create new version
        calculation.is_current_version = False
        db.commit()

        version_data = calculation.create_new_version(
            new_input_data=update_data.input_data or calculation.input_data,
            new_output_data=update_data.output_data or calculation.output_data,
            notes=update_data.notes
        )

        new_version = SavedCalculation(**version_data)
        db.add(new_version)
        db.commit()
        db.refresh(new_version)

        return new_version.to_dict()
    else:
        # Update in place
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(calculation, field, value)

        db.commit()
        db.refresh(calculation)

        return calculation.to_dict()


@router.delete("/{calculation_id}")
async def delete_calculation(
    calculation_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Delete a calculation (hard delete).

    For soft delete, use update endpoint with is_archived=true.
    """
    current_user, company = user_company

    filters = [
        SavedCalculation.id == calculation_id,
        SavedCalculation.user_id == current_user.id
    ]

    if company:
        filters.append(SavedCalculation.company_id == company.id)

    calculation = db.query(SavedCalculation).filter(*filters).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )

    db.delete(calculation)
    db.commit()

    return {"message": "Calculation deleted successfully"}


# ===== Version History Endpoints =====

@router.get("/{calculation_id}/versions", response_model=List[CalculationResponse])
async def get_calculation_versions(
    calculation_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Get all versions of a calculation.

    Returns version history for the calculation, ordered by version number.
    """
    current_user, company = user_company

    # First verify the user owns this calculation
    filters = [
        SavedCalculation.id == calculation_id,
        SavedCalculation.user_id == current_user.id
    ]

    if company:
        filters.append(SavedCalculation.company_id == company.id)

    calculation = db.query(SavedCalculation).filter(*filters).first()

    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )

    # Get all versions (following parent chain and children)
    # Find the root (earliest version)
    root = calculation
    while root.parent_id:
        root = db.query(SavedCalculation).filter(SavedCalculation.id == root.parent_id).first()

    # Get all descendants
    version_filters = [
        (SavedCalculation.id == root.id) |
        (SavedCalculation.parent_id.in_(
            db.query(SavedCalculation.id).filter(
                SavedCalculation.property_name == root.property_name,
                SavedCalculation.user_id == current_user.id
            )
        ))
    ]

    if company:
        version_filters.append(SavedCalculation.company_id == company.id)

    versions = db.query(SavedCalculation).filter(*version_filters).order_by(SavedCalculation.version).all()

    return [v.to_dict() for v in versions]


# ===== Bulk Operations =====

@router.post("/bulk-save", response_model=List[CalculationResponse])
async def bulk_save_calculations(
    calculations: List[CalculationSave],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Save multiple calculations at once.

    Useful for migrating from localStorage to database.
    """
    current_user, company = user_company
    saved_calculations = []

    for calc_data in calculations:
        new_calc = SavedCalculation(
            user_id=current_user.id,
            company_id=company.id if company else None,
            calculation_type=calc_data.calculation_type.value,
            property_name=calc_data.property_name,
            property_address=calc_data.property_address,
            version=1,
            is_current_version=True,
            input_data=calc_data.input_data,
            output_data=calc_data.output_data,
            notes=calc_data.notes,
            tags=calc_data.tags,
            is_favorite=calc_data.is_favorite or False,
        )
        db.add(new_calc)
        saved_calculations.append(new_calc)

    db.commit()

    for calc in saved_calculations:
        db.refresh(calc)

    return [calc.to_dict() for calc in saved_calculations]


@router.get("/stats/summary")
async def get_calculations_summary(
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """
    Get summary statistics for user's calculations.

    Returns counts by type, favorites, recent activity, etc.
    """
    current_user, company = user_company

    base_filters = [
        SavedCalculation.user_id == current_user.id,
        SavedCalculation.is_current_version == True,
        SavedCalculation.is_archived == False
    ]

    if company:
        base_filters.append(SavedCalculation.company_id == company.id)

    total = db.query(SavedCalculation).filter(*base_filters).count()

    favorites = db.query(SavedCalculation).filter(
        *base_filters,
        SavedCalculation.is_favorite == True
    ).count()

    # Count by type
    by_type = {}
    for calc_type in CalculationType:
        count = db.query(SavedCalculation).filter(
            *base_filters,
            SavedCalculation.calculation_type == calc_type.value
        ).count()
        if count > 0:
            by_type[calc_type.value] = count

    return {
        "total_calculations": total,
        "favorites": favorites,
        "by_type": by_type
    }
