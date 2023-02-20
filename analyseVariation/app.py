# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
sys.path.append('..')
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm, CausesForm, PlateauForm, RequestResetForm, ResetPasswordForm
from analyseVariation.models import User, ValeursAberrante, Enregistrement_AV, Cause, Plateau,Role, ActionProgramme, AnalyseApporter
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
# from .email import send_email
# from flask_mail import Message
from threading import Thread

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

# user_datastore = SQLAlchemyUserDatastore(db,User,Role)
# security = Security(app,user_datastore)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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



#Permet a l'admin de visualiser la liste des Utilisateurs.

# def login_required(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash("Vous êtes pas autorisé à acceder à cette ressource.", "warning")
#             return redirect(url_for('login'))
#     return wrap

@app.route("/compte", methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def compte():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method=='POST':
            password = 'Sovar@2023'
            print('test ', form.profil.data)
            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
            user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data, form.profil.data, hashed_password)
            if user.profil=='ADMIN':
                user.roles.append(Role(name='admin'))
            elif user.profil=='MANAGER_OPERATIONNEL':    
                user.roles.append(Role(name='mo'))
            else:
                user.roles.append(Role(name='so'))
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
    # print('profil',users.profil.value)
    return render_template('comptes.html', title='Register', form=form,data=users) 

#Cette page permet voir les détail d'un Utilisateur
@app.route("/editUser", methods=['GET', 'POST'])
@login_required
def editUser():
    form = RegistrationForm()   
    if request.method =='POST':
        data = User.query.get(request.form.get('id'))
        # data_Role = Role.query.get(request.form.get('id'))
        data.username = request.form['username']
        data.prenom = request.form['prenom']
        data.nom = request.form['nom']
        data.email = request.form['email']
        data.profil = form.profil.data
        print('profil',data.profil)
        if data.profil=='ADMIN':
            data.roles.clear()
            data.roles.append(Role(name='admin'))     
        elif data.profil=='MANAGER_OPERATIONNEL':
            data.roles.clear()
            data.roles.append(Role(name='mo'))
        else :
            data.roles.clear()
            data.roles.append(Role(name='so'))

        db.session.commit()
        flash('Utilisateur modifié avec Succès!','success')
        return redirect(url_for('compte'))
    return render_template('comptes.html', title='Register')

#Permet de Supprimer un utilisateur
@app.route("/supprimerUser/<id>/", methods=('GET', 'POST'))
@login_required
def supprimerUser(id):
    form = RegistrationForm()
    if not id or id != 0:
        oneUser = User.query.get(id)
        db.session.delete(oneUser)
        db.session.commit()
        flash('Utilisateur supprimer avec succès', 'success')
        return redirect(url_for('compte'))
    users = User.query.all() #Récuperation de l'enssemble des utilisateurs::
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
@login_required
@roles_required('admin')
def plateau():
    form = PlateauForm()
    if request.method =='POST':
        # if form.validate_on_submit():
            print('form.libelle.data')
            plateau = Plateau(form.libelle.data, form.description.data, form.univers.data)
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
    all_av = Enregistrement_AV.query.all()
    nbre_av =len(all_av)
    for elem in all_av:
        champ_analyse_variation = [elem.reference_av, elem.libelle_av, elem.agent, elem.date]
        liste_analyse_variation.append(champ_analyse_variation)
    return render_template('listeAv.html', title='Register', form=form, liste_analyse_variation=liste_analyse_variation, nbre_av=nbre_av)

@app.route("/listepa")
@login_required
def listepa():
    form = LoginForm()
    return render_template('listepa.html', title='Register', form=form)

@app.route("/editpa")
@login_required
def editpa():
    form = LoginForm()
    return render_template('editpa.html', title='Register', form=form)

#Permet de visualiser la liste des Valeurs Aberantes
@app.route("/listeVa", methods=('POST', 'GET'))
@login_required
def listeVa():
    form = RegistrationForm()
    ref = request.args.get('ref')
    liste = ValeursAberrante.query.filter_by(reference_av=ref).all()
    n = len(liste)
    statut_action = 'En attente'
    # print("data = ", liste[1].nom_cc, n)
    return render_template('listeVa.html',title='liste VA', form=form, liste=liste, n=n, reference=ref,statut_action=statut_action)

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
    return render_template('mise-a-jour-action.html',title='Analyse Cause', form=form)

