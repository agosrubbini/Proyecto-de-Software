from src.core.database import db 


class Address(db.Model):

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

    persons = db.relationship("Person",backref="persons")