import sys
import jwt
import os
from time import time
sys.path.append('.')
sys.path.append('..')
# from sqlalchemy import Boolean, Column, String, Integer
from flask import current_app, request #<---HERE
from analyseVariation import db, init_base, login_manager,app
from analyseVariation.enregistrement_AV_model import Enregistrement_AV
from analyseVariation.pourquoi_model import Pourquoi1,Pourquoi2,Pourquoi3,Pourquoi4,Pourquoi5
from sqlalchemy.orm import *
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class AnalyseApporter(db.Model):
    __tablename__='apporter_analyse'
    id = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(255), unique=True, nullable=False)
    # valeur = db.Column(db.String(255), unique=True, nullable=False)
    famille_causes = db.Column(db.String(500))
    probleme = db.Column(db.String(100))
    pourquoi_1 = db.Column(db.String(300))
    pourquoi_2 = db.Column(db.String(500))
    pourquoi_3 = db.Column(db.String(500))
    pourquoi_4 = db.Column(db.String(500))
    pourquoi_5 = db.Column(db.String(500))

    def __init__(self, identifiant, famille_causes, probleme, pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5):
        self.identifiant = identifiant
        # self.valeur = valeur
        self.famille_causes = famille_causes
        self.probleme = probleme
        self.pourquoi_1 = pourquoi_1
        self.pourquoi_2 = pourquoi_2
        self.pourquoi_3 = pourquoi_3
        self.pourquoi_4 = pourquoi_4
        self.pourquoi_5 = pourquoi_5

    def traitement_data_analyse_apporter(datacc):
        car_exclu = ['2.', '1.', '3.', '4.','5.','6.','7.','8.','9.','10.']
        axes_analyse = [ elem for elem in datacc.famille_causes.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_1 = [ elem for elem in datacc.pourquoi_1.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_2 = [ elem for elem in datacc.pourquoi_2.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_3 = [ elem for elem in datacc.pourquoi_3.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_4 = [ elem for elem in datacc.pourquoi_4.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_5 = [ elem for elem in datacc.pourquoi_5.split('_/_') if not [el for el in car_exclu if el==elem]]
        liste_pourquoi = [pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5, axes_analyse]
        nbre_pourquoi = [len(pourquoi_1), len(pourquoi_2), len(pourquoi_3), len(pourquoi_4), len(pourquoi_5)]

        return liste_pourquoi, nbre_pourquoi
    
    def traitement_data_pourquoi(id, datacc):
        car_exclu = ['2.', '1.', '3.', '4.','5.','6.','7.','8.','9.','10.']
        print('test id',id)
        axes_analyse = [ elem for elem in datacc.famille_causes.split('_/_') if not [el for el in car_exclu if el==elem]]
        pourquoi_1 = [ elem.details for elem in Pourquoi1.query.filter_by(id_valeur_aberrante=id).all()]
        pourquoi_2 = [ elem.details for elem in Pourquoi2.query.filter_by(id_valeur_aberrante=id).all()]
        pourquoi_3 = [ elem.details for elem in Pourquoi3.query.filter_by(id_valeur_aberrante=id).all()]
        pourquoi_4 = [ elem.details for elem in Pourquoi4.query.filter_by(id_valeur_aberrante=id).all()]
        pourquoi_5 = [ elem.details for elem in Pourquoi5.query.filter_by(id_valeur_aberrante=id).all()]
        liste_pourquoi = [pourquoi_1, pourquoi_2, pourquoi_3, pourquoi_4, pourquoi_5, axes_analyse]
        nbre_pourquoi = [len(pourquoi_1), len(pourquoi_2), len(pourquoi_3), len(pourquoi_4), len(pourquoi_5)]
        print(pourquoi_1)

        return liste_pourquoi, nbre_pourquoi

    def insert_update_pourquoi(id, datacc,reference):
        try:
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
            if not datacc:
                pourquoi = AnalyseApporter(id, axes_analyse, probleme, pourquoi1, pourquoi21+pourquoi22, pourquoi31+pourquoi32, pourquoi41+pourquoi42, pourquoi51+pourquoi52)
                print('lamine',pourquoi)
                db.session.add(pourquoi)
                db.session.commit()
            else:
                # AnalyseApporter.update_pourquoi(datacc,axes_analyse, probleme, pourquoi1, pourquoi21+pourquoi22,pourquoi31+pourquoi32, pourquoi41+pourquoi42, pourquoi51+pourquoi52)
                Enregistrement_AV.query.filter_by(reference_av=reference).first().libelle_av = request.form['libelle_av']
                datacc.famille_causes = axes_analyse
                datacc.probleme = probleme
                datacc.pourquoi_1 = pourquoi1
                datacc.pourquoi_2 = pourquoi21+pourquoi22
                datacc.pourquoi_3 = pourquoi31+pourquoi32
                datacc.pourquoi_4 = pourquoi41+pourquoi42
                datacc.pourquoi_5 = pourquoi51+pourquoi52
                db.session.commit()
        except:
            print("Quelque chose s'est mal passer")

init_base()