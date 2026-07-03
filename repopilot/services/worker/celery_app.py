# Celery app for RepoPilot workers

from celery import Celery
import sys
import os

# Add packages to path
sys.path.insert(0, '/packages/shared')
sys.path.insert(0, '/packages/evals')
sys.path.insert(0, '/app')

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    'repopilot',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.workers.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    worker_prefetch_multiplier=1,
    task_routes={
        'app.workers.tasks.ingest_repository_task': {'queue': 'ingestion'},
        'app.workers.tasks.codebase_query_task': {'queue': 'query'},
        'app.workers.tasks.bug_fix_task': {'queue': 'bugfix'},
        'app.workers.tasks.run_evaluation_task': {'queue': 'evaluation'},
    },
)

if __name__ == '__main__':
    celery_app.start()
