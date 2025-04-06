from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.users import User
from app.utils.jwt_helper import generate_token
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')  # default role = user

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    # Check if user already exists based on username or email
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Username or email already exists"}), 409

    # Create a new User instance
    new_user = User(username=username, role=role, email=data.get('email'))
    new_user.set_password(password)  # Hash and set the password

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 409

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user.username, user.id, user.role.value)
    return jsonify({"access_token": token}), 200
