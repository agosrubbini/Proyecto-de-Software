# TODO rename this file (esto es lo que está haciendo joaco. lo dejé a medias para tener una referencia de cómo hacerlo)

from flask import Blueprint, session, abort, redirect, url_for 
from src.web.handlers.auth import is_authenticated

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.get("/")
def index():

    if not is_authenticated(session):
        return abort(401)
    return redirect(url_for("home"))