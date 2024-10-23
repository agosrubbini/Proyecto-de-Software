from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.persons import (get_jya_users, find_address_by_id, find_jya_by_id, delete_jya_by_id, get_files_by_horseman_id, delete_file_by_id, 
                              create_JyA, create_file, updated_jya, find_file_by_title, find_file_by_id, updated_file, get_emergency_contacts, get_address, 
                              get_healthcare_plans, get_emergency_contact_by_id, get_healthcare_plan_by_id)
from src.core.institutions import get_schools, get_school_by_id
from src.core.persons.forms import registryFileForm, registryHorsemanForm
from src.core.auth.auth import inject_user_permissions, permission_required
from flask import current_app as app
from datetime import timedelta
from src.core.persons.models.file import File
from src.core.persons.models.person import JyA
from sqlalchemy import desc
import json
import io
from os import fstat


bp = Blueprint("horsemen_and_amazons", __name__, url_prefix="/users-jya")

def showHorsemen(request):
    
    """
        Muestra una lista paginada de jinetes y amazonas (JyA) con opciones de filtrado y ordenación.

        Esta función permite filtrar y ordenar los registros de jinetes y amazonas según varios criterios 
        como nombre, apellido, DNI y profesionales a cargo. Además, la lista se presenta de forma paginada.

        Parámetros:
        request (Request): El objeto de la solicitud HTTP que contiene los parámetros de la consulta. 
            - order_option (str): Opción de ordenación, como 'name_asc', 'name_desc', 'last_name_asc', o 'last_name_desc'.
            - page (int): El número de página para la paginación (predeterminado: 1).
            - name (str): Filtro por nombre del jinete/amazona (opcional).
            - last_name (str): Filtro por apellido del jinete/amazona (opcional).
            - dni (str): Filtro por DNI del jinete/amazona (opcional).
            - professionals (str): Filtro por nombre de los profesionales a cargo (opcional).

        Retorna:
        tuple: Una tupla que contiene:
            - horsemen (Pagination): Un objeto de paginación con los registros filtrados y ordenados de jinetes y amazonas.
            - page (int): El número de página actual.
            - order_by (str): La opción de ordenación seleccionada.
            - name (str): El filtro aplicado por nombre.
            - last_name (str): El filtro aplicado por apellido.
            - dni (str): El filtro aplicado por DNI.
            - attending_professionals (str): El filtro aplicado por profesionales a cargo.

    """
    # Determine the order option
    if request.method == 'POST':
        order_by = request.args.get('order_option', 'name_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'name_asc', type=str)

    app.logger.info("Call to showHorsemen function with order_option: %s", order_by)
    
    # Map order options to actual column sorting
    order_mapping = {
        'name_asc': JyA.name,
        'name_desc': desc(JyA.name),
        'last_name_asc': JyA.last_name,
        'last_name_desc': desc(JyA.last_name),
    }

    order_criteria = order_mapping.get(order_by, File.title)

    # Pagination
    page = request.args.get('page', 1, type=int)
    
    # Filtering options
    name = request.args.get('name', '', type=str)
    last_name = request.args.get('last_name', '', type=str)
    dni = request.args.get('dni', '', type=str)
    attending_professionals = request.args.get('professionals', '', type=str)

    app.logger.info("Name: %s,  Last Name: %s, DNI: %s, Profesionales: %s", name, last_name, dni, attending_professionals)

    # Build the query
    query = JyA.query
    
    if name:
        query = query.filter(JyA.name.like(f'%{name}%'))
    if last_name:
        query = query.filter(JyA.last_name.like(f'%{last_name}%'))
    if dni:
        query = query.filter(JyA.DNI.like(f'%{dni}%'))
    if attending_professionals:
        query = query.filter(JyA.attending_professionals.like(f'%{attending_professionals}%'))

    
    
    # Apply ordering and pagination
    horsemen = query.order_by(order_criteria).paginate(page=page, per_page=2)

    app.logger.info("End of call to showHorsemen function")

    return horsemen, page, order_by, name, last_name, dni, attending_professionals

def obtenerChoices(form):

    """ Esta función recibe el formulario de jinetes y amazonas y devuelve las instituciones, los contactos de emergencia, las obras sociales y las direcciones, 
        utilizadas como opciones de los distintos campos del formulario.


        Parámetros:
            - form (FlaskForm): Formulario de jinetes y amazonas.
        
    """
       
    schools = get_schools()

    emergency_contacts = get_emergency_contacts()

    healthcare_plans = get_healthcare_plans()

    addresses = get_address()

    # Asignar el id como value y la representación amigable como label
    form.address.choices = [(address.id, address.string()) for address in addresses]
    form.school.choices = [(school.id, school.name) for school in schools]
    form.emergency_contact_id_jya.choices = [(emergency_contact.id, emergency_contact.name) for emergency_contact in emergency_contacts]
    form.healthcare_plan_id_jya.choices = [(healthcare_plan.id, healthcare_plan.social_security) for healthcare_plan in healthcare_plans]

@bp.get("/")
@permission_required('jya_index')
@inject_user_permissions
def list_jya_users():

    """ 
        Muestra la vista del del listado de los jinetes y amazonas registrados en el sistema    
    """

    horsemen, page, order_by, name, last_name, dni, attending_professionals = showHorsemen(request)

    return render_template("horsemen_and_amazons/jya_users_list.html", users = horsemen, page=page, order_by=order_by, name=name, last_name=last_name, dni=dni, professionals=attending_professionals)

def showFiles(request):
   
    # Determine the order option
    if request.method == 'POST':
        order_by = request.args.get('order_option', 'title_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'title_asc', type=str)

    app.logger.info("Call to order_by function with order_option: %s", order_by)
    
    # Map order options to actual column sorting
    order_mapping = {
        'title_asc': File.title,
        'title_desc': desc(File.title),
        'date_asc': File.upload_date,
        'date_desc': desc(File.upload_date),
    }

    order_criteria = order_mapping.get(order_by, File.title)

    # Pagination
    page = request.args.get('page', 1, type=int)
    
    # Filtering options
    search = request.args.get('search', '', type=str)
    document_type = request.args.get('document_type', '', type=str)

    app.logger.info("Search: %s, Document_Type: %s", search, document_type)

    # Build the query
    query = File.query
    
    if search:
        query = query.filter(File.title.like(f'%{search}%'))
    if document_type and document_type != 'Selecciona un tipo':
        query = query.filter(File.document_type == document_type)
    
    # Apply ordering and pagination
    files = query.order_by(order_criteria).paginate(page=page, per_page=2)

    app.logger.info("End of call to order_by function")

    return files, page, order_by, search, document_type


@bp.get("/<int:user_id>")
@permission_required('jya_show')
@inject_user_permissions
def list_info_by_jya(user_id):

    """
        Esta función retorna la información del jinete o amazona asociado al id pasado por parámetro en la url.
    """
    
    app.logger.info("Call to index function")

    jya = find_jya_by_id(user_id)
    jya_address = find_address_by_id(jya.address_id).string()
    files = get_files_by_horseman_id(jya.id)
    jya_json = jya.to_dict(jya_address)
    files_json = []

    pagination, page, order_by, search, document_type = showFiles(request)

    if files:
        for file in files:    
            files_json.append(file.to_dict())

    context = {
        'pagination': pagination,
        'files': files_json,
        'user': jya_json,
        'id': user_id,
    }

    app.logger.info("End of call to index function")

    return render_template('horsemen_and_amazons/jya_user_info.html', context=context, page=page, order_by=order_by, search=search, document_type=document_type)

@bp.route("/add_jya", methods=['POST', 'GET'])
@permission_required('jya_new')
@inject_user_permissions
def add_horseman():

    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to add_horseman")
    form = registryHorsemanForm()

    obtenerChoices(form)

    app.logger.info("El formulario del jinete es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):
        
        """if (find_jya_by_id(user_id)):
            app.logger.error("The following jinete is already registered: %s ", form.title.data)
            flash("Ya existe un jinete con el id ingresado registrado en el sistema", "error")
            return redirect(url_for("horsemen_and_amazons.add_file", user_id=user_id)) """

        create_JyA(
            
            name = form.name.data,
            last_name = form.last_name.data,
            DNI = form.DNI.data,
            age = form.age.data,
            phone_number = form.phone_number.data,
            address_id = form.address.data,
            birthdate = form.birthdate.data,
            birth_place = form.birth_place.data,
            current_phone = form.current_phone.data,
            emergency_contact_id_jya = form.emergency_contact_id_jya.data,
            is_scholarshipped = form.is_scholarshipped.data,
            scholarship_percentage = form.scholarship_percentage.data,
            attending_professionals = form.attending_professionals.data,
            healthcare_plan_id_jya = form.healthcare_plan_id_jya.data,
            has_disability_certificate = form.has_disability_certificate.data,
            diagnosis = form.diagnosis.data,
            other_diagnosis = form.other_diagnosis.data,
            type_of_disability = form.type_of_disability.data,
            receives_family_allowance = form.receives_family_allowance.data,
            family_allowance = form.family_allowance.data,
            is_beneficiary_of_pension = form.is_beneficiary_of_pension.data,
            pension = form.pension.data,
            school_id = form.school.data,
        )

        flash("El jinete se ha creado correctamente", "success")
        return redirect(url_for('horsemen_and_amazons.list_jya_users'))
    
    else:
        print("Entre al false")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("horsemen_and_amazons/registry_horseman.html", form=form)

@bp.route("/edit_horseman/<user_id>", methods=['POST', 'GET'])
@permission_required('jya_update')
@inject_user_permissions
def edit_horseman(user_id):

    """
    Muestra la vista de edición del jinete, además valida los parametros, y guarda al jinete con los datos editados en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to edit_horseman")
    horseman = find_jya_by_id(user_id)
    
    form = registryHorsemanForm()
    
    obtenerChoices(form)
    
    address = find_address_by_id(horseman.address_id)
    emergency_contact = get_emergency_contact_by_id(horseman.emergency_contact_id_jya)
    healthcare_plan = get_healthcare_plan_by_id(horseman.healthcare_plan_id_jya)
    school = get_school_by_id(horseman.school_id)

 
    if horseman.scholarship_percentage is None:
        form.scholarship_percentage.data = " "
    if horseman.other_diagnosis is None:
        form.other_diagnosis.data = " "

    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):
        
        updated_jya(
            horseman,
            name = form.name.data,
            last_name = form.last_name.data,
            DNI = form.DNI.data,
            age = form.age.data,
            phone_number = form.phone_number.data,
            address_id = form.address.data,
            birthdate = form.birthdate.data,
            birth_place = form.birth_place.data,
            current_phone = form.current_phone.data,
            emergency_contact_id_jya = form.emergency_contact_id_jya.data,
            is_scholarshipped = form.is_scholarshipped.data,
            scholarship_percentage = form.scholarship_percentage.data,
            attending_professionals = form.attending_professionals.data,
            healthcare_plan_id_jya = form.healthcare_plan_id_jya.data,
            has_disability_certificate = form.has_disability_certificate.data,
            diagnosis = form.diagnosis.data,
            other_diagnosis = form.other_diagnosis.data,
            type_of_disability = form.type_of_disability.data,
            receives_family_allowance = form.receives_family_allowance.data,
            family_allowance = form.family_allowance.data,
            is_beneficiary_of_pension = form.is_beneficiary_of_pension.data,
            pension = form.pension.data,
            school_id = form.school.data,
        )

        flash("Jinete editado correctamente", "success")
        return redirect(url_for('horsemen_and_amazons.list_jya_users', user_id=user_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("horsemen_and_amazons/edit_horseman.html", form=form, user_id=user_id, horseman=horseman, address=address, healthcare_plan=healthcare_plan, emergency_contact=emergency_contact, school=school)

@bp.route("/delete_horseman/<int:user_id>", methods=['POST', 'GET'])
@permission_required('jya_destroy')
@inject_user_permissions
def delete_horseman(user_id):

    horseman = find_jya_by_id(user_id)
    delete_jya_by_id(user_id)

    flash('Jinete eliminado correctamente', 'success')

    # Redirigir a la vista order_by pasando el user_id y la opción de orden como query parameters
    return redirect(url_for('horsemen_and_amazons.list_jya_users'))

@bp.route("/<int:user_id>/delete_file/<int:file_id>", methods=['POST', 'GET'])
@permission_required('jya_destroy')
@inject_user_permissions
def delete_file(user_id, file_id):

    file = find_file_by_id(file_id)
    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']

    if (file.file_type == "Documento"):
        minio_client.remove_object(bucket_name, file.file_url)
    else:
        minio_client.remove_object(bucket_name, f"{file.title}_link.txt")
    delete_file_by_id(file_id)
    flash('Archivo eliminado correctamente', 'success')

    # Redirigir a la vista order_by pasando el user_id y la opción de orden como query parameters
    return redirect(url_for('horsemen_and_amazons.list_info_by_jya', user_id=user_id))
   
@bp.route("/<int:user_id>/add_file", methods=['POST', 'GET'])
@permission_required('jya_new')
@inject_user_permissions
def add_file(user_id):

    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to add_file")
    form = registryFileForm()

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']
    
    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):
        
        if (find_file_by_title(form.title.data)):
            app.logger.error("The following title is already registered: %s ", form.title.data)
            flash("Ya existe un archivo con el titutlo ingresado", "error")
            return redirect(url_for("horsemen_and_amazons.add_file", user_id=user_id))

        if form.file_type.data == 'Documento':
            # Manejar el archivo
            file = request.files['file_url']

            size = fstat(file.fileno()).st_size

            minio_client.put_object(bucket_name,file.filename,file,size,content_type=file.content_type)

            create_file(
                file_url = file.filename,
                file_type = form.file_type.data,
                document_type = form.document_type.data,
                title = form.title.data,
                horsemen_and_amazons_id = user_id,
            )

            
        
        elif form.file_type.data == 'Link':
            # Manejar el enlace
            link = form.link_url.data

            link_filename = f"{form.title.data}_link.txt"
            link_content = link.encode('utf-8')  # Convertir el enlace a bytes

                    # Subir a MinIO
            minio_client.put_object(
            bucket_name,
            link_filename,
            io.BytesIO(link_content),  # Envolver los bytes en un stream
            len(link_content),  # Especificar el tamaño del archivo
            content_type='text/plain',  
            )

                    # Guardar los metadatos en la base de datos
            create_file(
                file_url=link,
                file_type=form.file_type.data,
                document_type=form.document_type.data,
                title=form.title.data,
                horsemen_and_amazons_id=user_id,
            )

        flash("El archivo se ha creado correctamente", "success")
        return redirect(url_for('horsemen_and_amazons.list_info_by_jya', user_id=user_id))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("horsemen_and_amazons/registry_file.html", form=form, user_id=user_id)

@bp.route("/<int:user_id>/download_file/<file_id>", methods=['GET'])
@permission_required('jya_new')
@inject_user_permissions
def download_file(user_id, file_id):
    # Obtener el archivo de la base de datos usando el ID
    file = find_file_by_id(file_id)  # Función que obtenga el archivo desde la base de datos
    

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

@bp.route("/<int:user_id>/edit_file/<file_id>", methods=['POST', 'GET'])
@inject_user_permissions
def edit_file(user_id, file_id):

    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    app.logger.info("Call to add_file")
    file = find_file_by_id(file_id)
    
    form = registryFileForm()

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']
    
    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):

        if form.file_type.data == 'Documento':

            # Manejar el archivo
            new_file = request.files['file_url']
            
            if new_file:

                # Obtener el tamaño del archivo
                new_file.seek(0, 2)
                size = new_file.tell()
                new_file.seek(0)

                minio_client.put_object(bucket_name,new_file.filename,new_file,size,content_type=new_file.content_type)

                updated_file(
                    file, 
                    file_url = new_file.filename, 
                    file_type = form.file_type.data,  
                    document_type = form.document_type.data,
                    title = form.title.data,
                )
                
            else:
                flash("No se actualizo el contenido del documento, porque no se ingreso un nuevo archivo", "info")
                    
        elif form.file_type.data == 'Link':

            # Manejar el enlace
            link = form.link_url.data

            link_filename = f"{form.title.data}_link.txt"
            link_content = link.encode('utf-8')  # Convertir el enlace a bytes

            # Subir a MinIO
            minio_client.put_object(
            bucket_name,
            link_filename,
            io.BytesIO(link_content),  # Envolver los bytes en un stream
            len(link_content),  # Especificar el tamaño del archivo
            content_type='text/plain',  
            )

            #Actualizar el archivo 
            updated_file(
                file,
                file_url = link, 
                file_type = form.file_type.data,  
                document_type = form.document_type.data,
                title = form.title.data,
            )

        flash("Archivo editado correctamente", "success")
        return redirect(url_for('horsemen_and_amazons.list_info_by_jya', user_id=user_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("horsemen_and_amazons/edit_file.html", form=form, user_id=user_id, file=file)
