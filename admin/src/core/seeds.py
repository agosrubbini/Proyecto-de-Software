
from datetime import datetime
from src.core.models.auth import create_user
def run():
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

   
