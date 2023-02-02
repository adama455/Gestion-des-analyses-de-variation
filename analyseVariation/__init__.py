import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask


app = Flask(__name__)

#app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'
app.config.update(
    SECRET_KEY='e7e5848a58f7a679fd559d593ed8a9997bbe33024a3b98f4a9c621e3607afb9b',
    SQLALCHEMY_DATABASE_URI = 'mysql://analysevariation:anvar123@localhost/analysevariation',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category= 'danger'

# from .models import User
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
# _jwt.init_app(app)

def init_base():
    with app.app_context():
        db.create_all()
