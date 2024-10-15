from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SelectField, FileField, IntegerField, DateField, BooleanField
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


class registryHorsemanForm(FlaskForm):

    
    name = StringField("name", validators=[InputRequired(), Length(max=60)])
    last_name = StringField("last_name", validators=[InputRequired(), Length(max=60)])
    DNI = StringField("dni", validators=[InputRequired(), Length(max=60)])
    age = IntegerField("age", validators=[InputRequired()])
    phone_number = StringField("phone_number", validators=[InputRequired(), Length(max=60)])
    address = SelectField(
        "address",
        validators=[InputRequired()],
        choices=[],
    )
    birthdate = DateField("birthdate", validators=[InputRequired()])
    birth_place = StringField("birth_place", validators=[InputRequired(), Length(max=60)])
    current_phone = StringField("current_phone", validators=[InputRequired(), Length(max=60)])
    emergency_contact_id_jya = SelectField(
        "emergency_contact_id_jya",
        validators=[InputRequired()],
        choices=[],
    )
    is_scholarshipped = BooleanField("is_scholarshipped", validators=[Optional()])
    scholarship_percentage = StringField("scholarship_percentage", validators=[Optional(), Length(max=60)])
    attending_professionals = StringField("attending_professionals", validators=[InputRequired(), Length(max=60)])
    healthcare_plan_id_jya = SelectField(
        "healthcare_plan_id_jya",
        validators=[InputRequired()],
        choices=[],
    )
    has_disability_certificate =  BooleanField("has_disability_certificate", validators=[Optional()])
    diagnosis = SelectField(
        "diagnosis",
        validators=[Optional()],
        choices = [("No posee ningún diagnóstico", "Selecciona un diagnóstico"), ("Ecne", "ECNE"), ("Lesión post traumática", "LESIÓN POST TRAUMÁTICA"), ("Mielomeningocele", "MIELOMENINGOCELE"),
                   ("Esclerosis múltiple", "ESCLEROSIS MÚLTIPLE"), ("Escoliosis leve", "ESCOLIOSIS LEVE"), ("Secuelas acv", "SECUELAS ACV"), ("Discapacidad intelectual", "DISCAPACIDAD INTELECTUAL"),
                   ("Trastorno espectro autista", "TRASTORNO ESPECTRO AUTISTA"), ("Trastorno del aprendizaje", "TRASTORNO DEL APRENDIZAJE"), ("Trastorno por déficit de atención", "TRASTORNO POR DEFICIT DE ATENCIÓN"),
                   ("Trastorno de la comunicación", "TRASTORNO DE LA COMUNICACIÓN"), ("Trastorno de ansiedad", "TRASTORNO DE ANSIEDAD"), ("Síndrome de down", "SINDROME DE DOWN"),
                   ("Retraso madurativo", "RETRASO MADURATIVO"), ("Psicosis", "PSICOSIS"), ("Trastorno de conducta", "TRASTORNO DE CONDUCTA"), ("Trastornos del ánimo y afectivos", "TRASTORNOS DEL ÁNIMO Y AFECTIVOS"),
                   ("Trastorno alimentario", "TRASTORNO ALIMENTARIO"), ("Otro", "OTRO")]

    )
    other_diagnosis = StringField("other_diagnosis", validators=[Optional(), Length(max=60)])
    type_of_disability = SelectField(
        "type_of_disability",
        validators=[Optional()],
        choices = [("No padece una discapacidad", "Selecciona un tipo de discapacidad"), ("Mental", "Mental"), ("Motora", "Motora"), ("Sensorial", "Sensorial"), ("Visceral", "Visceral")]
    )
    receives_family_allowance = BooleanField("receives_family_allowance", validators=[Optional()])
    family_allowance =  SelectField(
        "family_allowance",
        validators=[Optional()],
        choices = [("No recibe asignación", "Selecciona una asignación"), ("Asignación universal por hijo", "Asignación universal por hijo"), ("Asignación universal por hijo con discapacidad", "Asignación universal por hijo con discapacidad"),
                   ("Asignación por ayuda escolar anual", "Asignación por ayuda escolar anual")]
    )
    is_beneficiary_of_pension = BooleanField("is_beneficiary_of_pension", validators=[Optional()])
    pension = SelectField(
        "pension",
        validators=[Optional()],
        choices=[("No recibe pensión","Selecciona una pensión"),("Nacional","Nacional"), ("Provincial","Provincial")],
    )
    school = SelectField(
        "school",
        validators=[InputRequired()],
        choices=[],
    )

    def validate(self, extra_validators=None):
        # Llama a la validación predeterminada, pasando extra_validators
        rv = FlaskForm.validate(self, extra_validators=extra_validators)
        if not rv:
            return False

        # Verifica si la casilla de beca está marcada
        if self.is_scholarshipped.data:
            # Si el campo de porcentaje de beca está vacío cuando la casilla está marcada, lanza un error
            if not self.scholarship_percentage.data:
                self.scholarship_percentage.errors.append("Este campo es obligatorio cuando está becado.")
                return False
        
        if self.has_disability_certificate.data:

            if self.diagnosis.data == "No posee ningún diagnóstico":
                self.has_disability_certificate.errors.append("Este campo es obligatorio cuando el jinete tiene un certificado de discapacidad")
                return False
            
            if self.diagnosis.data == "Otro":
                
                if not self.other_diagnosis.data:
                    self.has_disability_certificate.errors.append("Este campo es obligatorio cuando el diagnóstico es otro")
                    return False

            if self.type_of_disability.data == "No padece una discapacidad":
                self.has_disability_certificate.errors.append("Este campo es obligatorio cuando el jinete tiene un certificado de discapacidad")
                return False

        if self.receives_family_allowance.data:
            
            if self.family_allowance.data == "No recibe asignación":
                self.receives_family_allowance.errors.append("Este campo es obligatorio cuando el jinete recibe asignación familiar")
                return False
        
        if self.is_beneficiary_of_pension.data:

            if self.pension.data == "No recibe pensión":
                self.is_beneficiary_of_pension.errors.append("Este campo es obligatorio cuando el jinete recibe alguna pensión")
                return False

        return True
   