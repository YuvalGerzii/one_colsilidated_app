"""
Property Management System Database Models

This module contains all SQLAlchemy ORM models for the Property Management System,
replicating the functionality of the Property_Management_System.xlsx template.

Models:
- Property: Property master records
- OwnershipDetail: Ownership model tracking
- Unit: Unit inventory
- Lease: Rent roll / lease records
- MaintenanceRequest: Maintenance tracker
- PropertyFinancial: Income statement and cash flow
- BudgetItem: Budget vs actual tracking
- ROIMetric: ROI analysis
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, Boolean, Text,
    ForeignKey, Enum as SQLEnum, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


# Enumerations

class PropertyType(str, enum.Enum):
    """Property type classifications"""
    MULTIFAMILY = "Multifamily"
    SINGLE_FAMILY = "Single Family"
    COMMERCIAL_OFFICE = "Commercial Office"
    RETAIL = "Retail"
    INDUSTRIAL = "Industrial"
    MIXED_USE = "Mixed-Use"
    HOTEL_HOSPITALITY = "Hotel/Hospitality"


class OwnershipModel(str, enum.Enum):
    """Ownership structure models"""
    FULL_OWNERSHIP = "Full Ownership"
    MASTER_LEASE = "Master Lease"
    SUBLEASE = "Sublease"
    RENTAL_ARBITRAGE = "Rental Arbitrage (Airbnb/VRBO)"
    JOINT_VENTURE = "Joint Venture"
    MANAGEMENT_ONLY = "Management Contract Only"
    GROUND_LEASE = "Ground Lease"


class PropertyStatus(str, enum.Enum):
    """Property status"""
    ACTIVE = "Active"
    UNDER_CONTRACT = "Under Contract"
    SOLD = "Sold"
    INACTIVE = "Inactive"


class UnitStatus(str, enum.Enum):
    """Unit occupancy status"""
    OCCUPIED = "Occupied"
    VACANT = "Vacant"
    UNDER_RENOVATION = "Under Renovation"
    OFF_MARKET = "Off-Market"


class MaintenancePriority(str, enum.Enum):
    """Maintenance request priority levels"""
    EMERGENCY = "Emergency"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MaintenanceStatus(str, enum.Enum):
    """Maintenance request status"""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MaintenanceCategory(str, enum.Enum):
    """Maintenance categories"""
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    HVAC = "HVAC"
    APPLIANCE = "Appliance"
    STRUCTURAL = "Structural"
    COSMETIC = "Cosmetic"
    LANDSCAPING = "Landscaping"
    PEST_CONTROL = "Pest Control"
    SECURITY = "Security"
    OTHER = "Other"


# Database Models

class Property(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Property Master table - Central database of all properties

    Corresponds to the "Property Master" sheet in the Excel template.
    """

    __tablename__ = "properties"

    # Basic Information
    property_id = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Unique property identifier (e.g., PROP-001)"
    )
    property_name = Column(String(255), nullable=False, comment="Property name")
    address = Column(String(500), nullable=True, comment="Street address")
    city = Column(String(100), nullable=True, comment="City")
    state = Column(String(50), nullable=True, comment="State/Province")
    zip_code = Column(String(20), nullable=True, comment="ZIP/Postal code")
    country = Column(String(100), nullable=True, default="USA", comment="Country")

    # Property Classification
    property_type = Column(
        SQLEnum(PropertyType),
        nullable=False,
        comment="Property type (Multifamily, Commercial, etc.)"
    )
    ownership_model = Column(
        SQLEnum(OwnershipModel),
        nullable=False,
        comment="Ownership structure"
    )
    status = Column(
        SQLEnum(PropertyStatus),
        nullable=False,
        default=PropertyStatus.ACTIVE,
        comment="Current property status"
    )

    # Metrics
    total_units = Column(Integer, nullable=False, default=0, comment="Total number of units")
    total_square_footage = Column(Integer, nullable=True, comment="Total square footage")
    year_built = Column(Integer, nullable=True, comment="Year property was built")

    # Financial
    purchase_price = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Purchase price (or $0 if leased)"
    )
    purchase_date = Column(Date, nullable=True, comment="Acquisition date")
    current_value = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Current estimated market value"
    )

    # Additional Information
    notes = Column(Text, nullable=True, comment="Additional notes")

    # Relationships
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")
    leases = relationship("Lease", back_populates="property", cascade="all, delete-orphan")
    financials = relationship("PropertyFinancial", back_populates="property", cascade="all, delete-orphan")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="property", cascade="all, delete-orphan")
    ownership_detail = relationship("OwnershipDetail", back_populates="property", uselist=False, cascade="all, delete-orphan")
    roi_metrics = relationship("ROIMetric", back_populates="property", cascade="all, delete-orphan")
    budget_items = relationship("BudgetItem", back_populates="property", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('total_units >= 0', name='check_total_units_positive'),
    )


