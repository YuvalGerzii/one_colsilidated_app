"""
Project Tracking Models

Models for tracking personal and professional projects, tasks, and progress.
Supports work projects, deals, personal tasks, and more.
"""

import enum
from datetime import date, datetime
from sqlalchemy import Column, String, Text, Integer, Numeric, Date, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as GUID, ARRAY

from app.models.database import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class ProjectType(str, enum.Enum):
    """Project type classification"""
    WORK = "Work"
    PERSONAL = "Personal"
    DEAL = "Deal"
    CLIENT_PROJECT = "Client Project"
    REAL_ESTATE = "Real Estate"
    BUSINESS_DEVELOPMENT = "Business Development"
    RESEARCH = "Research"
    LEARNING = "Learning"
    OTHER = "Other"


class ProjectStatus(str, enum.Enum):
    """Project status"""
    PLANNING = "Planning"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class TaskStatus(str, enum.Enum):
    """Task status"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"
    CANCELLED = "Cancelled"


class TaskPriority(str, enum.Enum):
    """Task priority"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Project(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Project Model

    Tracks personal and professional projects of all types.
    Supports work projects, deals, personal initiatives, and more.
    """
    __tablename__ = "projects"

    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    project_number = Column(String(50), unique=True, index=True, nullable=True)
    project_type = Column(SQLEnum(ProjectType), nullable=False)
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING)
    description = Column(Text)
    color = Column(String(7), default="#1976d2")  # Hex color for visual organization
    tags = Column(ARRAY(String), default=[])  # Tags for organization and filtering

    # Timeline
    start_date = Column(Date)
    due_date = Column(Date)
    completed_date = Column(Date)

    # Financial (optional)
    total_budget = Column(Numeric(20, 2))
    spent_to_date = Column(Numeric(20, 2), default=0)

    # Team/Assignment (optional)
    owner = Column(String(200))  # Project owner/lead
    collaborators = Column(ARRAY(String), default=[])  # Team members

    # Metrics
    completion_percentage = Column(Numeric(5, 2), default=0)  # 0-100%
    priority = Column(Integer, default=0)  # For manual sorting/prioritization

    # Notes
    notes = Column(Text)

    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")

    @property
    def remaining_budget(self):
        """Calculate remaining budget"""
        if self.total_budget:
            return float(self.total_budget) - float(self.spent_to_date or 0)
        return None

    @property
    def budget_utilization(self):
        """Calculate budget utilization percentage"""
        if self.total_budget and self.total_budget > 0:
            return (float(self.spent_to_date or 0) / float(self.total_budget)) * 100
        return 0

    @property
    def days_remaining(self):
        """Calculate days remaining until due date"""
        if self.due_date:
            delta = self.due_date - date.today()
            return delta.days
        return None

    @property
    def is_overdue(self):
        """Check if project is overdue"""
        if self.due_date and self.status not in [ProjectStatus.COMPLETED, ProjectStatus.CANCELLED]:
            return date.today() > self.due_date
        return False

    @property
    def task_count(self):
        """Get total number of tasks"""
        return len(self.tasks) if self.tasks else 0

    @property
    def completed_task_count(self):
        """Get number of completed tasks"""
        if not self.tasks:
            return 0
        return len([t for t in self.tasks if t.status == TaskStatus.COMPLETED])


class Task(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Task Model

    Individual tasks/work items within a project.
    Supports subtasks, dependencies, and flexible organization.
    """
    __tablename__ = "tasks"

    # Basic Information
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    parent_task_id = Column(GUID, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)  # For subtasks
    name = Column(String(200), nullable=False)
    description = Column(Text)
    tags = Column(ARRAY(String), default=[])  # Tags for organization

    # Status & Priority
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)

    # Timeline
    start_date = Column(Date)
    due_date = Column(Date)
    completed_date = Column(Date)

    # Assignment
    assigned_to = Column(String(200))
    estimated_hours = Column(Numeric(10, 2))
    actual_hours = Column(Numeric(10, 2))

    # Financial (optional)
    estimated_cost = Column(Numeric(20, 2))
    actual_cost = Column(Numeric(20, 2))

    # Dependencies
    depends_on_task_id = Column(GUID, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)

    # Progress
    completion_percentage = Column(Numeric(5, 2), default=0)  # 0-100%
    order = Column(Integer, default=0)  # For manual ordering within project/parent

    # Notes
    notes = Column(Text)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    parent_task = relationship("Task", remote_side="Task.id", foreign_keys=[parent_task_id], backref="subtasks")
    dependencies = relationship("Task", remote_side="Task.id", foreign_keys=[depends_on_task_id])

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return date.today() > self.due_date
        return False

    @property
    def days_until_due(self):
        """Calculate days until due date"""
        if self.due_date:
            delta = self.due_date - date.today()
            return delta.days
        return None

    @property
    def has_subtasks(self):
        """Check if task has subtasks"""
        return hasattr(self, 'subtasks') and len(self.subtasks) > 0

    @property
    def subtask_count(self):
        """Get number of subtasks"""
        return len(self.subtasks) if hasattr(self, 'subtasks') else 0

    @property
    def completed_subtask_count(self):
        """Get number of completed subtasks"""
        if not hasattr(self, 'subtasks'):
            return 0
        return len([st for st in self.subtasks if st.status == TaskStatus.COMPLETED])


class Milestone(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Project Milestone Model

    Major milestones/checkpoints in a project.
    """
    __tablename__ = "milestones"

    # Basic Information
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Timeline
    target_date = Column(Date, nullable=False)
    actual_date = Column(Date)

    # Status
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Numeric(5, 2), default=0)

    # Financial
    budget_at_milestone = Column(Numeric(20, 2))
    actual_spend_at_milestone = Column(Numeric(20, 2))

    # Notes
    notes = Column(Text)

    # Relationships
    project = relationship("Project", back_populates="milestones")

    @property
    def is_overdue(self):
        """Check if milestone is overdue"""
        if not self.is_completed and self.target_date:
            return date.today() > self.target_date
        return False

    @property
    def days_until_target(self):
        """Calculate days until target date"""
        if self.target_date:
            delta = self.target_date - date.today()
            return delta.days
        return None


class ProjectUpdate(Base, UUIDMixin, TimestampMixin):
    """
    Project Update/Note Model

    Progress updates, notes, and status reports for projects.
    """
    __tablename__ = "project_updates"

    # Basic Information
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    # Metadata
    author = Column(String(200))
    update_date = Column(DateTime, default=datetime.utcnow)

    # Categorization
    update_type = Column(String(50))  # e.g., "Progress Update", "Issue", "Milestone", "Budget"

    # Attachments (file paths/URLs)
    attachments = Column(ARRAY(String), default=[])


# Export all models
__all__ = [
    "Project",
    "ProjectType",
    "ProjectStatus",
    "Task",
    "TaskStatus",
    "TaskPriority",
    "Milestone",
    "ProjectUpdate",
]
