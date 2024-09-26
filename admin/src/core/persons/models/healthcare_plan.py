from src.core.database import db 

class HealthcarePlan(db.Model):

    __tablename__ = "healthcare_plan"

    id = db.Column(db.Integer, primary_key=True)
    social_security = db.Column(db.String(255), nullable=False)
    affiliate_number = db.Column(db.String(255), nullable=False)
    has_guardianship = db.Column(db.Boolean, default=False)
    observation = db.Column(db.String(255), nullable=True)


    employees = db.relationship("Employee", backref="healthcare_plan_employees", foreign_keys="Employee.healthcare_plan_id_employee") # Creo que en lugar de tener estas 2 relaciones, deberia haber una tabla intermedia
    JyAs = db.relationship("JyA", backref="healthcare_plan_JyAs", foreign_keys="JyA.healthcare_plan_id_jya")

    def __init__(self, id=None, social_security=None, affiliate_number=None, has_guardianship=None, observation=None):

        self.id = id 
        self.social_security = social_security
        self.affiliate_number = affiliate_number
        self.has_guardianship = has_guardianship
        self.observation = observation