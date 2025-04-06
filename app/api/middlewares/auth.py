from functools import wraps
from flask import request, jsonify
from app.utils.jwt_helper import decode_token

# Requires valid JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401

        try:
            token = auth_header.split(" ")[1]
            data = decode_token(token)
            if "error" in data:
                return jsonify({"message": data["error"]}), 401

            request.user = data  # Attach user info to request context
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated


# Requires specific role
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"message": "Token is missing"}), 401

            try:
                token = auth_header.split(" ")[1]
                data = decode_token(token)
                if "error" in data:
                    return jsonify({"message": data["error"]}), 401

                if data.get("role") not in roles:
                    return jsonify({"message": "Unauthorized: insufficient permissions"}), 403

                request.user = data
            except Exception:
                return jsonify({"message": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated
    return wrapper
