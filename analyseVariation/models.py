import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import Boolean, Column,String,Integer
from analyseVariation import db, init_base
#import Model1.ActionProgramme as mod
from sqlalchemy.orm import *


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50))
    prenom=db.Column(db.String(50))
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))

    def __init__(self,id,name,username,email):
        self.id=id
        self.name=name
        self.username=username
        self.email=email

class ActionProgramme(db.Model):
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    action=db.Column(db.String(80))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    def __init__(self, id, action, porteur, echeance, statut, commentaire):
        self.id = id
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
    __tablename__='causes'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))
    desciption = db.Column(db.String(80))
    pourquoi = db.Column(db.String(80))

    def __init__(self, id, libelle, description, pourquoi):
        self.id = id
        self.libelle = libelle
        self.description = description
        self.pourquoi = pourquoi

class Statut(db.Model):
    __tablename__='statut'
    id = db.Column(db.Integer, primary_key=True)
    valide = db.Column(db.String(80))
    enregistre = db.Column(db.String(80))
    cloture = db.Column(db.String(80))

    def __init__(self, id, valide, enregistre, cloture):
        self.id = id
        self.valide = valide
        self.enregistre = enregistre
        self.cloture = cloture

class Enregistrement_AV(db.Model):
    __tablename__='enregistrement_av'
    id = db.Column(db.Integer, primary_key=True)
    agent = db.Column(db.String(80))
    valeur = db.Column(db.String(80))
    statut_analyse = db.Column(db.String(80))
    commentaire = db.Column(db.String(80))

    def __init__(self, id, agent, valeur, statut_analyse, commentaire):
        self.id = id
        self.agent = agent
        self.valeur = valeur
        self.statut_analyse = statut_analyse
        self.commentaire = commentaire

    def Valider(self, ):
        pass

    def Recherher(self, ):
        pass

    def Consulter(self, ):
        pass


class Fichier(db.Model):
    __tablename__='fichier'
    id = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Integer)
    conseiller = db.Column(db.String(80))
    def __init__(self, id, valeur, conseiller):
        self.Id = id
        self.Valeur = valeur
        self.conseiller = conseiller

    def Importer(self, ):
        pass

class Pourquoi(db.Model):
    __tablename__='pourquoi'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))

    def __init__(self, id, libelle):
        self.id = id
        self.libelle = libelle

class ValeursAberrante(db.Model):
    __tablename__='valeurs_aberante'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    enregistrement = db.Column(db.String(80))

    def __init__(self, id, date, enregistrement):
        self.id = id
        self.date = date
        self.enregistrement = enregistrement

    def Analyser(self, ):
        pass

class Profil(db.Model):
    __tablename__='profil'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))

    def __init__(self, id, libelle):
        self.id = id
        self.libelle = libelle


init_base()