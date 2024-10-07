from flask import Blueprint, render_template, request, redirect, url_for
from src.core.persons import get_jya_users, find_adress_by_id, find_jya_by_id, get_files_by_horseman_id, delete_file_by_id, create_JyA, create_file
from src.core.persons.forms import registryFileForm
from flask import current_app as app
from src.core.persons.models.file import File
from sqlalchemy import desc
import json

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
    delete_file_by_id(file_id)

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
    app.logger.info("El formulario del archivo es valido: %s", form.validate_on_submit())
    if (form.validate_on_submit()):
        
        if (find_user_by_email(form.email.data)):
            app.logger.error("The following email is already registered: %s ", form.email.data)
            flash("Ya existe un usuario con el mail ingresado", "error")
            return redirect(url_for("registry.registry_function"))

        create_file(
            file_url = form.file_url.data,
            file_type = form.file_type.data,
            document_type = form.document_type.data,
            title = form.title.data,
            horsemen_and_amazons_id = user_id,
        )
        app.logger.info("End of call to add_file")
        flash("Archivo creado correctamente", "success")
        return redirect(url_for('horsemen_and_amazons.order_by', user_id=user_id))
    
    return render_template("horsemen_and_amazons/registry_file.html", form=form, user_id=user_id)