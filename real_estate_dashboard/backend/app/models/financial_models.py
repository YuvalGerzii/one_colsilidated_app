"""
Financial Models Database Models

This module contains database models for storing DCF and LBO financial analysis.
"""

from sqlalchemy import Column, String, Float, Integer, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.database import BaseModel, SoftDeleteMixin


class DCFModel(BaseModel, SoftDeleteMixin):
    """
    DCF (Discounted Cash Flow) Valuation Model

    Stores complete DCF analysis including inputs, assumptions, and results.
    """

    __tablename__ = "dcf_models"

    # Basic Info
    name = Column(String(255), nullable=False, index=True, comment="Model name")
    company_name = Column(String(255), nullable=True, comment="Company being valued")
    ticker = Column(String(20), nullable=True, comment="Stock ticker symbol")
    description = Column(Text, nullable=True, comment="Model description")

    # Company Info
    current_stock_price = Column(Float, nullable=True, comment="Current stock price ($)")
    shares_outstanding = Column(Float, nullable=True, comment="Shares outstanding (millions)")

    # Financial Projections (stored as JSON for flexibility)
    revenue_projections = Column(JSON, nullable=True, comment="5-year revenue projections")
    ebitda_margins = Column(JSON, nullable=True, comment="5-year EBITDA margin projections")
    capex_assumptions = Column(JSON, nullable=True, comment="CapEx as % of revenue")
    nwc_assumptions = Column(JSON, nullable=True, comment="NWC as % of revenue")
    dna_assumptions = Column(JSON, nullable=True, comment="D&A assumptions")

    # WACC Inputs
    risk_free_rate = Column(Float, nullable=True, comment="Risk-free rate (%)")
    beta = Column(Float, nullable=True, comment="Levered beta")
    market_risk_premium = Column(Float, nullable=True, comment="Market risk premium (%)")
    cost_of_debt = Column(Float, nullable=True, comment="Pre-tax cost of debt (%)")
    tax_rate = Column(Float, nullable=True, comment="Corporate tax rate (%)")
    debt_to_equity = Column(Float, nullable=True, comment="Debt-to-equity ratio")

    # Terminal Value
    terminal_growth_rate = Column(Float, nullable=True, comment="Terminal growth rate (%)")
    exit_multiple = Column(Float, nullable=True, comment="Exit EBITDA multiple")
    terminal_method = Column(String(50), nullable=True, comment="Growth or Multiple")

    # Balance Sheet Items
    cash = Column(Float, nullable=True, comment="Cash & equivalents ($M)")
    total_debt = Column(Float, nullable=True, comment="Total debt ($M)")
    preferred_stock = Column(Float, nullable=True, comment="Preferred stock ($M)")
    minority_interest = Column(Float, nullable=True, comment="Minority interest ($M)")

    # Results (stored as JSON)
    results = Column(JSON, nullable=True, comment="Calculation results")
    sensitivity_analysis = Column(JSON, nullable=True, comment="Sensitivity tables")
    scenario_analysis = Column(JSON, nullable=True, comment="Bull/Base/Bear scenarios")

    # Trading Comps
    trading_comps = Column(JSON, nullable=True, comment="Comparable companies data")

    # Historical Financials
    historical_financials = Column(JSON, nullable=True, comment="Historical financial data")

    # Metadata (Multi-Tenancy)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True, comment="User who created the model")
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this model belongs to (for multi-tenancy)"
    )
    is_template = Column(Integer, default=0, comment="1 if template, 0 otherwise")
    version = Column(Integer, default=1, comment="Model version number")

    def __repr__(self):
        return f"<DCFModel(id={self.id}, name='{self.name}', company='{self.company_name}')>"


