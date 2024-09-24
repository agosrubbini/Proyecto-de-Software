from src.core.database import db 

class HealthcarePlan(db.Model):

    __tablename__ = "healthcare_plan"

    id = db.Column(db.Integer, primary_key=True)
    social_security = db.Column(db.String(255), nullable=False)
    affiliate_number = db.Column(db.String(255), nullable=False)
    has_guardianship = db.Column(db.Boolean, default=False)
    observation = db.Column(db.String(255), nullable=True)


    employees = db.relationship("Employee", backref="employees") # Creo que en lugar de tener estas 2 relaciones, deberia haber una tabla intermedia
    JyAs = db.relationship("JyA", backref="JyAs")