
from flask import Blueprint, render_template, request
from src.core.database import db
from flask import current_app as app
from core.auth import find_user_by_id, get_all_roles, update_role
from core.auth.auth import inject_user_permissions, permission_required


bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/<int:id>', methods=['GET'])
@permission_required('user_index')
@inject_user_permissions
def index(id):
    user = find_user_by_id(id)
    roles = get_all_roles()
    context = {
        'user': user,
        'roles': roles
    }
    print(context)
    return render_template('profile.html', context=context)

@bp.route('/<int:id>/block', methods=['POST'])
@permission_required('update_user')
@inject_user_permissions
def block_user(id):
    app.logger.info("Call to block_user function")
    user = find_user_by_id(id)
    roles = get_all_roles()
    if user:
        user.is_blocked = not user.is_blocked
        app.logger.info("User %s is blocked: %s", user.email, user.is_blocked)
        db.session.commit()  
    context = {
        'user': user,
        'roles': roles
    }
    app.logger.info("End of call to block_user function")
    return render_template('profile.html', context=context)

@bp.route('/<int:id>/update', methods=['POST'])
@permission_required('update_user')
@inject_user_permissions
def change_role(id):
    app.logger.info("Call to change_role function")
    role = request.form.get('role')
    user = find_user_by_id(id)
    roles = get_all_roles()
    if user:
        update_role(user, role)
        app.logger.info("User %s role_id changed to: %s", user.email, role) 
    context = {
        'user': user,
        'roles': roles
    }
    app.logger.info("End of call to change_role function")
    return render_template('profile.html', context=context)