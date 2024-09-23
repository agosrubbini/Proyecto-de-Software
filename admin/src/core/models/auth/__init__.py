from src.core.database import db
from src.core.models.auth.user import User
from src.core.models.auth.roles_and_permissions import Role, Permisions

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role

def create_permission(**kwargs):
    permission = Permisions(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission

def assign_user(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()

    return user