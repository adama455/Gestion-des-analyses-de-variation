# -*- coding: utf-8 -*-
import sys
import datetime
import subprocess
sys.path.append('.')
sys.path.append('..')
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm, CausesForm, PlateauForm, RequestResetForm, ResetPasswordForm
from analyseVariation.models import User, ValeursAberrante, Enregistrement_AV, Cause, Plateau,Role, ActionIndividuelle,ActionProgramme, AnalyseApporter, Fichiers, Pourquoi1, Pourquoi2, Pourquoi3, Pourquoi4, Pourquoi5, Kpi
from analyseVariation import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from flask_user import login_required, UserManager, SQLAlchemyAdapter
from flask_user import roles_required
from functools import wraps
import os
from tkinter import filedialog
from tkinter import *
from openpyxl import load_workbook
import csv
import pandas as pd
from datetime import date
from threading import Thread
db_adapter = SQLAlchemyAdapter(db, User) # Register the User model
user_manager = UserManager(db_adapter, app) # Initialize Flask-User
# user_datastore = SQLAlchemyUserDatastore(db,User,Role)
# security = Security(app,user_datastore)
from werkzeug.utils import secure_filename



#la racine ou page connexion des utilisateurs
@app.route('/', methods=('GET', 'POST'))
@app.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method=='POST':
    #if form.validate_on_submit():
        print(form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Une erreur s est produit, veillez verifier les information que vous avez saisi', 'danger')
    return render_template('login.html', title='Login', form=form)    

#La page acceuil de notre application
@app.route("/home")
@login_required
def home():
    form = RegistrationForm()
    return render_template('home.html', title='Régister', form=form)    

#Cette page permet a l'administrateur d'ajouter de users
@app.route("/addUser", methods=('GET', 'POST'))
@login_required
def addUser():
    if current_user.is_authenticated:
        return redirect(url_for('compte'))
    form = RegistrationForm()
    if request.method=='POST':
        password = 'Sovar@2023'
        prenom=request.args.get('prenom')
        print('test ', form.prenom.data)
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
            user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data, hashed_password)
            print(user)
            db.session.add(user)
            db.session.commit()
            flash('Votre compte a été bien créé', 'success') 
        return redirect(url_for('login'))
    return render_template('add-user.html', title='Register', form=form)
#Cette page permet voir les détail d'un Utilisateur
@app.route("/detailUser/<int:id>")
@login_required
def detailUser(id):
    oneUser = User.query.filter_by(id=id).first()
    if oneUser:
        return render_template('detail.user.html', title='Détail', user=oneUser) 
    return f"Utilisateur avec id ={id} n'existe pas!"    

#C'est ici que le changement de mot de passe est effectuer pour les utilisateurs
@app.route("/change-password")
@login_required
def changepassword():
    return render_template('changepassword.html')    

@app.route("/compte", methods=('GET', 'POST'))
# @login_required
# @roles_required('admin')
def compte():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method=='POST':
            password = 'Sovar@2023'
            print('test ', form.profil.data)
            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
            plateau_id=request.form['plateau']
            user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data, form.profil.data, plateau_id, hashed_password)
            print('data_User:', user)
            if user.profil=='ADMIN':
                user.roles.append(Role(name='admin'))
            elif user.profil=='MANAGER_OPERATIONNEL':    
                user.roles.append(Role(name='manager_operationnel'))
            else:
                user.roles.append(Role(name='superviseur_operationnel'))
            emailUser = User.query.filter_by(email=request.form.get('email')).first()
            if emailUser:
                flash('Email que vous avez entrez exist déjas','danger')
                return redirect(url_for('compte'))
            print(user)
            db.session.add(user)
            db.session.commit()
            flash('Votre compte a été bien créé','success')
            return redirect(url_for('compte'))

    users = User.query.all() #Récuperation de l'enssemble des utilisateurs::
    plateaux = Plateau.query.all() #Récuperation de l'enssemble des plateaux::
    
    # print('profil',users.profil.value)
    return render_template('comptes.html', title='Register', form=form,data=users, plateaux=plateaux) 

