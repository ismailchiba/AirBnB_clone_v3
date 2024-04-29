#!/usr/bin/python3
"""
This  Module is a subclass of BaseModel
It is used to represent a user
It holds class User
holds class User
"""

import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model 


class User(BaseModel, Base):
    """This is the class representation of a user
    It holds the user information
    Representation of a user
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
        """This method
        initializes user
        """
        super().__init__(*args, **kwargs)
