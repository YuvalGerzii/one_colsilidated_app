"""
Query Optimization Utilities

This module provides utilities to prevent N+1 query problems by eager loading
related data using SQLAlchemy's joinedload and selectinload.
"""

from sqlalchemy.orm import joinedload, selectinload, Query


def eager_load_property_relations(query: Query) -> Query:
    """
    Eager load common Property relationships to prevent N+1 queries.

    Usage:
        query = db.query(Property)
        query = eager_load_property_relations(query)
        properties = query.all()  # No N+1 queries!
    """
    return query.options(
        selectinload('units'),
        selectinload('leases'),
        selectinload('financials'),
        selectinload('maintenance_requests'),
    )


def eager_load_fund_relations(query: Query) -> Query:
    """
    Eager load common Fund relationships to prevent N+1 queries.

    Relationships loaded:
    - Limited partners
    - Capital calls
    - Distributions
    - Portfolio investments
    """
    return query.options(
        selectinload('limited_partners'),
        selectinload('capital_calls'),
        selectinload('distributions'),
        selectinload('portfolio_investments'),
    )


def eager_load_loan_relations(query: Query) -> Query:
    """
    Eager load common Loan relationships to prevent N+1 queries.

    Relationships loaded:
    - Property (if exists)
    - Amortization schedule entries
    - Debt covenants
    """
    return query.options(
        joinedload('property'),  # Many-to-one, use joinedload
        selectinload('amortization_entries'),
        selectinload('debt_covenants'),
    )


def eager_load_deal_relations(query: Query) -> Query:
    """
    Eager load common Deal relationships to prevent N+1 queries.

    Relationships loaded:
    - Broker
    - Comparables
    """
    return query.options(
        joinedload('broker'),
        selectinload('comps'),
    )


def eager_load_project_relations(query: Query) -> Query:
    """
    Eager load common Project relationships to prevent N+1 queries.

    Relationships loaded:
    - Tasks
    - Milestones
    - Updates
    """
    return query.options(
        selectinload('tasks'),
        selectinload('milestones'),
        selectinload('updates'),
    )


def eager_load_dashboard_relations(query: Query) -> Query:
    """
    Eager load common Dashboard relationships to prevent N+1 queries.

    Relationships loaded:
    - Widgets
    - Filters
    """
    return query.options(
        selectinload('widgets'),
        selectinload('filters'),
    )


# Export all utilities
__all__ = [
    'eager_load_property_relations',
    'eager_load_fund_relations',
    'eager_load_loan_relations',
    'eager_load_deal_relations',
    'eager_load_project_relations',
    'eager_load_dashboard_relations',
]
