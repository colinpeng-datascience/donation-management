"""REST API."""
from .donation import donation_bp
from flask import Flask
from ..config import Config

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

    # Register donations blueprint
    app.register_blueprint(donation_bp, url_prefix='/api')
    return app