from flask import Flask
from app.extensions import db, jwt, migrate, redis_client
from app.config import get_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    jwt.init_app(app)
    app.redis = redis_client
    migrate.init_app(app, db)
    from .models import users, task_logger, task_manager

    from app.api.routes.routes import main_bp
    app.register_blueprint(main_bp)

    from app.api.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    return app
