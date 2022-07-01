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


    
class PaginatedAPIMixin(object):
    @staticmethod
    def colAPI(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data



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

class Client(PaginatedAPIMixin,db.Model):
    __tablename__= 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True)
    firstName = db.Column(db.String(64))
    lastName = db.Column(db.String(64))
    nip = db.Column(db.String(10))
    balance = db.Column(db.Integer)
    startDate = db.Column(db.Date)
    ordered = relationship("Order", backref = 'client', lazy='dynamic')
    phoneNumber = db.Column(db.String(12))
    email = db.Column(db.String(120), index=True, unique=True)

    def __str__(self):
        return self.name  # value string

    def getOrdered(self):
        return self.ordered.all()


    def to_dict(self):
        data = {
            'id':self.id,
            'name':self.name,
            'firstName':self.firstName,
            'lastName':self.lastName,
            'nip':self.nip,
            'balance':self.balance,
            'start':self.startDate,
            'phoneNumber':self.phoneNumber,
            'email':self.email
        }
        return data

    

class StatusesEnum(enum.Enum):
    s1 = 'Przyjete'
    s2 = 'Outsourcowane'
    s3 = 'Komplikacje'
    s4 = 'Wykonane'
    s5 = 'Oddane'
    s0 = ''

    def __str__(self):
        return str(self.value)  # value string

class Order(PaginatedAPIMixin,db.Model):


    __tablename__= 'order'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    startDate = db.Column(db.Date)
    returnDate = db.Column(db.Date)
    subject = db.Column(db.String(128), index = True)
    description = db.Column(db.String(256))
    comment = db.Column(db.String(256))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    #client = relationship("Client", back_populates="ordered")
    status = db.Column(Enum(StatusesEnum))
    locked = db.Column(db.Boolean, default = False)

    def __str__(self):
        return self.subject  # value string

    def to_dict(self):
        data = {
            'id':self.id,
            'price':self.price,
            'startDate':self.startDate,
            'returnDate':self.returnDate,
            'subject':self.subject,
            'description':self.description,
            'comment':self.comment,
            'client_id':self.client_id,
            'status':{
                'name':self.status.name,
                'value':self.status.value
            }
        }
        return data
        
    def colAPI(query,page,per_page,endpoint, **kwargs):
            resources = query.paginate(page,per_page,False)
            data = {
                '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            'orders' : [res.to_dict() for res in resources.items],
            '_links':{
                'self': url_for(endpoint,page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint,page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint,page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None                
            }
            }
            return data
