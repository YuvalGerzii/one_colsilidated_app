"""
Interactive Dashboards API Endpoints

Endpoints for:
- Dashboard CRUD operations
- Widget management (drag-and-drop positioning)
- Custom KPI tracking
- Benchmark comparisons
- Performance attribution analysis
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.interactive_dashboards import (
    Dashboard, DashboardWidget, CustomKPI, Benchmark,
    PerformanceAttribution, DashboardFilter,
    DashboardType, WidgetType, KPICalculationType, BenchmarkType
)
from app.models.user import User
from app.models.company import Company

router = APIRouter()


# ================================
# PYDANTIC SCHEMAS
# ================================

class DashboardCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    dashboard_type: str
    company_id: Optional[UUID] = None
    is_public: bool = False
    is_default: bool = False
    layout_config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    default_filters: Optional[Dict[str, Any]] = None


class DashboardUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    layout_config: Optional[Dict[str, Any]] = None
    theme_config: Optional[Dict[str, Any]] = None
    default_filters: Optional[Dict[str, Any]] = None


class WidgetCreate(BaseModel):
    dashboard_id: UUID
    title: str = Field(..., max_length=200)
    widget_type: str
    position_x: int = 0
    position_y: int = 0
    width: int = 4
    height: int = 3
    data_source: Optional[str] = None
    data_config: Optional[Dict[str, Any]] = None
    chart_config: Optional[Dict[str, Any]] = None
    drill_down_enabled: bool = False


class WidgetUpdate(BaseModel):
    title: Optional[str] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    data_config: Optional[Dict[str, Any]] = None
    chart_config: Optional[Dict[str, Any]] = None
    is_visible: Optional[bool] = None


class CustomKPICreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    company_id: Optional[UUID] = None
    calculation_type: str
    formula: Optional[str] = None
    data_sources: Dict[str, Any]
    target_value: Optional[Decimal] = None
    unit: Optional[str] = None


class BenchmarkCreate(BaseModel):
    name: str = Field(..., max_length=200)
    benchmark_type: str
    metric_name: str
    value: Decimal
    company_id: Optional[UUID] = None
    geography: Optional[str] = None
    property_type: Optional[str] = None
    as_of_date: date
    data_source: Optional[str] = None


# ================================
# DASHBOARD CRUD
# ================================

@router.post("/dashboards", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_dashboard(
    dashboard: DashboardCreate,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Create a new dashboard.

    Supports custom layouts, themes, and default filters.
    """
    # Validate dashboard type
    try:
        DashboardType(dashboard.dashboard_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid dashboard type. Must be one of: {[t.value for t in DashboardType]}"
        )

    # Create dashboard
    new_dashboard = Dashboard(
        user_id=user_id,
        **dashboard.dict()
    )

    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)

    return {
        "id": str(new_dashboard.id),
        "name": new_dashboard.name,
        "dashboard_type": new_dashboard.dashboard_type,
        "is_public": new_dashboard.is_public,
        "created_at": new_dashboard.created_at.isoformat(),
    }


