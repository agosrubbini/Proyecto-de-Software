from src.core.database import db
from src.core.models.persons.person import Person, Employee, JyA, FamilyMemberOrTutor
from src.core.models.persons.address import Address
from src.core.models.persons.emergency_contact import EmergencyContact
from src.core.models.persons.healthcare_plan import HealthcarePlan

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