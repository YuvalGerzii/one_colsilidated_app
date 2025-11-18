"""Real estate investment model tables."""

from sqlalchemy import Column, Integer, JSON, String

from app.models.database import Base, TimestampMixin, UUIDMixin


class RealEstateModelBase(Base, UUIDMixin, TimestampMixin):
    """Common columns shared by all real estate model records."""

    __abstract__ = True

    name = Column(String(255), nullable=False, comment="Deal or project name")
    location = Column(String(255), nullable=True, comment="Primary market or address")
    analyst = Column(String(255), nullable=True, comment="Person who created the record")
    notes = Column(String, nullable=True, comment="Optional internal notes")
    model_version = Column(String(50), nullable=False, default="1.0", comment="Model template version")
    inputs = Column(JSON, nullable=False, comment="Serialized user inputs")
    results = Column(JSON, nullable=False, comment="Serialized output metrics and projections")


class HotelFinancialModel(RealEstateModelBase):
    """Hotel development or acquisition financial model snapshot."""

    __tablename__ = "hotel_financial_models"

    hotel_type = Column(String(100), nullable=False, comment="Hotel segment (e.g. Luxury, Upscale)")


class SingleFamilyRentalModel(RealEstateModelBase):
    """Single family rental buy-and-hold / BRRRR model snapshot."""

    __tablename__ = "single_family_rental_models"

    strategy = Column(String(100), nullable=False, default="buy_and_hold", comment="Primary investment strategy")


class FixAndFlipModel(RealEstateModelBase):
    """Fix-and-flip project model snapshot."""

    __tablename__ = "fix_and_flip_models"

    market_type = Column(String(100), nullable=True, comment="Market speed guidance (e.g. Hot, Moderate)")


class SmallMultifamilyModel(RealEstateModelBase):
    """Small multifamily acquisition model snapshot."""

    __tablename__ = "small_multifamily_models"

    asset_class = Column(String(100), nullable=True, comment="Asset quality classification (Core, Value-Add, etc.)")


class SmallMultifamilyAcquisitionModel(RealEstateModelBase):
    """Small multifamily acquisition financial model with detailed unit analysis."""

    __tablename__ = "small_multifamily_acquisition_models"

    property_type = Column(String(100), nullable=True, comment="Property type (duplex, triplex, quadplex, small_multifamily)")
    number_of_units = Column(Integer, nullable=True, comment="Number of units in the property")


class HighRiseMultifamilyModel(RealEstateModelBase):
    """High-rise multifamily development model snapshot."""

    __tablename__ = "high_rise_multifamily_models"

    total_units = Column(Integer, nullable=True, comment="Reported unit count summary")


class MixedUseDevelopmentModel(RealEstateModelBase):
    """Mixed-use tower model snapshot."""

    __tablename__ = "mixed_use_development_models"

    primary_mix = Column(String(255), nullable=True, comment="Comma separated allocation mix summary")


class LeaseAnalyzerModel(RealEstateModelBase):
    """Lease analysis model snapshot for commercial properties."""

    __tablename__ = "lease_analyzer_models"

    property_type = Column(String(100), nullable=True, comment="Property type (Office, Retail, Industrial, etc.)")


class RenovationBudgetModel(RealEstateModelBase):
    """Renovation budget and value-add analysis model snapshot."""

    __tablename__ = "renovation_budget_models"

    property_type = Column(String(100), nullable=True, comment="Property type being renovated")
    total_units = Column(Integer, nullable=True, comment="Total units being renovated")


class SubdivisionModel(RealEstateModelBase):
    """Multi-unit subdivision and condo conversion analysis model snapshot."""

    __tablename__ = "subdivision_models"

    property_type = Column(String(100), nullable=True, comment="Property type (Duplex, Triplex, etc.)")
    num_units = Column(Integer, nullable=True, comment="Number of units in the property")
    exit_strategy = Column(String(100), nullable=True, comment="Primary exit strategy (Subdivide, As-Is, BRRRR)")


class TaxStrategyModel(RealEstateModelBase):
    """Comprehensive tax strategy integration analysis model snapshot."""

    __tablename__ = "tax_strategy_models"

    property_type = Column(String(100), nullable=True, comment="Property type for tax calculations")
    current_entity_type = Column(String(100), nullable=True, comment="Current entity structure (LLC, S-Corp, etc.)")
    total_tax_savings = Column(Integer, nullable=True, comment="Total potential tax savings from all strategies")


class PortfolioModel(RealEstateModelBase):
    """Multi-property portfolio dashboard and analytics snapshot."""

    __tablename__ = "portfolio_models"

    num_properties = Column(Integer, nullable=True, comment="Number of properties in the portfolio")
    total_portfolio_value = Column(Integer, nullable=True, comment="Total portfolio value in dollars")
    diversification_score = Column(Integer, nullable=True, comment="Portfolio diversification score (0-100)")


__all__ = [
    "HotelFinancialModel",
    "SingleFamilyRentalModel",
    "FixAndFlipModel",
    "SmallMultifamilyModel",
    "SmallMultifamilyAcquisitionModel",
    "HighRiseMultifamilyModel",
    "MixedUseDevelopmentModel",
    "LeaseAnalyzerModel",
    "RenovationBudgetModel",
    "SubdivisionModel",
    "TaxStrategyModel",
    "PortfolioModel",
]
