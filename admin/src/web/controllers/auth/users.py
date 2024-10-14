from flask import Blueprint, flash, redirect, request,url_for
from flask import render_template
from core.auth import create_user, find_role_id_by_name, find_user_by_email, find_user_by_id, get_all_roles, update_role
from core.auth.forms import registryForm
from src.core.auth.models.user import User
from flask import current_app as app
from src.core.database import db
from sqlalchemy import desc
from src.core.auth.auth import inject_user_permissions, permission_required

bp = Blueprint('users', __name__, url_prefix='/users')

def showUsers(request):
    app.logger.info("Call to showUsers function")
    
    order_option = request.args.get('order_option', 'email_asc', type=str)
    app.logger.info("order_option: %s", order_option)
    
    # Map order options to actual column sorting
    order_mapping = {
        'email_asc': User.email,
        'email_desc': desc(User.email),
        'creation_date_asc': User.created_at,
        'creation_date_desc': desc(User.created_at)
    }
    order_criteria = order_mapping.get(order_option, User.email)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page=25
    
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
    users = query.order_by(order_criteria).paginate(page=page, per_page=per_page)
    
    context = {
        'users': users,
    }
    
    app.logger.info("End of call to showUsers function")
    return context, page, order_option, search, role, activity



@bp.route('/', methods=['GET', 'POST'])
@permission_required('user_index')
@inject_user_permissions
def index():
    app.logger.info("Call to index function")
    context, page, order_option, search, role, activity = showUsers(request)
    app.logger.info("End of call to index function")
    return render_template('users/user_list.html', context=context, page=page, order_option=order_option, search=search, role=role, activity=activity)



@bp.route('/crear', methods=['GET', 'POST'])
@permission_required('user_new')
@inject_user_permissions
def new_user():
    
    """
    Muestra la vista del registro, además valida los parametros, y guarda al usuario en la base de datos si
    se recibió el formulario y el mismo es válido.
    """
    app.logger.info("Call to registry_function")
    form = registryForm()
    app.logger.info("El formulario es valido: %s", form.validate_on_submit())

    if (form.validate_on_submit()):
        
        if (find_user_by_email(form.email.data)):
            app.logger.error("The following email is already registered: %s ", form.email.data)
            flash("Ya existe un usuario con el mail ingresado", "error")
            return redirect(url_for("users.new_user"))

        create_user(
            email = form.email.data,
            alias = form.alias.data,
            password = form.password.data,
            role_id = find_role_id_by_name(form.role.data),
        )
        app.logger.info("End of call to registry_function")
        flash("Usuario creado correctamente", "success")
        return render_template("home.html")
    
    return render_template("users/user_new.html", form=form)


@bp.route('/<int:id>', methods=['GET'])
@permission_required('user_show')
@inject_user_permissions
def show_user(id):
    user = find_user_by_id(id)
    roles = get_all_roles()
    context = {
        'user': user,
        'roles': roles
    }
    print(context)
    return render_template('users/user_show.html', context=context)


@bp.route('/update/<int:id>', methods=['GET'])
@permission_required('user_update')
@inject_user_permissions
def update_user(id):
    '''
        role = request.form.get('role')

    if user:
        user.is_blocked = not user.is_blocked
        app.logger.info("User %s is blocked: %s", user.email, user.is_blocked)
        db.session.commit()
    '''
    payment = User.query.get(id)
    form = registryForm()

    if form.payment_type.data != "Honorarios":
        beneficiary = None
    if form.validate_on_submit():
        payment.beneficiary = beneficiary
        payment.amount = form.amount.data
        payment.payment_type = form.payment_type.data
        payment.description = form.description.data
        db.session.commit()
        flash('Payment updated successfully!', 'success')
        return redirect(url_for('payment.show_payment', id=payment.id))

    
    user = find_user_by_id(id)
    roles = get_all_roles()
    context = {
        'user': user,
        'roles': roles,
        'form': form
    }
    return render_template('users/user_edit.html', context=context)