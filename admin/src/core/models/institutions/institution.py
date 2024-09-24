from src.core.database import db 
from sqlalchemy.dialects.postgresql import ARRAY

class InstitutionalWork(db.Model):

    __tablename__ = "institutional_works"

    id = db.Column(db.Integer, primary_key=True)
    proposal = db.Column(db.Enum("Hipoterapia", "Monta Terapéutica", "Deporte Ecuestre Adaptado", "Actividades Recreativas", 
                                 "Equitación", name="proposal"), nullable=False)
    condition = db.Column(db.Enum("REGULAR", "DE BAJA", name="condition"), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    days = db.Column(ARRAY(db.String), nullable=False)
    professional = db.Column(db.Integer, db.ForeignKey("employees.id"))
    rider = db.Column(db.Integer, db.ForeignKey("employees.id"))
    horse = db.Column(db.Integer, db.ForeignKey("horses.id"))
    auxiliar = db.Column(db.Integer, db.ForeignKey("employees.id"))

class School(db.Model):

    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    addres_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    phone_number = db.Column(db.String(255), nullable=False)
    current_year = db.Column(db.Enum("1ero", "2do", "3ero", "4to", "5to", "6to", name="current_year"), nullable=False)
    observation = db.Column(db.String(255), nullable=False)