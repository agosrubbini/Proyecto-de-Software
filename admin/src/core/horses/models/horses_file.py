from src.core.database import db
from datetime import datetime


class Horse_file(db.Model):

    __tablename__ = "horses_files"

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(1000), nullable=False)
    file_type = db.Column(db.Enum("Link", "Documento", name='file_type'), nullable=False)
    document_type = db.Column(db.Enum("Ficha general del caballo", "Planificacion de entrenamiento", "Informe de evolucion", "Carga de imagenes", "Registro veterinario", name='document_type'), nullable=False)
    horses_id = db.Column(db.Integer, db.ForeignKey('horses.id'), nullable=False)
    title = db.Column(db.String(70), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.now())

def __init__(self, id=None, file_url=None, file_type=None, document_type=None, horses_id=None, title=None, upload_date=None):

        self.id = id 
        self.file_url = file_url
        self.file_type = file_type
        self.document_type = document_type
        self.horses_id = horses_id
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
