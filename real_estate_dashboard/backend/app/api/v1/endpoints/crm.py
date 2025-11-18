"""CRM endpoints for deal pipeline, brokers/agents, and comps database."""

from datetime import date
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import desc, or_, func
from sqlalchemy.orm import Session
from pathlib import Path

from app.core.database import get_db
from app.core.auth import get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.crm import (
    Deal, DealStage, DealStatus, Broker, BrokerStatus, Comp,
    DealTask, TaskStatus, TaskPriority,
    DealDocument, DocumentStatus,
    DealReminder, ReminderType,
    DealStageRule,
    EmailTemplate,
    DealActivity, ActivityType,
    DealScore
)
from app.services.automation_service import deal_automation_service
from app.services.deal_scoring_service import deal_scoring_service
from app.services.comp_pulling_service import comp_pulling_service
from app.services.notification_service import notification_service
from app.services.due_diligence_integration import due_diligence_integration
from app.tasks.deal_scoring import score_single_deal
from app.tasks.deal_automation import auto_pull_comps

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[4] / "templates"))


# ===== Pydantic Schemas =====

class DealCreate(BaseModel):
    property_name: str
    property_address: Optional[str] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    stage: DealStage = DealStage.RESEARCH
    status: DealStatus = DealStatus.ACTIVE
    asking_price: Optional[float] = None
    offer_price: Optional[float] = None
    estimated_value: Optional[float] = None
    purchase_price: Optional[float] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    cap_rate: Optional[float] = None
    irr_target: Optional[float] = None
    broker_id: Optional[UUID] = None
    lead_analyst: Optional[str] = None
    date_identified: Optional[date] = None
    loi_date: Optional[date] = None
    due_diligence_start: Optional[date] = None
    due_diligence_end: Optional[date] = None
    expected_closing: Optional[date] = None
    actual_closing: Optional[date] = None
    notes: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    documents_url: Optional[str] = None
    priority: Optional[int] = 3
    confidence_level: Optional[int] = None


class DealUpdate(BaseModel):
    property_name: Optional[str] = None
    property_address: Optional[str] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    stage: Optional[DealStage] = None
    status: Optional[DealStatus] = None
    asking_price: Optional[float] = None
    offer_price: Optional[float] = None
    estimated_value: Optional[float] = None
    purchase_price: Optional[float] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    cap_rate: Optional[float] = None
    irr_target: Optional[float] = None
    broker_id: Optional[UUID] = None
    lead_analyst: Optional[str] = None
    date_identified: Optional[date] = None
    loi_date: Optional[date] = None
    due_diligence_start: Optional[date] = None
    due_diligence_end: Optional[date] = None
    expected_closing: Optional[date] = None
    actual_closing: Optional[date] = None
    notes: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    documents_url: Optional[str] = None
    priority: Optional[int] = None
    confidence_level: Optional[int] = None


class BrokerCreate(BaseModel):
    first_name: str
    last_name: str
    company: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    office_address: Optional[str] = None
    primary_market: Optional[str] = None
    specialties: Optional[str] = None
    status: BrokerStatus = BrokerStatus.ACTIVE
    relationship_strength: Optional[int] = 3
    notes: Optional[str] = None
    last_contact_date: Optional[date] = None


class BrokerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    office_address: Optional[str] = None
    primary_market: Optional[str] = None
    specialties: Optional[str] = None
    status: Optional[BrokerStatus] = None
    relationship_strength: Optional[int] = None
    notes: Optional[str] = None
    last_contact_date: Optional[date] = None


class CompCreate(BaseModel):
    property_name: str
    property_address: Optional[str] = None
    property_type: str
    market: Optional[str] = None
    submarket: Optional[str] = None
    sale_date: Optional[date] = None
    sale_price: Optional[float] = None
    price_per_unit: Optional[float] = None
    price_per_sf: Optional[float] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    year_built: Optional[int] = None
    year_renovated: Optional[int] = None
    noi: Optional[float] = None
    cap_rate: Optional[float] = None
    occupancy: Optional[float] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None
    broker_id: Optional[UUID] = None
    data_source: Optional[str] = None
    notes: Optional[str] = None
    confidence: Optional[int] = 3
    verified: Optional[int] = 0
    verified_date: Optional[date] = None


