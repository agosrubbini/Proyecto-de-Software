from src.core.database import db
from src.core.horses.models.horse import Horse


def create_horse(**kwargs):
    
    """
        Crea un objeto Horse en la base de datos con los valores recibidos por parámetro
    """
    
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()

    return horse