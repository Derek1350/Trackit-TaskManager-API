from app.extensions import db
from app.models.task_manager import TaskManager

# ✅ Helper to serialize task object
def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_active": task.is_active,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat() if task.created_at else None
    }

# 🚀 Add task to DB
def add_task_to_db(task):
    db.session.add(task)
    db.session.commit()
    return task

# 🚀 Get all tasks or tasks by user_id
def get_task_from_db(user_id=None,task_id=None):
    query = TaskManager.query

    if task_id:
        query = query.get(id=task_id)
    if user_id:
        query = query.filter_by(user_id=user_id)

    tasks = query.all()

    return tasks if tasks else None


# 🚀 Update task in DB
def update_task_in_db(task):
    db.session.commit()
    return task

# 🚀 Delete task from DB (doesn't need to return anything)
def delete_task_from_db(task):
    db.session.delete(task)
    db.session.commit()
