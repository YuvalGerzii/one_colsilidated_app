"""CRM models for deal pipeline, brokers/agents, and comps database."""

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Text, ForeignKey, Enum as SQLEnum, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from datetime import datetime

from app.models.database import BaseModel
# Import Deal from the new multi-type deal model
from app.models.deal import Deal


class DealStage(str, enum.Enum):
    """Deal pipeline stages."""
    RESEARCH = "research"
    LOI = "loi"
    DUE_DILIGENCE = "due_diligence"
    CLOSING = "closing"
    CLOSED = "closed"
    DEAD = "dead"


class DealStatus(str, enum.Enum):
    """Deal status."""
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    DEAD = "dead"
    CLOSED = "closed"


class BrokerStatus(str, enum.Enum):
    """Broker/Agent status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


# NOTE: Deal class is now imported from app.models.deal (see imports at top)
# The old Deal class that was here has been removed to avoid SQLAlchemy model conflicts.
# The new Deal model supports multi-type deals (real estate, acquisitions, shares, commodities, etc.)


class Broker(BaseModel):
    """
    Broker/Agent database for tracking relationships, past deals, and success rates.
    """

    __tablename__ = "brokers"

    # Basic Information
    first_name = Column(String(100), nullable=False, comment="First name")
    last_name = Column(String(100), nullable=False, comment="Last name")
    company = Column(String(255), nullable=True, index=True, comment="Brokerage firm")
    title = Column(String(100), nullable=True, comment="Job title")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this broker belongs to (for multi-tenancy)"
    )

    # Contact Information
    email = Column(String(255), nullable=True, index=True, comment="Email address")
    phone = Column(String(50), nullable=True, comment="Phone number")
    mobile = Column(String(50), nullable=True, comment="Mobile number")
    office_address = Column(String(500), nullable=True, comment="Office address")

    # Specialization
    primary_market = Column(String(100), nullable=True, comment="Primary market/geography")
    specialties = Column(String(500), nullable=True, comment="Comma-separated property types or specialties")

    # Relationship & Performance
    status = Column(
        SQLEnum(BrokerStatus, name="broker_status"),
        nullable=False,
        default=BrokerStatus.ACTIVE,
        index=True,
        comment="Broker status"
    )
    relationship_strength = Column(Integer, nullable=True, default=3, comment="Relationship strength (1-5, 5=strongest)")
    total_deals = Column(Integer, nullable=False, default=0, comment="Total deals worked together")
    closed_deals = Column(Integer, nullable=False, default=0, comment="Number of closed deals")
    total_volume = Column(Float, nullable=False, default=0.0, comment="Total dollar volume of closed deals")

    # Notes
    notes = Column(Text, nullable=True, comment="Notes about broker/relationship")
    last_contact_date = Column(Date, nullable=True, comment="Last contact date")

    # Relationships
    deals = relationship("Deal", back_populates="broker")
    comps = relationship("Comp", back_populates="broker")

    @property
    def full_name(self) -> str:
        """Return full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def success_rate(self) -> float:
        """Calculate success rate (closed deals / total deals)."""
        if self.total_deals == 0:
            return 0.0
        return (self.closed_deals / self.total_deals) * 100

    def __repr__(self):
        return f"<Broker(name='{self.full_name}', company='{self.company}')>"


