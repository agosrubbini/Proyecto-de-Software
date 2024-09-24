from src.core.database import db 
from datetime import datetime
import enum
#from src.core.persons import Address

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
    age = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=True)


class Employee(Person):

    __tablename__ = "employees"

    profession = db.Column(db.Enum(Profession), nullable=False)
    job_position = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, default = datetime.now)
    end_date = db.Column(db.DateTime)
    emergency_contact_id = db.Column(db.Integer, db.ForeignKey("emergency_contact.id"), nullable=True)
    condition = db.Column(db.Enum("Voluntario", "Personal Rentado", name="condition"), nullable=False)
    active = db.Column(db.Boolean, default=True)
    healthcare_plan_id = db.Column(db.Integer, db.ForeignKey("healthcare_plan.id"), nullable=True)
    # degree  = db.Column(db.String(255), nullable=True)--> Se debe poder subir un archivo, se guarda la ruta?
    # DNI_copy = db.Column(db.String(255), nullable=True)  --> Se debe poder subir un archivo, se guarda la ruta?
    # updated_CV = db.Columnt(db.String(255), nullable=True) --> Se debe poder subir un archivo, se guarda la ruta?
    

    # emergency_contact = db.relationship("EmergencyContact", backref="emergency_contact") # Creo que no es necesario porque ya tengo el id
    # healthcare_plan = db.relationship("HealthcarePlan", backref="healthcare_plan") # Creo que no es necesario porque ya tengo el id
    billings = db.relationship("Billing", backref="billings")
    payments = db.relationship("Payment", backref="payments")
    institutional_works = db.relationship("InstitutionalWork", backref="institutional_works")


class JyA(Person):

    __tablename__ = "horsemen_and_amazons"

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
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=True)

    # emergency_contact = db.relationship("EmergencyContact", backref="emergency_contact") Creo que no seria necesario porque ya tengo el id
    # healthcare_plan = db.relationship("HealthcarePlan", backref="healthcare_plan") Creo que no seria necesario porque ya tengo el id
    # school = db.relationship("School", backref="school") Creo que no seria necesario porque ya tengo el id

    billings = db.relationship("Billing", backref="billings")
    
class FamilyMemberOrTutor(Person):

    __tablename__ = "family_member_or_tutor"

    kinship = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    maximum_level_or_education = db.Column(db.Enum("Primario", "Secundario", "Terciario", "Universitario", name="maximum_level_or_education"),nullable=False)
    activity_or_occupation = db.Column(db.String(255), nullable=False)