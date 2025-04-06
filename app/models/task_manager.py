from app.extensions import db
from datetime import datetime

class TaskManager(db.Model):
    __tablename__ = 'task_managers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(50), default="low") 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    logs = db.relationship('TaskLogger', backref='task', lazy=True)
