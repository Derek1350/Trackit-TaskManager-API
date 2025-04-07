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
# redis_client = Redis.from_url("redis://redis:6379/0")  # You can replace this with your Redis URL in the environment

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = Redis.from_url(redis_url)
