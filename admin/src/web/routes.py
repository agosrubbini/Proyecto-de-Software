from flask import session, render_template
from src.core.auth.models.user import User
from src.core.auth import get_user_permissions

def register(app):
    @app.route("/")
    def home():
        user_permissions, user_system_admin = get_user_permissions(session.get("user"))

        context = {
            "user_permissions": user_permissions,
            "user_system_admin": user_system_admin,
        }
        return render_template("home.html", context=context)