class OwnershipDetail(Base, UUIDMixin, TimestampMixin):
    """
    Ownership model details

    Corresponds to the "Ownership Models" sheet in the Excel template.
    Tracks how each property is held/operated.
    """

    __tablename__ = "ownership_details"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    ownership_type = Column(
        SQLEnum(OwnershipModel),
        nullable=False,
        comment="Ownership structure type"
    )
    details = Column(Text, nullable=True, comment="Description of ownership structure")

    # Master Lease / Sublease specific
    master_lease_amount = Column(
        Numeric(12, 2),
        nullable=True,
        comment="Monthly master lease payment"
    )
    lease_start_date = Column(Date, nullable=True, comment="Master lease start date")
    lease_end_date = Column(Date, nullable=True, comment="Master lease end date")
    landlord_name = Column(String(255), nullable=True, comment="Landlord name")
    landlord_approval = Column(Boolean, nullable=True, comment="Landlord approval status")

    # Joint Venture specific
    equity_partners = Column(Text, nullable=True, comment="List of equity partners")
    profit_split_percent = Column(
        Numeric(5, 2),
        nullable=True,
        comment="Profit split percentage"
    )

    # Additional terms
    special_terms = Column(Text, nullable=True, comment="Special terms or conditions")
    escalation_rate = Column(
        Numeric(5, 2),
        nullable=True,
        comment="Annual rent escalation %"
    )

    # Relationship
    property = relationship("Property", back_populates="ownership_detail")


class Unit(Base, UUIDMixin, TimestampMixin):
    """
    Unit inventory table

    Corresponds to the "Unit Inventory" sheet in the Excel template.
    Tracks every rentable unit/space in each property.
    """

    __tablename__ = "units"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Unit Identification
    unit_number = Column(String(50), nullable=False, comment="Unit number (e.g., 1A, Suite 300)")
    unit_type = Column(String(100), nullable=True, comment="Unit type (e.g., 1BR/1BA, Office)")

    # Status
    status = Column(
        SQLEnum(UnitStatus),
        nullable=False,
        default=UnitStatus.VACANT,
        comment="Current unit status"
    )

    # Physical Characteristics
    beds = Column(Integer, nullable=True, default=0, comment="Number of bedrooms")
    baths = Column(Numeric(3, 1), nullable=True, default=0, comment="Number of bathrooms")
    square_footage = Column(Integer, nullable=True, comment="Unit square footage")
    floor_number = Column(Integer, nullable=True, comment="Floor number")

    # Financial
    market_rent = Column(
        Numeric(10, 2),
        nullable=False,
        default=0,
        comment="Market rent (what you could charge)"
    )
    current_rent = Column(
        Numeric(10, 2),
        nullable=False,
        default=0,
        comment="Current rent (what tenant pays)"
    )

    # Tenant Information
    tenant_name = Column(String(255), nullable=True, comment="Current tenant name")

    # Vacancy Tracking
    days_vacant = Column(Integer, nullable=True, default=0, comment="Days unit has been vacant")
    last_occupied_date = Column(Date, nullable=True, comment="Last date unit was occupied")

    # Renovation
    renovation_budget = Column(
        Numeric(10, 2),
        nullable=True,
        default=0,
        comment="Planned renovation budget"
    )
    renovation_notes = Column(Text, nullable=True, comment="Renovation notes")

    # Additional Information
    amenities = Column(Text, nullable=True, comment="Special amenities")
    notes = Column(Text, nullable=True, comment="Additional notes")

    # Relationship
    property = relationship("Property", back_populates="units")
    leases = relationship("Lease", back_populates="unit")

    __table_args__ = (
        CheckConstraint('market_rent >= 0', name='check_market_rent_positive'),
        CheckConstraint('current_rent >= 0', name='check_current_rent_positive'),
        CheckConstraint('beds >= 0', name='check_beds_positive'),
        CheckConstraint('days_vacant >= 0', name='check_days_vacant_positive'),
    )


