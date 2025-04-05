from flask import Blueprint, request, jsonify
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.api.middlewares.auth import token_required, role_required

task_bp = Blueprint('task_bp', __name__, url_prefix='/api/tasks')

# 🎯 Create a new task (Admin or User can create their tasks)
@task_bp.route('', methods=['POST'])
@token_required
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    task = create_task(request.user['user_id'], title, description)
    return jsonify({"message": "Task created", "task": task}), 201


# 🎯 Get tasks (Admin sees all, User sees their own)
@task_bp.route('', methods=['GET'])
@token_required
def get_all_tasks():
    tasks = get_tasks(request.user['user_id'], request.user['role'])
    return jsonify({"tasks": tasks})


# 🎯 Update a task (Admin or the task creator can update)
@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task_route(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title and not description:
        return jsonify({"message": "Either title or description must be provided to update"}), 400

    task = update_task(task_id, title, description, request.user['user_id'], request.user['role'])
    return jsonify({"message": "Task updated", "task": task})


# 🎯 Delete a task (Admin only)
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@role_required('admin')
@token_required
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"})
