"""
Celery workers for async task processing.
"""

from app.workers.tasks import celery_app

__all__ = ["celery_app"]
