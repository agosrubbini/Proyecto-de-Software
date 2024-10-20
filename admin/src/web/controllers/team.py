from datetime import timedelta
from os import fstat
from flask import Blueprint, current_app as app, render_template, redirect, request, url_for, flash
from src.core.persons import create_employee_file, delete_employee_file_by_id, find_address_by_id, find_employee_by_id, find_employee_file_by_id, find_employee_file_by_title, get_emergency_contact_by_id, get_files_by_employee_id, get_healthcare_plan_by_id, updated_employee_file
from src.core.auth.auth import inject_user_permissions, permission_required
from src.core.persons.models.person import Employee, Person
from src.core.persons.models.address import Address
from src.core.persons.models.healthcare_plan import HealthcarePlan
from src.core.persons.models.emergency_contact import EmergencyContact
from src.core.persons.forms import EmployeeFileForm, EmployeeForm
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
    professions = ["Psicólogo", "Psicomotricista", "Médico", "Kinesiólogo", "Terapista Ocupacional", "Psicopedagogo", "Docente", "Profesor", "Fonoaudiólogo", "Veterinario", "Otro"]
    
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
            emergency_contact_id_employee=emergency_contact.id,
            condition=form.condition.data,
            active=True,
            healthcare_plan_id_employee=healthcare_plan.id,
            email=form.email.data,
            birth_date=form.birth_date.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee created successfully!', 'success')
        return redirect(url_for('team.list_team'))

    return render_template('team/team_new.html', form=form, professions=professions)

@bp.route('/empleado/<int:id>')
@permission_required('team_show')
@inject_user_permissions
def show_employee(id):
    """
    Esta función retorna la información del jinete o amazona asociado al id pasado por parámetro en la url.
    """
    
    app.logger.info("Call to index function")

    employee = find_employee_by_id(id)
    employee_address = find_address_by_id(employee.address_id).string()
    employee_healthcare_plan = get_healthcare_plan_by_id(employee.healthcare_plan_id_employee)
    employee_emergency_contact = get_emergency_contact_by_id(employee.emergency_contact_id_employee)
    files = get_files_by_employee_id(employee.id)
    employee_json = employee.to_dict(employee_address, employee_healthcare_plan, employee_emergency_contact)
    employee_json['active'] = 'Activo' if employee.active else 'Inactivo'

    files_json = []
    if files:
        for file in files:    
            files_json.append(file.to_dict())

    context = {
        'files': files_json,
        'user': employee_json,
        'id': id,
    }

    app.logger.info("End of call to index function")

    return render_template('team/team_show.html', context=context)

@bp.route('/empleado/editar/<int:id>', methods=['GET', 'POST'])
@permission_required('team_update')
@inject_user_permissions
def edit_employee(id):
    employee = Employee.query.get(id)
    employee.healthcare_plan = HealthcarePlan.query.get(employee.healthcare_plan_id_employee)
    employee.start_date = employee.start_date.strftime('%Y-%m-%d')
    employee.birth_date = employee.birth_date.strftime('%Y-%m-%d')
    form = EmployeeForm()
    form.address_id.choices = [(address.id, address.string()) for address in Address.query.all()]
    form.emergency_contact.choices = [(emergency_contact.id, emergency_contact.name, emergency_contact.phone_number) for emergency_contact in EmergencyContact.query.all()]
    professions = ["Psicólogo", "Psicomotricista", "Médico", "Kinesiólogo", "Terapista Ocupacional", "Psicopedagogo", "Docente", "Profesor", "Fonoaudiólogo", "Veterinario", "Otro"]

    if form.validate_on_submit():
        # Campos de address
        if employee.address_id != form.address_id.data:
            address = Address.query.get(form.address_id.data)
            employee.address_id = address.id
        elif form.new_address.street.data:
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
            employee.address_id = address.id

        # Campos de healthcare_plan
        employee.healthcare_plan.social_security = form.healthcare_plan.social_security.data
        employee.healthcare_plan.affiliate_number = form.healthcare_plan.affiliate_number.data
        employee.healthcare_plan.has_guardianship = form.healthcare_plan.has_guardianship.data
        employee.healthcare_plan.observation = form.healthcare_plan.observation.data
        
        print(form.emergency_contact.data)
        print(form.new_emergency_contact.name)
        print(form.new_emergency_contact.phone_number)

        # Campos de emergency_contact
        if employee.emergency_contact_id_employee != form.emergency_contact.data:
            emergency_contact = EmergencyContact.query.get(form.emergency_contact.data)
            employee.emergency_contact_id_employee = emergency_contact.id
        elif form.new_emergency_contact.name != "":
            emergency_contact = EmergencyContact(
                name=form.new_emergency_contact.name,
                phone_number=form.new_emergency_contact.phone_number.data
            )
            db.session.add(emergency_contact)
            db.session.commit()
            employee.emergency_contact_id_employee = emergency_contact.id

        # Campos de employee
        employee.name = form.name.data
        employee.last_name = form.last_name.data
        employee.DNI = form.dni.data
        employee.phone_number = form.phone_number.data
        employee.profession = form.profession.data
        employee.job_position = form.job_position.data
        employee.start_date = form.start_date.data
        employee.end_date = form.end_date.data
        employee.condition = form.condition.data
        employee.active = form.active.data
        employee.email = form.email.data
        employee.birth_date = form.birth_date.data

        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('team.list_team'))
    
    return render_template('team/team_edit.html', form=form, employee=employee, professions=professions)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@permission_required('team_destroy')
