import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from analyseVariation import db, init_base, login_manager,app
from analyseVariation.models import Plateau
from sqlalchemy.orm import *
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom=db.Column(db.String(150), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    email=db.Column(db.String(50), unique=True, nullable=False)
    profil=db.Column(db.String(150), unique=True, nullable=False)
    # plateau=db.Column(db.String(150), nullable=False)
    # profil = db.Column(db.Enum(TypeProfil))
    plateau_id = db.Column(db.Integer(), db.ForeignKey('plateaux.id', ondelete='CASCADE'))
    password = db.Column(db.String(120), nullable=False)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'),cascade="all,save-update, merge, delete")

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def __init__(self, nom, prenom, username, email, profil, plateau_id, password):
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.profil = profil
        self.password = password
        self.plateau = plateau_id
        
# /////////////////////////////////////
# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
  
init_base()