from enum import unique
from typing import NamedTuple
from blog import db,login_manager
from datetime import datetime



from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column('isim',db.String,nullable=False,unique=True)
    email = db.Column('mail',db.String,nullable=False,unique=True)
    password = db.Column('password',db.String,nullable=False)
    is_admin = db.Column(db.Boolean,default=False)
    posts = db.relationship('Urun', backref='user', lazy=True)


    def __init__(self,name,password,email,admin):
        self.username = name
        self.password = password
        self.email = email
        self.is_admin = admin
    def __repr__(self):
        return f"User:{self.username} Email:{self.email}"


   


class Urun(db.Model):
    __tablename__  = "Urunler"
    id = db.Column(db.Integer,primary_key=True)
    urun_kodu = db.Column('urun_kodu',db.String,nullable=False, unique=True)
    cikis_tarihi = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'),nullable=False)
    status = db.relationship('Status',
        backref=db.backref('durum', lazy=True))
    
    def __init__(self,urun,user,status):
        self.urun_kodu = urun
        self.user = user
        self.status_id = status
   
    def __repr__(self):
        return str(self.status)

  

       

class Status(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   status_name = db.Column(db.String,nullable=False)


   def __repr__(self):
        return str(self.id)

