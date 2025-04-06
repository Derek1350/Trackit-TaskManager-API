import jwt
from datetime import datetime, timedelta
from flask import current_app

# 🔐 Generate JWT token
def generate_token(username, user_id, role, expires_in=3600):
    payload = {
        "username": username,
        "user_id": user_id,
        "role":role,
        "exp": datetime.now() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
    return token


# 🔓 Decode and validate JWT token
def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
