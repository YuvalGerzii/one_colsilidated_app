"""Dashboard API endpoints."""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.company import PortfolioCompany
from app.models.financial_metric import FinancialMetric

router = APIRouter()


@router.get("/")
def get_dashboard_data(
    fund_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """Get aggregated dashboard data."""
    # Base query
    query = db.query(PortfolioCompany).filter(
        PortfolioCompany.deleted_at == None
    )
    
    if fund_id:
        query = query.filter(PortfolioCompany.fund_id == fund_id)
    
    companies = query.all()
    
    # Calculate aggregates
    total_companies = len(companies)
    active_companies = len([c for c in companies if c.company_status == 'Active'])
    total_invested = sum(float(c.equity_invested or 0) for c in companies)
    
    # Get latest revenue and EBITDA
    latest_metrics = db.query(
        func.sum(FinancialMetric.revenue).label('total_revenue'),
        func.sum(FinancialMetric.ebitda).label('total_ebitda')
    ).join(PortfolioCompany).filter(
        PortfolioCompany.deleted_at == None
    )
    
    if fund_id:
        latest_metrics = latest_metrics.filter(PortfolioCompany.fund_id == fund_id)
    
    metrics = latest_metrics.first()
    
    return {
        "total_companies": total_companies,
        "active_companies": active_companies,
        "total_invested": total_invested,
        "total_revenue": float(metrics[0] or 0),
        "total_ebitda": float(metrics[1] or 0),
        "companies": [
            {
                "id": str(c.id),
                "name": c.company_name,
                "sector": c.sector,
                "status": c.company_status,
                "investment_date": c.investment_date.isoformat() if c.investment_date else None,
                "equity_invested": float(c.equity_invested or 0)
            }
            for c in companies[:10]  # Top 10 for summary
        ]
    }
