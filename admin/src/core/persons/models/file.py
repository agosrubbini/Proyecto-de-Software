from src.core.database import db
from datetime import datetime
import enum

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.Enum('entrevista', 'evaluación', 'planificación', 'evolución', 'cronicas', 'documental', name='file_type'), nullable=False)
    jinete_amazonas_id = db.Column(db.Integer, db.ForeignKey('jinete_amazonas.id'), nullable=False)
    title = db.Column(db.String(70), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.now())
    
    # Additional metadata fields (upload date, size, etc.)