from flask import Blueprint, render_template, request, redirect, flash, url_for
from src.core.auth import create_user
from src.core.database import db   
from src.core.auth.forms import registryForm
from src.core.auth import find_user_by_email, find_role_id_by_name

bp = Blueprint('registry', __name__, url_prefix='/registry')


@bp.route('/', methods=['GET','POST'])
def registry_function():

    """
    Muestra la vista del registro, además valida los parametros, y guarda al usuario en la base de datos si
    se recibió el formulario y el mismo es válido.
    """

    form = registryForm()
    print("El formulario es valido: ", form.validate_on_submit())
    if (form.validate_on_submit()):
        
        if (find_user_by_email(form.email.data)):
            flash("Ya existe un usuario con el mail ingresado", "error")
            return redirect(url_for("registry.registry_function"))

        create_user(
            email = form.email.data,
            alias = form.alias.data,
            password = form.password.data,
            role_id = find_role_id_by_name(form.role.data),
        )

        print("Usuario creado correctamente", "success")
        return render_template("home.html")
    
    return render_template("auth/registry.html", form=form)
