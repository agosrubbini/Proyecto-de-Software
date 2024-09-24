
from datetime import datetime
from src.core.models.persons.person import Profession, Diagnosis
from src.core.models.auth import create_user, create_role, create_permission
from src.core.models.horses import create_horse
from src.core.models.institutions import create_institutional_work, create_school
from src.core.models.payments import create_payment, create_billing
from src.core.models.persons import (
    create_person, create_employee, create_JyA, create_family_member_or_tutor, create_address, create_emergency_contact, 
    create_healthcare_plan)



def run():

    permission1 = create_permission(
        name="Escribir",
    )

    role1 = create_role(
        name="Administración",
    )

    address1 = create_address (
        street="Calle 45",
        number="985",
        department="5B",
        locality="La Plata",
        province="Buenos Aires",
        phone_number="2241",

    )

    emergency_contact1 = create_emergency_contact(
        name="El celu del abuelo",
        phone_number="4444",
    )

    healthcare_plan1 = create_healthcare_plan(
        social_security = "IOMA",
        affiliate_number = "6666",
        observation = "Se vence en 1 mes",
    )

    employee1 = create_employee(
        name="Ramiro",
        last_name="Alvarez",
        DNI="123456",
        age=32,
        phone_number="222",
        address_id=address1.id,  # Atributos heredados de Person
        profession=Profession.MEDICO,  # Atributo específico de Employee
        job_position="Jefe",
        emergency_contact_id_employee=emergency_contact1.id,
        condition="Voluntario",
        healthcare_plan_id_employee=healthcare_plan1.id
    )

    horse1 = create_horse(
        name = "Mancha",
        date_of_birth = datetime.now(),
        gender = "Macho",
        race = "Mustang",
        fur = "Blanco y marron",
        purchase_or_donation = "Donacion",
        date_of_entry = datetime.now(),
        type_jya_assigned = "Hipoterapia"
    )

    JyA1 = create_JyA(
        name="Joaquina",
        last_name="Saadi",
        DNI="987654",
        age=20,
        phone_number="333",
        address_id=address1.id,
        birthdate = datetime.now(),
        birth_place = "La Plata",
        current_phone = "7777",
        emergency_contact_id_jya = emergency_contact1.id,
        attending_professionals = "Lucia",
        healthcare_plan_id_jya = healthcare_plan1.id,
        diagnosis = Diagnosis.ESCLEROSIS_MULTIPLE,
        type_of_disability = "Mental"
    )

    institutional_work1 = create_institutional_work(
        condicion="Regular",
        proposal = "Hipoterapia",
        location = "La Plata",
        days = ["1","2","3"],
        professional = employee1.id,
        rider = employee1.id,
        horse = horse1.id,
        auxiliar = employee1.id,
    )

    admin_user = create_user(
        email="admin@example.com",
        alias="admin",
        password="hashed_admin_password",  # Asegúrate de usar una contraseña encriptada
        active=True,
        is_blocked=False,
        created_at=datetime.now()
    )

    regular_user = create_user(
        email="user@example.com",
        alias="user123",
        password="hashed_user_password",  # Asegúrate de usar una contraseña encriptada
        active=True,
        is_blocked=False,
        created_at=datetime.now()
    )

    guest_user = create_user(
        email="guest@example.com",
        alias="guest",
        password="hashed_guest_password",  # Asegúrate de usar una contraseña encriptada
        active=True,
        is_blocked=False,
        created_at=datetime.now()
    )

   
