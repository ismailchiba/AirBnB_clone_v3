#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5  # Import MD5 for password hashing

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
        if kwargs.get('password'):
            # Hash the password using MD5 if it's provided
            kwargs['password'] = md5(kwargs['password'].encode()).hexdigest()
        super().__init__(*args, **kwargs)

    def to_dict(self, include_password=False):
        """returns a dictionary representation of the User instance"""
        # Call the parent class's to_dict method
        user_dict = super().to_dict()

        # Exclude password unless include_password is True or storage_t is not db
        if not include_password and models.storage_t == 'db':
            user_dict.pop('password', None)

        return user_dict
