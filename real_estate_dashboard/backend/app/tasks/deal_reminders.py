"""Celery tasks for sending deal reminders and notifications."""

from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session

from app.tasks import celery_app
from app.core.database import SessionLocal
from app.models.crm import Deal, DealReminder, DealTask, DealDocument, ReminderType
from app.services.notification_service import notification_service

logger = logging.getLogger(__name__)


@celery_app.task(name='send_due_reminders')
def send_due_reminders():
    """
    Send reminders for tasks and documents that are due soon or overdue.
    Run daily.
    """
    db = SessionLocal()
    try:
        logger.info("Starting send_due_reminders task")

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        sent_count = 0

        # Check pending reminders
        pending_reminders = db.query(DealReminder).filter(
            DealReminder.is_sent == False,
            DealReminder.remind_at <= datetime.now(),
        ).all()

        for reminder in pending_reminders:
            try:
                # Get deal
                deal = db.query(Deal).filter(Deal.id == reminder.deal_id).first()
                if not deal:
                    continue

                # Parse recipient emails
                email_recipients = None
                if reminder.recipient_emails:
                    email_recipients = [e.strip() for e in reminder.recipient_emails.split(',')]

                # Parse Slack channels
                slack_channels = None
                if reminder.recipient_slack_channels:
                    slack_channels = [c.strip() for c in reminder.recipient_slack_channels.split(',')]

                # Send notification
                notification_service.send_notification(
                    db=db,
                    notification_type=reminder.reminder_type,
                    email_addresses=email_recipients,
                    slack_channels=slack_channels,
                    subject=reminder.title,
                    message=reminder.message,
                )

                # Mark as sent
                reminder.is_sent = True
                reminder.sent_at = datetime.now()

                # Handle recurring reminders
                if reminder.is_recurring and reminder.recurrence_days:
                    # Create next reminder
                    next_reminder = DealReminder(
                        deal_id=reminder.deal_id,
                        task_id=reminder.task_id,
                        title=reminder.title,
                        message=reminder.message,
                        remind_at=reminder.remind_at + timedelta(days=reminder.recurrence_days),
                        recipient_emails=reminder.recipient_emails,
                        recipient_slack_channels=reminder.recipient_slack_channels,
                        reminder_type=reminder.reminder_type,
                        is_recurring=True,
                        recurrence_days=reminder.recurrence_days,
                    )
                    db.add(next_reminder)

                sent_count += 1

            except Exception as e:
                logger.error(f"Error sending reminder {reminder.id}: {e}")

        # Check overdue tasks
        overdue_tasks = db.query(DealTask).filter(
            DealTask.due_date < today,
            DealTask.status.notin_(['completed', 'cancelled']),
        ).all()

        for task in overdue_tasks:
            try:
                deal = db.query(Deal).filter(Deal.id == task.deal_id).first()
                if not deal:
                    continue

                # Send notification
                recipients = []
                if task.assigned_to:
                    # Would need email lookup for assigned user
                    pass
                if deal.lead_analyst:
                    # Would need email lookup
                    pass

                if recipients:
                    notification_service.notify_task_due(
                        db=db,
                        deal=deal,
                        task=task,
                        notification_channels=ReminderType.ALL,
                        email_recipients=recipients,
                        slack_channels=['#deals-alerts'],
                    )
                    sent_count += 1

            except Exception as e:
                logger.error(f"Error notifying overdue task {task.id}: {e}")

        # Check upcoming task due dates (1 day warning)
        upcoming_tasks = db.query(DealTask).filter(
            DealTask.due_date == tomorrow,
            DealTask.status.notin_(['completed', 'cancelled']),
        ).all()

        for task in upcoming_tasks:
            try:
                deal = db.query(Deal).filter(Deal.id == task.deal_id).first()
                if not deal:
                    continue

                recipients = []
                if task.assigned_to:
                    pass
                if deal.lead_analyst:
                    pass

                if recipients:
                    notification_service.notify_task_due(
                        db=db,
                        deal=deal,
                        task=task,
                        notification_channels=ReminderType.ALL,
                        email_recipients=recipients,
                        slack_channels=['#deals-alerts'],
                    )
                    sent_count += 1

            except Exception as e:
                logger.error(f"Error notifying upcoming task {task.id}: {e}")

        # Check overdue documents
        overdue_docs = db.query(DealDocument).filter(
            DealDocument.due_date < today,
            DealDocument.status.notin_(['approved', 'rejected']),
            DealDocument.is_required == True,
        ).all()

        for doc in overdue_docs:
            try:
                deal = db.query(Deal).filter(Deal.id == doc.deal_id).first()
                if not deal:
                    continue

                recipients = []
                if deal.lead_analyst:
                    pass

                if recipients:
                    notification_service.notify_document_required(
                        db=db,
                        deal=deal,
                        document=doc,
                        notification_channels=ReminderType.ALL,
                        email_recipients=recipients,
                        slack_channels=['#deals-alerts'],
                    )
                    sent_count += 1

            except Exception as e:
                logger.error(f"Error notifying overdue document {doc.id}: {e}")

        db.commit()
        logger.info(f"Sent {sent_count} reminders and notifications")

        return {
            'success': True,
            'sent_count': sent_count,
        }

    except Exception as e:
        logger.error(f"Error in send_due_reminders task: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


@celery_app.task(name='send_weekly_deal_summary')
def send_weekly_deal_summary():
    """
    Send weekly summary of all active deals.
    Run weekly on Monday mornings.
    """
    db = SessionLocal()
    try:
        logger.info("Starting send_weekly_deal_summary task")

        # Get all active deals
        active_deals = db.query(Deal).filter(Deal.status == 'active').all()

        # Group by stage
        deals_by_stage = {}
        for deal in active_deals:
            stage = deal.stage.value
            if stage not in deals_by_stage:
                deals_by_stage[stage] = []
            deals_by_stage[stage].append(deal)

        # Build summary message
        message = "# Weekly Deal Pipeline Summary\n\n"
        message += f"Total Active Deals: {len(active_deals)}\n\n"

        for stage, deals in deals_by_stage.items():
            message += f"## {stage.replace('_', ' ').title()}: {len(deals)} deals\n"
            for deal in deals:
                asking_price = f"${deal.asking_price:,.0f}" if deal.asking_price else "N/A"
                message += f"- {deal.property_name} ({deal.property_type}) - {asking_price}\n"
            message += "\n"

        # Send to configured recipients
        # Would send via email and/or Slack

        logger.info("Weekly deal summary generated")

        return {
            'success': True,
            'total_deals': len(active_deals),
        }

    except Exception as e:
        logger.error(f"Error in send_weekly_deal_summary task: {e}")
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


# Configure Celery Beat schedule
celery_app.conf.beat_schedule = {
    'send-due-reminders-daily': {
        'task': 'send_due_reminders',
        'schedule': 86400.0,  # Every 24 hours (in seconds)
    },
    'send-weekly-summary': {
        'task': 'send_weekly_deal_summary',
        'schedule': 604800.0,  # Every 7 days
    },
}
