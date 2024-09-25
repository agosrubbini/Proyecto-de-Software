import datetime
from flask import Blueprint, render_template, request
from src.core.auth import create_user
from src.core.database import db    

bp_registry = Blueprint('registry', __name__, url_prefix='/registry')

@bp_registry.route('/')
def registry_index():
    return 'Registry Index'

@bp_registry.route('/registry', methods=['POST'])
def registry_add():
    try:
        user = create_user(
            email=request.form.get('email'),
            alias=request.form.get('alias'),
            password=request.form.get('password'), 
        )
        return render_template('home.html', user=user)
    except Exception as e:
        db.session.rollback()
        return f'Error al crear usuario: {str(e)}', 400