class Lease(Base, UUIDMixin, TimestampMixin):
    """
    Lease / Rent roll table

    Corresponds to the "Rent Roll" sheet in the Excel template.
    Tracks all active leases and tenant information.
    """

    __tablename__ = "leases"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    unit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("units.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Tenant Information
    tenant_name = Column(String(255), nullable=False, comment="Tenant name")
    tenant_email = Column(String(255), nullable=True, comment="Tenant email")
    tenant_phone = Column(String(50), nullable=True, comment="Tenant phone")

    # Lease Terms
    lease_start_date = Column(Date, nullable=False, comment="Lease start date")
    lease_end_date = Column(Date, nullable=False, comment="Lease end date")
    monthly_rent = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Monthly rent amount"
    )

    # Deposits & Fees
    security_deposit = Column(
        Numeric(10, 2),
        nullable=True,
        default=0,
        comment="Security deposit amount"
    )
    pet_deposit = Column(Numeric(10, 2), nullable=True, default=0, comment="Pet deposit")
    parking_fee = Column(Numeric(10, 2), nullable=True, default=0, comment="Monthly parking fee")

    # Tenant Qualification
    credit_score = Column(Integer, nullable=True, comment="Tenant credit score")
    employment_verified = Column(Boolean, nullable=True, comment="Employment verification status")

    # Renewal
    renewal_probability = Column(
        Numeric(3, 0),
        nullable=True,
        comment="Estimated renewal probability (0-100%)"
    )
    auto_renew = Column(Boolean, nullable=True, default=False, comment="Auto-renewal clause")

    # Status
    is_active = Column(Boolean, nullable=False, default=True, comment="Active lease status")

    # Additional
    lease_document_url = Column(String(500), nullable=True, comment="Link to signed lease")
    notes = Column(Text, nullable=True, comment="Additional notes")

    # Relationships
    property = relationship("Property", back_populates="leases")
    unit = relationship("Unit", back_populates="leases")

    __table_args__ = (
        CheckConstraint('monthly_rent > 0', name='check_monthly_rent_positive'),
        CheckConstraint('credit_score IS NULL OR (credit_score >= 300 AND credit_score <= 850)',
                       name='check_credit_score_range'),
        CheckConstraint('renewal_probability IS NULL OR (renewal_probability >= 0 AND renewal_probability <= 100)',
                       name='check_renewal_probability_range'),
    )


class PropertyFinancial(Base, UUIDMixin, TimestampMixin):
    """
    Property financials - Income statement and cash flow

    Corresponds to the "Income Statement" and "Cash Flow" sheets in Excel template.
    Tracks monthly financial performance by property.
    """

    __tablename__ = "property_financials"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Period
    period_date = Column(Date, nullable=False, comment="Period (first day of month)")
    fiscal_year = Column(Integer, nullable=False, comment="Fiscal year")
    fiscal_month = Column(Integer, nullable=False, comment="Fiscal month (1-12)")

    # Income
    gross_potential_rent = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Gross potential rent (100% occupancy)"
    )
    vacancy_loss = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Vacancy and credit loss (negative value)"
    )
    other_income = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Other income (parking, laundry, fees)"
    )

    # Operating Expenses
    property_taxes = Column(Numeric(12, 2), nullable=True, default=0)
    insurance = Column(Numeric(12, 2), nullable=True, default=0)
    utilities = Column(Numeric(12, 2), nullable=True, default=0)
    repairs_maintenance = Column(Numeric(12, 2), nullable=True, default=0)
    property_management_fee = Column(Numeric(12, 2), nullable=True, default=0)
    landscaping = Column(Numeric(12, 2), nullable=True, default=0)
    pest_control = Column(Numeric(12, 2), nullable=True, default=0)
    hoa_fees = Column(Numeric(12, 2), nullable=True, default=0)
    marketing = Column(Numeric(12, 2), nullable=True, default=0)
    administrative = Column(Numeric(12, 2), nullable=True, default=0)
    other_expenses = Column(Numeric(12, 2), nullable=True, default=0)

    # Debt Service
    debt_service = Column(
        Numeric(12, 2),
        nullable=True,
        default=0,
        comment="Total debt service (principal + interest)"
    )

    # Capital Expenditures
    capital_expenditures = Column(
        Numeric(12, 2),
        nullable=True,
        default=0,
        comment="CapEx for the period"
    )

    # Notes
    notes = Column(Text, nullable=True, comment="Financial period notes")

    # Relationship
    property = relationship("Property", back_populates="financials")

    __table_args__ = (
        CheckConstraint('fiscal_month >= 1 AND fiscal_month <= 12', name='check_fiscal_month_range'),
    )


