"""Fund CRUD operations."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fund import Fund
from app.schemas.fund import FundCreate, FundUpdate


class CRUDFund(CRUDBase[Fund, FundCreate, FundUpdate]):
    """CRUD operations for Fund."""
    
    def get_by_vintage_year(self, db: Session, vintage_year: int) -> List[Fund]:
        """Get funds by vintage year."""
        return db.query(Fund).filter(Fund.vintage_year == vintage_year).all()
    
    def get_active(self, db: Session, skip: int = 0, limit: int = 100) -> List[Fund]:
        """Get active funds."""
        return db.query(Fund).filter(
            Fund.fund_status == 'Active'
        ).offset(skip).limit(limit).all()


fund_crud = CRUDFund(Fund)
