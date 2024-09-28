from flask import Flask
from flask import render_template
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from src.web.controllers.auth.registry import bp_registry
from src.web.controllers.users import bp as bp_users
from src.core import database
from src.core import seeds
from src.core.config import config

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.register_blueprint(bp_registry)
    app.register_blueprint(bp_users)

    app.config.from_object(config[env])
    database.init_app(app)
    bcrypt.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    app.register_error_handler(404, error.error_not_found)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()
        
    return app