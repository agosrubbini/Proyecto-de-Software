from src.core.database import db
from datetime import datetime
import enum

class File(db.Model):

    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.Enum("Link", "Documento", name='file_type'), nullable=False)
    document_type = db.Column(db.Enum("Entrevista", "Evaluacion", "Planificación", "Evolucion", "Cronicas", "Documental", name='document_type'), nullable=False)
    horsemen_and_amazons_id = db.Column(db.Integer, db.ForeignKey('horsemen_and_amazons.id'), nullable=False)
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