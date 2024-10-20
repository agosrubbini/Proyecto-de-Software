from src.core.database import db 
from sqlalchemy.dialects.postgresql import ARRAY


class InstitutionalWork(db.Model):

    __tablename__ = "institutional_works"

    id = db.Column(db.Integer, primary_key=True)
    condicion = db.Column(db.Enum("Regular", "De Baja", name="condicion"), nullable=False)
    proposal = db.Column(db.Enum("Hipoterapia", "Monta Terapeutica", "Deporte Ecuestre Adaptado", "Actividades Recreativas", "Equitacion", name="proposal"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    days = db.Column(ARRAY(db.String), nullable=False)
    professional = db.Column(db.Integer, db.ForeignKey("persons.id"))
    rider = db.Column(db.Integer, db.ForeignKey("persons.id"))
    horse = db.Column(db.Integer, db.ForeignKey("horses.id", ondelete='CASCADE'))
    auxiliar = db.Column(db.Integer, db.ForeignKey("persons.id"))

    def __init__(self, id=None, proposal=None, condicion=None, location=None, days=None, professional=None, rider=None, horse=None, auxiliar=None):

        self.id = id 
        self.proposal = proposal
        self.condicion = condicion
        self.location = location
        self.days = days
        self.professional = professional
        self.rider = rider
        self.horse = horse
        self.auxiliar = auxiliar

class School(db.Model):

    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    addres_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    phone_number = db.Column(db.String(255), nullable=False)
    current_year = db.Column(db.Enum("1ero", "2do", "3ero", "4to", "5to", "6to", name="current_year"), nullable=False)
    observation = db.Column(db.String(255), nullable=False)

    def __init__(self, id=None, name=None, addres_id=None, phone_number=None, current_year=None, observation=None):
        
        self.id = id
        self.name = name
        self.addres_id = addres_id
        self.phone_number = phone_number
        self.current_year = current_year
        self.observation = observation