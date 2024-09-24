from src.core.database import db 

class EmergencyContact(db.Model):

    __tablename__ = "emergency_contact"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

    employees = db.relationship("Employee", backref="employees") # Creo que en lugar de tener estas 2 relaciones, deberia haber una tabla intermedia
    JyAs = db.relationship("JyA", backref="JyAs")