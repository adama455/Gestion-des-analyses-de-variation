from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from analyseVariation.forms import  RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '7540d096a1af7602423becbadf2f2df8'

#la racine ou page connexion des utilisateurs
@app.route('/')
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)    

#La page acceuil de notre application
@app.route("/home")
def home():
    form = RegistrationForm()
   
    return render_template('home.html', title='Régister', form=form)    

#Cette page permet a l'administrateur d'ajouter de users
@app.route("/addUser")
def addUser():
    form = RegistrationForm()
    return render_template('add-user.html', title='Régister', form=form)    

#C'est ici que le changement de mot de passe est effectuer pour les utilisateurs
@app.route("/change-password")
def changepassword():
    
    return render_template('changepassword.html')    

#Permet a l'admin de visualiser la liste des Utilisateurs
@app.route("/compte")
def compte():
     return render_template('comptes.html')  

#Permet a tout utilisateur de verifier son profil
@app.route("/profil")
def profil():
    return render_template('profil.html')    

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