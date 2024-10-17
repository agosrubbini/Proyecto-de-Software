from flask import Blueprint, render_template, redirect, request, url_for, flash
from src.core.auth.auth import inject_user_permissions, permission_required
from src.core.persons.models.person import Employee
from src.core.persons.models.address import Address
from src.core.persons.models.healthcare_plan import HealthcarePlan
from src.core.persons.models.emergency_contact import EmergencyContact
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

@bp.route('/crear', methods=['GET', 'POST'])
@permission_required('team_new')
@inject_user_permissions
def new_employee():
    form = EmployeeForm()
    form.address_id.choices = [(address.id, address.string()) for address in Address.query.all()]
    form.emergency_contact.choices = [(emergency_contact.id, emergency_contact.name, emergency_contact.phone_number) for emergency_contact in EmergencyContact.query.all()]
    professions = ["Psicólogo", "Psicomotricista", "Médico", "Kinesiólogo", "Terapista Ocupacional", "Psicopedagogo", "Docente", "Profesor", "Fonoaudiólogo",
    "Veterinario", "Otro"]
    
    if form.validate_on_submit():
        if form.address_id.data:
            address = Address.query.get(form.address_id.data)
        else:
            address = Address(
                street=form.new_address.street.data,
                number=form.new_address.number.data,
                department=form.new_address.department.data,
                locality=form.new_address.locality.data,
                province=form.new_address.province.data,
                phone_number=form.new_address.phone_number.data
            )
            db.session.add(address)
            db.session.commit()
        
        healthcare_plan = HealthcarePlan(
            social_security=form.healthcare_plan.social_security.data,
            affiliate_number=form.healthcare_plan.affiliate_number.data,
            has_guardianship=form.healthcare_plan.has_guardianship.data,
            observation=form.healthcare_plan.observation.data
        )
        db.session.add(healthcare_plan)
        db.session.commit()
        
        if form.emergency_contact.data:
            emergency_contact = EmergencyContact.query.get(form.emergency_contact.data)
        else:
            emergency_contact = EmergencyContact(
                name=form.new_emergency_contact.name.data,
                phone_number=form.new_emergency_contact.phone_number.data
            )
            db.session.add(emergency_contact)
            db.session.commit()

        employee = Employee(
            name=form.name.data,
            last_name=form.last_name.data,
            DNI=form.dni.data,
            phone_number=form.phone_number.data,
            address_id=address.id,
            profession=form.profession.data,
            job_position=form.job_position.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            emergency_contact=emergency_contact.id,
            condition=form.condition.data,
            active=True,
            healthcare_plan_id_employee=healthcare_plan.id,
            email=form.email.data,
            birth_date=form.birth_date.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee created successfully!', 'success')
        return redirect(url_for('team.list'))

    return render_template('team/team_new.html', form=form, professions=professions)

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