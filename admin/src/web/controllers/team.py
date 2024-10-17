from flask import Blueprint, render_template, redirect, request, url_for, flash
from src.core.auth.auth import inject_user_permissions, permission_required
from src.core.persons.models.person import Employee
from src.core.persons.forms import EmployeeForm
from src.core.database import db

bp = Blueprint('team', __name__, url_prefix='/empleados')

@bp.route('/')
@permission_required('team_index')
@inject_user_permissions
def list_team():
    employees = Employee.query.all()
    order=request.args.get('order', 'last_name_asc')
    q=request.args.get('q', None)
    page=request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page', 25, type=int)
    job_position=request.args.get('job_position', None)

    if order == 'last_name_asc':
        employees = Employee.query.order_by(Employee.last_name.asc())
    elif order == 'last_name_desc':
        employees = Employee.query.order_by(Employee.last_name.desc())
    elif order == 'name_asc':
        employees = Employee.query.order_by(Employee.name.asc())
    elif order == 'name_desc':
        employees = Employee.query.order_by(Employee.name.desc())
    elif order == 'date_asc':
        employees = Employee.query.order_by(Employee.start_date.asc())
    else:
        employees = Employee.query.order_by(Employee.start_date.desc())
    
    employees_pagination = employees.paginate(page=page, per_page=per_page, error_out=False)
    employees = employees_pagination.items

    if q:
        employees = [employee for employee in employees if q.lower() in employee.name.lower() or q.lower() in employee.last_name.lower() or q.lower() in employee.email.lower() or q in employee.DNI]

    if job_position:
        employees = [employee for employee in employees if job_position == employee.job_position]

    return render_template('team/team_list.html', employees=employees, order=order, q=q, pagination=employees_pagination, job_position=job_position,form=EmployeeForm())

@bp.route('/crear')
@permission_required('team_new')
@inject_user_permissions
def new_employee():
    return render_template('team/team_new.html')

@bp.route('/empleado/<int:id>')
@permission_required('team_show')
@inject_user_permissions
def show_employee(id):
    employee = Employee.query.get(id)
    return render_template('team/team_show.html', employee=employee)

@bp.route('/empleado/editar/<int:id>')
@permission_required('team_update')
@inject_user_permissions
def edit_employee(id):
    employee = Employee.query.get(id)
    return render_template('team/team_edit.html', employee=employee)

@bp.route('/empleado/eliminar/<int:id>', methods=['POST'])
@permission_required('team_destroy')
@inject_user_permissions
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('team.list_team'))