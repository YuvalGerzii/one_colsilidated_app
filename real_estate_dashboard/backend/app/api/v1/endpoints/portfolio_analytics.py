"""
Portfolio Analytics API Endpoints

Endpoints for:
- Historical performance tracking
- IRR calculations across portfolio
- Geographic heat maps
- Sector/property type diversification
- Cash flow projections
- Debt maturity schedule
- Risk metrics (concentration, leverage ratios)
"""

from datetime import date, datetime, timedelta
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
import numpy as np
from numpy_financial import irr as calculate_irr

from app.core.database import get_db
from app.models.portfolio_analytics import (
    PortfolioSnapshot,
    PortfolioPerformanceMetric,
    CashFlowProjection,
    PortfolioRiskMetric,
    GeographicPerformance,
    PerformanceMetricType,
    RiskMetricType,
)
from app.models.property_management import Property, PropertyFinancial, PropertyStatus
from app.models.fund_management import Fund, PortfolioInvestment, Distribution
from app.models.debt_management import Loan, LoanStatus
from app.models.company import Company

router = APIRouter()


# ================================
# HELPER FUNCTIONS - IRR & CALCULATIONS
# ================================

def calculate_portfolio_irr(
    db: Session,
    company_id: Optional[UUID] = None,
    fund_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Optional[float]:
    """
    Calculate IRR for a portfolio (company or fund level).

    IRR = rate at which NPV of all cash flows equals zero
    Cash flows include: initial investment, distributions, current value
    """
    # Build query for investments
    query = db.query(PortfolioInvestment)

    if company_id:
        query = query.filter(PortfolioInvestment.company_id == company_id)
    if fund_id:
        query = query.filter(PortfolioInvestment.fund_id == fund_id)

    investments = query.all()

    if not investments:
        return None

    # Collect all cash flows with dates
    cash_flows = []

    for inv in investments:
        # Initial investment (negative cash flow)
        if inv.acquisition_date:
            cash_flows.append({
                'date': inv.acquisition_date,
                'amount': -float(inv.initial_investment or 0)
            })

        # Distributions (positive cash flows)
        distributions = db.query(Distribution).filter(
            Distribution.property_id == inv.property_id
        ).all()

        for dist in distributions:
            if dist.distribution_date:
                cash_flows.append({
                    'date': dist.distribution_date,
                    'amount': float(dist.total_amount or 0)
                })

        # Current value (positive cash flow at end date)
        current_value = inv.current_value or inv.initial_investment or 0
        cash_flows.append({
            'date': end_date or date.today(),
            'amount': float(current_value)
        })

    if not cash_flows:
        return None

    # Sort by date
    cash_flows.sort(key=lambda x: x['date'])

    # Convert to time-weighted cash flows for IRR calculation
    # Using days from first cash flow
    first_date = cash_flows[0]['date']

    # Group by date and sum
    date_flows = {}
    for cf in cash_flows:
        days = (cf['date'] - first_date).days
        if days not in date_flows:
            date_flows[days] = 0
        date_flows[days] += cf['amount']

    # Convert to array for numpy_financial
    sorted_days = sorted(date_flows.keys())
    flows = [date_flows[d] for d in sorted_days]

    try:
        # Calculate IRR using numpy_financial
        irr_value = calculate_irr(flows)

        # Convert to annual percentage
        if not np.isnan(irr_value) and not np.isinf(irr_value):
            # Annualize based on period
            days_total = sorted_days[-1] if sorted_days else 365
            periods_per_year = 365 / max(days_total, 1)
            annual_irr = ((1 + irr_value) ** periods_per_year - 1) * 100
            return round(annual_irr, 2)
    except:
        pass

    return None


def calculate_moic(
    total_distributions: Decimal,
    current_value: Decimal,
    initial_investment: Decimal
) -> Optional[float]:
    """
    Calculate Multiple on Invested Capital (MOIC).

    MOIC = (Total Distributions + Current Value) / Initial Investment
    """
    if not initial_investment or initial_investment == 0:
        return None

    total_return = float(total_distributions + current_value)
    return round(total_return / float(initial_investment), 2)


def calculate_weighted_average(items: List[tuple], weight_key: str = 'value') -> Optional[float]:
    """Calculate weighted average."""
    if not items:
        return None

    total_weight = sum(item[1] for item in items)
    if total_weight == 0:
        return None

    weighted_sum = sum(item[0] * item[1] for item in items)
    return round(weighted_sum / total_weight, 2)


# ================================
# PORTFOLIO SNAPSHOTS
# ================================

@router.post("/snapshots", response_model=dict)
def create_portfolio_snapshot(
    snapshot_date: date = Body(...),
    company_id: Optional[UUID] = Body(None),
    fund_id: Optional[UUID] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Create a portfolio snapshot for a given date.

    Captures point-in-time metrics including:
    - Portfolio composition
    - Financial metrics
    - Performance metrics
    - Risk metrics
    - Geographic/sector distribution
    """
    # Validate that either company_id or fund_id is provided
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    # Query properties for this portfolio
    property_query = db.query(Property).filter(Property.status != PropertyStatus.SOLD)

    if company_id:
        property_query = property_query.filter(Property.company_id == company_id)
    if fund_id:
        # Properties linked to fund through PortfolioInvestment
        property_query = property_query.join(PortfolioInvestment).filter(
            PortfolioInvestment.fund_id == fund_id
        )

    properties = property_query.all()

    # Calculate portfolio composition
    total_properties = len(properties)
    total_units = sum(p.number_of_units or 0 for p in properties)
    total_square_feet = sum(float(p.square_footage or 0) for p in properties)

    # Calculate financial metrics
    total_asset_value = Decimal(0)
    total_equity = Decimal(0)
    total_debt = Decimal(0)

    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            total_asset_value += financials.total_assets or 0
            total_equity += financials.equity_value or 0

    # Calculate total debt from loans
    loan_query = db.query(func.sum(Loan.principal_amount)).filter(
        Loan.status == LoanStatus.ACTIVE
    )

    if company_id:
        loan_query = loan_query.filter(Loan.company_id == company_id)

    total_debt = loan_query.scalar() or Decimal(0)

    # Calculate income metrics
    gross_rental_income = Decimal(0)
    operating_expenses = Decimal(0)
    net_operating_income = Decimal(0)

    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            gross_rental_income += financials.gross_rental_income or 0
            operating_expenses += financials.total_operating_expenses or 0
            net_operating_income += financials.net_operating_income or 0

    # Calculate performance metrics
    portfolio_irr = calculate_portfolio_irr(db, company_id, fund_id, end_date=snapshot_date)

    # Calculate average occupancy (weighted by units)
    occupancy_data = [(p.occupancy_rate or 0, p.number_of_units or 0) for p in properties if p.occupancy_rate]
    average_occupancy = calculate_weighted_average(occupancy_data)

    # Calculate average cap rate (weighted by value)
    cap_rate_data = []
    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials and financials.cap_rate and financials.total_assets:
            cap_rate_data.append((financials.cap_rate, float(financials.total_assets)))

    average_cap_rate = calculate_weighted_average(cap_rate_data)

    # Calculate risk metrics
    average_ltv = None
    if total_asset_value > 0:
        average_ltv = round((float(total_debt) / float(total_asset_value)) * 100, 2)

    # Calculate geographic distribution
    geographic_distribution = {}
    for prop in properties:
        state = prop.state or "Unknown"
        if state not in geographic_distribution:
            geographic_distribution[state] = 0

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        value = float(financials.total_assets) if financials else 0
        geographic_distribution[state] += value

    # Calculate sector distribution
    sector_distribution = {}
    for prop in properties:
        property_type = prop.property_type.value if prop.property_type else "Unknown"
        if property_type not in sector_distribution:
            sector_distribution[property_type] = 0

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        value = float(financials.total_assets) if financials else 0
        sector_distribution[property_type] += value

    # Create snapshot
    snapshot = PortfolioSnapshot(
        snapshot_date=snapshot_date,
        company_id=company_id,
        fund_id=fund_id,
        total_properties=total_properties,
        total_units=total_units,
        total_square_feet=Decimal(str(total_square_feet)),
        total_asset_value=total_asset_value,
        total_equity=total_equity,
        total_debt=total_debt,
        total_cash=Decimal(0),  # TODO: Calculate from cash accounts
        gross_rental_income=gross_rental_income,
        operating_expenses=operating_expenses,
        net_operating_income=net_operating_income,
        portfolio_irr=portfolio_irr,
        average_occupancy=average_occupancy,
        average_cap_rate=average_cap_rate,
        average_ltv=average_ltv,
        geographic_distribution=geographic_distribution,
        sector_distribution=sector_distribution,
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return {
        "id": str(snapshot.id),
        "snapshot_date": snapshot.snapshot_date.isoformat(),
        "total_properties": snapshot.total_properties,
        "total_asset_value": float(snapshot.total_asset_value),
        "portfolio_irr": snapshot.portfolio_irr,
        "average_occupancy": snapshot.average_occupancy,
        "geographic_distribution": snapshot.geographic_distribution,
        "sector_distribution": snapshot.sector_distribution,
    }


@router.get("/snapshots", response_model=List[dict])
def get_portfolio_snapshots(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get historical portfolio snapshots."""
    query = db.query(PortfolioSnapshot)

    if company_id:
        query = query.filter(PortfolioSnapshot.company_id == company_id)
    if fund_id:
        query = query.filter(PortfolioSnapshot.fund_id == fund_id)
    if start_date:
        query = query.filter(PortfolioSnapshot.snapshot_date >= start_date)
    if end_date:
        query = query.filter(PortfolioSnapshot.snapshot_date <= end_date)

    snapshots = query.order_by(desc(PortfolioSnapshot.snapshot_date)).limit(limit).all()

    return [
        {
            "id": str(s.id),
            "snapshot_date": s.snapshot_date.isoformat(),
            "total_properties": s.total_properties,
            "total_units": s.total_units,
            "total_asset_value": float(s.total_asset_value),
            "total_equity": float(s.total_equity),
            "total_debt": float(s.total_debt),
            "net_operating_income": float(s.net_operating_income) if s.net_operating_income else None,
            "portfolio_irr": s.portfolio_irr,
            "average_occupancy": s.average_occupancy,
            "average_cap_rate": s.average_cap_rate,
            "average_ltv": s.average_ltv,
            "geographic_distribution": s.geographic_distribution,
            "sector_distribution": s.sector_distribution,
        }
        for s in snapshots
    ]


# ================================
# IRR & PERFORMANCE METRICS
# ================================

@router.get("/performance/irr", response_model=dict)
def get_portfolio_irr(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Calculate IRR across the portfolio.

    Returns IRR at portfolio level with breakdown by property.
    """
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    # Calculate portfolio-level IRR
    portfolio_irr = calculate_portfolio_irr(db, company_id, fund_id, start_date, end_date)

    # Get property-level IRRs
    property_irrs = []

    query = db.query(Property)
    if company_id:
        query = query.filter(Property.company_id == company_id)
    if fund_id:
        query = query.join(PortfolioInvestment).filter(PortfolioInvestment.fund_id == fund_id)

    properties = query.all()

    for prop in properties:
        # Get investment for this property
        inv = db.query(PortfolioInvestment).filter(
            PortfolioInvestment.property_id == prop.id
        ).first()

        if inv:
            # Calculate property-level IRR
            prop_irr = calculate_portfolio_irr(
                db,
                start_date=inv.acquisition_date,
                end_date=end_date or date.today()
            )

            property_irrs.append({
                "property_id": str(prop.id),
                "property_name": prop.name,
                "irr": prop_irr,
                "initial_investment": float(inv.initial_investment) if inv.initial_investment else None,
                "current_value": float(inv.current_value) if inv.current_value else None,
            })

    return {
        "portfolio_irr": portfolio_irr,
        "property_breakdown": property_irrs,
        "calculation_date": (end_date or date.today()).isoformat(),
    }


@router.get("/performance/metrics", response_model=dict)
def get_performance_metrics(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    metric_types: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get various performance metrics (IRR, MOIC, Cash-on-Cash, etc.).
    """
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    metrics = {}

    # IRR
    if not metric_types or "irr" in metric_types:
        metrics["irr"] = calculate_portfolio_irr(db, company_id, fund_id)

    # MOIC
    if not metric_types or "moic" in metric_types:
        # Get total investments
        inv_query = db.query(
            func.sum(PortfolioInvestment.initial_investment),
            func.sum(PortfolioInvestment.current_value)
        )

        if company_id:
            inv_query = inv_query.filter(PortfolioInvestment.company_id == company_id)
        if fund_id:
            inv_query = inv_query.filter(PortfolioInvestment.fund_id == fund_id)

        initial_inv, current_val = inv_query.first()

        # Get total distributions
        dist_query = db.query(func.sum(Distribution.total_amount))
        if company_id:
            dist_query = dist_query.filter(Distribution.company_id == company_id)
        if fund_id:
            dist_query = dist_query.filter(Distribution.fund_id == fund_id)

        total_dist = dist_query.scalar() or Decimal(0)

        moic = calculate_moic(total_dist, current_val or Decimal(0), initial_inv or Decimal(0))
        metrics["moic"] = moic

    # Average occupancy
    if not metric_types or "occupancy" in metric_types:
        prop_query = db.query(Property)
        if company_id:
            prop_query = prop_query.filter(Property.company_id == company_id)
        if fund_id:
            prop_query = prop_query.join(PortfolioInvestment).filter(
                PortfolioInvestment.fund_id == fund_id
            )

        properties = prop_query.all()
        occupancy_data = [(p.occupancy_rate or 0, p.number_of_units or 0) for p in properties if p.occupancy_rate]
        metrics["average_occupancy"] = calculate_weighted_average(occupancy_data)

    # NOI
    if not metric_types or "noi" in metric_types:
        prop_query = db.query(Property)
        if company_id:
            prop_query = prop_query.filter(Property.company_id == company_id)
        if fund_id:
            prop_query = prop_query.join(PortfolioInvestment).filter(
                PortfolioInvestment.fund_id == fund_id
            )

        properties = prop_query.all()
        total_noi = Decimal(0)

        for prop in properties:
            financials = db.query(PropertyFinancial).filter(
                PropertyFinancial.property_id == prop.id
            ).order_by(desc(PropertyFinancial.report_date)).first()

            if financials:
                total_noi += financials.net_operating_income or 0

        metrics["total_noi"] = float(total_noi)

    return metrics


# ================================
# GEOGRAPHIC HEAT MAP DATA
# ================================

@router.get("/geographic/performance", response_model=List[dict])
def get_geographic_performance(
    company_id: Optional[UUID] = Query(None),
    metric_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get performance metrics by geographic location for heat maps.

    Returns data suitable for rendering on a map with performance indicators.
    """
    if not metric_date:
        metric_date = date.today()

    # Get all properties
    query = db.query(Property).filter(Property.status != PropertyStatus.SOLD)
    if company_id:
        query = query.filter(Property.company_id == company_id)

    properties = query.all()

    # Group by location
    location_data = {}

    for prop in properties:
        # Use city as primary grouping
        location_key = f"{prop.city}, {prop.state}" if prop.city and prop.state else prop.state or "Unknown"

        if location_key not in location_data:
            location_data[location_key] = {
                "state": prop.state,
                "city": prop.city,
                "country": "USA",  # TODO: Add country to Property model
                "latitude": prop.latitude,
                "longitude": prop.longitude,
                "properties": [],
                "total_value": 0,
                "total_noi": 0,
                "total_units": 0,
            }

        # Get financials
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        location_data[location_key]["properties"].append(prop)
        location_data[location_key]["total_units"] += prop.number_of_units or 0

        if financials:
            location_data[location_key]["total_value"] += float(financials.total_assets or 0)
            location_data[location_key]["total_noi"] += float(financials.net_operating_income or 0)

    # Calculate metrics for each location
    result = []
    total_portfolio_value = sum(loc["total_value"] for loc in location_data.values())

    for location_key, data in location_data.items():
        properties = data["properties"]

        # Calculate weighted averages
        occupancy_data = [(p.occupancy_rate or 0, p.number_of_units or 0) for p in properties if p.occupancy_rate]
        avg_occupancy = calculate_weighted_average(occupancy_data)

        # Calculate concentration
        concentration = 0
        if total_portfolio_value > 0:
            concentration = round((data["total_value"] / total_portfolio_value) * 100, 2)

        result.append({
            "state": data["state"],
            "city": data["city"],
            "country": data["country"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "property_count": len(properties),
            "total_value": data["total_value"],
            "total_noi": data["total_noi"],
            "total_units": data["total_units"],
            "average_occupancy": avg_occupancy,
            "concentration_percentage": concentration,
        })

    return result


# ================================
# CASH FLOW PROJECTIONS
# ================================

@router.post("/cash-flow/projections", response_model=dict)
def create_cash_flow_projections(
    company_id: UUID = Body(...),
    projection_months: int = Body(12, ge=1, le=36),
    scenario: str = Body("base"),
    db: Session = Depends(get_db)
):
    """
    Create rolling cash flow projections.

    Projects income, expenses, and capital events for the next N months.
    Supports multiple scenarios: base, optimistic, pessimistic.
    """
    projection_date = date.today()

    # Get all active properties
    properties = db.query(Property).filter(
        Property.company_id == company_id,
        Property.status != PropertyStatus.SOLD
    ).all()

    projections = []

    for month in range(projection_months):
        # Calculate projection for this month
        future_date = projection_date + timedelta(days=30 * month)

        projected_rental_income = Decimal(0)
        projected_operating_expenses = Decimal(0)
        projected_debt_service = Decimal(0)

        for prop in properties:
            # Get latest financials
            financials = db.query(PropertyFinancial).filter(
                PropertyFinancial.property_id == prop.id
            ).order_by(desc(PropertyFinancial.report_date)).first()

            if financials:
                # Monthly rental income
                monthly_rental = (financials.gross_rental_income or 0) / 12

                # Apply scenario adjustments
                if scenario == "optimistic":
                    monthly_rental *= Decimal("1.1")  # 10% increase
                elif scenario == "pessimistic":
                    monthly_rental *= Decimal("0.9")  # 10% decrease

                projected_rental_income += monthly_rental

                # Monthly operating expenses
                monthly_opex = (financials.total_operating_expenses or 0) / 12
                projected_operating_expenses += monthly_opex

        # Get debt service
        loans = db.query(Loan).filter(
            Loan.company_id == company_id,
            Loan.status == LoanStatus.ACTIVE
        ).all()

        for loan in loans:
            # Calculate monthly payment
            if loan.monthly_payment:
                projected_debt_service += loan.monthly_payment

        # Net cash flow
        projected_total_income = projected_rental_income
        projected_total_expenses = projected_operating_expenses + projected_debt_service
        projected_net_cash_flow = projected_total_income - projected_total_expenses

        # Create projection
        projection = CashFlowProjection(
            projection_date=projection_date,
            projection_month=month,
            company_id=company_id,
            projected_rental_income=projected_rental_income,
            projected_total_income=projected_total_income,
            projected_operating_expenses=projected_operating_expenses,
            projected_debt_service=projected_debt_service,
            projected_total_expenses=projected_total_expenses,
            projected_net_cash_flow=projected_net_cash_flow,
            confidence_level="medium",
            scenario=scenario,
        )

        db.add(projection)
        projections.append(projection)

    db.commit()

    return {
        "projection_date": projection_date.isoformat(),
        "scenario": scenario,
        "projection_months": projection_months,
        "projections": [
            {
                "month": p.projection_month,
                "projected_total_income": float(p.projected_total_income),
                "projected_total_expenses": float(p.projected_total_expenses),
                "projected_net_cash_flow": float(p.projected_net_cash_flow),
            }
            for p in projections
        ]
    }


@router.get("/cash-flow/projections", response_model=List[dict])
def get_cash_flow_projections(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    scenario: Optional[str] = Query(None),
    limit: int = Query(12, ge=1, le=36),
    db: Session = Depends(get_db)
):
    """Get cash flow projections."""
    query = db.query(CashFlowProjection)

    if company_id:
        query = query.filter(CashFlowProjection.company_id == company_id)
    if fund_id:
        query = query.filter(CashFlowProjection.fund_id == fund_id)
    if scenario:
        query = query.filter(CashFlowProjection.scenario == scenario)

    # Get most recent projections
    latest_projection_date = db.query(func.max(CashFlowProjection.projection_date)).scalar()

    if latest_projection_date:
        query = query.filter(CashFlowProjection.projection_date == latest_projection_date)

    projections = query.order_by(CashFlowProjection.projection_month).limit(limit).all()

    return [
        {
            "projection_month": p.projection_month,
            "projected_total_income": float(p.projected_total_income),
            "projected_total_expenses": float(p.projected_total_expenses),
            "projected_net_cash_flow": float(p.projected_net_cash_flow),
            "projected_debt_service": float(p.projected_debt_service) if p.projected_debt_service else None,
            "scenario": p.scenario,
            "confidence_level": p.confidence_level,
        }
        for p in projections
    ]


# ================================
# DEBT MATURITY SCHEDULE
# ================================

@router.get("/debt/maturity-schedule", response_model=List[dict])
def get_debt_maturity_schedule(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    months_ahead: int = Query(36, ge=1, le=120),
    db: Session = Depends(get_db)
):
    """
    Get debt maturity schedule showing when loans come due.

    Returns loans grouped by maturity date for planning refinancing.
    """
    query = db.query(Loan).filter(Loan.status == LoanStatus.ACTIVE)

    if company_id:
        query = query.filter(Loan.company_id == company_id)

    loans = query.order_by(Loan.maturity_date).all()

    # Filter by months ahead
    cutoff_date = date.today() + timedelta(days=30 * months_ahead)

    maturity_schedule = []

    for loan in loans:
        if loan.maturity_date and loan.maturity_date <= cutoff_date:
            # Get property info
            property_name = "N/A"
            if loan.property_id:
                prop = db.query(Property).filter(Property.id == loan.property_id).first()
                if prop:
                    property_name = prop.name

            # Calculate months until maturity
            months_until = (loan.maturity_date - date.today()).days / 30

            maturity_schedule.append({
                "loan_id": str(loan.id),
                "property_id": str(loan.property_id) if loan.property_id else None,
                "property_name": property_name,
                "lender": loan.lender_name,
                "principal_amount": float(loan.principal_amount),
                "current_balance": float(loan.current_balance) if loan.current_balance else float(loan.principal_amount),
                "interest_rate": loan.interest_rate,
                "maturity_date": loan.maturity_date.isoformat(),
                "months_until_maturity": round(months_until, 1),
                "loan_type": loan.loan_type.value if loan.loan_type else None,
            })

    return maturity_schedule


# ================================
# RISK METRICS
# ================================

@router.get("/risk/concentration", response_model=dict)
def get_concentration_risk(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Calculate concentration risk across multiple dimensions:
    - Geographic concentration
    - Sector/property type concentration
    - Tenant concentration (if applicable)
    """
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    # Get properties
    query = db.query(Property).filter(Property.status != PropertyStatus.SOLD)
    if company_id:
        query = query.filter(Property.company_id == company_id)
    if fund_id:
        query = query.join(PortfolioInvestment).filter(PortfolioInvestment.fund_id == fund_id)

    properties = query.all()

    # Calculate total portfolio value
    total_value = Decimal(0)
    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            total_value += financials.total_assets or 0

    # Geographic concentration
    geographic_concentration = {}
    for prop in properties:
        state = prop.state or "Unknown"
        if state not in geographic_concentration:
            geographic_concentration[state] = 0

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        value = float(financials.total_assets) if financials else 0
        geographic_concentration[state] += value

    # Convert to percentages
    geographic_pct = {
        state: round((value / float(total_value)) * 100, 2) if total_value > 0 else 0
        for state, value in geographic_concentration.items()
    }

    # Sector concentration
    sector_concentration = {}
    for prop in properties:
        sector = prop.property_type.value if prop.property_type else "Unknown"
        if sector not in sector_concentration:
            sector_concentration[sector] = 0

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        value = float(financials.total_assets) if financials else 0
        sector_concentration[sector] += value

    # Convert to percentages
    sector_pct = {
        sector: round((value / float(total_value)) * 100, 2) if total_value > 0 else 0
        for sector, value in sector_concentration.items()
    }

    # Calculate risk scores (0-100)
    # Higher concentration = higher risk
    geo_risk_score = max(geographic_pct.values()) if geographic_pct else 0
    sector_risk_score = max(sector_pct.values()) if sector_pct else 0

    return {
        "geographic_concentration": geographic_pct,
        "geographic_risk_score": geo_risk_score,
        "sector_concentration": sector_pct,
        "sector_risk_score": sector_risk_score,
        "total_portfolio_value": float(total_value),
    }


@router.get("/risk/leverage", response_model=dict)
def get_leverage_metrics(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Calculate leverage and debt service metrics:
    - Loan-to-Value (LTV) ratio
    - Debt Service Coverage Ratio (DSCR)
    - Interest Coverage Ratio
    """
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    # Get total asset value
    query = db.query(Property).filter(Property.status != PropertyStatus.SOLD)
    if company_id:
        query = query.filter(Property.company_id == company_id)
    if fund_id:
        query = query.join(PortfolioInvestment).filter(PortfolioInvestment.fund_id == fund_id)

    properties = query.all()

    total_asset_value = Decimal(0)
    total_noi = Decimal(0)

    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            total_asset_value += financials.total_assets or 0
            total_noi += financials.net_operating_income or 0

    # Get total debt
    loan_query = db.query(Loan).filter(Loan.status == LoanStatus.ACTIVE)
    if company_id:
        loan_query = loan_query.filter(Loan.company_id == company_id)

    loans = loan_query.all()

    total_debt = sum(float(loan.current_balance or loan.principal_amount) for loan in loans)
    annual_debt_service = sum(float(loan.monthly_payment or 0) * 12 for loan in loans)

    # Calculate LTV
    ltv = None
    if total_asset_value > 0:
        ltv = round((total_debt / float(total_asset_value)) * 100, 2)

    # Calculate DSCR
    dscr = None
    if annual_debt_service > 0:
        dscr = round(float(total_noi) / annual_debt_service, 2)

    return {
        "total_asset_value": float(total_asset_value),
        "total_debt": total_debt,
        "loan_to_value": ltv,
        "debt_service_coverage_ratio": dscr,
        "annual_noi": float(total_noi),
        "annual_debt_service": annual_debt_service,
    }


# ================================
# DIVERSIFICATION ANALYSIS
# ================================

@router.get("/diversification", response_model=dict)
def get_diversification_analysis(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive diversification analysis across:
    - Property types
    - Geographic locations
    - Investment sizes
    - Vintage (acquisition years)
    """
    if not company_id and not fund_id:
        raise HTTPException(status_code=400, detail="Either company_id or fund_id must be provided")

    # Get properties
    query = db.query(Property).filter(Property.status != PropertyStatus.SOLD)
    if company_id:
        query = query.filter(Property.company_id == company_id)
    if fund_id:
        query = query.join(PortfolioInvestment).filter(PortfolioInvestment.fund_id == fund_id)

    properties = query.all()

    # Calculate total value
    total_value = Decimal(0)
    for prop in properties:
        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            total_value += financials.total_assets or 0

    # Property type distribution
    property_type_dist = {}
    for prop in properties:
        ptype = prop.property_type.value if prop.property_type else "Unknown"
        if ptype not in property_type_dist:
            property_type_dist[ptype] = {"count": 0, "value": 0}

        property_type_dist[ptype]["count"] += 1

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            property_type_dist[ptype]["value"] += float(financials.total_assets or 0)

    # Convert to percentages
    property_type_pct = {
        ptype: {
            "count": data["count"],
            "value": data["value"],
            "percentage": round((data["value"] / float(total_value)) * 100, 2) if total_value > 0 else 0
        }
        for ptype, data in property_type_dist.items()
    }

    # Geographic distribution
    geographic_dist = {}
    for prop in properties:
        state = prop.state or "Unknown"
        if state not in geographic_dist:
            geographic_dist[state] = {"count": 0, "value": 0}

        geographic_dist[state]["count"] += 1

        financials = db.query(PropertyFinancial).filter(
            PropertyFinancial.property_id == prop.id
        ).order_by(desc(PropertyFinancial.report_date)).first()

        if financials:
            geographic_dist[state]["value"] += float(financials.total_assets or 0)

    # Convert to percentages
    geographic_pct = {
        state: {
            "count": data["count"],
            "value": data["value"],
            "percentage": round((data["value"] / float(total_value)) * 100, 2) if total_value > 0 else 0
        }
        for state, data in geographic_dist.items()
    }

    return {
        "property_type_distribution": property_type_pct,
        "geographic_distribution": geographic_pct,
        "total_properties": len(properties),
        "total_value": float(total_value),
    }
