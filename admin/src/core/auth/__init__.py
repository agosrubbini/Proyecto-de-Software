from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.auth.models.user import User
from src.core.auth.models.roles_and_permissions import Role, Permision

def list_users():

    """
        Lista todos los usuarios almacenados en la base de datos y los retorna
    """

    users = User.query.all()

    return users

def create_user(**kwargs):

    """
        Crea un objeto User en la base de datos con los valores recibidos por parámetro
    """

    hash = bcrypt.generate_password_hash(kwargs['password'].encode('utf-8'))
    kwargs['password'] = hash.decode('utf-8')
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user


def create_role(**kwargs):

    """
        Crea un objeto Role en la base de datos con los valores recibidos por parámetro
    """

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

def find_user_by_email(email):

    """Devuelve al usuario con el email dado"""

    return User.query.filter_by(email=email).first()