import sys
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from analyseVariation import db, init_base, login_manager
#import Model1.ActionProgramme as mod
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
    password = db.Column(db.String(120), nullable=False)
    

    def __init__(self,nom, prenom, username,email,password):
        self.nom=nom
        self.prenom=prenom
        self.username=username
        self.email=email
        self.password=password

class ActionProgramme(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    action=db.Column(db.String(80))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    def __init__(self, action, porteur, echeance, statut, commentaire):
        self.action = action
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
    desciption = db.Column(db.String(80))
    pourquoi = db.Column(db.String(80))

    def __init__(self, libelle, description, pourquoi):
        self.libelle = libelle
        self.description = description
        self.pourquoi = pourquoi

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

class Pourquoi(db.Model):
    __tablename__='pourquoi'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))

    def __init__(self, libelle):
        self.libelle = libelle

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


init_base()