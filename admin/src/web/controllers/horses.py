from flask import Blueprint, request, flash, session, redirect, render_template, url_for
from flask import render_template, redirect, url_for
from src.core.auth.auth import inject_user_permissions, permission_required
from src.core.horses.models.horse import Horse
from src.core.database import db
from src.core.horses.forms import create_horse_Form, registryFileForm
from flask import current_app as app
from src.core.horses.__init__ import create_horse, find_horse_by_id, find_file_by_id, delete_file_by_id, create_file, find_file_by_title, updated_file
from sqlalchemy import desc
from src.core.persons import Employee
from src.core.horses.models.horses_file import Horse_file
from datetime import timedelta
import json
import io
from os import fstat

bp = Blueprint('horses', __name__, url_prefix='/horses')


@bp.get("/")
@permission_required('horse_index')
@inject_user_permissions
def list_horses():

    """
    Esta función retorna el listado de los caballos registrados en el sistema, 
    aplicando filtros de búsqueda, ordenación y paginación. 
    Permite filtrar por nombre y tipo de jinete/amazona asignado, y 
    ordenar por nombre, fecha de nacimiento o fecha de entrada de forma ascendente o descendente.


    Returns:
        render_template: Renderiza la plantilla 'ecuestre/horses.html' con los siguientes parámetros:
            - horses (list): Lista de objetos Horse correspondientes a la página actual, filtrados según los criterios aplicados.
            - order (str): El criterio de ordenamiento seleccionado.
            - q (str): Parámetro de búsqueda seleccionado.
            - pagination (Pagination): Objeto de paginación con información de la página actual, total de páginas y registros.
            - type_jya_assigned (str): El tipo de jinete/amazona aplicado como filtro (si corresponde).
            - form (Form): El formulario para crear un nuevo caballo.
    """

    order = request.args.get('order', 'name_asc') #orden default por nombre ascendente 
    q = request.args.get('q', None)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    type_jya = request.args.get('type_jya', None)
    horses_query = Horse.query.filter(~Horse.name.startswith('*'))

    if order == 'name_asc':
        horses_query = horses_query.order_by(Horse.name.asc())
    elif order == 'name_desc':
        horses_query = horses_query.order_by(Horse.name.desc())
    elif order == 'birth_date_asc':
        horses_query = horses_query.order_by(Horse.date_of_birth.asc())
    elif order == 'birth_date_desc':
        horses_query = horses_query.order_by(Horse.date_of_birth.desc())
    elif order == 'entry_date_asc':
        horses_query = horses_query.order_by(Horse.date_of_entry.asc())
    elif order == 'entry_date_desc':
        horses_query = horses_query.order_by(Horse.date_of_entry.desc())

    horse_pagination = horses_query.paginate(page=page, per_page=per_page, error_out=False)
    horses = horse_pagination.items


    if q:
        horses = [horse for horse in horses if q.lower() in horse.name.lower()]
    
    if type_jya:
        horses = [horse for horse in horses if type_jya in horse.type_jya_assigned]

    
    return render_template('ecuestre/horses.html', horses=horses, order=order, q=q, pagination=horse_pagination, type_jya_assigned=type_jya, form=create_horse_Form())




