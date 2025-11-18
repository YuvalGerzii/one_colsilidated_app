"""
Company KPI Database Model

Stores operational KPIs (non-financial metrics) for portfolio companies.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import Column, String, Date, Integer, Numeric, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.database import BaseModel, AuditMixin


class CompanyKPI(BaseModel, AuditMixin):
    """
    Company KPI Model
    
    Stores operational KPIs like customer metrics, headcount, product metrics.
    """
    
    __tablename__ = "company_kpis"
    __table_args__ = (
        CheckConstraint(
            "period_type IN ('Monthly', 'Quarterly', 'Annual')",
            name="valid_period_type"
        ),
    )
    
    company_id = Column(UUID(as_uuid=True), ForeignKey("portfolio_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    period_date = Column(Date, nullable=False, index=True)
    period_type = Column(String(20), nullable=False)
    
    # SaaS Metrics
    arr = Column(Numeric(15, 2), comment="Annual Recurring Revenue")
    mrr = Column(Numeric(15, 2), comment="Monthly Recurring Revenue")
    net_revenue_retention = Column(Numeric(5, 4), comment="Net Revenue Retention %")
    gross_revenue_retention = Column(Numeric(5, 4), comment="Gross Revenue Retention %")
    customer_churn_rate = Column(Numeric(5, 4), comment="Customer churn rate %")
    revenue_churn_rate = Column(Numeric(5, 4), comment="Revenue churn rate %")
    
    # Customer Metrics
    total_customers = Column(Integer, comment="Total customers")
    new_customers = Column(Integer, comment="New customers added")
    churned_customers = Column(Integer, comment="Customers churned")
    active_customers = Column(Integer, comment="Active customers")
    arpu = Column(Numeric(15, 2), comment="Average Revenue Per User")
    
    # Sales & Marketing
    cac = Column(Numeric(15, 2), comment="Customer Acquisition Cost")
    ltv = Column(Numeric(15, 2), comment="Lifetime Value")
    ltv_cac_ratio = Column(Numeric(10, 2), comment="LTV/CAC ratio")
    magic_number = Column(Numeric(10, 2), comment="SaaS Magic Number")
    sales_efficiency = Column(Numeric(10, 2), comment="Sales efficiency ratio")
    
    # Operational
    headcount = Column(Integer, comment="Total headcount")
    revenue_per_employee = Column(Numeric(15, 2), comment="Revenue per employee")
    gross_margin_per_employee = Column(Numeric(15, 2), comment="Gross margin per employee")
    
    # Product/Tech
    monthly_active_users = Column(Integer, comment="Monthly active users")
    daily_active_users = Column(Integer, comment="Daily active users")
    nps_score = Column(Integer, comment="Net Promoter Score")
    product_adoption_rate = Column(Numeric(5, 4), comment="Product adoption rate %")
    
    company = relationship("PortfolioCompany", back_populates="kpis")
    
    def __repr__(self):
        return f"<CompanyKPI(company_id={self.company_id}, period={self.period_date})>"
