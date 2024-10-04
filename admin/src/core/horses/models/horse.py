from src.core.database import db 

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
    purchase_or_donation = db.Column(db.Enum("Compra", "Donacion", name="purchase_or_donation"), nullable=False) 
    date_of_entry = db.Column(db.DateTime, nullable=False)
    sede = db.Column(db.String(255),nullable=False)
    type_jya_assigned = db.Column(db.Enum("Hipoterapia", "Monta Terapeutica", "Deporte Ecuestre Adaptado", 
                                          "Actividades Recreativas", "Equitacion", name="type_jya_assigned"), nullable=False) 
    
    employees = db.relationship("Employee", secondary=horse_employee, backref="horse")  

    def __init__(self, id=None, name=None, date_of_birth=None, gender=None, race=None, fur=None, purchase_or_donation=None, date_of_entry=None, sede=None,type_jya_assigned=None):

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

