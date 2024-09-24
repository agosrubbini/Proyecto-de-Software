from src.core.database import db 

class EmergencyContact(db.Model):

    __tablename__ = "emergency_contact"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

    employees = db.relationship("Employee", backref="emergency_contact_employees", foreign_keys="Employee.emergency_contact_id_employee") # Creo que en lugar de tener estas 2 relaciones, deberia haber una tabla intermedia
    JyAs = db.relationship("JyA", backref="emergency_contact_JyAs", foreign_keys="JyA.emergency_contact_id_jya")

    def __init__(self, id=None, name=None, phone_number=None):

        self.id = id
        self.name = name
        self.phone_number = phone_number
        