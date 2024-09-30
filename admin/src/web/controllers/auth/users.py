from flask import Blueprint, request
from flask import render_template
from src.core.auth.models.user import User
from src.core.database import db
from sqlalchemy import desc

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def list_users():
    users = None
    users = User.query.order_by(User.email).all()
    context = {
        'users': users,
    }
    return render_template('users.html', context=context)


@bp.route('/block', methods=['POST'])
def block_user():
    user_email = request.form.get('user_email')
    user = User.query.filter_by(email=user_email).first()
    if user:
        user.is_blocked = not user.is_blocked 
        db.session.commit()  
    users = None
    users = User.query.order_by(User.email).all()
    context = {
        'users': users,
    }
    return render_template('users.html', context=context)


#TODO no funciona el de fecha de creacion
@bp.route('/order', methods=['POST'])
def order_by():
    order_by = request.form.get('order_option')
    users = None
    if order_by == 'email_asc':
        users = User.query.order_by(User.email).all()
    elif order_by == 'email_desc':
        users = User.query.order_by(desc(User.email)).all()
    if order_by == 'creation_date_asc':
        users = User.query.order_by(User.created_at).all()
    elif order_by == 'creation_date_desc':
        users = User.query.order_by(desc(User.created_at)).all()
    context = {
        'users': users,
    }
    return render_template('users.html', context=context)