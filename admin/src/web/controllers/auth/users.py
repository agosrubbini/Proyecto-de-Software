from flask import Blueprint, request
from flask import render_template
from src.core.auth.models.user import User
from src.core.database import db
from flask import current_app as app
from sqlalchemy import desc
from src.core.auth.auth import permission_required

bp = Blueprint('users', __name__, url_prefix='/users')

def showUsers(request):
    app.logger.info("Call to showUsers function")
    
    # Determine the order option
    if request.method == 'POST':
        order_by = request.form.get('order_option', 'email_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'email_asc', type=str)
    app.logger.info("Call to order_by function with order_option: %s", order_by)
    
    # Map order options to actual column sorting
    order_mapping = {
        'email_asc': User.email,
        'email_desc': desc(User.email),
        'creation_date_asc': User.created_at,
        'creation_date_desc': desc(User.created_at)
    }
    order_criteria = order_mapping.get(order_by, User.email)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    
    # Filtering options
    search = request.args.get('search', '', type=str)
    role = request.args.get('role', '', type=int)
    activity = request.args.get('activity', '', type=str)
    app.logger.info("Search: %s, Role: %s, Activity: %s", search, role, activity)
    # Build the query
    query = User.query
    
    if search:
        query = query.filter(User.email.like(f'%{search}%'))
    if role:
        query = query.filter(User.role_id == role)
    if activity:
        is_active = True if activity == "active" else False
        app.logger.info("Activity: %s", is_active)
        query = query.filter(User.active == is_active)
    
    # Apply ordering and pagination
    users = query.order_by(order_criteria).paginate(page=page, per_page=2)
    
    context = {
        'users': users,
    }
    
    app.logger.info("End of call to showUsers function")
    return context, page, order_by, search, role, activity



@bp.route('/', methods=['GET', 'POST'])
@permission_required('team_index')
def index():
    app.logger.info("Call to index function")
    context, page, order_by, search, role, activity = showUsers(request)
    app.logger.info("End of call to index function")
    return render_template('users.html', context=context, page=page, order_by=order_by, search=search, role=role, activity=activity)



@bp.route('/block', methods=['POST'])
@permission_required('team_update')
def block_user():
    app.logger.info("Call to block_user function")
    user_email = request.form.get('user_email')
    user = User.query.filter_by(email=user_email).first()
    if user:
        user.is_blocked = not user.is_blocked
        app.logger.info("User %s is blocked: %s", user.email, user.is_blocked)
        db.session.commit()  
    context, page, order_by, search, role, activity = showUsers(request)
    app.logger.info("End of call to block_user function")
    return render_template('users.html', context=context, page=page, order_by=order_by, search=search, role=role, activity=activity)

@bp.route('/profile', methods=['GET'])
@permission_required('team_update')
def profile():
    users = User.query.all()
    context = {
        'users': users,
    }
    return render_template('profile.html', context=context)