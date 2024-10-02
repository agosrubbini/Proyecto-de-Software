import logging
from flask import Flask
from flask_session import Session
from web.controllers.auth.registry import bp as bp_registry
from web.controllers.auth.login import bp as bp_login
from web.controllers.auth.users import bp as bp_users
from web.controllers.horsemen_and_amazons.jya_users import bp as bp_jya
from src.core import database
from src.core.config import config
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from src.web import commands
from src.web import routes
from src.web.handlers.auth import is_authenticated, get_user_info


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
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_jya)
    # Register error handlers
    app.register_error_handler(404, error.error_not_found)
    app.register_error_handler(401, error.unautorized)
    # Register jinja filters
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(user=get_user_info)
    # Commands
    commands.register(app)
    # Routes
    routes.register(app)
        
    return app