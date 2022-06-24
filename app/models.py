from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from hashlib import md5
from flask_migrate import Migrate
from sqlalchemy.orm import declarative_base, relationship
import enum
from sqlalchemy import Enum


class User(UserMixin,db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permissionLevel = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Client(db.Model):
    __tablename__= 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True)
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    nip = db.Column(db.String(10))
    balance = db.Column(db.Numeric(10,2))
    startDate = db.Column(db.Date)
    ordered = relationship("Order", back_populates = 'client', lazy='dynamic')
    phoneNumber = db.Column(db.String(12))
    email = db.Column(db.String(120), index=True, unique=True)

    def __str__(self):
        return self.name  # value string

class StatusesEnum(enum.Enum):
    s1 = 'Przyjete'
    s2 = 'Outsourcowane'
    s3 = 'Komplikacje'
    s4 = 'Wykonane'
    s5 = 'Oddane'

    def __str__(self):
        return str(self.value)  # value string

    #def __html__(self):
    #    return self.value  # label string

#def coerce_for_enum(enum):
#    def coerce(name):
#        if isinstance(name, enum):
#            return name
#        try:
#            return enum[name]
#        except KeyError:
#            raise ValueError(name)
#    return coerce
    

class Order(db.Model):
    __tablename__= 'order'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10,2))
    startDate = db.Column(db.Date)
    returnDate = db.Column(db.Date)
    subject = db.Column(db.String(128), index = True)
    description = db.Column(db.String(256))
    comment = db.Column(db.String(256))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = relationship("Client", back_populates="ordered")
    status = db.Column(Enum(StatusesEnum))



    