@router.get("/dashboards", response_model=List[dict])
def get_dashboards(
    user_id: UUID = Query(...),
    company_id: Optional[UUID] = Query(None),
    dashboard_type: Optional[str] = Query(None),
    include_public: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Get all dashboards for a user.

    Includes user's own dashboards and public dashboards if requested.
    """
    query = db.query(Dashboard).filter(Dashboard.is_archived == False)

    # Build filter conditions
    conditions = [Dashboard.user_id == user_id]

    if include_public:
        public_condition = and_(
            Dashboard.is_public == True,
            Dashboard.company_id == company_id if company_id else True
        )
        conditions = [or_(Dashboard.user_id == user_id, public_condition)]

    query = query.filter(*conditions)

    if company_id:
        query = query.filter(Dashboard.company_id == company_id)

    if dashboard_type:
        query = query.filter(Dashboard.dashboard_type == dashboard_type)

    dashboards = query.order_by(desc(Dashboard.last_viewed_at), desc(Dashboard.created_at)).all()

    return [
        {
            "id": str(d.id),
            "name": d.name,
            "description": d.description,
            "dashboard_type": d.dashboard_type,
            "is_public": d.is_public,
            "is_default": d.is_default,
            "widget_count": len(d.widgets),
            "last_viewed_at": d.last_viewed_at.isoformat() if d.last_viewed_at else None,
            "created_at": d.created_at.isoformat(),
        }
        for d in dashboards
    ]


@router.get("/dashboards/{dashboard_id}", response_model=dict)
def get_dashboard(
    dashboard_id: UUID,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Get a specific dashboard with all its widgets.
    """
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()

    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    # Check permissions
    if dashboard.user_id != user_id and not dashboard.is_public:
        raise HTTPException(status_code=403, detail="Access denied")

    # Update last viewed
    dashboard.last_viewed_at = datetime.utcnow()
    dashboard.view_count += 1
    db.commit()

    # Get widgets
    widgets = db.query(DashboardWidget).filter(
        DashboardWidget.dashboard_id == dashboard_id,
        DashboardWidget.is_visible == True
    ).order_by(DashboardWidget.order).all()

    return {
        "id": str(dashboard.id),
        "name": dashboard.name,
        "description": dashboard.description,
        "dashboard_type": dashboard.dashboard_type,
        "layout_config": dashboard.layout_config,
        "theme_config": dashboard.theme_config,
        "default_filters": dashboard.default_filters,
        "is_public": dashboard.is_public,
        "widgets": [
            {
                "id": str(w.id),
                "title": w.title,
                "widget_type": w.widget_type,
                "position_x": w.position_x,
                "position_y": w.position_y,
                "width": w.width,
                "height": w.height,
                "data_source": w.data_source,
                "data_config": w.data_config,
                "chart_config": w.chart_config,
                "drill_down_enabled": w.drill_down_enabled,
                "drill_down_config": w.drill_down_config,
            }
            for w in widgets
        ],
        "created_at": dashboard.created_at.isoformat(),
        "updated_at": dashboard.updated_at.isoformat(),
    }


@router.put("/dashboards/{dashboard_id}", response_model=dict)
def update_dashboard(
    dashboard_id: UUID,
    dashboard_update: DashboardUpdate,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """Update dashboard configuration."""
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == dashboard_id,
        Dashboard.user_id == user_id
    ).first()

    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    # Update fields
    for field, value in dashboard_update.dict(exclude_unset=True).items():
        setattr(dashboard, field, value)

    db.commit()
    db.refresh(dashboard)

    return {
        "id": str(dashboard.id),
        "name": dashboard.name,
        "updated_at": dashboard.updated_at.isoformat(),
    }


@router.delete("/dashboards/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dashboard(
    dashboard_id: UUID,
    user_id: UUID = Query(...),
    permanent: bool = Query(False),
    db: Session = Depends(get_db)
):
    """
    Delete or archive a dashboard.

    By default, archives the dashboard. Use permanent=true to permanently delete.
    """
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == dashboard_id,
        Dashboard.user_id == user_id
    ).first()

    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    if permanent:
        db.delete(dashboard)
    else:
        dashboard.is_archived = True

    db.commit()


# ================================
# WIDGET MANAGEMENT
# ================================

