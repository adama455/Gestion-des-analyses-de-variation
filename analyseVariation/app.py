# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
sys.path.append('..')
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm
from analyseVariation.models import User
from analyseVariation import app, db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
import os
from tkinter import filedialog
from tkinter import *
from openpyxl import load_workbook
import csv
from threading import Thread
import pandas as pd



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
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
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
@app.route("/compte", methods=('GET', 'POST'))
@login_required 
def compte():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method=='POST':
            password = 'Sovar@2023'
            print('test ', form.prenom.data)
            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
            user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data, hashed_password)
            print(user)
            db.session.add(user)
            db.session.commit()
            flash('Votre compte a été bien créé','success')
            return redirect(url_for('compte'))
            
    users = User.query.all() #Récuperation de l'enssemble des utilisateurs::
    return render_template('comptes.html', title='Register', form=form, data=users) 

#Cette page permet voir les détail d'un Utilisateur
@app.route("/editUser", methods=['GET', 'POST'])
@login_required
def editUser():

    if request.method =='POST':
        data = User.query.get(request.form.get('id'))
        data.username = request.form['username']
        data.prenom = request.form['prenom']
        data.nom = request.form['nom']
        data.email = request.form['email']
    
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
 
#Permet de visualiser la liste des Analyses de Variation
@app.route("/listeAv")
@login_required
def listeAv():
    form = LoginForm()

    return render_template('listeAv.html', title='Register', form=form)  
 
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
@app.route("/listeVa")
@login_required
def listeVa():
    form = RegistrationForm()
    return render_template('listeVa.html',title='liste VA', form=form)  
 
 
#Permet d'enregistrer une cause
@app.route("/analyseCause")
@login_required
def analyseCause():
    form = RegistrationForm()
    return render_template('analyse-cause.html',title='Analyse Cause', form=form)  
 
#Permet de Méttre à jours une action:::::::::::::::::
@app.route("/miseAjourAc")
@login_required
def miseAjourAc():
    form = RegistrationForm()
    return render_template('mise-a-jour-action.html',title='Analyse Cause', form=form)  
 
#Permet de Méttre à jours une action:::::::::::::::::
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

    return render_template('profil.html',title='Analyse Cause', form=form)    

#enregistrement d'une AV par le MO
@app.route("/analyse_agent")
@login_required
def analyse_agent():
    
    return render_template('analyse-agent.html')    

#Analyse des causes par le MO
@app.route("/cause")
@login_required
def cause():
    
    return render_template('causes.html')    


@app.route("/demarrer-av")
@login_required
def demarrerav():
   
    return render_template('demarrer-av.html')    

@app.route("/logout")
def logout():
    logout_user()
    return redirect('login')    

@app.route("/synthese-av", methods=['POST', 'GET'])
def synthese_av():
    fichier = request.args.get('filename')
    if fichier :
        data = pd.read_excel(fichier)
        mesures = data.Mesures.dropna()
        data = data.dropna()
        data['Mesures'] = pd.to_numeric(data['Mesures'], errors='coerce')
        #data['Mesures'] = data['Mesures'].apply(lambda x : float(x[:]))
        max = pd.to_numeric(mesures, errors='coerce').max()
        min = pd.to_numeric(mesures, errors='coerce').min()
        nbr_va_sou_perf = data[data["Mesures"]<650].Nom.count()
        nbr_va_sur_perf = data[data["Mesures"]>1000].Nom.count()
        print(nbr_va_sou_perf)
        prenom = current_user.prenom
        nom = current_user.nom
        print(prenom)
        print(nom)
        #print("Voici votre fichier :",fichier)
        
        #print(nbr_va_sou_perf)
        return render_template('synthese-av.html', data=data, prenom=prenom, nom=nom, nbr_va_sou_perf=nbr_va_sou_perf, nbr_va_sur_perf=nbr_va_sur_perf)  
    if request.method=='POST':
        return redirect(url_for('listeVa'))  
    return render_template('synthese-av.html')


@app.route('/uploader', methods = ['GET', 'POST']) 
def upload_file () : 
    filename = filedialog.askopenfilename(initialdir='/home', title="Selectionner le fichier",
                                        filetypes=(("Fichier texte","*.txt"), ("Fichier excel","*.xsl"),("Tous les fichiers","*.*")))
        
    #print(filename )
    #os.popen(filename)
    #with open(filename, "r", encoding='latin-1') as file:
    #        myReader = csv.reader(file)
    #        for line in myReader:
    #            print(line)

    return redirect(url_for('synthese_av', filename=filename))


if __name__=='__main__':
    app.run()