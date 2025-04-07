import csv
import requests
import io
from flask import Blueprint, request, jsonify
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.api.middlewares.auth import token_required, role_required
from app.utils.jwt_helper import decode_token

task_bp = Blueprint('task_bp', __name__, url_prefix='/api/tasks')

def convert_to_csv_url(gsheet_url):
    if "/edit" in gsheet_url:
        return gsheet_url.split("/edit")[0] + "/export?format=csv"
    return gsheet_url

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
    token_payload = token_payload_retrieve(request)
    user_id = token_payload['user_id']
    data = request.get_json()

    csv_url = convert_to_csv_url(data.get('csv_url'))

    if csv_url:
        try:
            response = requests.get(csv_url)
            response.raise_for_status()
        except Exception as e:
            return jsonify({"error": "Unable to fetch CSV file", "details": str(e)}), 400

        stream = io.StringIO(response.text)
        csv_reader = csv.DictReader(stream)

        created_tasks = []
        for row in csv_reader:
            title = row.get('title')
            description = row.get('description')
            priority = row.get('priority', 'low')

            if not title or not description:
                continue  # Skip invalid rows

            task = create_task(user_id, title, description, priority)
            created_tasks.append(task)

        return jsonify({
            "message": f"{len(created_tasks)} tasks created from CSV.",
            "tasks": created_tasks
        }), 201

    # Fallback to normal JSON
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'low')

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    task = create_task(user_id, title, description, priority)
    return jsonify({"message": "Task created", "task": task}), 201


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
    token_payload = token_payload_retrieve(request)

    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Allow partial updates
    fields_to_update = {}
    allowed_fields = ['title', 'description', 'priority', 'is_active']

    for field in allowed_fields:
        if field in data:
            fields_to_update[field] = data[field]

    if not fields_to_update:
        return jsonify({"message": "No valid fields to update"}), 400

    task = update_task(
        task_id,
        fields_to_update,
        token_payload['user_id'],
        token_payload['role']
    )

    return jsonify({"message": "Task updated", "task": task})



# Delete a task (Admin only)
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@role_required('admin')
@token_required
def delete_task_route(task_id):
    deleted_task = delete_task(task_id)
    return jsonify({"message": "Task deleted successfully","Deleted_task":deleted_task})
