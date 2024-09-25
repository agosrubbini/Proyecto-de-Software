from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.models.user import User
from src.core.auth.models.roles_and_permissions import Role, Permision

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    hash = bcrypt.generate_password_hash(kwargs['password'].encode('utf-8'))
    kwargs['password'] = hash.decode('utf-8')
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
    permission = Permision(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission

def assign_user(user, role):
    user.role = role
    db.session.add(user)
    db.session.commit()

    return user