@bp.route('/create', methods=['GET', 'POST'])
@permission_required('horse_new')
@inject_user_permissions
def create_horse_view():
    """
    Muestra el formulario para crear un nuevo caballo y maneja la creación del mismo al enviar el formulario.

    Esta función carga un formulario para ingresar los datos del caballo y los empleados relacionados. 
    Al enviar el formulario, se valida la información ingresada y, si es correcta, se registra un nuevo 
    caballo en la base de datos, junto con los empleados asignados y los tipos de jinetes y amazonas seleccionados.

    En caso de error durante el proceso de creación del caballo, la función recarga la plantilla con el 
    contexto necesario para mantener el estado del formulario y los datos.

    Returns:
        redirect
            - Si el formulario es válido y el caballo se crea correctamente, redirige a la lista de caballos.
        render_template: 
           - Si la validación falla o hay un error, renderiza 'ecuestre/create_horse.html' con las 
              variables `form` y `horses` en el contexto para recargar el formulario con los datos 
              existentes y mostrar información adicional en la vista.

    Raises:
        Exception: 
            - Si ocurre un error durante la creación del caballo, se muestra un mensaje de error mediante 
              `flash` y se recarga la plantilla para que el usuario pueda intentar nuevamente.
        
    """
    form = create_horse_Form()

    form.employees.choices = [(e.id, e.name) for e in Employee.query.all()]  # Cargar empleados previamente para que el usuario pueda ver y seleccionar los empleados disponibles al crear el caballo
    
    if form.validate_on_submit():
        try:
            type_jya_assigned=[] #Array de tipos de jinete/amazonas asignados
            if form.type_jya_hipoterapia.data:
                type_jya_assigned.append ("Hipoterapia")
            if form.type_jya_monta_terapeutica.data:
                type_jya_assigned.append ("Monta Terapéutica")
            if form.type_jya_dea.data:
                type_jya_assigned.append ("Deporte Ecuestre Adaptado")
            if form.type_jya_ar.data:
                type_jya_assigned.append ("Actividades Recreativas")
            if form.type_jya_equitacion.data:
                type_jya_assigned.append ("Equitación")
            
            
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


            for empleado_id in form.employees.data: # Asignar los empleados al caballo
                empleado = Employee.query.get(empleado_id)
                new_horse.employees.append(empleado)


            db.session.add(new_horse)
            db.session.commit()
            
            app.logger.info("Caballo creado exitosamente: %s", form.name.data)
            flash("Caballo creado exitosamente", "success")
            return redirect(url_for('horses.list_horses'))  # Redirigir a la lista de caballos
        except Exception as e:
            app.logger.error("Error al crear el caballo: %s", str(e))
            flash("Ocurrió un error al crear el caballo", "error")

 
    context = { #diccionario de datos que se pasa hacia las plantillas HTML 
        'form': form,  #Permitir que el formulario se renderice y mantenga su estado si ocurre un error.
        'horses': Horse.query.order_by(Horse.name).all() 
    }

    return render_template('ecuestre/create_horse.html', context=context)  # Renderizar el formulario


@bp.route('/editar/<int:horse_id>', methods=['GET', 'POST'])
@permission_required('horse_update')
@inject_user_permissions
def edit_horse(horse_id):

    """
        Edita la información de un caballo específico asociado a su ID.

    Esta función maneja la edición de los detalles de un caballo, permitiendo
    actualizar su nombre, fecha de nacimiento, género, raza, tipo de pelaje,
    método de adquisición, fecha de ingreso, sede, tipos de JYA asignados y
    empleados asociados. Los cambios se guardan en la base de datos.

    Args:
        horse_id (int): ID del caballo que se desea editar.

    Returns:
        redirect
            - Redirige a la lista de información del caballo actualizado si 
              el formulario se valida correctamente.
        render_template
            - Renderiza la plantilla 'ecuestre/edit_horse.html' con el formulario,
              la lista de empleados y el caballo si la solicitud es GET o si 
              el formulario no es válido.
    """

    employee_list = Employee.query.all()
    horse = Horse.query.get(horse_id)
    form = create_horse_Form(obj=horse)
    form.gender.choices = [('Macho', 'Macho'), ('Hembra', 'Hembra')]
    form.purchase_or_donation.choices = [('Compra', 'Compra'), ('Donación', 'Donación')]
    form.employees.choices = [(e.id, e.name) for e in employee_list]


    if form.validate_on_submit():
        horse.name = form.name.data
        horse.date_of_birth = form.date_of_birth.data
        horse.gender = form.gender.data
        horse.race = form.race.data
        horse.fur = form.fur.data
        horse.purchase_or_donation = form.purchase_or_donation.data
        horse.date_of_entry = form.date_of_entry.data
        horse.sede = form.sede.data
        
        type_jya = []
        if form.type_jya_hipoterapia.data:
            type_jya.append('Hipoterapia')
        if form.type_jya_monta_terapeutica.data:
            type_jya.append('Monta Terapéutica')
        if form.type_jya_dea.data:
            type_jya.append('Deporte Ecuestre Adaptado')
        if form.type_jya_ar.data:
            type_jya.append('Actividades Recreativas')
        if form.type_jya_equitacion.data:
            type_jya.append('Equitación')

        horse.type_jya_assigned = type_jya

        selected_employee_ids = form.employees.data
        selected_employees = Employee.query.filter(Employee.id.in_(selected_employee_ids)).all()
        horse.employees = selected_employees

        db.session.commit()
        flash('Horse updated successfully!', 'success')
        return redirect(url_for('horses.list_info_by_id', horse_id=horse.id))
    return render_template('ecuestre/edit_horse.html', form=form, employee_list=employee_list, horse=horse)


