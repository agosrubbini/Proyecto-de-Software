from flask import session, render_template
from src.core.auth.models.user import User
from src.core.auth import get_user_permissions

def register(app):
    @app.route("/")
    def home():
        user_permissions = get_user_permissions(session.get("user"))

        context = {
            "user_permissions": user_permissions
        }
        return render_template("home.html", context=context)