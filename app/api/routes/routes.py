from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def landing():
    return render_template('index.html')

@main_bp.route('/api-reference')
def api_selector():
    return render_template('api_reference_select.html')

@main_bp.route('/api-reference/auth')
def auth_docs():
    return render_template('auth_routes.html')

@main_bp.route('/api-reference/tasks')
def task_docs():
    return render_template('task_routes.html')
