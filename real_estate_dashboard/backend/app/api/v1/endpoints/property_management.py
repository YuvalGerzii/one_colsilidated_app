"""
Property Management System API Endpoints

This module provides comprehensive REST API endpoints for the Property Management System,
including CRUD operations for properties, units, leases, financials, maintenance, and analytics.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract

from app.api.deps import get_db
from app.models.property_management import (
    Property,
    OwnershipDetail,
    Unit,
    Lease,
    PropertyFinancial,
    MaintenanceRequest,
    BudgetItem,
    ROIMetric,
    PropertyType,
    OwnershipModel,
    PropertyStatus,
    UnitStatus,
    MaintenancePriority,
    MaintenanceStatus,
    MaintenanceCategory,
)


router = APIRouter()


# Pydantic Schemas

class PropertyBase(BaseModel):
    property_id: str
    property_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: PropertyType
    ownership_model: OwnershipModel
    status: PropertyStatus = PropertyStatus.ACTIVE
    total_units: int = 0
    purchase_price: Optional[Decimal] = None
    purchase_date: Optional[date] = None
    current_value: Optional[Decimal] = None
    notes: Optional[str] = None


class PropertyCreate(PropertyBase):
    company_id: UUID


class PropertyUpdate(BaseModel):
    property_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[PropertyStatus] = None
    current_value: Optional[Decimal] = None
    notes: Optional[str] = None


class PropertyResponse(PropertyBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UnitBase(BaseModel):
    unit_number: str
    unit_type: Optional[str] = None
    status: UnitStatus = UnitStatus.VACANT
    beds: Optional[int] = 0
    baths: Optional[Decimal] = Decimal('0')
    square_footage: Optional[int] = None
    market_rent: Decimal = Decimal('0')
    current_rent: Decimal = Decimal('0')
    tenant_name: Optional[str] = None


class UnitCreate(UnitBase):
    property_id: UUID


class UnitUpdate(BaseModel):
    status: Optional[UnitStatus] = None
    market_rent: Optional[Decimal] = None
    current_rent: Optional[Decimal] = None
    tenant_name: Optional[str] = None
    renovation_budget: Optional[Decimal] = None


class UnitResponse(UnitBase):
    id: UUID
    property_id: UUID
    days_vacant: int
    created_at: datetime

    class Config:
        from_attributes = True


class LeaseBase(BaseModel):
    tenant_name: str
    lease_start_date: date
    lease_end_date: date
    monthly_rent: Decimal
    security_deposit: Optional[Decimal] = Decimal('0')
    credit_score: Optional[int] = None


class LeaseCreate(LeaseBase):
    property_id: UUID
    unit_id: UUID


class LeaseUpdate(BaseModel):
    monthly_rent: Optional[Decimal] = None
    lease_end_date: Optional[date] = None
    renewal_probability: Optional[int] = None
    is_active: Optional[bool] = None


class LeaseResponse(LeaseBase):
    id: UUID
    property_id: UUID
    unit_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MaintenanceRequestBase(BaseModel):
    request_number: str
    category: MaintenanceCategory
    description: str
    priority: MaintenancePriority = MaintenancePriority.MEDIUM
    status: MaintenanceStatus = MaintenanceStatus.OPEN
    date_reported: date


class MaintenanceRequestCreate(MaintenanceRequestBase):
    property_id: UUID
    unit_id: Optional[UUID] = None


class MaintenanceRequestUpdate(BaseModel):
    status: Optional[MaintenanceStatus] = None
    priority: Optional[MaintenancePriority] = None
    actual_cost: Optional[Decimal] = None
    date_completed: Optional[date] = None
    vendor_name: Optional[str] = None


class MaintenanceRequestResponse(MaintenanceRequestBase):
    id: UUID
    property_id: UUID
    unit_id: Optional[UUID]
    actual_cost: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Analytics Schemas

class PortfolioSummary(BaseModel):
    total_properties: int
    total_units: int
    occupied_units: int
    vacant_units: int
    physical_occupancy_rate: float
    portfolio_value: Decimal
    monthly_gpr: Decimal
    monthly_noi: Decimal
    portfolio_cap_rate: float


class DashboardAlerts(BaseModel):
    leases_expiring_60_days: int
    critical_leases: int
    vacant_units: int
    open_maintenance: int
    emergency_maintenance: int


# Property Endpoints

@router.post("/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    """Create a new property"""
    # Check if property_id already exists
    existing = db.query(Property).filter(Property.property_id == property_data.property_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Property with ID '{property_data.property_id}' already exists"
        )

    db_property = Property(**property_data.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@router.get("/properties", response_model=List[PropertyResponse])
async def get_properties(
    company_id: Optional[UUID] = Query(None, description="Filter by company ID"),
    status_filter: Optional[PropertyStatus] = Query(None, alias="status"),
    property_type: Optional[PropertyType] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all properties with optional filtering"""
    query = db.query(Property).filter(Property.deleted_at.is_(None))

    if company_id:
        query = query.filter(Property.company_id == company_id)
    if status_filter:
        query = query.filter(Property.status == status_filter)
    if property_type:
        query = query.filter(Property.property_type == property_type)

    query = query.order_by(Property.created_at.desc())
    properties = query.offset(skip).limit(limit).all()
    return properties


