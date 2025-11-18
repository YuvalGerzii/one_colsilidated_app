"""Seed data for deal pipeline automation - email templates and default rules."""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.crm import EmailTemplate, DealStageRule, DealStage
import logging

logger = logging.getLogger(__name__)


def seed_email_templates(db: Session):
    """Create default email templates."""

    templates = [
        {
            'name': 'deal_reminder',
            'subject': 'Reminder: {{ reminder_title }} - {{ deal_name }}',
            'category': 'reminder',
            'body_html': '''
<html>
<body>
    <h2>{{ reminder_title }}</h2>
    <p>{{ reminder_message }}</p>

    <h3>Deal Information</h3>
    <ul>
        <li><strong>Property:</strong> {{ deal_name }}</li>
        <li><strong>Stage:</strong> {{ deal_stage }}</li>
        <li><strong>Status:</strong> {{ deal_status }}</li>
        <li><strong>Property Type:</strong> {{ property_type }}</li>
        <li><strong>Market:</strong> {{ market }}</li>
        <li><strong>Asking Price:</strong> {{ asking_price }}</li>
        <li><strong>Lead Analyst:</strong> {{ lead_analyst }}</li>
    </ul>

    <p>Please take action on this deal as needed.</p>

    <p>Best regards,<br>Real Estate Dashboard</p>
</body>
</html>
            ''',
            'body_text': '''
{{ reminder_title }}

{{ reminder_message }}

Deal Information:
- Property: {{ deal_name }}
- Stage: {{ deal_stage }}
- Status: {{ deal_status }}
- Property Type: {{ property_type }}
- Market: {{ market }}
- Asking Price: {{ asking_price }}
- Lead Analyst: {{ lead_analyst }}

Please take action on this deal as needed.

Best regards,
Real Estate Dashboard
            ''',
            'available_variables': [
                'deal_name', 'deal_stage', 'deal_status', 'reminder_title',
                'reminder_message', 'property_type', 'market', 'asking_price', 'lead_analyst'
            ],
        },
        {
            'name': 'stage_transition',
            'subject': 'Deal Stage Updated: {{ deal_name }} → {{ to_stage }}',
            'category': 'stage_change',
            'body_html': '''
<html>
<body>
    <h2>Deal Stage Updated</h2>
    <p>The deal <strong>{{ deal_name }}</strong> has been moved from <strong>{{ from_stage }}</strong> to <strong>{{ to_stage }}</strong>.</p>

    <h3>Deal Information</h3>
    <ul>
        <li><strong>Property Type:</strong> {{ property_type }}</li>
        <li><strong>Market:</strong> {{ market }}</li>
        <li><strong>Lead Analyst:</strong> {{ lead_analyst }}</li>
    </ul>

    <p>Please review the updated deal status and take any necessary actions.</p>

    <p>Best regards,<br>Real Estate Dashboard</p>
</body>
</html>
            ''',
            'body_text': '''
Deal Stage Updated

The deal {{ deal_name }} has been moved from {{ from_stage }} to {{ to_stage }}.

Deal Information:
- Property Type: {{ property_type }}
- Market: {{ market }}
- Lead Analyst: {{ lead_analyst }}

Please review the updated deal status and take any necessary actions.

Best regards,
Real Estate Dashboard
            ''',
            'available_variables': [
                'deal_name', 'from_stage', 'to_stage', 'property_type', 'market', 'lead_analyst'
            ],
        },
        {
            'name': 'task_assignment',
            'subject': 'Task Assigned: {{ task_title }} - {{ deal_name }}',
            'category': 'task',
            'body_html': '''
<html>
<body>
    <h2>New Task Assigned</h2>
    <p>A new task has been assigned to you for deal <strong>{{ deal_name }}</strong>.</p>

    <h3>Task Details</h3>
    <ul>
        <li><strong>Title:</strong> {{ task_title }}</li>
        <li><strong>Description:</strong> {{ task_description }}</li>
        <li><strong>Priority:</strong> {{ task_priority }}</li>
        <li><strong>Due Date:</strong> {{ task_due_date }}</li>
        <li><strong>Assigned To:</strong> {{ assigned_to }}</li>
    </ul>

    <p>Please complete this task by the due date.</p>

    <p>Best regards,<br>Real Estate Dashboard</p>
</body>
</html>
            ''',
            'body_text': '''
New Task Assigned

A new task has been assigned to you for deal {{ deal_name }}.

Task Details:
- Title: {{ task_title }}
- Description: {{ task_description }}
- Priority: {{ task_priority }}
- Due Date: {{ task_due_date }}
- Assigned To: {{ assigned_to }}

Please complete this task by the due date.

Best regards,
Real Estate Dashboard
            ''',
            'available_variables': [
                'deal_name', 'task_title', 'task_description',
                'task_priority', 'task_due_date', 'assigned_to'
            ],
        },
        {
            'name': 'document_request',
            'subject': 'Document Required: {{ document_name }} - {{ deal_name }}',
            'category': 'document',
            'body_html': '''
<html>
<body>
    <h2>Document Required</h2>
    <p>The following document is required for deal <strong>{{ deal_name }}</strong>.</p>

    <h3>Document Details</h3>
    <ul>
        <li><strong>Document:</strong> {{ document_name }}</li>
        <li><strong>Type:</strong> {{ document_type }}</li>
        <li><strong>Description:</strong> {{ document_description }}</li>
        <li><strong>Due Date:</strong> {{ due_date }}</li>
        <li><strong>Required:</strong> {{ is_required }}</li>
    </ul>

    <p>Please provide this document as soon as possible.</p>

    <p>Best regards,<br>Real Estate Dashboard</p>
</body>
</html>
            ''',
            'body_text': '''
Document Required

The following document is required for deal {{ deal_name }}.

Document Details:
- Document: {{ document_name }}
- Type: {{ document_type }}
- Description: {{ document_description }}
- Due Date: {{ due_date }}
- Required: {{ is_required }}

Please provide this document as soon as possible.

Best regards,
Real Estate Dashboard
            ''',
            'available_variables': [
                'deal_name', 'document_name', 'document_type',
                'document_description', 'due_date', 'is_required'
            ],
        },
        {
            'name': 'due_diligence_complete',
            'subject': 'Due Diligence Complete: {{ deal_name }}',
            'category': 'milestone',
            'body_html': '''
<html>
<body>
    <h2>Due Diligence Complete</h2>
    <p>Due diligence has been completed for <strong>{{ deal_name }}</strong>.</p>

    <h3>Summary</h3>
    <ul>
        <li><strong>Property Type:</strong> {{ property_type }}</li>
        <li><strong>Market:</strong> {{ market }}</li>
        <li><strong>Total Tasks:</strong> {{ total_tasks }}</li>
        <li><strong>Completed Tasks:</strong> {{ completed_tasks }}</li>
        <li><strong>Expected Closing:</strong> {{ expected_closing }}</li>
        <li><strong>Lead Analyst:</strong> {{ lead_analyst }}</li>
    </ul>

    <p>Please proceed to the next stage of the transaction.</p>

    <p>Best regards,<br>Real Estate Dashboard</p>
</body>
</html>
            ''',
            'body_text': '''
Due Diligence Complete

Due diligence has been completed for {{ deal_name }}.

Summary:
- Property Type: {{ property_type }}
- Market: {{ market }}
- Total Tasks: {{ total_tasks }}
- Completed Tasks: {{ completed_tasks }}
- Expected Closing: {{ expected_closing }}
- Lead Analyst: {{ lead_analyst }}

Please proceed to the next stage of the transaction.

Best regards,
Real Estate Dashboard
            ''',
            'available_variables': [
                'deal_name', 'property_type', 'market', 'total_tasks',
                'completed_tasks', 'expected_closing', 'lead_analyst'
            ],
        },
    ]

    created_count = 0
    for template_data in templates:
        # Check if template already exists
        existing = db.query(EmailTemplate).filter(
            EmailTemplate.name == template_data['name']
        ).first()

        if not existing:
            template = EmailTemplate(**template_data)
            db.add(template)
            created_count += 1
            logger.info(f"Created email template: {template_data['name']}")

    db.commit()
    logger.info(f"Created {created_count} email templates")
    return created_count


