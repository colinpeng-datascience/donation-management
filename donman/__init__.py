from donman.controller import create_app
from flask_migrate import Migrate 
from donman.model import db
import sys; print(sys.executable)

app = create_app()
migrate = Migrate(app, db)

import donman.cli
if __name__ == '__main__':
    app.run()