class Comp(BaseModel):
    """
    Comparable properties database for building historical comps library.
    """

    __tablename__ = "comps"

    # Property Information
    property_name = Column(String(255), nullable=False, index=True, comment="Property name")
    property_address = Column(String(500), nullable=True, comment="Full property address")
    property_type = Column(String(100), nullable=False, index=True, comment="Property type")
    market = Column(String(100), nullable=True, index=True, comment="Market or submarket")
    submarket = Column(String(100), nullable=True, comment="Submarket")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this comp belongs to (for multi-tenancy)"
    )

    # Transaction Details
    sale_date = Column(Date, nullable=True, index=True, comment="Date of sale")
    sale_price = Column(Float, nullable=True, comment="Sale price")
    price_per_unit = Column(Float, nullable=True, comment="Price per unit (if multifamily)")
    price_per_sf = Column(Float, nullable=True, comment="Price per square foot")

    # Property Metrics
    units = Column(Integer, nullable=True, comment="Number of units")
    square_feet = Column(Integer, nullable=True, comment="Total square footage")
    year_built = Column(Integer, nullable=True, comment="Year built")
    year_renovated = Column(Integer, nullable=True, comment="Last renovation year")

    # Financial Metrics
    noi = Column(Float, nullable=True, comment="Net Operating Income")
    cap_rate = Column(Float, nullable=True, index=True, comment="Cap rate at sale (%)")
    occupancy = Column(Float, nullable=True, comment="Occupancy % at sale")

    # Additional Details
    buyer = Column(String(255), nullable=True, comment="Buyer name")
    seller = Column(String(255), nullable=True, comment="Seller name")
    broker_id = Column(UUID(as_uuid=True), ForeignKey("brokers.id", ondelete="SET NULL"), nullable=True)
    broker = relationship("Broker", back_populates="comps")

    # Data Source & Notes
    data_source = Column(String(255), nullable=True, comment="Where comp data came from")
    notes = Column(Text, nullable=True, comment="Additional notes")
    confidence = Column(Integer, nullable=True, default=3, comment="Data confidence (1-5, 5=highest)")

    # Verification
    verified = Column(Integer, nullable=False, default=0, comment="1 if verified, 0 if unverified")
    verified_date = Column(Date, nullable=True, comment="Date verified")

    def __repr__(self):
        return f"<Comp(property_name='{self.property_name}', sale_price={self.sale_price}, cap_rate={self.cap_rate})>"


