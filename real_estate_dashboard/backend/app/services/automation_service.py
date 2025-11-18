"""Deal pipeline automation service for stage transitions and task management."""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.crm import (
    Deal, DealStage, DealStageRule, DealTask, DealDocument, DealActivity,
    ActivityType, TaskStatus, DocumentStatus, TaskPriority, ReminderType
)
from app.services.notification_service import notification_service
from app.services.deal_scoring_service import deal_scoring_service
from app.settings import settings

logger = logging.getLogger(__name__)


class DealAutomationService:
    """Service for automating deal pipeline transitions and task management."""

    def __init__(self):
        """Initialize automation service."""
        self.notification_service = notification_service
        self.scoring_service = deal_scoring_service

    def check_stage_transition_eligibility(
        self,
        db: Session,
        deal: Deal,
        target_stage: DealStage,
    ) -> tuple[bool, List[str]]:
        """
        Check if a deal is eligible to transition to a new stage.

        Args:
            db: Database session
            deal: Deal object
            target_stage: Target stage to transition to

        Returns:
            Tuple of (is_eligible, list_of_blocking_reasons)
        """
        blocking_reasons = []

        # Get active rules for this transition
        rules = db.query(DealStageRule).filter(
            DealStageRule.from_stage == deal.stage,
            DealStageRule.to_stage == target_stage,
            DealStageRule.is_active == True,
        ).order_by(DealStageRule.priority.desc()).all()

        if not rules:
            # No rules defined, allow transition
            return True, []

        # Check each rule
        for rule in rules:
            if rule.conditions:
                conditions = rule.conditions
                rule_blocking = []

                # Check all tasks complete
                if conditions.get('all_tasks_complete'):
                    incomplete_tasks = db.query(DealTask).filter(
                        DealTask.deal_id == deal.id,
                        DealTask.blocks_stage_transition == True,
                        DealTask.status != TaskStatus.COMPLETED,
                    ).count()
                    if incomplete_tasks > 0:
                        rule_blocking.append(f"{incomplete_tasks} blocking tasks incomplete")

                # Check all documents approved
                if conditions.get('all_documents_approved'):
                    unapproved_docs = db.query(DealDocument).filter(
                        DealDocument.deal_id == deal.id,
                        DealDocument.blocks_stage_transition == True,
                        DealDocument.status != DocumentStatus.APPROVED,
                    ).count()
                    if unapproved_docs > 0:
                        rule_blocking.append(f"{unapproved_docs} blocking documents not approved")

                # Check minimum score
                if conditions.get('min_score'):
                    latest_score = self.scoring_service.get_latest_score(db, deal.id)
                    min_score = conditions['min_score']
                    if not latest_score or latest_score.total_score < min_score:
                        current_score = latest_score.total_score if latest_score else 0
                        rule_blocking.append(f"Deal score {current_score:.1f} below minimum {min_score}")

                # Check required fields
                if conditions.get('required_fields'):
                    for field in conditions['required_fields']:
                        if not getattr(deal, field, None):
                            rule_blocking.append(f"Required field '{field}' is missing")

                # Check minimum confidence
                if conditions.get('min_confidence'):
                    min_conf = conditions['min_confidence']
                    if not deal.confidence_level or deal.confidence_level < min_conf:
                        rule_blocking.append(f"Confidence {deal.confidence_level or 0}% below minimum {min_conf}%")

                # Check due diligence period
                if conditions.get('due_diligence_complete'):
                    if not deal.due_diligence_end:
                        rule_blocking.append("Due diligence end date not set")
                    elif datetime.now().date() < deal.due_diligence_end:
                        rule_blocking.append("Due diligence period not yet complete")

                blocking_reasons.extend(rule_blocking)

        is_eligible = len(blocking_reasons) == 0
        return is_eligible, blocking_reasons

    def attempt_stage_transition(
        self,
        db: Session,
        deal: Deal,
        target_stage: DealStage,
        user_email: Optional[str] = None,
        force: bool = False,
    ) -> tuple[bool, str]:
        """
        Attempt to transition a deal to a new stage.

        Args:
            db: Database session
            deal: Deal object
            target_stage: Target stage
            user_email: Email of user initiating transition
            force: Force transition even if conditions not met

        Returns:
            Tuple of (success, message)
        """
        old_stage = deal.stage

        # Check eligibility
        if not force:
            eligible, reasons = self.check_stage_transition_eligibility(db, deal, target_stage)
            if not eligible:
                return False, f"Cannot transition: {'; '.join(reasons)}"

        # Perform transition
        deal.stage = target_stage

        # Log activity
        activity = DealActivity(
            deal_id=deal.id,
            activity_type=ActivityType.STAGE_CHANGE,
            title=f"Stage changed: {old_stage.value} → {target_stage.value}",
            description=f"Deal transitioned from {old_stage.value} to {target_stage.value}",
            user_email=user_email,
            metadata={
                'old_stage': old_stage.value,
                'new_stage': target_stage.value,
                'forced': force,
            }
        )
        db.add(activity)

        # Execute post-transition actions
        self._execute_transition_actions(db, deal, old_stage, target_stage, user_email)

        db.commit()

        return True, f"Successfully transitioned to {target_stage.value}"

    def _execute_transition_actions(
        self,
        db: Session,
        deal: Deal,
        from_stage: DealStage,
        to_stage: DealStage,
        user_email: Optional[str] = None,
    ):
        """Execute automated actions after stage transition."""
        # Get applicable rules
        rules = db.query(DealStageRule).filter(
            DealStageRule.from_stage == from_stage,
            DealStageRule.to_stage == to_stage,
            DealStageRule.is_active == True,
        ).all()

        for rule in rules:
            if rule.actions:
                actions = rule.actions

                # Send email notification
                if actions.get('send_email'):
                    recipients = actions.get('email_recipients', [])
                    if deal.lead_analyst:
                        # Could parse email from analyst name or use a lookup
                        pass
                    if recipients:
                        self.notification_service.notify_deal_stage_change(
                            db=db,
                            deal=deal,
                            from_stage=from_stage.value,
                            to_stage=to_stage.value,
                            notification_channels=ReminderType.EMAIL,
                            email_recipients=recipients,
                        )

                # Notify Slack
                if actions.get('notify_slack'):
                    channels = actions.get('slack_channels', ['#deals'])
                    self.notification_service.notify_deal_stage_change(
                        db=db,
                        deal=deal,
                        from_stage=from_stage.value,
                        to_stage=to_stage.value,
                        notification_channels=ReminderType.SLACK,
                        slack_channels=channels,
                    )

                # Create tasks
                if actions.get('create_tasks'):
                    task_templates = actions['create_tasks']
                    self._create_tasks_from_templates(db, deal, task_templates)

                # Create document checklist
                if actions.get('create_documents'):
                    doc_templates = actions['create_documents']
                    self._create_documents_from_templates(db, deal, doc_templates)

                # Update deal score
                if actions.get('recalculate_score'):
                    self.scoring_service.calculate_deal_score(db, deal, save_to_db=True)

    def _create_tasks_from_templates(
        self,
        db: Session,
        deal: Deal,
        task_templates: List[Dict[str, Any]],
    ):
        """Create tasks from templates."""
        for template in task_templates:
            task = DealTask(
                deal_id=deal.id,
                title=template.get('title', 'Untitled Task'),
                description=template.get('description'),
                task_type=template.get('task_type'),
                priority=TaskPriority(template.get('priority', 'medium')),
                assigned_to=template.get('assigned_to', deal.lead_analyst),
                due_date=self._calculate_due_date(template.get('due_in_days')),
                blocks_stage_transition=template.get('blocks_stage_transition', False),
                auto_created=True,
            )
            db.add(task)

            # Log activity
            activity = DealActivity(
                deal_id=deal.id,
                activity_type=ActivityType.TASK_CREATED,
                title=f"Task created: {task.title}",
                description=f"Auto-created task: {task.title}",
                metadata={'task_id': str(task.id), 'auto_created': True}
            )
            db.add(activity)

    def _create_documents_from_templates(
        self,
        db: Session,
        deal: Deal,
        doc_templates: List[Dict[str, Any]],
    ):
        """Create document checklist from templates."""
        for template in doc_templates:
            document = DealDocument(
                deal_id=deal.id,
                document_name=template.get('name', 'Untitled Document'),
                document_type=template.get('type'),
                description=template.get('description'),
                is_required=template.get('is_required', True),
                blocks_stage_transition=template.get('blocks_stage_transition', False),
                due_date=self._calculate_due_date(template.get('due_in_days')),
            )
            db.add(document)

    def _calculate_due_date(self, due_in_days: Optional[int]):
        """Calculate due date from days."""
        if due_in_days is None:
            return None
        return (datetime.now() + timedelta(days=due_in_days)).date()

    def auto_create_due_diligence_checklist(
        self,
        db: Session,
        deal: Deal,
    ) -> int:
        """
        Auto-create standard due diligence checklist for a deal.

        Args:
            db: Database session
            deal: Deal object

        Returns:
            Number of items created
        """
        # Standard due diligence tasks
        standard_tasks = [
            {
                'title': 'Financial Review - Rent Roll Analysis',
                'description': 'Review current rent roll, vacancy rates, and lease expirations',
                'task_type': 'Financial Review',
                'priority': 'high',
                'due_in_days': 7,
                'blocks_stage_transition': True,
            },
            {
                'title': 'Financial Review - Operating Statements',
                'description': 'Analyze 3 years of historical operating statements',
                'task_type': 'Financial Review',
                'priority': 'high',
                'due_in_days': 7,
                'blocks_stage_transition': True,
            },
            {
                'title': 'Physical Inspection',
                'description': 'Conduct site visit and property condition assessment',
                'task_type': 'Site Visit',
                'priority': 'high',
                'due_in_days': 14,
                'blocks_stage_transition': True,
            },
            {
                'title': 'Environmental Review',
                'description': 'Review Phase I environmental report',
                'task_type': 'Environmental',
                'priority': 'high',
                'due_in_days': 21,
                'blocks_stage_transition': True,
            },
            {
                'title': 'Legal Review - Title & Survey',
                'description': 'Review title commitment and property survey',
                'task_type': 'Legal',
                'priority': 'high',
                'due_in_days': 21,
                'blocks_stage_transition': True,
            },
            {
                'title': 'Market Analysis',
                'description': 'Conduct market rent and comp analysis',
                'task_type': 'Market Research',
                'priority': 'medium',
                'due_in_days': 14,
                'blocks_stage_transition': False,
            },
        ]

        # Standard due diligence documents
        standard_documents = [
            {
                'name': 'Rent Roll',
                'type': 'Financial',
                'description': 'Current rent roll with lease terms',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 7,
            },
            {
                'name': 'Operating Statements (3 years)',
                'type': 'Financial',
                'description': 'Historical P&L statements',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 7,
            },
            {
                'name': 'Phase I Environmental Report',
                'type': 'Environmental',
                'description': 'Environmental site assessment',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 21,
            },
            {
                'name': 'Title Commitment',
                'type': 'Legal',
                'description': 'Preliminary title report',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 14,
            },
            {
                'name': 'Property Survey',
                'type': 'Legal',
                'description': 'ALTA survey of property',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 21,
            },
            {
                'name': 'Property Condition Report',
                'type': 'Physical',
                'description': 'Third-party property inspection report',
                'is_required': True,
                'blocks_stage_transition': True,
                'due_in_days': 30,
            },
        ]

        count = 0

        # Create tasks
        self._create_tasks_from_templates(db, deal, standard_tasks)
        count += len(standard_tasks)

        # Create documents
        self._create_documents_from_templates(db, deal, standard_documents)
        count += len(standard_documents)

        db.commit()

        logger.info(f"Created {count} due diligence items for deal {deal.id}")
        return count

    def monitor_and_auto_transition_deals(self, db: Session) -> int:
        """
        Check all active deals and auto-transition if eligible.

        Returns:
            Number of deals transitioned
        """
        # Get all active deals
        deals = db.query(Deal).filter(Deal.status == 'active').all()

        transitioned = 0

        for deal in deals:
            # Get applicable auto-transition rules
            rules = db.query(DealStageRule).filter(
                DealStageRule.from_stage == deal.stage,
                DealStageRule.is_active == True,
                DealStageRule.auto_transition == True,
            ).order_by(DealStageRule.priority.desc()).all()

            for rule in rules:
                # Check if eligible
                eligible, _ = self.check_stage_transition_eligibility(
                    db, deal, rule.to_stage
                )

                if eligible:
                    # Attempt transition
                    success, message = self.attempt_stage_transition(
                        db, deal, rule.to_stage, user_email='automation@system'
                    )
                    if success:
                        transitioned += 1
                        logger.info(f"Auto-transitioned deal {deal.id} to {rule.to_stage.value}")
                        break  # Only transition to first eligible stage

        return transitioned


# Global automation service instance
deal_automation_service = DealAutomationService()
