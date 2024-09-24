from src.core.database import db 
from datetime import datetime

class Billing(db.Model):

    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    jya_id = db.Column(db.Integer, db.ForeignKey("horsemen_and_amazons.id"))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)
    payment_method= db.Column(db.Enum("Efectivo", "Tarjeta de Credito", "Tarjeta de Debito", "Otros", name="payment_method"), nullable=False)
    observation = db.Column(db.String(255), nullable=False)