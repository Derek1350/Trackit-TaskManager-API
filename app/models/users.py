from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Store hashed password
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.user)

    tasks = db.relationship('TaskManager', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == RoleEnum.admin

    def has_permission(self, permission):
        if self.is_admin():
            return True
        if permission == "add_task":
            return True
        return False
