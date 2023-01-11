# # from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# # from analyseVariation.models import User



class RegistrationForm(FlaskForm):
    prenom = StringField('prenom', validators=[DataRequired(), Length(min=2, max=20)  ])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=20) ])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    profile = StringField('Profile', validators=[])

    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Valider')
  

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Connexion')
  