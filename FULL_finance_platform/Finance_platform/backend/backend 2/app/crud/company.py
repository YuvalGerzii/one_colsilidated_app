"""Company CRUD operations."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.company import PortfolioCompany
from app.schemas.company import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[PortfolioCompany, CompanyCreate, CompanyUpdate]):
    """CRUD operations for PortfolioCompany."""
    
    def get_by_fund(
        self, 
        db: Session, 
        fund_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PortfolioCompany]:
        """Get companies by fund."""
        return db.query(PortfolioCompany).filter(
            PortfolioCompany.fund_id == fund_id,
            PortfolioCompany.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_active(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PortfolioCompany]:
        """Get active companies."""
        return db.query(PortfolioCompany).filter(
            PortfolioCompany.company_status == 'Active',
            PortfolioCompany.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_sector(
        self, 
        db: Session, 
        sector: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[PortfolioCompany]:
        """Get companies by sector."""
        return db.query(PortfolioCompany).filter(
            PortfolioCompany.sector == sector,
            PortfolioCompany.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def soft_delete(self, db: Session, id: UUID, user_id: UUID = None) -> bool:
        """Soft delete a company."""
        company = self.get(db, id)
        if company:
            company.deleted_at = datetime.utcnow()
            company.deleted_by = user_id
            db.add(company)
            db.commit()
            return True
        return False


company_crud = CRUDCompany(PortfolioCompany)
