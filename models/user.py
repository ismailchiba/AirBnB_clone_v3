#!/usr/bin/python3
"""
User Class from Models Module
"""
import os
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from hashlib import md5

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

class User(BaseModel):
    """User class handles all application users"""
    if storage_type == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password_hash = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        def __init__(self, *args, **kwargs):
            """
            Initialize User Model, inherits from BaseModel
            """
            super().__init__(*args, **kwargs)
            self.email = ''
            self.password_hash = ''
            self.first_name = ''
            self.last_name = ''

    @property
    def password(self):
        """
        Getter for password
        :return: password (hashed)
        """
        return self.password_hash

    @password.setter
    def password(self, password):
        """
        Password setter, with md5 hashing
        :param password: password
        :return: nothing
        """
        self.password_hash = md5(password.encode('utf-8')).hexdigest()