class MaintenanceRequest(Base, UUIDMixin, TimestampMixin):
    """
    Maintenance tracker

    Corresponds to the "Maintenance Tracker" sheet in Excel template.
    Tracks work orders and maintenance requests.
    """

    __tablename__ = "maintenance_requests"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    unit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("units.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Request Details
    request_number = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Unique request ID"
    )
    category = Column(
        SQLEnum(MaintenanceCategory),
        nullable=False,
        comment="Maintenance category"
    )
    description = Column(Text, nullable=False, comment="Issue description")

    # Status
    status = Column(
        SQLEnum(MaintenanceStatus),
        nullable=False,
        default=MaintenanceStatus.OPEN,
        comment="Current status"
    )
    priority = Column(
        SQLEnum(MaintenancePriority),
        nullable=False,
        default=MaintenancePriority.MEDIUM,
        comment="Priority level"
    )

    # Dates
    date_reported = Column(Date, nullable=False, comment="Date reported")
    date_scheduled = Column(Date, nullable=True, comment="Scheduled date")
    date_completed = Column(Date, nullable=True, comment="Completion date")

    # Cost
    estimated_cost = Column(Numeric(10, 2), nullable=True, comment="Estimated cost")
    actual_cost = Column(Numeric(10, 2), nullable=True, default=0, comment="Actual cost")

    # Vendor
    vendor_name = Column(String(255), nullable=True, comment="Vendor/contractor name")
    vendor_contact = Column(String(255), nullable=True, comment="Vendor contact info")

    # Additional
    reported_by = Column(String(255), nullable=True, comment="Who reported the issue")
    assigned_to = Column(String(255), nullable=True, comment="Assigned staff member")
    photos_url = Column(String(500), nullable=True, comment="Link to photos")
    notes = Column(Text, nullable=True, comment="Additional notes")

    # Relationships
    property = relationship("Property", back_populates="maintenance_requests")


class BudgetItem(Base, UUIDMixin, TimestampMixin):
    """
    Budget vs Actual tracking

    Corresponds to the "Budget vs Actual" sheet in Excel template.
    Tracks budgeted vs actual expenses by category.
    """

    __tablename__ = "budget_items"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Period
    fiscal_year = Column(Integer, nullable=False, comment="Fiscal year")
    expense_category = Column(String(100), nullable=False, comment="Expense category")

    # Budget
    budget_monthly = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Monthly budget"
    )
    budget_annual = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Annual budget"
    )

    # Actual (YTD)
    actual_ytd = Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        comment="Year-to-date actual"
    )

    # Notes
    notes = Column(Text, nullable=True, comment="Budget notes")

    # Relationship
    property = relationship("Property", back_populates="budget_items")


class ROIMetric(Base, UUIDMixin, TimestampMixin):
    """
    ROI Analysis metrics

    Corresponds to the "ROI Analysis" sheet in Excel template.
    Tracks return metrics for each property.
    """

    __tablename__ = "roi_metrics"

    property_id = Column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Period
    as_of_date = Column(Date, nullable=False, comment="Valuation date")

    # Investment
    total_equity = Column(
        Numeric(15, 2),
        nullable=False,
        comment="Total equity invested"
    )
    total_debt = Column(
        Numeric(15, 2),
        nullable=True,
        default=0,
        comment="Total debt"
    )

    # Performance
    annual_noi = Column(Numeric(12, 2), nullable=True, comment="Annual NOI")
    annual_cash_flow = Column(
        Numeric(12, 2),
        nullable=True,
        comment="Annual cash flow after debt service"
    )
    cumulative_cash_flow = Column(
        Numeric(15, 2),
        nullable=True,
        default=0,
        comment="Cumulative cash flow to date"
    )

    # Value
    current_value = Column(Numeric(15, 2), nullable=True, comment="Current property value")
    appreciation = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Total appreciation (current - purchase)"
    )

    # Returns (calculated)
    cash_on_cash_return = Column(
        Numeric(7, 4),
        nullable=True,
        comment="Cash-on-cash return %"
    )
    total_roi = Column(Numeric(7, 4), nullable=True, comment="Total ROI %")
    approximate_irr = Column(Numeric(7, 4), nullable=True, comment="Approximate IRR %")

    # Holding Period
    years_held = Column(Numeric(5, 2), nullable=True, comment="Years held")

    # Relationship
    property = relationship("Property", back_populates="roi_metrics")


# Export all models
__all__ = [
    "PropertyType",
    "OwnershipModel",
    "PropertyStatus",
    "UnitStatus",
    "MaintenancePriority",
    "MaintenanceStatus",
    "MaintenanceCategory",
    "Property",
    "OwnershipDetail",
    "Unit",
    "Lease",
    "PropertyFinancial",
    "MaintenanceRequest",
    "BudgetItem",
    "ROIMetric",
]
