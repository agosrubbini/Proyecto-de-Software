from flask import Blueprint
from flask import render_template
from flask import url_for
from src.core.auth.models.user import User
from src.core.auth.models.roles_and_permissions import Role

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def list_users():
    users = None
    users = User.query.all()
    roles = Role.query.all()
    context = {
        'users': users,
        'roles': roles
    }
    return render_template('users.html', context=context)