class TaskStatus(str, enum.Enum):
    """Deal task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DocumentStatus(str, enum.Enum):
    """Document checklist status."""
    NOT_STARTED = "not_started"
    REQUESTED = "requested"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReminderType(str, enum.Enum):
    """Reminder types."""
    EMAIL = "email"
    SLACK = "slack"
    IN_APP = "in_app"
    ALL = "all"


class ActivityType(str, enum.Enum):
    """Deal activity types."""
    STAGE_CHANGE = "stage_change"
    STATUS_CHANGE = "status_change"
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    DOCUMENT_UPLOADED = "document_uploaded"
    DOCUMENT_APPROVED = "document_approved"
    NOTE_ADDED = "note_added"
    REMINDER_SENT = "reminder_sent"
    PRICE_UPDATED = "price_updated"
    COMP_ADDED = "comp_added"
    SCORE_UPDATED = "score_updated"


class DealTask(BaseModel):
    """
    Tasks associated with deals (especially for due diligence).
    """

    __tablename__ = "deal_tasks"

    # Relationships
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    deal = relationship("Deal", backref="tasks")

    # Task Details
    title = Column(String(255), nullable=False, comment="Task title")
    description = Column(Text, nullable=True, comment="Task description")
    task_type = Column(String(100), nullable=True, comment="Task type (e.g., Financial Review, Site Visit)")

    # Status & Priority
    status = Column(
        SQLEnum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.PENDING,
        index=True,
        comment="Task status"
    )
    priority = Column(
        SQLEnum(TaskPriority, name="task_priority"),
        nullable=False,
        default=TaskPriority.MEDIUM,
        comment="Task priority"
    )

    # Assignment
    assigned_to = Column(String(255), nullable=True, comment="Person assigned to task")

    # Dates
    due_date = Column(Date, nullable=True, comment="Task due date")
    completed_date = Column(Date, nullable=True, comment="Date task was completed")

    # Dependencies
    depends_on_task_id = Column(UUID(as_uuid=True), ForeignKey("deal_tasks.id", ondelete="SET NULL"), nullable=True)
    blocks_stage_transition = Column(Boolean, default=False, comment="If true, must complete before stage can advance")

    # Automation
    auto_created = Column(Boolean, default=False, comment="Whether task was auto-created by automation")

    def __repr__(self):
        return f"<DealTask(title='{self.title}', status='{self.status}', deal_id='{self.deal_id}')>"


class DealDocument(BaseModel):
    """
    Document checklist for deal due diligence.
    """

    __tablename__ = "deal_documents"

    # Relationships
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    deal = relationship("Deal", backref="documents")

    # Document Details
    document_name = Column(String(255), nullable=False, comment="Document name")
    document_type = Column(String(100), nullable=True, comment="Document category (e.g., Financial, Legal, Environmental)")
    description = Column(Text, nullable=True, comment="Document description")

    # Status
    status = Column(
        SQLEnum(DocumentStatus, name="document_status"),
        nullable=False,
        default=DocumentStatus.NOT_STARTED,
        index=True,
        comment="Document status"
    )

    # File Information
    file_url = Column(String(500), nullable=True, comment="URL to document file")
    file_size = Column(Integer, nullable=True, comment="File size in bytes")
    uploaded_by = Column(String(255), nullable=True, comment="Person who uploaded")

    # Dates
    due_date = Column(Date, nullable=True, comment="Document due date")
    received_date = Column(Date, nullable=True, comment="Date document was received")
    approved_date = Column(Date, nullable=True, comment="Date document was approved")

    # Review
    reviewed_by = Column(String(255), nullable=True, comment="Person who reviewed")
    review_notes = Column(Text, nullable=True, comment="Review notes")

    # Requirements
    is_required = Column(Boolean, default=True, comment="Whether document is required")
    blocks_stage_transition = Column(Boolean, default=False, comment="If true, must approve before stage can advance")

    def __repr__(self):
        return f"<DealDocument(name='{self.document_name}', status='{self.status}', deal_id='{self.deal_id}')>"


class DealReminder(BaseModel):
    """
    Automated reminders for deals.
    """

    __tablename__ = "deal_reminders"

    # Relationships
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    deal = relationship("Deal", backref="reminders")

    task_id = Column(UUID(as_uuid=True), ForeignKey("deal_tasks.id", ondelete="CASCADE"), nullable=True)

    # Reminder Details
    title = Column(String(255), nullable=False, comment="Reminder title")
    message = Column(Text, nullable=True, comment="Reminder message")

    # Timing
    remind_at = Column(DateTime, nullable=False, index=True, comment="When to send reminder")
    sent_at = Column(DateTime, nullable=True, comment="When reminder was actually sent")

    # Recipients
    recipient_emails = Column(String(500), nullable=True, comment="Comma-separated email addresses")
    recipient_slack_channels = Column(String(500), nullable=True, comment="Comma-separated Slack channels")

    # Configuration
    reminder_type = Column(
        SQLEnum(ReminderType, name="reminder_type"),
        nullable=False,
        default=ReminderType.EMAIL,
        comment="How to send reminder"
    )
    is_sent = Column(Boolean, default=False, index=True, comment="Whether reminder has been sent")

    # Recurrence
    is_recurring = Column(Boolean, default=False, comment="Whether reminder recurs")
    recurrence_days = Column(Integer, nullable=True, comment="Recur every N days")

    def __repr__(self):
        return f"<DealReminder(title='{self.title}', remind_at='{self.remind_at}', deal_id='{self.deal_id}')>"


class DealStageRule(BaseModel):
    """
    Automation rules for automatic stage transitions.
    """

    __tablename__ = "deal_stage_rules"

    # Rule Details
    name = Column(String(255), nullable=False, comment="Rule name")
    description = Column(Text, nullable=True, comment="Rule description")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this rule belongs to (for multi-tenancy)"
    )

    # Stage Configuration
    from_stage = Column(
        SQLEnum(DealStage, name="from_stage"),
        nullable=False,
        index=True,
        comment="Stage this rule applies to"
    )
    to_stage = Column(
        SQLEnum(DealStage, name="to_stage"),
        nullable=False,
        comment="Stage to transition to"
    )

    # Conditions (stored as JSON)
    conditions = Column(JSON, nullable=True, comment="Conditions that must be met (JSON)")
    # Example: {"all_tasks_complete": true, "all_documents_approved": true, "min_score": 70}

    # Actions (stored as JSON)
    actions = Column(JSON, nullable=True, comment="Actions to perform on transition (JSON)")
    # Example: {"send_email": true, "create_tasks": ["task1", "task2"], "notify_slack": true}

    # Configuration
    is_active = Column(Boolean, default=True, index=True, comment="Whether rule is active")
    auto_transition = Column(Boolean, default=False, comment="Automatically transition or just notify")

    # Priority (for when multiple rules match)
    priority = Column(Integer, default=1, comment="Rule priority (higher = runs first)")

    def __repr__(self):
        return f"<DealStageRule(name='{self.name}', {self.from_stage}->{self.to_stage})>"


class EmailTemplate(BaseModel):
    """
    Email templates for automated notifications.
    """

    __tablename__ = "email_templates"

    # Template Details
    name = Column(String(255), nullable=False, unique=True, index=True, comment="Template name/key")
    subject = Column(String(500), nullable=False, comment="Email subject line")
    body_html = Column(Text, nullable=True, comment="HTML email body")
    body_text = Column(Text, nullable=True, comment="Plain text email body")

    # Category
    category = Column(String(100), nullable=True, index=True, comment="Template category (e.g., reminder, stage_change)")

    # Multi-Tenancy
    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey('companies.id', ondelete='CASCADE'),
        nullable=True,
        index=True,
        comment="Company this template belongs to (for multi-tenancy)"
    )

    # Variables
    available_variables = Column(JSON, nullable=True, comment="List of available template variables")
    # Example: ["deal_name", "stage", "due_date", "assigned_to"]

    # Configuration
    is_active = Column(Boolean, default=True, comment="Whether template is active")

    def __repr__(self):
        return f"<EmailTemplate(name='{self.name}', category='{self.category}')>"


class DealActivity(BaseModel):
    """
    Activity log for deal pipeline (audit trail).
    """

    __tablename__ = "deal_activities"

    # Relationships
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    deal = relationship("Deal", backref="activities")

    # Activity Details
    activity_type = Column(
        SQLEnum(ActivityType, name="activity_type"),
        nullable=False,
        index=True,
        comment="Type of activity"
    )
    title = Column(String(255), nullable=False, comment="Activity title")
    description = Column(Text, nullable=True, comment="Activity description")

    # Actor
    user_name = Column(String(255), nullable=True, comment="User who performed action")
    user_email = Column(String(255), nullable=True, comment="User email")

    # Metadata
    activity_metadata = Column(JSON, nullable=True, comment="Additional activity metadata (JSON)")
    # Example: {"old_stage": "loi", "new_stage": "due_diligence", "score_change": "+5"}

    # Timestamp (using created_at from BaseModel)

    def __repr__(self):
        return f"<DealActivity(type='{self.activity_type}', deal_id='{self.deal_id}', created_at='{self.created_at}')>"


class DealScore(BaseModel):
    """
    Deal scoring for prioritization and success prediction.
    """

    __tablename__ = "deal_scores"

    # Relationships
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    deal = relationship("Deal", backref="scores")

    # Scores (0-100)
    total_score = Column(Float, nullable=False, index=True, comment="Overall deal score (0-100)")
    financial_score = Column(Float, nullable=True, comment="Financial metrics score")
    market_score = Column(Float, nullable=True, comment="Market conditions score")
    location_score = Column(Float, nullable=True, comment="Location quality score")
    property_score = Column(Float, nullable=True, comment="Property condition score")
    timing_score = Column(Float, nullable=True, comment="Deal timing score")
    relationship_score = Column(Float, nullable=True, comment="Broker relationship score")

    # ML Predictions
    success_probability = Column(Float, nullable=True, comment="Predicted probability of closing (0-100)")
    estimated_days_to_close = Column(Integer, nullable=True, comment="Predicted days to close")

    # Scoring Metadata
    scoring_model_version = Column(String(50), nullable=True, comment="Version of scoring algorithm used")
    factors = Column(JSON, nullable=True, comment="Detailed scoring factors (JSON)")

    # Confidence
    confidence = Column(Float, nullable=True, comment="Confidence in score (0-100)")

    def __repr__(self):
        return f"<DealScore(deal_id='{self.deal_id}', total_score={self.total_score}, success_prob={self.success_probability})>"


__all__ = [
    "Deal",
    "DealStage",
    "DealStatus",
    "Broker",
    "BrokerStatus",
    "Comp",
    "TaskStatus",
    "TaskPriority",
    "DocumentStatus",
    "ReminderType",
    "ActivityType",
    "DealTask",
    "DealDocument",
    "DealReminder",
    "DealStageRule",
    "EmailTemplate",
    "DealActivity",
    "DealScore",
]
