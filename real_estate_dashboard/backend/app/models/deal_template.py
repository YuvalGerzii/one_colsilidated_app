"""Deal Template model for reusable deal configurations."""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.database import BaseModel


class DealTemplate(BaseModel):
    """
    Deal Template model for saving reusable deal configurations.

    Allows users to save common deal setups (e.g., "Standard Multifamily Acquisition",
    "Small Cap Rate Deal", etc.) and quickly create new deals from these templates.
    """

    __tablename__ = "deal_templates"

    # Template Info
    name = Column(String(255), nullable=False, comment="Template name")
    description = Column(Text, nullable=True, comment="Template description")
    deal_type = Column(String(50), nullable=False, default="real_estate", comment="Type of deal")

    # Company Association
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="Associated company (if null, it's a system template)"
    )

    # Template Configuration (stores default values)
    default_values = Column(
        JSON,
        nullable=False,
        default=dict,
        comment="Default field values for this template (JSON)"
    )

    # Metadata
    is_system_template = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="If true, this is a system-wide template"
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Template is active and visible"
    )
    usage_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of times this template has been used"
    )

    # Relationships
    company = relationship("Company", foreign_keys=[company_id], backref="deal_templates")

    def to_dict(self):
        """Convert to dictionary with all fields."""
        data = super().to_dict()
        return data

    @property
    def is_public(self) -> bool:
        """Check if this is a public/system template."""
        return self.is_system_template or self.company_id is None