def seed_automation_rules(db: Session):
    """Create default automation rules."""

    rules = [
        {
            'name': 'Research to LOI - Auto Tasks',
            'description': 'Automatically create LOI tasks when moving from Research to LOI',
            'from_stage': DealStage.RESEARCH,
            'to_stage': DealStage.LOI,
            'is_active': True,
            'auto_transition': False,
            'priority': 1,
            'conditions': {
                'min_score': 60,
                'min_confidence': 50,
            },
            'actions': {
                'send_email': True,
                'notify_slack': True,
                'slack_channels': ['#deals'],
                'create_tasks': [
                    {
                        'title': 'Prepare LOI',
                        'description': 'Draft and review Letter of Intent',
                        'task_type': 'Legal',
                        'priority': 'high',
                        'due_in_days': 7,
                        'blocks_stage_transition': True,
                    },
                    {
                        'title': 'Financial Preliminary Analysis',
                        'description': 'Conduct initial financial review',
                        'task_type': 'Financial Review',
                        'priority': 'high',
                        'due_in_days': 5,
                        'blocks_stage_transition': False,
                    },
                ],
            },
        },
        {
            'name': 'LOI to Due Diligence - Auto Checklist',
            'description': 'Automatically create due diligence checklist when LOI is accepted',
            'from_stage': DealStage.LOI,
            'to_stage': DealStage.DUE_DILIGENCE,
            'is_active': True,
            'auto_transition': False,
            'priority': 1,
            'conditions': {
                'required_fields': ['loi_date', 'due_diligence_start', 'due_diligence_end'],
            },
            'actions': {
                'send_email': True,
                'notify_slack': True,
                'slack_channels': ['#deals'],
                'create_tasks': [],  # Tasks will be created by automation service
                'create_documents': [],  # Documents will be created by automation service
                'recalculate_score': True,
            },
        },
        {
            'name': 'Due Diligence to Closing - Completion Check',
            'description': 'Verify all DD tasks and documents before moving to closing',
            'from_stage': DealStage.DUE_DILIGENCE,
            'to_stage': DealStage.CLOSING,
            'is_active': True,
            'auto_transition': False,
            'priority': 1,
            'conditions': {
                'all_tasks_complete': True,
                'all_documents_approved': True,
                'min_score': 70,
                'due_diligence_complete': True,
            },
            'actions': {
                'send_email': True,
                'notify_slack': True,
                'slack_channels': ['#deals'],
                'recalculate_score': True,
            },
        },
        {
            'name': 'Closing to Closed - Final Steps',
            'description': 'Auto-transition to closed when all closing tasks complete',
            'from_stage': DealStage.CLOSING,
            'to_stage': DealStage.CLOSED,
            'is_active': True,
            'auto_transition': True,  # Auto-transition enabled
            'priority': 1,
            'conditions': {
                'all_tasks_complete': True,
                'required_fields': ['actual_closing', 'purchase_price'],
            },
            'actions': {
                'send_email': True,
                'notify_slack': True,
                'slack_channels': ['#deals'],
                'recalculate_score': True,
            },
        },
    ]

    created_count = 0
    for rule_data in rules:
        # Check if rule already exists
        existing = db.query(DealStageRule).filter(
            DealStageRule.name == rule_data['name']
        ).first()

        if not existing:
            rule = DealStageRule(**rule_data)
            db.add(rule)
            created_count += 1
            logger.info(f"Created automation rule: {rule_data['name']}")

    db.commit()
    logger.info(f"Created {created_count} automation rules")
    return created_count


def main():
    """Run seed data creation."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting automation data seeding...")

    db = SessionLocal()
    try:
        templates_created = seed_email_templates(db)
        rules_created = seed_automation_rules(db)

        logger.info(f"Seeding complete! Created {templates_created} templates and {rules_created} rules")

        return {
            'success': True,
            'templates_created': templates_created,
            'rules_created': rules_created,
        }
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


if __name__ == '__main__':
    main()
