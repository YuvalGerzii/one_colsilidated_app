"""
Database Models Module

This module contains all SQLAlchemy ORM models for the Portfolio Dashboard.
Each model corresponds to a table in the PostgreSQL database.
"""

from app.models.database import Base, TimestampMixin, UUIDMixin
from app.models.fund import Fund
from app.models.company import PortfolioCompany
from app.models.financial_metric import FinancialMetric
from app.models.company_kpi import CompanyKPI
from app.models.valuation import Valuation
from app.models.document import Document
from app.models.due_diligence import DueDiligenceItem
from app.models.value_creation import ValueCreationInitiative
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.real_estate import (
    FixAndFlipModel,
    HotelFinancialModel,
    SingleFamilyRentalModel,
    SmallMultifamilyModel,
)
from app.models.property_management import (
    Property,
    OwnershipDetail,
    Unit,
    Lease,
    PropertyFinancial,
    MaintenanceRequest,
    BudgetItem,
    ROIMetric,
)

__all__ = [
    "Base",
    "TimestampMixin",
    "UUIDMixin",
    "Fund",
    "PortfolioCompany",
    "FinancialMetric",
    "CompanyKPI",
    "Valuation",
    "Document",
    "DueDiligenceItem",
    "ValueCreationInitiative",
    "User",
    "AuditLog",
    "HotelFinancialModel",
    "SingleFamilyRentalModel",
    "FixAndFlipModel",
    "SmallMultifamilyModel",
    "Property",
    "OwnershipDetail",
    "Unit",
    "Lease",
    "PropertyFinancial",
    "MaintenanceRequest",
    "BudgetItem",
    "ROIMetric",
]
