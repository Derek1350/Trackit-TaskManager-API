import json
from app.repositories.task_repo import add_task_to_db, get_task_from_db, update_task_in_db, delete_task_from_db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from app.models.users import User
from app.extensions import redis_client, db
from datetime import datetime

# 🚀 Create a task
def create_task(user_id, title, description):
    task = TaskManager(user_id=user_id, title=title, description=description)
    task = add_task_to_db(task)

    # After adding the task, invalidate the Redis cache
    redis_client.delete("task_managers_all")

    return task

# 🚀 Get tasks for user or admin (with Redis caching)
def get_tasks(user_id, role):
    # Check Redis first for tasks
    cached_tasks = redis_client.get(f"tasks_user_{user_id}")
    
    if cached_tasks:
        return json.loads(cached_tasks)
    
    # If not in Redis, fetch from DB
    if role == 'admin':
        tasks = get_task_from_db()  # Admin can see all tasks
    else:
        tasks = get_task_from_db(user_id)  # User can only see their tasks

    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_active": task.is_active,
            "created_at": task.created_at.isoformat()
        }
        for task in tasks
    ]

    # Cache the tasks for 10 minutes
    redis_client.setex(f"tasks_user_{user_id}", 600, json.dumps(tasks_data))
    
    return tasks_data

# 🚀 Update a task (only user who created or admin can update)
def update_task(task_id, title, description, user_id, role):
    task = get_task_from_db(task_id)
    if not task:
        return None  # Task not found

    if task.user_id != user_id and role != 'admin':
        raise PermissionError("You are not authorized to update this task")

    task.title = title
    task.description = description
    task = update_task_in_db(task)

    # Invalidate Redis cache after updating the task
    redis_client.delete(f"tasks_user_{user_id}")
    redis_client.delete("task_managers_all")

    return task

# 🚀 Delete a task (only admin can delete)
def delete_task(task_id):
    task = get_task_from_db(task_id)
    if task:
        delete_task_from_db(task)
        
        # Invalidate Redis cache after deleting the task
        redis_client.delete(f"tasks_user_{task.user_id}")
        redis_client.delete("task_managers_all")

    return task
