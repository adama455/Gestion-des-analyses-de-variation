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
import enum
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class Pourquoi1(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi1'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_valeur_aberrante = db.Column(db.String(100))
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))

    def __init__(self,id_valeur_aberrante, code, details):
        self.id_valeur_aberrante = id_valeur_aberrante
        self.code = code
        self.details = details

    def insert_p1(id):
        for i in range(1,4):
            if i==1:
                data = Pourquoi1.query.filter_by(id_valeur_aberrante=id,code='P11').first()
                #print('data ',data)
                tmp = request.form.get('input_1')
            else:
                data = Pourquoi1.query.filter_by(id_valeur_aberrante=id,code=f'P1{i}').first()
                tmp = request.form.get(f'input_1{i}')
            #print('data ', data)
            if not data:
                data = Pourquoi1(id, f'P1{i}', tmp)
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi1.id_valeur_aberrante = id
                Pourquoi1.id = f'P1{i}'
                Pourquoi1.details = tmp


class Pourquoi2(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi2'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_valeur_aberrante = db.Column(db.String(100))
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))

    def __init__(self,id_valeur_aberrante, code, details):
        self.id_valeur_aberrante = id_valeur_aberrante
        self.code = code
        self.details = details

    def insert_p2(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi2.query.filter_by(id_valeur_aberrante=id,code='P21').first()
                #print('data ',data)
                tmp = request.form.get('input_2')
            else:
                data = Pourquoi2.query.filter_by(id_valeur_aberrante=id,code=f'P2{i}').first()
                tmp = request.form.get(f'input_2{i}')
                #print(i,data)
            #print('data ', data)
            if not data:
                data = Pourquoi2(id, f'P2{i}', tmp)
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi2.id_valeur_aberrante = id
                Pourquoi2.id = f'P2{i}'
                Pourquoi2.details = tmp


class Pourquoi3(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi3'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_valeur_aberrante = db.Column(db.String(100))
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))

    def __init__(self,id_valeur_aberrante, code, details):
        self.id_valeur_aberrante = id_valeur_aberrante
        self.code = code
        self.details = details

    def insert_p3(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi3.query.filter_by(id_valeur_aberrante=id,code='P31').first()
                #print('data ',data)
                tmp = request.form.get('input_3')
            else:
                data = Pourquoi3.query.filter_by(id_valeur_aberrante=id,code=f'P3{i}').first()
                tmp = request.form.get(f'input_3{i}')
                #print(i,data)
            #print('data ', data)
            if not data:
                data = Pourquoi3(id, f'P3{i}', tmp)
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi3.id_valeur_aberrante = id
                Pourquoi3.id = f'P3{i}'
                Pourquoi3.details = tmp


class Pourquoi4(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi4'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_valeur_aberrante = db.Column(db.String(100))
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))

    def __init__(self,id_valeur_aberrante, code, details):
        self.id_valeur_aberrante = id_valeur_aberrante
        self.code = code
        self.details = details

    def insert_p4(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi4.query.filter_by(id_valeur_aberrante=id,code='P41').first()
                #print('data ',data)
                tmp = request.form.get('input_4')
            else:
                data = Pourquoi4.query.filter_by(id_valeur_aberrante=id,code=f'P4{i}').first()
                tmp = request.form.get(f'input_4{i}')
                #print(i,data)
            #print('data ', data)
            if not data:
                data = Pourquoi4(id, f'P4{i}', tmp)
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi4.id_valeur_aberrante = id
                Pourquoi4.id = f'P4{i}'
                Pourquoi4.details = tmp


class Pourquoi5(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi5'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_valeur_aberrante = db.Column(db.String(100))
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))

    def __init__(self,id_valeur_aberrante, code, details):
        self.id_valeur_aberrante = id_valeur_aberrante
        self.code = code
        self.details = details

    def insert_p5(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi5.query.filter_by(id_valeur_aberrante=id,code='P51').first()
                #print('data ',data)
                tmp = request.form.get('input_5')
            else:
                data = Pourquoi5.query.filter_by(id_valeur_aberrante=id,code=f'P5{i}').first()
                tmp = request.form.get(f'input_5{i}')
                #print(i,data)
            #print('data ', data)
            if not data:
                data = Pourquoi5(id, f'P5{i}', tmp)
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi5.id_valeur_aberrante = id
                Pourquoi5.id = f'P5{i}'
                Pourquoi5.details = tmp

init_base()