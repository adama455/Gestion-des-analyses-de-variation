from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from analyseVariation.models import User



class RegistrationForm(FlaskForm):
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=20)  ])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=20) ])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20) ])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    profil = StringField('Profile', validators=[DataRequired()])
    # plateau_id = StringField('Plateau', validators=[DataRequired()])
    # plateau_id = (db.Integer, db.ForeignKey('plateaux.id'))
    
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Valider')
  

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Connexion')
  
class CausesForm(FlaskForm):
    libelle = StringField('Libellé', validators=[DataRequired(), Length(min=5, max=200)  ])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)  ])
      
    submit = SubmitField('Valider')

class PlateauForm(FlaskForm):
    libelle = StringField('Libellé', validators=[DataRequired(), Length(min=5, max=200)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    univers = StringField('Univers', validators=[DataRequired()])
    
      
    submit = SubmitField('Valider')
    

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')