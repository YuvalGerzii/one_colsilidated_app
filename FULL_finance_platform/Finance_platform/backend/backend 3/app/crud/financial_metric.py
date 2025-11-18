"""Financial metric CRUD operations."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.financial_metric import FinancialMetric
from app.schemas.financial_metric import FinancialMetricCreate, FinancialMetricUpdate


class CRUDFinancialMetric(CRUDBase[FinancialMetric, FinancialMetricCreate, FinancialMetricUpdate]):
    """CRUD operations for FinancialMetric."""
    
    def get_by_company(
        self, 
        db: Session, 
        company_id: UUID,
        period_type: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[FinancialMetric]:
        """Get financial metrics by company."""
        query = db.query(FinancialMetric).filter(
            FinancialMetric.company_id == company_id
        )
        if period_type:
            query = query.filter(FinancialMetric.period_type == period_type)
        return query.order_by(desc(FinancialMetric.period_date)).offset(skip).limit(limit).all()
    
    def get_latest(self, db: Session, company_id: UUID) -> Optional[FinancialMetric]:
        """Get latest financial metric for a company."""
        return db.query(FinancialMetric).filter(
            FinancialMetric.company_id == company_id
        ).order_by(desc(FinancialMetric.period_date)).first()


financial_metric_crud = CRUDFinancialMetric(FinancialMetric)
