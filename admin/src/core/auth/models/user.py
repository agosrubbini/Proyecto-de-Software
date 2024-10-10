from src.core.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    alias = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", backref="role")
    system_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_blocked = db.Column(db.Boolean, default=False)
    # person_id = db.Column(db.Integer, db.ForeignKey("roles.id")) Debería estar este atributo y que pueda tomar valor null?

    def __repr__(self):
        return f'<User #{self.id} email="{self.email}">'
    
    def __init__(self, id=None, email=None, alias=None, password=None, role_id=None, system_admin=None, active=None, created_at=None, is_blocked=None):

        self.id = id 
        self.email = email
        self.alias = alias
        self.password = password
        self.role_id = role_id
        self.system_admin = system_admin
        self.active = active
        self.created_at = created_at
        self.is_blocked = is_blocked
    

