"""REST API."""
from flask import Flask
from ..config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # app is a single object used by all the code modules in this package
    app = Flask(__name__)  # pylint: disable=invalid-name

    # Read settings from config module (donation_management/config.py)
    app.config.from_object(Config)

    # Overlay settings read from a Python file whose path is set in the environment
    # variable DONMAN_SETTINGS. Setting this environment variable is optional.
    # Docs: http://flask.pocoo.org/docs/latest/config/
    #
    # EXAMPLE:
    # $ export INSTA485_SETTINGS=secret_key_config.py
    app.config.from_envvar('DONMAN_SETTINGS', silent=True)


    db.init_app(app)
    
    # Register donations blueprint
    from .donation import donation_bp
    from .type import type_bp
    from .distribution import distribution_bp
    from .donor import donor_bp
    from .report import report_bp
    from .staff import staff_bp
    app.register_blueprint(donation_bp, url_prefix='/api')
    app.register_blueprint(type_bp, url_prefix='/api')
    app.register_blueprint(distribution_bp, url_prefix='/api')
    app.register_blueprint(donor_bp, url_prefix='/api')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(staff_bp, url_prefix='/api')
    

    return app