#Permet de Méttre à jours une action :::::::::::::::::
@app.route("/rejeterAv")
@login_required
def rejeterAv():
    form = RegistrationForm()
    return render_template('rejeterAv.html',title='Analyse Cause', form=form)

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
    reference = request.args.get('reference')
    data = Enregistrement_AV.query.filter_by(reference_av=reference).first()
    causes = Cause.query.all()
    cause = []
    for elem in causes:
        cause.append(elem.libelle)
    libelle = data.libelle_av
    valeurs_aberante = ValeursAberrante.query.all()
    n = request.args.get('n')
    nom_conseiller = valeurs_aberante[int(n)].nom_cc[-20:-2]
    valeurs_aberante_cc = valeurs_aberante[int(n)].valeurs
    agent = data.agent
    initial = agent.split(' ')[0][0] + agent.split(' ')[-1][0]
    if request.method=='POST':
        try:
            identifiant = request.form['identifiant']
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

            print(pourquoi31, pourquoi32)
            id = identifiant+initial
            datacc = AnalyseApporter.query.filter_by(identifiant=id).first()
            #print('pourquoi',pourquoi1, datacc)
            if not datacc:
                pourquoi = AnalyseApporter(id, axes_analyse, probleme, pourquoi1, pourquoi21+pourquoi22, pourquoi31+pourquoi32, pourquoi41+pourquoi42, pourquoi51+pourquoi52)
                db.session.add(pourquoi)
                db.session.commit()
            return redirect(url_for('ajouter_action', reference=reference, n=n, id=id))
            #else:
            #    flash('Axe deja analyser pour cet identifiant')
        except:
            flash("Une erreur s'est produit")
    return render_template('analyse-agent.html', reference=reference, libelle=libelle, agent=agent, cause=cause, nom_conseiller=nom_conseiller, valeurs_aberante_cc=valeurs_aberante_cc)    


@app.route("/ajouter_action", methods=('GET', 'POST'))
@login_required
def ajouter_action():
    exist = 0
    #recuperer la reference de l'AV au niveaude l'url et l'utiliser pour recuperer les infos corespondantes
    reference = request.args.get('reference')
    data = Enregistrement_AV.query.filter_by(reference_av=reference).first()
    causes = Cause.query.all()
    cause = []
    for elem in causes:
        cause.append(elem.libelle)
    libelle = data.libelle_av #libelle de l'analyse de variation
    valeurs_aberante = ValeursAberrante.query.all()
    n=request.args.get('n') #rang du conseiller sur la liste des valeurs aberantes
    nom_conseiller = valeurs_aberante[int(n)].nom_cc
    valeurs_aberante_cc = valeurs_aberante[int(n)].valeurs
    agent = data.agent
    id = request.args.get('id')
    print(id)
    datacc = AnalyseApporter.query.filter_by(identifiant=id).first()
    #Recuperation de l'ensemble des actions en rapport avec le conseiller pour les afficher sur le tableau recaputilatif
    action_cc = ActionProgramme.query.filter_by(identifiant_cc=id).all()
    liste_action = ActionProgramme.recup_action(action_cc)[0]
    nbre_act = ActionProgramme.recup_action(action_cc)[1]

    #Insertion des donnees action individuelles au niveau de la base de donnees
    #On recupere les donnees poster par js sur l'url ajouter-action
    try:
        data_input_action = request.form.get('data')
        #print(s_role.split('|'))
        data_input_action = data_input_action.split('|')
        data_input_action.pop()
        for el in data_input_action:
            act = [elem for elem in el.split(',') if elem!='']
            action = ActionProgramme(id, act[0], act[1], act[2], act[3], '','' )
            db.session.add(action)
            db.session.commit()
            # print('voyons voir',act)
    except:
        print('echec de recuperation des elements')
    if datacc:
        print(exist)
        liste_pourquoi = AnalyseApporter.traitement_data_analyse_apporter(datacc)[0]
        nbre_pourquoi = AnalyseApporter.traitement_data_analyse_apporter(datacc)[1]
        return render_template('ajouter-action.html', n=n, nbre_pourquoi=nbre_pourquoi, datacc=datacc, reference=reference, libelle=libelle, agent=agent, cause=cause, liste_action=liste_action,
                            liste_pourquoi=liste_pourquoi, nom_conseiller=id, exist=exist, valeurs_aberante_cc=valeurs_aberante_cc, nbre_act=nbre_act)

    if request.method=='POST':
        try:
            datacc.probleme = request.form['probleme_act']
            datacc.pourquoi_1 = request.form['input_1_act']
            datacc.pourquoi_2 = '1.'+' _/_'+request.form['input_2_act']+' _/_2.'+ ' _/_'+request.form['input_21_act']
            datacc.pourquoi_3 = '1.'+' _/_'+request.form['input_3_act']+' _/_2.'+ ' _/_'+request.form['input_31_act']+' _/_3.'+ ' _/_'+request.form['input_32_act']+' _/_4.'+ ' _/_'+request.form['input_33_act']
            datacc.pourquoi_4 = '1.'+' _/_'+request.form['input_4_act']+' _/_2.'+ ' _/_'+request.form['input_41_act']+' _/_3.'+ ' _/_'+request.form['input_42_act']+' _/_4.'+ ' _/_'+request.form['input_43_act']
            datacc.pourquoi_5 = '1.'+' _/_'+request.form['input_5_act']+' _/_2.'+ ' _/_'+request.form['input_51_act']+' _/_3.'+ ' _/_'+request.form['input_52_act']+' _/_4.'+ ' _/_'+request.form['input_53_act']
            db.session.commit()
            return redirect(url_for('listeVa', ref=reference))
        except:
            flash("Pas de modifications apportées sur les pourquoi saisis")


