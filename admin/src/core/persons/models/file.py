from src.core.database import db
from datetime import datetime

class File(db.Model):

    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(1000), nullable=False)
    file_type = db.Column(db.Enum("Link", "Documento", name='file_type'), nullable=False)
    document_type = db.Column(db.Enum("Entrevista", "Evaluación", "Planificación", "Evolución", "Crónicas", "Documental", name='document_type'), nullable=False)
    horsemen_and_amazons_id = db.Column(db.Integer, db.ForeignKey('horsemen_and_amazons.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(70), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.now())
    
    # Additional metadata fields (upload date, size, etc.)

    def __init__(self, id=None, file_url=None, file_type=None, document_type=None, horsemen_and_amazons_id=None, title=None, upload_date=None):

        self.id = id 
        self.file_url = file_url
        self.file_type = file_type
        self.document_type = document_type
        self.horsemen_and_amazons_id = horsemen_and_amazons_id
        self.title = title

    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "upload_date": self.upload_date.strftime('%Y-%m-%d'),
            "file_url": self.file_url,
            "file_type": self.file_type,
            "document_type": self.document_type,
        }
    
class EmployeeFile(db.Model):

    __tablename__ = "employee_files"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=True)
    document_type = db.Column(db.Enum("Titulo", "Copia DNI", "CV Actualiazdo", name='document_type'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.now())
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    
    # Additional metadata fields (upload date, size, etc.)

    def __init__(self, id=None, document_type=None, employee_id=None, title=None):

        self.id = id 
        self.document_type = document_type
        self.employee_id_id = employee_id
        self.title = title

    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "upload_date": self.upload_date.strftime('%Y-%m-%d'),
            "document_type": self.document_type,
        }