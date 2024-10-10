from src.core.database import db
from src.core.persons.models.person import Person, Employee, JyA, FamilyMemberOrTutor
from src.core.persons.models.address import Address
from src.core.persons.models.emergency_contact import EmergencyContact
from src.core.persons.models.healthcare_plan import HealthcarePlan
from src.core.persons.models.file import File
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

def get_jya_users():

    """ Devuelve la lista de jinetes y amazonas registrados en el sistema """
    
    return JyA.query.all()

def find_jya_by_id(id):

    """Devuelve el jinete o amazona con el id pasado por parámetro"""

    return JyA.query.filter_by(id=id).first()

def find_adress_by_id(id):

    """Devuelve la dirección con el id pasado por parámetro"""

    return Address.query.filter_by(id=id).first()

def get_files_by_horseman_id(horseman_id):
    
    """Devuelve los archivos asociados al jinete con el id pasado por parámetro"""

    return File.query.filter_by(horsemen_and_amazons_id = horseman_id).all()


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
            

    file.upload_date = datetime.now()  # Actualizar la fecha de subida

    db.session.add(file)
    db.session.commit()

    return file