import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
from flask import current_app, request #<---HERE
from analyseVariation import db, init_base, login_manager
from sqlalchemy.orm import *
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    nom=db.Column(db.String(50), nullable=False)
    prenom=db.Column(db.String(150), nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    email=db.Column(db.String(50), unique=True, nullable=False)
    profil=db.Column(db.String(150), unique=False, nullable=False)
    # plateau=db.Column(db.String(150), unique=True, nullable=True)
    plateau_id = db.Column(db.Integer, db.ForeignKey('plateaux.id', ondelete='CASCADE'))
    
    password = db.Column(db.String(120), nullable=False)
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
        self.plateau_id = plateau_id
        # self.roles = roles
        
        
# /////////////////////////////////////
# Define the Role data model
class Role(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)

# Define the UserRoles data model
class UserRoles(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
   
# /////////////////////////////////////////////////////////////////////////////////////

class ActionProgramme(UserMixin,db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='action_programme'
    id=db.Column(db.Integer, primary_key=True)
    cause_racine=db.Column(db.String(255))
    libelle_action=db.Column(db.String(255))
    porteur=db.Column(db.String(80))
    echeance=db.Column(db.String(80))
    status=db.Column(db.String(80))
    commentaire=db.Column(db.String(80))
    pourquoi5_id = db.Column(db.Integer(), db.ForeignKey('pourquoi5.id', ondelete='CASCADE'))
    
    def __init__(self, cause_racine, libelle_action, porteur, echeance, statut, commentaire, pourquoi5_id):
        self.cause_racine = cause_racine
        self.libelle_action = libelle_action
        self.porteur = porteur
        self.echeance = echeance
        self.status = statut
        self.commentaire = commentaire
        self.pourquoi5_id = pourquoi5_id
        
    def recup_action(data):
        try:
            act_1 = []
            act_2 = []
            act_3 = []
            act_4 = []
            act_5 = []
            act_6 = []
            # reference = []
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
                action = ActionProgramme.query.filter_by(pourquoi5_id=element.id).all()
                if f'P5{n}'==((element.code)):
                    # ref = []
                    lib = []
                    por = []
                    ech = []
                    stat = []
                    for elem in action:
                        # ref.append(elem.reference_action)
                        # reference.append(elem.reference_action)
                        lib.append(elem.libelle_action)
                        libelle.append(elem.libelle_action)
                        por.append(elem.porteur)
                        porteur.append(elem.porteur)
                        ech.append(elem.echeance)
                        echeance.append(elem.echeance)
                        stat.append(elem.status)
                        id.append(elem.id)
                        statut.append(elem.status)
                    # liste_action[n-1].append(ref)
                    liste_action[n-1].append(lib)
                    liste_action[n-1].append(por)
                    liste_action[n-1].append(ech)
                    liste_action[n-1].append(stat)
                n+=1
            table.append(libelle)
            table.append(porteur)
            table.append(echeance)
            table.append(id)
            table.append(statut)
            nbre_act = []
            for elem in liste_action:
                if elem:
                    nbre_act.append(len(elem[0]))
                else:
                    nbre_act.append(0)
        except:
            nbre_act = [0, 0, 0, 0, 0, 0]
            print('on a pas pu recuperer les infos correspondant a cette reference')
        return liste_action, nbre_act, table

        
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
                    stat = []
                    for elem in action:
                        ref.append(elem.reference_action)
                        reference.append(elem.reference_action)
                        lib.append(elem.libelle_action)
                        libelle.append(elem.libelle_action)
                        por.append(elem.porteur)
                        porteur.append(elem.porteur)
                        ech.append(elem.echeance)
                        echeance.append(elem.echeance)
                        stat.append(elem.status)
                        id.append(elem.id)
                        statut.append(elem.status)
                    liste_action[n-1].append(ref)
                    liste_action[n-1].append(lib)
                    liste_action[n-1].append(por)
                    liste_action[n-1].append(ech)
                    liste_action[n-1].append(stat)
                n+=1
            table.append(libelle)
            table.append(porteur)
            table.append(echeance)
            table.append(id)
            table.append(statut)
            nbre_act = []
            for elem in liste_action:
                if elem:
                    nbre_act.append(len(elem[0]))
                else:
                    nbre_act.append(0)
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
    libelle = db.Column(db.String(80))
    description = db.Column(db.String(80))
    def __init__(self, libelle, description):
        self.libelle = libelle
        self.description = description

class Kpi(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='kpi'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))
    description = db.Column(db.String(255))
    def __init__(self, libelle, description):
        self.libelle = libelle
        self.description = description

class Equipe(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='equipe'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(80))
    description = db.Column(db.String(255))
    plateau_id = db.Column(db.String(80))
    def __init__(self, libelle, description, plateau_id):
        self.libelle = libelle
        self.description = description
        self.plateau_id = plateau_id

class Fichiers(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='fichiers'
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(50), unique=True, nullable=False)
    libelle = db.Column(db.String(50))
    effectif = db.Column(db.String(50))
    date = db.Column(db.Date)
    intervale_analyse = db.Column(db.String(50))
    equipe = db.Column(db.String(50))
    vsf = db.Column(db.String(50))
    limite_ctrl_sup = db.Column(db.String(50))
    limite_ctrl_inf = db.Column(db.String(50))
    nbre_va_sur_perf = db.Column(db.String(50))
    nbre_va_sous_perf = db.Column(db.String(50))
    statut = db.Column(db.String(50))
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpi.id', ondelete='CASCADE'),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    def __init__(self, nom_fichier, libelle, effectif, date, intervale_analyse, equipe, vsf, limite_ctrl_sup, limite_ctrl_inf, nbre_va_sur_perf, nbre_va_sous_perf, statut, kpi_id, user_id):
        self.nom_fichier = nom_fichier
        self.libelle = libelle
        self.effectif = effectif
        self.date = date
        self.intervale_analyse = intervale_analyse
        self.equipe = equipe
        self.vsf = vsf
        self.limite_ctrl_sup = limite_ctrl_sup
        self.limite_ctrl_inf = limite_ctrl_inf
        self.nbre_va_sur_perf = nbre_va_sur_perf
        self.nbre_va_sous_perf = nbre_va_sous_perf
        self.statut = statut
        self.kpi_id = kpi_id
        self.user_id = user_id
    def Importer(self, ):
        pass
    def traitement_data_pourquoi(id):
        pourquoi_1 = [ elem.details for elem in Pourquoi1.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_2 = [ elem.details for elem in Pourquoi2.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_3 = [ elem.details for elem in Pourquoi3.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_4 = [ elem.details for elem in Pourquoi4.query.filter_by(valeur_aberrante_id=id).all()]
        pourquoi_5 = [ elem.details for elem in Pourquoi5.query.filter_by(valeur_aberrante_id=id).all()]
        axes_analyse_id = [ elem.axe_analyse_id for elem in Pourquoi5.query.filter_by(valeur_aberrante_id=id).all()]
        axes_analyse = []
        for id in axes_analyse_id:
            axes_analyse.append(Cause.query.filter_by(id=int(id)).first().libelle)
        liste_pourquoi = [pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5, axes_analyse]
        nbre_pourquoi = [len(pourquoi_1), len(pourquoi_2), len(pourquoi_3), len(pourquoi_4), len(pourquoi_5)]
        return liste_pourquoi, nbre_pourquoi

    def update_p1(id):
        for i in range(1,4):
            if i==1:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code=f'P11').first()
                tmp=request.form.get('input_1') 
            else:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code=f'P1{i}').first()
                tmp=request.form.get(f'input_1{i}')
            if data and tmp:
                data = Pourquoi1(f'P1{i}', tmp, int(id))
                data.details = tmp
                print("Pourquoi11: ", data.details) 
                print("Details 11 : ", request.form.get('input_1')) 
                db.session.commit()
                

class ValeursFichier(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='valeurs_fichier'
    id = db.Column(db.Integer, primary_key=True)
    conseiller = db.Column(db.String(100))
    valeur = db.Column(db.Float)
    fichier_id = db.Column(db.Integer, db.ForeignKey('fichiers.id', ondelete='CASCADE'))
    def __init__(self, valeur, conseiller, fichier_id):
        self.Valeur = valeur
        self.conseiller = conseiller
        self.fichier_id = fichier_id
    def Importer(self, ):
        pass


class ValeursAberrante(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__='valeurs_aberrante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_cc = db.Column(db.String(80))
    valeurs = db.Column(db.Float)
    probleme = db.Column(db.String(100))
    statut = db.Column(db.String(50))
    fichier_id = db.Column(db.Integer, db.ForeignKey('fichiers.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    def __init__(self, nom_cc, valeurs, probleme, statut, fichier_id, user_id):
        self.nom_cc = nom_cc
        self.valeurs = valeurs
        self.probleme = probleme
        self.statut = statut
        self.fichier_id = fichier_id
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
            # elif tmp:
            #     # Pourquoi1.valeur_aberrante_id = int(id)
            #     # Pourquoi1.code = f'P1{i}'
            #     Pourquoi1.details = tmp
            #     db.session.commit()
    
    def update_p1(id):
        for i in range(1,4):
            if i==1:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code=f'P11').first()
                data.details=request.form.get('input_1') 
                db.session.commit()
            else:
                data = Pourquoi1.query.filter_by(valeur_aberrante_id=int(id),code=f'P1{i}').first()
                print("Pourquoi1 : ",data)
                if data:
                    data.details=request.form.get(f'input_1{i}')
                    db.session.commit()
                
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
                tmp = request.form.get('input_2')
            else:
                data = Pourquoi2.query.filter_by(valeur_aberrante_id=int(id),code=f'P2{i}').first()
                tmp = request.form.get(f'input_2{i}')
            if not data and tmp:
                data = Pourquoi2(f'P2{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            # else:
            #     # Pourquoi2.valeur_aberrante_id = int(id)
            #     # Pourquoi2.id = f'P2{i}'
            #     Pourquoi2.details = tmp
            #     db.session.commit()

    def update_p2(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi2.query.filter_by(valeur_aberrante_id=int(id),code=f'P21').first()
                data.details=request.form.get('input_2') 
                print("Pourquoi21 : ",data.details)
                # db.session.commit()
            else:
                data = Pourquoi2.query.filter_by(valeur_aberrante_id=int(id),code=f'P2{i}').first()
                if data != None:
                    data.details=request.form.get(f'input_2{i}')
                    print("Pourquoi23 : ",data.details)
                    db.session.commit()
                else:
                    print('vide')

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
                tmp = request.form.get('input_3')
            else:
                data = Pourquoi3.query.filter_by(valeur_aberrante_id=int(id),code=f'P3{i}').first()
                tmp = request.form.get(f'input_3{i}')
            if not data and tmp:
                data = Pourquoi3(f'P3{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            # else:
            #     # Pourquoi3.valeur_aberrante_id = int(id)
            #     # Pourquoi3.id = f'P3{i}'
            #     Pourquoi3.details = tmp
            #     db.session.commit()
                
    def update_p3(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi3.query.filter_by(valeur_aberrante_id=int(id),code=f'P31').first()
                data.details=request.form.get('input_3') 
                print("Pourquoi31 : ",data)
                db.session.commit()
            else:
                data = Pourquoi3.query.filter_by(valeur_aberrante_id=int(id),code=f'P3{i}').first()
                if data != None:
                    data.details=request.form.get(f'input_3{i}')
                    print("Pourquoi32 : ",data.details)
                    db.session.commit()
                else:
                    print('vide')


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
                tmp = request.form.get('input_4')
            else:
                data = Pourquoi4.query.filter_by(valeur_aberrante_id=int(id),code=f'P4{i}').first()
                tmp = request.form.get(f'input_4{i}')
            if not data and tmp:
                data = Pourquoi4(f'P4{i}', tmp, int(id))
                db.session.add(data)
                db.session.commit()
            # else:
            #     # Pourquoi4.valeur_aberrante_id = int(id)
            #     # Pourquoi4.id = f'P4{i}'
            #     Pourquoi4.details = tmp
            #     db.session.commit()
                
    def update_p4(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi4.query.filter_by(valeur_aberrante_id=int(id),code=f'P41').first()
                data.details=request.form.get('input_4') 
                print("Pourquoi41 : ",data.details)
                db.session.commit()
            else:
                data = Pourquoi4.query.filter_by(valeur_aberrante_id=int(id),code=f'P4{i}').first()
                if data != None:
                    data.details=request.form.get(f'input_4{i}')
                    print("Pourquoi42 : ",data.details)
                    db.session.commit()
                else:
                    print('vide')

    
    
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
                tmp = request.form.get('input_5')
                axe_id = Cause.query.filter_by(libelle=axe).first().id
                if not data and tmp:
                    data = Pourquoi5(f'P5{i}', tmp, axe_id, int(id))
                    db.session.add(data)
                    db.session.commit()
                # else:
                #     # Pourquoi5.valeur_aberrante_id = int(id)
                #     # Pourquoi5.id = f'P5{i}'
                #     Pourquoi5.details = tmp
                #     db.session.commit()
            elif axe:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code=f'P5{i}').first()
                tmp = request.form.get(f'input_5{i}')
                axe_id = Cause.query.filter_by(libelle=axe).first().id
                if not data and tmp:
                    data = Pourquoi5(f'P5{i}', tmp, axe_id, int(id))
                    db.session.add(data)
                    db.session.commit()
                # else:
                #     # Pourquoi5.valeur_aberrante_id = int(id)
                #     # Pourquoi5.id = f'P5{i}'
                #     Pourquoi5.details = tmp
                #     db.session.commit()
                    
    def update_p5(id):
        for i in range(1,7):
            if i==1:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code=f'P51').first() 
                data.details=request.form.get('input_5') 
                print("Pourquoi51 : ",data.details)
                db.session.commit()
            else:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code=f'P5{i}').first()
                if data != None:
                    data.details=request.form.get(f'input_5{i}')
                    print("Pourquoi52 : ",data.details)
                    db.session.commit()
                else:
                    print('vide')
    
    def update_axe_cause(id):
        for i in range(1,7):
            axe = request.form.get(f'axes_{i}_analyse')
            if i==1:
                data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code='P51').first()
                axe_id = Cause.query.filter_by(libelle=axe).first().id
                print("axe_id : ",axe_id)
                print("data_1 : ",data.axe_analyse_id )
                if data:
                    # data = Pourquoi5(f'P5{i}', axe_id, int(id))
                    data.axe_analyse_id = axe_id
                    print("data_2 : ",data.axe_analyse_id)
                    db.session.commit()
            else:
                if axe:
                    data = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id),code=f'P5{i}').first()
                    axe_id = Cause.query.filter_by(libelle=axe).first().id
                    print("axe_id2 : ",axe_id)
                    print("data_11  : ",data.axe_analyse_id )
                    if data:
                        data.axe_analyse_id = axe_id
                        print("data_22  : ",data.axe_analyse_id ) 
                        # db.session.add(data)
                        db.session.commit()
    
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
        nbre_p1 = []
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
            table = ActionIndividuelle.recup_action(all_pourquoi5)[2] #l'ensemble des actions par id
            act = ActionIndividuelle.recup_action(all_pourquoi5)[1] # liste nombre d'actions par id
            table_pourquoi1.append(all_p1) # l'ensemble des pourquoi1 pour tous les conseillers
            nbre_p1.append(len(all_p1)) # l'ensemble des pourquoi1 pour tous les conseillers
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
        table_pourquoi_axe = [table_pourquoi1, table_pourquoi2, table_pourquoi3, table_pourquoi4, table_pourquoi5, table_axe, nbre_p1]
        return table_pourquoi_axe, Action, cc
    

    def position_button(all_causes_racines):
        if len(all_causes_racines) == 6:
            return "col-2"
        elif len(all_causes_racines) == 4:
            return "col-3"
        elif len(all_causes_racines) == 2:
            return "col-6"
        
init_base()