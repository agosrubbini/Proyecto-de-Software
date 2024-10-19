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

    def __init__(self, id=None, street=None, number=None, department=None, locality=None, province=None, phone_number=None):

        self.id = id 
        self.street = street
        self.number = number
        self.department = department
        self.locality = locality
        self.province = province
        self.phone_number = phone_number

    def __repr__(self):
        return f'{self.street} {self.number} "," {self.department} "," {self.locality} "," {self.province}'
    
    def string(self):
        return f'{self.street} {self.number}, {self.department}, {self.locality}, {self.province}'