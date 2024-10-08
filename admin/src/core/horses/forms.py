from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SelectMultipleField
from wtforms.validators import InputRequired, Length



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

    type_jya_assigned = SelectField(
        'Tipo de Jinetes y Amazonas asignados',
        choices=[("Hipoterapia", "Hipoterapia"), 
                 ("Monta Terapeutica", "Monta Terapeutica"), 
                 ("Deporte Ecuestre Adaptado", "Deporte Ecuestre Adaptado"),
                 ("Actividades Recreativas", "Actividades Recreativas"), 
                 ("Equitación", "Equitación")]  # revisar
    )

    employees = StringField("Asociar entrenadores y conductores", validators=[InputRequired(), Length(max=15)]) #terminar de hacer 

    employees = SelectMultipleField(
        "Asociar entrenadores y conductores", 
        choices=[],  # Se cargará dinámicamente con los empleados disponibles
        coerce=int  # Convertirá el valor a entero (ID de empleados)
    )

#editar eliminar
#busqueda nombre y tipo de jya asignados
#documentacion y enlaces
#filtros y ordenamientos para docs