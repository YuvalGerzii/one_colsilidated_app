"""Celery background tasks for deal pipeline automation."""

from celery import Celery
from app.settings import settings

# Initialize Celery
celery_app = Celery(
    'deal_automation',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Import tasks (this registers them with Celery)
from app.tasks import deal_reminders
from app.tasks import deal_automation
from app.tasks import deal_scoring

__all__ = ['celery_app']
