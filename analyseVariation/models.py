import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from flask import current_app #<---HERE
from analyseVariation import db, init_base, login_manager,app
from sqlalchemy.orm import *
from flask_login import UserMixin
import enum
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


class TypeProfil(enum.Enum):
    ADMIN = "ADMIN"
    MO ="MANAGER_OPERATIONNEL"
    SO = "SUPEVISEUR_OPERATIONNEL"
    
class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom=db.Column(db.String(150), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    email=db.Column(db.String(50), unique=True, nullable=False)
    profil = db.Column(db.Enum(TypeProfil))
    password = db.Column(db.String(120), nullable=False)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'),cascade="all,save-update, merge, delete")

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})
 
    # -----------------------Token------

    def __init__(self, nom, prenom, username, email, profil, password):
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.profil = profil
        self.password = password
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
   
# /////////////////////////////////////////////////////////////////////////////////////

class ActionProgramme(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    reference_action=db.Column(db.String(80))
    libelle_action=db.Column(db.String(255))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    def __init__(self, reference_action, libelle_action, porteur, echeance, statut, commentaire):
        self.reference_action = reference_action
        self.libelle_action = libelle_action
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut
        self.commentaire = commentaire

    def Valider(self, ):
        pass

    def Operation1(self, ):
        pass

class Cause(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='causes'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))
    description = db.Column(db.String(255))
    # pourquoi = db.Column(db.String(80))

    def __init__(self, libelle, description):
        self.libelle = libelle
        self.description = description
        # self.pourquoi = pourquoi


class Statut(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='statut'
    id = db.Column(db.Integer, primary_key=True)
    valide = db.Column(db.String(80))
    enregistre = db.Column(db.String(80))
    cloture = db.Column(db.String(80))

    def __init__(self, valide, enregistre, cloture):
        self.valide = valide
        self.enregistre = enregistre
        self.cloture = cloture

class Enregistrement_AV(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='enregistrement_av'
    id = db.Column(db.Integer, primary_key=True)
    agent = db.Column(db.String(80))
    reference_av = db.Column(db.String(80))
    libelle_av = db.Column(db.String(255))
    date = db.Column(db.Date)
    statut_analyse = db.Column(db.String(80))
    commentaire = db.Column(db.String(80), nullable=True)

    def __init__(self, agent, reference_av, libelle_av, date, statut_analyse, commentaire):
        self.agent = agent
        self.reference_av = reference_av
        self.libelle_av = libelle_av
        self.date = date
        self.statut_analyse = statut_analyse
        self.commentaire = commentaire

    def Valider(self, ):
        pass

    def Recherher(self, ):
        pass

    def Consulter(self, ):
        pass

class Fichier(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='fichier'
    id = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Integer)
    conseiller = db.Column(db.String(80))
    def __init__(self, valeur, conseiller):
        self.Valeur = valeur
        self.conseiller = conseiller

    def Importer(self, ):
        pass

class AnalyseApporter(db.Model):
    __tablename__='apporter_analyse'
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), unique=True, nullable=False)
    axe_analyse = db.Column(db.String(50))
    probleme = db.Column(db.String(100))
    pourquoi_1 = db.Column(db.String(500))
    pourquoi_2 = db.Column(db.String(500))
    pourquoi_3 = db.Column(db.String(500))
    pourquoi_4 = db.Column(db.String(500))
    pourquoi_5 = db.Column(db.String(500))

    def __init__(self, identifiant, axe_analyse, probleme, pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5):
        self.identifiant = identifiant
        self.axe_analyse = axe_analyse
        self.probleme = probleme
        self.pourquoi_1 = pourquoi_1
        self.pourquoi_2 = pourquoi_2
        self.pourquoi_3 = pourquoi_3
        self.pourquoi_4 = pourquoi_4
        self.pourquoi_5 = pourquoi_5

class ValeursAberrante(UserMixin, db.Model):    
    __table_args__ = {'extend_existing': True}
    __tablename__='valeurs_aberante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference_av = db.Column(db.String(80))
    nom_cc = db.Column(db.String(80))
    valeurs = db.Column(db.Float)

    def __init__(self, reference_av, nom_cc, valeurs):
        self.reference_av = reference_av
        self.nom_cc = nom_cc
        self.valeurs = valeurs

    def Analyser(self, ):
        pass

class Profil(UserMixin, db.Model):
    __tablename__='profil'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))

    def __init__(self, libelle):
        self.libelle = libelle

class Plateau(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='plateaux'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(100))
    description = db.Column(db.String(255))
    # UNIV = (
    #     ('FRONT OFFICE','FRONT OFFICE'),
    #     ('BACK OFFICE','BACK OFFICE'),
    # )
    univers  =db.Column(db.String(255))
    # metrique = models.ManyToManyField(Metrique)
    
    def __init__(self, libelle, description, univers):
        self.libelle = libelle
        self.description = description
        self.univers = univers

init_base()