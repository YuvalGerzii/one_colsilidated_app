"""
Project Tracking API Endpoints

Comprehensive API for personal and professional project/task management.
Supports projects, tasks, subtasks, and progress tracking.
"""

from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from decimal import Decimal

from app.core.database import get_db
from app.models.project_tracking import (
    Project,
    Task,
    Milestone,
    ProjectUpdate,
    ProjectType,
    ProjectStatus,
    TaskStatus,
    TaskPriority,
)


router = APIRouter()


# ================================
# PYDANTIC SCHEMAS
# ================================

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    project_number: Optional[str] = None
    project_type: ProjectType
    status: ProjectStatus = ProjectStatus.PLANNING
    description: Optional[str] = None
    color: str = "#1976d2"
    tags: List[str] = []
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    total_budget: Optional[Decimal] = None
    owner: Optional[str] = None
    collaborators: List[str] = []
    notes: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    project_number: Optional[str] = None
    project_type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    description: Optional[str] = None
    color: Optional[str] = None
    tags: Optional[List[str]] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    total_budget: Optional[Decimal] = None
    spent_to_date: Optional[Decimal] = None
    owner: Optional[str] = None
    collaborators: Optional[List[str]] = None
    completion_percentage: Optional[Decimal] = None
    priority: Optional[int] = None
    notes: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: str
    status: ProjectStatus
    completed_date: Optional[date] = None
    spent_to_date: Decimal = Decimal("0")
    completion_percentage: Decimal = Decimal("0")
    priority: int = 0
    created_at: datetime
    updated_at: datetime

    # Computed fields
    remaining_budget: Optional[float] = None
    budget_utilization: float = 0
    days_remaining: Optional[int] = None
    is_overdue: bool = False
    task_count: int = 0
    completed_task_count: int = 0

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: TaskPriority = TaskPriority.MEDIUM
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    assigned_to: Optional[str] = None
    estimated_hours: Optional[Decimal] = None
    estimated_cost: Optional[Decimal] = None
    depends_on_task_id: Optional[str] = None
    notes: Optional[str] = None


class TaskCreate(TaskBase):
    project_id: str
    parent_task_id: Optional[str] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    assigned_to: Optional[str] = None
    estimated_hours: Optional[Decimal] = None
    actual_hours: Optional[Decimal] = None
    estimated_cost: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    depends_on_task_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    completion_percentage: Optional[Decimal] = None
    order: Optional[int] = None
    notes: Optional[str] = None


class TaskResponse(TaskBase):
    id: str
    project_id: str
    parent_task_id: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    completed_date: Optional[date] = None
    actual_hours: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    completion_percentage: Decimal = Decimal("0")
    order: int = 0
    created_at: datetime
    updated_at: datetime

    # Computed fields
    is_overdue: bool = False
    days_until_due: Optional[int] = None
    has_subtasks: bool = False
    subtask_count: int = 0
    completed_subtask_count: int = 0

    class Config:
        from_attributes = True


