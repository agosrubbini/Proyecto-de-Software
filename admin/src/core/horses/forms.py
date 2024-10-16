from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SelectMultipleField, SelectField, FileField, BooleanField
from wtforms.validators import InputRequired, Length, Optional



class create_horse_Form(FlaskForm):

    name = StringField("Nombre", validators=[InputRequired(), Length(max=15)])

    date_of_birth = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[InputRequired()])

    gender = SelectField(
        'Genero',
        choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')]
    )
    
    race = StringField("Raza", validators=[InputRequired(), Length(max=15)])

    fur = StringField("Pelaje", validators=[InputRequired(), Length(max=15)])

    purchase_or_donation = SelectField(
        'Compra o Donacion',
        choices=[('Compra','Compra'), ('Donacion','Donacion')]#revisar
    )

    date_of_entry = DateField('Fecha de ingreso', format='%Y-%m-%d', validators=[InputRequired()])

    sede = StringField("Sede", validators=[InputRequired(), Length(max=255)])

    type_jya_hipoterapia = BooleanField (default=False) 
    type_jya_monta_terapeutica = BooleanField (default=False) 
    type_jya_dea = BooleanField (default=False) 
    type_jya_ar = BooleanField (default=False) 
    type_jya_equitacion = BooleanField (default=False) 
    
    

    #employees = StringField("Asociar entrenadores y conductores", validators=[InputRequired(), Length(max=15)]) #terminar de hacer 

    employees = SelectMultipleField('Empleados', coerce=int)
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
        choices=["Ficha general del caballo", "Planificacion de entrenamiento", "Informe de evolucion", "Carga de imagenes", "Registro veterinario"],
    )
    title = StringField("title", validators=[InputRequired(), Length(max=60)])

#editar eliminar
#busqueda nombre y tipo de jya asignados
#documentacion y enlaces
#filtros y ordenamientos para docs