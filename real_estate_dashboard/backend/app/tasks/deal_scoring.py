"""Celery tasks for deal scoring and analytics."""

import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.tasks import celery_app
from app.core.database import SessionLocal
from app.models.crm import Deal, DealScore, ActivityType, DealActivity
from app.services.deal_scoring_service import deal_scoring_service
from app.services.notification_service import notification_service

logger = logging.getLogger(__name__)


@celery_app.task(name='recalculate_deal_scores')
def recalculate_deal_scores():
    """
    Recalculate scores for all active deals.
    Run daily.
    """
    db = SessionLocal()
    try:
        logger.info("Starting recalculate_deal_scores task")

        count = deal_scoring_service.recalculate_all_scores(db)

        logger.info(f"Recalculated scores for {count} deals")

        return {
            'success': True,
            'deals_scored': count,
        }

    except Exception as e:
        logger.error(f"Error in recalculate_deal_scores task: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


@celery_app.task(name='score_single_deal')
def score_single_deal(deal_id: str, notify_on_change: bool = True):
    """
    Score a single deal and optionally notify if score changed significantly.

    Args:
        deal_id: Deal UUID
        notify_on_change: Send notification if score changes by >10 points
    """
    db = SessionLocal()
    try:
        logger.info(f"Scoring deal {deal_id}")

        # Get deal
        deal = db.query(Deal).filter(Deal.id == deal_id).first()
        if not deal:
            return {'success': False, 'error': 'Deal not found'}

        # Get previous score
        prev_score = deal_scoring_service.get_latest_score(db, deal_id)
        prev_total = prev_score.total_score if prev_score else None

        # Calculate new score
        new_total, factors = deal_scoring_service.calculate_deal_score(
            db, deal, save_to_db=True
        )

        # Log activity
        activity = DealActivity(
            deal_id=deal.id,
            activity_type=ActivityType.SCORE_UPDATED,
            title=f"Deal score updated: {new_total:.1f}",
            description=f"Deal score recalculated",
            metadata={
                'new_score': new_total,
                'previous_score': prev_total,
                'factors': factors,
            }
        )
        db.add(activity)
        db.commit()

        # Notify if significant change
        if notify_on_change and prev_total is not None:
            change = abs(new_total - prev_total)
            if change >= 10:
                # Notify team
                recipients = []
                if deal.lead_analyst:
                    pass  # Would add analyst email

                if recipients:
                    notification_service.notify_deal_score_updated(
                        db=db,
                        deal=deal,
                        old_score=prev_total,
                        new_score=new_total,
                        email_recipients=recipients,
                        slack_channels=['#deals-alerts'],
                    )

        logger.info(f"Deal {deal_id} scored: {new_total:.1f}")

        return {
            'success': True,
            'deal_id': deal_id,
            'score': new_total,
            'previous_score': prev_total,
            'change': new_total - prev_total if prev_total else None,
        }

    except Exception as e:
        logger.error(f"Error scoring deal {deal_id}: {e}")
        db.rollback()
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


@celery_app.task(name='identify_high_priority_deals')
def identify_high_priority_deals():
    """
    Identify and report high-priority deals based on scores.
    Run daily.
    """
    db = SessionLocal()
    try:
        logger.info("Starting identify_high_priority_deals task")

        # Get latest scores for all active deals
        from sqlalchemy import desc

        # Subquery to get latest score for each deal
        latest_scores = db.query(
            DealScore.deal_id,
            DealScore.total_score,
            DealScore.success_probability,
        ).distinct(DealScore.deal_id).order_by(
            DealScore.deal_id,
            desc(DealScore.created_at)
        ).all()

        # Find high-scoring deals (>80)
        high_priority = []
        for score_record in latest_scores:
            if score_record.total_score >= 80:
                deal = db.query(Deal).filter(
                    Deal.id == score_record.deal_id,
                    Deal.status == 'active'
                ).first()
                if deal:
                    high_priority.append({
                        'deal': deal,
                        'score': score_record.total_score,
                        'success_prob': score_record.success_probability,
                    })

        # Sort by score
        high_priority.sort(key=lambda x: x['score'], reverse=True)

        # Build report
        if high_priority:
            message = f"# High Priority Deals Report\n\n"
            message += f"Found {len(high_priority)} deals with score >= 80\n\n"

            for item in high_priority[:10]:  # Top 10
                deal = item['deal']
                message += f"## {deal.property_name} - Score: {item['score']:.1f}\n"
                message += f"- Property Type: {deal.property_type}\n"
                message += f"- Market: {deal.market}\n"
                message += f"- Stage: {deal.stage.value}\n"
                message += f"- Success Probability: {item['success_prob']:.1f}%\n"
                message += f"- Lead Analyst: {deal.lead_analyst or 'Unassigned'}\n\n"

            # Send report (email/Slack)
            logger.info(f"Identified {len(high_priority)} high-priority deals")

        return {
            'success': True,
            'high_priority_count': len(high_priority),
        }

    except Exception as e:
        logger.error(f"Error in identify_high_priority_deals task: {e}")
        return {
            'success': False,
            'error': str(e),
        }
    finally:
        db.close()


# Add to Celery Beat schedule
celery_app.conf.beat_schedule.update({
    'recalculate-deal-scores-daily': {
        'task': 'recalculate_deal_scores',
        'schedule': 86400.0,  # Every 24 hours
    },
    'identify-high-priority-deals-daily': {
        'task': 'identify_high_priority_deals',
        'schedule': 86400.0,  # Every 24 hours
    },
})
