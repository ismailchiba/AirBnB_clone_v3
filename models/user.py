#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib

class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            kwargs['password'] = self.generate_password_hash(kwargs['password'])
        super().__init__(*args, **kwargs)

    def generate_password_hash(self, password):
        salt = hashlib.new('md5', str(random.random()).encode()).hexdigest()
        return hashlib.md5(salt.encode() + password.encode()).hexdigest()

    def check_password(self, password):
        return self.generate_password_hash(password) == self.password
