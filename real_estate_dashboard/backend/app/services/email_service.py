"""Email service for sending automated notifications."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from jinja2 import Template
import logging

from app.settings import settings
from app.models.crm import EmailTemplate, Deal, DealTask, DealDocument
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails with template support."""

    def __init__(self):
        """Initialize email service with SMTP settings."""
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
        self.email_from_name = getattr(settings, 'EMAIL_FROM_NAME', 'Real Estate Dashboard')

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body_html: Optional[str] = None,
        body_text: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
    ) -> bool:
        """
        Send an email.

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body_html: HTML email body
            body_text: Plain text email body (fallback)
            cc_emails: CC recipients
            bcc_emails: BCC recipients

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.email_from_name} <{self.email_from}>"
            msg['To'] = ', '.join(to_emails)

            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)

            # Attach plain text and HTML versions
            if body_text:
                msg.attach(MIMEText(body_text, 'plain'))
            if body_html:
                msg.attach(MIMEText(body_html, 'html'))

            # Combine all recipients
            all_recipients = to_emails.copy()
            if cc_emails:
                all_recipients.extend(cc_emails)
            if bcc_emails:
                all_recipients.extend(bcc_emails)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {', '.join(to_emails)}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_template_email(
        self,
        db: Session,
        template_name: str,
        to_emails: List[str],
        variables: Dict[str, Any],
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
    ) -> bool:
        """
        Send an email using a template.

        Args:
            db: Database session
            template_name: Template name to use
            to_emails: List of recipient email addresses
            variables: Template variables
            cc_emails: CC recipients
            bcc_emails: BCC recipients

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Load template from database
            template = db.query(EmailTemplate).filter(
                EmailTemplate.name == template_name,
                EmailTemplate.is_active == True
            ).first()

            if not template:
                logger.error(f"Email template '{template_name}' not found")
                return False

            # Render subject
            subject_template = Template(template.subject)
            subject = subject_template.render(**variables)

            # Render HTML body
            body_html = None
            if template.body_html:
                html_template = Template(template.body_html)
                body_html = html_template.render(**variables)

            # Render text body
            body_text = None
            if template.body_text:
                text_template = Template(template.body_text)
                body_text = text_template.render(**variables)

            # Send email
            return self.send_email(
                to_emails=to_emails,
                subject=subject,
                body_html=body_html,
                body_text=body_text,
                cc_emails=cc_emails,
                bcc_emails=bcc_emails,
            )

        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False

    def send_deal_reminder(
        self,
        db: Session,
        deal: Deal,
        reminder_title: str,
        reminder_message: str,
        to_emails: List[str],
    ) -> bool:
        """
        Send a deal reminder email.

        Args:
            db: Database session
            deal: Deal object
            reminder_title: Reminder title
            reminder_message: Reminder message
            to_emails: Recipient emails

        Returns:
            True if sent successfully
        """
        variables = {
            'deal_name': deal.property_name,
            'deal_stage': deal.stage.value,
            'deal_status': deal.status.value,
            'reminder_title': reminder_title,
            'reminder_message': reminder_message,
            'property_type': deal.property_type or 'N/A',
            'market': deal.market or 'N/A',
            'asking_price': f"${deal.asking_price:,.0f}" if deal.asking_price else 'N/A',
            'lead_analyst': deal.lead_analyst or 'Unassigned',
        }

        return self.send_template_email(
            db=db,
            template_name='deal_reminder',
            to_emails=to_emails,
            variables=variables,
        )

    def send_stage_transition_notification(
        self,
        db: Session,
        deal: Deal,
        from_stage: str,
        to_stage: str,
        to_emails: List[str],
    ) -> bool:
        """
        Send notification when deal stage changes.

        Args:
            db: Database session
            deal: Deal object
            from_stage: Previous stage
            to_stage: New stage
            to_emails: Recipient emails

        Returns:
            True if sent successfully
        """
        variables = {
            'deal_name': deal.property_name,
            'from_stage': from_stage,
            'to_stage': to_stage,
            'property_type': deal.property_type or 'N/A',
            'market': deal.market or 'N/A',
            'lead_analyst': deal.lead_analyst or 'Unassigned',
        }

        return self.send_template_email(
            db=db,
            template_name='stage_transition',
            to_emails=to_emails,
            variables=variables,
        )

    def send_task_assignment(
        self,
        db: Session,
        deal: Deal,
        task: DealTask,
        to_emails: List[str],
    ) -> bool:
        """
        Send notification when task is assigned.

        Args:
            db: Database session
            deal: Deal object
            task: DealTask object
            to_emails: Recipient emails

        Returns:
            True if sent successfully
        """
        variables = {
            'deal_name': deal.property_name,
            'task_title': task.title,
            'task_description': task.description or 'No description',
            'task_priority': task.priority.value,
            'task_due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else 'No due date',
            'assigned_to': task.assigned_to or 'Unassigned',
        }

        return self.send_template_email(
            db=db,
            template_name='task_assignment',
            to_emails=to_emails,
            variables=variables,
        )

    def send_document_request(
        self,
        db: Session,
        deal: Deal,
        document: DealDocument,
        to_emails: List[str],
    ) -> bool:
        """
        Send notification requesting a document.

        Args:
            db: Database session
            deal: Deal object
            document: DealDocument object
            to_emails: Recipient emails

        Returns:
            True if sent successfully
        """
        variables = {
            'deal_name': deal.property_name,
            'document_name': document.document_name,
            'document_type': document.document_type or 'General',
            'document_description': document.description or 'No description',
            'due_date': document.due_date.strftime('%Y-%m-%d') if document.due_date else 'No due date',
            'is_required': 'Required' if document.is_required else 'Optional',
        }

        return self.send_template_email(
            db=db,
            template_name='document_request',
            to_emails=to_emails,
            variables=variables,
        )

    def send_due_diligence_complete(
        self,
        db: Session,
        deal: Deal,
        to_emails: List[str],
    ) -> bool:
        """
        Send notification when due diligence is complete.

        Args:
            db: Database session
            deal: Deal object
            to_emails: Recipient emails

        Returns:
            True if sent successfully
        """
        # Get task completion stats
        total_tasks = db.query(DealTask).filter(DealTask.deal_id == deal.id).count()
        completed_tasks = db.query(DealTask).filter(
            DealTask.deal_id == deal.id,
            DealTask.status == 'completed'
        ).count()

        variables = {
            'deal_name': deal.property_name,
            'property_type': deal.property_type or 'N/A',
            'market': deal.market or 'N/A',
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'expected_closing': deal.expected_closing.strftime('%Y-%m-%d') if deal.expected_closing else 'TBD',
            'lead_analyst': deal.lead_analyst or 'Unassigned',
        }

        return self.send_template_email(
            db=db,
            template_name='due_diligence_complete',
            to_emails=to_emails,
            variables=variables,
        )


# Global email service instance
email_service = EmailService()
