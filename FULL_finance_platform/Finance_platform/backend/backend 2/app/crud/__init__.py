"""CRUD operations."""

from app.crud.fund import fund_crud
from app.crud.company import company_crud
from app.crud.financial_metric import financial_metric_crud

__all__ = [
    "fund_crud",
    "company_crud",
    "financial_metric_crud",
]
