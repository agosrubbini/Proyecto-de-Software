from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SelectField, FileField, DateField, BooleanField, FormField
from wtforms.validators import InputRequired, Length, Optional


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

class AddressForm(FlaskForm):
    street = StringField("Street", validators=[Optional(), Length(max=255)])
    number = StringField("Number", validators=[Optional(), Length(max=255)])
    department = StringField("Department", validators=[Optional(), Length(max=255)])
    locality = StringField("Locality", validators=[Optional(), Length(max=255)])
    province = StringField("Province", validators=[Optional(), Length(max=255)])
    phone_number = StringField("Phone Number", validators=[Optional(), Length(max=255)])

class EmergencyContactForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=255)])
    phone_number = StringField("Phone Number", validators=[Optional(), Length(max=255)])

class HealthcarePlanForm(FlaskForm):
    social_security = StringField("Social Security", validators=[InputRequired(), Length(max=255)])
    affiliate_number = StringField("Affiliate Number", validators=[InputRequired(), Length(max=255)])
    has_guardianship = BooleanField("Has Guardianship", default=False)
    observation = StringField("Observation", validators=[Optional()])

class EmployeeForm(FlaskForm):
    # Campos de Person
    name = StringField("Name", validators=[InputRequired(), Length(max=255)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=255)])
    dni = StringField("DNI", validators=[InputRequired(), Length(max=12)])
    age = StringField("Age", validators=[InputRequired()])
    phone_number = StringField("Phone Number", validators=[InputRequired(), Length(max=255)])
    
    # Campos de Employee
    profession = StringField('Profession', validators=[InputRequired()])
    job_position = StringField("Job Position", validators=[InputRequired(), Length(max=255)])
    start_date = DateField("Start Date", validators=[InputRequired()])
    end_date = DateField("End Date", validators=[Optional()])
    condition = RadioField("Condition", choices=[
            ('Voluntario', 'Voluntario'),
            ('Personal rentado', 'Personal rentado')
        ], validators=[InputRequired()])
    active = BooleanField("Active", default=True)
    email = StringField("Email", validators=[InputRequired(), Length(max=255)])
    birth_date = DateField("Birth Date", validators=[InputRequired()])
    
    # Campos de Address
    address_id = SelectField("Address", coerce=int, validators=[Optional()])
    new_address = FormField(AddressForm)

    # Campos de EmergencyContact
    emergency_contact = SelectField("Emergency Contact", coerce=int, validators=[Optional()])
    new_emergency_contact = FormField(EmergencyContactForm)

    # Campos de HealthcarePlan
    healthcare_plan = FormField(HealthcarePlanForm)