@bp.route('/eliminar/<int:horse_id>', methods=['POST'])
@permission_required('horse_destroy')
@inject_user_permissions
def delete_horse(horse_id):

    """
    Elimina de forma lógica un caballo específico asociado a su ID.

    Esta función marca un caballo como eliminado al modificar su nombre, 
    anteponiendo un asterisco (*) al mismo. Esto permite realizar eliminaciones 
    lógicas sin borrar el registro de la base de datos.

    Args:
        horse_id (int): ID del caballo que se desea eliminar.

    Returns:
        redirect
            - Redirige a la lista de caballos después de intentar la eliminación.
            - Muestra un mensaje de éxito si la eliminación fue exitosa.
            - Muestra un mensaje de error si el caballo no fue encontrado.
    """

    horse = Horse.query.get(horse_id)
    if horse:
        horse.name = f'*{horse.name.strip()}'
        db.session.commit()
        flash('Horse deleted successfully!', 'success')
    else:
        flash('Horse not found!', 'danger')
    return redirect(url_for('horses.list_horses'))


def show_files(horse_id, request):
   
    # Determine the order option
    order_by = request.args.get('order_option', 'title_asc', type=str)

    
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
    title = request.args.get('title', '', type=str)
    document_type = request.args.get('document_type', '', type=str)


    # Build the query
    query = Horse_file.query.filter(Horse_file.horses_id == horse_id)
    
    if title:
        query = query.filter(Horse_file.title.ilike(f'%{title}%'))
    if document_type and document_type != 'Selecciona un tipo':
        query = query.filter(Horse_file.document_type == document_type)
    
    per_page = 2
    # Apply ordering and pagination
    pagination = query.order_by(order_criteria).paginate(page=page, per_page=per_page, error_out=False)

    return pagination, page, order_by, title, document_type


@bp.get("/<int:horse_id>")
@permission_required('horse_show')
@inject_user_permissions
def list_info_by_id(horse_id):

    """
    Muestra archivos asociados a un caballo específico, permitiendo la 
    ordenación y filtrado de los resultados.

    Esta función construye una consulta para recuperar archivos relacionados
    con un caballo, con opciones para ordenar por título o fecha, así como
    filtrar por título y tipo de documento. También implementa paginación
    para gestionar la visualización de archivos.

    Args:
        horse_id (int): ID del caballo cuyos archivos se desean mostrar.
        request: El objeto de solicitud que contiene parámetros de consulta para la ordenación y filtrado.

    Returns:
        tuple: 
            - pagination (Pagination): Objeto de paginación que contiene 
              los archivos filtrados y ordenados.
            - page (int): El número de la página actual.
            - order_by (str): La opción de ordenación seleccionada.
            - title (str): El título proporcionado para filtrar archivos.
            - document_type (str): El tipo de documento proporcionado para 
              filtrar archivos.
    """

    horse = find_horse_by_id(horse_id)
    horse_json = horse.to_dict()  
    files_json = []


    pagination, page, order_by, title, document_type = show_files(horse_id, request)

    files_json = [file.to_dict() for file in pagination.items]

    context = {
        'pagination': pagination,
        'files': files_json,
        'horse': horse_json,
        'id': horse_id,
    }

    
    return render_template('ecuestre/horses_info.html', context=context, page=page, order_by=order_by, title=title, document_type=document_type)


