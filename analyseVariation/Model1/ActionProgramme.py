#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
sys.path.append('.')
sys.path.append('..')
from sqlalchemy import Boolean, Column,String,Integer
from analyseVariation.base import base
from sqlalchemy.orm import *

db= base.db

class ActionProgramme(db.Model):
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    action=db.Column(db.String(80))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    def __init__(self):
        self.id = None
        self.action = None
        self.porteur = None
        self.echeance = None
        self.status = None
        self.commentaire = None

    def Valider(self, ):
        pass

    def Operation1(self, ):
        pass
base.init_base()
base.init_base()