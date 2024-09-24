from src.core.database import db 
from datetime import datetime

class Payment(db.Model):

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    beneficiary = db.Column(db.Integer, db.ForeignKey("persons.id"))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)
    payment_type = db.Column(db.Enum("Honorarios", "Proveedor", "Gastos Varios", name="payment_type"), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, id=None, beneficiary=None, amount=None, payment_date=None, payment_type=None, description=None):

        self.id = id 
        self.beneficiary = beneficiary
        self.amount = amount
        self.payment_date = payment_date
        self.payment_type = payment_type
        self.description = description

