import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from flask import current_app, request #<---HERE
from analyseVariation import db, init_base, login_manager,app
from analyseVariation.pourquoi_model import Pourquoi5 
from sqlalchemy.orm import *
from flask_login import UserMixin
import enum
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class ActionIndividuelle(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_individuelle'
    id=db.Column(db.Integer, primary_key=True)
    reference_action=db.Column(db.String(80))
    libelle_action=db.Column(db.String(255))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    pourquoi5_id = db.Column(db.Integer(), db.ForeignKey('pourquoi5.id', ondelete='CASCADE'))
    def __init__(self, reference_action, libelle_action, porteur, echeance, statut, commentaire, pourquoi5_id):
        self.reference_action = reference_action
        self.libelle_action = libelle_action
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut
        self.commentaire = commentaire
        self.pourquoi5_id = pourquoi5_id

    def Valider(self, ):
        pass

    def recup_action(data):
        try:
            #ref_act = request.form['data']
            #data_ref = ActionProgramme.query.filter_by(reference_action=ref_act).first()
            act_1 = []
            act_2 = []
            act_3 = []
            act_4 = []
            act_5 = []
            act_6 = []
            reference = []
            libelle = []
            porteur = []
            echeance = []
            id = []
            table = []
            liste_action = [act_1, act_2, act_3, act_4, act_5, act_6]
            n=1
            for element in data:
                #print(element.id)
                action = ActionIndividuelle.query.filter_by(pourquoi5_id=element.id).all()
                if f'P5{n}'==((element.code)):
                    ref = []
                    lib = []
                    por = []
                    ech = []
                    for elem in action:
                        ref.append(elem.reference_action)
                        reference.append(elem.reference_action)
                        lib.append(elem.libelle_action)
                        libelle.append(elem.libelle_action)
                        por.append(elem.porteur)
                        porteur.append(elem.porteur)
                        ech.append(elem.echeance)
                        echeance.append(elem.echeance)
                        id.append(elem.id)
                        
                    liste_action[n-1].append(ref)
                    liste_action[n-1].append(lib)
                    liste_action[n-1].append(por)
                    liste_action[n-1].append(ech)
                n+=1
            table.append(libelle)
            table.append(porteur)
            table.append(echeance)
            table.append(id)
            #print('fds', table)
            nbre_act = []
            for elem in liste_action:
                if elem:
                    nbre_act.append(len(elem[0]))
                else:
                    nbre_act.append(0)
            #print(nbre_act)
            #if data_ref:
            #    exist = 1
            #print(ref_act, exist)
        except:
            nbre_act = [0, 0, 0, 0, 0, 0]
            print('on a pas pu recuperer les infos correspondant a cette reference')
        
        return liste_action, nbre_act, table


# class ActionIndividuelle(UserMixin, db.Model):
#     __table_args__ = {'extend_existing': True}
#     __tablename__='action_individuelle'
#     id=db.Column(db.Integer, primary_key=True)
#     identifiant_cc=db.Column(db.String(80))
#     reference_action=db.Column(db.String(80))
#     libelle_action=db.Column(db.String(255))
#     porteur=db.Column(db.String(80))
#     echeance=db.Column(db.String(80))
#     status=db.Column(db.String(80))
#     commentaire=db.Column(db.String(80))
#     def __init__(self, identifiant_cc, reference_action, libelle_action, porteur, echeance, statut, commentaire):
#         self.identifiant_cc = identifiant_cc
#         self.reference_action = reference_action
#         self.libelle_action = libelle_action
#         self.porteur = porteur
#         self.echeance = echeance
#         self.status = statut
#         self.commentaire = commentaire

#     def Valider(self, ):
#         pass

#     def recup_action(data):
#         try:
#             #ref_act = request.form['data']
#             #data_ref = ActionProgramme.query.filter_by(reference_action=ref_act).first()
#             act_1 = []
#             act_2 = []
#             act_3 = []
#             act_4 = []
#             act_5 = []
#             act_6 = []
                
#             liste_action = [act_1, act_2, act_3, act_4, act_5, act_6]
#             for i in range(1,7):
#                 ref = []
#                 lib = []
#                 por = []
#                 ech = []
#                 n=0
#                 for elem in data:
#                     k = elem.reference_action.split('_')[2].split('.')[0]
#                     #print(i==int(k))
#                     if i==int(k):
#                         n+=1
#                         ref.append(elem.reference_action)
#                         lib.append(elem.libelle_action)
#                         por.append(elem.porteur)
#                         ech.append(elem.echeance)
#                         #champ_act = [elem.reference_action, elem.libelle_action, elem.porteur, elem.echeance]
#                         #print(elem.reference_action.split('_')[2].split('.')[0])
#                         liste_action[i-1].append(ref)
#                         liste_action[i-1].append(lib)
#                         liste_action[i-1].append(por)
#                         liste_action[i-1].append(ech)
#                     #print('test',n, i)
#                     #print(liste_action[int(k)-1], int(k), n )
#                     #print(liste_action[int(k)-1][0], n)
#             nbre_act = []
#             for elem in liste_action:
#                 if elem:
#                     nbre_act.append(len(elem[0]))
#                 else:
#                     nbre_act.append(0)
#             #print(nbre_act)
#             #if data_ref:
#             #    exist = 1
#             #print(ref_act, exist)
#         except:
#             nbre_act = [0, 0, 0, 0, 0, 0]
#             print('on a pas pu recuperer les infos correspondant a cette reference')
        
#         return liste_action, nbre_act

init_base()