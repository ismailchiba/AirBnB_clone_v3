#!/usr/bin/python3

"""
This is the user module.
It contains the User class that inherits from BaseModel
It does the following:
- creates a relationship with the Place class
- creates a relationship with the Review class
- creates a getter attribute reviews that returns the list of Review instances
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    This is the User class
    Representation of a user
    It contains the following attributes:
    - email: string - empty string
    - password: string - empty string
    - first_name: string - empty string
    """
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
        """
        This is the initialization of the User class
        initializes user"""
        super().__init__(*args, **kwargs)
