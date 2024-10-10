from flask import render_template
from src.core.auth.models.user import User
from src.core.auth.auth import inject_user_permissions

def register(app):
    @app.route("/")
    @inject_user_permissions
    def home():
        return render_template("home.html")