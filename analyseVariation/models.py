# from sqlalchemy import Boolean, Column,String,Integer
# import base
# from sqlalchemy.orm import *

# db= base.db

# class User(db.Model):
#     __tablename__='users'
#     id=db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String(50))
#     username=db.Column(db.String(50))
#     email=db.Column(db.String(50))

#     def __init__(self,id,name,username,email):
#         self.id=id
#         self.name=name
#         self.username=username
#         self.email=email
               
# base.init_base()