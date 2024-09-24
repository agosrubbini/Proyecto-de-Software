from src.core.database import db
from src.core.models.institutions.institution import School, InstitutionalWork


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