@inject_user_permissions
def delete_employee(id):
    print('Employee id:', id)
    employee = Employee.query.get(id)
    if not employee:
        print('Employee not found', 'error')
    else:
        db.session.delete(employee)
        db.session.commit()
        print('Employee deleted successfully!', 'success')
    # Que pasa cuando quiero eliminar un empleado que tiene billings asociados?
    # Empleado con archivos se borran ambos.
    # Que otro caso existe?
    return redirect(url_for('team.list_team'))

@bp.route('/empleado/<int:id>/add_file', methods=['POST', 'GET'])
@permission_required('team_update')
@inject_user_permissions    
def add_file(id):
    
    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to add_file")
    form = EmployeeFileForm()

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']
    
    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):
            #Tengo que hacer esto pero para empleado        
        if (find_employee_file_by_title(form.title.data)):
            app.logger.error("The following title is already registered: %s ", form.title.data)
            flash("Ya existe un archivo con el titutlo ingresado", "error")
            return redirect(url_for("team.add_file", id=id))

        # Manejar el archivo
        file = request.files['file_url']

        size = fstat(file.fileno()).st_size

        minio_client.put_object(bucket_name,file.filename,file,size,content_type=file.content_type)

        create_employee_file(
            file_url = file.filename,
            title = form.title.data,
            document_type = form.document_type.data,
            employee_id = id,
        )

        flash("El archivo se ha creado correctamente", "success")
        return redirect(url_for('team.show_employee', id=id))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("team/file_new.html", form=form, id=id)

@bp.route('/empleado/<int:id>/archivo/<int:file_id>/eliminar', methods=['POST', 'GET'])
@permission_required('team_delete_file')
@inject_user_permissions
def delete_file(id, file_id):
    file = find_employee_file_by_id(file_id)
    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']

    minio_client.remove_object(bucket_name, file.file_url)
    delete_employee_file_by_id(file_id)
    flash('Archivo eliminado correctamente', 'success')

    # Redirigir a la vista order_by pasando el user_id y la opción de orden como query parameters
    return redirect(url_for('team.show_employee', id=id))

@bp.route('/empleado/<int:user_id>/archivo/<int:file_id>/descargar', methods=['GET'])
@permission_required('team_download_file')
@inject_user_permissions
def download_file(user_id, file_id):
    # Obtener el archivo de la base de datos usando el ID
    file = find_employee_file_by_id(file_id)  # Función que obtenga el archivo desde la base de datos
    

    # Configurar MinIO
    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']

    # Parámetros adicionales para forzar la descarga
    download_headers = {
        'response-content-disposition': f'attachment; filename="{file.file_url}"'
    }

    presigned_url = minio_client.presigned_get_object(bucket_name, file.file_url, expires=timedelta(hours=1), response_headers=download_headers)

        # Redirigir al usuario al enlace de descarga
    return redirect(presigned_url)

@bp.route('/empleado/<int:user_id>/archivo/<int:file_id>/editar', methods=['GET', 'POST'])
@permission_required('team_view_file')
@inject_user_permissions
def edit_file(user_id, file_id):
    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to add_file")
    file = find_employee_file_by_id(file_id)
    
    form = EmployeeFileForm()

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']
    
    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):

        # Manejar el archivo
        new_file = request.files['file_url']
        
        if new_file:

            # Obtener el tamaño del archivo
            size = fstat(file.fileno()).st_size

            minio_client.put_object(bucket_name,new_file.filename,new_file,size,content_type=new_file.content_type)

            updated_employee_file(
                file, 
                file_url = new_file.filename, 
                file_type = form.file_type.data,  
                document_type = form.document_type.data,
                title = form.title.data,
            )
            
        else:
            flash("No se actualizo el contenido del documento, porque no se ingreso un nuevo archivo", "info")

        flash("Archivo editado correctamente", "success")
        return redirect(url_for('team.show_employee', id=user_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("team/file_edit.html", form=form, user_id=user_id, file=file)
