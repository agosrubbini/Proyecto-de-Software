from datetime import datetime, date as dt_date
import re
from flask import current_app as app
from core.auth import find_user_by_alias, find_user_by_email, get_all_roles
from core.persons import find_jya_by_dni, get_healthcare_plan_by_social_security_and_affiliate_number
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
    
def validate_payment_form(form):
    errors = []

    #TODO fix this validation
    '''
    if form.payment_type.data != 'Honorarios' and form.beneficiary.data:
        errors.append("No se puede ingresar una beneficiario si el tipo de pago no es 'Honorarios'")
        app.logger.error("You cannot enter a beneficiary if the payment type is not 'Honorarios'") 
    '''

    if form.payment_type.data == 'Honorarios' and not form.beneficiary.data:
        errors.append("Debe ingresar un beneficiario")
        app.logger.error("You must enter a beneficiary")    

    if not validate_amount(form.amount.data):
        errors.append("El monto ingresado no es valido")
        app.logger.error("The entered amount is not valid")

    if form.beneficiary.data:
        if not validate_beneficiary(form.beneficiary.data):
            errors.append("El beneficiario ingresado no es valido")
            app.logger.error("The entered beneficiary is not valid")

    return " ".join(errors)

def validate_horseman_name(name):
    '''
        Valida que el nombre no esté vacío y contenga solo letras
    '''
    return bool(name) and all(char.isalpha() or char.isspace() for char in name)

def validate_horseman_name_new_contact(name):
    '''
        Valida que el nombre no esté vacío y contenga solo letras
    '''
    return bool(name) and all(char.isalpha() or char.isspace() for char in name)

def validate_attending_professionals(attending_professionals):
    '''
        Valida que los nombres de los profesionales no tengan números
    '''

    return bool(attending_professionals) and all(char.isalpha() or char.isspace() for char in attending_professionals)

def validate_healthcare_plan_name(healthcare_plan_name):
    '''
        Valida que los nombres de los profesionales no tengan números
    '''

    if hasattr(healthcare_plan_name, 'data'):
        healthcare_plan_name = healthcare_plan_name.data  # Obtiene el valor del campo

    return bool(healthcare_plan_name) and all(char.isalpha() or char.isspace() for char in healthcare_plan_name)

def validate_horseman_last_name(last_name):
    '''
        Valida que el apellido no esté vacío y contenga solo letras
    '''
    return bool(last_name) and all(char.isalpha() or char.isspace() for char in last_name)

def validate_numeric(value):
    '''
        Valida que el valor contenga solo números
    '''
    if isinstance(value, int):
        value = str(value)
    # Comprobar que el valor sea un string y contenga solo dígitos
    return isinstance(value, str) and value.isdigit()

def validate_age(age):
    '''
        Valida que la edad sea un número positivo y no mayor que 150
    '''
    if not validate_numeric(age):
        return False
    age_number = int(age)
    return 0 < age_number <= 150

def validate_new_address(form, errors):

    if form.is_new_address.data:
        
        if not form.new_address.street.data:
            errors.append("La calle es obligatoria")
        if not form.new_address.department.data:
            errors.append("El piso es obligatorio")
        if not form.new_address.locality.data:
            errors.append("La localidad es obligatoria")
        if not form.new_address.province.data:
            errors.append("La provincia es obligatoria")
        if not form.new_address.number.data:
            errors.append("El número es obligatorio")
        else:
            if not validate_numeric(form.new_address.number.data):
                errors.append("El número de la dirección debe contener solo números")
        if not form.new_address.phone_number.data:
            errors.append("El número de teléfono es obligatorio")
        else:
            if not validate_numeric(form.new_address.phone_number.data):
                errors.append("El número de teléfono de la  dirección debe contener solo números")
        

def validate_new_emergency_contact(form, errors):
   

    if form.is_new_emergency_contact.data:
        if not form.new_emergency_contact.name_emergency_contact.data:
            errors.append("El nombre del contacto de emergencia es obligatorio")
        else:
            if not validate_horseman_name_new_contact(form.new_emergency_contact.name_emergency_contact.data):
                errors.append("El nombre del contacto de emergencia no debe contener números")
        if not validate_numeric(form.new_emergency_contact.phone_number.data):
            errors.append("El número de teléfono del contacto de emergencia debe contener solo números")

def validate_unique_fields_horseman(form):
    errors = []

    if find_jya_by_dni(form.DNI.data):
        errors.append("Ya existe un jinete con el dni ingresado")
        app.logger.error("The following alias is already registered: %s", form.DNI.data)
    
    return "\n".join(errors)

def validate_healthcare_plan(form, errors):

    healthcare_plan = get_healthcare_plan_by_social_security_and_affiliate_number(form.healthcare_plan.social_security.data, form.healthcare_plan.affiliate_number.data)

    if healthcare_plan:
        errors.append("Ya existe un jinete con esa obra social y ese número de afiliado")
        app.logger.error("The following healthcare plan is already registered: %s", form.DNI.data)

def validate_horseman_form(form):
    errors = []

    if not validate_numeric(form.DNI.data):
        errors.append("El DNI debe contener solo números")
        app.logger.error("El DNI ingresado no es válido")

    if not validate_numeric(form.phone_number.data):
        errors.append("El número de teléfono debe contener solo números")
        app.logger.error("El número de teléfono ingresado no es válido")

    if not validate_age(form.age.data):
        errors.append("La edad debe ser un número entre 1 y 150")
        app.logger.error("La edad ingresada no es válida")
    
    if not validate_numeric(form.current_phone.data):
        errors.append("El número de teléfono actual debe contener solo números")
        app.logger.error("El número de teléfono actual ingresado no es válido")
    
    if not validate_attending_professionals(form.attending_professionals.data):
        errors.append("El/Los nombres de los profesionales no deben tener números")
        app.logger.error("El/Los nombres de los profesionales ingresados no son válidos")

    if not validate_healthcare_plan_name(form.healthcare_plan.social_security):
        errors.append("El nombre de la obra social no debe contener números")
        app.logger.error("El nombre de la obra social ingresado no es válido")

    if form.is_scholarshipped.data:
        if not validate_numeric(form.scholarship_percentage.data):
            errors.append("La fecha de nacimiento no puede ser futura")
            app.logger.error("La fecha de nacimiento ingresada no es válida")

    validate_new_address(form, errors)
    validate_new_emergency_contact(form, errors)
    validate_healthcare_plan(form, errors)

    return "\n".join([f"{i+1}. {error}" for i, error in enumerate(errors)])


