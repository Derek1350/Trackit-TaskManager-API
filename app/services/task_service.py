import json
from app.repositories.task_repo import add_task_to_db, get_task_from_db, update_task_in_db, delete_task_from_db
from app.models.task_manager import TaskManager
from app.extensions import redis_client, db
from datetime import timedelta

CACHE_EXPIRY = 600 

def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_active": task.is_active,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "priority": task.priority
    }

def create_task(user_id, title, description, priority):
    task = TaskManager(user_id=user_id, title=title, description=description, priority=priority)
    add_task_to_db(task)

    # Invalidate related caches
    redis_client.delete("all_tasks")
    redis_client.delete(f"user_tasks:{user_id}")

    return serialize_task(task)

def get_tasks(user_id, role):
    if role == 'admin':
        cached = redis_client.get("all_tasks")
        if cached:
            return json.loads(cached)

        tasks = [serialize_task(task) for task in get_task_from_db()]
        redis_client.setex("all_tasks", CACHE_EXPIRY, json.dumps(tasks))
        return tasks

    else:
        cache_key = f"user_tasks:{user_id}"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        tasks = [serialize_task(task) for task in get_task_from_db(user_id)]
        redis_client.setex(cache_key, CACHE_EXPIRY, json.dumps(tasks))
        return tasks

def update_task(task_id, updated_fields, user_id, role):
    task = TaskManager.query.get(task_id)

    if not task:
        return {"error": "Task not found"}, 404

    if task.user_id != user_id and role != 'admin':
        return {"error": "Unauthorized"}, 403

    for key, value in updated_fields.items():
        setattr(task, key, value)

    update_task_in_db()

    redis_client.delete("all_tasks")
    redis_client.delete(f"user_tasks:{task.user_id}")

    return serialize_task(task)

def delete_task(task_id):
    task = get_task_from_db(task_id=task_id)
    if task:
        delete_task_from_db(task)

        redis_client.delete("all_tasks")
        redis_client.delete(f"user_tasks:{task.user_id}")

    return serialize_task(task)