class LBOModel(BaseModel, SoftDeleteMixin):
    """
    LBO (Leveraged Buyout) Model

    Stores complete LBO analysis including transaction structure, debt schedule,
    projections, and returns analysis.
    """

    __tablename__ = "lbo_models"

    # Basic Info
    name = Column(String(255), nullable=False, index=True, comment="Model name")
    company_name = Column(String(255), nullable=True, comment="Target company name")
    industry = Column(String(100), nullable=True, comment="Industry sector")
    description = Column(Text, nullable=True, comment="Model description")

    # Transaction Info
    transaction_date = Column(String(50), nullable=True, comment="Transaction date")
    holding_period = Column(Integer, nullable=True, comment="Holding period (years)")

    # Entry Valuation
    ltm_revenue = Column(Float, nullable=True, comment="LTM Revenue ($M)")
    ltm_ebitda = Column(Float, nullable=True, comment="LTM EBITDA ($M)")
    entry_ev_revenue_multiple = Column(Float, nullable=True, comment="Entry EV/Revenue")
    entry_ev_ebitda_multiple = Column(Float, nullable=True, comment="Entry EV/EBITDA")
    purchase_price = Column(Float, nullable=True, comment="Purchase price / EV ($M)")

    # Financing Structure
    total_leverage = Column(Float, nullable=True, comment="Total Debt / EBITDA")
    senior_leverage = Column(Float, nullable=True, comment="Senior Debt / EBITDA")

    # Sources & Uses (stored as JSON)
    sources = Column(JSON, nullable=True, comment="Sources of funds")
    uses = Column(JSON, nullable=True, comment="Uses of funds")

    # Transaction Costs
    ma_fees_pct = Column(Float, nullable=True, comment="M&A advisory fees (% of EV)")
    legal_fees = Column(Float, nullable=True, comment="Legal & other fees ($M)")
    financing_fees_pct = Column(Float, nullable=True, comment="Financing fees (% of debt)")

    # Debt Structure (stored as JSON for multiple tranches)
    debt_schedule = Column(JSON, nullable=True, comment="Detailed debt schedule")

    # Operating Projections (stored as JSON)
    revenue_projections = Column(JSON, nullable=True, comment="7-year revenue projections")
    ebitda_margins = Column(JSON, nullable=True, comment="7-year EBITDA margins")
    capex_assumptions = Column(JSON, nullable=True, comment="CapEx assumptions")
    nwc_assumptions = Column(JSON, nullable=True, comment="NWC assumptions")
    dna_expense = Column(JSON, nullable=True, comment="D&A expense")

    # Exit Assumptions
    exit_ev_ebitda_multiple = Column(Float, nullable=True, comment="Exit EV/EBITDA")

    # Distribution Waterfall
    preferred_return = Column(Float, nullable=True, comment="Preferred return / hurdle (%)")
    gp_catchup_pct = Column(Float, nullable=True, comment="GP catch-up percentage")
    carried_interest_pct = Column(Float, nullable=True, comment="Carried interest / GP carry (%)")

    # Results (stored as JSON)
    results = Column(JSON, nullable=True, comment="Returns analysis results")
    credit_metrics = Column(JSON, nullable=True, comment="Leverage and coverage ratios")
    sensitivity_analysis = Column(JSON, nullable=True, comment="Sensitivity tables")
    distribution_waterfall = Column(JSON, nullable=True, comment="LP/GP distribution details")

    # Metadata (Multi-Tenancy)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True, comment="User who created the model")
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this model belongs to (for multi-tenancy)"
    )
    is_template = Column(Integer, default=0, comment="1 if template, 0 otherwise")
    version = Column(Integer, default=1, comment="Model version number")

    def __repr__(self):
        return f"<LBOModel(id={self.id}, name='{self.name}', company='{self.company_name}')>"


class ComparableCompany(BaseModel):
    """
    Comparable Company for Trading Comps Analysis

    Used in DCF models for relative valuation.
    """

    __tablename__ = "comparable_companies"

    # Foreign Key
    dcf_model_id = Column(UUID(as_uuid=True), ForeignKey('dcf_models.id'), nullable=True)

    # Company Info
    company_name = Column(String(255), nullable=False, comment="Company name")
    ticker = Column(String(20), nullable=True, comment="Ticker symbol")

    # Valuation Metrics
    market_cap = Column(Float, nullable=True, comment="Market capitalization ($M)")
    enterprise_value = Column(Float, nullable=True, comment="Enterprise value ($M)")

    # Financial Metrics
    revenue_ltm = Column(Float, nullable=True, comment="LTM Revenue ($M)")
    ebitda_ltm = Column(Float, nullable=True, comment="LTM EBITDA ($M)")
    ebit_ltm = Column(Float, nullable=True, comment="LTM EBIT ($M)")
    net_income = Column(Float, nullable=True, comment="Net income ($M)")

    # Growth & Margins
    revenue_growth = Column(Float, nullable=True, comment="Revenue growth rate (%)")
    ebitda_margin = Column(Float, nullable=True, comment="EBITDA margin (%)")

    # Calculated Multiples (can be computed)
    ev_revenue = Column(Float, nullable=True, comment="EV/Revenue multiple")
    ev_ebitda = Column(Float, nullable=True, comment="EV/EBITDA multiple")
    ev_ebit = Column(Float, nullable=True, comment="EV/EBIT multiple")
    pe_ratio = Column(Float, nullable=True, comment="P/E ratio")

    # Relationship
    dcf_model = relationship("DCFModel", backref="comparables")

    def __repr__(self):
        return f"<ComparableCompany(id={self.id}, name='{self.company_name}', ticker='{self.ticker}')>"


# Export all
__all__ = [
    "DCFModel",
    "LBOModel",
    "ComparableCompany",
]