#Cette page permet voir les détail d'un Utilisateur
@app.route("/editUser", methods=['GET', 'POST'])
@login_required
def editUser():
    form = RegistrationForm()   
    if request.method =='POST':
        data = User.query.get(request.form.get('id'))
        data.username = request.form['username']
        data.prenom = request.form['prenom']
        data.nom = request.form['nom']
        data.email = request.form['email']
        data.profil = form.profil.data
        data.plateau_id = request.form['plateau']
        print('profil',data.plateau_id)
        print("Roles_utilisateur:",data.roles) 
        for role in data.roles:
            role.name = form.profil.data.lower()
                
        db.session.commit()
        flash('Utilisateur modifié avec Succès!','success')
        return redirect(url_for('compte'))
    return render_template('comptes.html', title='Register')

#Permet de Supprimer un utilisateur
@app.route("/supprimerUser/<id>/", methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def supprimerUser(id):
    form = RegistrationForm()
    if not id or id != 0:
        oneUser = User.query.get(id)
        db.session.delete(oneUser)
        db.session.commit()
        flash('Utilisateur supprimer avec succès', 'success')
        return redirect(url_for('compte'))
    users = User.query.all()
    return render_template('comptes.html', title='Register', form=form, data=users) 

#Permet de Lister une Cause
@app.route("/cause", methods=['POST','GET'])
@login_required
@roles_required('admin')
def cause():
    form = CausesForm()
    if request.method =='POST':
        if form.validate_on_submit():
            cause = Cause(form.libelle.data, form.description.data)
            db.session.add(cause)
            db.session.commit()
            flash('Une nouvelle Cause vient être ajoutée', 'success') 
        return redirect(url_for('cause'))
    data = Cause.query.all()
    return render_template('causes.html', title='Cause', form=form, causes = data)    

#Cette page permet Modifier une Cause
@app.route("/editCause", methods=['POST','GET'])
@login_required
@roles_required('admin')
def editCause():
    if request.method =='POST':
        data = Cause.query.get(request.form.get('id'))
        data.libelle = request.form['libelle']
        data.description = request.form['description']
        db.session.commit()
        flash('Cause modifié avec Succès!','success')
        return redirect(url_for('cause'))
    return render_template('causes.html', title='Cause')

#Permet de Supprimer une Cause
@app.route("/supprimerCause/<id>/", methods=('GET', 'POST'))
@login_required
def supprimerCause(id):
    form = CausesForm()
    if not id or id != 0:
        oneCause = Cause.query.get(id)
        db.session.delete(oneCause)
        db.session.commit()
        flash('Cause supprimer avec succès', 'success')
        return redirect(url_for('cause'))
    data = Cause.query.all() #Récuperation de l'enssemble des utilisateurs::
    return render_template('causes.html', title='Cause', form=form, causes=data) 

#C'est ici qu'on voit les plateaux
@app.route("/plateau", methods=('GET', 'POST'))
# @login_required
# @roles_required('admin')
def plateau():
    form = PlateauForm()
    if request.method =='POST':
        # if form.validate_on_submit():
            print('form.libelle.data')
            plateau = Plateau(form.libelle.data, form.description.data, form.univers.data)
            plateau.users=[]
            db.session.add(plateau)
            db.session.commit()
            flash('Un nouveau Plateau vient être ajoutée', 'success') 
            return redirect(url_for('plateau'))
    data = Plateau.query.all()
    return render_template('plateau.html', tiltle='Plateau', form=form, plateaux=data)    

#Cette page permet Modifier une Cause
@app.route("/editPlateau", methods=['POST','GET'])
@login_required
@roles_required('admin')
def editPlateau():
    if request.method =='POST':
        data = Plateau.query.get(request.form.get('id'))
        data.libelle = request.form['libelle']
        data.description = request.form['description']
        data.univers= request.form['univers']
        db.session.commit()
        flash('Plateau modifié avec Succès!','success')
        return redirect(url_for('plateau'))
    return render_template('plateau.html', title='Plateau')

#Permet de Supprimer une Cause
@app.route("/supprimerPlateau/<id>/", methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def supprimerPlateau(id):
    form = PlateauForm()
    if not id or id != 0:
        onePlateau = Plateau.query.get(id)
        db.session.delete(onePlateau)
        db.session.commit()
        flash('Plateau supprimer avec succès', 'success')
        return redirect(url_for('plateau'))
    data = Plateau.query.all() #Récuperation de l'enssemble des utilisateurs::
    return render_template('plateau.html', title='Plateau', form=form, plateaux=data) 

#Permet de visualiser la liste des Analyses de Variation
@app.route("/listeAv")
@login_required
def listeAv():
    form = LoginForm()
    liste_analyse_variation = []
    all_av = Fichiers.query.all()
    nbre_av =len(all_av)
    for elem in all_av:
        nom = User.query.filter_by(id=elem.user_id).first().nom
        prenom = User.query.filter_by(id=elem.user_id).first().prenom
        agent = prenom + ' '+ nom.upper()
        champ_analyse_variation = [elem.id, elem.libelle, agent, elem.date]
        liste_analyse_variation.append(champ_analyse_variation)
    return render_template('listeAv.html', title='Register', form=form, liste_analyse_variation=liste_analyse_variation, 
                           nbre_av=nbre_av)

#Permet de visualiser la liste des Analyses de Variation
@app.route("/fichiers")
@login_required
def fichiers():
    form = LoginForm()
    liste_fichier = []
    all_av = Fichiers.query.all() 
    nbre_av =len(all_av)
    for elem in all_av:
        nom = User.query.filter_by(id=elem.user_id).first().nom
        prenom = User.query.filter_by(id=elem.user_id).first().prenom
        agent = prenom + ' '+ nom.upper()
        champ_fichier = [elem.id, elem.nom_fichier, elem.effectif, elem.date, elem.libelle, agent]
        liste_fichier.append(champ_fichier)
    return render_template('fichiers.html', title='Register', form=form, liste_fichier=liste_fichier, nbre_av=nbre_av)

#Permet de visualiser le fichier en global(nom cc et valeurs)
@app.route("/fichiers_global")
@login_required
def fichiers_global():
    return render_template('fichiers_global.html', title='fichier global')
    

@app.route("/listepa")
@login_required
def listepa():
    form = LoginForm()
    return render_template('listepa.html', title='Register', form=form)

@app.route("/editpa", methods=('GET', 'POST'))
@login_required
def editpa():
    form = LoginForm()
    id_action=request.args.get('id_action')
    action = ActionIndividuelle.query.filter_by(id=int(id_action)).first()
    id_va = Pourquoi5.query.filter_by(id=action.pourquoi5_id).first().valeur_aberrante_id
    valeur_aberrante = ValeursAberrante.query.filter_by(id=id_va).first()
    user = User.query.filter_by(id=valeur_aberrante.user_id).first()
    if request.method=='POST':
        action.status = request.form.get('status')
        action.libelle_action = request.form.get('libelle_action')
        action.porteur = request.form.get('porteur_action')
        action.echeance = request.form.get('echeance_action')
        action.commentaire = request.form.get('commentaire')
        db.session.commit()
    return render_template('editpa.html', title='Register', form=form, action=action, user=user, 
                           valeur_aberrante=valeur_aberrante)

#Permet de visualiser la liste des Valeurs Aberantes
@app.route("/listeVa", methods=('GET', 'POST' ))
@login_required
def listeVa():
    form = RegistrationForm()
    infos_fichier = []
    fichier_id = int(request.args.get('fichier_id'))
    liste = ValeursAberrante.query.filter_by(fichier_id=fichier_id).all()
    n = len(liste)
    data = Fichiers.query.filter_by(id=fichier_id).all()
    nbre_fichier = len(data)
    print ("Liste va :", data)
    for elem in data:
        nom = User.query.filter_by(id=elem.user_id).first().nom
        prenom = User.query.filter_by(id=elem.user_id).first().prenom
        agent = prenom + ' '+ nom.upper()
        kpi = Kpi.query.filter_by(id=elem.user_id).first().libelle
        info = [
            elem.id, elem.date, agent, elem.libelle, kpi, elem.equipe,
            elem.vsf, elem.limite_ctrl_sup,elem.limite_ctrl_inf,
            elem.nbre_va_sur_perf,elem.nbre_va_sous_perf,elem.effectif,elem.statut
        ]
        infos_fichier.append(info)
        print("info : ", infos_fichier)
    statut_action = 'En attente'
    return render_template('listeVa.html',title='liste VA', form=form, liste=liste, n=n, fichier_id=fichier_id, 
                           statut_action=statut_action, nbre_fichier=nbre_fichier, infos_fichier=infos_fichier)

#Permet d'enregistrer une cause
@app.route("/analyseCause")
@login_required
def analyseCause():
    form = RegistrationForm()
    return render_template('analyse-cause.html',title='Analyse Cause', form=form)

#Permet de Méttre à jours une action :::::::::::::::::
@app.route("/miseAjourAc")
@login_required
def miseAjourAc():
    form = RegistrationForm()
    return render_template('mise-a-jour-action.html', title='Analyse Cause', form=form)

#Permet de Méttre à jours une action :::::::::::::::::::::::::::::
@app.route("/rejeterAv")
@login_required
@roles_required('admin')
def rejeterAv():
    form = RegistrationForm()
    reference = request.args.get('reference')
    print ('data.libelle_av:', reference)
    data = Enregistrement_AV.query.filter_by(reference_av=reference).first()
    libelle = data.libelle_av
    agent = data.agent
    return render_template('rejeterAv.html',title='Analyse Cause', form=form, reference=reference, 
                           libelle=libelle, agent=agent)

#Permet a tout utilisateur de verifier son profil
@app.route("/profil", methods=('GET', 'POST'))
@login_required
def profil():
    form = RegistrationForm()
    #request_data = request.get_json()
    return render_template('profil.html',title='Analyse Cause', form=form)

#enregistrement d'une AV par le MO
@app.route("/analyse_agent", methods=('GET', 'POST'))
@login_required
def analyse_agent():
    #recuperer la reference de l'AV au niveaude l'url et l'utiliser pour recuperer les infos corespondantes
    fichier_id = int(request.args.get('fichier_id'))
    try:
        data_fichier = Fichiers.query.filter_by(id=fichier_id).first()
        causes = Cause.query.all()
        cause = []
        for elem in causes:
            cause.append(elem.libelle)
        libelle = data_fichier.libelle
        id_va = request.args.get('id_va') ### Il constitut l'id de la valeur aberrante
        valeurs_aberante = ValeursAberrante.query.filter_by(id=int(id_va)).first()
        nom_conseiller = valeurs_aberante.nom_cc.split('(')[1].split(')')[0].strip(' ')
        valeurs_aberante_cc = valeurs_aberante.valeurs
        nom = User.query.filter_by(id=data_fichier.user_id).first().nom
        prenom = User.query.filter_by(id=data_fichier.user_id).first().prenom
        agent = prenom + ' '+ nom
        initial =prenom[0] + nom[0]
        id = nom_conseiller+initial
        data_exist = 0
        datacc = Pourquoi5.query.filter_by(valeur_aberrante_id=id_va).first()
    except AttributeError:
        print('Un probleme est survenu sur la recuperation des attributs.')
    if request.method=='POST':
        Pourquoi1.insert_p1(int(id_va))
        Pourquoi2.insert_p2(int(id_va))
        Pourquoi3.insert_p3(int(id_va))
        Pourquoi4.insert_p4(int(id_va))
        Pourquoi5.insert_p5(int(id_va))
        # AnalyseApporter.insert_update_pourquoi(id, datacc, fichier_id)
        return redirect(url_for('ajouter_action', fichier_id=fichier_id, id_va=id_va, id=id))
    elif datacc:
        data_exist = 1
        liste_pourquoi = AnalyseApporter.traitement_data_pourquoi(id_va,datacc)[0]
        #nbre_pourquoi = AnalyseApporter.traitement_data_pourquoi(datacc)[1]
        #print(liste_pourquoi,liste_pourquoiBis)
        #liste_pourquoi = AnalyseApporter.update_pourquoi(datacc, liste_pourquoi)[0]
        #nbre_pourquoi = AnalyseApporter.update_pourquoi(datacc)[1]
        return render_template('analyse-agent.html', data_exist=data_exist, liste_pourquoi=liste_pourquoi, 
                               fichier_id=fichier_id, libelle=libelle, cause=cause, nom_conseiller=nom_conseiller, 
                               valeurs_aberante_cc=valeurs_aberante_cc, agent=agent)
        # except:
        flash("Une erreur s'est produit")
    try:
        return render_template('analyse-agent.html', fichier_id=fichier_id, libelle=libelle, agent=agent, cause=cause, 
                           nom_conseiller=nom_conseiller, valeurs_aberante_cc=valeurs_aberante_cc)    
    except UnboundLocalError:
        flash('Erreur de referencement.')
        return render_template('analyse-agent.html')

@app.route("/ajouter_action", methods=('GET', 'POST'))
@login_required
def ajouter_action():
    #recuperer la reference de l'AV au niveaude l'url et l'utiliser pour recuperer les infos corespondantes
    fichier_id = request.args.get('fichier_id')
    print(fichier_id)
    data_fichier = Fichiers.query.filter_by(id=int(fichier_id)).first()
    causes = Cause.query.all()
    cause = []
    for elem in causes:
        cause.append(elem.libelle)
    libelle = data_fichier.libelle #libelle de l'analyse de variation
    id_va= int(request.args.get('id_va')) #rang du conseiller sur la liste des valeurs aberantes
    nom_conseiller = ValeursAberrante.query.filter_by(id=id_va).first().nom_cc
    valeurs_aberante_cc = ValeursAberrante.query.filter_by(id=id_va).first().valeurs
    nom = User.query.filter_by(id=data_fichier.user_id).first().nom
    prenom = User.query.filter_by(id=data_fichier.user_id).first().prenom
    agent = prenom + ' '+ nom
    datacc = Pourquoi5.query.filter_by(valeur_aberrante_id=id_va).first()
    #Recuperation de l'ensemble des actions en rapport avec le conseiller 
    # pour les afficher sur le tableau recaputilatif
    all_causes_racines = Pourquoi5.query.filter_by(valeur_aberrante_id=int(id_va)).all()
    liste_action = ActionIndividuelle.recup_action(all_causes_racines)[0]                        
    nbre_act = ActionIndividuelle.recup_action(all_causes_racines)[1]
    #Insertion des donnees action individuelles au niveau de la base de donnees
    #On recupere les donnees poster par ajouteaction.js sur l'url ajouter-action............
    try:
        data_input_action = request.form.get('data')
        data_input_action = data_input_action.split('|')
        data_input_action.pop()
        print("data_input_action :", data_input_action)
        for el in data_input_action:
            act = [elem for elem in el.split(',') if elem!='']
            print('data :' ,act)
            # k=act[0].split('_')[2].split('.')[0]    
            k=act[4].split('_')[2].split('.')[0]              
            p5_id = Pourquoi5.query.filter_by(code=f'P5{k}', valeur_aberrante_id=id_va).first().id
            act_exist = ActionIndividuelle.query.filter_by(pourquoi5_id=p5_id,reference_action=act[0]).first() 
            if not act_exist:
                action = ActionIndividuelle(act[0], act[1], act[2], act[3], 'En attente','', p5_id)
                db.session.add(action)
                db.session.commit()
    except AttributeError:
        print('echec de recuperation des elements, erreur attribut')
    if request.method=='POST':
        return redirect(url_for('listeVa', fichier_id=fichier_id))
        # except:
        # flash("Pas de modifications apportées sur les pourquoi saisis")
    if datacc:
        data_pourquoi = AnalyseApporter.traitement_data_pourquoi(id_va,datacc)
        liste_pourquoi = data_pourquoi[0]
        nbre_pourquoi = data_pourquoi[1]
        all_va = ValeursAberrante.query.filter_by(id=id_va).all()
        Pourquoi = Pourquoi5.recup_all_pourquoi(all_va)[0]
        Action = Pourquoi5.recup_all_pourquoi(all_va)[1]
        CC = Pourquoi5.recup_all_pourquoi(all_va)[2]
        disposition_btn = Pourquoi5.position_button(all_causes_racines) # pour le positionnement des boutons definir action
        return render_template('ajouter-action.html', id_va=id_va, nbre_pourquoi=nbre_pourquoi, datacc=datacc, 
                               fichier_id=fichier_id, libelle=libelle, agent=agent, liste_action=liste_action, 
                               Pourquoi=Pourquoi,CC=CC, Action=Action, liste_pourquoi=liste_pourquoi, nom_conseiller=id, 
                               valeurs_aberante_cc=valeurs_aberante_cc, nbre_act=nbre_act, cause=cause, position_button=disposition_btn)

@app.route("/recaputilatif", methods=('POST', 'GET'))
@login_required
def recap_value():
    #all_data = AnalyseApporter.query.all()
    all_va = ValeursAberrante.query.all()
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
    table_pourquoi_axe = [table_pourquoi1, table_pourquoi2, table_pourquoi3, table_pourquoi4, table_pourquoi5, table_axe]
    #print(table_pourquoi_axe)
    #act_p1 = [3, 2, 0, 0, 0, 0]
    #print()
    return render_template('recap.html', N=N, nbre_act=nbre_act, nbre_cc=nbre_cc, table_pourquoi_axe=table_pourquoi_axe, 
                        table_action=table_action, Nom_cc=Nom_cc, Valeur_cc=Valeur_cc) 


    return render_template('recap.html', table_liste_pourquoi=table_liste_pourquoi, table_nbre_pourquoi=table_nbre_pourquoi, liste_identifiant=liste_identifiant,
                           table_liste_action=table_liste_action, table_nbre_action=table_nbre_action, nbre_analyse=nbre_analyse, reference=reference)

# @app.route("/reset_request", methods=('POST', 'GET'))
# @login_required
# def reset_request():
#     request_data = request.get_json()

#     return render_template('reset_request.html')

# @app.route("/demarrer-av")
# @login_required
# def demarrerav():

#     return render_template('demarrer-av.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('login')

@app.route("/synthese-av", methods=('POST', 'GET'))
def synthese_av():
    try :
        nom_fichier = request.args.get('filename')
        kpi = request.args.get('kpi')
        libelle_analyse = request.args.get('libelle_analyse')
        equipe = request.args.get('equipe')
        reference = '000012'
        data = pd.read_excel(nom_fichier)
        mesures = data.Mesures.dropna()
        data = data.dropna()
        Date = date.today()
        effectif = data["Mesures"].count()
        exist_file = Fichiers.query.filter_by(nom_fichier=nom_fichier).first()
        print(current_user.id)
        #intervale_analyse = request.form.get('date1') + '-'+request.form.get('date2')
        data['Mesures'] = pd.to_numeric(data['Mesures'], errors='coerce')
        limite_ctrl_sup = round(data['Mesures'].std() + data['Mesures'].mean(), 2)
        limite_ctrl_inf = round(data['Mesures'].mean() - data['Mesures'].std(), 2)
        VSF = round((data['Mesures'].std()*6)/data['Mesures'].mean(), 2)
        nbre_mesure = data.Nom.count()
        print( limite_ctrl_sup, data['Mesures'].std(), data['Mesures'].mean())
        if kpi == 'DMT':
            #max = pd.to_numeric(mesures, errors='coerce').max()
            #min = pd.to_numeric(mesures, errors='coerce').min()
            nbre_va_sous_perf = data[data["Mesures"]<limite_ctrl_inf].Nom.count()
            nbre_va_sur_perf = data[data["Mesures"]> limite_ctrl_sup].Nom.count()
            #data = data[(data["Mesures"]<limite_ctrl_inf)|(data['Mesures']> limite_ctrl_sup)]
            data = data[(data["Mesures"]<650)|(data['Mesures']> 1000)]
            kpi_id = Kpi.query.filter_by(libelle='dmt').first().id
        mesures_a_objectif = nbre_mesure-(nbre_va_sur_perf + nbre_va_sous_perf)
        paramettre_analyse_variation = [ limite_ctrl_sup, limite_ctrl_inf, VSF, nbre_mesure, mesures_a_objectif]
        prenom = current_user.prenom
        nom = current_user.nom
        insert_fichier = Fichiers(nom_fichier, libelle_analyse, effectif, Date, ' ', 'Equipe', VSF, limite_ctrl_sup, 
                                  limite_ctrl_inf, nbre_va_sur_perf, nbre_va_sous_perf, 'En cours', kpi_id,  
                                  int(current_user.id))
        if not exist_file:
            db.session.add(insert_fichier)
            db.session.commit()
    except:
        flash('Aucun fichier ou format non compatible','warning')

    fichier = Fichiers.query.filter_by(nom_fichier=nom_fichier).first()
    valeur_exist = ValeursAberrante.query.filter_by(fichier_id=fichier.id).first()
    if not valeur_exist:
        for i in range(data.shape[0]):
            valeur_aberante = ValeursAberrante(data['Nom'][data.index[i]], data['Mesures'][data.index[i]], ' ', 'En cours', fichier.id, int(current_user.id))
            db.session.add(valeur_aberante)
            db.session.commit()

    if request.method=='POST':
        libelle = request.form['libelle']
        statut = request.form['statut']
        Fichiers.agent = prenom +' '+ nom
        Fichiers.reference_av = reference
        Fichiers.libelle = libelle
        Fichiers.date = Date
        Fichiers.statut_analyse = statut
        db.session.commit()
        return redirect(url_for('listeVa', fichier_id=fichier.id)) 
    try:
        return render_template('synthese-av.html', fichier_id=fichier.id, prenom=prenom, Date=Date, nom=nom, nbr_va_sou_perf=nbre_va_sous_perf, 
                               nbr_va_sur_perf=nbre_va_sur_perf, libelle_analyse=libelle_analyse, kpi=kpi, paramettre_analyse_variation=paramettre_analyse_variation)  
    except:
        return render_template('home.html')
    
# # UPLOAD_FOLDER = "/home"

# def CreateNewDir():
#     print("I am being called")
#     global UPLOAD_FOLDER
#     print (UPLOAD_FOLDER)
#     UPLOAD_FOLDER = UPLOAD_FOLDER+datetime.datetime.now().strftime("%d%m%y%H")
#     cmd="mkdir -p %s && ls -lrt %s"%(UPLOAD_FOLDER,UPLOAD_FOLDER)
#     output = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE).communicate()[0]

#     if "total 0" in output:
#         print ("Success: Created Directory %s"%(UPLOAD_FOLDER)) 
#     else:
#         print ("Failure: Failed to Create a Directory (or) Directory already Exists",UPLOAD_FOLDER)


# UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xsl'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file () :
    try:
        print(request.form['libelle_analyse'])
        print(request.form['kpi'])
        kpi = request.form['kpi']
        libelle_analyse = request.form['libelle_analyse']
        if request.method == 'POST':
            #check if the post request has the file part
            # if 'file' not in request.files:
            #     flash('No file part')
            #     return redirect(request.url)
            file = request.files['file']
            # # # If the user does not select a file, the browser submits an
            # # # empty file without a filename.
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            # if file and allowed_file(file.filename):
            file.save(secure_filename(file.filename))
            filename = secure_filename(file.filename)
            print('filename : ', filename)
            # file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('synthese_av', filename=filename, kpi=kpi, libelle_analyse=libelle_analyse))
        # filename = filedialog.askopenfilename(initialdir='/home', title="Selectionner le fichier",
        #                                      filetypes=(("Tous les fichiers","*.*"), ("Fichier texte","*.txt"), ("Fichier excel","*.xsl")))

        return render_template(url_for('synthese-av.html', filename=filename, kpi=kpi, libelle_analyse=libelle_analyse))
    except:
        flash('Erreur de chargement du fichier ','danger')

@app.route("/action_programme", methods=["GET", "POST"])
@login_required
def action_programme():
    #Insertion des donnees action programme au niveau de la base de donnees
    #On recupere les donnees poster par js sur l'url ajouter-action............
    try:
        data_act_prog = request.form['data']
        data_act_prog = data_act_prog.split('|')
        data_act_prog.pop()
        for el in data_act_prog:
            act_prg = [elem for elem in el.split('{') if elem!='']
            if act_prg:
                for el in act_prg:
                    print("element:", el)
                    actions = [elem for elem in el.split(',') if elem !='']
                    print("actionsss:", actions)
                    print("act1:", act_prg[1])
                    if actions: 
                        action = ActionProgramme(actions[0], actions[1], actions[2], actions[3], 'En attente','')
                        print(action)
                        db.session.add(action)
                        db.session.commit()
    except:
        print('echec de recuperation des elements')
    return render_template('action_programme.html')

@app.route("/suivi_actions", methods=["GET", "POST"])
#@login_required
def suivi_action():
    all_va = ValeursAberrante.query.all()
    table_pourquoi = []
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
        all_pourquoi5 = Pourquoi5.query.filter_by(valeur_aberrante_id=element).all()
        all_cause_racine = []
        all_axe_analyse = []
        for elem in all_pourquoi5:
            axe = Cause.query.filter_by(id=elem.axe_analyse_id).first().libelle
            all_axe_analyse.append(axe)
            all_cause_racine.append(elem.details)
        nom_cc = ValeursAberrante.query.filter_by(id=element).first().nom_cc
        Nom_cc.append(nom_cc)
        valeur_cc = ValeursAberrante.query.filter_by(id=element).first().valeurs
        Valeur_cc.append(valeur_cc)
        # Pour chaque cause racine on recupere l'ensemble des actions definis 
        #liste_action = ActionIndividuelle.recup_action(all_pourquoi5)[0] #l'ensemble des actions par id
        table = ActionIndividuelle.recup_action(all_pourquoi5)[2] #l'ensemble des actions par id
        act = ActionIndividuelle.recup_action(all_pourquoi5)[1] # liste nombre d'actions par id
        table_pourquoi.append(all_cause_racine) # l'ensemble des causes racines pour tous les conseillers
        table_axe.append(all_axe_analyse) # l'ensemble des axes d'analyses pour tous les conseillers
        table_action.append(table) #l'ensemble des actions pour tous les conseillers
        nbre_act.append(act) # l'ensemble des liste de nombre d'actions pour tous les conseillers
        N.append(act[0]+act[1]+act[2]+act[3]+act[4]+act[5])# liste des nombre d'actions totale pour tous les conseillers
        nbre_cc += 1
    table_pourquoi_axe = [table_pourquoi, table_axe]
    return render_template('suivi_actions.html', N=N, nbre_act=nbre_act, nbre_cc=nbre_cc, liste_identifiant=liste_identifiant, table_pourquoi_axe=table_pourquoi_axe, 
                           table_action=table_action, Nom_cc=Nom_cc, Valeur_cc=Valeur_cc)


@app.route("/recap_action_programme", methods=["GET", "POST"])
@login_required
def recap_action_programme():
    all_data = ActionProgramme.query.all() #on recupere tous les identifiants des conseiller deja analysé
    table_liste_causes = []
    table_liste_action = []
    table_liste_porteur = []
    table_liste_echeance = []
    nbre_analyse = len(all_data)
    liste_identifiant = []
    nbre = []
    
    for el in all_data :
        table_liste_causes.append(el.cause_racine)
        table_liste_action.append(el.action)
        table_liste_porteur.append(el.porteur)
        table_liste_echeance.append(el.echeance)
        table_nbre_action = len(table_liste_action)
        table_nbre_cause = len(table_liste_causes)
        # freq = Counter(table_liste_causes).get(el.cause_racine)
        # nbre.append(freq)
        # for  elem in table_liste_causes:
        if table_liste_causes.count(el.cause_racine)==1:
            nbre.append(el.cause_racine)
    
        print("Cause_racine:", el.cause_racine);
            
    print("all_data:", table_liste_causes);
    print("Nbre:", nbre)
    return render_template('recap_action_programme.html',nbre=nbre, nbre_analyse=nbre_analyse,table_nbre_cause=table_nbre_cause, 
                            table_liste_causes=table_liste_causes,table_liste_action=table_liste_action,
                            table_liste_porteur=table_liste_porteur,table_liste_echeance=table_liste_echeance
                        )
    
    
    
    
if __name__=='__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()