@bp.route("/<int:horse_id>/delete_file/<int:file_id>", methods=['POST', 'GET'])
@permission_required('horse_update')
@inject_user_permissions
def delete_file(horse_id, file_id):

    """
    Elimina un archivo asociado a un caballo específico dado su ID.

    Este método maneja la eliminación de un archivo almacenado en un
    servicio de almacenamiento (MinIO) y realiza una eliminación lógica 
    en la base de datos. Dependiendo del tipo de archivo, se elimina el 
    archivo correspondiente en el almacenamiento externo.

    Args:
        horse_id (int): ID del caballo al que está asociado el archivo que 
            se desea eliminar.
        file_id (int): ID del archivo que se desea eliminar.

    Returns:
        redirect: Redirige a la lista de archivos del caballo 
            correspondiente después de la eliminación del archivo.


    """

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
@permission_required('horse_update')
@inject_user_permissions
def add_file(horse_id):

    """
    Muestra la vista para agregar un archivo asociado a un caballo y 
    valida los parámetros antes de guardar el archivo.

    Este método maneja la subida de archivos y enlaces, realizando
    validaciones para asegurar que no se dupliquen títulos. Si se recibe
    un formulario válido, se guarda el archivo en el almacenamiento (MinIO)
    y se registran los metadatos en la base de datos.

    Args:
        horse_id (int): ID del caballo al que se asociará el archivo.

    Returns:
        - Redirige a la lista de información del caballo correspondiente 
          después de agregar el archivo si el formulario es válido.
        - Renderiza la plantilla de registro de archivo si la solicitud 
          es GET o si el formulario no es válido.

    """

    form = registryFileForm()

    minio_client = app.storage.client
    bucket_name = app.config['BUCKET_NAME']
    
    
    if (form.validate_on_submit()):
        
        if (find_file_by_title(form.title.data)):
            
            flash("Ya existe un archivo con el titutlo ingresado", "error")
            return redirect(url_for("horses.add_file", horse_id=horse_id))

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
                horses_id = horse_id,
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
                horses_id=horse_id,
            )

        flash("El archivo se ha creado correctamente", "success")
        return redirect(url_for('horses.list_info_by_id', horse_id=horse_id))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"El formulario no es válido, error en el/los campos {getattr(form, field).label.text}: {error}", "error")

    return render_template("ecuestre/registry_file.html", form=form, horse_id=horse_id)


@bp.route("/<int:horse_id>/download_file/<file_id>", methods=['GET'])
@permission_required('horse_update')
@inject_user_permissions
def download_file(horse_id, file_id):

    """
    Permite la descarga de un archivo asociado a un caballo específico 
    dado su ID.

    Este método recupera un archivo de la base de datos utilizando su ID,
    genera una URL firmada en MinIO para permitir la descarga del archivo 
    y redirige al usuario a esa URL.

    Args:
        horse_id (int): ID del caballo al que está asociado el archivo a 
            descargar.
        file_id (int): ID del archivo que se desea descargar.

    Returns:
        Redirige al usuario a la URL firmada para la descarga del archivo.
    """
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
@permission_required('horse_update')
@inject_user_permissions
def edit_file(horse_id, file_id):

    """
    Muestra la vista para editar un archivo asociado a un caballo y 
    valida los parámetros antes de actualizar el archivo en la base de datos.

    Este método permite modificar un archivo existente, ya sea un 
    documento o un enlace. Si se recibe un formulario válido, el archivo 
    se actualiza en el almacenamiento (MinIO) y se registran los nuevos 
    metadatos en la base de datos.

    Args:
        horse_id (int): ID del caballo al que está asociado el archivo.
        file_id (int): ID del archivo que se desea editar.

    Returns:
        - Redirige a la lista de información del caballo correspondiente 
          después de editar el archivo si el formulario es válido.
        - Renderiza la plantilla de edición de archivo si la solicitud 
          es GET o si el formulario no es válido.

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

