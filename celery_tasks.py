# celery_tasks.py
from app.extensions import db, redis_client
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from celery_worker import celery
from datetime import datetime

@celery.task(name='tasks.move_inactive_tasks_to_logs')
def move_inactive_tasks_to_logs():
    inactive_tasks = TaskManager.query.filter_by(is_active=False).all()

    for task in inactive_tasks:
        log = TaskLogger(task_id=task.id, log_message="Task archived at midnight.")
        db.session.add(log)
        db.session.delete(task)

    db.session.commit()

    # 🚨 Invalidate Redis caches
    redis_client.flushdb()  # Optional: use delete("all_tasks") etc. if more control needed

    print(f"[{datetime.now()}] Archived {len(inactive_tasks)} tasks.")
