from flask import Blueprint, render_template, redirect, flash, url_for, session
from src.core.auth import create_user 
from src.core.auth.forms import registryForm
from flask import current_app as app
from src.core.auth import find_user_by_email, find_role_id_by_name
from src.core.auth import get_user_permissions
from src.web.handlers.auth import is_authenticated

bp = Blueprint('registry', __name__, url_prefix='/registry')


@bp.route('/', methods=['GET','POST'])
def registry_function():

    """
    Muestra la vista del registro, además valida los parametros, y guarda al usuario en la base de datos si
    se recibió el formulario y el mismo es válido.
    """
    if is_authenticated(session):
        flash("Ya te encuentras logueado", "warning")
        return render_template("home.html")

    app.logger.info("Call to registry_function")
    form = registryForm()
    app.logger.info("El formulario es valido: %s", form.validate_on_submit())
    user_permissions, user_system_admin = get_user_permissions(session.get("user"))

    context = {
        "user_permissions": user_permissions,
        "user_system_admin": user_system_admin,
    }
    if (form.validate_on_submit()):
        
        if (find_user_by_email(form.email.data)):
            app.logger.error("The following email is already registered: %s ", form.email.data)
            flash("Ya existe un usuario con el mail ingresado", "error")
            return redirect(url_for("registry.registry_function"))

        create_user(
            email = form.email.data,
            alias = form.alias.data,
            password = form.password.data,
            role_id = find_role_id_by_name(form.role.data),
        )
        app.logger.info("End of call to registry_function")
        flash("Usuario creado correctamente", "success")
        return render_template("home.html", context=context)
    
    return render_template("auth/registry.html",context=context, form=form)
