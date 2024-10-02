from flask import Blueprint, render_template
from src.core.persons import get_jya_users, find_adress_by_id, find_jya_by_id
import json

bp = Blueprint("jya_users", __name__, url_prefix="/users-jya")

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
     print(jya_address)
     jya_json = json.dumps(jya.to_dict(jya_address))
     print("ESTE ES EL JSON", jya_json)
     return render_template("horsemen_and_amazons/jya_user_info.html", user_jya = jya_json)
