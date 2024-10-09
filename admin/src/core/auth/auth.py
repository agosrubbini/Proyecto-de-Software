from functools import wraps
from flask import abort, session, redirect, url_for, g
from src.core.auth.models.user import User
from src.core.auth import get_user_permissions

# Decorador para verificar si el usuario tiene un permiso específico
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_mail = session.get("user")

            if not user_mail:
                return redirect(url_for('login.login'))  # Redirigir a inicio de sesión

            user = User.query.filter_by(email=user_mail).first()
            user_permissions = {perm.name for perm in user.role.permissions}

            if permission not in user_permissions and not user.system_admin:
                abort(401)  # Acceso prohibido si no encuentra el permiso

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def inject_user_permissions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener los permisos del usuario
        user_permissions, user_system_admin = get_user_permissions(session.get("user"))
        
        # Inyectar permisos y estado de admin en 'g'
        g.user_permissions = user_permissions
        g.user_system_admin = user_system_admin
        
        # Llamar a la función decorada
        return f(*args, **kwargs)

    return decorated_function