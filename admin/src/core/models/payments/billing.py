from src.core.database import db 
from datetime import datetime

class Billing(db.Model):

    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    jya_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now())
    payment_method= db.Column(db.Enum("Efectivo", "Tarjeta de Credito", "Tarjeta de Debito", "Otros", name="payment_method"), nullable=False)
    observation = db.Column(db.String(255), nullable=False)

    def __init__(self, id=None, jya_id=None, amount=None, payment_date=None, payment_method=None, observation=None):

        self.id = id 
        self.jya_id = jya_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.observation = observation