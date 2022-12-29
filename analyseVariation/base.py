#import sys
#sys.path.append('.')
#sys.path.append('..')
from app import app
from flask_sqlalchemy import SQLAlchemy



app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI = 'mysql://analyse:test123@localhost/analyse',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)

def init_base():
    with app.app_context():
        db.create_all()
