from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.persons import get_jya_users, find_adress_by_id, find_jya_by_id, get_files_by_horseman_id, delete_file_by_id, create_JyA, create_file, find_file_by_title, find_file_by_id, updated_file
from src.core.persons.forms import registryFileForm
from flask import current_app as app
from datetime import timedelta
from src.core.persons.models.file import File
from src.core.persons.models.person import JyA
from sqlalchemy import desc
import json
import io
from src.core.auth.auth import inject_user_permissions


bp = Blueprint("horsemen_and_amazons", __name__, url_prefix="/users-jya")

def showHorsemen(request):
   
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

@bp.get("/")
@inject_user_permissions
def list_jya_users():

    """
        Esta función retorna el listado con los jinetes y amazonas registrados en el sistema.
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
@inject_user_permissions
def list_info_by_jya(user_id):

    """
        Esta función retorna la información del jinete o amazona asociado al id pasado por parámetro en la url.
    """
    
    app.logger.info("Call to index function")

    jya = find_jya_by_id(user_id)
    jya_address = find_adress_by_id(jya.address_id).string()
    files = get_files_by_horseman_id(jya.id)
    jya_json = jya.to_dict(jya_address)
    files_json = []

    files, page, order_by, search, document_type = showFiles(request)

    if files:
        for file in files:    
            files_json.append(file.to_dict())

    context = {
        'pagination': files,
        'files': files_json,
        'user': jya_json,
        'id': user_id,
    }

    app.logger.info("End of call to index function")

    return render_template('horsemen_and_amazons/jya_user_info.html', context=context, page=page, order_by=order_by, search=search, document_type=document_type)

@bp.route("/<int:user_id>/delete_file/<int:file_id>", methods=['POST', 'GET'])
@inject_user_permissions
def delete_file(user_id, file_id):

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
    return redirect(url_for('horsemen_and_amazons.list_info_by_jya', user_id=user_id))
   
@bp.route("/<int:user_id>/add_file", methods=['POST', 'GET'])
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
                horsemen_and_amazons_id = user_id,
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
        return redirect(url_for('horsemen_and_amazons.list_info_by_jya', user_id=user_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("horsemen_and_amazons/edit_file.html", form=form, user_id=user_id, file=file)