@app.route("/recaputilatif", methods=('POST', 'GET'))
@login_required
def recap_value():
    all_data = AnalyseApporter.query.all() #on recupere tous les identifiants des conseiller deja analysé
    table_liste_pourquoi = []
    table_nbre_pourquoi = []
    table_liste_action = []
    table_nbre_action = []
    nbre_analyse = len(all_data)
    liste_identifiant = []
    for elem in all_data:
        liste_pourquoi = AnalyseApporter.traitement_data_analyse_apporter(elem)[0]
        table_liste_pourquoi.append(liste_pourquoi)
        nbre_pourquoi = AnalyseApporter.traitement_data_analyse_apporter(elem)[1]
        table_nbre_pourquoi.append(nbre_pourquoi)
        liste_identifiant.append(elem.identifiant)
        action_cc = ActionProgramme.query.filter_by(identifiant_cc=elem.identifiant).all()
        liste_action = ActionProgramme.recup_action(action_cc)[0]
        nbre_action = ActionProgramme.recup_action(action_cc)[1]
        table_liste_action.append(liste_action)
        table_nbre_action.append(nbre_action)
    return render_template('recap.html', table_liste_pourquoi=table_liste_pourquoi, table_nbre_pourquoi=table_nbre_pourquoi, liste_identifiant=liste_identifiant,
                           table_liste_action=table_liste_action, table_nbre_action=table_nbre_action, nbre_analyse=nbre_analyse)


@app.route("/reset_request", methods=('POST', 'GET'))
@login_required
def reset_request():
    request_data = request.get_json()

    return render_template('reset_request.html')

@app.route("/demarrer-av")
@login_required
def demarrerav():

    return render_template('demarrer-av.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('login')

@app.route("/synthese-av", methods=('POST', 'GET'))
def synthese_av():
    fichier = request.args.get('filename')
    try :
        reference = '000012'
        data = pd.read_excel(fichier)
        mesures = data.Mesures.dropna()
        data = data.dropna()
        data['Mesures'] = pd.to_numeric(data['Mesures'], errors='coerce')
        max = pd.to_numeric(mesures, errors='coerce').max()
        min = pd.to_numeric(mesures, errors='coerce').min()
        nbr_va_sou_perf = data[data["Mesures"]<650].Nom.count()
        nbr_va_sur_perf = data[data["Mesures"]>1000].Nom.count()
        data = data[(data["Mesures"]<650)|(data['Mesures']>1000)]
        prenom = current_user.prenom
        nom = current_user.nom
        Date = date.today()

    except:
        flash('Aucun fichier ou format non compatible','warning')

    analyse_variation = Enregistrement_AV.query.filter_by(reference_av=reference).first()
    if not analyse_variation:
        for i in range(data.shape[0]):
            #print(reference, data.index[i])
            valeur_aberante = ValeursAberrante(reference, data['Nom'][data.index[i]], data['Mesures'][data.index[i]])
            db.session.add(valeur_aberante)
            db.session.commit()
        av = Enregistrement_AV(prenom +' '+ nom, reference, '', Date, 'Statut en cour','')
        db.session.add(av)
        db.session.commit()

    if request.method=='POST':
        libelle = request.form['libelle']
        statut = request.form['statut']
        print(analyse_variation.agent)
        analyse_variation.agent = prenom +' '+ nom
        analyse_variation.reference_av = reference
        analyse_variation.libelle_av = libelle
        analyse_variation.date = Date
        analyse_variation.statut_analyse = statut
        db.session.commit()
        return redirect(url_for('listeVa', ref=reference)) 
    try:
        return render_template('synthese-av.html', ref=reference, prenom=prenom, Date=Date, nom=nom, nbr_va_sou_perf=nbr_va_sou_perf, nbr_va_sur_perf=nbr_va_sur_perf)  
    except:
        return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file () : 
    try:
        filename = filedialog.askopenfilename(initialdir='/home', title="Selectionner le fichier",
                                            filetypes=(("Tous les fichiers","*.*"), ("Fichier texte","*.txt"), ("Fichier excel","*.xsl")))

        #flash("Fichier charge avec succes ! ")
        return redirect(url_for('synthese_av', filename=filename))
    except:
        flash('Erreur de chargement du fichier ','danger')
    #abort(404)

@app.route("/action_programme")
@login_required
def action_programme():
    return render_template('action_programme.html')


if __name__=='__main__':
    app.run()