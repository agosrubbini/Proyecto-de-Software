from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core import auth
from flask import current_app as app
from flask_bcrypt import Bcrypt
from src.web.handlers.auth import is_authenticated

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.get("/")
def login():#muestra el forms
    if is_authenticated(session):
        flash("Ya te encuentras logueado", "warning")
        return render_template("home.html")
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
    
    if user.is_blocked:
        app.logger.error("User is blocked")
        flash("El usuario se encuentra bloqueado", "error")
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
    app.logger.info("Call to logout method")
    if session.get("user"):
        app.logger.info("Deleting session of: %s",session.get("user"))
        del session["user"]
        session.clear()
        flash("Sesión cerrada correctamente", "success")
    else:
        flash("No hay una sesión activa", "error")
    app.logger.info("End of call to logout method")
    return redirect(url_for("home"))

