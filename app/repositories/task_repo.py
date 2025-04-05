from app.extensions import db
from app.models.task_manager import TaskManager

# 🚀 Add task to DB
def add_task_to_db(task):
    db.session.add(task)
    db.session.commit()
    return task

# 🚀 Get all tasks or tasks by specific user_id
def get_task_from_db(user_id=None):
    if user_id:
        return TaskManager.query.filter_by(user_id=user_id).all()  # Get tasks for a specific user
    return TaskManager.query.all()  # Get all tasks

# 🚀 Update task in DB
def update_task_in_db(task):
    db.session.commit()  # Commit any changes made to task
    return task

# 🚀 Delete task from DB
def delete_task_from_db(task):
    db.session.delete(task)
    db.session.commit()
