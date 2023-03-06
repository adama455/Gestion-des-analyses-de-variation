import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from flask import current_app, request #<---HERE
from analyseVariation import db, init_base, login_manager,app
from sqlalchemy.orm import *
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

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

init_base()