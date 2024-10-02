from flask import Blueprint, request
from flask import render_template
from src.core.auth.models.user import User
from src.core.database import db
from flask import current_app as app
from sqlalchemy import desc

bp = Blueprint('users', __name__, url_prefix='/users')

def showUsers(request):
    app.logger.info("Call to showUsers function")
    if(request.method == 'POST'):
        order_by = request.form.get('order_option', 'email_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'email_asc', type=str)
    app.logger.info("Call to order_by function with order_option: %s", order_by)
    order_mapping = {
        'email_asc': User.email,
        'email_desc': desc(User.email),
        'creation_date_asc': User.created_at,
        'creation_date_desc': desc(User.created_at)
    }
    order_criteria = order_mapping.get(order_by, User.email)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(order_criteria).paginate(
        page=page, per_page=2)
    context = {
        'users': users,
    }
    return context, page, order_by

@bp.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info("Call to index function")
    context, page, order_by = showUsers(request)
    app.logger.info("End of call to index function")
    return render_template('users.html', context=context, page=page, order_by=order_by)


@bp.route('/block', methods=['POST'])
def block_user():
    app.logger.info("Call to block_user function")
    user_email = request.form.get('user_email')
    user = User.query.filter_by(email=user_email).first()
    if user:
        user.is_blocked = not user.is_blocked
        app.logger.info("User %s is blocked: %s", user.email, user.is_blocked)
        db.session.commit()  
    context, page, order_by = showUsers(request)
    app.logger.info("End of call to block_user function")
    return render_template('users.html', context=context, page=page, order_by=order_by)