# Dashboard Summary Schema
class DashboardSummary(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    on_hold_projects: int
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    overdue_tasks: int
    high_priority_tasks: int
    tasks_due_this_week: int
    recent_projects: List[ProjectResponse]
    upcoming_tasks: List[TaskResponse]


# ================================
# PROJECT ENDPOINTS
# ================================

@router.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    try:
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create project: {str(e)}")


@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(
    status: Optional[ProjectStatus] = None,
    project_type: Optional[ProjectType] = None,
    tags: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all projects with optional filtering"""
    query = db.query(Project).filter(Project.deleted_at.is_(None))

    if status:
        query = query.filter(Project.status == status)
    if project_type:
        query = query.filter(Project.project_type == project_type)
    if tags:
        # Filter by tags (projects that have any of the specified tags)
        for tag in tags:
            query = query.filter(Project.tags.contains([tag]))

    projects = query.order_by(Project.priority.desc(), Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get a specific project by ID"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.deleted_at.is_(None)
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.deleted_at.is_(None)
    ).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    # Auto-set completed_date if status changed to completed
    if project_update.status == ProjectStatus.COMPLETED and not db_project.completed_date:
        db_project.completed_date = date.today()

    try:
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update project: {str(e)}")


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str, hard_delete: bool = False, db: Session = Depends(get_db)):
    """Delete a project (soft delete by default)"""
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if hard_delete:
        db.delete(db_project)
    else:
        db_project.deleted_at = datetime.utcnow()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete project: {str(e)}")


# ================================
# TASK ENDPOINTS
# ================================

@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    # Verify project exists
    project = db.query(Project).filter(
        Project.id == task.project_id,
        Project.deleted_at.is_(None)
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verify parent task exists if specified
    if task.parent_task_id:
        parent_task = db.query(Task).filter(
            Task.id == task.parent_task_id,
            Task.deleted_at.is_(None)
        ).first()
        if not parent_task:
            raise HTTPException(status_code=404, detail="Parent task not found")

    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    project_id: Optional[str] = None,
    parent_task_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assigned_to: Optional[str] = None,
    overdue_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering"""
    query = db.query(Task).filter(Task.deleted_at.is_(None))

    if project_id:
        query = query.filter(Task.project_id == project_id)
    if parent_task_id:
        query = query.filter(Task.parent_task_id == parent_task_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    tasks = query.order_by(Task.order.asc(), Task.created_at.desc()).offset(skip).limit(limit).all()

    # Filter overdue tasks if requested
    if overdue_only:
        tasks = [t for t in tasks if t.is_overdue]

    return tasks


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: str, db: Session = Depends(get_db)):
    """Get all tasks for a specific project"""
    # Verify project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.deleted_at.is_(None)
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = db.query(Task).filter(
        Task.project_id == project_id,
        Task.deleted_at.is_(None)
    ).order_by(Task.order.asc(), Task.created_at.desc()).all()

    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.deleted_at.is_(None)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/tasks/{task_id}/subtasks", response_model=List[TaskResponse])
def get_subtasks(task_id: str, db: Session = Depends(get_db)):
    """Get all subtasks for a task"""
    # Verify parent task exists
    parent_task = db.query(Task).filter(
        Task.id == task_id,
        Task.deleted_at.is_(None)
    ).first()

    if not parent_task:
        raise HTTPException(status_code=404, detail="Task not found")

    subtasks = db.query(Task).filter(
        Task.parent_task_id == task_id,
        Task.deleted_at.is_(None)
    ).order_by(Task.order.asc()).all()

    return subtasks


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.deleted_at.is_(None)
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Auto-set completed_date if status changed to completed
    if task_update.status == TaskStatus.COMPLETED and not db_task.completed_date:
        db_task.completed_date = date.today()
        db_task.completion_percentage = Decimal("100")

    try:
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update task: {str(e)}")


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, hard_delete: bool = False, db: Session = Depends(get_db)):
    """Delete a task (soft delete by default)"""
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if hard_delete:
        db.delete(db_task)
    else:
        db_task.deleted_at = datetime.utcnow()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete task: {str(e)}")


# ================================
# DASHBOARD & SUMMARY ENDPOINTS
# ================================

@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary with key metrics

    FALLBACK: Returns empty data if tables don't exist (database not migrated yet)
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        # Project stats
        all_projects = db.query(Project).filter(Project.deleted_at.is_(None)).all()
        total_projects = len(all_projects)
        active_projects = len([p for p in all_projects if p.status == ProjectStatus.IN_PROGRESS])
        completed_projects = len([p for p in all_projects if p.status == ProjectStatus.COMPLETED])
        on_hold_projects = len([p for p in all_projects if p.status == ProjectStatus.ON_HOLD])

        # Task stats
        all_tasks = db.query(Task).filter(Task.deleted_at.is_(None)).all()
        total_tasks = len(all_tasks)
        pending_tasks = len([t for t in all_tasks if t.status == TaskStatus.NOT_STARTED])
        in_progress_tasks = len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS])
        completed_tasks = len([t for t in all_tasks if t.status == TaskStatus.COMPLETED])
        overdue_tasks = len([t for t in all_tasks if t.is_overdue])
        high_priority_tasks = len([t for t in all_tasks if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL] and t.status != TaskStatus.COMPLETED])

        # Tasks due this week
        from datetime import timedelta
        week_from_now = date.today() + timedelta(days=7)
        tasks_due_this_week = len([
            t for t in all_tasks
            if t.due_date and date.today() <= t.due_date <= week_from_now and t.status != TaskStatus.COMPLETED
        ])

        # Recent projects (last 5)
        recent_projects = db.query(Project).filter(
            Project.deleted_at.is_(None)
        ).order_by(Project.created_at.desc()).limit(5).all()

        # Upcoming tasks (next 10 tasks by due date)
        upcoming_tasks = db.query(Task).filter(
            Task.deleted_at.is_(None),
            Task.status != TaskStatus.COMPLETED,
            Task.due_date.isnot(None)
        ).order_by(Task.due_date.asc()).limit(10).all()

        return DashboardSummary(
            total_projects=total_projects,
            active_projects=active_projects,
            completed_projects=completed_projects,
            on_hold_projects=on_hold_projects,
            total_tasks=total_tasks,
            pending_tasks=pending_tasks,
            in_progress_tasks=in_progress_tasks,
            completed_tasks=completed_tasks,
            overdue_tasks=overdue_tasks,
            high_priority_tasks=high_priority_tasks,
            tasks_due_this_week=tasks_due_this_week,
            recent_projects=recent_projects,
            upcoming_tasks=upcoming_tasks
        )
    except Exception as e:
        # FALLBACK: If tables don't exist or any database error, return empty data
        logger.warning(f"Project tracking tables not available (database not migrated): {str(e)}")
        logger.info("Returning empty project tracking data - run migrations to enable this feature")

        return DashboardSummary(
            total_projects=0,
            active_projects=0,
            completed_projects=0,
            on_hold_projects=0,
            total_tasks=0,
            pending_tasks=0,
            in_progress_tasks=0,
            completed_tasks=0,
            overdue_tasks=0,
            high_priority_tasks=0,
            tasks_due_this_week=0,
            recent_projects=[],
            upcoming_tasks=[]
        )


@router.post("/tasks/bulk-update-order", status_code=200)
def bulk_update_task_order(
    task_orders: List[dict],
    db: Session = Depends(get_db)
):
    """
    Bulk update task order (for drag-and-drop reordering)

    Expects: [{"id": "task-uuid", "order": 0}, ...]
    """
    try:
        for item in task_orders:
            task = db.query(Task).filter(
                Task.id == item["id"],
                Task.deleted_at.is_(None)
            ).first()
            if task:
                task.order = item["order"]

        db.commit()
        return {"message": "Task order updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update task order: {str(e)}")


# Export router
__all__ = ["router"]
