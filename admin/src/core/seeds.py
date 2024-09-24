
from datetime import datetime
from src.core.models.auth import create_user, create_role, create_permission
from src.core.models.horses import create_horse
from src.core.models.institutions import create_institutional_work, create_school
from src.core.models.payments import create_payment, create_billing
from src.core.models.persons import create_employee, create_employee, create_JyA, create_family_member_or_tutor, create_address, create_emergency_contact, create_healthcare_plan


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

    person1 = create_person (
        name = "Ramiro",
        last_name = "Alvarez",
        DNI = "123456",
        age = 32,
        phone_number = "222",
        address_id = address1.id
    )

    employee1 = create_employee(
        id = person1.id,
        profession = "Medico",
        job_position = "Jefe",
        emergency_contact_id = emergency_contact1.id,
        condition = "Voluntario",
        healthcare_plan_id = healthcare_plan1.id,
    )

    horse1 = create_horse(

        name = "Mancha",
        date_of_birth = "12/06/2023",
        gender = "Macho",
        race = "Mustang",
        fur = "Blanco y marron",
        purchase_or_donation = "Donacion",
        type_jya_assigned = "Hipoterapia"
    )

    JyA1 = create_JyA(
        birthdate = datetime.now,
        birth_place = "La Plata",
        current_phone = "7777",
        emergency_contact_id = emergency_contact1.id,
        attending_professionals = "Ramiro",
        healthcare_plan_id = healthcare_plan1.id,
        diagnosis = "LESION_POST_TRAUMATICA",
        type_of_disability = "Mental"
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

   
