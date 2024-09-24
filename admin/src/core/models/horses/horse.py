from src.core.database import db 

"""horse_employee = db.Table(
    "horse_employee",
    db.Column("horse_id", db.Integer, db.ForeignKey("horses.id")),
    db.Column("employee_id", db.Integer, db.ForeignKey("employees.id"))
)"""


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
    type_jya_assigned = db.Column(db.Enum("Hipoterapia", "Monta Terapeutica", "Deporte Ecuestre Adaptado", 
                                          "Actividades Recreativas", "Equitacion", name="type_jya_assigned"), nullable=False) 
    
    #employees = db.relationship("Employee", secondary=horse_employee, backref="horse")  


