from .. import db, flask_bcrypt
import datetime
# from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union


class Book(db.Model):
    """ book Model for storing book related details """
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_in_lib = db.Column(db.Boolean, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    date_borrowed = db.Column(db.DateTime, nullable=True)
    bookname = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    
    

    
    
    

    def __repr__(self):
        return "<book '{}'>".format(self.bookname)