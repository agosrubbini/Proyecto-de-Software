
from datetime import datetime
from src.core.auth import create_user, create_role, create_permission, initialice_admin_permissions, initialice_tecnica_permissions, initialice_ecuestre_permissions
from src.core.horses import create_horse
from src.core.institutions import create_institutional_work, create_school
from src.core.payments import create_payment, create_billing
from src.core.persons import (
    create_person, create_employee, create_JyA, create_family_member_or_tutor, create_address, create_emergency_contact, 
    create_healthcare_plan, create_file)



def run():

    print("Creando objetos en la base de datos.... \U0000231B")

    administracion = create_role(
        name="Administración",
    )

    tecnica = create_role(
        name="Técnica",
    )

    ecuestre = create_role(
        name="Ecuestre",
    )

    voluntariado = create_role(
        name="Voluntariado",
    )

    sin_rol = create_role(
        name="Sin rol",
    )

    system_admin = create_user(
        email="system_admin@gmail.com",
        alias="system_admin",
        password="1234",
        role_id=administracion.id,
        system_admin=True,
        active=True,
        is_blocked=False
    )

    user_admin = create_user(
        email="user_admin@gmail.com",
        alias="user_admin",
        password="1234",
        role_id=administracion.id,
        system_admin=False,
        active=True,
        is_blocked=False
    )

    user_tecnica = create_user(
        email="user_tecnica@gmail.com",
        alias="user_tecnica",
        password="1234",
        role_id=tecnica.id,
        system_admin=False,
        active=True,
        is_blocked=False
    )

    user_ecuestre = create_user(
        email="user_ecuestre@gmail.com",
        alias="user_ecuestre",
        password="1234",
        role_id=ecuestre.id,
        system_admin=False,
        active=True,
        is_blocked=False
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

    school1 = create_school(
        name = "Sagrado Corazon",
        addres_id = address1.id,
        phone_number = "2241548363",
        current_year = "1ero",
        observation = "La primer escuela",
    )

    employee1 = create_employee(
        name="Ramiro",
        last_name="Alvarez",
        DNI="123456",
        age=32,
        phone_number="222",
        address_id=address1.id,  # Atributos heredados de Person
        profession= "Médico",  # Atributo específico de Employee
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
        sede = "arg",
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
        diagnosis = "Esclerosis múltiple",
        type_of_disability = "Mental"
    )

    file1 = create_file(
        file_url = "hola",
        file_type = "Link",
        document_type = "Entrevista",
        horsemen_and_amazons_id = JyA1.id,
        title = "LINK DE PRUEBA",
    )

    file2 = create_file(
        file_url = "chau",
        file_type = "Documento",
        document_type = "Evaluación",
        horsemen_and_amazons_id = JyA1.id,
        title = "ARCHIVO DE PRUEBA",
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

    billing1 = create_billing(
        employee_id=employee1.id,
        jya_id=JyA1.id,
        amount=2000,
        payment_method="Efectivo",
        observation="Se abona en efectivo",
    )

    team_index = create_permission(
        name="team_index",
    )

    team_new = create_permission(
        name="team_new",
    )

    team_show = create_permission(
        name="team_show",
    )

    team_update = create_permission(
        name="team_update",
    )

    team_destroy = create_permission(
        name="team_destroy",
    )

    payment_index = create_permission(
        name="payment_index",
    )

    payment_new = create_permission(
        name="payment_new",
    )

    payment_show = create_permission(
        name="payment_show",
    )

    payment_update = create_permission(
        name="payment_update",
    )

    payment_destroy = create_permission(
        name="payment_destroy",
    )

    jya_index = create_permission(
        name="jya_index",
    )
    
    jya_new = create_permission(
        name="jya_new",
    )

    jya_show = create_permission(
        name="jya_show",
    )

    jya_update = create_permission(
        name="jya_update",
    )

    jya_destroy = create_permission(
        name="jya_destroy",
    )

    billing_index = create_permission(
        name="billing_index",
    )

    billing_new = create_permission(
        name="billing_new",
    )

    billing_show = create_permission(
        name="billing_show",
    )

    billing_update = create_permission(
        name="billing_update",
    )

    billing_destroy = create_permission(
        name="billing_destroy",
    )

    horse_index = create_permission(
        name="horse_index",
    )

    horse_new = create_permission(
        name="horse_new",
    )

    horse_show = create_permission(
        name="horse_show",
    )

    horse_update = create_permission(
        name="horse_update",
    )

    horse_destroy = create_permission(
        name="horse_destroy",
    )

    initialice_admin_permissions()
    initialice_tecnica_permissions()
    initialice_ecuestre_permissions()

    print("Objetos creados correctamente \U0001F680")
