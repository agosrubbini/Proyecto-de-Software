from src.core.database import db 
from datetime import datetime

class Payment(db.Model):

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    beneficiary = db.Column(db.Integer, db.ForeignKey("employees.id"))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)
    payment_type = db.Column(db.Enum("Honorarios", "Proveedor", "Gastos Varios", name="payment_type"), nullable=False)
    description = db.Column(db.String(255), nullable=False)

