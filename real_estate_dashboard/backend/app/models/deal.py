"""Deal model for multi-type transactions (real estate, company acquisition, shares, commodities)."""

from sqlalchemy import Column, String, Integer, Float, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.database import BaseModel


class DealStage(str, enum.Enum):
    """Deal pipeline stages."""
    IDENTIFIED = "identified"
    INITIAL_REVIEW = "initial_review"
    LOI_SUBMITTED = "loi_submitted"
    DUE_DILIGENCE = "due_diligence"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"
    CLOSED = "closed"
    PASSED = "passed"


class DealStatus(str, enum.Enum):
    """Deal status."""
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DealType(str, enum.Enum):
    """Types of deals supported."""
    REAL_ESTATE = "real_estate"
    COMPANY_ACQUISITION = "company_acquisition"
    SHARES = "shares"
    COMMODITIES = "commodities"
    DEBT = "debt"
    OTHER = "other"


class Deal(BaseModel):
    """
    Deal model supporting multiple transaction types.

    Supports:
    - Real estate transactions
    - Company acquisitions
    - Share purchases
    - Commodity trading
    - Debt instruments
    """

    __tablename__ = "deals"
    __table_args__ = {'extend_existing': True}

    # Core Deal Information
    deal_type = Column(String(50), default="real_estate", nullable=False, index=True, comment="Type of deal")
    deal_name = Column(String(255), nullable=True, comment="General deal name")
    stage = Column(String(50), nullable=True, index=True, comment="Current stage in pipeline")
    status = Column(String(50), nullable=True, index=True, comment="Deal status")

    # Company Association
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="Associated company"
    )

    # Financial Information (Universal)
    asking_price = Column(Float, nullable=True, comment="Asking/listed price")
    offer_price = Column(Float, nullable=True, comment="Our offer price")
    estimated_value = Column(Float, nullable=True, comment="Estimated market value")
    purchase_price = Column(Float, nullable=True, comment="Final purchase price")
    currency = Column(String(10), default="USD", comment="Currency code")

    # Real Estate Specific
    property_name = Column(String(255), nullable=True, comment="Property name")
    property_address = Column(String(500), nullable=True, comment="Property address")
    property_type = Column(String(100), nullable=True, comment="Property type (multifamily, office, etc)")
    market = Column(String(100), nullable=True, comment="Market/location")
    units = Column(Integer, nullable=True, comment="Number of units")
    square_feet = Column(Integer, nullable=True, comment="Square footage")
    cap_rate = Column(Float, nullable=True, comment="Capitalization rate")
    irr_target = Column(Float, nullable=True, comment="Target IRR %")

    # Company Acquisition Specific
    target_company = Column(String(255), nullable=True, comment="Target company name")
    sector = Column(String(100), nullable=True, comment="Industry sector")

    # Shares/Equity Specific
    ticker_symbol = Column(String(20), nullable=True, comment="Stock ticker symbol")
    quantity = Column(Float, nullable=True, comment="Quantity of shares/units")
    asset_class = Column(String(100), nullable=True, comment="Asset class (equity, debt, etc)")

    # Commodities Specific
    commodity_type = Column(String(100), nullable=True, comment="Type of commodity")

    # Team & External Parties
    broker_id = Column(UUID(as_uuid=True), ForeignKey("brokers.id"), nullable=True, comment="Broker/intermediary")
    lead_analyst = Column(String(255), nullable=True, comment="Lead analyst/deal manager")

    # Timeline
    date_identified = Column(Date, nullable=True, comment="Date deal was identified")
    loi_date = Column(Date, nullable=True, comment="Letter of Intent date")
    due_diligence_start = Column(Date, nullable=True, comment="DD start date")
    due_diligence_end = Column(Date, nullable=True, comment="DD end date")
    expected_closing = Column(Date, nullable=True, comment="Expected closing date")
    actual_closing = Column(Date, nullable=True, comment="Actual closing date")

    # Analysis
    notes = Column(Text, nullable=True, comment="General notes")
    pros = Column(Text, nullable=True, comment="Pros/advantages")
    cons = Column(Text, nullable=True, comment="Cons/risks")

    # Metadata
    documents_url = Column(String(500), nullable=True, comment="Document storage URL")
    priority = Column(Integer, default=5, comment="Priority (1-10)")
    confidence_level = Column(Integer, nullable=True, comment="Confidence level (0-100)")

    # Relationships
    company = relationship("Company", foreign_keys=[company_id], backref="deals")
    broker = relationship("Broker", foreign_keys=[broker_id], back_populates="deals")

    def to_dict(self):
        """Convert to dictionary with all fields."""
        data = super().to_dict()
        # Convert enums to strings
        if self.stage:
            data['stage'] = str(self.stage)
        if self.status:
            data['status'] = str(self.status)
        if self.deal_type:
            data['deal_type'] = str(self.deal_type)
        return data

    @property
    def display_name(self) -> str:
        """Get display name based on deal type."""
        if self.deal_name:
            return self.deal_name
        elif self.property_name:
            return self.property_name
        elif self.target_company:
            return self.target_company
        elif self.ticker_symbol:
            return f"{self.ticker_symbol} ({self.quantity} shares)"
        elif self.commodity_type:
            return f"{self.commodity_type} ({self.quantity})"
        return f"Deal {self.id}"

    @property
    def is_real_estate(self) -> bool:
        """Check if this is a real estate deal."""
        return self.deal_type == DealType.REAL_ESTATE.value

    @property
    def is_company_acquisition(self) -> bool:
        """Check if this is a company acquisition."""
        return self.deal_type == DealType.COMPANY_ACQUISITION.value

    @property
    def is_shares(self) -> bool:
        """Check if this is a shares/equity deal."""
        return self.deal_type == DealType.SHARES.value

    @property
    def is_commodity(self) -> bool:
        """Check if this is a commodity deal."""
        return self.deal_type == DealType.COMMODITIES.value
