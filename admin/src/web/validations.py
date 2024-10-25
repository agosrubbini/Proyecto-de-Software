from datetime import datetime, date as dt_date
import re
from flask import current_app as app
from core.auth import find_user_by_alias, find_user_by_email, get_all_roles
from core.payments import validate_beneficiary


def validate_role(role):
    '''
        Valida que el rol seleccionado exista en la lista de roles
    '''
    return role in list(map(lambda role:role.name, get_all_roles()))

def validate_passwords(password, confirm_password):
    '''
        Valida que las contraseñas ingresadas sean iguales
    '''
    return password == confirm_password

def validate_email(email):
    '''
        Valida que el email ingresado sea valido
    '''
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    return re.match(email_regex, email)

def validate_user_form(form):
    errors = []

    if not validate_passwords(form.password.data, form.confirm.data):
        errors.append("Las contraseñas no coinciden")
        app.logger.error("The passwords do not match")

    if not validate_role(form.role.data):
        errors.append("No fue seleccionado ningun rol")
        app.logger.error("The role was not selected")

    if not validate_email(form.email.data):
        errors.append("El email ingresado no es valido")
        app.logger.error("The email entered is not valid")

    return " ".join(errors)

def validate_unique_fields(form):
    errors = []

    if find_user_by_alias(form.alias.data):
        errors.append("Ya existe un usuario con el alias ingresado")
        app.logger.error("The following alias is already registered: %s", form.alias.data)

    if find_user_by_email(form.email.data):
        errors.append("Ya existe un usuario con el mail ingresado")
        app.logger.error("The following email is already registered: %s", form.email.data)

    return " ".join(errors)

def validate_user_update_form(form, id):
    errors = []

    user_with_email = find_user_by_email(form.email.data)
    if user_with_email and user_with_email.id != id:
        errors.append("Ya existe un usuario con el mail ingresado")
        app.logger.error("The following email is already registered: %s", form.email.data)

    user_with_alias = find_user_by_alias(form.alias.data)
    if user_with_alias and user_with_alias.id != id:
        errors.append("Ya existe un usuario con el alias ingresado")
        app.logger.error("The following alias is already registered: %s", form.alias.data)

    return " ".join(errors)



def validate_amount(amount):
    '''
        Valida que el monto ingresado sea un numero
    '''
    if not amount:
        return False
    try:
        number = float(amount)
        return number > 0
    except ValueError:
        return False
    
def validate_date(date):
    if isinstance(date, (datetime, dt_date)):
        # Convertir a datetime si el parámetro es solo una fecha
        if isinstance(date, dt_date):
            date = datetime.combine(date, datetime.min.time())
        # Asegúrate de llamar a datetime.now() con paréntesis
        return date <= datetime.now()
    else:
        return False
    
def validate_payment_form(form):
    errors = []

    if not validate_amount(form.amount.data):
        errors.append("El monto ingresado no es valido")
        app.logger.error("The entered amount is not valid")

    if not validate_beneficiary(form.beneficiary.data):
        errors.append("El beneficiario ingresado no es valido")
        app.logger.error("The entered beneficiary is not valid")

    if not validate_date(form.payment_date.data):
        errors.append("La fecha ingresada no es válida o no es menor al día de hoy")
        app.logger.error("The entered date is not valid or is not earlier than today")

    return " ".join(errors)