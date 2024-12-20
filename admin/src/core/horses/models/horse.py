from src.core.database import db 
from sqlalchemy.dialects.postgresql import ARRAY

horse_employee = db.Table(
    "horse_employee",
    db.Column("horses_id", db.Integer, db.ForeignKey("horses.id")),
    db.Column("employee_id", db.Integer, db.ForeignKey("persons.id")),
)


class Horse(db.Model):

    __tablename__ = "horses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Enum("Macho", "Hembra", name="gender"), nullable=False) 
    race = db.Column(db.String(255), nullable=False)
    fur = db.Column(db.String(255), nullable=False)
    purchase_or_donation = db.Column(db.Enum("Compra", "Donación", name="purchase_or_donation"), nullable=False) 
    date_of_entry = db.Column(db.DateTime, nullable=False)
    sede = db.Column(db.String(255),nullable=False)
    type_jya_assigned = db.Column(ARRAY(db.String), nullable=False) 
    
    employees = db.relationship("Employee", secondary=horse_employee, backref="horse")

    files = db.relationship("Horse_file", backref="horse" , cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'ecuestre',
    }

    def __init__(self, id=None, name=None, date_of_birth=None, gender=None, race=None, fur=None, purchase_or_donation=None, date_of_entry=None, sede=None,type_jya_assigned=None, employees=None):

        self.id = id 
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.race = race
        self.fur = fur
        self.purchase_or_donation = purchase_or_donation
        self.date_of_entry = date_of_entry
        self.sede = sede
        self.type_jya_assigned = type_jya_assigned
        #self.employees = employees


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime('%d-%m-%Y'),
            "date_of_entry": self.date_of_entry.strftime('%d-%m-%Y'),
            "gender": self.gender,
            "race": self.race,
            "fur": self.fur,
            "purchase_or_donation": self.purchase_or_donation,
            "sede": self.sede,
            "type_jya_assigned": self.type_jya_assigned,
            # Serializamos los empleados en una lista de diccionarios con su información relevante
        "employees": [
            {
                "id": emp.id,
                "name": emp.name,
            }
            for emp in self.employees
        ],
        }
