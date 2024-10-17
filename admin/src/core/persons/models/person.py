from src.core.database import db 
from datetime import datetime
import enum

class Profession(enum.Enum):
    
    PSICOLOGO = "psicologo/a"
    PSICOMOTRICISTA = "psicomotricista"
    MEDICO = "medico/a"
    KINESIOLOGO = "kinesiologo/a" 
    TERAPISTA_OCUPACIONAL = "terapista_ocupacional"
    PSICOPEDAGOGO = "psicopedagogo/a"
    DOCENTE = "docente"
    PROFESOR = "profesor"
    FONOAUDIOLOGO = "fonoaudiologo/a"
    VETERINARIO = "veterinario/a"
    OTRO = "otro"

class Diagnosis(enum.Enum):

    ECNE = "ECNE"
    LESION_POST_TRAUMATICA = "lesion_post_traumatica"
    MIELOMENINGOCELE = "mielomeningocele" 
    ESCLEROSIS_MULTIPLE = "esclerosis multiple"
    ESCOLIOSIS_LEVE = "escoliosis_leve"
    SECUELAS_ACV = "secuelas_de_ACV"
    DISCAPACIDAD_INTELECTUAL = "discapacidad_intelectual"
    TRASTORNO_ESPECTRO_AUTISTA = "trastorno_del_espectro_autista"
    TRASTORNO_DEL_APRENDIZAJE = "trastorno_del_aprendizaje"
    TRASTORNO_POR_DEFICIT_DE_ATENCION = "trastorno_por_deficit_de_atencion/hiperactividad"
    TRASTORNO_DE_LA_COMUNICACION = "trastorno_de_la_comunicacion"
    TRASTORNO_DE_ANSIEDAD = "trastorno_de_ansiedad"
    SINDROME_DE_DOWN = "sindrome_de_down"
    RETRASO_MADURATIVO = "retraso_madurativo"
    PSICOSIS = "psicosis"
    TRASTORNO_DE_CONDUCTA = "trastorno_de_conducta"
    TRASTORNOS_DEL_ANIMO_Y_AFECTIVOS = "trastornos_del_animo_y_afectivos"
    TRASTORNO_ALIMENTARIO = "trastorno_alimentario"
    OTRO = "otro"

class Person(db.Model):
    
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    DNI = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Discriminator column to track which subclass it is
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'person',  # Nombre base
        'polymorphic_on': type  # Define qué columna discrimina la subclase
    }

    def __init__(self, id=None, name=None, last_name=None, DNI=None, age=None, phone_number=None, address_id=None, user_id=None):

        self.id = id 
        self.name = name
        self.last_name = last_name
        self.DNI = DNI
        self.age = age
        self.phone_number = phone_number
        self.address_id = address_id
        self.user_id = user_id

class Employee(Person):

    __tablename__ = "employees"

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    profession = db.Column(db.Enum(Profession), nullable=False)
    job_position = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, default = datetime.now)
    end_date = db.Column(db.DateTime)
    emergency_contact_id_employee = db.Column(db.Integer, db.ForeignKey("emergency_contact.id"), nullable=True)
    condition = db.Column(db.Enum("Voluntario", "Personal Rentado", name="condition"), nullable=False)
    active = db.Column(db.Boolean, default=True)
    healthcare_plan_id_employee = db.Column(db.Integer, db.ForeignKey("healthcare_plan.id"), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    # degree  = db.Column(db.String(255), nullable=True)--> Se debe poder subir un archivo, se guarda la ruta?
    # DNI_copy = db.Column(db.String(255), nullable=True)  --> Se debe poder subir un archivo, se guarda la ruta?
    # updated_CV = db.Columnt(db.String(255), nullable=True) --> Se debe poder subir un archivo, se guarda la ruta?
    

    # emergency_contact = db.relationship("EmergencyContact", backref="emergency_contact") # Creo que no es necesario porque ya tengo el id
    # healthcare_plan = db.relationship("HealthcarePlan", backref="healthcare_plan") # Creo que no es necesario porque ya tengo el id
    billings = db.relationship("Billing", backref="billings_employee", foreign_keys="Billing.employee_id")
    payments = db.relationship("Payment", backref="payments")
    institutional_works = db.relationship("InstitutionalWork", backref="institutional_works", foreign_keys="InstitutionalWork.professional")

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
    }

    def __init__(self, name=None, last_name=None, DNI=None, age=None, phone_number=None, address_id=None, user_id=None, 
                 profession=None, job_position=None, start_date=None, end_date=None, emergency_contact_id_employee=None, 
                 condition=None, active=None, healthcare_plan_id_employee=None, email=None, birth_date=None):

        super().__init__(name=name, last_name=last_name, DNI=DNI, age=age, phone_number=phone_number, address_id=address_id, user_id=user_id)
        self.profession = profession
        self.job_position = job_position
        self.start_date = start_date
        self.end_date = end_date
        self.emergency_contact_id_employee = emergency_contact_id_employee
        self.condition = condition
        self.active = active
        self.healthcare_plan_id_employee = healthcare_plan_id_employee
        self.email = email
        self.birth_date = birth_date

