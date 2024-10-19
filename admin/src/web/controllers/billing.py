from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from core.auth import find_user_by_email
from src.core.payments import create_billing
from src.core.database import db
from src.core.payments.models.billing import Billing
from src.core.persons.models.person import Employee, JyA, Person
from src.core.payments.forms import BillingForm
from core.auth.auth import inject_user_permissions, permission_required
from datetime import datetime

bp = Blueprint('billing', __name__, url_prefix='/cobros')

def get_person_name_and_last_name(person_id):
    person = Person.query.filter_by(id=person_id).first()
    if person:
        return person.name + ' ' + person.last_name
    return None, None

@bp.route('/', methods=['GET', 'POST'])
@permission_required('billing_index')
@inject_user_permissions
def list_billings():

    """
        Esta funcion se encarga de listar los cobros realizados
        aplicando filtros de busqueda y realizando la paginacion.

    """

    order = request.args.get('order', 'asc')
    q = request.args.get('q', None)
    start_date_str = request.args.get('start_date', None)
    end_date_str = request.args.get('end_date', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    payment_method = request.args.get('payment_method', None)

    if order == 'desc':
        billings_query = Billing.query.order_by(Billing.payment_date.desc())
    else:
        billings_query = Billing.query.order_by(Billing.payment_date.asc())

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        billings_query = billings_query.filter(Billing.payment_date >= start_date)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        billings_query = billings_query.filter(Billing.payment_date <= end_date)

    billings_pagination = billings_query.paginate(page=page, per_page=per_page, error_out=False)
    billings = billings_pagination.items

    pos = 1
    for billing in billings:
        billing.employee_name = get_person_name_and_last_name(billing.employee_id)
        billing.jya_name = get_person_name_and_last_name(billing.jya_id)
        billing.pos = pos
        pos += 1

    if q:
        billings = [billing for billing in billings if q.lower() in billing.employee_name.lower()]
    
    if payment_method:
        billings = [billing for billing in billings if payment_method.lower() in billing.payment_method.lower()]

    return render_template('billing/billing_list.html', billings=billings, order=order, q=q, pagination=billings_pagination, payment_method=payment_method, start_date=start_date_str, end_date=end_date_str, form=BillingForm())

@bp.route('/crear', methods=['GET', 'POST'])
@permission_required('billing_new')
@inject_user_permissions
def new_billing():

    """
        Esta funcion se encarga de crear un nuevo cobro.
    """

    form = BillingForm()
    jya_list = JyA.query.all()
    employee_list = Employee.query.all()
    
    employee_actual = find_user_by_email(session.get('user'))

    if employee_actual.system_admin:
        employee_actual = None
    elif employee_actual in employee_list:
        employee_list = employee_list.remove(employee_actual)

    if form.validate_on_submit():
        create_billing(
            employee_id=form.employee_id.data,
            jya_id=form.jya_id.data,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            observation=form.observation.data
        )
        flash('Billing created successfully!', 'success')
        return redirect(url_for('billing.list_billings'))
    return render_template('billing/billing_new.html', form=form, jya_list=jya_list, employee_list=employee_list, employee_actual=employee_actual)

@bp.route('/cobro/<int:billing_id>', methods=['GET', 'POST'])
@permission_required('billing_show')
@inject_user_permissions
def show_billing(billing_id):

    """
        Esta funcion se encarga de mostrar un cobro en especifico asociado a un id.
    """

    billing = Billing.query.get(billing_id)
    billing.employee_name = get_person_name_and_last_name(billing.employee_id)
    billing.jya_name = get_person_name_and_last_name(billing.jya_id)
    return render_template('billing/billing_show.html', billing=billing)

@bp.route('/cobro/editar/<int:billing_id>', methods=['GET', 'POST'])
@permission_required('billing_edit')
@inject_user_permissions
def edit_billing(billing_id):

    """
        Esta funcion se encarga de editar un cobro en especifico asociado a un id.
    """

    billing = Billing.query.get(billing_id)
    form = BillingForm(obj=billing)
    jya_list = JyA.query.all()
    employee_list = Employee.query.all()

    if form.validate_on_submit():
        billing.employee_id = form.employee_id.data
        billing.jya_id = form.jya_id.data
        billing.amount = form.amount.data
        billing.payment_method = form.payment_method.data
        billing.observation = form.observation.data
        db.session.commit()
        flash('Billing updated successfully!', 'success')
        return redirect(url_for('billing.show_billing', billing_id=billing.id))
    return render_template('billing/billing_edit.html', form=form, jya_list=jya_list, employee_list=employee_list, billing=billing)

@bp.route('/eliminar/<int:billing_id>', methods=['POST'])
@permission_required('billing_delete')
@inject_user_permissions
def delete_billing(billing_id):

    """
    Esta funcion se encarga de eliminar un cobro en especifico asociado a un id.
    """

    billing = Billing.query.get(billing_id)
    if billing:
        db.session.delete(billing)
        db.session.commit()
        flash('Billing deleted successfully!', 'success')
    else:
        flash('Billing not found!', 'danger')
    return redirect(url_for('billing.list_billings'))