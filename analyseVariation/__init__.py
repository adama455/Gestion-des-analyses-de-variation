
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'


app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI = 'mysql://analysevariation:anvar123@localhost/analysevariation',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def init_base():
    with app.app_context():
        db.create_all()


#from .app import app
#from .models import models

# Connect sqlalchemy to app
#models.db.init_app(app)