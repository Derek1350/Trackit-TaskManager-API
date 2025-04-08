from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from redis import Redis
import os

# Initialize SQLAlchemy, JWT, Migrate
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

# Initialize Redis client
redis_url = os.getenv("REDIS_URL")
redis_client = Redis.from_url(redis_url)  # You can replace this with your Redis URL in the environment