class CompUpdate(BaseModel):
    property_name: Optional[str] = None
    property_address: Optional[str] = None
    property_type: Optional[str] = None
    market: Optional[str] = None
    submarket: Optional[str] = None
    sale_date: Optional[date] = None
    sale_price: Optional[float] = None
    price_per_unit: Optional[float] = None
    price_per_sf: Optional[float] = None
    units: Optional[int] = None
    square_feet: Optional[int] = None
    year_built: Optional[int] = None
    year_renovated: Optional[int] = None
    noi: Optional[float] = None
    cap_rate: Optional[float] = None
    occupancy: Optional[float] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None
    broker_id: Optional[UUID] = None
    data_source: Optional[str] = None
    notes: Optional[str] = None
    confidence: Optional[int] = None
    verified: Optional[int] = None
    verified_date: Optional[date] = None


# ===== HTML UI Endpoints =====

@router.get("/", response_class=HTMLResponse)
async def crm_home(request: Request, db: Session = Depends(get_db)):
    """CRM home page with overview."""
    # Get summary statistics
    total_deals = db.query(Deal).count()
    active_deals = db.query(Deal).filter(Deal.status == DealStatus.ACTIVE).count()
    total_brokers = db.query(Broker).filter(Broker.status == BrokerStatus.ACTIVE).count()
    total_comps = db.query(Comp).count()

    # Get deals by stage
    deals_by_stage = {}
    for stage in DealStage:
        count = db.query(Deal).filter(Deal.stage == stage, Deal.status == DealStatus.ACTIVE).count()
        deals_by_stage[stage.value] = count

    context = {
        "request": request,
        "total_deals": total_deals,
        "active_deals": active_deals,
        "total_brokers": total_brokers,
        "total_comps": total_comps,
        "deals_by_stage": deals_by_stage,
    }
    return templates.TemplateResponse("crm/home.html", context)


