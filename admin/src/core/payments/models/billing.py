from src.core.database import db
from datetime import datetime

class Billing(db.Model):
    __tablename__ = "billings"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    jya_id = db.Column(db.Integer, db.ForeignKey('persons.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    observation = db.Column(db.String(255))
    payment_date = db.Column(db.DateTime, default=datetime.now)

    employee = db.relationship("Employee", back_populates="billings", foreign_keys=[employee_id], overlaps="billings_employee")
    jya = db.relationship("JyA", back_populates="billings", foreign_keys=[jya_id], overlaps="billings_jya")