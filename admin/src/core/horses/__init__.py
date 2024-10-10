from src.core.database import db
from src.core.horses.models.horse import Horse
from src.core.horses.models.horses_file import File


def create_horse(**kwargs):
    
    """
        Crea un objeto Horse en la base de datos con los valores recibidos por parámetro
    """
    employees = kwargs.pop('employees', None)  # Extrae empleados si están presentes
    horse = Horse(**kwargs)
    if employees:
        horse.employees = employees  # Asigna los empleados si están presentes
    
    db.session.add(horse)
    db.session.commit()

    return horse

def create_file(**kwargs):
    file = File(**kwargs)
    db.session.add(file)
    db.session.commit()

    return file


def get_files_by_horse_id(horse_id):

    return File.query.filter_by(horse_id = horse_id).all()

def delete_file_by_id(file_id):

    """Elimina de la base de datos el archivo con el id pasado como parámetro """
    
    print("Este es el file id en la función", file_id)
    file = File.query.filter_by(id = file_id).first()
    print("ESTE ES EL FILE", file)
    db.session.delete(file)
    db.session.commit()

def find_file_by_id(id):

    return File.query.filter_by(id=id).first()

def find_file_by_title(file_title):

    return File.query.filter_by(title=file_title).first()

def updated_file(file, **kwargs):

    allowed_fields = ['file_url', 'file_type', 'document_type', 'title', 'horse_id']
    
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            setattr(file, key, value)
            

    file.upload_date = datetime.now()  # Actualizar la fecha de subida

    db.session.add(file)
    db.session.commit()

    return file
