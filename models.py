from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()



class User(UserMixin, db.Model):
    
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(256), index=True, unique=True)
    firstname = db.Column(db.String(255))
    lastname= db.Column(db.String(255))
    datecreated = db.Column(db.Integer)
    password = db.Column(db.String(255))
    datemodified = db.Column(db.Integer)
    lastlogin = db.Column(db.Integer)
    userlevel = db.Column(db.Integer)
    accountstatus = db.Column(db.Integer)
    authtoken = db.Column(db.String(255))
    resettoken = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id_user)