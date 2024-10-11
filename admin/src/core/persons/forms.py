from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SelectField, FileField
from wtforms.validators import InputRequired, Length, EqualTo, Optional



class registryFileForm(FlaskForm):

    file_url = StringField("file_url", validators=[InputRequired(), Length(max=60)])
    file_type = SelectField(
        "File_type",
        validators=[InputRequired()],
        choices=["Link", "Documento"],
    )
    file_url = FileField('File', validators=[Optional()])  # Campo de tipo archivo
    link_url = StringField('Link', validators=[Optional()])  # Campo para ingresar un enlace
    document_type = SelectField(
        "Document_type",
        validators=[InputRequired()],
        choices=["Entrevista", "Evaluación", "Planificación", "Evolución", "Crónicas", "Documental"],
    )
    title = StringField("title", validators=[InputRequired(), Length(max=60)])