@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific property by ID"""
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return property_obj


@router.patch("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    property_update: PropertyUpdate,
    db: Session = Depends(get_db)
):
    """Update a property"""
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    update_data = property_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(property_obj, field, value)

    db.commit()
    db.refresh(property_obj)
    return property_obj


@router.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: UUID,
    db: Session = Depends(get_db)
):
    """Soft delete a property"""
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    property_obj.soft_delete()
    db.commit()


# Unit Endpoints

@router.post("/units", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
async def create_unit(
    unit_data: UnitCreate,
    db: Session = Depends(get_db)
):
    """Create a new unit"""
    # Verify property exists
    property_obj = db.query(Property).filter(Property.id == unit_data.property_id).first()
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    db_unit = Unit(**unit_data.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


@router.get("/units", response_model=List[UnitResponse])
async def get_units(
    property_id: Optional[UUID] = Query(None),
    status_filter: Optional[UnitStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all units with optional filtering"""
    query = db.query(Unit)

    if property_id:
        query = query.filter(Unit.property_id == property_id)
    if status_filter:
        query = query.filter(Unit.status == status_filter)

    units = query.offset(skip).limit(limit).all()
    return units


@router.get("/units/{unit_id}", response_model=UnitResponse)
async def get_unit(
    unit_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific unit"""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )
    return unit


@router.patch("/units/{unit_id}", response_model=UnitResponse)
async def update_unit(
    unit_id: UUID,
    unit_update: UnitUpdate,
    db: Session = Depends(get_db)
):
    """Update a unit"""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )

    update_data = unit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(unit, field, value)

    db.commit()
    db.refresh(unit)
    return unit


# Lease Endpoints

@router.post("/leases", response_model=LeaseResponse, status_code=status.HTTP_201_CREATED)
async def create_lease(
    lease_data: LeaseCreate,
    db: Session = Depends(get_db)
):
    """Create a new lease"""
    # Verify property and unit exist
    unit = db.query(Unit).filter(Unit.id == lease_data.unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )

    db_lease = Lease(**lease_data.dict(), is_active=True)
    db.add(db_lease)

    # Update unit status
    unit.status = UnitStatus.OCCUPIED
    unit.current_rent = lease_data.monthly_rent
    unit.tenant_name = lease_data.tenant_name

    db.commit()
    db.refresh(db_lease)
    return db_lease


@router.get("/leases", response_model=List[LeaseResponse])
async def get_leases(
    property_id: Optional[UUID] = Query(None),
    is_active: Optional[bool] = Query(None),
    expiring_within_days: Optional[int] = Query(None, ge=0, le=365),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all leases with optional filtering"""
    query = db.query(Lease)

    if property_id:
        query = query.filter(Lease.property_id == property_id)
    if is_active is not None:
        query = query.filter(Lease.is_active == is_active)
    if expiring_within_days is not None:
        cutoff_date = date.today() + timedelta(days=expiring_within_days)
        query = query.filter(
            Lease.lease_end_date <= cutoff_date,
            Lease.lease_end_date >= date.today()
        )

    leases = query.order_by(Lease.lease_end_date).offset(skip).limit(limit).all()
    return leases


@router.get("/leases/expiring", response_model=List[LeaseResponse])
async def get_expiring_leases(
    days: int = Query(60, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get leases expiring within specified days"""
    from datetime import timedelta
    cutoff_date = date.today() + timedelta(days=days)

    leases = db.query(Lease).filter(
        Lease.is_active == True,
        Lease.lease_end_date <= cutoff_date,
        Lease.lease_end_date >= date.today()
    ).order_by(Lease.lease_end_date).all()

    return leases


@router.patch("/leases/{lease_id}", response_model=LeaseResponse)
async def update_lease(
    lease_id: UUID,
    lease_update: LeaseUpdate,
    db: Session = Depends(get_db)
):
    """Update a lease"""
    lease = db.query(Lease).filter(Lease.id == lease_id).first()
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lease not found"
        )

    update_data = lease_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lease, field, value)

    db.commit()
    db.refresh(lease)
    return lease


# Maintenance Endpoints

@router.post("/maintenance", response_model=MaintenanceRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_request(
    request_data: MaintenanceRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new maintenance request"""
    db_request = MaintenanceRequest(**request_data.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/maintenance", response_model=List[MaintenanceRequestResponse])
async def get_maintenance_requests(
    property_id: Optional[UUID] = Query(None),
    status_filter: Optional[MaintenanceStatus] = Query(None, alias="status"),
    priority: Optional[MaintenancePriority] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get maintenance requests with optional filtering"""
    query = db.query(MaintenanceRequest)

    if property_id:
        query = query.filter(MaintenanceRequest.property_id == property_id)
    if status_filter:
        query = query.filter(MaintenanceRequest.status == status_filter)
    if priority:
        query = query.filter(MaintenanceRequest.priority == priority)

    requests = query.order_by(
        MaintenanceRequest.priority.desc(),
        MaintenanceRequest.date_reported.desc()
    ).offset(skip).limit(limit).all()

    return requests


@router.patch("/maintenance/{request_id}", response_model=MaintenanceRequestResponse)
async def update_maintenance_request(
    request_id: UUID,
    request_update: MaintenanceRequestUpdate,
    db: Session = Depends(get_db)
):
    """Update a maintenance request"""
    request_obj = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not request_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance request not found"
        )

    update_data = request_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(request_obj, field, value)

    db.commit()
    db.refresh(request_obj)
    return request_obj


# Dashboard & Analytics Endpoints

@router.get("/dashboard/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    db: Session = Depends(get_db)
):
    """Get complete portfolio summary with key metrics"""
    # Count properties
    total_properties = db.query(func.count(Property.id)).filter(
        Property.status == PropertyStatus.ACTIVE,
        Property.deleted_at.is_(None)
    ).scalar() or 0

    # Count units
    total_units = db.query(func.count(Unit.id)).scalar() or 0
    occupied_units = db.query(func.count(Unit.id)).filter(
        Unit.status == UnitStatus.OCCUPIED
    ).scalar() or 0
    vacant_units = total_units - occupied_units

    # Calculate occupancy rate
    occupancy_rate = (occupied_units / total_units * 100) if total_units > 0 else 0

    # Portfolio value
    portfolio_value = db.query(func.sum(Property.current_value)).filter(
        Property.status == PropertyStatus.ACTIVE,
        Property.deleted_at.is_(None)
    ).scalar() or Decimal('0')

    # Monthly GPR
    monthly_gpr = db.query(func.sum(Unit.market_rent)).scalar() or Decimal('0')

    # Monthly NOI (from financials)
    latest_financials = db.query(
        func.sum(PropertyFinancial.gross_potential_rent +
                PropertyFinancial.vacancy_loss +
                PropertyFinancial.other_income -
                PropertyFinancial.property_taxes -
                PropertyFinancial.insurance -
                PropertyFinancial.utilities -
                PropertyFinancial.repairs_maintenance -
                PropertyFinancial.property_management_fee -
                PropertyFinancial.landscaping -
                PropertyFinancial.pest_control -
                PropertyFinancial.hoa_fees -
                PropertyFinancial.marketing -
                PropertyFinancial.administrative -
                PropertyFinancial.other_expenses)
    ).scalar() or Decimal('0')

    # Calculate cap rate
    annual_noi = latest_financials * 12
    cap_rate = float((annual_noi / portfolio_value * 100)) if portfolio_value > 0 else 0

    return PortfolioSummary(
        total_properties=total_properties,
        total_units=total_units,
        occupied_units=occupied_units,
        vacant_units=vacant_units,
        physical_occupancy_rate=float(occupancy_rate),
        portfolio_value=portfolio_value,
        monthly_gpr=monthly_gpr,
        monthly_noi=latest_financials,
        portfolio_cap_rate=cap_rate
    )


@router.get("/dashboard/alerts", response_model=DashboardAlerts)
async def get_dashboard_alerts(
    db: Session = Depends(get_db)
):
    """Get dashboard alerts for critical items"""
    from datetime import timedelta

    # Leases expiring in 60 days
    cutoff_60_days = date.today() + timedelta(days=60)
    leases_expiring_60 = db.query(func.count(Lease.id)).filter(
        Lease.is_active == True,
        Lease.lease_end_date <= cutoff_60_days,
        Lease.lease_end_date >= date.today()
    ).scalar() or 0

    # Critical leases (< 60 days)
    critical_leases = leases_expiring_60

    # Vacant units
    vacant_units = db.query(func.count(Unit.id)).filter(
        Unit.status == UnitStatus.VACANT
    ).scalar() or 0

    # Open maintenance
    open_maintenance = db.query(func.count(MaintenanceRequest.id)).filter(
        MaintenanceRequest.status.in_([MaintenanceStatus.OPEN, MaintenanceStatus.IN_PROGRESS])
    ).scalar() or 0

    # Emergency maintenance
    emergency_maintenance = db.query(func.count(MaintenanceRequest.id)).filter(
        MaintenanceRequest.priority == MaintenancePriority.EMERGENCY,
        MaintenanceRequest.status != MaintenanceStatus.COMPLETED
    ).scalar() or 0

    return DashboardAlerts(
        leases_expiring_60_days=leases_expiring_60,
        critical_leases=critical_leases,
        vacant_units=vacant_units,
        open_maintenance=open_maintenance,
        emergency_maintenance=emergency_maintenance
    )


@router.get("/properties/{property_id}/occupancy")
async def get_property_occupancy(
    property_id: UUID,
    db: Session = Depends(get_db)
):
    """Get occupancy metrics for a specific property"""
    # Verify property exists
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    # Get unit counts
    total_units = db.query(func.count(Unit.id)).filter(Unit.property_id == property_id).scalar() or 0
    occupied = db.query(func.count(Unit.id)).filter(
        Unit.property_id == property_id,
        Unit.status == UnitStatus.OCCUPIED
    ).scalar() or 0

    occupancy_rate = (occupied / total_units * 100) if total_units > 0 else 0

    return {
        "property_id": property_id,
        "total_units": total_units,
        "occupied_units": occupied,
        "vacant_units": total_units - occupied,
        "occupancy_rate": occupancy_rate
    }


__all__ = ["router"]
