from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm
from analyseVariation import  app, db
from analyseVariation.models import User

#from config import get_config

# app = Flask(__name__)

# app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'


#La page acceuil de notre application
@app.route("/home")
def home():
    form = RegistrationForm()
   
    return render_template('home.html', title='Régister', form=form)    

#Cette page permet a l'administrateur d'ajouter de users
@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                prenom=form.prenom.data,
                nom=form.nom.data,
                username=form.username.data,
                email=form.email.data
                    )
            db.session.add(user)
            db.session.commit()
            flash('Votre compte a été créé avec succès!')
            return redirect(url_for('login'))
    
    return render_template('add-user.html', title='Register', form=form)    

#la racine ou page connexion des utilisateurs
@app.route('/')
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)    


#C'est ici que le changement de mot de passe est effectuer pour les utilisateurs
@app.route("/change-password")
def changepassword():
    
    return render_template('changepassword.html')    

#Permet a l'admin de visualiser la liste des Utilisateurs
@app.route("/compte", methods=['GET', 'POST'])
def compte():
    form = RegistrationForm()
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
@app.route("/profil")
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