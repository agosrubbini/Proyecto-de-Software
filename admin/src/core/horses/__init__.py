from src.core.database import db
from src.core.horses.models.horse import Horse


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