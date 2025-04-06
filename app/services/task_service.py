import json
from app.repositories.task_repo import add_task_to_db, get_task_from_db, update_task_in_db, delete_task_from_db
from app.models.task_manager import TaskManager
from app.extensions import redis_client, db

def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_active": task.is_active,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "priority" :task.priority
    }

def create_task(user_id, title, description,priority):
    task = TaskManager(user_id=user_id, title=title, description=description, priority=priority)
    add_task_to_db(task)

    return serialize_task(task)

def get_tasks(user_id, role):
    if role == 'admin':
        tasks = [serialize_task(task) for task in get_task_from_db()]  # Admin can see all tasks
    else:
        tasks = [serialize_task(task) for task in get_task_from_db(user_id)]  # User can only see their tasks
    
    return tasks

def update_task(task_id, title, description, user_id, role):
    task = get_task_from_db(task_id=task_id)
    if not task:
        return None  # Task not found

    if task.user_id != user_id and role != 'admin':
        raise PermissionError("You are not authorized to update this task")

    task.title = title
    task.description = description
    task = update_task_in_db(task)

    return serialize_task(task)

# Delete a task (only admin can delete)
def delete_task(task_id):
    task = get_task_from_db(task_id=task_id)
    if task:
        delete_task_from_db(task)
        
    return serialize_task(task)
