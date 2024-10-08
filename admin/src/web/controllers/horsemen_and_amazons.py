from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.persons import get_jya_users, find_adress_by_id, find_jya_by_id, get_files_by_horseman_id, delete_file_by_id, create_JyA, create_file, find_file_by_title, find_file_by_id, updated_file
from src.core.persons.forms import registryFileForm
from flask import current_app as app
from datetime import timedelta
from src.core.persons.models.file import File
from sqlalchemy import desc
import json
import io


bp = Blueprint("horsemen_and_amazons", __name__, url_prefix="/users-jya")


@bp.get("/")
def list_jya_users():

    """
        Esta función retorna el listado con los jinetes y amazonas registrados en el sistema.
    """

    jya_users = get_jya_users()

    return render_template("horsemen_and_amazons/jya_users_list.html", users = jya_users)

@bp.get("/<int:user_id>")
def list_info_by_jya(user_id):

    """
        Esta función retorna la información del jinete o amazona asociado al id pasado por parámetro en la url.
    """
    
    jya = find_jya_by_id(user_id)
    jya_address = find_adress_by_id(jya.address_id).string()
    files = get_files_by_horseman_id(jya.id)
    jya_json = jya.to_dict(jya_address)
    files_json = []

    if files:
        for file in files:    
            files_json.append(file.to_dict())

    context = {
        'files': files_json,
        'user': jya_json,
        'id': user_id,
    }

    return render_template("horsemen_and_amazons/jya_user_info.html", context=context)

@bp.route("/<int:user_id>/order", methods=['POST', 'GET'])
def order_by(user_id):
    order_by = request.form.get('order_option')
    print("ESTE ES EL USER ID", user_id)
    jya = find_jya_by_id(user_id)
    jya_address = find_adress_by_id(jya.address_id).string()
    jya_json = jya.to_dict(jya_address)
    files = get_files_by_horseman_id(jya.id)
    files_json = []

    if order_by:
        if order_by == 'title_asc':
            files = File.query.order_by(File.title).all()
        elif order_by == 'title_desc':
            files = File.query.order_by(desc(File.title)).all()
        if order_by == 'date_asc':
            files = File.query.order_by(File.upload_date).all()
        elif order_by == 'date_desc':
            files = File.query.order_by(desc(File.upload_date)).all()
        
    if files:
        for file in files:    
            files_json.append(file.to_dict())
            print("Estos son los archivos ordenados por nombre", files_json)

    context = {
        'files': files_json,
        'user': jya_json,
        'id': user_id,
    }

    return render_template("horsemen_and_amazons/jya_user_info.html", context=context)


@bp.route("/<int:user_id>/delete_file/<int:file_id>", methods=['POST', 'GET'])
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
    return redirect(url_for('horsemen_and_amazons.order_by', user_id=user_id))
   
@bp.route("/<int:user_id>/add_file", methods=['POST', 'GET'])
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
        return redirect(url_for('horsemen_and_amazons.order_by', user_id=user_id))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("horsemen_and_amazons/registry_file.html", form=form, user_id=user_id)

@bp.route("/<int:user_id>/download_file/<file_id>", methods=['GET'])
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
        return redirect(url_for('horsemen_and_amazons.order_by', user_id=user_id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")
            
    return render_template("horsemen_and_amazons/edit_file.html", form=form, user_id=user_id, file=file)
