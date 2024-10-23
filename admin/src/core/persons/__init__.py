from src.core.database import db
from src.core.persons.models.person import Person, Employee, JyA, FamilyMemberOrTutor
from src.core.persons.models.address import Address
from src.core.persons.models.emergency_contact import EmergencyContact
from src.core.persons.models.healthcare_plan import HealthcarePlan
from src.core.persons.models.file import EmployeeFile, File
from datetime import datetime

def create_person(**kwargs):
    person = Person(**kwargs)
    db.session.add(person)
    db.session.commit()

    return person

def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee

def create_JyA(**kwargs):
    jya = JyA(**kwargs)
    db.session.add(jya)
    db.session.commit()

    return jya

def create_family_member_or_tutor(**kwargs):
    family_member_or_tutor = FamilyMemberOrTutor(**kwargs)
    db.session.add(family_member_or_tutor)
    db.session.commit()

    return family_member_or_tutor

def create_address(**kwargs):
    address = Address(**kwargs)
    db.session.add(address)
    db.session.commit()

    return address

def create_emergency_contact(**kwargs):
    emergency_contact = EmergencyContact(**kwargs)
    db.session.add(emergency_contact)
    db.session.commit()

    return emergency_contact

def create_healthcare_plan(**kwargs):
    healthcare_plan = HealthcarePlan(**kwargs)
    db.session.add(healthcare_plan)
    db.session.commit()

    return healthcare_plan

def create_file(**kwargs):
    file = File(**kwargs)
    db.session.add(file)
    db.session.commit()

    return file

def create_employee_file(**kwargs):
    employee_file = EmployeeFile(**kwargs)
    db.session.add(employee_file)
    db.session.commit()

    return employee_file

def get_jya_users():

    """ Devuelve la lista de jinetes y amazonas registrados en el sistema """
    
    return JyA.query.all()

def find_jya_by_id(id):

    """Devuelve el jinete o amazona con el id pasado por parámetro"""

    return JyA.query.filter_by(id=id).first()

def updated_jya(horseman, **kwargs):

    """Edita el jinete con el id pasado por parámetro"""
    
    for key, value in kwargs.items():
        if value is not None:
            setattr(horseman, key, value)
            
    db.session.add(horseman)
    db.session.commit()

    return horseman

def delete_jya_by_id(jya_id):

    """Elimina de la base de datos el jinete con el id pasado como parámetro """
    
    horseman = JyA.query.filter_by(id = jya_id).first()
    db.session.delete(horseman)
    db.session.commit()

def find_address_by_id(id):

    """Devuelve la dirección con el id pasado por parámetro"""

    return Address.query.filter_by(id=id).first()

def get_files_by_horseman_id(horseman_id):
    
    """Devuelve los archivos asociados al jinete con el id pasado por parámetro"""

    return File.query.filter_by(horsemen_and_amazons_id = horseman_id).all()

def find_jya_by_dni(horseman_dni):

    """Devuelve el jinete con el dni pasado por parámetro en caso de que exista en la base de datos"""

    return JyA.query.filter_by(DNI = horseman_dni).first()

def delete_file_by_id(file_id):

    """Elimina de la base de datos el archivo con el id pasado como parámetro """
    
    print("Este es el file id en la función", file_id)
    file = File.query.filter_by(id = file_id).first()
    print("ESTE ES EL FILE", file)
    db.session.delete(file)
    db.session.commit()

def find_file_by_id(id):

    """Devuelve el archivo con el id pasado por parámetro"""

    return File.query.filter_by(id=id).first()

def find_file_by_title(file_title):

    """Devuelve el archivo con el titulo pasado por parámetro"""

    return File.query.filter_by(title=file_title).first()

def updated_file(file, **kwargs):

    """Edita el archivo con el id pasado por parámetro"""

    allowed_fields = ['file_url', 'file_type', 'document_type', 'title', 'horsemen_and_amazons_id']
    
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            setattr(file, key, value)
            

    file.upload_date = datetime.now()  

    db.session.add(file)
    db.session.commit()

    return file

def get_emergency_contacts():
    
    """Devuelve todos los contactos de emergencia existentes en la base de datos"""

    return EmergencyContact.query.all()

def get_healthcare_plans():

    """Devuelve todos los contactos de emergencia existentes en la base de datos"""

    return HealthcarePlan.query.all()

def get_address():

    """Devuelve todas las direcciones existentes en la base de datos"""

    return Address.query.all()

def get_emergency_contact_by_id(emergency_contact_id):

    """Devuelve el contacto de emergencia con el id pasado por parámetro"""

    return EmergencyContact.query.filter_by(id=emergency_contact_id).first()

def get_healthcare_plan_by_id(healthcare_plan_id):

    """Devuelve el plan de salud con el id pasado por parámetro"""

    return HealthcarePlan.query.filter_by(id=healthcare_plan_id).first()

def find_employee_by_id(id):

    """Devuelve el empleado con el id pasado por parámetro"""

    return Employee.query.filter_by(id=id).first()

def get_files_by_employee_id(id):
    
    """Devuelve los archivos asociados al empleado con el id pasado por parámetro"""

    return EmployeeFile.query.filter_by(employee_id = id).all()

def find_employee_file_by_title(title):

    """Devuelve el archivo con el titulo pasado por parámetro"""

    return EmployeeFile.query.filter_by(title=title).first()

def find_employee_file_by_id(id):

    """Devuelve el archivo con el id pasado por parámetro"""

    return EmployeeFile.query.filter_by(id=id).first()

def delete_employee_file_by_id(id):

    """Elimina de la base de datos el archivo con el id pasado como parámetro """
    
    employee_file = EmployeeFile.query.filter_by(id = id).first()
    db.session.delete(employee_file)
    db.session.commit()

def updated_employee_file(employee_file, **kwargs):

    """Edita el archivo con el id pasado por parámetro"""

    allowed_fields = ['file_url', 'title', 'document_type', 'employee_id']
    
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            setattr(employee_file, key, value)
            
    employee_file.upload_date = datetime.now()  # Actualizar la fecha de subida

    db.session.add(employee_file)
    db.session.commit()

    return employee_file