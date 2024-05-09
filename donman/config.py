"""development configuration."""

import pathlib

class Config:
    # Root of this application, useful if it doesn't occupy an entire domain
    APPLICATION_ROOT = '/'

    # Secret key for encrypting cookies
    SESSION_COOKIE_NAME = 'login'
    # FIXME SET WITH: $ python3 -c "import os; print(os.urandom(24))"
    SECRET_KEY = b';\xb5\xf7(#|\xa3_\x88.\xa0FF\xa4J\x1fq\xf9\xdc\x14\x01\xbe\xf8\x82'

    # Database file
    DONMAN_ROOT = pathlib.Path(__file__).resolve().parent.parent
    DATABASE_FILENAME = DONMAN_ROOT/'var'/'donation_management.sqlite3'

