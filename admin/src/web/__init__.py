import logging
from flask import Flask
from flask_session import Session
from web.controllers.auth.login import bp as bp_login
from web.controllers.auth.users import bp as bp_users
from web.controllers.payment import bp as bp_payment
from web.controllers.horsemen_and_amazons import bp as bp_jya
from web.controllers.billing import bp as bp_billing
from web.controllers.team import bp as bp_team
from src.web.controllers.horses import bp as bp_horses
from src.core import database
from src.core.config import config
from src.core.bcrypt import bcrypt
from src.web.handlers import error
from src.web.storage import storage
from src.web import commands
from src.web import routes
from src.web.handlers.auth import is_authenticated, get_user_info
from src.web.controllers.horses import bp as bp_horses


session = Session()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def create_app(env="production", static_folder="../../static"):
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
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_horses)
    app.register_blueprint(bp_jya)
    app.register_blueprint(bp_billing)
    app.register_blueprint(bp_payment)
    app.register_blueprint(bp_team)

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
    
    # Register object storage
    storage.init_app(app)
    
    return app