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
        self.action = action
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut


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
            statut = []
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
                        statut.append(elem.status)
                        
                    liste_action[n-1].append(ref)
                    liste_action[n-1].append(lib)
                    liste_action[n-1].append(por)
                    liste_action[n-1].append(ech)
                n+=1
            table.append(libelle)
            table.append(porteur)
            table.append(echeance)
            table.append(id)
            table.append(statut)
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
    effectif = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, reference, effectif, date, user_id):
        self.reference = reference
        self.effectif = effectif
        self.date = date
        self.user_id = user_id

    def Importer(self, ):
        pass

class ValeursFichier(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='valeurs_fichier'
    id = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Integer)
    conseiller = db.Column(db.String(80))
    fichier_id = db.Column(db.Integer, db.ForeignKey('fichiers.id', ondelete='CASCADE'))
    def __init__(self, valeur, conseiller, fichier_id):
        self.Valeur = valeur
        self.conseiller = conseiller
        self.fichier_id = fichier_id

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
    
    def traitement_data_pourquoi(id, datacc):
        car_exclu = ['2.', '1.', '3.', '4.','5.','6.','7.','8.','9.','10.']
        print('test id',id)
        axes_analyse = [ elem for elem in datacc.famille_causes.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_1 = [ elem.details for elem in Pourquoi1.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_2 = [ elem.details for elem in Pourquoi2.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_3 = [ elem.details for elem in Pourquoi3.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_4 = [ elem.details for elem in Pourquoi4.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_5 = [ elem.details for elem in Pourquoi5.query.filter_by(valeur_aberrante_id=id).all()]
        liste_pourquoi = [pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5, axes_analyse]
        nbre_pourquoi = [len(pourquoi_1), len(pourquoi_2), len(pourquoi_3), len(pourquoi_4), len(pourquoi_5)]
        print(pourquoi_1)

        return liste_pourquoi, nbre_pourquoi

    def insert_update_pourquoi(id, datacc,reference):
        try:
            probleme = request.form['probleme']
            axes_analyse = ''
            for i in range(1,7):
                axes = request.form.get(f'axes_{i}_analyse')
                axes_analyse += f'{i}._/_'+axes+f'_/_{i+1}._/_'
            pourquoi1 = '1._/_'+request.form.get('input_1')+'_/_' +'2._/_'+ request.form.get('input_12') +'_/_' +'3._/_'+ request.form.get('input_13')
            pourquoi21 = '1._/_'+request.form.get('input_2')+'_/_' +'2._/_'+ request.form.get('input_22') +'_/_' +'3._/_'+ request.form.get('input_23')
            pourquoi22= '_/_4._/_'+request.form.get('input_24') +'_/_' +'5._/_'+ request.form.get('input_25') +'_/_' +'6._/_'+ request.form.get('input_26')
            pourquoi31 = '1._/_'+request.form.get('input_3')+'_/_' +'2._/_'+ request.form.get('input_32') +'_/_' +'3._/_'+ request.form.get('input_33')
            pourquoi32= '_/_4._/_'+request.form.get('input_34') +'_/_' +'5._/_'+ request.form.get('input_35') +'_/_' +'6._/_'+ request.form.get('input_36')
            pourquoi41 = '1._/_'+request.form.get('input_4')+'_/_' +'2._/_'+ request.form.get('input_42') +'_/_' +'3._/_'+ request.form.get('input_43')
            pourquoi42= '_/_4._/_'+request.form.get('input_44') +'_/_' +'5._/_'+ request.form.get('input_45') +'_/_' +'6._/_'+ request.form.get('input_46')
            pourquoi51 = '1._/_'+request.form.get('input_5')+'_/_' +'2._/_'+ request.form.get('input_52') +'_/_' +'3._/_'+ request.form.get('input_53')
            pourquoi52= '_/_4._/_'+request.form.get('input_54') +'_/_' +'5._/_'+ request.form.get('input_55') +'_/_' +'6._/_'+ request.form.get('input_56')
            if not datacc:
                pourquoi = AnalyseApporter(id, axes_analyse, probleme, pourquoi1, pourquoi21+pourquoi22, pourquoi31+pourquoi32, pourquoi41+pourquoi42, pourquoi51+pourquoi52)
                print('lamine',pourquoi)
                db.session.add(pourquoi)
                db.session.commit()
            else:
                # AnalyseApporter.update_pourquoi(datacc,axes_analyse, probleme, pourquoi1, pourquoi21+pourquoi22,pourquoi31+pourquoi32, pourquoi41+pourquoi42, pourquoi51+pourquoi52)
                Enregistrement_AV.query.filter_by(reference_av=reference).first().libelle_av = request.form['libelle_av']
                datacc.famille_causes = axes_analyse
                datacc.probleme = probleme
                datacc.pourquoi_1 = pourquoi1
                datacc.pourquoi_2 = pourquoi21+pourquoi22
                datacc.pourquoi_3 = pourquoi31+pourquoi32
                datacc.pourquoi_4 = pourquoi41+pourquoi42
                datacc.pourquoi_5 = pourquoi51+pourquoi52
                db.session.commit()
        except:
            print("Quelque chose s'est mal passer")


class ValeursAberrante(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='valeurs_aberrante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference_av = db.Column(db.String(80))
    nom_cc = db.Column(db.String(80))
    valeurs = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, reference_av, nom_cc, valeurs, user_id):
        self.reference_av = reference_av
        self.nom_cc = nom_cc
        self.valeurs = valeurs
        self.user_id = user_id

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


        
##################################### MODELISATION 2.0 ###################################################


class Pourquoi1(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi1'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))
    valeur_aberrante_id = db.Column(db.Integer, db.ForeignKey('valeurs_aberrante.id', ondelete='CASCADE'))

    def __init__(self, code, details, valeur_aberrante_id):
        self.code = code
        self.details = details
        self.valeur_aberrante_id = valeur_aberrante_id

    def insert_p1(id):
        for i in range(1,4):
            if i==1:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code='P11').first()
                tmp = request.form.get('input_1')
            else:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code=f'P1{i}').first()
                tmp = request.form.get(f'input_1{i}')
            if not data and tmp:
                data = Pourquoi1(f'P1{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            elif tmp:
                Pourquoi1.valeur_aberrante_id = int(id)
                Pourquoi1.code = f'P1{i}'
                Pourquoi1.details = tmp   


class Pourquoi2(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi2'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))
    valeur_aberrante_id = db.Column(db.Integer, db.ForeignKey('valeurs_aberrante.id', ondelete='CASCADE'))

    def __init__(self, code, details, valeur_aberrante_id):
        self.code = code
        self.details = details
        self.valeur_aberrante_id = valeur_aberrante_id

    def insert_p2(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi2.query.filter_by(valeur_aberrante_id=int(id),code='P21').first()
                #print('data ',data)
                tmp = request.form.get('input_2')
            else:
                data = Pourquoi2.query.filter_by(valeur_aberrante_id=int(id),code=f'P2{i}').first()
                tmp = request.form.get(f'input_2{i}')
                #print(i,data)
            #print('data ', data)
            if not data and tmp:
                data = Pourquoi2(f'P2{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi2.valeur_aberrante_id = int(id)
                Pourquoi2.id = f'P2{i}'
                Pourquoi2.details = tmp


class Pourquoi3(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi3'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))
    valeur_aberrante_id = db.Column(db.Integer, db.ForeignKey('valeurs_aberrante.id', ondelete='CASCADE'))

    def __init__(self, code, details, valeur_aberrante_id):
        self.code = code
        self.details = details
        self.valeur_aberrante_id = valeur_aberrante_id

    def insert_p3(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi3.query.filter_by(valeur_aberrante_id=int(id),code='P31').first()
                #print('data ',data)
                tmp = request.form.get('input_3')
            else:
                data = Pourquoi3.query.filter_by(valeur_aberrante_id=int(id),code=f'P3{i}').first()
                tmp = request.form.get(f'input_3{i}')
                #print(i,data)
            #print('data ', data)
            if not data and tmp:
                data = Pourquoi3(f'P3{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi3.valeur_aberrante_id = int(id)
                Pourquoi3.id = f'P3{i}'
                Pourquoi3.details = tmp

class Pourquoi4(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi4'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))
    valeur_aberrante_id = db.Column(db.Integer, db.ForeignKey('valeurs_aberrante.id', ondelete='CASCADE'))

    def __init__(self, code, details, valeur_aberrante_id):
        self.code = code
        self.details = details
        self.valeur_aberrante_id = valeur_aberrante_id

    def insert_p4(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi4.query.filter_by(valeur_aberrante_id=int(id),code='P41').first()
                #print('data ',data)
                tmp = request.form.get('input_4')
            else:
                data = Pourquoi4.query.filter_by(valeur_aberrante_id=int(id),code=f'P4{i}').first()
                tmp = request.form.get(f'input_4{i}')
                #print(i,data)
            #print('data ', data)
            if not data and tmp:
                data = Pourquoi4(f'P4{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            else:
                Pourquoi4.valeur_aberrante_id = int(id)
                Pourquoi4.id = f'P4{i}'
                Pourquoi4.details = tmp

class Pourquoi5(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='pourquoi5'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    details=db.Column(db.String(255))
    axe_analyse_id = db.Column(db.Integer(), db.ForeignKey('causes.id', ondelete='CASCADE'))
    valeur_aberrante_id = db.Column(db.Integer, db.ForeignKey('valeurs_aberrante.id', ondelete='CASCADE'))

    def __init__(self, code, details, axe_analyse_id, valeur_aberrante_id):
        self.code = code
        self.details = details
        self.axe_analyse_id = axe_analyse_id
        self.valeur_aberrante_id = valeur_aberrante_id

    def insert_p5(id):
        for i in range(1,7):
            axe = request.form.get(f'axes_{i}_analyse')
            if i==1 and axe:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code='P51').first()
                #print('data ',data)
                tmp = request.form.get('input_5')
                axe_id = Cause.query.filter_by(libelle=axe).first().id
                if not data and tmp:
                    data = Pourquoi5(f'P5{i}', tmp, axe_id, int(id))
                    db.session.add(data)
                    db.session.commit()
                else:
                    Pourquoi5.valeur_aberrante_id = int(id)
                    Pourquoi5.id = f'P5{i}'
                    Pourquoi5.details = tmp
            elif axe:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code=f'P5{i}').first()
                tmp = request.form.get(f'input_5{i}')
                axe_id = Cause.query.filter_by(libelle=axe).first().id
                #print(i,data)
                #print('data ', data)
                if not data and tmp:
                    data = Pourquoi5(f'P5{i}', tmp, axe_id, int(id))
                    db.session.add(data)
                    db.session.commit()
                else:
                    Pourquoi5.valeur_aberrante_id = int(id)
                    Pourquoi5.id = f'P5{i}'
                    Pourquoi5.details = tmp

    def recup_all_pourquoi(all_va):
        table_pourquoi1 = []
        table_pourquoi2 = []
        table_pourquoi3 = []
        table_pourquoi4 = []
        table_pourquoi5 = []
        table_axe = []
        liste_identifiant = []
        table_liste_pourquoi = []
        nbre_act = []
        N = []
        Nom_cc = []
        Valeur_cc = []
        table_action = []
        nbre_cc=0
        liste_id=[]
        # On récupere tous les identifiants qui ont ete analyse qu'on met dans list_id
        for element in all_va:
            all_pourquoi5 = Pourquoi5.query.filter_by(valeur_aberrante_id=element.id).all()
            for elem in all_pourquoi5:
                if element.id not in liste_id:
                    liste_id.append(element.id)
        # Pour chaque id on recupere l'ensemble des causes racines et les axes d'analyses correspondante
        for element in liste_id:
            #print(element, liste_id)
            all_pourquoi1 = Pourquoi1.query.filter_by(valeur_aberrante_id=element).all()
            all_p1 = []
            for elem in all_pourquoi1:
                all_p1.append(elem.details)
            all_pourquoi2 = Pourquoi2.query.filter_by(valeur_aberrante_id=element).all()
            all_pourquoi3 = Pourquoi3.query.filter_by(valeur_aberrante_id=element).all()
            all_pourquoi4 = Pourquoi4.query.filter_by(valeur_aberrante_id=element).all()
            all_pourquoi5 = Pourquoi5.query.filter_by(valeur_aberrante_id=element).all()
            all_p2 = []
            all_p3 = []
            all_p4 = []
            all_p5 = []
            all_axe_analyse = []
            for i in range(len(all_pourquoi5)):
                #print(elem.details)
                axe = Cause.query.filter_by(id=all_pourquoi5[i].axe_analyse_id).first().libelle
                all_axe_analyse.append(axe)
                all_p2.append(all_pourquoi2[i].details)
                all_p3.append(all_pourquoi3[i].details)
                all_p4.append(all_pourquoi4[i].details)
                all_p5.append(all_pourquoi5[i].details)
            nom_cc = ValeursAberrante.query.filter_by(id=element).first().nom_cc
            Nom_cc.append(nom_cc)
            valeur_cc = ValeursAberrante.query.filter_by(id=element).first().valeurs
            Valeur_cc.append(valeur_cc)

            # Pour chaque cause racine on recupere l'ensemble des actions definis 
            #liste_action = ActionIndividuelle.recup_action(all_pourquoi5)[0] #l'ensemble des actions par id
            table = ActionIndividuelle.recup_action(all_pourquoi5)[2] #l'ensemble des actions par id
            act = ActionIndividuelle.recup_action(all_pourquoi5)[1] # liste nombre d'actions par id
            table_pourquoi1.append(all_p1) # l'ensemble des pourquoi1 pour tous les conseillers
            table_pourquoi2.append(all_p2) # l'ensemble des pourquoi2 pour tous les conseillers
            table_pourquoi3.append(all_p3) # l'ensemble des pourquoi3 pour tous les conseillers
            table_pourquoi4.append(all_p4) # l'ensemble des pourquoi4 pour tous les conseillers
            table_pourquoi5.append(all_p5) # l'ensemble des pourquoi5 pour tous les conseillers
            table_axe.append(all_axe_analyse) # l'ensemble des axes d'analyses pour tous les conseillers
            table_action.append(table) #l'ensemble des actions pour tous les conseillers
            nbre_act.append(act) # l'ensemble des liste de nombre d'actions pour tous les conseillers
            N.append(act[0]+act[1]+act[2]+act[3]+act[4]+act[5])# liste des nombre d'actions totale pour tous les conseillers
            nbre_cc += 1
        cc = [nbre_cc, Nom_cc, Valeur_cc]
        Action = [N, nbre_act, table_action]
        table_pourquoi_axe = [table_pourquoi1, table_pourquoi2, table_pourquoi3, table_pourquoi4, table_pourquoi5, table_axe]
        #print(Action)
        #print(table_pourquoi_axe)
        return table_pourquoi_axe, Action, cc

init_base()