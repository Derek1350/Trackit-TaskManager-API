from celery import Celery
from celery.schedules import crontab
import os

def make_celery():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return Celery('worker', broker=redis_url, backend=redis_url)

celery = make_celery()

# ⏰ Schedule the midnight job
celery.conf.beat_schedule = {
    'move-inactive-tasks-nightly': {
        'task': 'tasks.move_inactive_tasks_to_logs',
        'schedule': crontab(hour=0, minute=0),  # Every midnight
    },
}
celery.conf.timezone = 'Asia/Kolkata'  # Or your local timezone

import celery_tasks