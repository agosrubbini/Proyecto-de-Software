import logging
from flask import Flask
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from web.controllers.auth.registry import bp as bp_registry
from src.core import database
from src.web import commands
from src.web import routes
from src.core.config import config
from web.controllers.auth.login import bp as bp_login
from flask_session import Session

session = Session()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    # load config
    app.config.from_object(config[env])
    #init database
    database.init_app(app)
    #init bcrypt
    bcrypt.init_app(app)
    #init session
    session.init_app(app)
    # Register blueprints
    app.register_blueprint(bp_registry)
    app.register_blueprint(bp_login)
    # Register error handlers
    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.unautorized)
    # Commands
    commands.register(app)
    # Routes
    routes.register(app)
        
    return app