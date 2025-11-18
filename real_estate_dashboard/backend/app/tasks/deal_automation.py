"""Celery tasks for deal pipeline automation."""

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.tasks import celery_app
from app.core.database import SessionLocal
from app.models.crm import Deal, DealStage
from app.services.automation_service import deal_automation_service
from app.services.comp_pulling_service import comp_pulling_service

logger = logging.getLogger(__name__)


@celery_app.task(name='auto_transition_deals')
def auto_transition_deals():
    """
    Check all active deals and auto-transition if eligible.
    Run every 6 hours.
    """
    db = SessionLocal()
    try:
        logger.info("Starting auto_transition_deals task")

        transitioned = deal_automation_service.monitor_and_auto_transition_deals(db)

        logger.info(f"Auto-transitioned {transitioned} deals")

        return {
            'success': True,
            'transitioned_count': transitioned,
        }

    except Exception as e:
        logger.error(f"Error in auto_transition_deals task: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


@celery_app.task(name='auto_create_due_diligence_checklists')
def auto_create_due_diligence_checklists():
    """
    Auto-create due diligence checklists for deals entering DD stage.
    Run hourly.
    """
    db = SessionLocal()
    try:
        logger.info("Starting auto_create_due_diligence_checklists task")

        # Find deals in due diligence stage without tasks
        dd_deals = db.query(Deal).filter(
            Deal.stage == DealStage.DUE_DILIGENCE,
            Deal.status == 'active',
        ).all()

        created_count = 0

        for deal in dd_deals:
            # Check if deal already has tasks
            from app.models.crm import DealTask
            existing_tasks = db.query(DealTask).filter(
                DealTask.deal_id == deal.id
            ).count()

            if existing_tasks == 0:
                # Create checklist
                items_created = deal_automation_service.auto_create_due_diligence_checklist(
                    db, deal
                )
                created_count += items_created
                logger.info(f"Created {items_created} DD items for deal {deal.id}")

        logger.info(f"Created {created_count} total DD checklist items")

        return {
            'success': True,
            'items_created': created_count,
        }

    except Exception as e:
        logger.error(f"Error in auto_create_due_diligence_checklists task: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


@celery_app.task(name='auto_pull_comps')
def auto_pull_comps(deal_id: str = None):
    """
    Auto-pull comparable properties for new deals.

    Args:
        deal_id: Specific deal ID, or None to process all new deals
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting auto_pull_comps task for deal_id={deal_id}")

        if deal_id:
            # Pull comps for specific deal
            deal = db.query(Deal).filter(Deal.id == deal_id).first()
            if not deal:
                return {'success': False, 'error': 'Deal not found'}

            comps = comp_pulling_service.pull_comps_for_deal(
                db=db,
                deal=deal,
                radius_miles=5.0,
                max_results=20,
            )

            return {
                'success': True,
                'deal_id': deal_id,
                'comps_pulled': len(comps),
            }
        else:
            # Pull comps for all new deals (identified in last 7 days)
            from datetime import date
            week_ago = date.today() - timedelta(days=7)

            new_deals = db.query(Deal).filter(
                Deal.date_identified >= week_ago,
                Deal.status == 'active',
            ).all()

            total_comps = 0
            for deal in new_deals:
                from app.models.crm import Comp
                existing_comps = db.query(Comp).filter(
                    Comp.market == deal.market,
                    Comp.property_type == deal.property_type,
                ).count()

                # Only pull if we don't have many comps
                if existing_comps < 10:
                    comps = comp_pulling_service.pull_comps_for_deal(
                        db=db,
                        deal=deal,
                        radius_miles=5.0,
                        max_results=20,
                    )
                    total_comps += len(comps)

            logger.info(f"Pulled {total_comps} total comps for {len(new_deals)} deals")

            return {
                'success': True,
                'deals_processed': len(new_deals),
                'total_comps': total_comps,
            }

    except Exception as e:
        logger.error(f"Error in auto_pull_comps task: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


# Add to Celery Beat schedule
celery_app.conf.beat_schedule.update({
    'auto-transition-deals': {
        'task': 'auto_transition_deals',
        'schedule': 21600.0,  # Every 6 hours
    },
    'auto-create-dd-checklists': {
        'task': 'auto_create_due_diligence_checklists',
        'schedule': 3600.0,  # Every hour
    },
    'auto-pull-comps-weekly': {
        'task': 'auto_pull_comps',
        'schedule': 604800.0,  # Once a week
    },
})
