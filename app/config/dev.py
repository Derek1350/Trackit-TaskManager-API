import os
class DevConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://flaskuser:flaskpass@db:5432/flaskdb')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