@router.get("/deals", response_class=HTMLResponse)
async def deals_list(
    request: Request,
    stage: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Deal pipeline list view."""
    query = db.query(Deal).order_by(desc(Deal.created_at))

    if stage:
        query = query.filter(Deal.stage == stage)
    if status:
        query = query.filter(Deal.status == status)

    deals = query.all()

    # Get all brokers for dropdowns
    brokers = db.query(Broker).filter(Broker.status == BrokerStatus.ACTIVE).order_by(Broker.last_name).all()

    context = {
        "request": request,
        "deals": deals,
        "brokers": brokers,
        "stages": [s.value for s in DealStage],
        "statuses": [s.value for s in DealStatus],
        "current_stage": stage,
        "current_status": status,
    }
    return templates.TemplateResponse("crm/deals.html", context)


@router.get("/brokers", response_class=HTMLResponse)
async def brokers_list(request: Request, db: Session = Depends(get_db)):
    """Broker/Agent database list view."""
    brokers = db.query(Broker).filter(Broker.status == BrokerStatus.ACTIVE).order_by(Broker.last_name).all()

    context = {
        "request": request,
        "brokers": brokers,
    }
    return templates.TemplateResponse("crm/brokers.html", context)


@router.get("/comps", response_class=HTMLResponse)
async def comps_list(
    request: Request,
    property_type: Optional[str] = None,
    market: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Comps database list view."""
    query = db.query(Comp).order_by(desc(Comp.sale_date))

    if property_type:
        query = query.filter(Comp.property_type == property_type)
    if market:
        query = query.filter(Comp.market == market)

    comps = query.all()

    # Get unique property types and markets for filters
    property_types = db.query(Comp.property_type).distinct().filter(Comp.property_type.isnot(None)).all()
    property_types = sorted([pt[0] for pt in property_types])

    markets = db.query(Comp.market).distinct().filter(Comp.market.isnot(None)).all()
    markets = sorted([m[0] for m in markets])

    # Get all brokers for dropdowns
    brokers = db.query(Broker).filter(Broker.status == BrokerStatus.ACTIVE).order_by(Broker.last_name).all()

    context = {
        "request": request,
        "comps": comps,
        "brokers": brokers,
        "property_types": property_types,
        "markets": markets,
        "current_property_type": property_type,
        "current_market": market,
    }
    return templates.TemplateResponse("crm/comps.html", context)


# ===== API Endpoints - Deals =====

@router.get("/api/deals")
async def get_deals(
    stage: Optional[DealStage] = None,
    status: Optional[DealStatus] = None,
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all deals with optional filters."""
    current_user, company = user_company

    query = db.query(Deal)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Deal.company_id == company.id)

    if stage:
        query = query.filter(Deal.stage == stage)
    if status:
        query = query.filter(Deal.status == status)

    total = query.count()
    deals = query.order_by(desc(Deal.created_at)).offset(skip).limit(limit).all()

    return {
        "total": total,
        "deals": [deal.to_dict() for deal in deals]
    }


@router.post("/api/deals")
async def create_deal(
    deal: DealCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new deal."""
    current_user, company = user_company

    db_deal = Deal(
        **deal.dict(),
        company_id=company.id if company else None
    )
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return {"success": True, "deal": db_deal.to_dict()}


@router.get("/api/deals/{deal_id}")
async def get_deal(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get a specific deal by ID."""
    current_user, company = user_company

    filters = [Deal.id == deal_id]

    if company:
        filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal.to_dict()


@router.put("/api/deals/{deal_id}")
async def update_deal(
    deal_id: UUID,
    deal: DealUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update a deal."""
    current_user, company = user_company

    filters = [Deal.id == deal_id]

    if company:
        filters.append(Deal.company_id == company.id)

    db_deal = db.query(Deal).filter(*filters).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    update_data = deal.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_deal, field, value)

    db.commit()
    db.refresh(db_deal)
    return {"success": True, "deal": db_deal.to_dict()}


@router.delete("/api/deals/{deal_id}")
async def delete_deal(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete a deal."""
    current_user, company = user_company

    filters = [Deal.id == deal_id]

    if company:
        filters.append(Deal.company_id == company.id)

    db_deal = db.query(Deal).filter(*filters).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    db.delete(db_deal)
    db.commit()
    return {"success": True, "message": "Deal deleted"}


# ===== API Endpoints - Brokers =====

@router.get("/api/brokers")
async def get_brokers(
    status: Optional[BrokerStatus] = None,
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all brokers with optional filters."""
    current_user, company = user_company

    query = db.query(Broker)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Broker.company_id == company.id)

    if status:
        query = query.filter(Broker.status == status)

    total = query.count()
    brokers = query.order_by(Broker.last_name).offset(skip).limit(limit).all()

    return {
        "total": total,
        "brokers": [broker.to_dict() for broker in brokers]
    }


@router.post("/api/brokers")
async def create_broker(
    broker: BrokerCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new broker."""
    current_user, company = user_company

    db_broker = Broker(
        **broker.dict(),
        company_id=company.id if company else None
    )
    db.add(db_broker)
    db.commit()
    db.refresh(db_broker)
    return {"success": True, "broker": db_broker.to_dict()}


@router.get("/api/brokers/{broker_id}")
async def get_broker(
    broker_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get a specific broker by ID."""
    current_user, company = user_company

    filters = [Broker.id == broker_id]

    if company:
        filters.append(Broker.company_id == company.id)

    broker = db.query(Broker).filter(*filters).first()
    if not broker:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker.to_dict()


@router.put("/api/brokers/{broker_id}")
async def update_broker(
    broker_id: UUID,
    broker: BrokerUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update a broker."""
    current_user, company = user_company

    filters = [Broker.id == broker_id]

    if company:
        filters.append(Broker.company_id == company.id)

    db_broker = db.query(Broker).filter(*filters).first()
    if not db_broker:
        raise HTTPException(status_code=404, detail="Broker not found")

    update_data = broker.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_broker, field, value)

    db.commit()
    db.refresh(db_broker)
    return {"success": True, "broker": db_broker.to_dict()}


@router.delete("/api/brokers/{broker_id}")
async def delete_broker(
    broker_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete a broker."""
    current_user, company = user_company

    filters = [Broker.id == broker_id]

    if company:
        filters.append(Broker.company_id == company.id)

    db_broker = db.query(Broker).filter(*filters).first()
    if not db_broker:
        raise HTTPException(status_code=404, detail="Broker not found")

    db.delete(db_broker)
    db.commit()
    return {"success": True, "message": "Broker deleted"}


@router.post("/api/brokers/{broker_id}/update-stats")
async def update_broker_stats(
    broker_id: UUID,
    total_deals: Optional[int] = None,
    closed_deals: Optional[int] = None,
    total_volume: Optional[float] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update broker performance statistics."""
    current_user, company = user_company

    filters = [Broker.id == broker_id]

    if company:
        filters.append(Broker.company_id == company.id)

    db_broker = db.query(Broker).filter(*filters).first()
    if not db_broker:
        raise HTTPException(status_code=404, detail="Broker not found")

    if total_deals is not None:
        db_broker.total_deals = total_deals
    if closed_deals is not None:
        db_broker.closed_deals = closed_deals
    if total_volume is not None:
        db_broker.total_volume = total_volume

    db.commit()
    db.refresh(db_broker)
    return {"success": True, "broker": db_broker.to_dict()}


# ===== API Endpoints - Comps =====

@router.get("/api/comps")
async def get_comps(
    property_type: Optional[str] = None,
    market: Optional[str] = None,
    min_cap_rate: Optional[float] = None,
    max_cap_rate: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all comps with optional filters."""
    current_user, company = user_company

    query = db.query(Comp)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Comp.company_id == company.id)

    if property_type:
        query = query.filter(Comp.property_type == property_type)
    if market:
        query = query.filter(Comp.market == market)
    if min_cap_rate is not None:
        query = query.filter(Comp.cap_rate >= min_cap_rate)
    if max_cap_rate is not None:
        query = query.filter(Comp.cap_rate <= max_cap_rate)

    total = query.count()
    comps = query.order_by(desc(Comp.sale_date)).offset(skip).limit(limit).all()

    return {
        "total": total,
        "comps": [comp.to_dict() for comp in comps]
    }


@router.post("/api/comps")
async def create_comp(
    comp: CompCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new comp."""
    current_user, company = user_company

    db_comp = Comp(
        **comp.dict(),
        company_id=company.id if company else None
    )
    db.add(db_comp)
    db.commit()
    db.refresh(db_comp)
    return {"success": True, "comp": db_comp.to_dict()}


@router.get("/api/comps/{comp_id}")
async def get_comp(
    comp_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get a specific comp by ID."""
    current_user, company = user_company

    filters = [Comp.id == comp_id]

    if company:
        filters.append(Comp.company_id == company.id)

    comp = db.query(Comp).filter(*filters).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comp not found")
    return comp.to_dict()


@router.put("/api/comps/{comp_id}")
async def update_comp(
    comp_id: UUID,
    comp: CompUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update a comp."""
    current_user, company = user_company

    filters = [Comp.id == comp_id]

    if company:
        filters.append(Comp.company_id == company.id)

    db_comp = db.query(Comp).filter(*filters).first()
    if not db_comp:
        raise HTTPException(status_code=404, detail="Comp not found")

    update_data = comp.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comp, field, value)

    db.commit()
    db.refresh(db_comp)
    return {"success": True, "comp": db_comp.to_dict()}


@router.delete("/api/comps/{comp_id}")
async def delete_comp(
    comp_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete a comp."""
    current_user, company = user_company

    filters = [Comp.id == comp_id]

    if company:
        filters.append(Comp.company_id == company.id)

    db_comp = db.query(Comp).filter(*filters).first()
    if not db_comp:
        raise HTTPException(status_code=404, detail="Comp not found")

    db.delete(db_comp)
    db.commit()
    return {"success": True, "message": "Comp deleted"}


@router.get("/api/comps/search")
async def search_comps(
    q: str = Query(..., min_length=1),
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Search comps by property name, address, or market."""
    current_user, company = user_company

    query = db.query(Comp).filter(
        or_(
            Comp.property_name.ilike(f"%{q}%"),
            Comp.property_address.ilike(f"%{q}%"),
            Comp.market.ilike(f"%{q}%")
        )
    )

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Comp.company_id == company.id)

    comps = query.order_by(desc(Comp.sale_date)).limit(50).all()

    return {
        "total": len(comps),
        "comps": [comp.to_dict() for comp in comps]
    }


# ===== Deal Tasks Endpoints =====

@router.get("/api/deals/{deal_id}/tasks")
async def get_deal_tasks(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all tasks for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    tasks = db.query(DealTask).filter(DealTask.deal_id == deal_id).order_by(DealTask.due_date).all()
    return {
        "total": len(tasks),
        "tasks": [task.to_dict() for task in tasks]
    }


@router.post("/api/deals/{deal_id}/tasks")
async def create_deal_task(
    deal_id: UUID,
    task_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new task for a deal."""
    current_user, company = user_company

    # Verify deal exists and ownership
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    task = DealTask(deal_id=deal_id, **task_data)
    db.add(task)

    # Log activity
    activity = DealActivity(
        deal_id=deal_id,
        activity_type=ActivityType.TASK_CREATED,
        title=f"Task created: {task.title}",
        description=f"New task created: {task.title}"
    )
    db.add(activity)

    db.commit()
    db.refresh(task)
    return {"success": True, "task": task.to_dict()}


@router.put("/api/tasks/{task_id}")
async def update_task(
    task_id: UUID,
    task_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update a task."""
    current_user, company = user_company

    task = db.query(DealTask).filter(DealTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify parent deal ownership
    deal_filters = [Deal.id == task.deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status

    for field, value in task_data.items():
        setattr(task, field, value)

    # If task completed, log activity
    if old_status != TaskStatus.COMPLETED and task.status == TaskStatus.COMPLETED:
        task.completed_date = date.today()
        activity = DealActivity(
            deal_id=task.deal_id,
            activity_type=ActivityType.TASK_COMPLETED,
            title=f"Task completed: {task.title}",
            description=f"Task completed: {task.title}"
        )
        db.add(activity)

    db.commit()
    db.refresh(task)
    return {"success": True, "task": task.to_dict()}


@router.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete a task."""
    current_user, company = user_company

    task = db.query(DealTask).filter(DealTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify parent deal ownership
    deal_filters = [Deal.id == task.deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"success": True, "message": "Task deleted"}


# ===== Deal Documents Endpoints =====

@router.get("/api/deals/{deal_id}/documents")
async def get_deal_documents(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all documents for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    documents = db.query(DealDocument).filter(DealDocument.deal_id == deal_id).order_by(DealDocument.due_date).all()
    return {
        "total": len(documents),
        "documents": [doc.to_dict() for doc in documents]
    }


@router.post("/api/deals/{deal_id}/documents")
async def create_deal_document(
    deal_id: UUID,
    doc_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new document for a deal."""
    current_user, company = user_company

    # Verify deal exists and ownership
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    document = DealDocument(deal_id=deal_id, **doc_data)
    db.add(document)

    # Log activity
    activity = DealActivity(
        deal_id=deal_id,
        activity_type=ActivityType.DOCUMENT_UPLOADED,
        title=f"Document added: {document.document_name}",
        description=f"Document checklist item added: {document.document_name}"
    )
    db.add(activity)

    db.commit()
    db.refresh(document)
    return {"success": True, "document": document.to_dict()}


@router.put("/api/documents/{document_id}")
async def update_document(
    document_id: UUID,
    doc_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update a document."""
    current_user, company = user_company

    document = db.query(DealDocument).filter(DealDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Verify parent deal ownership
    deal_filters = [Deal.id == document.deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Document not found")

    old_status = document.status

    for field, value in doc_data.items():
        setattr(document, field, value)

    # If document approved, log activity
    if old_status != DocumentStatus.APPROVED and document.status == DocumentStatus.APPROVED:
        document.approved_date = date.today()
        activity = DealActivity(
            deal_id=document.deal_id,
            activity_type=ActivityType.DOCUMENT_APPROVED,
            title=f"Document approved: {document.document_name}",
            description=f"Document approved: {document.document_name}"
        )
        db.add(activity)

    db.commit()
    db.refresh(document)
    return {"success": True, "document": document.to_dict()}


# ===== Deal Activity Log Endpoints =====

@router.get("/api/deals/{deal_id}/activity")
async def get_deal_activity(
    deal_id: UUID,
    limit: int = 50,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get activity log for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    activities = db.query(DealActivity).filter(
        DealActivity.deal_id == deal_id
    ).order_by(desc(DealActivity.created_at)).limit(limit).all()

    return {
        "total": len(activities),
        "activities": [activity.to_dict() for activity in activities]
    }


# ===== Deal Scoring Endpoints =====

@router.get("/api/deals/{deal_id}/score")
async def get_deal_score(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get the latest score for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    score = deal_scoring_service.get_latest_score(db, deal_id)
    if not score:
        return {"success": False, "message": "No score found for this deal"}

    return {"success": True, "score": score.to_dict()}


@router.post("/api/deals/{deal_id}/score")
async def calculate_deal_score(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Calculate/recalculate score for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Trigger async task
    score_single_deal.delay(str(deal_id), notify_on_change=True)

    return {"success": True, "message": "Scoring task queued"}


@router.get("/api/deals/{deal_id}/score/history")
async def get_deal_score_history(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get score history for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    scores = db.query(DealScore).filter(
        DealScore.deal_id == deal_id
    ).order_by(desc(DealScore.created_at)).limit(20).all()

    return {
        "total": len(scores),
        "scores": [score.to_dict() for score in scores]
    }


# ===== Deal Automation Endpoints =====

@router.post("/api/deals/{deal_id}/transition")
async def transition_deal_stage(
    deal_id: UUID,
    target_stage: DealStage,
    force: bool = False,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Attempt to transition a deal to a new stage."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    success, message = deal_automation_service.attempt_stage_transition(
        db=db,
        deal=deal,
        target_stage=target_stage,
        force=force
    )

    return {
        "success": success,
        "message": message,
        "current_stage": deal.stage.value
    }


@router.get("/api/deals/{deal_id}/transition/check")
async def check_transition_eligibility(
    deal_id: UUID,
    target_stage: DealStage,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Check if a deal can transition to a new stage."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    eligible, reasons = deal_automation_service.check_stage_transition_eligibility(
        db=db,
        deal=deal,
        target_stage=target_stage
    )

    return {
        "eligible": eligible,
        "blocking_reasons": reasons
    }


@router.post("/api/deals/{deal_id}/checklist/create")
async def create_due_diligence_checklist(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Auto-create due diligence checklist for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    items_created = deal_automation_service.auto_create_due_diligence_checklist(db, deal)

    return {
        "success": True,
        "items_created": items_created,
        "message": f"Created {items_created} due diligence items"
    }


# ===== Comp Pulling Endpoints =====

@router.post("/api/deals/{deal_id}/comps/pull")
async def pull_comps_for_deal(
    deal_id: UUID,
    radius_miles: float = 5.0,
    max_results: int = 20,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Auto-pull comparable properties for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Trigger async task
    auto_pull_comps.delay(str(deal_id))

    return {
        "success": True,
        "message": "Comp pulling task queued"
    }


# ===== Automation Rules Endpoints =====

@router.get("/api/automation/rules")
async def get_automation_rules(
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all automation rules."""
    current_user, company = user_company

    query = db.query(DealStageRule)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(DealStageRule.company_id == company.id)

    rules = query.order_by(DealStageRule.priority.desc()).all()
    return {
        "total": len(rules),
        "rules": [rule.to_dict() for rule in rules]
    }


@router.post("/api/automation/rules")
async def create_automation_rule(
    rule_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new automation rule."""
    current_user, company = user_company

    rule = DealStageRule(
        **rule_data,
        company_id=company.id if company else None
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}


@router.put("/api/automation/rules/{rule_id}")
async def update_automation_rule(
    rule_id: UUID,
    rule_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update an automation rule."""
    current_user, company = user_company

    filters = [DealStageRule.id == rule_id]

    if company:
        filters.append(DealStageRule.company_id == company.id)

    rule = db.query(DealStageRule).filter(*filters).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for field, value in rule_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}


@router.delete("/api/automation/rules/{rule_id}")
async def delete_automation_rule(
    rule_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete an automation rule."""
    current_user, company = user_company

    filters = [DealStageRule.id == rule_id]

    if company:
        filters.append(DealStageRule.company_id == company.id)

    rule = db.query(DealStageRule).filter(*filters).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"success": True, "message": "Rule deleted"}


# ===== Email Template Endpoints =====

@router.get("/api/automation/email-templates")
async def get_email_templates(
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all email templates."""
    current_user, company = user_company

    query = db.query(EmailTemplate)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(EmailTemplate.company_id == company.id)

    templates = query.all()
    return {
        "total": len(templates),
        "templates": [template.to_dict() for template in templates]
    }


@router.post("/api/automation/email-templates")
async def create_email_template(
    template_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new email template."""
    current_user, company = user_company

    template = EmailTemplate(
        **template_data,
        company_id=company.id if company else None
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return {"success": True, "template": template.to_dict()}


# ===== Due Diligence Integration Endpoints =====

@router.post("/api/deals/{deal_id}/due-diligence/create")
async def create_dd_model(
    deal_id: UUID,
    user_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a due diligence model for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    dd_model = due_diligence_integration.create_dd_model_for_deal(db, deal, user_id)

    return {
        "success": True,
        "dd_model_id": str(dd_model.id),
        "message": "Due diligence model created"
    }


@router.get("/api/deals/{deal_id}/due-diligence")
async def get_dd_model(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get the due diligence model for a deal."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    dd_model = due_diligence_integration.get_dd_model_for_deal(db, deal_id)

    if not dd_model:
        return {
            "success": False,
            "message": "No due diligence model found for this deal"
        }

    return {
        "success": True,
        "dd_model": dd_model.to_dict()
    }


@router.post("/api/deals/{deal_id}/due-diligence/sync")
async def sync_dd_progress(
    deal_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Sync due diligence progress from tasks and documents."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    dd_model = due_diligence_integration.get_dd_model_for_deal(db, deal_id)
    if not dd_model:
        raise HTTPException(status_code=404, detail="No DD model found for this deal")

    # Update progress from tasks
    dd_model = due_diligence_integration.update_dd_progress_from_tasks(db, deal, dd_model)

    # Sync documents
    dd_model = due_diligence_integration.sync_documents_to_dd_model(db, deal, dd_model)

    # Calculate risk rating
    risk_rating = due_diligence_integration.calculate_risk_rating(db, dd_model)

    # Generate recommendation
    recommendation = due_diligence_integration.generate_recommendation(db, deal, dd_model)

    return {
        "success": True,
        "completion": dd_model.output_data.get('completion_percentage'),
        "risk_rating": risk_rating,
        "recommendation": recommendation,
    }


@router.post("/api/deals/{deal_id}/due-diligence/finding")
async def add_dd_finding(
    deal_id: UUID,
    category: str,
    finding: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Add a finding to due diligence model."""
    current_user, company = user_company

    # Verify deal ownership first
    deal_filters = [Deal.id == deal_id]
    if company:
        deal_filters.append(Deal.company_id == company.id)

    deal = db.query(Deal).filter(*deal_filters).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    dd_model = due_diligence_integration.get_dd_model_for_deal(db, deal_id)
    if not dd_model:
        raise HTTPException(status_code=404, detail="No DD model found for this deal")

    dd_model = due_diligence_integration.add_finding_to_dd_model(
        db, dd_model, category, finding
    )

    return {
        "success": True,
        "message": "Finding added to due diligence model"
    }
