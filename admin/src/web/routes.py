from flask import redirect, render_template, url_for
from src.core.auth.models.user import User
from src.core.auth.auth import inject_user_permissions
from authlib.integrations.flask_client import OAuth

def register(app):
    @app.route("/")
    @inject_user_permissions
    def home():
        return render_template("home.html")
    
    @app.route('/login')
    def login():
        google = OAuth.create_client('google')
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route('/authorize')
    def authorize():
        google = OAuth.create_client('google')
        token = google.authorize_access_token()
        resp = google.get(userinfo)
        userinfo = resp.json()
        #profile = resp.json()
        # do something with the token and profile
        return redirect('/')