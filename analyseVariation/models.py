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


# class TypeProfil(enum.Enum):
#     ADMIN = "ADMIN"
#     MO ="MANAGER_OPERATIONNEL"
#     SO = "SUPEVISEUR_OPERATIONNEL"
    
class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom=db.Column(db.String(150), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    email=db.Column(db.String(50), unique=True, nullable=False)
    profil=db.Column(db.String(150), unique=True, nullable=False)
    plateau=db.Column(db.String(150), unique=True, nullable=False)
    # profil = db.Column(db.Enum(TypeProfil))
    password = db.Column(db.String(120), nullable=False)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'),cascade="all,save-update, merge, delete")

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def __init__(self, nom, prenom, username, email, profil, plateau, password):
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.profil = profil
        self.password = password
        self.plateau = plateau
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


class ActionProgramme(UserMixin,db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    cause_racine=db.Column(db.String(255))
    action=db.Column(db.String(255))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    def __init__(self, cause_racine, action, porteur, echeance, statut):
        self.cause_racine = cause_racine
        self.action = porteur
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut


class ActionIndividuelle(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_individuelle'
    id=db.Column(db.Integer, primary_key=True)
    identifiant_cc=db.Column(db.String(80))
    reference_action=db.Column(db.String(80))
    libelle_action=db.Column(db.String(255))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    def __init__(self, identifiant_cc, reference_action, libelle_action, porteur, echeance, statut, commentaire):
        self.identifiant_cc = identifiant_cc
        self.reference_action = reference_action
        self.libelle_action = libelle_action
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut
        self.commentaire = commentaire

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
                
            liste_action = [act_1, act_2, act_3, act_4, act_5, act_6]
            for i in range(1,7):
                ref = []
                lib = []
                por = []
                ech = []
                n=0
                for elem in data:
                    k = elem.reference_action.split('_')[2].split('.')[0]
                    #print(i==int(k))
                    if i==int(k):
                        n+=1
                        ref.append(elem.reference_action)
                        lib.append(elem.libelle_action)
                        por.append(elem.porteur)
                        ech.append(elem.echeance)
                        #champ_act = [elem.reference_action, elem.libelle_action, elem.porteur, elem.echeance]
                        #print(elem.reference_action.split('_')[2].split('.')[0])
                        liste_action[i-1].append(ref)
                        liste_action[i-1].append(lib)
                        liste_action[i-1].append(por)
                        liste_action[i-1].append(ech)
                    #print('test',n, i)
                    #print(liste_action[int(k)-1], int(k), n )
                    #print(liste_action[int(k)-1][0], n)
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
        
        return liste_action, nbre_act


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

class Fichiers(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='fichiers'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50))
    nom = db.Column(db.String(80))
    effectif = db.Column(db.String(50))
    def __init__(self, reference, nom, effectif):
        self.reference = reference
        self.nom = nom
        self.effectif = effectif

    def Importer(self, ):
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
    # valeur = db.Column(db.String(255), unique=True, nullable=False)
    famille_causes = db.Column(db.String(500))
    probleme = db.Column(db.String(100))
    pourquoi_1 = db.Column(db.String(300))
    pourquoi_2 = db.Column(db.String(500))
    pourquoi_3 = db.Column(db.String(500))
    pourquoi_4 = db.Column(db.String(500))
    pourquoi_5 = db.Column(db.String(500))

    def __init__(self, identifiant, famille_causes, probleme, pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5):
        self.identifiant = identifiant
        # self.valeur = valeur
        self.famille_causes = famille_causes
        self.probleme = probleme
        self.pourquoi_1 = pourquoi_1
        self.pourquoi_2 = pourquoi_2
        self.pourquoi_3 = pourquoi_3
        self.pourquoi_4 = pourquoi_4
        self.pourquoi_5 = pourquoi_5

    def traitement_data_analyse_apporter(datacc):
        car_exclu = ['2.', '1.', '3.', '4.','5.','6.','7.','8.','9.','10.']
        axes_analyse = [ elem for elem in datacc.famille_causes.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_1 = [ elem for elem in datacc.pourquoi_1.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_2 = [ elem for elem in datacc.pourquoi_2.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_3 = [ elem for elem in datacc.pourquoi_3.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_4 = [ elem for elem in datacc.pourquoi_4.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_5 = [ elem for elem in datacc.pourquoi_5.split('_/_') if not [el for el in car_exclu if el==elem]]
        liste_pourquoi = [pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5, axes_analyse]
        nbre_pourquoi = [len(pourquoi_1), len(pourquoi_2), len(pourquoi_3), len(pourquoi_4), len(pourquoi_5)]

        return liste_pourquoi, nbre_pourquoi
    
    def update_pourquoi(object, axe_analyse, probleme, pourquoi1, pourquoi2, pourquoi3, pourquoi4, pourquoi5):
        try:
            # pourquoi1 = '1._/_'+liste_pourquoi[0][0]+'_/_' +'2._/_'+ liste_pourquoi[0][1] +'_/_' +'3._/_'+ liste_pourquoi[0][2]
            # pourquoi21 = '1._/_'+liste_pourquoi[1][0]+'_/_' +'2._/_'+ liste_pourquoi[1][1] +'_/_' +'3._/_'+ liste_pourquoi[1][2]
            # pourquoi22= '_/_4._/_'+liste_pourquoi[1][3] +'_/_' +'5._/_'+ liste_pourquoi[1][4] +'_/_' +'6._/_'+ liste_pourquoi[1][5]
            # pourquoi31 = '1._/_'+liste_pourquoi[2][0]+'_/_' +'2._/_'+ liste_pourquoi[2][1] +'_/_' +'3._/_'+ liste_pourquoi[2][2]
            # pourquoi32= '_/_4._/_'+liste_pourquoi[2][3] +'_/_' +'5._/_'+ liste_pourquoi[2][4] +'_/_' +'6._/_'+ liste_pourquoi[2][5]
            # pourquoi41 = '1._/_'+liste_pourquoi[3][0]+'_/_' +'2._/_'+ liste_pourquoi[3][1] +'_/_' +'3._/_'+ liste_pourquoi[3][2]
            # pourquoi42= '_/_4._/_'+liste_pourquoi[3][3] +'_/_' +'5._/_'+ liste_pourquoi[3][4] +'_/_' +'6._/_'+ liste_pourquoi[3][5]
            # pourquoi51 = '1._/_'+liste_pourquoi[4][0]+'_/_' +'2._/_'+ liste_pourquoi[4][1] +'_/_' +'3._/_'+ liste_pourquoi[4][2]
            # pourquoi52= '_/_4._/_'+liste_pourquoi[4][3] +'_/_' +'5._/_'+ liste_pourquoi[4][4] +'_/_' +'6._/_'+ liste_pourquoi[4][5]
            # liste_pourquoi = [pourquoi1,pourquoi21 + pourquoi22,pourquoi31 + pourquoi32,pourquoi41 + pourquoi42,pourquoi51 + pourquoi52]
            object.famille_causes = axe_analyse
            object.probleme = probleme
            object.pourquoi_1 = pourquoi1
            object.pourquoi_2 = pourquoi2
            object.pourquoi_3 = pourquoi3
            object.pourquoi_4 = pourquoi4
            object.pourquoi_5 = pourquoi5
        except:
            print("Quelque chose s'est mal passer")
        

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
    univers=db.Column(db.String(255))
    
    def __init__(self, libelle, description, univers):
        self.libelle = libelle
        self.description = description
        self.univers = univers

init_base()