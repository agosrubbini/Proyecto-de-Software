from flask import Blueprint, request, flash, session, redirect, render_template, url_for
from flask import render_template, redirect, url_for
from src.core.horses.models.horse import Horse
from src.core.database import db
from src.core.horses.forms import create_horse_Form, registryFileForm
from flask import current_app as app
from src.core.horses.__init__ import create_horse, find_horse_by_id, get_files_by_horse_id, find_file_by_id, delete_file_by_id, get_horses, create_file, find_file_by_title, updated_file
from sqlalchemy import desc
from src.core.persons import Employee
from src.core.horses.models.horses_file import Horse_file
from datetime import timedelta
import json
import io

bp = Blueprint('horses', __name__, url_prefix='/horses')

def show_horses(request):
   
    # Determine the order option
    if request.method == 'POST':
        order_by = request.args.get('order_option', 'name_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'name_asc', type=str)
    

    # Map order options to actual column sorting
    order_mapping = {
        'name_asc': Horse.name,
        'name_desc': desc(Horse.name),
        'birth_date_asc': Horse.date_of_birth,
        'birth_date_desc': desc(Horse.date_of_birth),
        'entry_date_asc': Horse.date_of_entry,
        'entry_date_desc': desc(Horse.date_of_entry),
    }

    order_criteria = order_mapping.get(order_by, Horse_file.title)

    # Pagination
    page = request.args.get('page', 1, type=int)
    
    # Filtering options
    name = request.args.get('name', '', type=str)
    type_jya_assigned = request.args.get('type_jya_assigned', '', type=str)


    # Build the query
    query = Horse.query
    
    if name:
        query = query.filter(Horse.name.like(f'%{name}%'))
    if type_jya_assigned:
        query = query.filter(Horse.type_jya_assigned.contains([type_jya_assigned]))
    
    # Apply ordering and pagination
    horse = query.order_by(order_criteria).paginate(page=page, per_page=2)

    return horse, page, order_by, name, type_jya_assigned

@bp.get("/")
#@inject_user_permissions
def list_horses():

    """
        Esta función retorna el listado con los caballos registrados en el sistema.
    """

    horse, page, order_by, name, type_jya_assigned = show_horses(request)

    return render_template ("ecuestre/horses.html", horses = horse, page=page, order_by=order_by, name=name, type_jya_assigned=type_jya_assigned)


@bp.route('/create', methods=['GET', 'POST'])
def create_horse_view():
    form = create_horse_Form()

    form.employees.choices = [(e.id, e.name) for e in Employee.query.all()]  # Cargar empleados
    
    if form.validate_on_submit():
        try:
            type_jya_assigned=[]
            if form.type_jya_hipoterapia.data:
                type_jya_assigned.append ("Hipoterapia")
            if form.type_jya_monta_terapeutica.data:
                type_jya_assigned.append ("Monta Terapeutica")
            if form.type_jya_dea.data:
                type_jya_assigned.append ("Deporte Ecuestre Adaptado")
            if form.type_jya_ar.data:
                type_jya_assigned.append ("Actividades Recreativas")
            if form.type_jya_equitacion.data:
                type_jya_assigned.append ("Equitacion")
            
            
            new_horse = Horse(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                gender=form.gender.data,
                race=form.race.data,
                fur=form.fur.data,
                purchase_or_donation=form.purchase_or_donation.data,
                date_of_entry=form.date_of_entry.data,
                sede=form.sede.data,
                type_jya_assigned=type_jya_assigned,
            )


            for empleado_id in form.employees.data:
                empleado = Employee.query.get(empleado_id)
                new_horse.employees.append(empleado)


            db.session.add(new_horse)
            db.session.commit()
            
            app.logger.info("Caballo creado exitosamente: %s", form.name.data)#controlar
            flash("Caballo creado exitosamente", "success")
            return redirect(url_for('horses.list_horses'))  # Redirigir a la lista de caballos
        except Exception as e:
            app.logger.error("Error al crear el caballo: %s", str(e))
            flash("Ocurrió un error al crear el caballo", "error")

 
    context = {
        'form': form,  # Pasa el formulario para que esté disponible en la plantilla
        'horses': Horse.query.order_by(Horse.name).all()  # Puedes cargar los caballos aquí si deseas
    }

    return render_template('ecuestre/create_horse.html', context=context)  # Renderizar el formulario



def show_files(request):
   
    # Determine the order option
    if request.method == 'POST':
        order_by = request.args.get('order_option', 'title_asc', type=str)
    else:
        order_by = request.args.get('order_option', 'title_asc', type=str)

    app.logger.info("Call to order_by function with order_option: %s", order_by)
    
    # Map order options to actual column sorting
    order_mapping = {
        'title_asc': Horse_file.title,
        'title_desc': desc(Horse_file.title),
        'date_asc': Horse_file.upload_date,
        'date_desc': desc(Horse_file.upload_date),
    }

    order_criteria = order_mapping.get(order_by, Horse_file.title)

    # Pagination
    page = request.args.get('page', 1, type=int)
    
    # Filtering options
    search = request.args.get('search', '', type=str)
    document_type = request.args.get('document_type', '', type=str)

    app.logger.info("Search: %s, Document_Type: %s", search, document_type)

    # Build the query
    query = Horse_file.query
    
    if search:
        query = query.filter(Horse_file.title.like(f'%{search}%'))
    if document_type and document_type != 'Selecciona un tipo':
        query = query.filter(Horse_file.document_type == document_type)
    
    # Apply ordering and pagination
    files = query.order_by(order_criteria).paginate(page=page, per_page=2)

    return files, page, order_by, search, document_type


@bp.get("/<int:horse_id>")
#@inject_user_permissions
def list_info_by_id(horse_id):

    """
        Esta función retorna la información del caballo asociado al id pasado por parámetro en la url.
    """

    horse = find_horse_by_id(horse_id)
    files = get_files_by_horse_id(horse_id)
    horse_json = horse.to_dict()  
    files_json = []

    files, page, order_by, search, document_type = show_files(request)

    if files:
        for file in files:    
            files_json.append(file.to_dict())

    context = {
        'pagination': files,
        'files': files_json,
        'horse': horse_json,
        'id': horse_id,
    }

    
    return render_template('ecuestre/horses_info.html', context=context, page=page, order_by=order_by, search=search, document_type=document_type)


@bp.route("/<int:horse_id>/delete_file/<int:file_id>", methods=['POST', 'GET'])
#@inject_user_permissions
def delete_file(horse_id, file_id):

    print("Este es el file id", file_id)
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
    return redirect(url_for('horses.list_info_by_id', horse_id=horse_id))


@bp.route("/<int:horse_id>/add_file", methods=['POST', 'GET'])
#@inject_user_permissions
def add_file(horse_id):

    """
    Muestra la vista del registro,  valida los parametros, y guarda al archivo en la base de datos si
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
            return redirect(url_for("horses.add_file", horse_id=horse_id))

        if form.file_type.data == 'Documento':
            # Manejar el archivo
            file = request.files['file_url']

            # Obtener el tamaño del archivo
            file.seek(0, 2)  # Mover el cursor al final para obtener el tamaño
            size = file.tell()
            file.seek(0)  # Volver al inicio del archivo

            minio_client.put_object(bucket_name,file.filename,file,size,content_type=file.content_type)

            create_file(
                file_url = file.filename,
                file_type = form.file_type.data,
                document_type = form.document_type.data,
                title = form.title.data,
                horse_id = horse_id,
            )

            
        
        elif form.file_type.data == 'Link':
            # Manejar el enlace
            link = form.link_url.data

            print(link)

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
                horse_id=horse_id,
            )

        flash("El archivo se ha creado correctamente", "success")
        return redirect(url_for('horses.list_info_by_id', horse_id=horse_id))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("ecuestre/registry_file.html", form=form, horse_id=horse_id)


@bp.route("/<int:horse_id>/download_file/<file_id>", methods=['GET'])
#@inject_user_permissions
def download_file(horse_id, file_id):
    # Obtener el archivo de la base de datos usando el ID
    file = find_file_by_id(file_id)

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

@bp.route("/<int:horse_id>/edit_file/<file_id>", methods=['POST', 'GET'])
#@inject_user_permissions
def edit_file(horse_id, file_id):

    """
    Muestra la vista del registro, además valida los parametros, y guarda al archivo en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

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
                new_file.seek(0, 2)  # Mover el cursor al final para obtener el tamaño
                size = new_file.tell()
                new_file.seek(0)  # Volver al inicio del archivo

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

            print(link)

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

            updated_file(
                file,
                file_url = link, 
                file_type = form.file_type.data,  
                document_type = form.document_type.data,
                title = form.title.data,
            )

        flash("Archivo editado correctamente", "success")
        return redirect(url_for('horses.list_info_by_id', horse_id=horse_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("ecuestre/edit_file.html", form=form, horse_id=horse_id, file=file)

#actualizar
#eliminar
#asociar entrenadores y conductores
#busqueda