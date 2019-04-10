
from flask import Flask
from flask import request, Response, make_response
from config import *


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from views import *


if __name__ == '__main__':
    app.run(DEBUG = True)
    