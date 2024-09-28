from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core import auth
from flask import current_app as app
from flask_bcrypt import Bcrypt

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.get("/")
def login():#muestra el forms
    return render_template("auth/login.html")

@bp.post("/authenticate")
def authenticate():
    app.logger.info("Call to authenticate method")
    params = request.form  # objeto desde donde obtengo los parámetros de entrada de un form
    bcrypt = Bcrypt()  # inicializa Bcrypt

    # 1. Buscar al usuario en la base de datos por email
    user = auth.find_user_by_email(params["email"])

    if not user:
        # Si el usuario no existe
        app.logger.error("Incorrect user mail")
        flash("Usuario o contraseña incorrecta", "error")
        return redirect(url_for("login.login"))

    # 2. Verificar si la contraseña ingresada coincide con el hash almacenado
    if not bcrypt.check_password_hash(user.password, params["password"]):
        # Si la contraseña es incorrecta
        app.logger.error("Incorrect password")
        flash("Contraseña incorrecta", "error")
        return redirect(url_for("login.login"))

    # 3. Si la autenticación es exitosa, iniciar la sesión
    session["user"] = user.email
    app.logger.info("End of call to authenticate method")
    flash("La sesión se inició correctamente!", "success")
    return redirect(url_for("home"))

@bp.get("/logout")
def logout():
    pass

