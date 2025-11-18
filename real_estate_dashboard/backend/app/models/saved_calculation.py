"""Saved Calculations model for storing calculator results with versioning."""

from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import enum

from app.models.database import BaseModel


class CalculationType(str, enum.Enum):
    """Types of financial calculators."""
    FIX_AND_FLIP = "fix_and_flip"
    SINGLE_FAMILY_RENTAL = "single_family_rental"
    SMALL_MULTIFAMILY = "small_multifamily"
    HIGHRISE_MULTIFAMILY = "highrise_multifamily"
    HOTEL = "hotel"
    MIXED_USE = "mixed_use"
    LEASE_ANALYZER = "lease_analyzer"
    RENOVATION_BUDGET = "renovation_budget"
    DCF_VALUATION = "dcf_valuation"
    DUE_DILIGENCE = "due_diligence"


class SavedCalculation(BaseModel):
    """
    Saved calculator results with versioning support.

    Allows users to save, load, and track versions of their calculations.
    """

    __tablename__ = "saved_calculations"
    __table_args__ = (
        Index('ix_saved_calculations_user_type', 'user_id', 'calculation_type'),
        Index('ix_saved_calculations_user_property', 'user_id', 'property_name'),
        Index('ix_saved_calculations_company_type', 'company_id', 'calculation_type'),
    )

    # Ownership (Multi-Tenancy)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this calculation belongs to (for multi-tenancy)"
    )

    # Calculation Info
    calculation_type = Column(String(50), nullable=False, comment="Type of calculator")
    property_name = Column(String(255), nullable=False, index=True, comment="Property name/identifier")
    property_address = Column(String(500), nullable=True, comment="Property address")

    # Version Control
    version = Column(Integer, default=1, nullable=False, comment="Version number")
    is_current_version = Column(Boolean, default=True, nullable=False, comment="Is this the latest version")
    parent_id = Column(UUID(as_uuid=True), ForeignKey('saved_calculations.id'), nullable=True, comment="Parent version")

    # Data Storage
    input_data = Column(JSONB, nullable=False, comment="Calculator input values (JSON)")
    output_data = Column(JSONB, nullable=False, comment="Calculator output/results (JSON)")

    # Metadata
    notes = Column(Text, nullable=True, comment="User notes about this calculation")
    tags = Column(JSONB, nullable=True, comment="Tags for organization (array)")
    is_favorite = Column(Boolean, default=False, comment="Mark as favorite")
    is_archived = Column(Boolean, default=False, comment="Archived calculation")

    # Sharing (future feature)
    is_shared = Column(Boolean, default=False, comment="Shared with team")
    share_token = Column(String(64), nullable=True, unique=True, comment="Public share token")

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    company = relationship("Company", foreign_keys=[company_id])
    parent_version = relationship("SavedCalculation", remote_side="SavedCalculation.id", foreign_keys=[parent_id])
    child_versions = relationship("SavedCalculation", back_populates="parent_version", foreign_keys=[parent_id])

    def to_dict(self):
        """Convert to dictionary with nested data."""
        data = super().to_dict()
        # input_data and output_data are already JSON from JSONB
        return data

    def create_new_version(self, new_input_data, new_output_data, notes=None):
        """
        Create a new version of this calculation.

        Returns a dict with the new version data.
        """
        return {
            'user_id': self.user_id,
            'company_id': self.company_id,
            'calculation_type': self.calculation_type,
            'property_name': self.property_name,
            'property_address': self.property_address,
            'version': self.version + 1,
            'is_current_version': True,
            'parent_id': self.id,
            'input_data': new_input_data,
            'output_data': new_output_data,
            'notes': notes,
            'tags': self.tags,
            'is_favorite': self.is_favorite,
        }