@router.post("/widgets", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_widget(
    widget: WidgetCreate,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Add a widget to a dashboard.

    Supports various chart types and data visualizations.
    """
    # Verify dashboard ownership
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == widget.dashboard_id,
        Dashboard.user_id == user_id
    ).first()

    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    # Validate widget type
    try:
        WidgetType(widget.widget_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid widget type. Must be one of: {[t.value for t in WidgetType]}"
        )

    # Create widget
    new_widget = DashboardWidget(**widget.dict())

    db.add(new_widget)
    db.commit()
    db.refresh(new_widget)

    return {
        "id": str(new_widget.id),
        "dashboard_id": str(new_widget.dashboard_id),
        "title": new_widget.title,
        "widget_type": new_widget.widget_type,
        "created_at": new_widget.created_at.isoformat(),
    }


@router.put("/widgets/{widget_id}", response_model=dict)
def update_widget(
    widget_id: UUID,
    widget_update: WidgetUpdate,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Update widget configuration or position.

    Use this for drag-and-drop positioning updates.
    """
    # Get widget and verify ownership through dashboard
    widget = db.query(DashboardWidget).join(Dashboard).filter(
        DashboardWidget.id == widget_id,
        Dashboard.user_id == user_id
    ).first()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    # Update fields
    for field, value in widget_update.dict(exclude_unset=True).items():
        setattr(widget, field, value)

    db.commit()
    db.refresh(widget)

    return {
        "id": str(widget.id),
        "position_x": widget.position_x,
        "position_y": widget.position_y,
        "width": widget.width,
        "height": widget.height,
        "updated_at": widget.updated_at.isoformat(),
    }


@router.post("/widgets/bulk-update", response_model=dict)
def bulk_update_widgets(
    updates: List[dict] = Body(..., description="List of widget updates with id and position"),
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Bulk update widget positions.

    Useful for saving layout changes after drag-and-drop operations.
    """
    updated_count = 0

    for update in updates:
        widget_id = UUID(update["id"])

        widget = db.query(DashboardWidget).join(Dashboard).filter(
            DashboardWidget.id == widget_id,
            Dashboard.user_id == user_id
        ).first()

        if widget:
            widget.position_x = update.get("position_x", widget.position_x)
            widget.position_y = update.get("position_y", widget.position_y)
            widget.width = update.get("width", widget.width)
            widget.height = update.get("height", widget.height)
            updated_count += 1

    db.commit()

    return {
        "updated_count": updated_count,
        "total_requested": len(updates),
    }


@router.delete("/widgets/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_widget(
    widget_id: UUID,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """Remove a widget from a dashboard."""
    widget = db.query(DashboardWidget).join(Dashboard).filter(
        DashboardWidget.id == widget_id,
        Dashboard.user_id == user_id
    ).first()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    db.delete(widget)
    db.commit()


# ================================
# CUSTOM KPIS
# ================================

@router.post("/kpis", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_custom_kpi(
    kpi: CustomKPICreate,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    """
    Define a custom KPI for tracking.

    Supports various calculation methods including custom formulas.
    """
    # Validate calculation type
    try:
        KPICalculationType(kpi.calculation_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid calculation type. Must be one of: {[t.value for t in KPICalculationType]}"
        )

    new_kpi = CustomKPI(
        user_id=user_id,
        **kpi.dict()
    )

    db.add(new_kpi)
    db.commit()
    db.refresh(new_kpi)

    return {
        "id": str(new_kpi.id),
        "name": new_kpi.name,
        "calculation_type": new_kpi.calculation_type,
        "created_at": new_kpi.created_at.isoformat(),
    }


@router.get("/kpis", response_model=List[dict])
def get_custom_kpis(
    user_id: UUID = Query(...),
    company_id: Optional[UUID] = Query(None),
    category: Optional[str] = Query(None),
    include_public: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all custom KPIs for a user."""
    query = db.query(CustomKPI).filter(CustomKPI.is_active == True)

    # User's own KPIs or public KPIs
    conditions = [CustomKPI.user_id == user_id]

    if include_public:
        public_condition = and_(
            CustomKPI.is_public == True,
            CustomKPI.company_id == company_id if company_id else True
        )
        conditions = [or_(CustomKPI.user_id == user_id, public_condition)]

    query = query.filter(*conditions)

    if category:
        query = query.filter(CustomKPI.category == category)

    kpis = query.order_by(desc(CustomKPI.created_at)).all()

    return [
        {
            "id": str(k.id),
            "name": k.name,
            "category": k.category,
            "calculation_type": k.calculation_type,
            "target_value": float(k.target_value) if k.target_value else None,
            "last_calculated_value": float(k.last_calculated_value) if k.last_calculated_value else None,
            "last_calculated_at": k.last_calculated_at.isoformat() if k.last_calculated_at else None,
            "unit": k.unit,
        }
        for k in kpis
    ]


@router.get("/kpis/{kpi_id}/calculate", response_model=dict)
def calculate_kpi(
    kpi_id: UUID,
    user_id: UUID = Query(...),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Calculate a custom KPI value.

    Returns the calculated value and comparison to target/previous period.
    """
    kpi = db.query(CustomKPI).filter(CustomKPI.id == kpi_id).first()

    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    # Check permissions
    if kpi.user_id != user_id and not kpi.is_public:
        raise HTTPException(status_code=403, detail="Access denied")

    # TODO: Implement actual calculation logic based on kpi.calculation_type and kpi.data_sources
    # This would query the appropriate data sources and apply the formula

    calculated_value = 0.0  # Placeholder

    # Update KPI record
    kpi.last_calculated_value = Decimal(str(calculated_value))
    kpi.last_calculated_at = datetime.utcnow()
    db.commit()

    return {
        "kpi_id": str(kpi.id),
        "name": kpi.name,
        "calculated_value": calculated_value,
        "target_value": float(kpi.target_value) if kpi.target_value else None,
        "variance": calculated_value - float(kpi.target_value) if kpi.target_value else None,
        "variance_percentage": (
            ((calculated_value - float(kpi.target_value)) / float(kpi.target_value) * 100)
            if kpi.target_value and kpi.target_value != 0 else None
        ),
        "unit": kpi.unit,
        "calculated_at": datetime.utcnow().isoformat(),
    }


# ================================
# BENCHMARKS
# ================================

@router.post("/benchmarks", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_benchmark(
    benchmark: BenchmarkCreate,
    db: Session = Depends(get_db)
):
    """
    Create a benchmark for comparison.

    Supports industry averages, peer groups, and custom targets.
    """
    # Validate benchmark type
    try:
        BenchmarkType(benchmark.benchmark_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid benchmark type. Must be one of: {[t.value for t in BenchmarkType]}"
        )

    new_benchmark = Benchmark(**benchmark.dict())

    db.add(new_benchmark)
    db.commit()
    db.refresh(new_benchmark)

    return {
        "id": str(new_benchmark.id),
        "name": new_benchmark.name,
        "benchmark_type": new_benchmark.benchmark_type,
        "metric_name": new_benchmark.metric_name,
        "value": float(new_benchmark.value),
        "created_at": new_benchmark.created_at.isoformat(),
    }


@router.get("/benchmarks", response_model=List[dict])
def get_benchmarks(
    metric_name: Optional[str] = Query(None),
    benchmark_type: Optional[str] = Query(None),
    company_id: Optional[UUID] = Query(None),
    geography: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get benchmarks filtered by various criteria.
    """
    query = db.query(Benchmark).filter(Benchmark.is_active == True)

    if metric_name:
        query = query.filter(Benchmark.metric_name == metric_name)
    if benchmark_type:
        query = query.filter(Benchmark.benchmark_type == benchmark_type)
    if company_id:
        query = query.filter(
            or_(Benchmark.company_id == company_id, Benchmark.company_id == None)
        )
    if geography:
        query = query.filter(Benchmark.geography == geography)
    if property_type:
        query = query.filter(Benchmark.property_type == property_type)

    benchmarks = query.order_by(desc(Benchmark.as_of_date)).limit(100).all()

    return [
        {
            "id": str(b.id),
            "name": b.name,
            "benchmark_type": b.benchmark_type,
            "metric_name": b.metric_name,
            "value": float(b.value),
            "value_range_min": float(b.value_range_min) if b.value_range_min else None,
            "value_range_max": float(b.value_range_max) if b.value_range_max else None,
            "geography": b.geography,
            "property_type": b.property_type,
            "as_of_date": b.as_of_date.isoformat(),
            "data_source": b.data_source,
            "percentile_25": float(b.percentile_25) if b.percentile_25 else None,
            "percentile_50": float(b.percentile_50) if b.percentile_50 else None,
            "percentile_75": float(b.percentile_75) if b.percentile_75 else None,
        }
        for b in benchmarks
    ]


@router.get("/benchmarks/compare", response_model=dict)
def compare_to_benchmark(
    metric_name: str = Query(...),
    actual_value: float = Query(...),
    benchmark_type: str = Query(...),
    company_id: Optional[UUID] = Query(None),
    geography: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Compare an actual value to benchmarks.

    Returns the variance and percentile ranking.
    """
    # Find matching benchmark
    query = db.query(Benchmark).filter(
        Benchmark.metric_name == metric_name,
        Benchmark.benchmark_type == benchmark_type,
        Benchmark.is_active == True
    )

    if company_id:
        query = query.filter(
            or_(Benchmark.company_id == company_id, Benchmark.company_id == None)
        )
    if geography:
        query = query.filter(Benchmark.geography == geography)
    if property_type:
        query = query.filter(Benchmark.property_type == property_type)

    benchmark = query.order_by(desc(Benchmark.as_of_date)).first()

    if not benchmark:
        raise HTTPException(status_code=404, detail="No matching benchmark found")

    # Calculate comparison metrics
    variance = actual_value - float(benchmark.value)
    variance_pct = (variance / float(benchmark.value) * 100) if benchmark.value != 0 else None

    # Determine percentile if available
    percentile_rank = None
    if benchmark.percentile_25 and benchmark.percentile_75:
        if actual_value < float(benchmark.percentile_25):
            percentile_rank = "Below 25th percentile"
        elif actual_value > float(benchmark.percentile_75):
            percentile_rank = "Above 75th percentile"
        else:
            percentile_rank = "25th-75th percentile"

    return {
        "actual_value": actual_value,
        "benchmark_value": float(benchmark.value),
        "benchmark_name": benchmark.name,
        "variance": variance,
        "variance_percentage": variance_pct,
        "percentile_rank": percentile_rank,
        "benchmark_date": benchmark.as_of_date.isoformat(),
        "data_source": benchmark.data_source,
    }


# ================================
# PERFORMANCE ATTRIBUTION
# ================================

@router.post("/performance-attribution/analyze", response_model=dict)
def analyze_performance_attribution(
    company_id: UUID = Body(...),
    start_date: date = Body(...),
    end_date: date = Body(...),
    db: Session = Depends(get_db)
):
    """
    Perform performance attribution analysis.

    Breaks down returns into asset allocation, security selection,
    and interaction effects.
    """
    # TODO: Implement actual attribution calculation
    # This would involve:
    # 1. Calculate portfolio returns
    # 2. Calculate benchmark returns
    # 3. Decompose into allocation and selection effects
    # 4. Calculate risk-adjusted metrics

    # Placeholder implementation
    attribution = PerformanceAttribution(
        analysis_date=date.today(),
        analysis_period_start=start_date,
        analysis_period_end=end_date,
        company_id=company_id,
        total_return=Decimal("12.5"),
        benchmark_return=Decimal("10.0"),
        excess_return=Decimal("2.5"),
        asset_allocation_effect=Decimal("1.2"),
        security_selection_effect=Decimal("1.5"),
        interaction_effect=Decimal("-0.2"),
        attribution_method="Brinson",
    )

    db.add(attribution)
    db.commit()
    db.refresh(attribution)

    return {
        "id": str(attribution.id),
        "total_return": float(attribution.total_return),
        "benchmark_return": float(attribution.benchmark_return),
        "excess_return": float(attribution.excess_return),
        "asset_allocation_effect": float(attribution.asset_allocation_effect),
        "security_selection_effect": float(attribution.security_selection_effect),
        "interaction_effect": float(attribution.interaction_effect),
        "analysis_period": f"{start_date.isoformat()} to {end_date.isoformat()}",
    }


@router.get("/performance-attribution", response_model=List[dict])
def get_performance_attribution(
    company_id: Optional[UUID] = Query(None),
    fund_id: Optional[UUID] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get historical performance attribution analyses."""
    query = db.query(PerformanceAttribution)

    if company_id:
        query = query.filter(PerformanceAttribution.company_id == company_id)
    if fund_id:
        query = query.filter(PerformanceAttribution.fund_id == fund_id)
    if start_date:
        query = query.filter(PerformanceAttribution.analysis_date >= start_date)
    if end_date:
        query = query.filter(PerformanceAttribution.analysis_date <= end_date)

    attributions = query.order_by(desc(PerformanceAttribution.analysis_date)).limit(limit).all()

    return [
        {
            "id": str(a.id),
            "analysis_date": a.analysis_date.isoformat(),
            "total_return": float(a.total_return),
            "benchmark_return": float(a.benchmark_return) if a.benchmark_return else None,
            "excess_return": float(a.excess_return) if a.excess_return else None,
            "asset_allocation_effect": float(a.asset_allocation_effect) if a.asset_allocation_effect else None,
            "security_selection_effect": float(a.security_selection_effect) if a.security_selection_effect else None,
        }
        for a in attributions
    ]
