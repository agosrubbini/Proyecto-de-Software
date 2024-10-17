from src.core.database import db
from src.core.institutions.models.institution import School, InstitutionalWork


def create_institutional_work(**kwargs):
    institutional_work = InstitutionalWork(**kwargs)
    db.session.add(institutional_work)
    db.session.commit()

    return institutional_work

def create_school(**kwargs):
    school = School(**kwargs)
    db.session.add(school)
    db.session.commit()

    return school

def get_schools():

    "Retorna todas las escuelas existentes en la base de datos"

    return School.query.all()


def get_school_by_id(school_id):

    """Devuelve la escuela con el id pasado por parámetro"""

    return School.query.filter_by(id=school_id).first()