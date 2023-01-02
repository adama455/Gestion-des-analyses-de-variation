from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#la racine ou page connexion des utilisateurs
@app.route('/')
@app.route("/login")
def login():
    
    return render_template('login.html')    

#La page acceuil de notre application
@app.route("/home")
def home():
   
    return render_template('home.html')    

#Cette page permet a l'administrateur d'ajouter de users
@app.route("/addUser")
def addUser():
    
    return render_template('add-user.html')    

#C'est ici que le changement de mot de passe est effectuer pour les utilisateurs
@app.route("/change-password")
def changepassword():
    
    return render_template('changepassword.html')    

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



@app.route("/index")
def index():
   
    return render_template('index.html')    

@app.route("/page-signup")
def signup():
   
    return render_template('page-signup.html')    

@app.route("/connexion")
def connexion():
   
    return render_template('page-connections.html')    



if __name__=='__main__':
    app.run()