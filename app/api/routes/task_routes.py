from flask import Blueprint, request, jsonify
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.api.middlewares.auth import token_required, role_required
from app.utils.jwt_helper import decode_token

task_bp = Blueprint('task_bp', __name__, url_prefix='/api/tasks')

def token_payload_retrieve(request):
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]
        token_payload = decode_token(token)
    else:
        token_payload = {"error": "Authorization header missing or invalid"}
    return token_payload

# Create a new task (Admin or User can create their tasks)
@task_bp.route('', methods=['POST'])
@token_required
def add_task():
    token_payload=token_payload_retrieve(request)
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    user_id = token_payload['user_id']

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    task = create_task(user_id, title, description, priority)
    return jsonify({"message": "Task created","task":task}), 201


# Get tasks (Admin sees all, User sees their own)
@task_bp.route('', methods=['GET'])
@token_required
def get_all_tasks():
    token_payload=token_payload_retrieve(request)
    tasks = get_tasks(token_payload['user_id'], token_payload['role'])
    return jsonify({"tasks": tasks})


# Update a task (Admin or the task creator can update)
@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task_route(task_id):
    data = request.get_json()
    token_payload=token_payload_retrieve(request)
    title = data.get('title')
    description = data.get('description')

    if not title and not description:
        return jsonify({"message": "Either title or description must be provided to update"}), 400

    task = update_task(task_id, title, description, token_payload['user_id'], token_payload['role'])
    return jsonify({"message": "Task updated", "task": task})


# Delete a task (Admin only)
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@role_required('admin')
@token_required
def delete_task_route(task_id):
    deleted_task = delete_task(task_id)
    return jsonify({"message": "Task deleted successfully","Deleted_task":deleted_task})