class JyA(Person):

    __tablename__ = "horsemen_and_amazons"

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    birthdate = db.Column(db.DateTime, nullable = False)
    birth_place = db.Column(db.String(255), nullable=False)
    current_phone = db.Column(db.String(255), nullable=False)
    emergency_contact_id_jya = db.Column(db.Integer, db.ForeignKey("emergency_contact.id"), nullable=True)
    is_scholarshipped = db.Column(db.Boolean, default=False)
    scholarship_percentage = db.Column(db.String(255), nullable=True)
    attending_professionals = db.Column(db.String(255), nullable=False)
    healthcare_plan_id_jya = db.Column(db.Integer, db.ForeignKey("healthcare_plan.id"), nullable=True)
    has_disability_certificate =  db.Column(db.Boolean, default=False)
    diagnosis = db.Column(db.Enum(Diagnosis), nullable=False)
    other_diagnosis = db.Column(db.String(255), nullable=True)
    type_of_disability = db.Column(db.Enum("Mental", "Motora", "Sensorial", "Visceral", name="type_of_disability"), nullable=True)
    receives_family_allowance = db.Column(db.Boolean, default=False)
    family_allowance = db.Column(db.Enum("Asignación Universal por hijo","Asignación Universal por hijo con Discapacidad", "Asignación por ayuda escolar anual", name="family_allowance"), nullable=True)
    is_beneficiary_of_pension = db.Column(db.Boolean, default=False)
    pension = db.Column(db.Enum("Nacional", "Provincial", name="pension"), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)

    # emergency_contact = db.relationship("EmergencyContact", backref="emergency_contact") Creo que no seria necesario porque ya tengo el id
    # healthcare_plan = db.relationship("HealthcarePlan", backref="healthcare_plan") Creo que no seria necesario porque ya tengo el id
    # school = db.relationship("School", backref="school") Creo que no seria necesario porque ya tengo el id

    billings = db.relationship("Billing", backref="billings_jya", foreign_keys="Billing.jya_id")
    files = db.relationship("File", backref="files")

    __mapper_args__ = {
        'polymorphic_identity': 'jya',
    }

    def __init__(self, name=None, last_name=None, DNI=None, age=None, phone_number=None, address_id=None, user_id=None, 
                       birthdate=None, birth_place=None, current_phone=None, emergency_contact_id_jya=None, is_scholarshipped=None, 
                       scholarship_percentage=None, attending_professionals=None, healthcare_plan_id_jya=None, 
                       has_disability_certificate=None, diagnosis=None, other_diagnosis=None, type_of_disability=None,
                       receives_family_allowance=None, family_allowance=None, is_beneficiary_of_pension=None,pension=None, school_id=None):
        
        super().__init__(name=name, last_name=last_name, DNI=DNI, age=age, phone_number=phone_number, address_id=address_id, user_id=user_id)
        self.birthdate = birthdate
        self.birth_place = birth_place
        self.current_phone = current_phone
        self.emergency_contact_id_jya = emergency_contact_id_jya
        self.is_scholarshipped = is_scholarshipped
        self.scholarship_percentage = scholarship_percentage
        self.attending_professionals = attending_professionals
        self.healthcare_plan_id_jya = healthcare_plan_id_jya
        self.has_disability_certificate = has_disability_certificate
        self.diagnosis = diagnosis
        self.other_diagnosis = other_diagnosis
        self.type_of_disability = type_of_disability
        self.receives_family_allowance = receives_family_allowance
        self.family_allowance = family_allowance
        self.is_beneficiary_of_pension = is_beneficiary_of_pension
        self.pension = pension
        self.school_id = school_id
    
    def to_dict(self, addres):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "DNI": self.DNI,
            "age": self.age,
            "phone_number": self.phone_number,
            "address": addres,
        }

class FamilyMemberOrTutor(Person):

    __tablename__ = "family_member_or_tutor"

    id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
    kinship = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    maximum_level_or_education = db.Column(db.Enum("Primario", "Secundario", "Terciario", "Universitario", name="maximum_level_or_education"),nullable=False)
    activity_or_occupation = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'family_member_or_tutor',
    }

    def __init__(self, name=None, last_name=None, DNI=None, age=None, phone_number=None, address_id=None, user_id=None,
                       kinship=None, email=None, maximum_level_or_education=None, activity_or_occupation=None):

        super().__init__(name=name, last_name=last_name, DNI=DNI, age=age, phone_number=phone_number, address_id=address_id, user_id=user_id)
        self.kinship = kinship
        self.email = email
        self.maximum_level_or_education = maximum_level_or_education
        self.activity_or_occupation = activity_or_occupation

        