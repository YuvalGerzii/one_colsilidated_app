"""Multi-channel notification service for deal pipeline automation."""

from typing import List, Optional, Dict, Any
import logging
from sqlalchemy.orm import Session

from app.models.crm import Deal, DealTask, DealDocument, ReminderType
from app.services.email_service import email_service
from app.integrations.tools.slack import SlackIntegration
from app.integrations.base import IntegrationConfig
from app.settings import settings

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending multi-channel notifications."""

    def __init__(self):
        """Initialize notification service."""
        self.email_service = email_service
        self.slack_client = None

        # Initialize Slack if configured
        slack_token = getattr(settings, 'SLACK_BOT_TOKEN', None)
        if slack_token:
            try:
                config = IntegrationConfig(
                    api_key=slack_token,
                    is_active=True
                )
                self.slack_client = SlackIntegration(config=config)
            except Exception as e:
                logger.warning(f"Failed to initialize Slack client: {e}")

    def send_notification(
        self,
        db: Session,
        notification_type: ReminderType,
        email_addresses: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
        subject: str = "",
        message: str = "",
        template_name: Optional[str] = None,
        template_variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification via multiple channels.

        Args:
            db: Database session
            notification_type: Type of notification (email, slack, in_app, all)
            email_addresses: Email recipients
            slack_channels: Slack channels to notify
            subject: Notification subject
            message: Notification message
            template_name: Email template name (optional)
            template_variables: Template variables (optional)

        Returns:
            Dict with success status for each channel
        """
        results = {
            'email': False,
            'slack': False,
        }

        # Send email notification
        if notification_type in [ReminderType.EMAIL, ReminderType.ALL]:
            if email_addresses:
                if template_name and template_variables:
                    results['email'] = self.email_service.send_template_email(
                        db=db,
                        template_name=template_name,
                        to_emails=email_addresses,
                        variables=template_variables,
                    )
                else:
                    results['email'] = self.email_service.send_email(
                        to_emails=email_addresses,
                        subject=subject,
                        body_text=message,
                        body_html=f"<html><body>{message}</body></html>",
                    )

        # Send Slack notification
        if notification_type in [ReminderType.SLACK, ReminderType.ALL]:
            if slack_channels and self.slack_client:
                try:
                    for channel in slack_channels:
                        self.slack_client.send_message(
                            channel=channel,
                            text=f"*{subject}*\n{message}",
                        )
                    results['slack'] = True
                except Exception as e:
                    logger.error(f"Failed to send Slack notification: {e}")
                    results['slack'] = False

        return results

    def notify_deal_stage_change(
        self,
        db: Session,
        deal: Deal,
        from_stage: str,
        to_stage: str,
        notification_channels: ReminderType = ReminderType.ALL,
        email_recipients: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification when deal stage changes.

        Args:
            db: Database session
            deal: Deal object
            from_stage: Previous stage
            to_stage: New stage
            notification_channels: Which channels to use
            email_recipients: Email addresses
            slack_channels: Slack channels

        Returns:
            Dict with success status for each channel
        """
        subject = f"Deal Stage Updated: {deal.property_name}"
        message = (
            f"Deal '{deal.property_name}' has moved from {from_stage} to {to_stage}.\n\n"
            f"Property Type: {deal.property_type or 'N/A'}\n"
            f"Market: {deal.market or 'N/A'}\n"
            f"Lead Analyst: {deal.lead_analyst or 'Unassigned'}"
        )

        return self.send_notification(
            db=db,
            notification_type=notification_channels,
            email_addresses=email_recipients,
            slack_channels=slack_channels,
            subject=subject,
            message=message,
            template_name='stage_transition',
            template_variables={
                'deal_name': deal.property_name,
                'from_stage': from_stage,
                'to_stage': to_stage,
                'property_type': deal.property_type or 'N/A',
                'market': deal.market or 'N/A',
                'lead_analyst': deal.lead_analyst or 'Unassigned',
            }
        )

    def notify_task_due(
        self,
        db: Session,
        deal: Deal,
        task: DealTask,
        notification_channels: ReminderType = ReminderType.ALL,
        email_recipients: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification when task is due.

        Args:
            db: Database session
            deal: Deal object
            task: Task object
            notification_channels: Which channels to use
            email_recipients: Email addresses
            slack_channels: Slack channels

        Returns:
            Dict with success status for each channel
        """
        due_date_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No due date'
        subject = f"Task Due: {task.title}"
        message = (
            f"Task '{task.title}' is due for deal '{deal.property_name}'.\n\n"
            f"Due Date: {due_date_str}\n"
            f"Priority: {task.priority.value}\n"
            f"Assigned To: {task.assigned_to or 'Unassigned'}\n"
            f"Description: {task.description or 'No description'}"
        )

        return self.send_notification(
            db=db,
            notification_type=notification_channels,
            email_addresses=email_recipients,
            slack_channels=slack_channels,
            subject=subject,
            message=message,
        )

    def notify_document_required(
        self,
        db: Session,
        deal: Deal,
        document: DealDocument,
        notification_channels: ReminderType = ReminderType.ALL,
        email_recipients: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification when document is required.

        Args:
            db: Database session
            deal: Deal object
            document: Document object
            notification_channels: Which channels to use
            email_recipients: Email addresses
            slack_channels: Slack channels

        Returns:
            Dict with success status for each channel
        """
        due_date_str = document.due_date.strftime('%Y-%m-%d') if document.due_date else 'No due date'
        subject = f"Document Required: {document.document_name}"
        message = (
            f"Document '{document.document_name}' is required for deal '{deal.property_name}'.\n\n"
            f"Document Type: {document.document_type or 'General'}\n"
            f"Due Date: {due_date_str}\n"
            f"Required: {'Yes' if document.is_required else 'No'}\n"
            f"Description: {document.description or 'No description'}"
        )

        return self.send_notification(
            db=db,
            notification_type=notification_channels,
            email_addresses=email_recipients,
            slack_channels=slack_channels,
            subject=subject,
            message=message,
        )

    def notify_due_diligence_milestone(
        self,
        db: Session,
        deal: Deal,
        milestone: str,
        notification_channels: ReminderType = ReminderType.ALL,
        email_recipients: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification for due diligence milestone.

        Args:
            db: Database session
            deal: Deal object
            milestone: Milestone description
            notification_channels: Which channels to use
            email_recipients: Email addresses
            slack_channels: Slack channels

        Returns:
            Dict with success status for each channel
        """
        subject = f"Due Diligence Milestone: {deal.property_name}"
        message = (
            f"Deal '{deal.property_name}' has reached milestone: {milestone}\n\n"
            f"Property Type: {deal.property_type or 'N/A'}\n"
            f"Market: {deal.market or 'N/A'}\n"
            f"Current Stage: {deal.stage.value}\n"
            f"Lead Analyst: {deal.lead_analyst or 'Unassigned'}"
        )

        return self.send_notification(
            db=db,
            notification_type=notification_channels,
            email_addresses=email_recipients,
            slack_channels=slack_channels,
            subject=subject,
            message=message,
        )

    def notify_deal_score_updated(
        self,
        db: Session,
        deal: Deal,
        old_score: float,
        new_score: float,
        notification_channels: ReminderType = ReminderType.ALL,
        email_recipients: Optional[List[str]] = None,
        slack_channels: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Send notification when deal score is updated.

        Args:
            db: Database session
            deal: Deal object
            old_score: Previous score
            new_score: New score
            notification_channels: Which channels to use
            email_recipients: Email addresses
            slack_channels: Slack channels

        Returns:
            Dict with success status for each channel
        """
        score_change = new_score - old_score
        direction = "increased" if score_change > 0 else "decreased"

        subject = f"Deal Score Updated: {deal.property_name}"
        message = (
            f"Deal score for '{deal.property_name}' has {direction} from "
            f"{old_score:.1f} to {new_score:.1f} ({score_change:+.1f}).\n\n"
            f"Current Stage: {deal.stage.value}\n"
            f"Lead Analyst: {deal.lead_analyst or 'Unassigned'}"
        )

        return self.send_notification(
            db=db,
            notification_type=notification_channels,
            email_addresses=email_recipients,
            slack_channels=slack_channels,
            subject=subject,
            message=message,
        )


# Global notification service instance
notification_service = NotificationService()
