import sys
sys.path.append('.')
sys.path.append('..')
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm
from analyseVariation.models import User
from analyseVariation import app, db

#app = Flask(__name__)

#app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'

#la racine ou page connexion des utilisateurs

@app.route('/', methods=('GET', 'POST'))
@app.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method=='POST':
        print(form.email.data)
        data = User.query.filter_by(username=form.email.data).first()
        #data = User.query.all()
        print(data.username)
        if data.password==form.password.data:
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)    

#La page acceuil de notre application
@app.route("/home")
def home():
    form = RegistrationForm()
   
    return render_template('home.html', title='Régister', form=form)    

#Cette page permet a l'administrateur d'ajouter de users
@app.route("/addUser", methods=('GET', 'POST'))
def addUser():
    form = RegistrationForm()
    if request.method=='POST':
        prenom=request.args.get('prenom')
        print('test ', form.prenom.data)
        #if form.validate_on_submit():
        user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        #flash('Votre compte a été bien créé')

        return redirect(url_for('login'))
    return render_template('add-user.html', title='Register', form=form)    

#C'est ici que le changement de mot de passe est effectuer pour les utilisateurs
@app.route("/change-password")
def changepassword():
    
    return render_template('changepassword.html')    

#Permet a l'admin de visualiser la liste des Utilisateurs
@app.route("/compte", methods=('GET', 'POST'))
def compte():
    form = RegistrationForm()
    if request.method=='POST':
        print('test ', form.prenom.data)
        #if form.validate_on_submit():
        user = User(form.nom.data, form.prenom.data, form.username.data, form.email.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été bien créé')
        return redirect(url_for('compte'))
    return render_template('comptes.html', title='Register', form=form) 
 
 
#Permet de visualiser la liste des Analyses de Variation
@app.route("/listeAv")
def listeAv():
    form = LoginForm()

    return render_template('listeAv.html', title='Register', form=form)  
 
@app.route("/listepa")
def listepa():
    form = LoginForm()
    return render_template('listepa.html', title='Register', form=form)  
 
@app.route("/editpa")
def editpa():
    form = LoginForm()
    return render_template('editpa.html', title='Register', form=form)  
 
 
#Permet de visualiser la liste des Valeurs Aberantes
@app.route("/listeVa")
def listeVa():
    form = RegistrationForm()
    return render_template('listeVa.html',title='liste VA', form=form)  
 
 
#Permet d'enregistrer une cause
@app.route("/analyseCause")
def analyseCause():
    form = RegistrationForm()
    return render_template('analyse-cause.html',title='Analyse Cause', form=form)  
 
#Permet de Méttre à jours une action:::::::::::::::::
@app.route("/miseAjourAc")
def miseAjourAc():
    form = RegistrationForm()
    return render_template('mise-a-jour-action.html',title='Analyse Cause', form=form)  
 
#Permet de Méttre à jours une action:::::::::::::::::
@app.route("/rejeterAv")
def rejeterAv():
    form = RegistrationForm()
    return render_template('rejeterAv.html',title='Analyse Cause', form=form)  
 
 
#Permet a tout utilisateur de verifier son profil
@app.route("/profil", methods=('GET', 'POST'))
def profil():
    form = RegistrationForm()

    return render_template('profil.html',title='Analyse Cause', form=form)    

#enregistrement d'une AV par le MO
@app.route("/analyse_agent")
def analyse_agent():
    
    return render_template('analyse-agent.html')    

#Analyse des causes par le MO
@app.route("/cause")
def cause():
    
    return render_template('causes.html')    


@app.route("/demarrer-av")
def demarrerav():
   
    return render_template('demarrer-av.html')    

@app.route("/page-signup")
def signup():
   
    return render_template('page-signup.html')    

@app.route("/connexion")
def connexion():
   
    return render_template('page-connections.html')    



if __name__=='__main__':
    app.run()