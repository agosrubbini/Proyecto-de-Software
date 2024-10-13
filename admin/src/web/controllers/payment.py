from datetime import datetime
from src.core.payments import create_payment
from src.core.database import db 
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src.core.auth import find_user_by_email
from src.core.auth.auth import inject_user_permissions, permission_required
from src.core.payments.forms import PaymentForm
from src.core.persons.models.person import Employee
from flask import current_app as app
from src.core.payments.models.payment import Payment
from web.controllers.billing import get_person_name_and_last_name


bp = Blueprint('payment', __name__, url_prefix='/pagos')

@bp.route('/', methods=['GET', 'POST'])
@permission_required('payment_index')
@inject_user_permissions
def list_payments():
    order = request.args.get('order', 'asc')
    start_date_str = request.args.get('start_date', None)
    end_date_str = request.args.get('end_date', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    payment_method = request.args.get('payment_method', None)

    if order == 'desc':
        payments_query = Payment.query.order_by(Payment.payment_date.desc())
    else:
         payments_query = Payment.query.order_by(Payment.payment_date.asc())

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        payments_query =  payments_query.filter(Payment.payment_date >= start_date)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        payments_query =  payments_query.filter(Payment.payment_date <= end_date)

    payments_pagination =  payments_query.paginate(page=page, per_page=per_page, error_out=False)
    payments = payments_pagination.items

    pos = 1
    for payment in payments:
        payment.employee_name = get_person_name_and_last_name(payment.beneficiary)
        payment.pos = pos
        pos += 1
    
    if payment_method:
        payments = [payment for payment in payments if payment_method.lower() in payment.payment_type.lower()]

    return render_template('payment/payment_list.html', payments=payments, order=order, pagination=payments_pagination, payment_method=payment_method, start_date=start_date_str, end_date=end_date_str)
    

@bp.route('/crear', methods=['GET', 'POST'])
@permission_required('payment_new')
@inject_user_permissions
def new_payment():
    app.logger.info("Call to new_payment function")
    form = PaymentForm()
    employee_list = Employee.query.all()
    
    employee_actual = find_user_by_email(session.get('user'))

    if employee_actual.system_admin:
        employee_actual = None
    elif employee_actual in employee_list:
        employee_list = employee_list.remove(employee_actual)

        
    if not form.validate_on_submit():
        app.logger.error("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                app.logger.error("Error in the %s field - %s", field, error)

    if form.validate_on_submit():
        create_payment(
            beneficiary=form.beneficiary.data,
            amount=form.amount.data,
            payment_date=form.payment_date.data,
            payment_type=form.payment_type.data,
            description=form.description.data
        )
        flash('Payment created successfully!', 'success')
        app.logger.info('Payment created successfully!')
        return redirect(url_for('payment.list_payments'))
    app.logger.info("End of call to new_payment function")
    return render_template('payment/payment_new.html', form=form, employee_list=employee_list, employee_actual=employee_actual)

@bp.route('/<int:id>', methods=['GET', 'POST'])
@permission_required('payment_show')
@inject_user_permissions
def show_payment(id):
    payment = Payment.query.get(id)
    payment.employee_name = get_person_name_and_last_name(payment.beneficiary)
    return render_template('payment/payment_show.html', payment=payment)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@permission_required('payment_update')
@inject_user_permissions
def edit_payment(id):
    payment = Payment.query.get(id)
    form = PaymentForm(obj=payment)
    employee_list = Employee.query.all()

    if form.validate_on_submit():
        payment.beneficiary = form.beneficiary.data
        payment.amount = form.amount.data
        payment.payment_type = form.payment_type.data
        payment.description = form.description.data
        db.session.commit()
        flash('Payment updated successfully!', 'success')
        return redirect(url_for('payment.show_payment', id=payment.id))
    return render_template('payment/payment_edit.html', form=form, employee_list=employee_list, payment=payment)






'''
@bp.route('/crear', methods=['GET', 'POST'])
@permission_required('payment_destroy')
@inject_user_permissions
def delete_payment(id):
    pass
'''